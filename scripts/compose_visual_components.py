#!/usr/bin/env python3
"""Add a deterministic code-generated visual component plan to slide_spec.json.

The composer intentionally favors editable PowerPoint-native stickers and layout
accents. It never adds components inside declared text or hero safe zones.
"""
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path

SLIDE_W = 13.333
SLIDE_H = 7.5


def item(id_, type_, x, y, w, h, layer="foreground", **extra):
    return {"id": id_, "type": type_, "x": x, "y": y, "w": w, "h": h, "layer": layer, **extra}


PLANS = {
    "kindergarten-speech-cover": [
        item("top_scallops", "scallop_strip", 0.0, 0.02, 13.33, 0.28, "background", fill="#F8D4E2", transparency=8, count=20),
        item("bottom_grass", "grass", 0.55, 6.60, 2.3, 0.55, "background", fill="#88B96B", transparency=12),
        item("corner_flower", "flower_sticker", 0.42, 5.75, 0.82, 0.82, fill="#F6A6C8", accent="#FFD66B"),
        item("sparkles", "sparkle_cluster", 5.78, 0.55, 0.92, 0.92, fill="#FFD66B", transparency=5),
        item("butterfly", "butterfly", 11.92, 0.62, 0.78, 0.64, fill="#C9B8F4", accent="#F6A6C8"),
    ],
    "hello-and-wave": [
        item("corner_dots", "dots", 0.30, 5.65, 1.35, 1.10, fill="#F6A6C8", transparency=8),
        item("hello_butterfly", "butterfly", 11.70, 0.45, 0.82, 0.68, fill="#C9B8F4", accent="#FFD66B"),
        item("hello_sparkles", "sparkle_cluster", 6.35, 4.85, 0.85, 0.75, fill="#FFD66B", transparency=12),
    ],
    "this-is-me": [
        item("name_badge", "badge", 10.95, 4.55, 1.05, 1.05, fill="#FFD66B", accent="#F3A861", text="ME", font_size_pt=14),
        item("me_leaf", "leaf_sprig", 0.35, 5.65, 1.25, 0.90, fill="#88B96B"),
        item("me_sparkle", "sparkle_cluster", 6.35, 4.85, 0.85, 0.75, fill="#FFD66B", transparency=12),
    ],
    "show-one-object": [
        item("object_leaf", "leaf_sprig", 11.55, 0.45, 1.20, 0.92, fill="#88B96B"),
        item("object_dots", "dots", 11.20, 5.50, 1.25, 0.90, transparency=12),
        item("object_sparkles", "sparkle_cluster", 5.80, 4.15, 0.78, 0.70, fill="#FFD66B", transparency=8),
    ],
    "one-action-one-line": [
        item("action_panel", "paper_panel", 0.65, 0.55, 12.0, 4.45, "background", fill="#FFFDF8", line="#F6D4E2", transparency=0),
        item("action_drops", "dots", 10.65, 0.55, 1.25, 1.05, colors=["#9ED9F6", "#72C8F0", "#D8EEFA"], transparency=4),
        item("action_heart", "heart", 8.80, 1.25, 0.70, 0.64, fill="#F6A6C8", transparency=7),
        item("action_grass", "grass", 3.78, 3.70, 2.35, 0.52, "background", fill="#88B96B", transparency=18),
    ],
    "weather-pair": [
        item("weather_panel", "paper_panel", 0.48, 0.55, 12.37, 4.65, "background", fill="#FFFDF8", line="#F4E0B6", transparency=0),
        item("weather_top_ribbon", "ribbon", 4.45, 0.35, 4.35, 0.55, "foreground", fill="#FFF0B5", accent="#FFD66B", text="SUN + RAIN", text_color="#8A5A3B", font_size_pt=20),
        item("weather_leaf", "leaf_sprig", 0.45, 4.45, 1.20, 0.88, fill="#88B96B"),
        item("weather_sparkles", "sparkle_cluster", 11.65, 4.45, 0.85, 0.75, fill="#FFD66B", transparency=10),
    ],
    "before-and-after": [
        item("before_dots", "dots", 0.25, 0.25, 0.95, 0.72, transparency=18),
        item("after_sparkles", "sparkle_cluster", 11.95, 0.22, 0.82, 0.72, fill="#FFD66B", transparency=6),
        item("growth_leaf", "leaf_sprig", 5.95, 4.45, 1.35, 0.90, fill="#88B96B"),
    ],
    "emotion-moment": [
        item("emotion_sparkles_left", "sparkle_cluster", 0.55, 3.85, 0.95, 0.85, fill="#FFD66B", transparency=7),
        item("emotion_sparkles_right", "sparkle_cluster", 11.65, 3.65, 0.95, 0.85, fill="#FFD66B", transparency=7),
        item("emotion_butterfly", "butterfly", 10.85, 0.55, 0.78, 0.66, fill="#C9B8F4", accent="#F6A6C8"),
    ],
    "simple-closing": [
        item("closing_scallops", "scallop_strip", 0.0, 6.88, 13.33, 0.30, "background", fill="#DFF3E1", transparency=5, count=20),
        item("closing_flower", "flower_sticker", 0.38, 5.72, 0.82, 0.82, fill="#F6A6C8", accent="#FFD66B"),
        item("closing_butterfly", "butterfly", 5.65, 0.50, 0.82, 0.68, fill="#C9B8F4", accent="#FFD66B"),
        item("closing_sparkles", "sparkle_cluster", 11.75, 5.35, 0.88, 0.80, fill="#FFD66B", transparency=8),
    ],
}

ALIASES = {
    "cover": "kindergarten-speech-cover",
    "side": "show-one-object",
    "card": "show-one-object",
    "card2": "show-one-object",
    "imageLeft": "one-action-one-line",
    "weather": "weather-pair",
    "bloom": "emotion-moment",
    "lesson": "before-and-after",
    "closing": "simple-closing",
}

NATIVE_SCENE_LAYOUTS = {"one-action-one-line", "weather-pair", "before-and-after", "emotion-moment"}


def enhance_slide(slide: dict, replace: bool, density: str) -> None:
    visual = slide.setdefault("visual", {})
    layout = ALIASES.get(visual.get("layout", "show-one-object"), visual.get("layout", "show-one-object"))
    visual["layout"] = layout
    if replace or not visual.get("component_plan"):
        visual["component_plan"] = deepcopy(PLANS.get(layout, PLANS["show-one-object"]))
    visual["native_scene"] = layout in NATIVE_SCENE_LAYOUTS or bool(visual.get("native_scene"))
    visual["completion"] = {
        "density": density,
        "intentional_minimalism": bool(visual.get("intentional_minimalism", False)),
        "minimum_layers": 4 if density != "rich" else 5,
        "base_layers": [
            "background",
            "text" if slide.get("screen", {}).get("text_blocks") else None,
            "native_scene" if visual.get("native_scene") else None,
            "ai_or_source_image" if visual.get("asset_ids") else None,
            "code_components" if visual.get("component_plan") else None,
        ],
    }
    visual["completion"]["base_layers"] = [x for x in visual["completion"]["base_layers"] if x]


def main() -> int:
    parser = argparse.ArgumentParser(description="Compose editable visual components into slide_spec.json")
    parser.add_argument("spec")
    parser.add_argument("--out", required=True)
    parser.add_argument("--replace", action="store_true")
    parser.add_argument("--density", choices=["light", "balanced", "rich"], default="balanced")
    parser.add_argument("--sticker-dir", help="Optional generated sticker-pack directory; enables small animated GIF accents")
    args = parser.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    sticker_dir = Path(args.sticker_dir).resolve() if args.sticker_dir else None
    for slide in spec.get("slides", []):
        enhance_slide(slide, args.replace, args.density)
        if sticker_dir and slide.get("visual", {}).get("layout") == "simple-closing":
            gif = sticker_dir / "sparkle-pulse.gif"
            if gif.exists():
                slide["visual"].setdefault("component_plan", []).append(
                    item("closing_motion_sparkle", "animated_gif", 11.65, 0.42, 0.62, 0.62, file=str(gif))
                )
    spec.setdefault("visual_component_system", {})
    spec["visual_component_system"].update({
        "version": "0.6",
        "renderer": "native-pptx-shapes",
        "density": args.density,
        "policy": "Use code-generated components before requesting decorative AI images.",
    })
    Path(args.out).write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PASS", "slides": len(spec.get("slides", [])), "output": args.out}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
