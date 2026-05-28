# Tuning Guide

How to improve Ralph loop results through observation and guardrails.

## The Playground Metaphor

> "Ralph is given instructions to construct a playground. Ralph comes home bruised because he fell off the slide, so you add a sign: 'SLIDE DOWN, DON'T JUMP.' Eventually all Ralph thinks about is the signs — that's a tuned prompt."

Start minimal. Observe failures. Add specific guardrails.

## Tuning Process

1. **Run with minimal prompt**
2. **Watch for failure patterns**
3. **Add guardrail for that specific failure**
4. **Repeat**

Don't anticipate failures. React to them.

## Common Failure Patterns

### Reimplements existing code

**Symptom:** Creates auth module that already exists.

**Guardrail:**
```markdown
99999. Before implementing, search codebase to confirm not already done.
```

### Incomplete implementations

**Symptom:** Writes function stubs, TODO comments, placeholder logic.

**Guardrail:**
```markdown
99999. Implement completely. No placeholders, stubs, or TODOs.
```

### Forgets to run tests

**Symptom:** Commits broken code, tests fail after session.

**Guardrail:**
```markdown
99999. Run tests before committing. Fix failures first.
```

### Too many changes per session

**Symptom:** Giant commits, refactors + features mixed.

**Guardrail:**
```markdown
99999. One task per session. Commit and exit after completing one task.
```

### Ignores the plan

**Symptom:** Works on low priority or random tasks.

**Guardrail:**
```markdown
99999. Follow IMPLEMENTATION_PLAN.md priorities strictly.
```

### Bloats documentation

**Symptom:** AGENTS.md grows into huge changelog.

**Guardrail:**
```markdown
99999. Keep AGENTS.md operational only (~50 lines).
```

### Wrong patterns/conventions

**Symptom:** Uses different style than existing code.

**Guardrail:**
```markdown
99999. Study existing code patterns before implementing. Match conventions.
```

### Hallucinates APIs

**Symptom:** Uses library functions that don't exist.

**Guardrail:**
```markdown
99999. Only use documented APIs. Check docs before using any library function.
```

## Guardrail Numbering

Higher numbers = higher priority (processed last, remembered more):

```markdown
1. Read codebase.
2. Choose one task.
3. Implement it.

99999. Search before implementing.
999999. Run tests before committing.
9999999. Never commit if tests fail.
```

New guardrails: add to end with more digits.

## When to Regenerate vs Tune

**Regenerate the plan when:**
- Agent is clearly off track
- Requirements changed
- Plan is outdated

**Tune the prompt when:**
- Same failure pattern repeats
- Agent misunderstands specific instructions
- Output quality issues

Plans are disposable. Prompts are refined.

## Diminishing Returns

Too many guardrails = agent only thinks about guardrails.

Signs of over-tuning:
- Agent confused by contradicting rules
- More time parsing instructions than working
- Output quality plateaus or declines

If this happens: start fresh with minimal prompt.

## Environment Variables

For CLI-specific tuning:

```bash
# Change agent
export GUMLOOP_CLI=amp

# Custom flags for unsupported CLIs
export GUMLOOP_FLAGS="--auto-approve --max-tokens 8000"
```
