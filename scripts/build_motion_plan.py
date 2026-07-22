#!/usr/bin/env python3
"""Create a conservative child-stage motion plan sidecar from slide_spec.json."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec")
    parser.add_argument("--out", required=True)
    parser.add_argument("--mode", choices=["none", "gentle", "story-reveal"], default="gentle")
    args = parser.parse_args()
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    slides = []
    for slide in spec.get("slides", []):
        sid = slide.get("id", "S")
        objects = []
        if args.mode != "none":
            blocks = slide.get("screen", {}).get("text_blocks", [])
            if blocks:
                objects.append({"target": blocks[0].get("id", f"{sid}_Title"), "effect": "fade", "order": 1, "duration_ms": 450})
            if len(blocks) > 1:
                objects.append({"target": blocks[1].get("id", f"{sid}_Translation"), "effect": "fade", "order": 2, "duration_ms": 350})
            visual = slide.get("visual", {})
            if visual.get("asset_ids"):
                objects.append({"target": f"{sid}_Hero_Image", "effect": "float-up", "order": 1, "duration_ms": 550})
            for idx, component in enumerate(visual.get("component_plan", [])[:4], 1):
                objects.append({
                    "target": f"{sid}_{component.get('id', f'component_{idx:02d}')}",
                    "effect": "pop" if component.get("type") in {"star", "heart", "flower_sticker", "sparkle_cluster", "badge"} else "fade",
                    "order": 2 + idx,
                    "duration_ms": 260,
                })
        slides.append({"slide_id": sid, "transition": "fade" if args.mode != "none" else "none", "objects": objects})
    output = {"version": "0.6", "mode": args.mode, "safety": {"max_objects_per_slide": 6, "allowed_effects": ["fade", "float-up", "pop"]}, "slides": slides}
    Path(args.out).write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PASS", "slides": len(slides), "output": args.out}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
