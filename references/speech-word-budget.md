# Child Speech Word Budget

Use this reference whenever the user asks for a kindergarten or elementary speech deck, bilingual speech, competition speech, show-and-tell, self-introduction, or stage presentation.

## Required intake

Before generation, determine both budgets separately:

1. **Speaker script word budget**: total English words or approximate total bilingual speaking time.
2. **Visible PPT word budget**: how much text should appear on audience slides.

Do not treat these as the same number. The stage deck is visual support; the speaker script may be much richer.

## Defaults

If the user gives no numbers and the environment is interactive, ask one compact question:

> How rich should the speech be?  
> A. light: 60-90 English words, very easy  
> B. standard: 120-170 English words  
> C. rich: 220-300 English words, still child-friendly  
> Or give a target word count.

If the user says to continue or gives a directional change, infer from the latest request and record the assumption in `speech_profile`.

## Difficulty levels

| difficulty | English script words | stage text density | sentence rule |
|---|---:|---|---|
| light | 60-90 | one short cue per slide | 3-7 words per sentence |
| standard | 120-170 | one main cue plus one small support cue | 4-10 words per sentence |
| rich | 220-300 | richer stage cues, but never full paragraphs | 5-12 words per sentence |

Rich mode is not adult mode. Use more concrete child-life details, repeated sentence frames, actions, feelings, and simple transitions. Do not add abstract moralizing, long clauses, or textbook vocabulary.

## PPT visible text budget

For child stage decks, visible text should normally be 25-55% of the spoken English word count, depending on the deck role:

- **audience_support**: 25-35%
- **paired_alternating**: 35-50%
- **rehearsal version**: may include more cues, but separate from the stage deck

When the user asks to increase PPT words by a percentage, update `speech_profile.stage_word_budget` and check the final stage visible words against it with tolerance.

## Strong rule

A stage slide may show cue phrases, key words, or one short sentence. It must not show the complete spoken paragraph unless the user explicitly asks for a reading-first deck.
