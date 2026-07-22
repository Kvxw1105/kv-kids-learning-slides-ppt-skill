# 角色连续性与身份锁

## 一、角色圣经

角色型课件必须建立 `character_bible.characters[]`：

```json
{
  "character_id": "speaker-girl-01",
  "role": "speaker-avatar",
  "identity_lock": {
    "age": 5,
    "hair": "short brown hair",
    "outfit": "pink dress",
    "signature": "pink flower hair clip",
    "face_shape": "round",
    "render_style": "soft pastel storybook"
  },
  "forbidden_changes": ["hair color", "outfit", "age", "signature accessory"]
}
```

同一故事线不得无说明改变年龄、发型、服装、脸型和标志性饰品。

## 二、视觉资产绑定

包含人物的 `visual_plan.assets[]` 必须填写：

- `character_ids[]`
- `identity_lock_ref`
- `story_state`
- `required_action`
- `reuse_policy`

封面候选确认后，将其作为角色参考。后续生成优先使用图像参考、种子或宿主支持的角色一致性方式；不支持时重复完整身份锁提示词。

## 三、复用规则

- 同一张主图可在封面与结束页有意呼应。
- 叙事连续页默认不得复用同一主图冒充不同动作。
- `reuse_policy: anchor_only` 只允许在封面、章节或结束页使用。
- `reuse_policy: narrative_repeat` 必须说明其叙事目的。

## 四、自动检查边界

脚本只能检查结构化身份锁、引用和复用规则，不能凭空保证像素层面的同一人物。若宿主可做视觉比较，应额外检查发型、服装、年龄、脸型和标志物；无法检查时在 QA 标为 `unverified_visual_identity`，不得宣称已验证。
