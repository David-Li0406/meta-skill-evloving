---
name: page-estimation
description: Use this skill when estimating screenplay length, calculating runtime, tracking page count, or validating target length for submission requirements.
---

# Page Estimation Skill

## Invocation Triggers
Apply this skill when:
- Estimating screenplay length
- Calculating runtime
- Tracking page count
- Validating target length

## The Page-to-Screen Rule

### Standard Formula
```
1 page of screenplay ≈ 1 minute of screen time
```

### Genre Adjustments
| Genre    | Adjustment      | Typical Length   |
|----------|-----------------|------------------|
| Action   | 0.8-0.9 min/page| 95-115 pages     |
| Comedy   | 1.0 min/page    | 90-110 pages     |
| Drama    | 1.0-1.1 min/page| 100-120 pages    |
| Thriller | 0.9-1.0 min/page| 100-115 pages    |
| Horror   | 0.9-1.0 min/page| 85-100 pages     |
| Animation| 0.7-0.8 min/page| 75-95 pages      |

### Why It Varies
- **Action-heavy scripts:** More white space, faster pace → shorter pages
- **Dialogue-heavy scripts:** Dense pages → longer runtime per page
- **Visual storytelling:** Less text, more subtext → varies

## Estimation Methods

### Method 1: Element Count
Rough estimate based on script elements:
```markdown
Scenes: 60 scenes × 1.5 pages avg = 90 pages
Adjustment for dialogue density: +10%
Estimated: ~99 pages
```

### Method 2: Word Count
```markdown
Total words: 20,000
Average screenplay: 180-200 words/page
Estimated: 20,000 ÷ 190 = 105 pages
```

### Method 3: Structural Estimate
```markdown
Act One (Setup): 25 pages
Act Two (Confrontation): 55 pages
Act Three (Resolution): 25 pages
Total: 105 pages
```

### Method 4: Scene-by-Scene
Most accurate:
```markdown
| Scene | Est. Pages |
|-------|-----------|
| 1     | 2         |
| 2     | 1.5       |
| 3     | 3         |
| ...   | ...       |
| Total | X         |
```

## Fountain Page Count

### Title Page
- Always counts as page 1
- Not numbered in output
- Adds ~1 page to total

### Scene Headings
- Each scene heading takes ~2 lines
- 55-60 lines per page standard
- Many short scenes = more page overhead

### Dialogue vs. Action
- Dialogue: ~35-40 lines per page (narrower column)
- Action: ~55-60 lines per page (full width)
- Heavy dialogue = fewer scenes per page

### Elements That Add Length
- Dual dialogue (takes more vertical space)
- Parentheticals (extra lines)
- Transitions (blank lines)