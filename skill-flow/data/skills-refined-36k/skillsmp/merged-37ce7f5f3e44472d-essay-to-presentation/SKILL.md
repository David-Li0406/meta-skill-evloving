---
name: essay-to-presentation
description: Use this skill when transforming written essays into spoken presentations and creating complete slide decks from talk tracks.
---

# Essay to Presentation

Transform written essays into spoken word presentations and generate complete slide decks from talk tracks. This skill combines the processes of adapting essays for verbal delivery and building presentation-ready slides.

## When to Use

Invoke when the user:
- Wants to turn an essay into a presentation talk track
- Needs to adapt written content for verbal delivery
- Is preparing a speech from written material
- Has essay-to-speech output and wants slides
- Says "create slides from this talk track"
- Uses `/essay-to-presentation` command

## Transformation Intensity

Default to **full** transformation unless the essay is already conversational.

| Mode | When to Use | Approach |
|------|-------------|----------|
| **Full** (default) | Academic, formal, or dense prose | Aggressive rewrite for natural speech |
| **Light** | Already conversational, personal voice | Preserve author's voice, minimal changes |

**Auto-detect**: If the essay uses "I", contractions, and short sentences, use light mode. If it uses passive voice, complex clauses, and formal language, use full mode.

## Core Process

### 1. Segment the Essay

Break the essay into atomic chunks based on:
- **Existing structure first**: Honor headings, sections, paragraph breaks
- **Argument units**: Each chunk = one coherent point or idea
- **Slide-sized thinking**: Could this chunk support one slide?

### 2. Transform Each Chunk

Convert written prose to spoken language, ensuring clarity and engagement. Use semantic tags to mark key structural moments.

| Written Pattern | Spoken Pattern |
|----------------|----------------|
| "This essay examines..." | "Today I want to share..." |
| "As previously mentioned..." | "Remember when I said..." |
| "It is important to note that..." | "Here's what matters..." |

#### Rhythm and Breath

Vary sentence length deliberately and insert natural pauses to enhance delivery.

### 3. Assess Images (if present)

Identify and evaluate images referenced in the essay. Apply a critical eye to ensure they are presentation-ready.

### 4. Preserve the Connection

Output both the original text and the transformed talk track for each chunk.

## Slide Building Process

### 1. Parse Essay-to-Speech Output

Extract structured data from each section, including original text, talk track, images, and slide ideas.

### 2. Plan Slide Deck

Map semantic tags to slides, ensuring each slide conveys a single idea or point.

| Tag | Slide Type | Typical Visual |
|-----|------------|----------------|
| `[HOOK]` | Title/Opening | Bold statement, striking image |
| `[KEY_POINT]` | Statement | Single phrase, minimal graphic |
| `[EVIDENCE]` | Data | Chart, statistic callout, comparison |

### 3. Handle Images

Process image assessments from essay-to-speech output, determining whether to use, adapt, recreate, or skip each image.

### 4. Generate Output

Create a structured presentation format, including YAML frontmatter, slide index, and individual slide content with speaker notes.

## Output Format

### Structure

```yaml
---
version: 5
title: "Presentation Title"
subtitle: "Optional Subtitle"
author: "Presenter Name"
date: "2025-01-15"
target_minutes: 15
audio_voice: "af_heart"
brand:
  primary: "#557373"
  background: "#F2EFEA"
  text: "#0D0D0D"
sections:
  - id: opening
    name: "Opening"
    color: "#557373"
  - id: problem
    name: "The Problem"
    color: "#6B8E6B"
  - id: solution
    name: "The Solution"
    color: "#C4785A"
  - id: closing
    name: "Closing"
    color: "#557373"
---

## Slides

| # | Slug | Title | Image | Section |
|---|------|-------|-------|---------|
| 1 | hook | The Question | hook.png | opening |
| 2 | problem-1 | What's Broken | problem-chart.png | problem |
| 3 | evidence | The Data | evidence.png | problem |
| 4 | solution | A New Approach | solution.png | solution |
| 5 | action | Your Next Step | cta.png | closing |
```

### Best Practices

1. **Preserve meaning**: The talk track conveys the same arguments, just spoken.
2. **Respect structure**: Don't arbitrarily merge or split the author's sections.
3. **Natural chunking**: Each section should feel like a complete thought.
4. **One idea per slide**: Split dense content for clarity.
5. **High contrast**: Ensure readability from the back row.

## What This Skill Does NOT Do

- Edit or create original essay content
- Design custom graphics
- Record actual audio
- Render final video

## References

- `references/talk-track-v5.md` - Complete format specification
- `references/html-engine.md` - Static HTML slide player
- `references/remotion-video.md` - React video export setup
- `references/voice-options.md` - TTS configuration and comparison
- `references/image-handling.md` - Full image processing workflow
- `references/examples.md` - Complete input→output examples