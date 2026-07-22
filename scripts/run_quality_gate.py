#!/usr/bin/env python3
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(script: str, args: list[str]) -> dict:
    completed = subprocess.run(
        [sys.executable, str(ROOT / script), *args],
        capture_output=True,
        text=True,
    )
    try:
        return json.loads(completed.stdout)
    except Exception:
        return {
            "status": "BLOCKED",
            "errors": [completed.stderr.strip() or completed.stdout.strip() or f"{script} produced no JSON"],
            "warnings": [],
        }


def file_sha(path: str | None) -> str | None:
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    h = hashlib.sha256()
    with p.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def gate_status(*reports: dict) -> str:
    if any(report.get("status") == "BLOCKED" for report in reports if report):
        return "BLOCKED"
    if any(report.get("warnings") for report in reports if report):
        return "PASS_WITH_WARNINGS"
    return "PASS"


def composition_thresholds(spec_path: str) -> tuple[float, float, float]:
    try:
        spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    except Exception:
        return 0.28, 0.40, 0.44
    profile = spec.get("composition_profile", {}) or {}
    density = str(profile.get("density", "balanced"))
    defaults = {
        "light": (0.24, 0.34, 0.50),
        "balanced": (0.28, 0.40, 0.44),
        "rich": (0.34, 0.46, 0.38),
    }.get(density, (0.28, 0.40, 0.44))
    min_coverage = float(profile.get("min_coverage_ratio", defaults[0]))
    warn_coverage = float(profile.get("warn_coverage_ratio", defaults[1]))
    max_empty = float(profile.get("max_empty_region_ratio", defaults[2]))
    return min_coverage, warn_coverage, max_empty


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--visual")
    parser.add_argument("--pptx")
    parser.add_argument("--script-md")
    parser.add_argument("--script-docx")
    parser.add_argument("--profile", default="classroom_learning")
    parser.add_argument("--out", default="qa_report.json")
    parser.add_argument("--max-size-mb", type=float)
    parser.add_argument("--visual-review")
    parser.add_argument("--require-visual-review", action="store_true")
    args = parser.parse_args()

    spec_report = run("validate_slide_spec.py", [args.spec])
    visual_density_report = run("validate_visual_density.py", [args.spec])
    typography_report = run("validate_typography.py", [args.spec])
    storybook_report = run("validate_storybook_composition.py", [args.spec]) if args.profile == "child_stage_speech" else None
    visual_report = run("validate_visual_plan.py", [args.visual]) if args.visual else None
    character_report = run("validate_character_plan.py", [args.visual]) if args.visual else None
    pptx_args = [args.pptx, "--profile", args.profile] if args.pptx else []
    if args.pptx and args.profile == "child_stage_speech":
        min_coverage, warn_coverage, max_empty = composition_thresholds(args.spec)
        pptx_args += [
            "--min-coverage", str(min_coverage),
            "--warn-coverage", str(warn_coverage),
            "--max-empty-region", str(max_empty),
        ]
    if args.max_size_mb is not None:
        pptx_args += ["--max-size-mb", str(args.max_size_mb)]
    pptx_report = run("inspect_pptx.py", pptx_args) if args.pptx else None
    geometry_report = run("audit_pptx_geometry.py", [args.pptx, "--profile", args.profile]) if args.pptx else None
    if args.visual_review and args.pptx:
        visual_review_report = run("validate_visual_review.py", [args.visual_review, "--pptx", args.pptx])
    elif args.require_visual_review:
        visual_review_report = {"status": "BLOCKED", "errors": ["required visual review report was not provided"], "warnings": []}
    else:
        visual_review_report = {"status": "PASS", "errors": [], "warnings": ["rendered visual review was not provided"]} if args.pptx else None

    speech_report = None
    script_md_report = run("validate_speaker_script_md.py", [args.script_md]) if args.script_md else None
    script_docx_args = [args.script_docx] if args.script_docx else []
    if args.script_docx and args.script_md:
        script_docx_args += ["--markdown", args.script_md]
    script_docx_report = run("inspect_speaker_script_docx.py", script_docx_args) if args.script_docx else None
    if args.profile == "child_stage_speech":
        speech_report = run("validate_speech_spec.py", [args.spec])

    content_gate = gate_status(spec_report)
    scenario_gate = "PASS"
    age_gate = "PASS"
    speech_gate = "PASS"
    bilingual_gate = "PASS"
    if speech_report:
        gates = speech_report.get("gates", {})
        scenario_gate = gates.get("scenario_gate", {}).get("status", "BLOCKED")
        age_gate = gates.get("age_gate", {}).get("status", "BLOCKED")
        speech_gate = gates.get("speech_gate", {}).get("status", "BLOCKED")
        bilingual_gate = gates.get("bilingual_gate", {}).get("status", "BLOCKED")
        speech_profile_gate = gates.get("speech_profile_gate", {}).get("status", "BLOCKED")

    visual_gate = gate_status(*(report for report in [visual_density_report, typography_report, storybook_report, visual_report, character_report, visual_review_report] if report))
    engineering_gate = gate_status(*(report for report in [pptx_report, geometry_report] if report)) if (pptx_report or geometry_report) else "PASS_WITH_WARNINGS"
    script_gate = gate_status(*(report for report in [script_md_report, script_docx_report] if report)) if (script_md_report or script_docx_report) else ("PASS_WITH_WARNINGS" if args.profile == "child_stage_speech" else "PASS")

    gates = {
        "content_gate": content_gate,
        "scenario_gate": scenario_gate,
        "age_gate": age_gate,
        "speech_gate": speech_gate,
        "bilingual_gate": bilingual_gate,
        "speech_profile_gate": speech_profile_gate if speech_report else "PASS",
        "visual_gate": visual_gate,
        "engineering_gate": engineering_gate,
        "script_document_gate": script_gate,
    }
    release_status = "BLOCKED" if "BLOCKED" in gates.values() else (
        "PASS_WITH_WARNINGS" if "PASS_WITH_WARNINGS" in gates.values() else "PASS"
    )

    result = {
        "status": release_status,
        "release_status": release_status,
        "profile": args.profile,
        "artifact_bindings": {
            "spec_sha256": file_sha(args.spec),
            "visual_plan_sha256": file_sha(args.visual),
            "pptx_sha256": file_sha(args.pptx),
            "speaker_script_md_sha256": file_sha(args.script_md),
            "speaker_script_docx_sha256": file_sha(args.script_docx),
        },
        "gates": gates,
        "reports": {
            "slide_spec": spec_report,
            "visual_density": visual_density_report,
            "typography": typography_report,
            **({"storybook_composition": storybook_report} if storybook_report else {}),
            **({"speech": speech_report} if speech_report else {}),
            **({"visual_plan": visual_report} if visual_report else {}),
            **({"character_plan": character_report} if character_report else {}),
            **({"pptx": pptx_report} if pptx_report else {}),
            **({"pptx_geometry": geometry_report} if geometry_report else {}),
            **({"visual_review": visual_review_report} if visual_review_report else {}),
            **({"speaker_script_md": script_md_report} if script_md_report else {}),
            **({"speaker_script_docx": script_docx_report} if script_docx_report else {}),
        },
    }
    Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if release_status == "BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
