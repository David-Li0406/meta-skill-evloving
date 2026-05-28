# Content Extraction Guidelines

Detailed rules for extracting presentation content from different document types.

## General Principles

### What to Extract
- Numbers and statistics (percentages, amounts, counts)
- Key metrics with targets
- Decision points and outcomes
- Short impactful phrases (max 10 words)
- Section headers for chapter navigation

### What to Skip
- Introductions and preambles
- Detailed explanations and rationale
- Implementation specifics unless critical
- Redundant information
- Contact information and signatures

### Slide Density
- Aim for 1 core idea per slide
- If a section has 5 key points, create 5 slides
- Prefer more slides with less content over fewer dense slides

---

## PRD (Product Requirements Document)

### Structure Mapping

| PRD Section | Slide Treatment |
|-------------|-----------------|
| Background | Skip or 1 context slide |
| Goals | 1 slide per goal with metric |
| Constraints | Group into 1-2 slides |
| Phases | Chapter + overview slide each |
| Features | 1 slide per major feature |
| User Flows | Simplified diagram or key steps |
| Tech Requirements | Comparison if options exist |
| Open Questions | Summary slide or skip |

### Extraction Examples

**Goals section:**
```
מטרות:
* הגדלת מכירות נוי ב-20%
* הפחתת עומס תפעולי
```

Extract as:
- Hero number slide: "20%" with context "Sales growth target"
- Key point slide: "Reduce operational overhead"

**Phase breakdown:**
```
Phase 1 – In scope:
* פורטל הזמנות B2B
* סנכרון מלאי
* דשבורד אדמין
```

Extract as:
- Chapter title: "Phase 1"
- Card grid slide with 3 cards for each scope item

**Technical options:**
```
שלוש אופציות:
1. Off-the-shelf (Shopify)
2. Custom-made (React + Node.js) - מומלץ
3. Hybrid (Frontend + Monday.com)
```

Extract as:
- Comparison slide with 3 options
- Highlight recommended option

---

## Meeting Transcript / Notes

### Structure Mapping

| Content Type | Slide Treatment |
|--------------|-----------------|
| Decisions made | 1 slide per decision |
| Action items | Grouped list slide |
| Key quotes | Quote slide with attribution |
| Statistics mentioned | Hero number slides |
| Discussion topics | Chapter titles |
| Follow-ups | Summary list slide |

### Extraction Examples

**Decision:**
```
We decided to go with the microservices architecture
because it allows independent scaling.
```

Extract as:
- Key point: "Microservices architecture"
- Context: "Independent scaling"

**Action item list:**
```
Action items:
- John: Review security requirements by Friday
- Sarah: Prepare cost analysis
- Team: Schedule follow-up meeting
```

Extract as:
- List slide with 3 items (names + tasks only)

**Quote:**
```
"We need to ship this by Q2 or we lose the market window"
- CEO
```

Extract as:
- Quote slide with text and attribution

---

## Article / Blog Post

### Structure Mapping

| Content Type | Slide Treatment |
|--------------|-----------------|
| Headlines | Chapter titles |
| Subheadings | Section markers |
| Statistics | Hero number slides |
| Key arguments | Key point slides |
| Lists | List slides (max 4 items) |
| Conclusions | Summary slide |

### Extraction Examples

**Headline with stat:**
```
# 73% of Companies Fail at Digital Transformation
```

Extract as:
- Hero number: "73%"
- Context: "of companies fail at digital transformation"

**Argument with evidence:**
```
Remote work increases productivity. Studies show
employees work an average of 1.4 more days per month.
```

Extract as:
- Key point: "Remote work increases productivity"
- Hero number: "1.4 extra days/month"

---

## General Notes / Bullet Points

### Structure Mapping

| Content Type | Slide Treatment |
|--------------|-----------------|
| Top-level bullets | Chapters |
| Sub-bullets | Individual slides |
| Numbers anywhere | Hero number slides |
| Short phrases | Key point slides |
| Long explanations | Summarize to key phrase |

### Extraction Examples

**Nested bullets:**
```
- Marketing Strategy
  - Focus on enterprise clients
  - Budget: $500K annually
  - Target: 50 new accounts
```

Extract as:
- Chapter: "Marketing Strategy"
- Key point: "Enterprise focus"
- Hero number: "$500K" with "annual budget"
- Hero number: "50" with "new accounts target"

---

## Slide Type Selection Guide

### Use Hero Number When:
- There's a specific percentage
- There's a dollar/currency amount
- There's a count or quantity
- There's a time period (days, months, years)

### Use Key Point When:
- Single important statement
- Decision or conclusion
- Strategy or approach
- No specific number involved

### Use List When:
- 3-4 related items
- Steps in a process
- Features or capabilities
- Requirements or criteria

### Use Comparison When:
- Options being evaluated
- Before/after states
- Pros/cons analysis
- Two competing approaches

### Use Quote When:
- Direct speech from stakeholder
- Customer testimonial
- Expert opinion
- Memorable phrase

### Use Card Grid When:
- Features with icons
- Team or roles
- Multiple parallel concepts
- Benefits or advantages

---

## Language-Specific Notes

### Hebrew (RTL)
- Numbers remain LTR within RTL text
- Preserve Hebrew punctuation
- Keep technical terms in English if commonly used

### Multi-language Documents
- Detect primary language by character frequency
- Keep code/technical terms in original language
- Translate only if necessary for clarity
