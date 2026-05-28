# Semantic Compliance Scoring

Semantic Compliance measures how well content adheres to the Semantic SEO framework rules. The target is >85% compliance for high-quality content that minimizes Cost of Retrieval.

## Table of Contents

1. [Compliance Components](#compliance-components)
2. [Scoring Methodology](#scoring-methodology)
3. [Validation Checklist](#validation-checklist)
4. [Improvement Strategies](#improvement-strategies)

---

## Compliance Components

### Component Overview

| Component | Weight | Description |
|-----------|--------|-------------|
| Contextual Flow | 20% | Logical heading sequence and transitions |
| EAV Quality | 20% | Fact structure and consistency |
| Information Density | 15% | Facts per sentence ratio |
| Link Compliance | 15% | Anchor text and placement rules |
| Format Compliance | 15% | Correct content formats for intent |
| Technical Compliance | 15% | Schema, accessibility, performance |

---

## Scoring Methodology

### Contextual Flow Score (20%)

| Criterion | Points | Validation |
|-----------|--------|------------|
| H1-H2-H3 logical order | 4 | Headings follow incremental flow |
| Attribute priority correct | 4 | Unique -> Root -> Rare order |
| Contextual bridges present | 4 | Transitions between sections justified |
| Discourse integration | 4 | Anchor segments connect paragraphs |
| Subordinate text direct | 4 | First sentence answers heading |
| **Total** | **20** | |

### EAV Quality Score (20%)

| Criterion | Points | Validation |
|-----------|--------|------------|
| All facts as triples | 4 | Subject-Predicate-Object structure |
| Values specific | 4 | Numbers, not "many" or "some" |
| Consistency maintained | 4 | Same values across pages |
| Modality appropriate | 4 | "is" for facts, "can" for possibilities |
| Sources cited | 4 | Facts have verifiable sources |
| **Total** | **20** | |

### Information Density Score (15%)

| Criterion | Points | Validation |
|-----------|--------|------------|
| One fact per sentence | 3 | Each sentence delivers unique EAV |
| No filler words | 3 | No "basically", "really", "very" |
| No redundancy | 3 | Information not repeated |
| Concise sentences | 3 | <30 words per sentence average |
| No fluff paragraphs | 3 | Every paragraph adds value |
| **Total** | **15** | |

### Link Compliance Score (15%)

| Criterion | Points | Validation |
|-----------|--------|------------|
| Anchor text <3x repeated | 3 | Same anchor max 3 times |
| Links after definition | 3 | Entity defined before linking |
| Annotation text aligned | 3 | Surrounding text supports link |
| Link count <150 | 3 | Total internal links controlled |
| Main content priority | 3 | More links in main than boilerplate |
| **Total** | **15** | |

### Format Compliance Score (15%)

| Criterion | Points | Validation |
|-----------|--------|------------|
| Format matches intent | 3 | Lists for how-to, tables for comparison |
| List intro sentence | 3 | Count stated before list |
| Featured snippet ready | 3 | Answer in <40 words after heading |
| Visual hierarchy correct | 3 | Important content prominent |
| Semantic HTML used | 3 | Proper tags for structure |
| **Total** | **15** | |

### Technical Compliance Score (15%)

| Criterion | Points | Validation |
|-----------|--------|------------|
| Schema implemented | 3 | Correct type, no errors |
| Alt text optimized | 3 | Varies topicality beyond H1 |
| URL structure correct | 3 | Short, hierarchical, consistent |
| Response time <100ms | 3 | Fast server response |
| DOM size <1500 | 3 | Clean, minimal code |
| **Total** | **15** | |

---

## Validation Checklist

### Pre-Content Validation

Before writing, verify the brief:

```
[ ] Single Macro Context defined
[ ] Heading sequence logical
[ ] EAV requirements specified
[ ] Link targets and anchors defined
[ ] Format for each section specified
[ ] Featured snippet targets identified
```

### During-Content Validation

While writing, check:

```
[ ] Each sentence has one fact
[ ] Sentences under 30 words
[ ] No filler words used
[ ] Headings follow the brief
[ ] Subordinate text answers directly
[ ] Links placed after definitions
```

### Post-Content Validation

After writing, audit:

```
[ ] All EAVs included and consistent
[ ] No anchor text repeated >3x
[ ] Contextual bridges in place
[ ] Discourse integration maintained
[ ] Featured snippet answers optimized
[ ] Schema correctly implemented
```

---

## Compliance Scoring Sheet

### Quick Score Calculator

For each criterion, score 0-5 (0=missing, 5=perfect):

**Contextual Flow**
| Item | Score |
|------|-------|
| Heading logic | /5 |
| Attribute order | /5 |
| Bridges | /5 |
| Discourse integration | /5 |
| Subordinate text | /5 |
| **Subtotal** | /25 -> /20 |

**EAV Quality**
| Item | Score |
|------|-------|
| Triple structure | /5 |
| Value specificity | /5 |
| Consistency | /5 |
| Modality | /5 |
| Sources | /5 |
| **Subtotal** | /25 -> /20 |

**Information Density**
| Item | Score |
|------|-------|
| Fact density | /5 |
| No filler | /5 |
| No redundancy | /5 |
| Conciseness | /5 |
| No fluff | /5 |
| **Subtotal** | /25 -> /15 |

**Link Compliance**
| Item | Score |
|------|-------|
| Anchor limit | /5 |
| Placement | /5 |
| Annotation | /5 |
| Count | /5 |
| Priority | /5 |
| **Subtotal** | /25 -> /15 |

**Format Compliance**
| Item | Score |
|------|-------|
| Format match | /5 |
| List intro | /5 |
| FS ready | /5 |
| Visual hierarchy | /5 |
| Semantic HTML | /5 |
| **Subtotal** | /25 -> /15 |

**Technical Compliance**
| Item | Score |
|------|-------|
| Schema | /5 |
| Alt text | /5 |
| URL structure | /5 |
| Response time | /5 |
| DOM size | /5 |
| **Subtotal** | /25 -> /15 |

### Total Score

| Component | Weight | Raw Score | Weighted |
|-----------|--------|-----------|----------|
| Contextual Flow | 20% | /20 | |
| EAV Quality | 20% | /20 | |
| Information Density | 15% | /15 | |
| Link Compliance | 15% | /15 | |
| Format Compliance | 15% | /15 | |
| Technical | 15% | /15 | |
| **Total** | 100% | | **/100** |

**Interpretation**:
- 90-100: Excellent compliance
- 85-89: Good (meets threshold)
- 70-84: Needs improvement
- <70: Major revision required

---

## Improvement Strategies

### Low Contextual Flow Score

| Issue | Fix |
|-------|-----|
| Headings out of order | Reorder to logical sequence |
| Missing bridges | Add transitional H2/H3 sections |
| Poor discourse integration | Add anchor segments between paragraphs |
| Weak subordinate text | Rewrite first sentences to answer directly |

### Low EAV Quality Score

| Issue | Fix |
|-------|-----|
| Vague values | Replace with specific numbers/data |
| Inconsistent facts | Audit all pages, standardize values |
| Wrong modality | Change "can" to "is" for facts |
| Missing sources | Add citations |

### Low Information Density Score

| Issue | Fix |
|-------|-----|
| Filler words | Delete "very", "really", "basically" |
| Long sentences | Break into shorter statements |
| Redundant paragraphs | Consolidate or remove |
| Fluff content | Replace with facts |

### Low Link Compliance Score

| Issue | Fix |
|-------|-----|
| Repeated anchors | Use synonyms/variations |
| Links too early | Move after entity definition |
| Poor annotation | Rewrite surrounding context |
| Too many links | Reduce to <150, prioritize main content |

### Low Format Compliance Score

| Issue | Fix |
|-------|-----|
| Wrong format | Use tables for comparison, lists for steps |
| No list intro | Add sentence stating item count |
| Long FS answers | Cut to <40 words |
| Bad visual hierarchy | Reorder components by importance |

### Low Technical Score

| Issue | Fix |
|-------|-----|
| Schema errors | Validate and fix markup |
| Duplicate alt text | Vary with synonyms/attributes |
| Slow response | Optimize server configuration |
| Large DOM | Remove unnecessary elements |
