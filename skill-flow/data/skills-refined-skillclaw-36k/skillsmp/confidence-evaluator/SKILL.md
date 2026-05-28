---
name: confidence-evaluator
description: Evaluate requirement clarity and completeness using ISO/IEC/IEEE 29148:2018 criteria. Use when user asks to implement features, fix bugs, or make changes. Automatically invoked when confidence_policy is enabled in ai-settings.json.
---

# Confidence Evaluator Skill

You are evaluating the clarity and completeness of a user requirement against **ISO/IEC/IEEE 29148:2018** standards.

## When to Use This Skill

- User requests implementation of a feature
- User asks for bug fixes
- User proposes architectural changes
- Any task requiring code modifications

## Configuration

Read the threshold from `.ai/ai-settings.json`:
```json
{
  "framework": {
    "confidence_policy": true,
    "confidence_threshold": 85
  }
}
```

If `confidence_policy` is `false`, skip evaluation entirely.

## Evaluation Process

### Step 1: Calculate Intuitive Estimate

Give your subjective confidence (0-100) based on:
- How well you understand the requirement
- Whether you can identify all necessary changes
- Clarity of success criteria

### Step 2: Calculate Structured Score (maximum 100 points)

Evaluate the requirement against these criteria:

#### Requirements Category (60 points)

| Criterion | Weight | Evaluation Questions |
|-----------|--------|---------------------|
| Unambiguous formulation | 20 | Is there only one way to interpret this? |
| Completeness (input/output/constraints) | 20 | Are all inputs, outputs, and constraints defined? |
| Verifiable result | 15 | Can completion be objectively measured? |
| Consistency with project | 10 | Does it conflict with existing requirements? |
| Rationale (source) | 5 | Is the reason for this requirement stated? |
| Technical feasibility | 5 | Is it achievable within constraints? |

#### Formatting Category (40 points)

| Criterion | Weight | Evaluation Questions |
|-----------|--------|---------------------|
| Structured prompt | 10 | Is it logically organized? |
| Explicit tasks | 7 | Does it use "must/shall/должен"? |
| Result examples | 4 | Are concrete examples provided? |
| Decomposable | 4 | Can it be broken into subtasks? |

### Step 3: Calculate Final Confidence

```
confidence = (intuitive_estimate + structured_score) / 2
```

### Step 4: Compare with Threshold

If `confidence < threshold`:
- **DO NOT** proceed with implementation
- Return 1-3 clarifying questions
- Provide an example of a well-formed requirement

If `confidence >= threshold`:
- Proceed with the task

## Output Format

### When Confidence is Sufficient

```
Confidence Assessment: 87/100 (threshold: 85)

- Intuitive estimate: 85/100
- Structured score: 89/100
  - Requirements: 53/60
  - Formatting: 36/40

Proceeding with implementation...
```

### When Confidence is Insufficient

```
Confidence Assessment: 72/100 (threshold: 85)

- Intuitive estimate: 70/100
- Structured score: 74/100
  - Requirements: 42/60 (missing completeness criteria)
  - Formatting: 32/40 (no examples provided)

## Clarifying Questions

1. What are the expected input formats for this feature?
2. Should this handle edge cases like X, Y, Z?

## Improved Requirement Example

[Provide a rewritten version of the requirement with sufficient detail]
```

## References

See [iso_criteria.md](iso_criteria.md) for detailed ISO/IEC/IEEE 29148:2018 criteria explanations.
See [templates/clarifying_questions.md](templates/clarifying_questions.md) for question templates by requirement type.
