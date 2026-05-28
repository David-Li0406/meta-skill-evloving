# Self-Consistency

Multiple independent reasoning paths with voting. For high-accuracy needs.

## Template

```xml
<task>
[Problem requiring high accuracy]
</task>

<instructions>
Generate 5 independent solutions. Each must use different reasoning.
Do not let previous solutions influence subsequent ones.

<solution id="1">
<reasoning>[Path 1]</reasoning>
<answer>[Result]</answer>
</solution>

<solution id="2">
<reasoning>[Path 2]</reasoning>
<answer>[Result]</answer>
</solution>

[... solutions 3-5 ...]

<consensus>
Most frequent answer: [Answer]
Appears in: [N/5] solutions
Confidence: [High/Medium/Low]
Final answer: [Selected]
</consensus>
</instructions>
```

## Example

```xml
<task>
What is 17% of 340?
</task>

<solution id="1">
<reasoning>Convert to decimal: 0.17 × 340 = 57.8</reasoning>
<answer>57.8</answer>
</solution>

<solution id="2">
<reasoning>10% of 340 = 34. 7% of 340 = 23.8. Total: 34 + 23.8 = 57.8</reasoning>
<answer>57.8</answer>
</solution>

<solution id="3">
<reasoning>17/100 × 340 = 5780/100 = 57.8</reasoning>
<answer>57.8</answer>
</solution>

<solution id="4">
<reasoning>340 × 17 = 5780. Divide by 100 = 57.8</reasoning>
<answer>57.8</answer>
</solution>

<solution id="5">
<reasoning>1% of 340 = 3.4. 17 × 3.4 = 57.8</reasoning>
<answer>57.8</answer>
</solution>

<consensus>
Most frequent answer: 57.8
Appears in: 5/5 solutions
Confidence: High
Final answer: 57.8
</consensus>
```

## When to Use

- Critical calculations
- High-stakes decisions
- When you need confidence scores
- Ambiguous problems with multiple valid interpretations

## When NOT to Use

- Token budget is tight (uses 5x tokens)
- Speed is critical
- Simple/obvious answers
- Creative tasks (no "right" answer)
