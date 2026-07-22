#!/usr/bin/env python3
import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def has_alpha(image: Image.Image) -> bool:
    return image.mode in {"RGBA", "LA"} or (image.mode == "P" and "transparency" in image.info)


def main() -> int:
    parser = argparse.ArgumentParser(description="Resize, compress and deduplicate slide assets")
    parser.add_argument("manifest")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--write-manifest", required=True)
    parser.add_argument("--max-edge", type=int, default=1600)
    parser.add_argument("--quality", type=int, default=88)
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    root = manifest_path.parent
    output_dir = Path(args.out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    seen: dict[str, dict] = {}
    errors: list[str] = []
    total_before = 0
    total_after = 0

    for asset in manifest.get("assets", []):
        source = Path(asset.get("file", ""))
        if not source.is_absolute():
            source = root / source
        if not source.exists():
            errors.append(f"{asset.get('asset_id')}: missing file {source}")
            continue
        original_hash = sha256_file(source)
        original_bytes = source.stat().st_size
        total_before += original_bytes
        asset["original_sha256"] = original_hash
        asset["original_bytes"] = original_bytes

        if original_hash in seen:
            canonical = seen[original_hash]
            asset.update(
                {
                    "canonical_asset_id": canonical["asset_id"],
                    "optimized_file": canonical["optimized_file"],
                    "sha256": canonical["sha256"],
                    "optimized_bytes": canonical["optimized_bytes"],
                    "deduplicated": True,
                }
            )
            continue

        try:
            with Image.open(source) as image:
                image.load()
                width, height = image.size
                scale = min(1.0, args.max_edge / max(width, height))
                new_size = (max(1, round(width * scale)), max(1, round(height * scale)))
                if new_size != image.size:
                    image = image.resize(new_size, Image.Resampling.LANCZOS)
                alpha = has_alpha(image)
                stem = asset.get("asset_id") or source.stem
                if alpha:
                    output = output_dir / f"{stem}.png"
                    image.convert("RGBA").save(output, format="PNG", optimize=True)
                else:
                    output = output_dir / f"{stem}.jpg"
                    image.convert("RGB").save(
                        output,
                        format="JPEG",
                        quality=args.quality,
                        optimize=True,
                        progressive=True,
                    )
                optimized_hash = sha256_file(output)
                optimized_bytes = output.stat().st_size
                total_after += optimized_bytes
                asset.update(
                    {
                        "optimized_file": str(output),
                        "width": new_size[0],
                        "height": new_size[1],
                        "sha256": optimized_hash,
                        "optimized_bytes": optimized_bytes,
                        "deduplicated": False,
                    }
                )
                seen[original_hash] = {
                    "asset_id": asset.get("asset_id"),
                    "optimized_file": str(output),
                    "sha256": optimized_hash,
                    "optimized_bytes": optimized_bytes,
                }
        except Exception:
            output = output_dir / source.name
            shutil.copy2(source, output)
            optimized_hash = sha256_file(output)
            optimized_bytes = output.stat().st_size
            total_after += optimized_bytes
            asset.update(
                {
                    "optimized_file": str(output),
                    "sha256": optimized_hash,
                    "optimized_bytes": optimized_bytes,
                    "deduplicated": False,
                }
            )
            seen[original_hash] = {
                "asset_id": asset.get("asset_id"),
                "optimized_file": str(output),
                "sha256": optimized_hash,
                "optimized_bytes": optimized_bytes,
            }

    manifest["optimization"] = {
        "max_edge": args.max_edge,
        "quality": args.quality,
        "total_original_bytes": total_before,
        "total_unique_optimized_bytes": total_after,
        "errors": errors,
    }
    Path(args.write_manifest).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(manifest["optimization"], ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
