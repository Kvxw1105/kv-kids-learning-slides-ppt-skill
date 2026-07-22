# 多质量门

总体状态不能只由“文件能打开”决定。

## 内容门

- 事实、教材、术语、数量、算式、翻译和答案一致。
- 课堂路线每个学习目标有讲解、练习和验收。
- 演讲路线至少有一个具体细节、一个动作和一个情绪变化。

## 场景门

- 课堂、舞台演讲和家庭排练的页面角色正确。
- 正式演讲版不显示教师提示、训练指令或完整讲稿。
- 输出版本与用户要求一致。

## 年龄门

- 认知路径、句长、可见文字数量和字号符合年龄。
- 四至六岁舞台版任何观众可见文字不低于 20pt。
- 内容过多时拆页，不靠缩字解决。

## 双语与演讲门

- 双语模式唯一且显式。
- 屏幕语言顺序、讲稿顺序和停留时间一致。
- 每页一个故事节点，节奏可表演。
- 正式版与排练版的可见信息严格分离。

## 视觉门

- 三秒看出焦点和当前动作。
- 图片表现当前故事状态，不能只做主题相关装饰。
- 角色身份锁一致；无法视觉验证时标记未验证。
- 无遮挡、溢出、断图、低清拉伸和重复骨架疲劳。

## 工程门

- PPTX 可打开，页面数正确，关键对象原生可编辑。
- 记录 PPTX SHA-256、生成脚本或规格来源。
- 无本地绝对路径、用户名和临时目录泄露。
- 关键对象语义命名，不全部为 `Text 1`、`Image 2`。
- 包体符合预算，媒体按哈希去重；七页、三张主图的演讲稿建议不超过 5MB。
- 有条件时通过实际渲染；动画未实现时明确写入限制。

## 发布状态

QA 应输出分门状态：`content_gate, scenario_gate, age_gate, speech_gate, visual_gate, engineering_gate`。

- `PASS`：所有关键门通过。
- `PASS_WITH_WARNINGS`：可用，只有非阻断限制。
- `BLOCKED`：任一关键门失败；例如场景误路由、正式版显示讲稿、舞台字号过小、角色严重矛盾、文件损坏或本地路径泄露。

报告必须绑定当前产物哈希，禁止把旧检查结果用于新文件。


## 儿童演讲难度质量门

演讲路线检查 `speech_profile`。缺少 `difficulty`、缺少目标时长/目标词数、或英文完整稿严重偏离目标词数时,状态为 BLOCKED 或 WARN。屏幕短句规则与字号规则仍然独立执行。

布局安全区检查必须关注标签与原生图案是否重叠。`before-and-after`、`weather-pair` 等带标签的布局,标签应放在明确留白区或卡片标题区,不得压在花盆、太阳、云、人物脸部等主体上。


## v0.4 content and layout gates

Child speech QA must check both spoken and visible word budgets.

- `total_english_words` should fit `speech_profile.target_english_words` with tolerance.
- `stage_visible_english_words` should fit `speech_profile.stage_word_budget` with tolerance.
- If the user asks for a relative increase, the explicit converted budget must be recorded in `speech_profile.assumptions`.
- Text boxes must stay in verified blank zones and must not cover faces, flower heads, action objects, or before/after labels.
- Mature style mode requires at least one non-default typography treatment: title ribbon, cloud card, paper label, editorial side rail, or layered stage panel.

## 讲稿文档门

儿童演讲默认同时检查 Markdown 与 Word：

- `speaker_script.md` 是内容母稿，每个 Sxx 节点必须有英文、中文和动作。
- `speaker_script.docx` 必须从当前 Markdown 派生，核心属性记录 Markdown SHA-256。
- Word 必须使用原生段落、样式和表格，允许用户修改；禁止整页背景图包装。
- Word 至少包含封面、元数据、使用建议、分页讲稿和连贯排练稿。
- Word 中不得出现本地路径、临时目录、工具内部标记或缺失字体造成的方框。
- 最终 DOCX 必须实际渲染为 PNG，并逐页检查无截断、重叠、跨页断裂、表格错位和页眉页脚异常。
- 无 DOCX 生成能力时，Markdown 可以作为降级交付，但发布状态必须说明 Word 未生成。
- 无 DOCX 渲染能力时，允许结构检查通过，但必须标记视觉未验证。

## v0.6 视觉完成度门

- 非刻意极简页面至少具有四个视觉层。
- 没有 AI 图片时，必须存在原生场景或代码视觉组件。
- 默认每页 2–5 个辅助组件；超过 8 个给出装饰过密警告。
- PPTX 实际检查估算内容覆盖率。覆盖率低于约 16% 且有效对象少于 5 个时阻止发布；16%–24% 且对象较少时给出警告。
- 留白必须服务焦点、动作或节奏，不能只是没有完成排版。
- 轻动效计划每页最多 6 个对象，只允许淡入、轻微上浮和弹出；动画能力不可用时交付静态版与 sidecar 计划。

## 几何门与视觉自审门

结构化规格通过后，仍必须检查实际 PPTX。

- 几何门检查文字框与分隔线、边框、手绘下划线、标签和故事主体的实际坐标关系。
- 文字与细线至少保留 0.06 英寸净距；标题与装饰线建议 0.10 英寸以上。
- 几何门通过不代表视觉门通过。字体替换、实际字形、阴影、重心和细微压线必须通过渲染截图复核。
- 正式演讲、比赛和重视觉模式必须生成逐页 PNG 与 contact sheet，由 Agent 逐页填写 `visual_review.json`。
- 视觉审查报告必须绑定当前 PPTX SHA-256；PPTX 发生任何改动后，旧报告立即失效。
- 任一页面标记 `BLOCKED`、未审查或审查图片缺失时，不得发布。

命令见 `references/geometry-and-visual-self-review.md`。
