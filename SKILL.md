---
name: kv-kids-learning-slides
description: Create, adapt, and quality-check child-friendly learning and speaking presentations from a topic, textbook excerpt, lesson plan, source file, existing PPTX, or a child's speech idea. Use for kindergarten or elementary PPT/PPTX, bilingual child speeches, classroom courseware, family tutoring decks, self-study lessons, teacher notes, polished editable Markdown and Word speaker scripts, rehearsal and stage versions, practice and answer versions, editable PowerPoint delivery, educational illustrations, character-consistent image planning, image search or generation, and adapting a user-provided teaching template. The skill senses available image/search/PPTX capabilities, selects one production route, and degrades safely when image generation or rendering is unavailable.
---

# 儿童学习与演讲课件工坊

把模糊主题、教材内容或儿童演讲想法转化为**适龄、可讲、可练、可演、可编辑、经过验收**的 PPTX。内容、教学或演讲、视觉、素材和文件工程必须同时成立。

## 必须按顺序执行

1. 先读 `references/routing.md`，只选择一条顶层路线。
2. 课堂任务读教学契约；儿童舞台演讲任务改读 `references/child-stage-speech.md`、`references/bilingual-speech.md` 与 `references/speech-intake.md`，禁止沿用课堂课件骨架。
3. 演讲路线若未给出时长、词数或难度，先询问 `light / standard / rich` 或目标词数；低 token / Codex / 代理环境中必须先问清楚再生成。
4. 检测当前环境的搜图、作图、PPTX、备注、动画和渲染能力；本地检测可运行 `scripts/detect_capabilities.py`。
5. 生成 `course_brief.json`。课堂路线再生成 `lesson_map.json`；演讲路线生成包含 `speech_profile` 的 `speech_map.json`。
6. 按 `references/visual-assets.md` 决定无图、智能配图或重视觉模式，生成 `visual_plan.json` 与角色圣经。随后运行响应式绘本排版引擎，禁止直接套用固定左右分栏。
7. 运行 `scripts/plan_storybook_layout.py`，为每页选择绘本构图原型、语义区域、主图尺度、文字容器与边缘处理；再做三个代表性 Showcase。
8. 生成统一的 `slide_spec.json`。儿童演讲先派生排版清晰的 `speaker_script.md`，再从该 Markdown 编译可编辑 `speaker_script.docx`；同时派生正式放映版与排练版。
9. 先执行实际 PPTX 几何审查，再渲染 PPTX 与 DOCX。打开缩略图和可疑单页完成视觉自审，修复源规格或生成代码后重新导出，直到几何门与视觉审查门都通过。禁止只修最终文件。

不要从一句主题直接跳到整套 PPTX。不要让 HTML、PPTX、讲稿、排练稿和练习各写一套互相矛盾的内容。

## 顶层路线

- **create-learning-deck**：主题、教材、课文、教案或资料从零生成课堂学习课件。
- **create-child-speech-deck**：幼儿园或小学生演讲、自我介绍、双语展示、故事分享；输出正式放映版与讲稿，必要时输出排练版。
- **fill-child-template**：填充本 Skill 或用户指定的儿童模板。
- **adapt-user-pptx**：读取用户 PPTX，保留或重构其内容与视觉。
- **enhance-learning-deck**：给现有课件补讲稿、互动、练习、答案、配图或质量修复。

路线判断与默认值见 `references/routing.md`。演讲路线必须加载 `references/child-stage-speech.md`。

## 三种视觉生产模式

### 快速模式

适合临时讲解、家庭辅导和短演讲。使用原生形状、少量图标和一至三张关键图。仍要保证适龄、可编辑和可投影。

### 智能配图模式（默认）

先完成内容结构，再只为高价值页面配置图片：封面主视觉、核心解释图、角色连续图和必要题目图。确认视觉方向后自动完成，不逐张打断用户。

### 重视觉工作室模式

适合公开课、正式比赛和精品交付。先提出二至三个真正不同的视觉方向，确认角色与封面后再生产整套资产。

## 能力感知与降级

先检查宿主的真实工具列表，不要假设一定存在图像生成、网页搜图、浏览器、PPTX 渲染器或 MCP。

- 有原生作图能力：按视觉计划生成；角色型故事先锁定角色参考与身份字段。
- 有搜图能力：真实对象、文物、动植物和实验器材优先检索可靠参考并记录授权。
- 只有外部工具或 MCP：按真实接口调用，不虚构连接器。
- 无作图能力：提供原生图形版、用户上传版和外部提示词包。
- 用户仍要生成图片：输出逐资产提示词、比例、动作、留白、身份锁和禁止项，等待回传后继续。

详细流程见 `references/visual-assets.md` 与 `references/character-continuity.md`。

## 课堂教学硬规则

- 每页只承担一个儿童可说出的学习任务。
- 先唤起经验，再制造问题，再观察或操作，再揭示规律，再练习、纠错和迁移。
- 每个学习目标必须对应讲解、练习和验收证据。
- 图像必须参与解释、观察或情绪引导；纯装饰不得争夺注意力。
- 低年级从实物、动作、图示到符号；高年级可以增加结构化文字，但禁止成人汇报式堆字。
- 教师层与屏幕层分离。教师讲法、预期回答、追问和误区写入备注或逐页讲稿。

读 `references/pedagogy-contract.md`、`references/age-cognition-matrix.md`、`references/lesson-architectures.md`。上海小学数学任务应联动 `shanghai-primary-math-generator`。

## 儿童舞台演讲硬规则

- 正式放映版是观众视觉背景，不是提词器和训练卡。
- `speaker_notes`、动作指导和完整讲稿不得复制到正式屏幕。
- 默认输出 `stage_deck.pptx`、`speaker_script.md` 与 `speaker_script.docx`；需要排练时再输出 `rehearsal_deck.pptx`。Markdown 是讲稿内容母稿，Word 只做可编辑包装。
- 四至六岁舞台版任何观众可见文字不得低于 20pt；核心句通常为 28–36pt。
- 一页一个动作、物体、变化或情绪节点；图片必须表现当前故事状态。
- 双语模式、难度档位和目标词数必须显式确定，屏幕、讲稿和切换顺序保持一致。
- 同一角色必须绑定稳定 `character_id` 与 `identity_lock`，不得无说明改变发型、服装、年龄和标志性饰品。

完整规则见 `references/child-stage-speech.md`、`references/bilingual-speech.md`、`references/speech-intake.md`、`references/speaker-script-delivery.md` 与 `references/character-continuity.md`。

## 视觉与布局

从 `assets/registries/visual-systems.json` 选择视觉系统，从 `assets/registries/layouts.json` 查询语义布局：

```bash
python scripts/query_layouts.py --age 4-6 --usage child_stage_speech --stage-safe
python scripts/query_layouts.py --age 7-9 --role guided-discovery --visual block-math-lab
```

每套成品建立 `visual_bible.json`，记录色板、字体层级、形状语言、插图复杂度、角色识别点、背景复杂度、图片留字区和禁止变化。中文文字默认由 PPT 原生对象覆盖，不写进 AI 图片。

Child-stage decks must also select a typography theme from `assets/registries/typography-themes.json`. English and Chinese titles must be designed as one pair; plain black Chinese translation text is not acceptable unless the selected visual system explicitly requires it. Use editable soft echoes, pale shadows, brush underlines, or paper labels instead of heavy effects.

Declare a `composition_profile` and per-slide white-space intent. When a page feels sparse, repair in this order: enlarge the hero, enlarge the type, rebalance zones, add a meaningful container or ground plane, then add a small number of topic-linked code components. Do not begin with random stickers.

Read `references/typography-and-tone.md` and `references/white-space-and-composition.md` for these rules.

详细规范见 `references/visual-systems.md` 与 `references/layout-registry.md`。

### 响应式绘本排版

儿童演讲与低年级绘本课件必须读取 `references/responsive-layout-engine.md` 与 `references/picturebook-art-direction.md`。先测量文字、语言、图片和关键词数量，再选择构图。内容少时放大主图与核心文字；内容多时切换为分镜、三联画、对象星座或图文环绕，禁止保持小对象和大片无职责空白。

```bash
python scripts/plan_storybook_layout.py slide_spec.json --out slide_spec_planned.json --density balanced
python scripts/build_storybook_components.py --out-dir generated_storybook_components --palette watercolor
python scripts/validate_storybook_composition.py slide_spec_planned.json
```

三个以上关键词必须组成花瓣簇、叶片标签、胶囊组或对象星座。英文与中文必须成为一个视觉组合；中文核心句通常为英文的 68%–85%，不得缩成脚注。连续三页不得使用同一构图原型。默认使用云朵气泡、聊天气泡、水彩色块、扯纸、花瓣、叶片与波浪边缘，纯矩形只作为特定清爽编辑风的例外。

开源项目的可吸收经验与许可边界见 `references/open-source-layout-and-picturebook-study.md`。

## 可编辑 PPTX 合约

优先使用宿主专业幻灯片能力或 PptxGenJS。环境受限时可用 `scripts/build_basic_pptx.py`；儿童舞台演讲可用 `scripts/build_child_speech_pptx.py` 生成可编辑的正式版、排练版、Markdown 讲稿与 Word 讲稿。也可单独运行 `scripts/build_speaker_script_docx.py` 将已修改的 Markdown 重新编译为 DOCX。

必须保持原生可编辑：标题、正文、题目、答案、算式、表格、流程、箭头、标签、页码和常规几何图形。复杂绘本场景、角色和自然对象可以是图片；关键知识结构不能整页栅格化。

导出前应运行素材优化和元数据清理：

```bash
python scripts/optimize_assets.py asset_manifest.json --out-dir optimized_assets --write-manifest optimized_manifest.json
python scripts/sanitize_pptx.py input.pptx output.pptx
```

完整规范见 `references/editable-pptx-contract.md`。

## 讲稿 Markdown 与 Word

儿童演讲必须先生成结构清晰、可直接修改的 `speaker_script.md`，再从同一内容源生成 `speaker_script.docx`。Word 应包含封面、元数据、使用建议、逐页双语稿、动作与节奏提示、可修改备注及文末连贯稿。所有内容保持原生可编辑，禁止用整页图片包装。

推荐命令：

```bash
python scripts/build_child_speech_pptx.py slide_spec.json \
  --stage-out stage_deck.pptx \
  --rehearsal-out rehearsal_deck.pptx \
  --script-out speaker_script.md \
  --script-docx-out speaker_script.docx \
  --script-theme paper-theater
```

用户修改 Markdown 后，可重新生成 Word：

```bash
python scripts/build_speaker_script_docx.py speaker_script.md --out speaker_script.docx --theme paper-theater
```

详细规范见 `references/speaker-script-delivery.md`。


## 商业精品生产线 v1.0

当用户提到比赛、公开展示、付费交付、商业级、精品、样板案例、商品页或明确要求高审美时，进入 `commercial-premium`。先读取 `references/commercial-delivery-levels.md`、`references/art-direction-contract.md`、`references/composition-candidate-engine.md`、`references/character-performance-assets.md` 与 `references/commercial-aesthetic-review.md`。

商业精品路线必须先生成 `art_direction.json`，再做角色表演资产计划和关键页多候选构图。不要一次性生成整套后只修补错误；先做封面、情绪高潮页和结尾页三张 Showcase，确认视觉系统成立后再扩展。

商业精品至少执行：

```bash
python scripts/create_art_direction.py speech_map.json --out art_direction.json --level commercial-premium
python scripts/build_character_asset_plan.py art_direction.json --out character_asset_plan.json
python scripts/generate_composition_candidates.py slide_spec.json --art art_direction.json --out composition_candidates.json
python scripts/score_commercial_quality.py --spec slide_spec.json --art art_direction.json --visual-review visual_review/visual_review.json --out commercial_quality_report.json --min-overall 8 --min-dimension 7
```

商业精品交付时必须明确说出：这是草稿、标准成品还是商业精品。技术 QA 通过不等于商业精品，若商业审美评分未达标，只能称为标准成品或待精修稿。

## 标准中间产物

```text
course_brief.json
lesson_map.json | speech_map.json
visual_bible.json
visual_plan.json
asset_manifest.json
slide_spec.json
teacher_notes.md | speaker_script.md
speaker_script.docx
stage_deck.pptx | editable_deck.pptx
rehearsal_deck.pptx (optional)
rendered_slides/
contact_sheet.png
qa_report.json
```

结构见 `references/schemas.md`。课堂样例与演讲样例位于 `assets/sample-lessons/`。

## 质量门

至少执行：

```bash
python scripts/validate_visual_plan.py visual_plan.json
python scripts/validate_slide_spec.py slide_spec.json
python scripts/validate_typography.py slide_spec.json
python scripts/validate_visual_density.py slide_spec.json
python scripts/validate_storybook_composition.py slide_spec.json
python scripts/audit_pptx_geometry.py stage_deck.pptx --profile child_stage_speech --out geometry_report.json
python scripts/prepare_visual_review.py stage_deck.pptx --out-dir visual_review
# 打开 contact_sheet.png 与可疑单页，填写 visual_review/visual_review.json 后：
python scripts/run_quality_gate.py --spec slide_spec.json --visual visual_plan.json --pptx stage_deck.pptx --script-md speaker_script.md --script-docx speaker_script.docx --profile child_stage_speech --visual-review visual_review/visual_review.json --require-visual-review
```

演讲路线会额外执行 `validate_speech_spec.py` 和角色一致性门。PPTX 检查必须覆盖：ZIP 完整性、文件哈希、包体预算、重复媒体、本地路径泄露、最小字号、字体主题、文字颜色、备注、动画计划、对象命名、内容覆盖率、最大连续空白区、矩形支配度、构图原型重复与孤立词汇标签。

先运行 `scripts/audit_pptx_geometry.py` 检查文字与线框、边框、标签和主体的实际坐标关系。若本地存在 LibreOffice，必须运行 `scripts/prepare_visual_review.py` 生成逐页 PNG、总览和绑定产物哈希的视觉审查表；Agent 要亲自打开图片复核并填写结果。正式舞台与重视觉模式在 `run_quality_gate.py` 中使用 `--require-visual-review`。详见 `references/geometry-and-visual-self-review.md` 与 `references/quality-gates.md`。

## 交付

课堂快速模式至少交付 PPTX、教师讲稿和 QA 报告。儿童演讲至少交付正式放映版、Markdown 演讲稿、可编辑 Word 演讲稿和 QA 报告；排练版按需要生成。完整模式再交付结构化规格、资产清单、缩略图总览和来源说明。

如某项受环境限制未完成，明确区分已完成、降级完成和未验证，禁止把概念方案冒充可用文件。

## 来源与边界

本 Skill 的工作流吸收成熟开源 PPT 项目的架构经验，但脚本为独立实现。来源、许可与不可复制边界见 `references/sources-and-licenses.md`。
