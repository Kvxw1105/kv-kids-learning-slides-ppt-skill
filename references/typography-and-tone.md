# Typography and Tone System

Typography is a primary visual layer, not a final formatting step. Child decks must not look like text copied from a word processor.

## Required decisions

Every child-stage speech deck must select one typography theme from `assets/registries/typography-themes.json`. The theme controls English title, Chinese title, English core line, Chinese core line, labels, colors, and subtle effects.

## Rules

- Do not use pure black for child-stage titles or visible bilingual core lines unless the visual system explicitly requires it.
- Pair English and Chinese typefaces intentionally. They may differ, but must share weight, softness, and visual era.
- Use no more than four font families and five visible text colors in one deck.
- Chinese titles need the same visual attention as English titles. Do not treat Chinese as a small black translation line.
- Use subtle rendering only: a soft editable echo, a pale shadow duplicate, a brush underline, or a light paper label. Avoid heavy outlines, bevels, neon glows, and dense drop shadows.
- Place type inside a designed zone. The text box, illustration, and decorative components must form one composition.
- Increase text scale before filling a large empty region with random stickers.
- For age 4-6 stage decks, titles are usually 34-48pt and core lines 26-38pt.

## Font fallback

Do not bundle or distribute font files. Store ordered fallback lists. Prefer a theme font when available and use a common installed fallback when it is not. The final QA report should state the requested font families so another agent can check substitution risk.

## Watercolor direction

For `storybook-watercolor-glow`, prefer a serif or storybook English title, a soft Chinese serif or rounded sans title, rose and moss colors, and a pale echo effect. Avoid plain black Chinese text and office-default alignment.
