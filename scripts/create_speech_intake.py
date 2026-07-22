#!/usr/bin/env python3
"""Create a compact intake question and default speech_profile for child speeches."""
from __future__ import annotations
import argparse, json

PROFILES = {
    "light": {
        "difficulty": "light",
        "target_duration_seconds": 75,
        "target_english_words": [45, 70],
        "screen_density": "short_cues",
        "script_density": "simple",
        "label": "轻量版: 60-90 秒, 英文约 45-70 词, 句子很短",
    },
    "standard": {
        "difficulty": "standard",
        "target_duration_seconds": 100,
        "target_english_words": [70, 110],
        "screen_density": "short_cues",
        "script_density": "moderate",
        "label": "标准版: 90-120 秒, 英文约 70-110 词, 适合幼儿园展示",
    },
    "rich": {
        "difficulty": "rich",
        "target_duration_seconds": 150,
        "target_english_words": [110, 180],
        "screen_density": "short_cues",
        "script_density": "rich",
        "label": "丰富版: 2-3 分钟, 英文约 110-180 词, 表达更完整但仍幼儿可背",
    },
}

QUESTION = "先确认演讲难度和长度,这样我不会把内容写得太少或太难。请选择 light / standard / rich,也可以直接给目标词数或比赛时长。"

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--difficulty", choices=sorted(PROFILES), default="standard")
    parser.add_argument("--target-words", type=str, help="single number or range like 80-120")
    parser.add_argument("--duration", type=int, help="target speech duration in seconds")
    args = parser.parse_args()
    profile = dict(PROFILES[args.difficulty])
    if args.target_words:
        raw = args.target_words.replace("–", "-").replace("—", "-")
        if "-" in raw:
            lo, hi = [int(x.strip()) for x in raw.split("-", 1)]
        else:
            mid = int(raw.strip())
            lo, hi = max(1, int(mid * 0.85)), int(mid * 1.15)
        profile["target_english_words"] = [lo, hi]
    if args.duration:
        profile["target_duration_seconds"] = args.duration
    print(json.dumps({"question": QUESTION, "options": PROFILES, "selected_profile": profile}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
