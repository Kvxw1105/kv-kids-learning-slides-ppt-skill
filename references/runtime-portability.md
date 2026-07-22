# 跨 Agent 运行与能力探测

Skill 不能假设宿主名称等于能力。每次通过真实工具清单和可执行环境判断。

## 能力矩阵

- `image_generate`：原生图片生成或外部生成 MCP。
- `image_edit`：可编辑用户图或统一风格。
- `image_search`：可查询公开图片与来源。
- `pptx_native`：专业幻灯片工具、PptxGenJS 或 python-pptx。
- `pptx_render`：PowerPoint、LibreOffice 或其他渲染器。
- `browser_preview`：HTML 预览、截图与交互测试。
- `file_write`：可创建并交付文件。

## 降级顺序

原生高保真 PPTX → 受约束 HTML→PPTX → 基础可编辑 PPTX → HTML 预览/逐页方案。无文件写入能力时，只输出结构化方案并明确限制。

作图能力缺失时：用户上传 → 搜图 → 外部提示词包 → 无图组件。不要把“没有图片”当成停止教学设计的理由。

## 无图像生成能力时的视觉完成度

宿主没有图像生成工具时，运行 `compose_visual_components.py` 与 `build_sticker_pack.py`。原生场景、代码贴纸和结构容器足以完成多数儿童演讲页；只有人物或复杂叙事画面需要外部图片回传。
