# 儿童视觉系统

注册表位于 `assets/registries/visual-systems.json`。

## 共同约束

- 一套成品只使用一个主视觉系统，最多一个辅助章节系统。
- 角色识别点、线条、色板、光照、材质和镜头语言稳定。
- 信息主体与背景对比高，背景复杂度低于主体。
- 幼儿演讲优先大主体、圆润形状、柔和纸艺或绘本容器；禁止连续使用普通办公白框。
- 装饰必须来自故事对象，例如花瓣、叶片、云朵、积木，而不是无关图标堆积。
- 像素游戏风适合闯关和反馈页，不自动覆盖全部知识或演讲页面。

## visual_bible 必填字段

`visual_id, target_age, usage_mode, tone, palette, type_scale, line_style, shape_language, text_container_language, texture, background_complexity, illustration_rules, mascot_or_character, forbidden_changes`。

儿童舞台演讲追加：`stage_distance_m, stage_min_font_pt, character_bible, animation_mode, screen_role`。

## 内置方向

- `storybook-warm`：绘本童趣，幼儿演讲、语文、英语启蒙和生活主题。
- `block-math-lab`：积木数学实验室，数学和逻辑。
- `nature-observation`：自然观察站，科学和自然。
- `paper-culture`：纸艺国风，古诗、传统文化和历史启蒙。
- `clean-classroom`：清爽课堂，高年级、复习和公开课。
- `pixel-quest`：像素闯关，练习、复习和奖励反馈。


## v0.4 premium child-speech visual directions

Do not overfit to one paper-cut look. For formal child speeches, offer or infer one of these higher-finish directions:

1. **premium-paper-theater**: layered paper stage, scalloped curtains, soft shadows, warm cream background, editorial title panels. Best for polished kindergarten speeches.
2. **storybook-watercolor-glow**: soft watercolor garden, hand-painted edges, gentle empty spaces, warm emotions. Best for tender personal stories.
3. **soft-clay-diorama**: clay-like 3D miniatures, rounded objects, tactile toy-world feeling. Best for show-and-tell and playful themes.
4. **felt-craft-classroom**: felt fabric, stitched edges, tactile shapes. Best for preschool and handmade-school themes.
5. **clean-nursery-editorial**: simple but premium white space, pastel editorial typography, fewer illustrations. Best when parents want a more tasteful look.
6. **pastel-game-quest**: small map, badges, path and rewards. Best for practice or competition rehearsal, not for every formal speech.

Each direction must define: title panel grammar, safe text zones, image reuse policy, typography pairing, decorative density, and whether stage text is inside a card, ribbon, cloud, or open blank space.
