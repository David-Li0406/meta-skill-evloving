---
name: essay-to-presentation
description: Use this skill when you need to transform written essays into engaging spoken presentations and corresponding slide decks.
---

# Essay to Presentation

Transform written essays into spoken word presentations and complete slide decks. This skill outputs both the original text and a talk track, ready for presentation.

## When to Use

Invoke when you:
- Want to turn an essay into a presentation talk track
- Need to adapt written content for verbal delivery
- Are preparing a speech from written material
- Have essay-to-speech output and want to create slides
- Use `/essay-to-presentation` command

## Core Process

### 1. Transform Essay to Speech

#### Segment the Essay

Break the essay into atomic chunks based on:
- **Existing structure first**: Honor headings, sections, paragraph breaks
- **Argument units**: Each chunk = one coherent point or idea
- **Slide-sized thinking**: Could this chunk support one slide?

Typical segmentation:
- Introduction → Opening hook chunk
- Each major section → 1-3 chunks depending on density
- Conclusion → Landing chunk

#### Transform Each Chunk

Convert written prose to spoken language:

| Written Pattern | Spoken Pattern |
|----------------|----------------|
| "This essay examines..." | "Today I want to share..." |
| "As previously mentioned..." | "Remember when I said..." |
| "It is important to note that..." | "Here's what matters..." |
| "In conclusion, this paper has demonstrated..." | "So what does this mean for you?" |
| Complex nested clauses | Shorter, punchier sentences |
| Passive voice | Active voice |
| Academic hedging | Confident assertions |
| Dense paragraphs | Breathing room, varied rhythm |

### 2. Build Presentation Slides

#### Parse Essay-to-Speech Output

Extract structured data from each section:

```
Section → {
  title: string,
  original: string,
  talkTrack: TaggedContent[],
  images: ImageAssessment[],
  slideIdeas: string[]
}
```

**Semantic tags to identify:**
- `[HOOK]` - Opening attention-grabber → Title/hook slide
- `[KEY_POINT]` - Core argument → Statement slide
- `[EVIDENCE]` - Data/proof → Data visualization slide
- `[STORY]` - Narrative → Story/quote slide
- `[TRANSITION]` - Bridge → Section divider or no slide
- `[CALLBACK]` - Reference → Recap element
- `[LANDING]` - Conclusion → Summary slide
- `[CTA]` - Call to action → Action slide

#### Plan Slide Deck

Map semantic tags to slides:

| Tag | Slide Type | Typical Visual |
|-----|------------|----------------|
| `[HOOK]` | Title/Opening | Bold statement, striking image |
| `[KEY_POINT]` | Statement | Single phrase, minimal graphic |
| `[EVIDENCE]` | Data | Chart, statistic callout, comparison |
| `[STORY]` | Story | Photo, quote attribution, timeline |
| `[TRANSITION]` | Divider (optional) | Section title, progress indicator |
| `[CALLBACK]` | Recap | Reference to earlier slide |
| `[LANDING]` | Summary | Key takeaways, visual recap |
| `[CTA]` | Action | Contact info, next steps, QR code |

**Slide count heuristic:**
- 1-2 slides per `[KEY_POINT]`
- 1 slide per `[EVIDENCE]` block
- Section dividers are optional (skip for tight decks)
- Target: 1 slide per 45-60 sec