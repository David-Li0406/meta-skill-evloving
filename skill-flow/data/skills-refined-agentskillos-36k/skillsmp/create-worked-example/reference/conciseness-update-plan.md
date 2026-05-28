# Conciseness Update Plan for Worked Example Skill

## Problem Statement

Current worked example decks are too verbose compared to the SGI exemplar decks. Key issues:

1. **Explanatory subtitles** - "First, let's figure out how fast turtle g is moving..."
2. **Redundant info boxes** - "Reading the graph: At point (6,12)..."
3. **Two-part CFU questions** - "What is X? How did you calculate it?"
4. **Long answer explanations** - Multiple sentences with extra context
5. **Content duplication** - Same information in both left text column AND right visual column

## Exemplar Standard (SGI Decks)

### What Makes SGI Decks Concise:

| Element | SGI Pattern | Example |
|---------|-------------|---------|
| Problem reminder | 15 words max | "30 nuggets total. 6 per student. How many students?" |
| Step subtitle | NONE | (removed entirely) |
| CFU question | Single question, ≤12 words | "Why did I put the '?' at the beginning?" |
| Answer explanation | 1-2 sentences, ≤25 words | "Each box represents one student." |
| Math display | LARGE (60-80px) | Equations dominate the slide |
| Columns | Complementary | Left = text, Right = visual (no duplication) |

### The "3-Second Rule"
A student should be able to scan the slide and understand the key point in 3 seconds. Every extra word slows this down.

---

## Changes Made

### 1. pedagogy.md - Added Rule 5: "Conciseness Rule" ✅

- Text limit table (problem reminder, CFU, answer)
- Complementary columns principle (no duplication)
- What to REMOVE vs KEEP lists
- Updated CFU question patterns with word counts

### 2. protocol.md - Added Conciseness Checks ✅

- CFU format rules (ONE question, ≤12 words)
- Answer box requirements (≤25 words)
- Left column conciseness section with word limits
- Two-column complementary rule with examples
- Pre-flight checklist with conciseness section
- Added problem-reminder to slide component lists

### 3. index.md (Phase 3) - Updated Slide Structure ✅

- Added problem-reminder as mandatory component for slides 2-8
- Updated card-patterns list to include problem-reminder

### 4. layout-presets.md - Column Purpose Clarification ✅

- Explicit left vs right column purposes
- Content type restrictions per column (allowed/not allowed tables)
- The Complementary Test explanation

### 5. problem-reminder.html - New Pattern ✅

- Condensed format template with 15-word max
- Good/bad transformation examples
- Usage instructions

### 6. Phase 2 (confirm-and-plan) - Scenario Template ✅

- Added "Problem Reminder" field to each scenario
- Conciseness guidance with examples
- Problem reminders defined upfront during planning

---

## Word Limit Summary

| Element | Max Words | Notes |
|---------|-----------|-------|
| Problem reminder box | 15 | Condensed summary repeated on slides 2-8 |
| Step subtitle | 0 | REMOVED - no explanatory prose |
| CFU question | 12 | Single question only |
| Answer explanation | 25 | 1-2 sentences max |
| Supporting text (left col) | 10 | Only if absolutely needed |
| Visual labels (right col) | 3-5 per label | Numbers, variable names only |

---

## Banned Patterns

**Never include:**
- "First, let's..." / "Now we need to..." / "Let's start by..."
- "Reading the graph: At point (x, y)..."
- Two-part questions ("What is X? How did you calculate it?")
- Extra context ("This is also called the constant of proportionality!")
- Explanatory text boxes inside visual diagrams

---

## Validation Checklist

Before generating any slide, verify:

- [ ] Problem reminder ≤15 words
- [ ] No explanatory subtitles
- [ ] CFU is ONE question, ≤12 words
- [ ] Answer is ≤25 words, 1-2 sentences
- [ ] Left and right columns show DIFFERENT content (no duplication)
- [ ] Math/equations are the dominant visual element
- [ ] Slide is scannable in 3 seconds

---

## Files Updated

| File | Status | Changes |
|------|--------|---------|
| `reference/pedagogy.md` | ✅ Done | Added Rule 5 with text limits and complementary columns |
| `phases/03-generate-slides/protocol.md` | ✅ Done | Added CFU/Answer requirements, left column rules, pre-flight checks, problem-reminder reference |
| `phases/03-generate-slides/index.md` | ✅ Done | Added problem-reminder to component lists and slide structure table |
| `reference/layout-presets.md` | ✅ Done | Column purpose clarification with allowed/not allowed tables |
| `phases/03-generate-slides/card-patterns/simple-patterns/problem-reminder.html` | ✅ Done | New pattern with transformation examples |
| `phases/02-confirm-and-plan/index.md` | ✅ Done | Added problem reminder field to scenario template |

---

## Next Steps

1. ~~Complete layout-presets.md update~~ ✅
2. ~~Add problem-reminder.html pattern~~ ✅
3. ~~Update Phase 2 to capture problem reminders upfront~~ ✅
4. ~~Update Phase 3 index.md and protocol.md with problem-reminder~~ ✅
5. ~~Update content-box.html with larger text sizes~~ ✅
6. ~~Update diagram-patterns.md with "simple visuals" guidance~~ ✅
7. Update browser wizard (`src/app/scm/workedExamples/create/`) to match these rules (if needed)
8. Test by generating a new worked example and comparing to SGI exemplar

---

## Additional Changes (Visual Dominance)

### 7. content-box.html - Larger Text Sizes ✅

Updated default sizes for ~380px column width:
- Header: 14px → 18px (default)
- Body: 14px → 16px (default)
- Equation: 24px → 36px (default), 48px (large/focus)

### 8. diagram-patterns.md - Simple Visuals Guidance ✅

Added "Simple Visuals That Speak for Themselves" section:
- The "Delete Test" - if visual makes sense without text, delete the text
- Labels vs. Explanations table (what's allowed vs. not)
- Visuals should FILL their column

### 9. "3-Second Scan" Rule Enshrined ✅

Updated across all key files:
- **pedagogy.md**: Rule 5 renamed to "The 3-Second Scan Rule"
- **protocol.md**: Pre-flight checklist now leads with 3-second scan test
- **layout-presets.md**: Added 3-second scan test to column rules
