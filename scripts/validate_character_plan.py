#!/usr/bin/env python3
import json
import sys
from pathlib import Path

IDENTITY_FIELDS = {"age", "hair", "outfit", "signature", "face_shape", "render_style"}


def validate(data: dict) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    characters = data.get("character_bible", {}).get("characters", [])
    index: dict[str, dict] = {}

    for char in characters:
        character_id = char.get("character_id")
        if not character_id:
            errors.append("character missing character_id")
            continue
        if character_id in index:
            errors.append(f"duplicate character_id {character_id}")
        index[character_id] = char
        lock = char.get("identity_lock", {})
        missing = IDENTITY_FIELDS - set(lock)
        if missing:
            warnings.append(f"{character_id}: identity_lock missing {sorted(missing)}")
        if not char.get("forbidden_changes"):
            warnings.append(f"{character_id}: forbidden_changes is empty")

    refs: dict[str, list[str]] = {character_id: [] for character_id in index}
    for asset in data.get("assets", []):
        for character_id in asset.get("character_ids", []):
            if character_id not in index:
                errors.append(f"{asset.get('asset_id')}: unknown character_id {character_id}")
            else:
                refs[character_id].append(asset.get("asset_id", "?"))
        if asset.get("character_ids") and not asset.get("identity_lock_ref"):
            errors.append(f"{asset.get('asset_id')}: missing identity_lock_ref")

    for character_id, asset_ids in refs.items():
        if not asset_ids:
            warnings.append(f"{character_id}: character is defined but unused")

    return {
        "status": "PASS" if not errors else "BLOCKED",
        "characters": sorted(index),
        "references": refs,
        "errors": errors,
        "warnings": warnings,
        "visual_identity_verified": False,
        "visual_identity_note": "Structure is validated; pixel-level character identity still requires visual inspection or a capable vision tool.",
    }


def main(path: str) -> int:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    result = validate(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
