---
name: skill-judge
description: "Evaluate Agent Skills against official specifications and 8-dimensional scoring framework. Use when: (1) Reviewing SKILL.md files for quality, (2) Auditing skill packages for compliance, (3) Improving existing skills with actionable feedback, (4) Validating skill design before deployment. Outputs structured evaluation report with dimension scores and improvement suggestions."
---

# Skill Judge

Evaluate Agent Skills against official specifications and best practices using an 8-dimensional scoring framework (120 points total).

## Decision Tree

Choose evaluation approach based on context:

| Evaluation Context | Primary Focus | When to Use |
|--------------------|---------------|-------------|
| Quick review (5-10 min) | Description + Knowledge Delta | Initial screening, triage |
| Full audit (20-30 min) | All 8 dimensions | Comprehensive quality assessment |
| Compliance check (5 min) | Frontmatter + Description | Format validation only |
| Improvement guidance (30+ min) | All dimensions + detailed feedback | Skill optimization |

## Workflow

### Step 1: Load Evaluation Framework

**MANDATORY - READ ENTIRE FILE**: Before proceeding, you MUST read [`evaluation-guide.md`](references/evaluation-guide.md) completely from start to finish. **NEVER set any range limits when reading this file.**

### Step 2: Quick Scan (5 minutes)

Read SKILL.md completely and identify:
- **Skill type**: Mindset (~50 lines), Navigation (~30 lines), Philosophy (~150 lines), Process (~200 lines), Tool (~300 lines)
- **Line count**: Is it appropriate for the type?
- **Description quality**: Does it have WHAT, WHEN, and keywords?
- **Knowledge delta**: Any obvious "explaining basics" sections?

### Step 3: Dimension Evaluation (15-20 minutes)

Evaluate each dimension in order:

| Priority | Dimension | Points | Why This Order |
|----------|-----------|--------|----------------|
| 1 | D4: Specification Compliance (Description) | 15 | Poor description = skill never used |
| 2 | D1: Knowledge Delta | 20 | Core dimension - determines value |
| 3 | D7: Pattern Recognition | 10 | Sets expectations for structure |
| 4 | D5: Progressive Disclosure | 15 | Checks if references are used properly |
| 5 | D2: Mindset + Procedures | 15 | Evaluates thinking patterns |
| 6 | D3: Anti-Pattern Quality | 15 | Checks for NEVER lists |
| 7 | D6: Freedom Calibration | 15 | Matches freedom to task fragility |
| 8 | D8: Practical Usability | 15 | Can Agent actually use it? |

### Step 4: Score Calculation

Sum all dimension scores (max 120 points). Calculate percentage and assign grade:

| Score Range | Grade | Interpretation |
|-------------|-------|----------------|
| 96-120 | A | Excellent - Production ready |
| 84-95 | B | Good - Minor improvements needed |
| 72-83 | C | Acceptable - Moderate improvements needed |
| 60-71 | D | Poor - Significant improvements needed |
| <60 | F | Fail - Major redesign required |

### Step 5: Generate Report

**MANDATORY - READ ENTIRE FILE**: Before generating report, you MUST read [`scoring-guide.md`](references/scoring-guide.md) completely.

Output structured report in this format:

```markdown
# Skill Evaluation Report

## Overview
- **Skill**: [skill-name]
- **Type**: [Mindset/Navigation/Philosophy/Process/Tool]
- **Total Score**: [X]/120 ([X]%)
- **Grade**: [A/B/C/D/F]

## Dimension Scores

| Dimension | Score | Max | Notes |
|-----------|-------|-----|-------|
| D1: Knowledge Delta | [X] | 20 | [brief notes] |
| D2: Mindset + Procedures | [X] | 15 | [brief notes] |
| D3: Anti-Pattern Quality | [X] | 15 | [brief notes] |
| D4: Specification Compliance | [X] | 15 | [brief notes] |
| D5: Progressive Disclosure | [X] | 15 | [brief notes] |
| D6: Freedom Calibration | [X] | 15 | [brief notes] |
| D7: Pattern Recognition | [X] | 10 | [brief notes] |
| D8: Practical Usability | [X] | 15 | [brief notes] |

## Critical Issues (Must Fix)
1. [Issue 1]
2. [Issue 2]

## Improvement Suggestions (Should Fix)
1. [Suggestion 1]
2. [Suggestion 2]

## Strengths (Keep)
1. [Strength 1]
2. [Strength 2]
```

## NEVER Do When Evaluating

**Scoring Mistakes**
- NEVER give high scores for "professional formatting" alone - content matters most
- NEVER ignore token waste - every redundant paragraph = deduction
- NEVER let length impress you - 43-line skill can outperform 500-line skill
- NEVER assume all procedures are valuable - distinguish domain-specific from generic

**Evaluation Mistakes**
- NEVER skip mentally testing decision trees - do they lead to correct choices?
- NEVER forgive explaining basics with "but it provides helpful context"
- NEVER overlook missing anti-patterns - no NEVER list = significant gap
- NEVER undervalue description field - poor description = skill never used

**Reporting Mistakes**
- NEVER give vague feedback like "improve quality" - be specific
- NEVER suggest changes without explaining WHY
- NEVER provide scores without actionable improvement suggestions

## Quick Reference

### Knowledge Delta Red Flags (D1)
- "What is [basic concept]" sections
- Step-by-step tutorials for standard operations
- Explaining how to use common libraries
- Generic best practices ("write clean code")
- Definitions of industry-standard terms

### Knowledge Delta Green Flags (D1)
- Decision trees for non-obvious choices
- Trade-offs only experts know
- Edge cases from real-world experience
- "NEVER do X because [non-obvious reason]"
- Domain-specific thinking frameworks

### Anti-Pattern Quality (D3)
- Score 0-3: No anti-patterns mentioned
- Score 4-7: Generic warnings ("avoid errors")
- Score 8-11: Specific NEVER list with some reasoning
- Score 12-15: Expert-grade anti-patterns with WHY

### Description Quality (D4)
- Must answer: WHAT (functionality), WHEN (trigger scenarios), KEYWORDS (searchable terms)
- Poor: "处理文档相关功能" (vague, no triggers, no keywords)
- Excellent: "Comprehensive document creation, editing, and analysis. Use when Claude needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying content, (3) Working with tracked changes"

### Pattern Recognition (D7)
| Pattern | ~Lines | When to Use |
|---------|--------|-------------|
| Mindset | ~50 | Creative tasks requiring taste |
| Navigation | ~30 | Multiple distinct sub-scenarios |
| Philosophy | ~150 | Art/creation requiring originality |
| Process | ~200 | Complex multi-step projects |
| Tool | ~300 | Precise operations on specific formats |

### Freedom Calibration (D6)
- High freedom: Creative/Design tasks (frontend-design)
- Medium freedom: Code review, judgment-based tasks
- Low freedom: File format operations (docx, pdf, xlsx)

## Output Format

Always output evaluation report in the structured format shown in Step 5. Include:
- Overview with total score and grade
- Dimension scores table with notes
- Critical issues (must fix)
- Improvement suggestions (should fix)
- Strengths (keep)

Do NOT output:
- Unstructured feedback
- Scores without explanations
- Generic comments without specific examples
