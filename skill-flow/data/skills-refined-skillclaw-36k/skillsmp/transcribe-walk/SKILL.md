---
name: transcribe-walk
description: "Process walk recordings into usable research material. Transcription workflow, insight extraction, integration with pipeline. Use after WALK stage recording."
---

# Transcribe Walk Skill

**Purpose:** Convert walk recordings into structured research material.

---

## When to Use

After a walk recording is complete, before advancing to OUTLINE stage.

---

## The Workflow

```
Recording → Transcription → Cleanup → Extraction → Integration
```

### 1. Recording

**During the walk:**
- Voice memo app on phone
- Walk-and-talk guide visible for reference
- Stream of consciousness is fine
- Tangents are often the insights

**Ideal recording:**
- 20-45 minutes
- Captures responses to guide questions
- Includes spontaneous thoughts
- Natural pauses are fine

### 2. Transcription

**Options:**

| Method | Pros | Cons |
|--------|------|------|
| **Whisper (local)** | Private, free, accurate | Requires setup |
| **Otter.ai** | Easy, good quality | Cloud, subscription |
| **Built-in (iOS/Android)** | Convenient | Variable quality |
| **Manual** | Perfect accuracy | Time-consuming |

**Whisper command:**
```bash
whisper recording.m4a --model medium --language en --output_format txt
```

**Output:** Raw transcript in `pipeline/active/NNN-slug/03-walk-raw.txt`

### 3. Cleanup

The raw transcript needs light editing:
- Fix obvious transcription errors
- Add paragraph breaks at topic shifts
- Mark unclear sections with [?]
- Don't over-edit - preserve natural speech

**Output:** Cleaned transcript in `pipeline/active/NNN-slug/03-walk-transcript.md`

### 4. Extraction

Pull out the valuable material:

```markdown
# Walk Insights: [Article Title]

## Key Quotes
> "[Direct quote that captures something essential]"

> "[Another quote - preserve exact words]"

## Insights Discovered
- [Insight 1: Something they didn't know they knew]
- [Insight 2: Connection they made while walking]
- [Insight 3: Story detail that emerged]

## Emotional Beats
- [Moment of energy/excitement about X]
- [Moment of struggle/difficulty with Y]
- [Moment of realization about Z]

## Story Elements
- **Opening hook possibility:** [Something that could start the article]
- **Core tension:** [What the story is really about]
- **Resolution:** [How it lands]

## Questions Raised
- [New question that emerged]
- [Gap that needs more research]

## Natural Language
[Phrases, metaphors, ways of explaining that should carry into the article]
```

### 5. Integration

The extracted material feeds into OUTLINE:
- Key quotes become potential pull quotes
- Insights become section topics
- Emotional beats guide narrative arc
- Natural language informs voice
- Questions may require returning to RESEARCH

---

## Quality Gate

**Gate question:** Did you extract the heart of the story?

**Checklist:**
- [ ] Transcript is clean and readable
- [ ] Key quotes are identified
- [ ] Insights are extracted
- [ ] Emotional arc is visible
- [ ] Natural language is captured
- [ ] Material is ready to inform OUTLINE

---

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Recording too short | Guide not engaging | Revisit question design |
| All surface, no depth | Questions too broad | Add tacit knowledge triggers |
| Can't hear clearly | Recording quality | Better mic, quieter route |
| Tangents everywhere | No structure | Guide wasn't used |
| Nothing new emerged | Already knew the story | Skip walk for this article |

---

## When Walk Adds Most Value

- Stories with emotional content
- Topics where you "know it but can't say it"
- Personal journey narratives
- Methodology you've internalized

## When Walk May Be Skippable

- Purely technical content
- You've already articulated this clearly
- Time pressure
- Story is simple and straightforward

---

*The walk surfaces what you know. The transcript preserves it. The extraction makes it usable.*
