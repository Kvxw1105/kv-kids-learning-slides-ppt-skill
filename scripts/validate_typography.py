#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / 'assets' / 'registries' / 'typography-themes.json'
PURE_BLACK = {'#000000', '000000', '#000', '000'}


def load_themes() -> list[dict]:
    return json.loads(REGISTRY.read_text(encoding='utf-8'))


def infer_theme_id(spec: dict, themes: list[dict]) -> str | None:
    explicit = spec.get('typography', {}).get('theme_id')
    if explicit:
        return explicit
    visual_system = spec.get('visual_system')
    for theme in themes:
        if visual_system in theme.get('visual_systems', []):
            return theme.get('id')
    return None


def color_is_black(value: str | None) -> bool:
    if not value:
        return False
    return str(value).strip().lower() in PURE_BLACK


def count_words(text: str) -> int:
    return len(re.findall(r"[A-Za-z]+|[\u4e00-\u9fff]", text or ''))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('spec')
    args = parser.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding='utf-8'))
    themes = load_themes()
    theme_id = infer_theme_id(spec, themes)
    theme = next((item for item in themes if item.get('id') == theme_id), None)
    errors: list[str] = []
    warnings: list[str] = []
    block_reports: list[dict] = []

    if spec.get('usage_mode') == 'child_stage_speech' and not theme:
        errors.append('child-stage speech decks must select or infer a typography theme')
    if theme:
        required = ['title_en', 'title_zh', 'core_en', 'core_zh', 'label']
        for key in required:
            if key not in theme:
                errors.append(f'typography theme {theme_id} is missing {key}')
        rules = theme.get('rules', {})
        families = set()
        colors = set()
        for key in required:
            style = theme.get(key, {})
            families.update(style.get('font_families', []))
            color = style.get('color')
            if color:
                colors.add(color.lower())
            if not style.get('font_families'):
                errors.append(f'{theme_id}.{key} has no font fallback list')
            if rules.get('prohibit_pure_black') and color_is_black(color):
                errors.append(f'{theme_id}.{key} uses pure black')
        if len(families) > int(rules.get('max_font_families', 4)) * 3:
            warnings.append(f'typography theme exposes many fallback families ({len(families)})')
        if len(colors) > int(rules.get('max_text_colors', 5)):
            errors.append(f'typography theme uses {len(colors)} text colors, above the theme limit')
        title_size = max(float(theme.get('title_en', {}).get('size_pt', 0)), float(theme.get('title_zh', {}).get('size_pt', 0)))
        body_size = max(float(theme.get('core_en', {}).get('size_pt', 1)), float(theme.get('core_zh', {}).get('size_pt', 1)))
        ratio = title_size / max(body_size, 1)
        if ratio < float(rules.get('min_title_body_ratio', 1.2)):
            warnings.append(f'title/body scale ratio is only {ratio:.2f}')

    for index, slide in enumerate(spec.get('slides', []), 1):
        sid = slide.get('id', f'S{index:02d}')
        for block in slide.get('screen', {}).get('text_blocks', []) or []:
            role = block.get('role', 'core_line')
            lang = block.get('lang', 'en')
            text = block.get('text', '')
            size = float(block.get('font_size_pt', 0) or 0)
            color = block.get('color')
            if color_is_black(color) and spec.get('usage_mode') == 'child_stage_speech':
                errors.append(f'{sid}:{block.get("id", role)} overrides text to pure black')
            if role == 'title' and size and size < 34:
                warnings.append(f'{sid}:{block.get("id", role)} title is only {size:g}pt')
            if role in {'core_line', 'translation'} and size and size < 22:
                errors.append(f'{sid}:{block.get("id", role)} visible line is below 22pt')
            if role == 'translation' and lang == 'zh' and color_is_black(color):
                errors.append(f'{sid}:{block.get("id", role)} treats Chinese translation as plain black text')
            if count_words(text) > 18 and size < 28:
                warnings.append(f'{sid}:{block.get("id", role)} is dense for its font size')
            block_reports.append({'slide_id': sid, 'block_id': block.get('id'), 'role': role, 'lang': lang, 'font_size_pt': size, 'color_override': color})

    result = {
        'status': 'BLOCKED' if errors else 'PASS',
        'theme_id': theme_id,
        'errors': errors,
        'warnings': warnings,
        'blocks': block_reports,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
