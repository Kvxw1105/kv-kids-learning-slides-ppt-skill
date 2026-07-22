#!/usr/bin/env python3
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    p = argparse.ArgumentParser(description="Render a PPTX and prepare a per-slide visual-review manifest")
    p.add_argument("pptx")
    p.add_argument("--out-dir", default="visual_review")
    p.add_argument("--dpi", type=int, default=180)
    args = p.parse_args()

    pptx = Path(args.pptx).resolve()
    out = Path(args.out_dir).resolve()
    rendered = out / "rendered"
    out.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        [sys.executable, str(ROOT / "render_pptx.py"), str(pptx), "--out", str(rendered), "--dpi", str(args.dpi)],
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        print(completed.stderr or completed.stdout, file=sys.stderr)
        return completed.returncode

    images = sorted(rendered.glob("slide-*.png"))
    if not images:
        print("no rendered slide images found", file=sys.stderr)
        return 3
    contact = out / "contact_sheet.png"
    subprocess.run([sys.executable, str(ROOT / "make_contact_sheet.py"), str(rendered), str(contact)], check=True)

    report = {
        "status": "PENDING_REVIEW",
        "pptx": str(pptx),
        "pptx_sha256": sha256_file(pptx),
        "contact_sheet": str(contact),
        "review_instructions": [
            "Open the contact sheet first, then inspect any suspicious slide PNG at full size.",
            "Check text-line intersections, border clearance, font substitution, clipping, hierarchy, spacing, density, and visual focus.",
            "Set every slide status to PASS, WARN, or BLOCKED and record concrete issues.",
            "After any PPTX change, rerender and recreate this report; do not reuse old approval.",
        ],
        "slides": [
            {
                "slide": i,
                "image": str(image),
                "status": "PENDING",
                "issues": [],
                "notes": "",
            }
            for i, image in enumerate(images, 1)
        ],
    }
    report_path = out / "visual_review.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
