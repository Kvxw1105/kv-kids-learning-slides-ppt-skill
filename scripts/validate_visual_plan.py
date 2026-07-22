#!/usr/bin/env python3
import json
import sys
from collections import defaultdict
from pathlib import Path

REQUIRED = {
    "asset_id",
    "slide_ids",
    "purpose",
    "required",
    "source_strategy",
    "aspect_ratio",
    "status",
}
VALID_MODES = {"none", "smart", "studio", "external-prompt-pack"}
NARRATIVE_PURPOSES = {
    "cover_hero",
    "story_hero",
    "character_action",
    "state_change",
    "closing_hero",
}


def validate(data: dict) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    ids: set[str] = set()

    if data.get("mode") not in VALID_MODES:
        errors.append("invalid mode")

    characters = {
        c.get("character_id"): c
        for c in data.get("character_bible", {}).get("characters", [])
        if c.get("character_id")
    }
    identity_refs = {
        f"character_bible:{character_id}": character_id for character_id in characters
    }
    slide_assets: dict[str, list[dict]] = defaultdict(list)

    for index, asset in enumerate(data.get("assets", []), 1):
        missing = REQUIRED - set(asset)
        errors.extend(f"asset {index} missing {key}" for key in sorted(missing))
        asset_id = asset.get("asset_id")
        if asset_id in ids:
            errors.append(f"duplicate asset_id {asset_id}")
        if asset_id:
            ids.add(asset_id)

        if asset.get("required") and not asset.get("slide_ids"):
            errors.append(f"{asset_id}: required asset has no slide_ids")
        if asset.get("source_strategy") in {"generate", "external-prompt-pack"} and not asset.get("prompt"):
            warnings.append(f"{asset_id}: missing prompt")
        if asset.get("required") and not asset.get("overlay_safe_area"):
            warnings.append(f"{asset_id}: required asset has no overlay_safe_area")

        purpose = asset.get("purpose")
        if purpose in NARRATIVE_PURPOSES or asset.get("story_state"):
            if not asset.get("required_action") and purpose not in {"cover_hero", "closing_hero"}:
                errors.append(f"{asset_id}: narrative asset missing required_action")
            if "must_show_change" not in asset:
                warnings.append(f"{asset_id}: narrative asset should declare must_show_change")

        character_ids = asset.get("character_ids", [])
        if character_ids:
            ref = asset.get("identity_lock_ref")
            if not ref:
                errors.append(f"{asset_id}: character asset missing identity_lock_ref")
            elif ref not in identity_refs:
                errors.append(f"{asset_id}: unknown identity_lock_ref {ref}")
            for character_id in character_ids:
                if character_id not in characters:
                    errors.append(f"{asset_id}: unknown character_id {character_id}")

        prompt = (asset.get("prompt") or "").lower()
        if any(term in prompt for term in ["watermark", "logo of", "disney", "pixar character"]):
            warnings.append(f"{asset_id}: check IP/watermark wording")

        for slide_id in asset.get("slide_ids", []):
            slide_assets[slide_id].append(asset)

    for asset in data.get("assets", []):
        slide_ids = asset.get("slide_ids", [])
        if len(slide_ids) > 1 and asset.get("reuse_policy") == "anchor_only":
            non_anchor = [
                sid for sid in slide_ids if not sid.upper().endswith(("01", "07", "08", "09", "10"))
            ]
            if non_anchor:
                warnings.append(
                    f"{asset.get('asset_id')}: anchor_only asset reused on possible narrative slides {non_anchor}"
                )

    status = "PASS" if not errors else "BLOCKED"
    return {
        "status": status,
        "asset_count": len(data.get("assets", [])),
        "character_count": len(characters),
        "errors": errors,
        "warnings": warnings,
    }


def main(path: str) -> int:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    result = validate(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
