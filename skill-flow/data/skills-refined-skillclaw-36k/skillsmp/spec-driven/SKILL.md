---
name: spec-driven
description: Spec-driven development workflow. Use when implementing new features, skills, or game mechanics. Ensures specs exist before code.
---

# Spec-Driven Development

## Workflow

Before writing ANY implementation code:

1. **Check for existing spec** in `/specs/`
2. **If no spec exists**, create one first
3. **If spec exists**, follow it exactly

## Spec Structure

Every spec should define:

```markdown
## Input
What data the skill/feature receives (use Pydantic models)

## Process  
Step-by-step logic (reference SRD rules if applicable)

## Output
Structured result (use Pydantic models)

## Edge Cases
What happens on invalid input, failures, etc.
```

## Implementation Rules

- Use `from __future__ import annotations`
- Use Pydantic for all input/output validation
- Skills MUST be stateless (no global variables)
- Skills MUST NOT call LLMs directly
- Use type hints: `str | None` not `Optional[str]`
- Follow existing patterns in `src/skills/`

## Testing

- Write tests BEFORE or alongside implementation
- Tests live in `tests/test_<module>.py`
- Use pytest with AAA pattern (Arrange-Act-Assert)
- Aim for 100% coverage
