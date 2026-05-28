---
id: surveys
name: "Surveys and Questionnaires"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Surveys and Questionnaires

## Metadata
- **Category:** UX / Research Methods
- **Difficulty:** Intermediate
- **Tags:** #methodology #ux #research #surveys #quantitative
- **Agent:** faion-ux-researcher-agent

---

## Problem

You need input from many users but cannot interview everyone. Qualitative insights need quantitative validation. You want to measure satisfaction or preferences across your user base. Individual opinions may not represent the larger population.

Without surveys:
- Limited sample feedback
- No quantitative data
- Cannot generalize findings
- Missing user voice at scale

---

## Framework

### What are UX Surveys?

Surveys collect structured data from many users through standardized questions. They quantify user attitudes, preferences, and experiences.

### Survey Types

| Type | Purpose | Example |
|------|---------|---------|
| **Satisfaction** | Measure happiness | CSAT, NPS |
| **Task-based** | Post-task feedback | SUS, SEQ |
| **Preference** | Compare options | A vs B preference |
| **Exploratory** | Understand behaviors | Usage patterns |

### When to Use Surveys

| Use Case | Survey Appropriate |
|----------|-------------------|
| Measure satisfaction | Yes |
| Understand "why" | Better with interviews |
| Large sample needed | Yes |
| Deep exploration | No, use interviews |
| Quantify findings | Yes |
| Validate qualitative | Yes |

---

## Process

### Step 1: Define Objectives

What do you want to learn?

```
Examples:
- What is our current user satisfaction score?
- Which features are most valuable?
- How do users rate our onboarding?
```

### Step 2: Choose Question Types

| Type | When to Use | Analysis |
|------|-------------|----------|
| **Multiple choice** | Fixed options | Percentages |
| **Rating scale** | Measure intensity | Averages |
| **Ranking** | Prioritization | Order |
| **Open-ended** | Exploration | Qualitative |
| **Matrix** | Multiple items, same scale | Comparison |

### Step 3: Write Questions

**Good questions:**
- Clear and concise
- One concept per question
- Neutral wording
- Appropriate answer options

### Step 4: Design Survey Flow

```
1. Introduction and consent
2. Screening questions (if needed)
3. Easy questions first
4. Core questions
5. Demographics (at end)
6. Thank you
```

### Step 5: Test and Launch

- Pilot test with 5-10 people
- Check for confusion
- Time the completion
- Fix issues
- Launch

### Step 6: Analyze Results

- Calculate response rate
- Analyze quantitative data
- Code open-ended responses
- Look for patterns by segment
- Report findings

---

## Templates

### Survey Planning Template

```markdown
# Survey Plan: [Survey Name]

**Objective:** [What you want to learn]
**Target audience:** [Who should respond]
**Sample size needed:** [N]
**Distribution:** [How to reach respondents]
**Timeline:** [When]

## Questions

### Screening
1. [Screening question if needed]

### Core Questions
1. [Question]
   - Type: [Multiple choice / Scale / etc.]
   - Options: [List options]

2. [Question]
   - Type:
   - Options:

### Demographics
1. [Question]

## Success Metrics
- Response rate: [Target %]
- Completion rate: [Target %]
```

### Standard Survey Questions

```markdown
# [Survey Name]

## Introduction
Thank you for taking this survey. Your feedback helps us
improve [product]. This takes approximately [X] minutes.
Your responses are anonymous.

## Satisfaction Questions

1. Overall, how satisfied are you with [product]?
   ○ Very dissatisfied
   ○ Dissatisfied
   ○ Neutral
   ○ Satisfied
   ○ Very satisfied

2. How likely are you to recommend [product] to a colleague?
   (0-10 scale, NPS)

3. How easy is [product] to use?
   ○ Very difficult
   ○ Difficult
   ○ Neither easy nor difficult
   ○ Easy
   ○ Very easy

## Feature Questions

4. How valuable are the following features?
   (Not valuable, Somewhat, Very, Extremely)
   - Feature A: ○ ○ ○ ○
   - Feature B: ○ ○ ○ ○
   - Feature C: ○ ○ ○ ○

## Open-ended

5. What is the one thing you would improve?
   [Text box]

## Demographics

6. How long have you used [product]?
   ○ Less than 1 month
   ○ 1-6 months
   ○ 6-12 months
   ○ More than 1 year
```

---

## Standard UX Metrics

### Net Promoter Score (NPS)

```
Question: How likely are you to recommend [X] to a friend
or colleague? (0-10)

Calculation:
- Detractors (0-6): % of respondents
- Passives (7-8): Excluded
- Promoters (9-10): % of respondents

NPS = % Promoters - % Detractors
Range: -100 to +100
```

### System Usability Scale (SUS)

```
10 standardized questions, 1-5 scale
Score range: 0-100
Average score: 68
Above 80: Excellent
Below 50: Poor
```

### Customer Satisfaction (CSAT)

```
Question: How satisfied are you with [X]?
Scale: 1-5 or 1-7

CSAT = (Satisfied responses / Total responses) x 100
```

### Single Ease Question (SEQ)

```
Question: Overall, how easy or difficult was this task?
Scale: 1-7 (Very difficult to Very easy)

Use after each task in usability testing
Average benchmark: 5.5
```

---

## Examples

### Good Question Examples

```
Clear: "How often do you use the search feature?"
- Never
- Less than once a week
- 1-3 times per week
- Daily
- Multiple times per day
```

### Bad Question Examples

```
Double-barreled: "How satisfied are you with the speed
and accuracy of search results?"
(Two concepts in one question)

Leading: "How much do you love our new feature?"
(Assumes positive sentiment)

Vague: "How often do you use it?"
(What is "it"? What is "often"?)
```

---

## Common Mistakes

1. **Too long** - Aim for <5 minutes
2. **Leading questions** - Biased wording
3. **Too many open-ended** - Analysis burden
4. **No pilot test** - Unclear questions
5. **Wrong audience** - Sample does not represent users

---

## Response Rate Tips

| Factor | Impact |
|--------|--------|
| Length | Shorter = higher response |
| Incentive | Increases response |
| Timing | Mid-week, mid-day best |
| Mobile-friendly | Many complete on phone |
| Clear purpose | Why should they respond? |
| Personalization | Addressed to them |

---

## Analysis Tips

### Quantitative
- Calculate descriptive statistics
- Compare segments (new vs. experienced)
- Track over time
- Look for significant differences

### Qualitative (Open-ended)
- Code responses into themes
- Count theme frequency
- Pull representative quotes
- Connect to quantitative data

---

## Checklist

- [ ] Clear research objective
- [ ] Questions are clear and unbiased
- [ ] Answer options are complete
- [ ] Survey is reasonable length
- [ ] Mobile-friendly format
- [ ] Pilot tested
- [ ] Privacy/consent addressed
- [ ] Sample is representative
- [ ] Analysis plan defined
- [ ] Results actionable

---

## References

- Survey Design Best Practices
- Questionnaire Design by Oppenheim
- Measuring the User Experience