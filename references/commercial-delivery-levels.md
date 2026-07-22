# Commercial delivery levels

Use three explicit levels before production.

## quick-draft
Fast structure-first output. Allow code components and limited visual review. Do not claim commercial finish.

## standard-finished
Default public-use quality. Require stable visual system, at least three layout prototypes across the deck, rendered review, geometry audit, editable PPTX, speaker script Markdown and DOCX for speeches.

## commercial-premium
Use for competitions, paid customer delivery, showcase samples, product demos, or when the user asks for commercial quality. Requirements:

1. Produce `art_direction.json` before slide generation.
2. Create or plan a character performance asset set for character-led stories.
3. Generate at least three composition candidates for cover, emotional peak, and closing slides.
4. Run rendered visual review twice: first after rough assembly, again after refinement.
5. Run `score_commercial_quality.py`; every major dimension must be >= 7 and overall >= 8 before claiming commercial quality.
6. Deliver a short `delivery_note.md` explaining output level, unresolved limitations, and editable surfaces.

Never call a deck commercial-premium solely because QA is technically clean. Commercial finish requires memorability, rhythm, typography integration, and a clear visual concept.
