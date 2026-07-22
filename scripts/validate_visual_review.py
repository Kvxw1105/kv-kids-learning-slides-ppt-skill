#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    p = argparse.ArgumentParser(description="Validate a completed agent visual-review report")
    p.add_argument("report")
    p.add_argument("--pptx", required=True)
    args = p.parse_args()

    report_path = Path(args.report)
    pptx = Path(args.pptx)
    errors = []
    warnings = []
    if not report_path.exists():
        errors.append("visual review report not found")
        data = {}
    else:
        try:
            data = json.loads(report_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid visual review JSON: {exc}")
            data = {}
    if not pptx.exists():
        errors.append("PPTX not found")
    elif data.get("pptx_sha256") != sha256_file(pptx):
        errors.append("visual review is bound to a different PPTX hash")

    slides = data.get("slides") or []
    if not slides:
        errors.append("visual review contains no slides")
    for item in slides:
        slide = item.get("slide")
        status = str(item.get("status", "PENDING")).upper()
        if status in {"PENDING", "", "NOT_REVIEWED"}:
            errors.append(f"slide {slide} has not been visually reviewed")
        elif status == "BLOCKED":
            errors.append(f"slide {slide} is visually blocked: {item.get('issues') or item.get('notes') or 'unspecified issue'}")
        elif status == "WARN":
            warnings.append(f"slide {slide} visual warning: {item.get('issues') or item.get('notes') or 'unspecified warning'}")
        elif status != "PASS":
            errors.append(f"slide {slide} has invalid review status {status}")
        image = Path(str(item.get("image", "")))
        if not image.exists():
            errors.append(f"slide {slide} review image is missing")

    result = {
        "status": "PASS" if not errors else "BLOCKED",
        "pptx_sha256": sha256_file(pptx) if pptx.exists() else None,
        "reviewed_slides": len(slides),
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
