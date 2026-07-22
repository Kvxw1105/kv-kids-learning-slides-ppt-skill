#!/usr/bin/env python3
import argparse
import json
import re
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
CP_NS = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
PATH_RE = re.compile(r"(?:/mnt/data/|/home/|file:///|[A-Za-z]:\\Users\\)[^\s\"'<>]+")
GENERIC_NAME = re.compile(
    r"^(?:TextBox|Text|Picture|Image|Rectangle|Rounded Rectangle|Oval|Line|Shape|Group|Freeform|Object)(?:\s|_|-)*\d*$",
    re.IGNORECASE,
)


def slide_number(filename: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", filename)
    return int(match.group(1)) if match else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Remove local path metadata and normalize generic shape names")
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--name-map", help="JSON mapping: slide -> cNvPr id -> semantic name")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    name_map = {}
    if args.name_map:
        name_map = json.loads(Path(args.name_map).read_text(encoding="utf-8"))

    report = {"paths_redacted": 0, "names_changed": 0, "errors": []}
    with zipfile.ZipFile(input_path, "r") as source, zipfile.ZipFile(
        output_path, "w", compression=zipfile.ZIP_DEFLATED
    ) as target:
        for info in source.infolist():
            payload = source.read(info.filename)
            if not info.filename.endswith(".xml"):
                target.writestr(info, payload)
                continue
            try:
                root = ET.fromstring(payload)
                changed = False
                s_num = slide_number(info.filename)
                object_counter = 0
                for node in root.iter():
                    tag = node.tag.rsplit("}", 1)[-1]
                    if tag == "cNvPr":
                        object_counter += 1
                        object_id = node.attrib.get("id", str(object_counter))
                        mapped = name_map.get(str(s_num), {}).get(str(object_id)) if s_num else None
                        current_name = node.attrib.get("name", "")
                        if mapped:
                            node.set("name", mapped)
                            report["names_changed"] += 1
                            changed = True
                        elif s_num and GENERIC_NAME.match(current_name.strip()):
                            node.set("name", f"S{s_num:02d}_Object_{object_counter:02d}")
                            report["names_changed"] += 1
                            changed = True
                        for attr in ("descr", "title"):
                            value = node.attrib.get(attr)
                            if value and PATH_RE.search(value):
                                node.set(attr, "Generated visual asset")
                                report["paths_redacted"] += 1
                                changed = True
                    if node.text and PATH_RE.search(node.text):
                        node.text = PATH_RE.sub("[redacted-local-path]", node.text)
                        report["paths_redacted"] += 1
                        changed = True
                    for attr, value in list(node.attrib.items()):
                        if attr not in {"descr", "title"} and PATH_RE.search(value):
                            node.set(attr, PATH_RE.sub("[redacted-local-path]", value))
                            report["paths_redacted"] += 1
                            changed = True
                payload = ET.tostring(root, encoding="utf-8", xml_declaration=True) if changed else payload
            except Exception as exc:
                report["errors"].append(f"{info.filename}: {exc}")
            target.writestr(info, payload)

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
