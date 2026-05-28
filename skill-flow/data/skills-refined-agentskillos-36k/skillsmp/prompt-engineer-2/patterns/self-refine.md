# Self-Refine Pattern (Iterative Improvement)

## Overview

Generate initial output, critique it, then refine based on the critique. Repeat until quality threshold met.

**When to Use:**
- Quality-critical outputs
- Tasks with clear evaluation criteria
- When you need explainability of improvements
- Any generation task where iteration helps

**Community Validation:**
- Self-Refine paper (Madaan et al.): 500+ citations
- DeepLearning.AI: Most discussed agentic pattern
- 40-50% error reduction across benchmarks
- Cost-effective: 2-3 iterations = 80% of benefit

---

## Architecture

```
Generate → Critique → Refine → [Validate] → [Repeat if needed] → Final
```

---

## Generation Prompt

```xml
<role>
You are an expert at {{TASK_TYPE}} creation.
</role>

<task>
Create a {{TASK_TYPE}} that meets these requirements:
</task>

<requirements>
{{REQUIREMENTS}}
</requirements>

<format>
{{FORMAT_SPECIFICATION}}
</format>

<instructions>
1. Carefully analyze all requirements
2. Create your best initial attempt
3. Ensure all requirements are addressed
4. Follow the specified format exactly
</instructions>

Generate your best attempt:
```

---

## Critique Prompt

```xml
<role>
You are an expert critic evaluating a {{TASK_TYPE}}.
Your job is to find issues and suggest specific improvements.
</role>

<original_requirements>
{{REQUIREMENTS}}
</original_requirements>

<generated_output>
{{GENERATED_OUTPUT}}
</generated_output>

<evaluation_criteria>
1. **Completeness**: Does it address all requirements? What's missing?
2. **Clarity**: Are instructions unambiguous? What's confusing?
3. **Correctness**: Are there logical errors or inconsistencies?
4. **Format**: Does it match the specified structure?
5. **Quality**: Examples relevant? Appropriate detail level?
</evaluation_criteria>

<format>
<evaluation>
## Criterion: Completeness
**Score**: X/5
**Issues**: [specific issues found]
**Suggestions**: [concrete improvements]

## Criterion: Clarity
**Score**: X/5
**Issues**: [specific issues found]
**Suggestions**: [concrete improvements]

[Continue for each criterion...]
</evaluation>

<overall_assessment>
**Total Score**: X/25
**Keep**: [what should be preserved]
**Fix**: [what must be changed]
**Add**: [what's missing]
</overall_assessment>
</format>

Evaluate this output thoroughly:
```

---

## Refinement Prompt

```xml
<role>
You are improving a {{TASK_TYPE}} based on expert critique.
Preserve what works while addressing identified issues.
</role>

<original_output>
{{GENERATED_OUTPUT}}
</original_output>

<critique>
{{CRITIQUE_OUTPUT}}
</critique>

<requirements>
{{ORIGINAL_REQUIREMENTS}}
</requirements>

<instructions>
1. Review the critique carefully
2. Address each issue identified in "Fix"
3. Add each element listed in "Add"
4. Preserve everything listed in "Keep"
5. Maintain the original format
6. Do NOT introduce new issues
</instructions>

Create an improved version:
```

---

## Validation Prompt (Optional)

```xml
<role>
You are a validator checking if improvements were successfully applied.
</role>

<original_issues>
{{ISSUES_FROM_CRITIQUE}}
</original_issues>

<refined_output>
{{REFINED_OUTPUT}}
</refined_output>

<checklist>
For each original issue:
- [ ] Issue resolved?
- [ ] No regression introduced?
- [ ] Quality improved?
</checklist>

<format>
<validation>
## Issue 1: [original issue]
**Resolved**: YES/NO
**Evidence**: [how it was fixed or why not]

## Issue 2: [original issue]
...
</validation>

<summary>
**Issues Resolved**: X/Y
**New Issues**: [any regressions]
**Recommendation**: ACCEPT / ITERATE AGAIN
</summary>
</format>
```

---

## Implementation Pattern

```python
def self_refine(task: str, requirements: str, max_iterations: int = 3) -> str:
    # Step 1: Generate initial output
    output = llm_call(GENERATE_PROMPT.format(
        TASK_TYPE=task,
        REQUIREMENTS=requirements
    ))

    for i in range(max_iterations):
        # Step 2: Critique
        critique = llm_call(CRITIQUE_PROMPT.format(
            REQUIREMENTS=requirements,
            GENERATED_OUTPUT=output
        ))

        # Check if quality threshold met
        score = extract_score(critique)
        if score >= 20:  # 80% threshold (20/25)
            break

        # Step 3: Refine
        output = llm_call(REFINE_PROMPT.format(
            GENERATED_OUTPUT=output,
            CRITIQUE_OUTPUT=critique,
            ORIGINAL_REQUIREMENTS=requirements
        ))

    return output
```

---

## Iteration Guidelines

| Score | Quality | Action |
|-------|---------|--------|
| 22-25 | Excellent | Accept immediately |
| 18-21 | Good | Accept or 1 iteration |
| 14-17 | Fair | 1-2 iterations |
| 10-13 | Poor | 2-3 iterations |
| <10 | Very Poor | Consider redesign |

**Maximum iterations**: 3 (diminishing returns beyond)

---

## Best Practices

1. **Specific critique criteria**: Define exactly what to evaluate
2. **Actionable feedback**: Critique must suggest concrete fixes
3. **Preserve what works**: Explicitly state what to keep
4. **Track improvements**: Log score changes across iterations
5. **Know when to stop**: Set quality threshold
6. **Handle plateaus**: If score doesn't improve, try different approach

---

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| No improvement | Vague critique | Make criteria more specific |
| Regression | Lost good parts | Explicitly list "Keep" items |
| Infinite loop | No threshold | Add score-based exit |
| Overcorrection | Too aggressive refine | Ask to preserve structure |

---

## Variants

### Multi-Critic Self-Refine

```
Generate → Critic 1 → Critic 2 → Critic 3 → Aggregate → Refine
```

### Domain-Specific Self-Refine

```
Generate → Domain Expert Critique → Refine → User Feedback → Refine
```

### Comparative Self-Refine

```
Generate V1 → Generate V2 → Compare → Pick Best → Refine
```

---

## When NOT to Use

- Speed-critical applications (adds latency)
- Simple tasks with clear answers
- When evaluation criteria aren't clear
- Very limited token budget

---

## Version

**Version**: 1.0.0
**Source**: Madaan et al. Self-Refine paper
