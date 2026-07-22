#!/usr/bin/env python3
"""Plan responsive, picture-book-inspired slide layouts.

The planner is deterministic and dependency-free. It borrows only general
architecture ideas from flexbox/constraint layout systems: content is measured,
classified, assigned to semantic zones, then optically corrected for a fixed
PowerPoint stage. It never copies upstream code.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path
from typing import Any

SLIDE_W = 13.333
SLIDE_H = 7.5

PLAYFUL_CONTAINERS = [
    "cloud_bubble",
    "speech_bubble",
    "scalloped_panel",
    "watercolor_blob",
    "leaf_label",
    "petal_cluster",
    "torn_paper",
]

ARCHETYPES: dict[str, dict[str, Any]] = {
    "full-bleed-caption-island": {
        "roles": {"cover", "closing"},
        "container": "scalloped_panel",
        "edge": "soft_full_bleed",
        "zones": {
            "hero": [6.15, 0.25, 6.85, 6.85],
            "text": [0.65, 0.72, 5.6, 4.35],
            "accent": [0.35, 5.4, 5.1, 1.35],
        },
    },
    "character-speech-cloud": {
        "roles": {"greeting", "self-introduction", "dialogue"},
        "container": "speech_bubble",
        "edge": "corner_garden",
        "zones": {
            "hero": [0.3, 0.45, 6.35, 6.35],
            "text": [6.55, 0.75, 6.15, 4.55],
            "accent": [7.0, 5.45, 4.8, 1.25],
        },
    },
    "wraparound-object-story": {
        "roles": {"object-introduction", "show-one-object", "description"},
        "container": "watercolor_blob",
        "edge": "botanical_wrap",
        "zones": {
            "hero": [0.45, 0.55, 6.15, 5.95],
            "text": [6.35, 0.82, 6.3, 3.85],
            "accent": [6.65, 4.9, 5.35, 1.55],
        },
    },
    "diagonal-action": {
        "roles": {"action", "one-action-one-line", "process"},
        "container": "speech_bubble",
        "edge": "diagonal_motion",
        "zones": {
            "hero": [0.25, 0.45, 7.4, 6.5],
            "text": [7.15, 0.75, 5.55, 3.7],
            "accent": [8.15, 4.75, 3.8, 1.45],
        },
    },
    "weather-triptych": {
        "roles": {"weather", "weather-pair", "compare"},
        "container": "leaf_label",
        "edge": "three_scene_strip",
        "zones": {
            "left": [0.45, 0.75, 3.65, 4.55],
            "center": [4.55, 0.55, 4.2, 5.1],
            "right": [9.15, 0.75, 3.65, 4.55],
            "text": [1.25, 5.35, 10.85, 1.35],
        },
    },
    "three-vignette-growth": {
        "roles": {"growth", "before-and-after", "sequence", "progress"},
        "container": "scalloped_panel",
        "edge": "vignette_ribbon",
        "zones": {
            "v1": [0.55, 1.0, 3.55, 4.35],
            "v2": [4.88, 0.65, 3.55, 4.7],
            "v3": [9.2, 0.35, 3.55, 5.0],
            "text": [1.05, 5.55, 11.2, 1.1],
        },
    },
    "emotion-closeup": {
        "roles": {"emotion", "emotion-moment", "reflection"},
        "container": "cloud_bubble",
        "edge": "heart_and_petals",
        "zones": {
            "hero": [5.0, 0.25, 7.85, 6.75],
            "text": [0.65, 0.85, 5.45, 4.3],
            "accent": [0.5, 5.2, 4.9, 1.55],
        },
    },
    "object-constellation": {
        "roles": {"keywords", "vocabulary", "features"},
        "container": "petal_cluster",
        "edge": "floating_labels",
        "zones": {
            "hero": [4.1, 0.75, 5.2, 5.55],
            "text": [0.55, 0.4, 4.2, 2.2],
            "accent": [0.45, 2.5, 12.25, 4.35],
        },
    },
    "picturebook-window": {
        "roles": {"default", "explanation", "story"},
        "container": "torn_paper",
        "edge": "framed_window",
        "zones": {
            "hero": [0.55, 0.55, 7.35, 6.2],
            "text": [7.55, 0.8, 5.2, 4.55],
            "accent": [8.15, 5.05, 3.95, 1.4],
        },
    },
}

ROLE_ALIASES = {
    "hello-and-wave": "greeting",
    "this-is-me": "self-introduction",
    "show-one-object": "object-introduction",
    "one-action-one-line": "action",
    "weather-pair": "weather",
    "before-and-after": "growth",
    "emotion-moment": "emotion",
    "simple-closing": "closing",
}


def word_units(text: str) -> int:
    return len(re.findall(r"[A-Za-z]+|[\u4e00-\u9fff]", text or ""))


def slide_word_units(slide: dict) -> int:
    return sum(word_units(str(block.get("text", ""))) for block in slide.get("screen", {}).get("text_blocks", []) or [])


def content_level(units: int) -> str:
    if units <= 10:
        return "sparse"
    if units <= 24:
        return "medium"
    return "rich"


def role_key(slide: dict) -> str:
    visual_layout = str(slide.get("visual", {}).get("layout", "")).strip()
    role = str(slide.get("role", "default")).strip()
    return ROLE_ALIASES.get(visual_layout, ROLE_ALIASES.get(role, role or "default"))


def choose_archetype(slide: dict, previous: str | None = None) -> str:
    role = role_key(slide)
    keyword_count = sum(1 for b in slide.get("screen", {}).get("text_blocks", []) or [] if b.get("role") in {"keyword", "label", "vocabulary"})
    if keyword_count >= 3:
        return "object-constellation"
    for name, item in ARCHETYPES.items():
        if role in item["roles"]:
            return name
    return "picturebook-window"


def mirrored(zones: dict[str, list[float]]) -> dict[str, list[float]]:
    out: dict[str, list[float]] = {}
    for key, box in zones.items():
        x, y, w, h = box
        out[key] = [round(SLIDE_W - x - w, 3), y, w, h]
    return out


def recommended_scale(level: str, density: str) -> tuple[float, float, float]:
    hero = {"sparse": 0.48, "medium": 0.40, "rich": 0.33}[level]
    text = {"sparse": 1.20, "medium": 1.05, "rich": 0.95}[level]
    coverage = {"light": 0.43, "balanced": 0.53, "rich": 0.62}.get(density, 0.53)
    return hero, text, coverage


def plan_slide(slide: dict, index: int, density: str, previous_archetype: str | None) -> dict:
    units = slide_word_units(slide)
    level = content_level(units)
    archetype = choose_archetype(slide, previous_archetype)
    base = ARCHETYPES[archetype]
    zones = copy.deepcopy(base["zones"])
    # Alternate visual direction to avoid mechanically repeated left/right pages.
    if index % 2 == 0 and archetype in {"character-speech-cloud", "wraparound-object-story", "emotion-closeup", "picturebook-window"}:
        zones = mirrored(zones)
    hero_scale, text_scale, coverage = recommended_scale(level, density)
    blocks = slide.get("screen", {}).get("text_blocks", []) or []
    keywords = [b for b in blocks if b.get("role") in {"keyword", "label", "vocabulary"}]
    pair_groups = []
    by_lang = {"en": [], "zh": []}
    for block in blocks:
        by_lang.setdefault(str(block.get("lang", "other")), []).append(block.get("id"))
    if by_lang.get("en") and by_lang.get("zh"):
        pair_groups.append({"id": f"{slide.get('id', f'S{index:02d}')}_bilingual_pair", "en": by_lang["en"], "zh": by_lang["zh"]})
    return {
        "engine": "storybook-responsive-v1",
        "archetype": archetype,
        "content_level": level,
        "word_units": units,
        "density": density,
        "zones": zones,
        "text_container_style": base["container"],
        "edge_treatment": base["edge"],
        "hero_scale_ratio": hero_scale,
        "text_scale_ratio": text_scale,
        "target_coverage_ratio": coverage,
        "max_empty_region_ratio": 0.34 if density == "rich" else 0.40,
        "optical_corrections": [
            "prefer optical centering over mathematical centering",
            "let one focal element cross a zone boundary by 3-8%",
            "keep bilingual lines as one visual family",
        ],
        "keyword_group": {
            "style": "petal_cluster" if len(keywords) >= 3 else "chip_row",
            "block_ids": [b.get("id") for b in keywords],
        },
        "bilingual_pair_groups": pair_groups,
    }


def apply_plan(spec: dict, density: str) -> dict:
    result = copy.deepcopy(spec)
    result["layout_engine"] = {
        "id": "storybook-responsive-v1",
        "stage": [SLIDE_W, SLIDE_H],
        "density": density,
        "principles": ["content-measured", "semantic-zones", "optical-correction", "layout-variety"],
    }
    previous: str | None = None
    for index, slide in enumerate(result.get("slides", []), 1):
        plan = plan_slide(slide, index, density, previous)
        slide.setdefault("visual", {})["layout_plan"] = plan
        completion = slide["visual"].setdefault("completion", {})
        completion["density"] = density
        completion["hero_scale_ratio"] = plan["hero_scale_ratio"]
        completion["text_scale_ratio"] = plan["text_scale_ratio"]
        completion["target_coverage_ratio"] = plan["target_coverage_ratio"]
        completion["max_empty_region_ratio"] = plan["max_empty_region_ratio"]
        completion["white_space_intent"] = "frame the focal point and preserve a clear reading path; no unused dead zones"
        completion["fill_strategy"] = ["scale focal art", "scale paired typography", "switch archetype", "add semantic component family"]
        previous = plan["archetype"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec")
    parser.add_argument("--out", required=True)
    parser.add_argument("--density", choices=["light", "balanced", "rich"], default="balanced")
    args = parser.parse_args()
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    planned = apply_plan(spec, args.density)
    Path(args.out).write_text(json.dumps(planned, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = [{"slide": s.get("id"), "archetype": s.get("visual", {}).get("layout_plan", {}).get("archetype"), "content_level": s.get("visual", {}).get("layout_plan", {}).get("content_level")} for s in planned.get("slides", [])]
    print(json.dumps({"status": "PASS", "out": args.out, "slides": summary}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
