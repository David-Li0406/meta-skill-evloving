# Statistical Reference

Data from analysis of 200 Claude Opus 4.5 samples vs 6,000 human texts.

## Punctuation Overuse

| Punctuation | AI Rate (per 1k chars) | Human Rate | Ratio |
|-------------|------------------------|------------|-------|
| Em dash (—) | 4.79 | 0.28 | 16.9x |
| Colon | 4.12 | 1.01 | 4.1x |
| Semicolon | 0.69 | 0.23 | 3.1x |

## Sentence Length Distribution

| Metric | AI | Human |
|--------|-----|-------|
| Mean length | 23.9 words | 19.8 words |
| Coefficient of variation | 137.1% | 70.5% |
| Short sentences (1-10 words) | 39.9% | 23.9% |
| Medium sentences (11-25 words) | 34.1% | 50.3% |
| Long sentences (26+ words) | 26.1% | 25.8% |

Key insight: AI has MORE variation, but it's bimodal (alternating very short/very long). Human writing clusters around medium length.

## Passive Voice

| Metric | AI | Human |
|--------|-----|-------|
| Passive voice usage | 4.7% | 14.9% |

Key insight: AI uses LESS passive voice than humans. Don't over-correct.

## Paragraph Structure

| Metric | AI | Human |
|--------|-----|-------|
| Avg paragraph length | 16.2 words | 209.6 words |
| Paragraphs per document | 18.4 | ~1 |

Key insight: AI fragments into many short paragraphs. Combine related ideas.

## List Usage

| Metric | AI | Human |
|--------|-----|-------|
| List items per document | 9.5 | ~0 |

Key insight: AI overuses bullets. Convert to prose when possible.

## Most Distinctive Words/Phrases

| Pattern | AI vs Human Ratio |
|---------|-------------------|
| comprehensive | 24.5x |
| in essence | very high |
| fundamentally | 17.0x |
| nuanced | 17.0x |
| paradigm | 15.1x |
| robust | 3.1x |
| essentially | 3.1x |

## Patterns NOT Found in Opus 4.5

These classic LLM-isms appear to have been reduced in newer models:
- delve
- tapestry
- vibrant
- myriad

## Multi-Model Comparison

Comparison of 50 samples from each model (January 2026):

### Punctuation by Model (per 1k chars)

| Punctuation | Human | Haiku 3 | Sonnet 3.7 | Sonnet 4 | Opus 4.5 |
|-------------|-------|---------|------------|----------|----------|
| Em dash | 0.28 | 0.00 | 0.23 | 0.25 | 4.78 |
| Colon | 1.01 | 2.43 | 3.90 | 4.68 | 4.11 |
| Semicolon | 0.23 | 0.01 | 0.30 | 0.41 | 0.69 |

Key insight: Em dash overuse is Opus 4.5 specific. Other models are at/below human levels.

### Word Patterns by Model (per 10k chars)

| Word | Human | Haiku 3 | Sonnet 3.7 | Sonnet 4 | Opus 4.5 |
|------|-------|---------|------------|----------|----------|
| comprehensive | 0.06 | 2.24 | 1.71 | 2.15 | 1.39 |
| robust | 0.03 | 1.25 | 0.19 | 0.22 | 0.09 |
| nuanced | 0.00 | 0.00 | 0.30 | 0.15 | 0.04 |
| paradigm | 0.01 | 0.09 | 0.28 | 0.44 | 0.18 |

Key insights:
- Haiku 3 overuses "robust" (43x) and "comprehensive" (40x)
- Sonnet 4 overuses "nuanced" (56x) and "paradigm" (37x)
- Opus 4.5 has relatively lower word overuse but worst em dash problem

## Sentence Starters

AI overuses formulaic starters:

| Starter | AI vs Human Ratio |
|---------|-------------------|
| "This document..." | 623x |
| "Comprehensive..." | 680x |
| "Technical..." | 82x |
| "Introduction..." | 58x |

## Transition Words (Counterintuitive)

AI uses FEWER transitions than humans:

| Metric | AI | Human |
|--------|-----|-------|
| Formal transitions per 100 sentences | 0.3 | 0.9 |
| Casual transitions per 100 sentences | 2.3 | 4.0 |

Only overused: "conversely" (50x), "nevertheless" (8x)

## Hedging Language

AI uses 1.2x more hedging overall. Specific overused words:

| Word | AI per 1k | Human per 1k | Ratio |
|------|-----------|--------------|-------|
| typically | 0.54 | 0.06 | 9.6x |
| often | 1.12 | 0.23 | 4.9x |
| sometimes | 0.47 | 0.11 | 4.2x |
| potentially | 0.15 | 0.04 | 3.4x |
| usually | 0.40 | 0.12 | 3.4x |

## Source

Analysis conducted using log-odds ratios comparing:
- 200 Claude Opus 4.5 samples (47,012 words)
- 50 samples each from Sonnet 4, Sonnet 3.7, Haiku 3
- 6,000 human texts from Wikipedia, OpenWebText, C4 (1,208,418 words)
