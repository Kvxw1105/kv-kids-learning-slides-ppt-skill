#!/usr/bin/env python3
import json
import re
import sys
from collections import Counter
from pathlib import Path

VALID_DIFFICULTIES = {"light", "standard", "rich"}

VALID_MODES = {
    "english_primary",
    "chinese_primary",
    "paired_alternating",
    "english_then_chinese",
    "audience_support",
}
TRAINING_MARKERS = (
    "say:",
    "说：",
    "speak slowly",
    "teacher tip",
    "老师提示",
    "排练提示",
)
NARRATIVE_ROLES = {
    "object-introduction",
    "action",
    "supporting-condition",
    "change",
    "emotion",
    "sequence",
}


def words(text: str) -> int:
    english = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text)
    chinese = re.findall(r"[\u4e00-\u9fff]", text)
    return len(english) + len(chinese)


def gate(status: str, errors: list[str], warnings: list[str]) -> dict:
    return {"status": status, "errors": errors, "warnings": warnings}


def validate(data: dict) -> dict:
    scenario_errors: list[str] = []
    scenario_warnings: list[str] = []
    age_errors: list[str] = []
    age_warnings: list[str] = []
    speech_errors: list[str] = []
    speech_warnings: list[str] = []
    bilingual_errors: list[str] = []
    bilingual_warnings: list[str] = []
    profile_errors: list[str] = []
    profile_warnings: list[str] = []

    usage = data.get("usage_mode")
    route = data.get("route")
    if usage != "child_stage_speech" and route != "create-child-speech-deck":
        scenario_errors.append("speech validator requires child_stage_speech usage or create-child-speech-deck route")

    variants = set(data.get("output_variants", []))
    if "stage" not in variants:
        scenario_errors.append("output_variants must include stage")
    if not ({"speaker_script", "notes"} & variants):
        scenario_errors.append("output_variants must include speaker_script or notes")

    audience = data.get("audience", {})
    age_band = audience.get("age_band") or data.get("age_band")
    if age_band not in {"4-6", "6-8"}:
        age_warnings.append(f"unusual child speech age_band: {age_band!r}")

    speech_profile = data.get("speech_profile", {})
    difficulty = speech_profile.get("difficulty")
    if difficulty not in VALID_DIFFICULTIES:
        profile_errors.append(f"invalid or missing speech_profile.difficulty: {difficulty!r}")
    target_words = speech_profile.get("target_english_words")
    target_duration = speech_profile.get("target_duration_seconds")
    stage_word_budget = speech_profile.get("stage_word_budget")
    if not target_words and not target_duration:
        profile_errors.append("speech_profile requires target_english_words or target_duration_seconds")
    if target_words and (not isinstance(target_words, list) or len(target_words) != 2):
        profile_errors.append("speech_profile.target_english_words must be [min, max]")
    if stage_word_budget and (not isinstance(stage_word_budget, list) or len(stage_word_budget) != 2):
        profile_errors.append("speech_profile.stage_word_budget must be [min, max]")

    bilingual = data.get("bilingual", {})
    mode = bilingual.get("mode")
    if mode not in VALID_MODES:
        bilingual_errors.append(f"invalid or missing bilingual.mode: {mode!r}")
    sequence = bilingual.get("speaker_sequence", [])
    if mode == "paired_alternating" and sequence != ["en", "zh"]:
        bilingual_warnings.append("paired_alternating normally uses speaker_sequence ['en', 'zh']")

    story = data.get("speech_story", {})
    for field in ("specific_object", "action", "emotion_change"):
        if not story.get(field):
            speech_errors.append(f"speech_story missing {field}")

    characters = {
        c.get("character_id")
        for c in data.get("character_bible", {}).get("characters", [])
        if c.get("character_id")
    }
    slides = data.get("slides", [])
    layout_ids: list[str] = []
    total_duration = 0
    total_english_words = 0
    stage_visible_english_words = 0
    previous_stage_text: str | None = None

    for index, slide in enumerate(slides, 1):
        sid = slide.get("id", f"slide-{index}")
        layout = slide.get("visual", {}).get("layout")
        if layout:
            layout_ids.append(layout)

        blocks = slide.get("screen", {}).get("text_blocks", [])
        if not blocks:
            scenario_errors.append(f"{sid}: child speech slide requires screen.text_blocks")
            continue
        stage_blocks = [b for b in blocks if "stage" in b.get("visible_in", ["stage"])]
        if len(stage_blocks) > 2:
            age_errors.append(f"{sid}: stage has {len(stage_blocks)} visible text blocks; max is 2")

        stage_texts = []
        langs = set()
        for block in stage_blocks:
            text = str(block.get("text", "")).strip()
            stage_texts.append(text)
            if block.get("lang") == "en":
                stage_visible_english_words += len(re.findall(r"[A-Za-z]+(?:\'[A-Za-z]+)?", text))
            lang = block.get("lang")
            if lang:
                langs.add(lang)
            font_size = block.get("font_size_pt")
            if not isinstance(font_size, (int, float)):
                age_errors.append(f"{sid}/{block.get('id','?')}: missing font_size_pt")
            elif font_size < 20:
                age_errors.append(f"{sid}/{block.get('id','?')}: stage font {font_size}pt is below 20pt")
            if words(text) > 12:
                age_warnings.append(f"{sid}/{block.get('id','?')}: visible line may be too long ({words(text)} units)")
            lowered = text.lower()
            if any(marker in lowered for marker in TRAINING_MARKERS):
                scenario_errors.append(f"{sid}: training instruction is visible in stage text: {text!r}")

        combined_stage = " | ".join(stage_texts)
        if previous_stage_text and combined_stage and combined_stage == previous_stage_text:
            speech_warnings.append(f"{sid}: repeats the previous slide's stage text")
        previous_stage_text = combined_stage

        if mode == "paired_alternating" and not {"en", "zh"}.issubset(langs):
            bilingual_warnings.append(f"{sid}: paired_alternating stage lacks both en and zh blocks")

        speaker = slide.get("speaker", {})
        script_en = str(speaker.get("script_en", "")).strip()
        script_zh = str(speaker.get("script_zh", "")).strip()
        if not (script_en or script_zh):
            speech_errors.append(f"{sid}: missing speaker script")
        total_english_words += len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", script_en))
        if mode in {"english_primary", "paired_alternating", "english_then_chinese"} and not script_en:
            bilingual_errors.append(f"{sid}: bilingual mode requires script_en")
        if mode in {"chinese_primary", "paired_alternating", "english_then_chinese"} and not script_zh:
            bilingual_errors.append(f"{sid}: bilingual mode requires script_zh")
        for sentence in re.split(r"[.!?]+", script_en):
            if len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", sentence)) > 12:
                speech_warnings.append(f"{sid}: English sentence may be hard for a young child: {sentence.strip()!r}")

        visual = slide.get("visual", {})
        if slide.get("role") in NARRATIVE_ROLES:
            if not visual.get("story_state"):
                speech_errors.append(f"{sid}: narrative slide missing visual.story_state")
            if not visual.get("required_action") and slide.get("role") not in {"supporting-condition", "change"}:
                speech_errors.append(f"{sid}: narrative slide missing visual.required_action")
        for character_id in visual.get("character_ids", []):
            if character_id not in characters:
                speech_errors.append(f"{sid}: unknown character_id {character_id}")

        duration = slide.get("stage", {}).get("duration_seconds", 0)
        if isinstance(duration, (int, float)):
            total_duration += duration
        else:
            speech_warnings.append(f"{sid}: invalid duration_seconds")

        full_script = f"{script_en} {script_zh}".strip()
        if full_script and len(combined_stage) > 25 and combined_stage in full_script:
            scenario_warnings.append(f"{sid}: screen may be copying too much of the complete script")

    if len(slides) >= 5 and len(set(layout_ids)) < 3:
        scenario_errors.append("five-or-more-slide speech deck must use at least three distinct layouts")
    if total_duration and not (45 <= total_duration <= 240):
        speech_warnings.append(f"total planned duration {total_duration}s is unusual for a short child speech")
    if isinstance(target_words, list) and len(target_words) == 2:
        lo, hi = target_words
        if isinstance(lo, (int, float)) and isinstance(hi, (int, float)):
            soft_lo = int(lo * 0.85)
            soft_hi = int(hi * 1.15)
            if total_english_words < soft_lo or total_english_words > soft_hi:
                profile_warnings.append(
                    f"English script word count {total_english_words} is outside target range {lo}-{hi} with 15% tolerance"
                )

    if isinstance(stage_word_budget, list) and len(stage_word_budget) == 2:
        lo, hi = stage_word_budget
        if isinstance(lo, (int, float)) and isinstance(hi, (int, float)):
            soft_lo = int(lo * 0.85)
            soft_hi = int(hi * 1.15)
            if stage_visible_english_words < soft_lo or stage_visible_english_words > soft_hi:
                profile_warnings.append(
                    f"Stage visible English word count {stage_visible_english_words} is outside target range {lo}-{hi} with 15% tolerance"
                )

    gates = {
        "scenario_gate": gate("BLOCKED" if scenario_errors else "PASS", scenario_errors, scenario_warnings),
        "age_gate": gate("BLOCKED" if age_errors else "PASS", age_errors, age_warnings),
        "speech_gate": gate("BLOCKED" if speech_errors else "PASS", speech_errors, speech_warnings),
        "bilingual_gate": gate("BLOCKED" if bilingual_errors else "PASS", bilingual_errors, bilingual_warnings),
        "speech_profile_gate": gate("BLOCKED" if profile_errors else "PASS", profile_errors, profile_warnings),
    }
    errors = scenario_errors + age_errors + speech_errors + bilingual_errors + profile_errors
    warnings = scenario_warnings + age_warnings + speech_warnings + bilingual_warnings + profile_warnings
    return {
        "status": "PASS" if not errors else "BLOCKED",
        "slide_count": len(slides),
        "planned_duration_seconds": total_duration,
        "total_english_words": total_english_words,
        "stage_visible_english_words": stage_visible_english_words,
        "distinct_layouts": sorted(set(layout_ids)),
        "gates": gates,
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
