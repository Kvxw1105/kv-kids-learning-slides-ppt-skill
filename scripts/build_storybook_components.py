#!/usr/bin/env python3
"""Generate a reusable SVG component family for children's slides.

The output stays vector-based. The irregular outlines are independently
implemented with deterministic path jitter; no third-party code is bundled.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path


def svg_wrap(body: str, w: int = 1200, h: int = 800) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{body}</svg>'


def jittered_rect(x: float, y: float, w: float, h: float, seed: int, jitter: float = 12) -> str:
    rng = random.Random(seed)
    pts = []
    steps = 8
    for i in range(steps + 1):
        pts.append((x + w * i / steps, y + rng.uniform(-jitter, jitter)))
    for i in range(1, steps + 1):
        pts.append((x + w + rng.uniform(-jitter, jitter), y + h * i / steps))
    for i in range(1, steps + 1):
        pts.append((x + w * (steps - i) / steps, y + h + rng.uniform(-jitter, jitter)))
    for i in range(1, steps):
        pts.append((x + rng.uniform(-jitter, jitter), y + h * (steps - i) / steps))
    return "M " + " L ".join(f"{px:.1f},{py:.1f}" for px, py in pts) + " Z"


def write(out: Path, name: str, svg: str, category: str, manifest: list[dict]) -> None:
    path = out / f"{name}.svg"
    path.write_text(svg, encoding="utf-8")
    manifest.append({"id": name, "file": path.name, "category": category, "editable_source": "svg"})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--palette", default="watercolor")
    args = parser.parse_args()
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    palettes = {
        "watercolor": {"pink": "#F4A7C4", "green": "#8DBA79", "yellow": "#F4C95D", "cream": "#FFF8E8", "ink": "#5D4B50", "blue": "#A8D8EA"},
        "crayon": {"pink": "#FF8FB1", "green": "#7BBE68", "yellow": "#FFD34E", "cream": "#FFF5D8", "ink": "#594A42", "blue": "#8BC7F0"},
    }
    p = palettes.get(args.palette, palettes["watercolor"])
    manifest: list[dict] = []

    cloud = f'<path d="M155 520 C80 430 130 290 260 292 C280 155 480 110 555 230 C650 120 850 170 850 315 C1000 300 1070 440 975 535 C850 650 280 650 155 520 Z" fill="{p["cream"]}" stroke="{p["pink"]}" stroke-width="18" stroke-linecap="round"/><path d="M910 560 L1035 650 L885 625 Z" fill="{p["cream"]}" stroke="{p["pink"]}" stroke-width="18" stroke-linejoin="round"/>'
    write(out, "cloud-bubble", svg_wrap(cloud), "container", manifest)

    speech = f'<rect x="95" y="100" width="950" height="520" rx="110" fill="{p["cream"]}" stroke="{p["green"]}" stroke-width="18"/><path d="M300 610 L220 735 L430 615 Z" fill="{p["cream"]}" stroke="{p["green"]}" stroke-width="18" stroke-linejoin="round"/>'
    write(out, "speech-bubble", svg_wrap(speech), "container", manifest)

    scallops = ''.join(f'<circle cx="{100+i*90}" cy="690" r="58" fill="{p["cream"]}" stroke="{p["pink"]}" stroke-width="8"/>' for i in range(12))
    panel = f'<rect x="80" y="85" width="1040" height="610" rx="70" fill="{p["cream"]}" stroke="{p["pink"]}" stroke-width="16"/>{scallops}'
    write(out, "scalloped-panel", svg_wrap(panel), "container", manifest)

    torn_path = jittered_rect(105, 90, 990, 620, seed=23, jitter=16)
    torn = f'<path d="{torn_path}" fill="{p["cream"]}" stroke="{p["green"]}" stroke-width="14" stroke-linejoin="round"/>'
    write(out, "torn-paper-panel", svg_wrap(torn), "container", manifest)

    blob = '<path d="M145 425 C95 230 275 105 475 165 C650 35 930 105 1010 310 C1120 535 900 720 660 650 C470 780 190 690 145 425 Z" fill="%s" stroke="%s" stroke-width="13" opacity="0.96"/>' % (p["cream"], p["blue"])
    write(out, "watercolor-blob", svg_wrap(blob), "container", manifest)

    petals = ''.join(f'<ellipse cx="600" cy="400" rx="185" ry="80" transform="rotate({a} 600 400)" fill="{p["pink"]}" opacity="0.94"/>' for a in range(0, 360, 60))
    chip = f'{petals}<circle cx="600" cy="400" r="92" fill="{p["yellow"]}"/>'
    write(out, "petal-chip", svg_wrap(chip), "label", manifest)

    leaf = f'<path d="M170 520 C250 180 720 95 1035 250 C895 575 500 720 170 520 Z" fill="{p["green"]}" opacity="0.92"/><path d="M260 520 C520 420 710 310 920 245" fill="none" stroke="{p["cream"]}" stroke-width="16" stroke-linecap="round"/>'
    write(out, "leaf-label", svg_wrap(leaf), "label", manifest)

    underline = f'<path d="M115 480 C260 420 390 525 535 455 C700 380 820 520 1080 430" fill="none" stroke="{p["pink"]}" stroke-width="42" stroke-linecap="round" opacity="0.72"/><path d="M140 535 C340 485 620 575 1030 500" fill="none" stroke="{p["yellow"]}" stroke-width="22" stroke-linecap="round" opacity="0.55"/>'
    write(out, "brush-underline", svg_wrap(underline), "typography-accent", manifest)

    frame = f'<path d="M80 105 Q600 15 1120 105 M1120 105 Q1195 400 1120 695 M1120 695 Q600 785 80 695 M80 695 Q5 400 80 105" fill="none" stroke="{p["green"]}" stroke-width="16" stroke-dasharray="14 18" stroke-linecap="round"/>'
    write(out, "storybook-frame", svg_wrap(frame), "frame", manifest)

    data = {"version": "0.8", "palette": args.palette, "license": "generated by skill; no third-party artwork bundled", "components": manifest}
    (out / "manifest.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PASS", "out_dir": str(out), "components": len(manifest)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
