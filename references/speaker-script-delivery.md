# 演讲稿 Markdown 与 Word 交付

儿童演讲路线默认把讲稿作为独立、可修改、可打印的正式产物。不要只把台词塞进 PPT 备注，也不要让 Markdown 与 Word 各写一套内容。

## 单一内容源

1. 先从 `slide_spec.json` 生成 `speaker_script.md`。
2. 人工或用户修改时，优先修改 Markdown。
3. 再从同一份 Markdown 编译 `speaker_script.docx`。
4. Word 中记录 Markdown 的 SHA-256，确保两个版本可追溯。

Markdown 是内容母稿；Word 是包装与打印版本。不得在 Word 中另行改写事实、顺序、翻译或动作提示。

## 默认交付

儿童演讲至少交付：

- `stage_deck.pptx`
- `speaker_script.md`
- `speaker_script.docx`
- `qa_report.json`

需要排练时增加 `rehearsal_deck.pptx`。用户明确只要一种讲稿格式时可以减少交付，但不得删除源文件而只保留不可追溯的派生稿。

## Markdown 结构

推荐结构：

```markdown
# My Little Flower / 我的小花

> **Speaker / 演讲者：** Mia
> **Age / 年龄：** 5
> **Duration / 建议时长：** 约 3 分钟
> **Difficulty / 难度：** rich
> **Bilingual mode / 双语模式：** paired_alternating
> **English words / 英文词数：** 252

## 使用建议 / How to Use
- 先读英文，再看中文理解。
- 动作提示只用于排练，不需要逐字念出。

## S01 · My Little Flower / 我的小花
### English
...
### 中文
...
### Stage actions / 舞台动作
- Smile
- Wave
### Rhythm and pronunciation / 节奏与发音
- Pause after “everyone”.
### Editable notes / 可修改备注
> 家长或老师可在这里补充。
```

每个演讲节点必须同时包含英文、中文和动作。节奏与发音提示可选，但正式比赛或双语演讲建议保留。

## Word 包装结构

Word 使用原生段落、样式和表格，确保用户可以直接修改：

1. 封面：题目、演讲者、年龄、时长、难度、双语模式。
2. 使用建议：排练方法、语言切换规则、动作使用原则。
3. 分页讲稿：每个 PPT 节点一个清晰区块，英文与中文并列或上下排列。
4. 舞台动作：独立色块，不混入正文。
5. 节奏与发音：独立提示区。
6. 连贯稿：文末提供纯英文连贯稿和中文参考稿，便于打印背诵。
7. 可修改备注：保留空白区域供家长、老师和孩子手写或编辑。

禁止把整页做成背景图。字体、表格、标题、页眉页脚和提示框都必须保持可编辑。

## 视觉主题

Word 应与 PPT 视觉系统同源，但比 PPT 更克制：

- `paper-theater`：奶油纸、珊瑚粉、鼠尾草绿，适合剪纸、纸片剧场。
- `watercolor-glow`：浅蓝、薰衣草、暖黄，适合水彩与梦幻故事。
- `clean-editorial`：海军蓝、浅灰、珊瑚红，适合较正式的比赛和高年级。

不要嵌入或分发字体文件。优先使用常见字体，并设置中英文字体回退。

## 能力检测与降级

- 有 `python-docx`：生成可编辑 DOCX。
- 有 LibreOffice：渲染 DOCX 为 PNG，逐页检查。
- 无 `python-docx`：至少交付排版清晰的 Markdown，并明确 Word 未生成。
- 无渲染器：可以生成 DOCX，但必须标记为“结构检查通过、视觉未验证”。

## 质量门

Markdown：

- 有标题和元数据。
- 每个节点有英文、中文和动作。
- 词数与 `speech_profile` 一致。
- 不包含本地路径、临时目录或工具内部标记。

Word：

- 能正常打开，段落和表格可编辑。
- 有封面、元数据、分节点讲稿和连贯稿。
- 中英文无缺字、遮挡、截断或表格跨页异常。
- 页眉页脚、页码和边距正常。
- 核心属性中包含 Markdown SHA-256。
- 必须经过 render → inspect → fix → re-render 后才能作为最终交付。
