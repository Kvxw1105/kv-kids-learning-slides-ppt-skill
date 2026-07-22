# 儿童双语演讲模式

生成前必须确定唯一 `bilingual.mode`。

## 模式

### english_primary

孩子主要讲英文。正式屏幕以英文为主；中文只作为一行辅助或完全放入讲稿。适合英语比赛和英语展示。

### chinese_primary

孩子主要讲中文，英文是短词或一句补充。

### paired_alternating

同一故事节点先英文后中文。屏幕可同时显示一行英文和一行中文，但不能复制完整讲稿。适合幼儿园双语展示。

### english_then_chinese

先完成一段英文，再完成对应中文。适合需要明确语言分段的比赛。

### audience_support

孩子只讲一种语言，屏幕用另一种语言帮助观众理解。

## 结构字段

```json
{
  "bilingual": {
    "mode": "paired_alternating",
    "primary_language": "en",
    "screen_policy": "one_short_line_per_language",
    "speaker_sequence": ["en", "zh"]
  }
}
```

## 硬规则

- `screen.text_blocks[].lang` 必须标明语言。
- `visible_in` 决定文字出现在哪个版本；正式版不显示发音提示。
- 屏幕语言顺序与 `speaker_sequence` 一致。
- 翻译要保持儿童口语自然，不逐字硬译。
- 英文专有名称和拟人昵称在中英文稿中保持一致。
