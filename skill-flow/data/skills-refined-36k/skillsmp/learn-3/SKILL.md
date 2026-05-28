---
name: learn
description: Unified learning skill - log decisions (--decision), review launches (--launch), or extract patterns from history (--patterns)
---

# Learn

## Overview

The learning skill closes the feedback loop in the PM algorithm: OBSERVE → THINK → PLAN → BUILD → EXECUTE → VERIFY → **LEARN**. It combines three modes:

| Mode | Purpose | Output |
|------|---------|--------|
| `--decision` | Log decision context, rationale, expected outcomes | `outputs/decisions/YYYY-MM-DD-[title].md` |
| `--launch` | Post-launch retrospective (30/60/90 days) | `outputs/reviews/launch-review-[initiative]-YYYY-MM-DD.md` |
| `--patterns` | Extract patterns from history, update learned rules | `.claude/rules/learned/[skill]-patterns.md` |

## When to Use

### --decision Mode
- Prioritizing Feature A over Feature B
- Deciding to defer/cut scope
- Choosing between technical approaches
- Making strategic bets in quarterly planning
- Any decision you'd want to revisit in 30-90 days

### --launch Mode
- 30/60/90 days after product/feature launch
- After major initiative completes
- Quarterly retrospectives on past launches
- When a launch clearly succeeded or failed (learn from extremes)

### --patterns Mode
- **Automatic:** Weekly hook runs `pm-os learn --auto`
- **Manual:** `pm-os learn <skill-name>` to analyze a specific skill
- After major milestone (post-launch, post-quarter, post-strategy cycle)

---

## Mode: --decision

### Process

**Step 1: Create Decision Log**

Create file: `outputs/decisions/YYYY-MM-DD-[short-title].md`

**Step 2: Fill Decision Template**

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: learn --decision
review_date: YYYY-MM-DD
status: open
---

# Decision: [Short descriptive title]

## Context
[What situation prompted this decision? What's the business context?]

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| [Option A] | [Benefits] | [Drawbacks] |
| [Option B] | [Benefits] | [Drawbacks] |
| [Option C] | [Benefits] | [Drawbacks] |

## Decision
**Chosen:** [Which option]

**Rationale:**
- [Reason 1] `[Evidence/Assumption]`
- [Reason 2] `[Evidence/Assumption]`
- [Reason 3] `[Evidence/Assumption]`

## Expected Outcome
[What do you expect to happen as a result of this decision?]

## Success Criteria
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] [Measurable criterion 3]

## Review Date
**Check back:** YYYY-MM-DD (typically 30-90 days)

---

## Outcome (fill in at review date)

**Status:** *(pending | correct | partially correct | wrong)*

**Actual Result:**
[What actually happened?]

**Success Criteria Results:**
- [ ] [Criterion 1]: [Met/Not met - why]
- [ ] [Criterion 2]: [Met/Not met - why]
- [ ] [Criterion 3]: [Met/Not met - why]

**Lessons Learned:**
- [What would you do differently?]
- [What assumptions were wrong?]
- [What signals did you miss?]

**Calibration Note:**
[Did your intuition match reality? Over/under-confident?]
```

**Step 3: Set Calendar Reminder**

After logging, set a reminder for the review date.

**Step 4: Review Process**

At review date:
1. Open the decision log
2. Fill in the Outcome section honestly
3. Update status in frontmatter
4. Extract lessons for future decisions

### Quarterly Decision Review

Every quarter, review all decisions from 90+ days ago:

```markdown
## Q[X] Decision Review

| Decision | Expected | Actual | Outcome | Key Lesson |
|----------|----------|--------|---------|------------|
| [Title] | [Expected] | [Actual] | pass/partial/fail | [Lesson] |

**Patterns:**
- [What types of decisions am I good at?]
- [What types of decisions am I bad at?]
- [What signals should I weight more/less?]
```

---

## Mode: --launch

### Process

**Step 1: Identify the Launch**

Ask user:
- "Which product/feature launch are we reviewing?"
- "When did it launch?"
- "What was the original GTM plan or charter?"
- "How long post-launch? (30/60/90 days)"

Read the original GTM plan/charter to understand predictions.

**Step 2: Metrics Review (Predicted vs Actual)**

For each metric in the original plan, compare:
- **Predicted:** What we said would happen
- **Actual:** What actually happened
- **Variance:** How far off were we? (%)
- **Explanation:** Why the difference?

**Step 3: What Went Well (Success Analysis)**

Identify 3-5 things that worked:
- **What:** Specific thing that succeeded
- **Why:** Root cause of success (not just "good execution")
- **Pattern to Reinforce:** Repeatable lesson

**Step 4: What Went Wrong (Failure Analysis)**

Identify 3-5 things that didn't work:
- **What:** Specific failure
- **Why:** Root cause (use 5 whys if needed)
- **Fix for Next Time:** Concrete process change

**Step 5: Lessons Learned → PM OS Updates**

For each lesson, identify process improvements:
- **Update skill:** Which skill file needs changes?
- **New template section:** What should we add to templates?
- **New vocabulary term:** Domain terms to add?
- **New quality gate:** Checkpoint to add to process?

**Step 6: Generate Output**

Write to `outputs/reviews/launch-review-[initiative]-YYYY-MM-DD.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: learn --launch
initiative: [Product/Feature]
launch_date: YYYY-MM-DD
review_period: [30/60/90 days post-launch]
sources:
  - outputs/gtm/gtm-[initiative]-YYYY-MM-DD.md (modified: YYYY-MM-DD)
  - (actual metrics from [analytics source])
downstream:
  - (process improvements to PM OS)
---

# Launch Review: [Initiative]

## Launch Context
**What:** [Product/feature name]
**Launch date:** [YYYY-MM-DD]
**Review period:** [30/60/90 days]
**Original plan:** [Link to GTM plan or charter]

## Predicted vs Actual

### Leading Indicators (Early Signals)

| Metric | Predicted | Actual | Variance | Explanation |
|--------|-----------|--------|----------|-------------|
| [Signups Week 1] | [N] | [N] | [+/-X%] | [Why different?] |

### Lagging Indicators (Business Outcomes)

| Metric | Predicted | Actual | Variance | Explanation |
|--------|-----------|--------|----------|-------------|
| [Revenue Q1] | $[N] | $[N] | [+/-X%] | [Why different?] |

### Overall Assessment

**Result:** Exceeded expectations / Mixed results / Missed targets

**Summary:** [1-2 sentences on overall outcome]

## What Went Well

| What | Why (Root Cause) | Pattern to Reinforce | Evidence |
|------|------------------|---------------------|----------|
| [Success 1] | [Root cause] | [Repeatable lesson] | [Metric or feedback] |

## What Went Wrong

| What | Why (Root Cause) | Fix for Next Time | Owner |
|------|------------------|-------------------|-------|
| [Failure 1] | [Root cause - use 5 whys] | [Specific process change] | [PM/team] |

## Lessons Learned

### Lesson 1: [Title]
**What we learned:** [Description]
**Why it matters:** [Impact on future launches]
**Action:** Update `skills/[skill-name]/SKILL.md` - [Specific change]

## Recommendations for Next Launch

### Do More Of
1. [Success pattern to repeat]

### Do Less Of / Stop
1. [Failure pattern to avoid]

### Try Differently
1. [Experiment to try next time]

## Sources Used
- [GTM plan path]
- [Analytics dashboard link]

## Claims Ledger

| Claim | Type | Source |
|-------|------|--------|
| [Metric exceeded target] | Evidence | [Analytics:dashboard] |
| [Root cause was Y] | Assumption | [PM analysis - needs validation] |
```

**Step 7: Apply Learnings**

Actually update the identified files:
1. Edit skill files with lessons learned
2. Update templates with new sections
3. Add vocabulary terms
4. Document quality gates

---

## Mode: --patterns

### Process

**Step 1: Identify Analysis Scope**

Ask user (or determine from hook trigger):
- "Which skill should I analyze?" (e.g., generating-quarterly-charters)
- "What time period?" (e.g., last 6 months, all time)
- "Looking for anything specific?" (e.g., what makes charters get approved?)

**Step 2: Read History Files**

For the target skill, read all files in `history/[skill-name]/`:
- Count total outputs
- Note date range
- Identify versions (e.g., charter v1, v2, v3)

Also read related decision logs:
- `outputs/decisions/*.md` for outcome data
- Look for feedback ratings, success/failure notes

**Step 3: Pattern Detection**

Analyze for:

### Success Patterns
- What do successful outputs have in common?
- Format patterns (tables vs bullets, length, structure)
- Content patterns (evidence types, specificity, metrics format)
- Process patterns (review cycles, stakeholder involvement)

### Failure Patterns
- What do rejected/reworked outputs have in common?
- What causes revisions?
- What warnings were ignored?

### Personal Preferences
- User's consistent choices (format, detail level, tone)
- User's typical review cycle
- User's stakeholder patterns

**Step 4: Quantify Patterns**

For each pattern, provide evidence:
- **Sample size:** N outputs analyzed
- **Correlation:** X/Y successful outputs had this pattern
- **Confidence:** Strong (>80%), Medium (50-80%), Weak (<50%)

**Step 5: Generate Learned Rules File**

Write to `.claude/rules/learned/[skill-name]-patterns.md`:

```markdown
---
generated: YYYY-MM-DD HH:MM
skill: learn --patterns
analyzed_skill: [skill-name]
sample_size: [N]
date_range: [YYYY-MM-DD to YYYY-MM-DD]
paths:
  - "outputs/[output-dir]/**/*.md"
  - "history/[skill-name]/**/*.md"
---

# Learned Patterns: [Skill Name]

## Analysis Summary
- **Outputs analyzed:** [N] files from history/[skill-name]/
- **Time period:** [Date range]
- **Outcomes tracked:** [M] decision logs with results
- **Confidence:** Patterns based on [N] data points

## Success Patterns (Correlate with Approved/Successful Outputs)

### Pattern 1: [Title]
**Observation:** [What we see in successful outputs]
**Evidence:** [X/Y] successful outputs had this ([%])
**Recommendation:** Default to this pattern

## Failure Patterns (Correlate with Rejected/Reworked Outputs)

### Anti-Pattern 1: [Title]
**Observation:** [What we see in failed outputs]
**Evidence:** [X/Y] rejected outputs had this ([%])
**Recommendation:** Avoid this pattern

## Recommendations for [Skill Name]

Based on analysis of [N] outputs:

1. **[Recommendation 1]:** [Specific guidance]
   - Evidence: [X/Y outputs ([%])]
   - Confidence: Strong/Medium/Weak

## Quality Trends Over Time

| Time Period | Outputs | Approved First Try | Avg Revisions | Quality Trend |
|-------------|---------|-------------------|---------------|---------------|
| [Q1 YYYY] | [N] | [%] | [N] | up/stable/down |

## Unknowns / Need More Data

- [Pattern needs more data points to confirm]
```

**Step 6: Update Personal Preferences**

Append or update `CLAUDE.local.md`:

```markdown
# Learned Preferences (from history analysis)

## [Skill Name] Preferences
**Last updated:** YYYY-MM-DD
**Based on:** [N] outputs

- User prefers [format/style choice] ([X/Y times, [%]])
- User's typical review cycle: [N rounds before approval]
- User always requests [specific thing] ([observed pattern])
```

---

## Quick Reference

### Pattern Confidence Levels

| Confidence | Sample Size | Correlation | Interpretation |
|------------|-------------|-------------|----------------|
| **Strong** | N >= 10 | >=80% | Reliable pattern, use as default |
| **Medium** | N >= 5 | 50-80% | Promising pattern, test more |
| **Weak** | N < 5 | <50% | Insufficient data, need more |

### Root Cause Analysis (5 Whys)

**Problem:** "Documentation was incomplete at launch"
1. Why? -> Docs not reviewed before launch
2. Why? -> No docs review in launch checklist
3. Why? -> Checklist doesn't include docs
4. Why? -> No one responsible for docs quality
5. Why? -> Role not defined in GTM plan
**Root cause:** GTM template missing docs owner/checklist

---

## Common Mistakes

### --decision Mode
- **No review date:** Logging without follow-up
- **Retrofitting rationale:** Adjusting reasoning after knowing outcome
- **Vague success criteria:** "It worked" vs measurable criteria

### --launch Mode
- **Blame, not learning:** Focusing on who failed vs why system failed
- **Surface-level:** "Communication was bad" -> Dig deeper with 5 whys
- **No follow-through:** Identifying lessons but not updating processes
- **Confirmation bias:** Only reviewing metrics that confirm expectations

### --patterns Mode
- **Overfitting:** Seeing patterns in noise (need sufficient sample size)
- **Confirmation bias:** Only looking for patterns you expect
- **No validation:** Not tracking whether patterns actually improve outcomes

---

## Verification Checklist

### --decision
- [ ] Decision log created with context and options
- [ ] Rationale tagged as Evidence/Assumption
- [ ] Success criteria are measurable
- [ ] Review date set (30-90 days)
- [ ] Calendar reminder created

### --launch
- [ ] Read original GTM plan/charter
- [ ] Collected actual metrics (leading + lagging)
- [ ] Identified 3-5 successes with root causes
- [ ] Identified 3-5 failures with root causes
- [ ] Extracted lessons with specific PM OS updates
- [ ] Actually updated skill files/templates

### --patterns
- [ ] Read all history files for target skill
- [ ] Cross-referenced decision logs for outcomes
- [ ] Identified success patterns with evidence
- [ ] Identified failure patterns with evidence
- [ ] Quantified confidence levels
- [ ] Wrote learned rules to `.claude/rules/learned/`
- [ ] Updated `CLAUDE.local.md` with preferences

---

## Output Locations

| Mode | Primary Output | History |
|------|---------------|---------|
| `--decision` | `outputs/decisions/YYYY-MM-DD-[title].md` | `history/learn/decisions/` |
| `--launch` | `outputs/reviews/launch-review-[initiative]-YYYY-MM-DD.md` | `history/learn/reviews/` |
| `--patterns` | `.claude/rules/learned/[skill]-patterns.md` | `history/learn/patterns/` |

---

## Evidence Tracking

| Claim | Type | Source |
|-------|------|--------|
| [Decision rationale] | Evidence/Assumption | [Document reference] |
| [Launch metric result] | Evidence | [Analytics dashboard] |
| [Pattern X correlates with success] | Evidence | [Analyzed N=X outputs] |
| [Pattern will improve outcomes] | Assumption | [Needs validation] |
