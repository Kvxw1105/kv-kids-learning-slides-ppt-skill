#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

SLIDE_RE = re.compile(r"^##\s+(S\d+)\s*[·.-]\s*(.+?)\s*$")


def count_words(text: str) -> int:
    return len(re.findall(r"\b[A-Za-z]+(?:['’][A-Za-z]+)?\b", text))


def parse_script(text: str) -> dict:
    lines = text.splitlines()
    title = next((line[2:].strip() for line in lines if line.startswith("# ")), "")
    slides = []
    current = None
    subsection = None
    metadata = {}
    for line in lines:
        if line.startswith("> **") and "：**" in line:
            key, value = line[4:].split("：**", 1)
            metadata[key.strip()] = value.strip()
            continue
        match = SLIDE_RE.match(line)
        if match:
            current = {"id": match.group(1), "title": match.group(2), "sections": {}}
            slides.append(current)
            subsection = None
            continue
        if line.startswith("### ") and current:
            subsection = line[4:].strip()
            current["sections"][subsection] = []
            continue
        if current and subsection and line.strip():
            current["sections"][subsection].append(line.strip())
    return {"title": title, "metadata": metadata, "slides": slides}


def section_text(slide: dict, prefixes: tuple[str, ...]) -> str:
    for key, values in slide.get("sections", {}).items():
        if key.lower().startswith(tuple(prefix.lower() for prefix in prefixes)):
            return " ".join(value.lstrip("- ").lstrip("> ") for value in values)
    return ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("markdown")
    args = parser.parse_args()
    path = Path(args.markdown)
    errors = []
    warnings = []
    if not path.exists():
        result = {"status": "BLOCKED", "errors": [f"missing file: {path}"], "warnings": []}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1
    text = path.read_text(encoding="utf-8")
    parsed = parse_script(text)
    if not parsed["title"]:
        errors.append("missing H1 title")
    if not parsed["slides"]:
        errors.append("no Sxx speech sections found")
    total_english = 0
    for slide in parsed["slides"]:
        en = section_text(slide, ("english",))
        zh = section_text(slide, ("中文", "chinese"))
        actions = section_text(slide, ("stage actions", "舞台动作", "actions"))
        if not en:
            errors.append(f"{slide['id']}: missing English section")
        if not zh:
            errors.append(f"{slide['id']}: missing Chinese section")
        if not actions:
            errors.append(f"{slide['id']}: missing stage actions section")
        total_english += count_words(en)
    if "/mnt/data/" in text or "\\Users\\" in text or "/tmp/" in text:
        errors.append("local path leaked into Markdown")
    declared = None
    for key, value in parsed["metadata"].items():
        if "English words" in key or "英文词数" in key:
            match = re.search(r"\d+", value)
            if match:
                declared = int(match.group())
                break
    if declared is not None and abs(declared - total_english) > max(3, declared * 0.03):
        warnings.append(f"declared English words {declared}, calculated {total_english}")
    status = "BLOCKED" if errors else ("PASS_WITH_WARNINGS" if warnings else "PASS")
    result = {
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "title": parsed["title"],
        "slide_sections": len(parsed["slides"]),
        "calculated_english_words": total_english,
        "declared_english_words": declared,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
