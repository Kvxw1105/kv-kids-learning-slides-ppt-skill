#!/usr/bin/env python3
"""Validate intentional visual density, scale, and white-space use."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

SLIDE_AREA = 13.333 * 7.5
DENSITY = {
    'light': {'target': 0.38, 'max_empty': 0.50, 'min_components': 2, 'hero': 0.28},
    'balanced': {'target': 0.48, 'max_empty': 0.42, 'min_components': 3, 'hero': 0.34},
    'rich': {'target': 0.58, 'max_empty': 0.35, 'min_components': 4, 'hero': 0.40},
}


def text_area_estimate(blocks: list[dict]) -> float:
    score = 0.0
    for block in blocks:
        text = str(block.get('text', ''))
        size = float(block.get('font_size_pt', 24) or 24)
        units = max(1, len(text.strip()))
        score += min(0.09, 0.012 + (size / 36.0) * min(units, 30) / 520.0)
    return min(score, 0.20)


def component_area_estimate(components: list[dict]) -> float:
    area = 0.0
    for item in components:
        try:
            w = max(0.0, float(item.get('w', 0)))
            h = max(0.0, float(item.get('h', 0)))
        except Exception:
            continue
        area += min(w * h, SLIDE_AREA * 0.12)
    return min(area / SLIDE_AREA, 0.22)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('spec')
    args = parser.parse_args()
    spec = json.loads(Path(args.spec).read_text(encoding='utf-8'))
    errors: list[str] = []
    warnings: list[str] = []
    slides_report: list[dict] = []

    root_profile = spec.get('composition_profile', {}) or {}
    for index, slide in enumerate(spec.get('slides', []), 1):
        sid = slide.get('id', f'S{index:02d}')
        visual = slide.get('visual', {})
        completion = visual.get('completion', {}) or {}
        components = visual.get('component_plan', []) or []
        assets = visual.get('asset_ids', []) or []
        text_blocks = slide.get('screen', {}).get('text_blocks', []) or []
        layers = set(completion.get('base_layers', []))
        if text_blocks:
            layers.add('text')
        layers.add('background')
        if components:
            layers.add('code_components')
        if assets:
            layers.add('ai_or_source_image')
        if visual.get('native_scene'):
            layers.add('native_scene')

        minimum = int(completion.get('minimum_layers', 4))
        intentional = bool(completion.get('intentional_minimalism', False))
        density_id = str(completion.get('density') or root_profile.get('density') or 'balanced')
        defaults = DENSITY.get(density_id, DENSITY['balanced'])
        target = float(completion.get('target_coverage_ratio', root_profile.get('target_coverage_ratio', defaults['target'])))
        max_empty = float(completion.get('max_empty_region_ratio', root_profile.get('max_empty_region_ratio', defaults['max_empty'])))
        hero_scale = completion.get('hero_scale_ratio')
        if hero_scale is None:
            hero_scale = defaults['hero'] if (assets or visual.get('native_scene')) else 0.0
        hero_scale = float(hero_scale)
        declared_empty = completion.get('largest_empty_region_ratio')
        text_scale = float(completion.get('text_scale_ratio', root_profile.get('text_scale_ratio', 1.0)))

        component_ratio = component_area_estimate(components)
        text_ratio = min(0.24, text_area_estimate(text_blocks) * max(0.7, text_scale))
        estimated = min(0.86, hero_scale + component_ratio + text_ratio)

        if not intentional and len(layers) < minimum:
            errors.append(f'{sid}: only {len(layers)} visual layers, minimum is {minimum}')
        if not intentional and not components and not assets and not visual.get('native_scene'):
            errors.append(f'{sid}: no image, native scene, or code-generated visual components')
        if len(components) > 8:
            warnings.append(f'{sid}: {len(components)} code components may create decorative clutter')
        if not intentional and density_id in {'balanced', 'rich'} and len(components) < defaults['min_components'] and not assets and not visual.get('native_scene'):
            errors.append(f'{sid}: {density_id} composition lacks a visual anchor and enough support components')
        if not intentional and estimated < target - 0.12:
            errors.append(f'{sid}: estimated occupied coverage {estimated:.0%} is far below target {target:.0%}')
        elif not intentional and estimated < target:
            warnings.append(f'{sid}: estimated occupied coverage {estimated:.0%} is below target {target:.0%}')
        if declared_empty is not None and float(declared_empty) > max_empty and not intentional:
            errors.append(f'{sid}: declared largest empty region {float(declared_empty):.0%} exceeds {max_empty:.0%}')
        if (assets or visual.get('native_scene')) and hero_scale < defaults['hero'] - 0.08 and not intentional:
            warnings.append(f'{sid}: hero scale {hero_scale:.0%} may feel too small for {density_id} composition')
        if not completion.get('white_space_intent') and not intentional:
            warnings.append(f'{sid}: white-space intent is not documented')
        if not completion.get('fill_strategy') and not intentional:
            warnings.append(f'{sid}: sparse-page repair strategy is not documented')
        max_font = max((float(block.get('font_size_pt', 0) or 0) for block in text_blocks), default=0)
        if density_id in {'balanced', 'rich'} and max_font and max_font < 30:
            warnings.append(f'{sid}: largest visible text is only {max_font:g}pt for a {density_id} child-stage page')

        slides_report.append({
            'slide_id': sid,
            'density': density_id,
            'layers': sorted(layers),
            'minimum_layers': minimum,
            'component_count': len(components),
            'asset_count': len(assets),
            'hero_scale_ratio': round(hero_scale, 3),
            'component_area_ratio': round(component_ratio, 3),
            'text_area_ratio': round(text_ratio, 3),
            'estimated_coverage_ratio': round(estimated, 3),
            'target_coverage_ratio': target,
            'max_empty_region_ratio': max_empty,
            'intentional_minimalism': intentional,
        })

    result = {'status': 'BLOCKED' if errors else 'PASS', 'errors': errors, 'warnings': warnings, 'slides': slides_report}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
