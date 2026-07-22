#!/usr/bin/env python3
import argparse
import json
import tempfile
import zipfile
from pathlib import Path

FADE = '<p:transition spd="med" advClick="1"><p:fade/></p:transition>'


def apply_transitions(path: Path, output: Path | None = None) -> dict:
    output = output or path
    temp_output = output
    if output.resolve() == path.resolve():
        handle = tempfile.NamedTemporaryFile(suffix=".pptx", delete=False)
        handle.close()
        temp_output = Path(handle.name)
    changed = 0
    with zipfile.ZipFile(path, "r") as source, zipfile.ZipFile(
        temp_output, "w", compression=zipfile.ZIP_DEFLATED
    ) as target:
        for info in source.infolist():
            payload = source.read(info.filename)
            if info.filename.startswith("ppt/slides/slide") and info.filename.endswith(".xml"):
                text = payload.decode("utf-8")
                if "<p:transition" not in text:
                    if "<p:timing" in text:
                        text = text.replace("<p:timing", FADE + "<p:timing", 1)
                    elif "<p:extLst" in text:
                        text = text.replace("<p:extLst", FADE + "<p:extLst", 1)
                    else:
                        text = text.replace("</p:sld>", FADE + "</p:sld>", 1)
                    payload = text.encode("utf-8")
                    changed += 1
            target.writestr(info, payload)
    if temp_output != output:
        temp_output.replace(output)
    return {"slides_changed": changed, "output": str(output)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply a gentle fade transition to slides without one")
    parser.add_argument("pptx")
    parser.add_argument("--out")
    args = parser.parse_args()
    result = apply_transitions(Path(args.pptx), Path(args.out) if args.out else None)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
