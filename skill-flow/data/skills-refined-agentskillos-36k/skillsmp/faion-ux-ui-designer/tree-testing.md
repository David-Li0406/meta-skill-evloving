---
id: tree-testing
name: "Tree Testing"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Tree Testing

## Metadata
- **Category:** UX / Research Methods
- **Difficulty:** Intermediate
- **Tags:** #methodology #ux #research #tree-testing #information-architecture
- **Agent:** faion-ux-researcher-agent

---

## Problem

Your navigation structure seems logical to your team. Users cannot find content even with search. Information architecture (IA) debates are based on opinions. You redesigned navigation and need to validate before building. Card sorting gave you structure but you have not tested it.

Without tree testing:
- Navigation based on org structure
- Findability problems discovered late
- No data to resolve IA debates
- Expensive redesigns after launch

---

## Framework

### What is Tree Testing?

Tree testing evaluates the findability of topics in a website's hierarchy. Users are given tasks and navigate a text-only version of the site structure (no design, no content) to find where they would expect the answer.

### Tree Testing vs. Card Sorting

| Aspect | Card Sorting | Tree Testing |
|--------|--------------|--------------|
| Purpose | Create structure | Validate structure |
| When | Before IA exists | After IA draft |
| User task | Group items | Find items |
| Output | Suggested categories | Success/failure data |

### Key Metrics

| Metric | Definition | Good Target |
|--------|------------|-------------|
| **Success rate** | Found correct answer | >80% |
| **Directness** | Found it without backtracking | >70% |
| **Time to complete** | How long task took | Varies by task |
| **First click** | Where users started | Correct category |

---

## Process

### Step 1: Create the Tree

Convert your IA to a text hierarchy:

```
Home
├── Products
│   ├── Category A
│   │   ├── Product 1
│   │   └── Product 2
│   └── Category B
│       └── Product 3
├── Support
│   ├── FAQs
│   ├── Contact Us
│   └── Returns
└── Account
    ├── Orders
    └── Settings
```

**Rules:**
- Use actual labels (no placeholder text)
- Include all navigation levels
- Match planned structure exactly
- Limit to ~100 items for clarity

### Step 2: Write Tasks

**Task format:** Where would you find [thing]?

```
Good tasks:
- "You want to return a product. Where would you go?"
- "Find information about shipping costs."
- "Look for your order history."

Bad tasks:
- "Find Returns" (gives away the label)
- "Navigate to the support section" (too directive)
```

**Task selection:**
- Cover key user goals (10-15 tasks)
- Include different depths of navigation
- Represent different content types
- Prioritize high-traffic/high-value tasks

### Step 3: Define Correct Answers

For each task, identify:
- **Correct destination(s)** - Where they should end up
- **Acceptable paths** - Alternative valid locations

```
Task: "You want to check your order status"
Correct: Account > Orders
Also acceptable: Support > Order Status (if exists)
```

### Step 4: Run the Test

**Participants:**
- 30-50 for statistical confidence
- Representative of target users
- No prior knowledge of your IA

**Test execution:**
- Unmoderated remote works well
- Takes 10-15 minutes typically
- Randomize task order

### Step 5: Analyze Results

For each task:
1. Calculate success rate
2. Map where people went wrong
3. Identify first-click patterns
4. Note common wrong paths

### Step 6: Iterate

Based on findings:
- Rename confusing labels
- Move misplaced content
- Add cross-links if needed
- Retest problem areas

---

## Templates

### Test Plan Template

```markdown
# Tree Testing Plan

**Project:** [Name]
**Date:** [Date]
**IA Version:** [Version number]

## Objectives
- Validate proposed information architecture
- Identify navigation problems before development
- Compare alternative structures (if testing variants)

## Tree Structure

[Paste tree here]

## Tasks (10-15)

| # | Task | Correct Answer | Priority |
|---|------|----------------|----------|
| 1 | "You want to..." | [Path > To > Answer] | High |
| 2 | "Find where to..." | [Path > To > Answer] | High |
| 3 | | | |

## Participants
- **Target:** 50 participants
- **Criteria:** [Screening criteria]
- **Recruitment:** [Platform/method]
- **Incentive:** [Amount]

## Success Criteria
- Overall success rate: >80%
- No task below 60% success
- Directness: >70%

## Timeline
- Tree setup: [Date]
- Recruitment: [Date range]
- Data collection: [Date range]
- Analysis: [Date]
- Report: [Date]
```

### Results Report Template

```markdown
# Tree Testing Results

**Test dates:** [Start] to [End]
**Participants:** [N]
**Tasks:** [N]

## Executive Summary

**Overall success rate:** [X%]
**Overall directness:** [X%]

**Key findings:**
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

## Task Results

### Task 1: "[Task description]"

**Success rate:** [X%]
**Directness:** [X%]
**Average time:** [X seconds]

**Path analysis:**
| Path taken | Count | % |
|------------|-------|---|
| Products > Category A (correct) | 40 | 80% |
| Support > FAQs | 7 | 14% |
| Account > Settings | 3 | 6% |

**First clicks:**
| Category | % of users |
|----------|------------|
| Products | 85% |
| Support | 10% |
| Account | 5% |

**Insight:** [What this tells us]
**Recommendation:** [What to do]

### Task 2: "[Task description]"
[Same structure]

## Problem Areas

| Issue | Affected Tasks | Severity | Recommendation |
|-------|----------------|----------|----------------|
| [Label confusion] | 2, 5, 8 | High | [Fix] |
| [Missing category] | 3 | Medium | [Fix] |

## Recommendations

1. **High priority:**
   - [Change 1]
   - [Change 2]

2. **Consider:**
   - [Change 3]

3. **Monitor:**
   - [Area to watch]

## Appendix
- Full tree structure
- Task list
- Participant demographics
- Raw data
```

---

## Examples

### Example 1: E-commerce Navigation

**Task:** "Find the return policy"

**Results:**
- Support > Returns: 45%
- Support > FAQs: 25%
- Products > [random product]: 15%
- Account > Orders: 10%
- Gave up: 5%

**Insight:** Users split between "Returns" and "FAQs". Consider:
- Make "Returns" more prominent
- Add return policy link to FAQs
- Add contextual link in order pages

### Example 2: Comparing Two Structures

**Tree A:** Products organized by type
**Tree B:** Products organized by use case

**Task:** "Find a laptop for gaming"

| Metric | Tree A | Tree B |
|--------|--------|--------|
| Success | 60% | 85% |
| Directness | 45% | 75% |
| First click correct | 50% | 80% |

**Decision:** Tree B (use-case organization) performs better.

---

## Tools

| Tool | Features | Pricing |
|------|----------|---------|
| **Optimal Workshop Treejack** | Industry standard, robust | $$$$ |
| **UserZoom** | Enterprise features | $$$$ |
| **PlaybookUX** | Simple, affordable | $$ |
| **UXtweak** | Good free tier | $-$$ |
| **Maze** | Modern interface | $$$ |

---

## Common Mistakes

1. **Testing too many levels** - Keep tree to 3-4 levels max
2. **Tasks reveal the answer** - Don't use exact labels in tasks
3. **Too few participants** - Need 30+ for reliable data
4. **Ignoring first-click data** - Shows initial mental model
5. **Testing without iteration** - Should be iterative process

---

## Interpreting Results

### Success Rate Guidelines

| Success Rate | Interpretation |
|--------------|----------------|
| >80% | Excellent, move forward |
| 60-80% | Acceptable, minor fixes |
| 40-60% | Problem area, needs work |
| <40% | Major issue, redesign needed |

### First Click Analysis

```
First click is crucial:
- If first click is correct: 87% likely to succeed
- If first click is wrong: only 46% likely to succeed

Focus first on getting users to the right section.
```

### Path Analysis

Look for patterns:
- **Common wrong paths** = Label or structure problem
- **Random paths** = Users are lost, label unclear
- **Backtracking** = Structure doesn't match mental model
- **Abandonment** = Content seems to not exist

---

## Combining with Other Methods

### Recommended Sequence

```
1. Card sorting → Understand user mental models
2. Create IA draft → Based on card sorting + business needs
3. Tree testing → Validate the draft
4. Iterate → Fix problems found
5. Retest → Confirm improvements
6. Usability testing → Full design with IA
```

### Triangulation

| Method | What it reveals |
|--------|-----------------|
| Card sorting | How users group concepts |
| Tree testing | If users can find things |
| Analytics | What users actually do |
| Usability testing | How full experience works |

---

## Checklist

- [ ] Tree structure finalized
- [ ] Labels match planned design
- [ ] 10-15 tasks written
- [ ] Tasks cover key user goals
- [ ] Tasks don't reveal answers
- [ ] Correct answers defined
- [ ] Test tool set up
- [ ] 30-50 participants recruited
- [ ] Test launched
- [ ] Results analyzed by task
- [ ] Problem areas identified
- [ ] Recommendations documented
- [ ] Iterations planned

---

## References

- Information Architecture by Rosenfeld, Morville, Arango
- Optimal Workshop: Tree Testing Guide
- UX research community: Tree Testing