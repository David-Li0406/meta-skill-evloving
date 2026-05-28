---
name: generate-script
description: Generate a 60-second video script from the project concept. Use when in a video project folder with a README containing a concept.
disable-model-invocation: true
allowed-tools: Read, Write, Glob
---

# Generate Video Script

Read the README.md in the current project folder and generate a script for a 60-second short-form video.

## Steps

1. Read README.md to get the concept (Hook, Core idea, Why it works)
2. Generate a script following the structure below
3. Save as `script.md` in the current folder

## Script Structure

```markdown
# Script: [Title]

## Video Info
- **Duration:** 60 seconds
- **Word count:** ~150 words (1 second ≈ 2.5 words)

---

## HOOK (0:00 - 0:03)
[Attention-grabbing opening - visual and text/VO]

## BUILD-UP (0:03 - 0:45)
[Scene-by-scene breakdown with timestamps]

### Scene 1 (0:03 - 0:08)
**Visual:** [What we see]
**VO/Text:** [What we hear/read]

### Scene 2 (0:08 - 0:15)
...continue for ~8-10 scenes...

## PAYOFF (0:45 - 0:55)
[Climax, twist, or main reveal]

## CTA (0:55 - 0:60)
[Call to action - follow, like, comment prompt]

---

## Full Script (for voiceover)
[Complete script text in one block, ~150 words]
```

## Guidelines

- Hook MUST grab attention in first 2 seconds
- Keep total word count under 150 words for 60s
- Each scene should be 3-8 seconds
- Write for vertical format (9:16)
- Include text overlay suggestions
- Make it punchy, no filler words
- End with curiosity or satisfaction

## Output

Save the script to `script.md` and confirm with the user.
