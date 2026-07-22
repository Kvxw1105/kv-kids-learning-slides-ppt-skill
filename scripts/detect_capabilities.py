#!/usr/bin/env python3
import argparse
import importlib.util
import json
import os
import shutil
import subprocess


def has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def node_has(package: str) -> bool:
    if not shutil.which("node"):
        return False
    probe = subprocess.run(
        ["node", "-e", f"try{{require.resolve('{package}');process.exit(0)}}catch(e){{process.exit(1)}}"],
        capture_output=True,
    )
    return probe.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hint", action="append", default=[])
    args = parser.parse_args()
    hints = {item.strip().lower() for item in args.hint}
    result = {
        "local": {
            "python_pptx": has_module("pptx"),
            "python_docx": has_module("docx"),
            "pillow": has_module("PIL"),
            "libreoffice": bool(shutil.which("libreoffice") or shutil.which("soffice")),
            "docx_render": bool(shutil.which("libreoffice") or shutil.which("soffice")),
            "node": bool(shutil.which("node")),
            "npm": bool(shutil.which("npm")),
            "pptxgenjs": node_has("pptxgenjs"),
            "speaker_notes_python_pptx": has_module("pptx"),
            "image_optimization": has_module("PIL"),
        },
        "host_declared": {
            "image_generate": "image-generate" in hints or os.getenv("KIDS_SLIDES_IMAGE_GENERATE") == "1",
            "image_search": "image-search" in hints or os.getenv("KIDS_SLIDES_IMAGE_SEARCH") == "1",
            "browser_preview": "browser-preview" in hints or os.getenv("KIDS_SLIDES_BROWSER_PREVIEW") == "1",
            "pptx_native": "pptx-native" in hints or os.getenv("KIDS_SLIDES_PPTX_NATIVE") == "1",
            "pptx_animation": "pptx-animation" in hints or os.getenv("KIDS_SLIDES_PPTX_ANIMATION") == "1",
        },
        "warning": "A local script cannot discover ChatGPT/Claude/Codex host tools reliably; inspect the actual Agent tool list first.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
