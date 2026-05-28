# Zero-Shot

Direct instruction without examples. The simplest technique.

## Template

```markdown
Task: [What to do]
Requirements: [List of specific requirements]
Format: [Exact output structure]
Constraints: [Boundaries and limitations]
```

## Example

```markdown
Task: Categorize this support ticket
Requirements:
- Assign one category: Bug, Feature, Question, or Billing
- Provide confidence score 0.0-1.0
- Give one-sentence reasoning
Format: JSON with keys: category, confidence, reasoning
Constraints: Only use provided categories, no additional fields
```

## When NOT to Use

- Task requires learning from examples → Use Few-shot
- Task requires reasoning steps → Use CoT
- Task is complex/exploratory → Use ToT
