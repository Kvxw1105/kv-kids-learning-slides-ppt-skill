# White Space and Composition

White space must read as breathing room, not unfinished construction.

## Composition targets

For child-stage speech decks:

- `light`: target occupied coverage 34-46 percent; largest continuous empty region below about 48 percent.
- `balanced`: target occupied coverage 42-58 percent; largest continuous empty region below about 40 percent.
- `rich`: target occupied coverage 50-66 percent; largest continuous empty region below about 34 percent.

These are soft visual targets, not a reason to fill every corner.

## Repair order for sparse pages

1. Enlarge the hero illustration or native scene.
2. Enlarge the title or core bilingual line.
3. Rebalance the text and image zones.
4. Add a meaningful container, ground plane, border, or story object.
5. Add a small number of code-generated stickers tied to the topic.

Do not begin by scattering unrelated stickers.

## Required completion fields

Each slide may declare `visual.completion.target_coverage_ratio`, `max_empty_region_ratio`, `hero_scale_ratio`, `text_scale_ratio`, `white_space_intent`, and `fill_strategy`. The renderer and QA tools should use these values when available.

## Blocking failures

Block release when a non-minimal slide has a tiny hero, undersized text, low occupied coverage, or one very large empty connected region without an explicit compositional reason.
