#!/usr/bin/env python3
import json
import sys
from pathlib import Path

REQUIRED_CLASSROOM = {"id", "role", "learning_goal", "screen", "visual", "teacher"}
REQUIRED_SPEECH = {"id", "role", "purpose", "screen", "visual", "speaker", "stage"}


def validate(data: dict) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    ids: set[str] = set()
    slides = data.get("slides", [])
    speech_mode = data.get("usage_mode") == "child_stage_speech" or data.get("route") == "create-child-speech-deck"
    required = REQUIRED_SPEECH if speech_mode else REQUIRED_CLASSROOM

    if not slides:
        errors.append("slides is empty")
    for index, slide in enumerate(slides, 1):
        for key in sorted(required - set(slide)):
            errors.append(f"slide {index} missing {key}")
        sid = slide.get("id")
        if sid in ids:
            errors.append(f"duplicate slide id {sid}")
        if sid:
            ids.add(sid)

        if speech_mode:
            blocks = slide.get("screen", {}).get("text_blocks", [])
            visible_text = " ".join(str(b.get("text", "")) for b in blocks)
            if len(visible_text) > 120:
                warnings.append(f"{sid}: speech screen may be dense ({len(visible_text)} chars)")
            if not slide.get("speaker", {}).get("script_en") and not slide.get("speaker", {}).get("script_zh"):
                warnings.append(f"{sid}: missing speaker script")
        else:
            screen = slide.get("screen", {})
            text = " ".join(str(screen.get(key, "")) for key in ("title", "body", "prompt"))
            if len(text) > 220:
                warnings.append(f"{sid}: screen text may be dense ({len(text)} chars)")
            if not slide.get("teacher", {}).get("script"):
                warnings.append(f"{sid}: missing teacher script")
            if slide.get("role") in {"practice", "assessment", "challenge"} and not slide.get("teacher", {}).get("expected_answer"):
                warnings.append(f"{sid}: practice/assessment missing expected answer")

    result = {
        "status": "PASS" if not errors else "BLOCKED",
        "profile": "child_stage_speech" if speech_mode else "classroom_learning",
        "slide_count": len(slides),
        "errors": errors,
        "warnings": warnings,
    }
    if speech_mode:
        try:
            from validate_speech_spec import validate as validate_speech
            speech = validate_speech(data)
            result["speech"] = speech
            if speech["status"] == "BLOCKED":
                result["status"] = "BLOCKED"
                result["errors"].extend(speech["errors"])
            result["warnings"].extend(speech["warnings"])
        except Exception as exc:
            result["status"] = "BLOCKED"
            result["errors"].append(f"speech validator failed: {exc}")
    return result


def main(path: str) -> int:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    result = validate(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
