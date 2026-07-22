# 视觉组件合成器

## 目标

用 PowerPoint 原生形状、代码生成 SVG 与轻量 GIF 补充主插画，降低对 AI 生图的依赖，同时保持可编辑、统一和低成本。

## 视觉来源优先级

1. 能用原生 PPT 形状表达的结构、标签、贴纸和装饰，优先使用原生对象。
2. 需要复用但不适合手工拼形状的图标，使用代码生成 SVG。
3. 需要轻微循环动作时，使用小尺寸透明 GIF，并保留静态降级帧。
4. 只有承担人物、情绪、真实场景或复杂叙事时才调用 AI 生图。

## 页面视觉层

每页从以下层中选择至少四层：

- 背景或舞台框架；
- 主体图片或原生场景；
- 标题与文本容器；
- 代码生成贴纸或结构图形；
- 底部承托、边框或章节标识；
- 轻动效或揭示线索。

留白可以很大，但必须有清晰重心和边界。没有视觉焦点、容器和辅助节奏的空白属于未完成页面。

## 组件计划

在 `slide_spec.json` 的 `visual.component_plan[]` 中声明：

`id, type, x, y, w, h, layer, fill, accent, line, rotation, transparency, text, font_size_pt`。

支持的基础组件：

`flower_sticker, leaf_sprig, butterfly, sparkle_cluster, heart, star, ribbon, scallop_strip, dots, grass, badge`。

坐标使用英寸，基于 13.333 × 7.5 的 16:9 画布。组件不得进入标题、人物脸部、主物体和双语核心句的安全区。

## 推荐命令

```bash
python scripts/compose_visual_components.py slide_spec.json --out slide_spec_composed.json --density balanced
python scripts/build_sticker_pack.py --out-dir generated_stickers
python scripts/build_motion_plan.py slide_spec_composed.json --out motion_plan.json --mode gentle
```

## 装配纪律

- 同一页默认 2–5 个辅助组件；超过 8 个需要说明。
- 同一种角标连续出现不超过三页。
- 贴纸只做节奏与指向，不与主插画争夺注意力。
- 代码组件必须语义命名，并在 PowerPoint 中保持可拆分、改色和缩放。
