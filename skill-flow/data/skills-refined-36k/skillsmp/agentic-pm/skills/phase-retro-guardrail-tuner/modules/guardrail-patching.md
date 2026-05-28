# Module: Guardrail Patching (Concrete Changes)

## Objective

Propose specific, minimal changes to prevent pattern recurrence.

## Rules for proposals

1. **Smallest change**: Propose the smallest change that prevents recurrence
2. **Templates over prose**: Prefer templates/checklists over "remember to..."
3. **Auditable**: Make guardrails binary (pass/fail), not subjective
4. **Evidence-based**: Link every proposal to a specific pattern

## Patch-style format

Every proposal must use this format:

```markdown
### Proposal: <title>

**Pattern addressed**: <pattern name>

**Target file**: <path>
- Example: `.claude/skills/agentic-pm/templates/task-file.template.md`
- Example: `.claude/skills/agentic-pm/modules/task-file-authoring.md`

**Change type**: Add / Replace / Remove

**Exact text block**:
```diff
+ <new text to add>
- <old text to remove>
```

**Rationale**: <1-2 sentences explaining what failure this prevents>

**Applies to**: <all tasks / tasks touching schema / tasks with dependencies / etc.>
```

## Change categories

### Template changes
- Add new sections
- Add checklist items
- Clarify instructions
- Add examples

### Module changes
- Add guardrail rules
- Add red flags
- Clarify procedures
- Add stop-and-ask triggers

### Schema changes
- Add required fields
- Add validation rules
- Add new types

## Anti-patterns to avoid

- **Too big**: Changes that require extensive training
- **Too vague**: "Be more careful about X"
- **Not testable**: Can't verify if followed
- **Over-engineered**: Adds bureaucracy without value

## Proposal validation

Before finalizing, verify:
- [ ] Change is minimal
- [ ] Change is specific (exact text provided)
- [ ] Change is auditable (can verify compliance)
- [ ] Change addresses root cause (not symptom)
- [ ] Change won't create new friction
