#!/usr/bin/env python3
"""Validate picture-book composition, component framing, and layout variety."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

PLAYFUL = {"cloud_bubble", "speech_bubble", "scalloped_panel", "watercolor_blob", "leaf_label", "petal_cluster", "torn_paper"}
RECTANGULAR = {"rectangle", "rounded_rectangle", "paper_panel", "card"}
KEYWORD_ROLES = {"keyword", "label", "vocabulary"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec")
    args = parser.parse_args()
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []
    slides_report: list[dict] = []
    archetypes: list[str] = []
    container_counts: Counter[str] = Counter()

    for idx, slide in enumerate(spec.get("slides", []), 1):
        sid = slide.get("id", f"S{idx:02d}")
        visual = slide.get("visual", {}) or {}
        plan = visual.get("layout_plan") or {}
        blocks = slide.get("screen", {}).get("text_blocks", []) or []
        if spec.get("usage_mode") == "child_stage_speech" and not plan:
            errors.append(f"{sid}: missing visual.layout_plan from responsive storybook planner")
            continue
        archetype = str(plan.get("archetype", ""))
        container = str(plan.get("text_container_style", ""))
        archetypes.append(archetype)
        if container:
            container_counts[container] += 1
        if container not in PLAYFUL:
            warnings.append(f"{sid}: text container '{container or 'none'}' is not in the playful picture-book family")
        if not plan.get("edge_treatment"):
            warnings.append(f"{sid}: no edge treatment; page may read as floating objects on a blank canvas")
        zones = plan.get("zones") or {}
        if len(zones) < 2:
            errors.append(f"{sid}: layout plan has fewer than two semantic zones")
        hero_scale = float(plan.get("hero_scale_ratio", 0) or 0)
        level = plan.get("content_level", "medium")
        minimum_hero = {"sparse": 0.42, "medium": 0.34, "rich": 0.26}.get(level, 0.34)
        if hero_scale < minimum_hero:
            errors.append(f"{sid}: hero scale {hero_scale:.0%} is too small for {level} content")
        keyword_blocks = [b for b in blocks if b.get("role") in KEYWORD_ROLES]
        keyword_plan = plan.get("keyword_group") or {}
        if len(keyword_blocks) >= 3 and keyword_plan.get("style") not in {"petal_cluster", "chip_row", "object_constellation"}:
            errors.append(f"{sid}: three or more vocabulary labels are not grouped into a designed component family")
        for block in keyword_blocks:
            if not (block.get("container_style") or block.get("visual_binding") or block.get("container_id") or block.get("id") in keyword_plan.get("block_ids", [])):
                errors.append(f"{sid}:{block.get('id', 'keyword')} is an orphan label with no frame or visual binding")

        en_sizes = [float(b.get("font_size_pt", 0) or 0) for b in blocks if b.get("lang") == "en" and b.get("role") in {"title", "core_line"}]
        zh_sizes = [float(b.get("font_size_pt", 0) or 0) for b in blocks if b.get("lang") == "zh" and b.get("role") in {"translation", "core_line"}]
        if en_sizes and zh_sizes:
            ratio = max(zh_sizes) / max(en_sizes)
            if ratio < 0.55:
                errors.append(f"{sid}: Chinese counterpart is only {ratio:.0%} of the English size")
            elif ratio < 0.68:
                warnings.append(f"{sid}: Chinese counterpart may feel visually subordinate ({ratio:.0%} size ratio)")
            if not plan.get("bilingual_pair_groups"):
                warnings.append(f"{sid}: bilingual text is not explicitly grouped as one visual unit")

        components = visual.get("component_plan", []) or []
        component_types = [str(c.get("type", "")) for c in components]
        rect_count = sum(1 for t in component_types if t in RECTANGULAR)
        if len(component_types) >= 3 and rect_count / max(1, len(component_types)) > 0.65:
            warnings.append(f"{sid}: {rect_count}/{len(component_types)} components are rectangular; shape language may feel template-like")
        target = float(plan.get("target_coverage_ratio", 0.5) or 0.5)
        max_empty = float(plan.get("max_empty_region_ratio", 0.4) or 0.4)
        if target < 0.46 and spec.get("usage_mode") == "child_stage_speech":
            warnings.append(f"{sid}: target coverage {target:.0%} is conservative for a children's picture-book slide")
        if max_empty > 0.42:
            warnings.append(f"{sid}: allowed continuous empty region {max_empty:.0%} is high")
        slides_report.append({"slide_id": sid, "archetype": archetype, "container": container, "keyword_count": len(keyword_blocks), "hero_scale_ratio": hero_scale, "target_coverage_ratio": target})

    for i in range(len(archetypes) - 2):
        if archetypes[i] and archetypes[i] == archetypes[i + 1] == archetypes[i + 2]:
            errors.append(f"slides {i+1}-{i+3}: same layout archetype repeated three times")
    if archetypes and len(set(archetypes)) < min(4, max(2, len(archetypes) // 2)):
        warnings.append(f"deck uses only {len(set(archetypes))} layout archetype(s) across {len(archetypes)} slides")
    if container_counts:
        dominant, count = container_counts.most_common(1)[0]
        if count / sum(container_counts.values()) > 0.65:
            warnings.append(f"text container '{dominant}' dominates {count}/{sum(container_counts.values())} slides")

    result = {"status": "BLOCKED" if errors else "PASS", "errors": errors, "warnings": warnings, "archetype_counts": dict(Counter(archetypes)), "container_counts": dict(container_counts), "slides": slides_report}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
