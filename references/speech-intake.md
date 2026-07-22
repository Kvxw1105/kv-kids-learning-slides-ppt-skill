# 儿童演讲难度与词汇量询问协议

## 目标

儿童演讲不能只按年龄自动压到极短。年龄决定底线,但演讲词汇量、句长和难度应由用户目标热插拔控制。

## 何时必须询问

当用户要做幼儿园、小学生、双语演讲、自我介绍、故事分享、比赛展示或舞台发言,且没有明确说明时长、词数或难度时,先用一个简短选择问题锁定目标。

低 token / Codex / 代理环境中,优先先问清楚再生成,不要先做一版再大改。

## 建议问法

```text
先确认演讲难度和长度,这样我不会把内容写得太少或太难:
A. 轻量版: 60-90 秒,英文约 45-70 词,句子很短
B. 标准版: 90-120 秒,英文约 70-110 词,适合幼儿园展示
C. 丰富版: 2-3 分钟,英文约 110-180 词,表达更完整但仍然幼儿可背
也可以直接告诉我目标总词数或比赛时长。
```

若用户已经要求“节省 token”“Codex”“先问清楚”,必须提出上面的问题,不要自行假设。

## 默认值

用户没有指定且不能追问时,默认选择 `standard`。

```json
{
  "speech_profile": {
    "difficulty": "standard",
    "target_duration_seconds": 100,
    "target_english_words": [70, 110],
    "screen_density": "short_cues",
    "script_density": "moderate"
  }
}
```

## 难度档位

### light

适合第一次登台或英语基础弱的孩子。英文 45-70 词,每句 3-6 词。屏幕只放关键词和超短句。

### standard

适合幼儿园正式双语展示。英文 70-110 词,每句 4-8 词,可以有少量形容词、动作和感受。

### rich

适合比赛、公开展示或表达能力较强的孩子。英文 110-180 词,每句 5-10 词,可以加入一个小细节、一个转折或一个观众互动。屏幕仍保持短句,完整内容放入讲稿和备注。

## 屏幕与讲稿分离

提高词汇量不等于把更多文字放到 PPT 上。

- `screen_density` 控制观众看到的文字量。
- `script_density` 控制孩子实际讲的完整稿。
- 正式舞台版默认只显示关键词或短句。
- 排练版可以显示更多提示。
- 完整稿写入 `speaker_script.md` 和备注。

## 验收

- `speech_profile.difficulty` 必须存在。
- `target_english_words` 或 `target_duration_seconds` 至少存在一个。
- 生成后检查英文讲稿总词数是否落入目标区间;允许 15% 浮动。
- 屏幕文字仍必须符合 4-6 岁最小字号和短句规则。


## v0.4 word-budget intake

For child speeches, always separate two budgets:

- `target_english_words`: total English words in the speaker script.
- `stage_word_budget`: visible English cue words on the stage deck.

Ask one compact question when the user has not provided enough information, especially in Codex or low-token environments:

> 这次演讲想要多长？可以选：A 轻量 60-90 英文词，B 标准 120-170 英文词，C 丰富 220-300 英文词。PPT屏幕文字要少、中等，还是比上一版多 40%？

If the user gives a relative instruction, convert it into explicit numbers and store the assumption in `speech_profile.assumptions`.

Load `references/speech-word-budget.md` before writing the script.
