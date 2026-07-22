# 语义布局注册表

布局不是装饰模板，而是承担教学或演讲动作的页面组件。注册表位于 `assets/registries/layouts.json`。

每个布局记录：`id, role, age_bands, usage_modes, best_for, visual_systems, max_words, max_visible_words, min_font_size_pt, media_slots, supports_reveal, stage_safe, editable_objects`。

推荐查询：

```bash
python scripts/query_layouts.py --role misconception --age 6-8
python scripts/query_layouts.py --age 4-6 --usage child_stage_speech --stage-safe
python scripts/query_layouts.py --keyword 浇水 --visual storybook-warm
```

选择顺序：先匹配使用场景和角色，再匹配年龄、视觉系统和媒体条件。找不到年龄或场景匹配项时应阻断或明确降级，不能静默自由排版。

同一成品允许复用布局家族，但五页以上至少使用三种明显不同、同系统的骨架；避免连续三页完全相同的左右分栏或普通白框。
