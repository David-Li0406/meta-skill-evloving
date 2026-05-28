---
name: question-refiner
description: Transform raw research questions into structured, validated research prompts with automatic research type detection and output format validation. Ensures prompts are ready for research-executor with comprehensive quality checks.
---

# Question Refiner

## Overview

Transform vague research questions into structured, actionable research prompts through strategic clarifying questions with automatic research type detection and quality validation.

## When to Use

- User provides a raw, unstructured research question
- Research scope is unclear or too broad
- Need validated structured prompt for research-executor
- Want to ensure prompt meets quality standards (≥8.0)

## Core Approach

**Progressive Questioning** (2 rounds max):
1. **Round 1** (3 questions): Topic focus, output format, audience
2. **Round 2** (conditional): Scope, sources, special requirements
3. **Auto-detect** research type → Select template → Generate & validate

## Research Type Detection

| Type | Indicators | Example |
|------|-----------|---------|
| **Exploratory** | "what is", "overview", "landscape" | "What is the AI market like?" |
| **Comparative** | "vs", "compare", "difference" | "Compare GPT-4 vs Claude" |
| **Problem-Solving** | "how to", "solve", "fix" | "How to improve API performance" |
| **Forecasting** | "future", "trend", "prediction" | "Future of quantum computing" |
| **Deep Dive** | "technical", "architecture" | "How does BERT work internally" |
| **Market Analysis** | "market", "industry", "competition" | "AI chip market analysis" |

## Output Structure

```markdown
### RESEARCH TYPE
[auto-detected type]

### TASK
[Clear, specific research objective]

### CONTEXT/BACKGROUND
[Why this matters, who will use it]

### SPECIFIC QUESTIONS
1-7 concrete sub-questions

### KEYWORDS
[Search terms ≥5]

### CONSTRAINTS
- Timeframe: [e.g., 2020-present]
- Geography: [e.g., global]
- Source types: [academic, industry, news]

### OUTPUT FORMAT
- Type: [comprehensive_report|executive_summary|comparison_table]
- Citation style: [inline-with-url|footnotes]

### QUALITY SCORE
[0-10, must be ≥8.0]
```

## Quality Validation

| Component | Weight | Criteria |
|-----------|--------|----------|
| Completeness | 30% | All required fields present |
| Specificity | 30% | Questions are specific, not vague |
| Keyword Richness | 20% | ≥5 search terms with synonyms |
| Constraint Clarity | 20% | Clear, realistic constraints |

**Process**: Generate → Validate → If score < 8.0: Refine (max 2 attempts)

## Token Optimization

> 📋 **Reference**: `.claude/shared/constants/token_optimization.md`

**Context Budget**: 10k tokens max

## Error Handling

> 📋 **Reference**: `.claude/shared/constants/error_codes.md`

- **E001**: Insufficient context → Ask clarifying questions
- **E003**: Validation failed → Refine and retry
- **E004**: Quality < 8.0 after retries → Request manual review

---

**See also**: [Skill Base Template](../../shared/templates/skill_base_template.md)

## Examples

See [examples.md](./examples.md) for detailed interaction patterns.

## Detailed Instructions

See [instructions.md](./instructions.md) for complete questioning strategy.
