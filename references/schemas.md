# 中间产物结构

## course_brief.json

通用字段：

`title, route, subject, age, age_band, grade, duration_minutes, usage_mode, goals[], constraints[], output_mode, output_variants[], visual_mode`

儿童演讲追加：

`speaker_name, speech_duration_seconds, bilingual, viewing_distance_m, story_details, rehearsal_needed`

## lesson_map.json

`phases[]`，每项含 `name, purpose, minutes, target_ids[], slide_roles[], evidence`。

## speech_map.json

`beats[]`，每项含 `id, purpose, duration_seconds, object_or_action, emotion, slide_role, script_intent`。

## visual_plan.json

顶层：`mode, visual_system, capability_snapshot, character_bible, assets[]`。

资产：

`asset_id, slide_ids, purpose, required, source_strategy, aspect_ratio, composition, overlay_safe_area, story_state, required_action, must_show_change, character_ids, identity_lock_ref, reuse_policy, prompt, negative_prompt, status, source`。

## slide_spec.json

顶层推荐字段：

`title, route, usage_mode, audience, aspect_ratio, visual_system, output_variants, bilingual, speech_story, character_bible, slides[]`。

课堂页保留：

`id, role, learning_goal, screen, visual, interaction, teacher, assessment, notes`。

儿童演讲页：

```json
{
  "id": "S03",
  "role": "show-one-object",
  "purpose": "介绍小花的名字和来历",
  "screen": {
    "text_blocks": [
      {
        "id": "S03-line-en",
        "role": "core_line",
        "text": "Her name is Pinky.",
        "lang": "en",
        "font_size_pt": 32,
        "visible_in": ["stage", "rehearsal"]
      },
      {
        "id": "S03-line-zh",
        "role": "translation",
        "text": "她叫小粉。",
        "lang": "zh",
        "font_size_pt": 24,
        "visible_in": ["stage", "rehearsal"]
      }
    ]
  },
  "visual": {
    "layout": "show-one-object",
    "asset_ids": ["pinky-pot"],
    "story_state": "introduction",
    "required_action": "girl holds the flower pot",
    "character_ids": ["speaker-girl-01"]
  },
  "speaker": {
    "script_en": "Her name is Pinky. Grandma gave her to me.",
    "script_zh": "她叫小粉，是外婆送给我的。",
    "actions": ["hold the flower pot"]
  },
  "stage": {
    "duration_seconds": 12,
    "animation_mode": "gentle",
    "reveal_plan": ["hero", "english", "chinese"]
  }
}
```

## asset_manifest.json

`assets[]` 含 `asset_id, file, mime, width, height, sha256, source_type, source_url, license, prompt_hash, approved, character_ids[], used_on_slides[]`。


## Speech profile schema

儿童演讲规格必须包含 `speech_profile`。

```json
{
  "speech_profile": {
    "difficulty": "light | standard | rich",
    "target_duration_seconds": 100,
    "target_english_words": [70, 110],
    "screen_density": "minimal | short_cues | moderate_cues",
    "script_density": "simple | moderate | rich"
  }
}
```

`target_english_words` 是完整英文讲稿的目标词数,不是正式屏幕可见词数。

## speaker_script.md

儿童演讲路线的规范化内容母稿。建议包含：

- H1 标题；
- 演讲者、年龄、时长、难度、双语模式、英文词数、PPT 可见词数和视觉风格；
- 使用建议；
- 每个 `Sxx` 节点的 `English`、`中文`、`Stage actions`、`Rhythm and pronunciation`、`Editable notes`；
- 文末英文连贯稿与中文参考稿。

详细结构见 `references/speaker-script-delivery.md`。

## speaker_script.docx

由 `speaker_script.md` 派生的可编辑 Word。Word 只负责样式、分页、表格、页眉页脚与打印包装，不得重新改写讲稿内容。核心属性 `comments` 中记录：

`source_markdown_sha256=<sha256>`

## visual.component_plan

每页可声明代码生成视觉组件：

```json
{
  "visual": {
    "component_plan": [
      {
        "id": "corner-butterfly",
        "type": "butterfly",
        "x": 11.7,
        "y": 0.5,
        "w": 0.8,
        "h": 0.7,
        "layer": "foreground",
        "fill": "#C9B8F4",
        "accent": "#F6A6C8"
      }
    ],
    "completion": {
      "density": "balanced",
      "intentional_minimalism": false,
      "minimum_layers": 4,
      "base_layers": ["background", "text", "native_scene", "code_components"]
    }
  }
}
```

组件坐标使用 13.333 × 7.5 英寸画布。支持类型见 `assets/registries/visual-components.json`。

## motion_plan.json

`version, mode, safety, slides[]`。每页含 `slide_id, transition, objects[]`，对象含 `target, effect, order, duration_ms`。当前安全效果限定为 `fade, float-up, pop`。
