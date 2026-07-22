#!/usr/bin/env python3
"""Generate reusable child-friendly SVG stickers and optional animated GIFs.

No external image model is required. SVGs are source assets; GIFs are optional
small motion accents for PowerPoint or HTML previews.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw

PALETTE = {
    "cream": "#FFF9EC",
    "pink": "#F6A6C8",
    "deep_pink": "#D95D8A",
    "yellow": "#FFD66B",
    "green": "#88B96B",
    "deep_green": "#4E7B55",
    "blue": "#9ED9F6",
    "lavender": "#C9B8F4",
    "ink": "#503F45",
}


def svg_wrap(body: str, size: int = 256) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">{body}</svg>\n'


def flower_svg() -> str:
    petals = []
    cx = cy = 128
    for angle in range(0, 360, 60):
        rad = math.radians(angle)
        x = cx + math.cos(rad) * 52
        y = cy + math.sin(rad) * 52
        petals.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="38" ry="28" fill="{PALETTE["pink"]}" transform="rotate({angle+90} {x:.1f} {y:.1f})"/>')
    return svg_wrap(''.join(petals) + f'<circle cx="128" cy="128" r="34" fill="{PALETTE["yellow"]}"/>')


def leaf_svg() -> str:
    return svg_wrap(
        f'<path d="M48 204 C82 120, 154 60, 220 38" fill="none" stroke="{PALETTE["deep_green"]}" stroke-width="12" stroke-linecap="round"/>'
        f'<ellipse cx="92" cy="158" rx="46" ry="26" fill="{PALETTE["green"]}" transform="rotate(-35 92 158)"/>'
        f'<ellipse cx="128" cy="118" rx="43" ry="24" fill="{PALETTE["green"]}" transform="rotate(28 128 118)"/>'
        f'<ellipse cx="172" cy="78" rx="40" ry="23" fill="{PALETTE["green"]}" transform="rotate(-35 172 78)"/>'
    )


def butterfly_svg() -> str:
    return svg_wrap(
        f'<ellipse cx="76" cy="86" rx="54" ry="38" fill="{PALETTE["lavender"]}" transform="rotate(-25 76 86)"/>'
        f'<ellipse cx="78" cy="164" rx="43" ry="34" fill="{PALETTE["pink"]}" transform="rotate(18 78 164)"/>'
        f'<ellipse cx="180" cy="86" rx="54" ry="38" fill="{PALETTE["lavender"]}" transform="rotate(25 180 86)"/>'
        f'<ellipse cx="178" cy="164" rx="43" ry="34" fill="{PALETTE["pink"]}" transform="rotate(-18 178 164)"/>'
        f'<ellipse cx="128" cy="128" rx="13" ry="72" fill="{PALETTE["ink"]}"/>'
    )


def star_svg() -> str:
    points = []
    for i in range(10):
        angle = -math.pi/2 + i*math.pi/5
        r = 92 if i % 2 == 0 else 40
        points.append(f'{128 + math.cos(angle)*r:.1f},{128 + math.sin(angle)*r:.1f}')
    return svg_wrap(f'<polygon points="{" ".join(points)}" fill="{PALETTE["yellow"]}" stroke="#F3A861" stroke-width="8" stroke-linejoin="round"/>')


def heart_svg() -> str:
    return svg_wrap(f'<path d="M128 218 C98 190, 34 150, 34 88 C34 42, 92 26, 128 72 C164 26, 222 42, 222 88 C222 150, 158 190, 128 218 Z" fill="{PALETTE["pink"]}"/>')


def cloud_svg() -> str:
    return svg_wrap(
        f'<path d="M56 184 C22 184, 18 132, 54 122 C50 70, 116 44, 150 82 C190 58, 234 92, 224 134 C254 154, 230 190, 196 188 Z" fill="{PALETTE["blue"]}"/>'
        f'<circle cx="102" cy="136" r="8" fill="{PALETTE["ink"]}"/><circle cx="164" cy="136" r="8" fill="{PALETTE["ink"]}"/>'
        f'<path d="M112 158 Q132 174 154 158" fill="none" stroke="{PALETTE["ink"]}" stroke-width="6" stroke-linecap="round"/>'
    )


def ribbon_svg() -> str:
    return svg_wrap(
        f'<polygon points="22,86 68,56 68,200 22,172" fill="{PALETTE["deep_pink"]}"/>'
        f'<rect x="56" y="52" width="144" height="148" rx="28" fill="{PALETTE["pink"]}"/>'
        f'<polygon points="188,56 234,86 234,172 188,200" fill="{PALETTE["deep_pink"]}"/>'
    )

STATIC = {
    "flower": flower_svg,
    "leaf-sprig": leaf_svg,
    "butterfly": butterfly_svg,
    "star": star_svg,
    "heart": heart_svg,
    "cloud": cloud_svg,
    "ribbon": ribbon_svg,
}


def animated_sparkle(path: Path) -> None:
    frames = []
    for scale in (0.62, 0.82, 1.0, 0.82):
        im = Image.new("RGBA", (192, 192), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        cx = cy = 96
        r1, r2 = 70*scale, 26*scale
        pts = []
        for i in range(10):
            angle = -math.pi/2 + i*math.pi/5
            r = r1 if i % 2 == 0 else r2
            pts.append((cx + math.cos(angle)*r, cy + math.sin(angle)*r))
        draw.polygon(pts, fill=(255, 214, 107, 245))
        frames.append(im)
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=140, loop=0, disposal=2)


def animated_butterfly(path: Path) -> None:
    frames = []
    for wing in (1.0, 0.70, 0.42, 0.70):
        im = Image.new("RGBA", (220, 180), (0, 0, 0, 0))
        draw = ImageDraw.Draw(im)
        cx = 110
        draw.ellipse((cx-8, 38, cx+8, 146), fill=(80, 63, 69, 255))
        wing_w = int(76*wing)
        draw.ellipse((cx-wing_w-12, 20, cx-12, 95), fill=(201, 184, 244, 245))
        draw.ellipse((cx+12, 20, cx+wing_w+12, 95), fill=(201, 184, 244, 245))
        draw.ellipse((cx-wing_w, 78, cx-12, 148), fill=(246, 166, 200, 245))
        draw.ellipse((cx+12, 78, cx+wing_w, 148), fill=(246, 166, 200, 245))
        frames.append(im)
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=120, loop=0, disposal=2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    assets = []
    for name, builder in STATIC.items():
        path = out / f"{name}.svg"
        path.write_text(builder(), encoding="utf-8")
        assets.append({"id": name, "file": path.name, "format": "svg", "animated": False})
    animated_sparkle(out / "sparkle-pulse.gif")
    animated_butterfly(out / "butterfly-flap.gif")
    assets.extend([
        {"id": "sparkle-pulse", "file": "sparkle-pulse.gif", "format": "gif", "animated": True},
        {"id": "butterfly-flap", "file": "butterfly-flap.gif", "format": "gif", "animated": True},
    ])
    manifest = {"version": "0.6", "generator": "build_sticker_pack.py", "assets": assets}
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PASS", "out_dir": str(out), "assets": len(assets)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
