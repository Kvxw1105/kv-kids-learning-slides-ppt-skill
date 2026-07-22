#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Query registered child slide layouts")
    parser.add_argument("--role")
    parser.add_argument("--age")
    parser.add_argument("--visual")
    parser.add_argument("--usage", help="usage mode, e.g. child_stage_speech")
    parser.add_argument("--keyword")
    parser.add_argument("--stage-safe", action="store_true")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    data = json.loads((ROOT / "assets/registries/layouts.json").read_text(encoding="utf-8"))
    output = []
    for item in data:
        if args.role and item.get("role") != args.role:
            continue
        if args.age and args.age not in item.get("age_bands", []):
            continue
        if args.visual and args.visual not in item.get("visual_systems", []):
            continue
        if args.usage and args.usage not in item.get("usage_modes", []):
            continue
        if args.stage_safe and not item.get("stage_safe", False):
            continue
        haystack = " ".join(
            [item.get("id", ""), item.get("role", ""), *item.get("best_for", [])]
        ).lower()
        if args.keyword and args.keyword.lower() not in haystack:
            continue
        output.append(item)

    print(json.dumps(output[: args.limit], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
