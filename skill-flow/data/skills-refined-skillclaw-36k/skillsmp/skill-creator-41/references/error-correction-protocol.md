# Error Correction Protocol

How to capture learnings when mistakes occur, so they don't repeat.

## When to Add a Learning

Add a learning when ANY of these occur:

1. **Same mistake made 2+ times** - Pattern is sticky
2. **Non-obvious gotcha discovered** - Would trip up future Claude
3. **User explicitly corrects** - "No, do it this way..."
4. **Code review reveals issue** - CodeQL, lint, test failure
5. **Workaround needed** - Framework/library quirk

## Where to Add

### Skill-Specific Learning → `references/learnings.md`

Use when the learning is specific to ONE skill's domain:
- CI error patterns → `ci-doctor/references/learnings.md`
- Lint rule quirks → `lint-fixer/references/learnings.md`
- Test mocking issues → `test-writer/references/learnings.md`

### Global Learning → `.claude/LEARNINGS.md`

Use when the learning applies ACROSS skills:
- React/TypeScript patterns
- Supabase/database behaviors
- Process patterns (debugging, exploring)
- Codebase conventions

## How to Write a Learning

### Format for Gotchas

```markdown
### [Issue Title]
- **Pattern:** What triggers this mistake
- **Wrong:** The incorrect approach
- **Right:** The correct approach
- **Why:** Root cause explanation
```

### Format for Anti-Patterns (Table)

```markdown
| Don't | Do Instead | Reason |
|-------|------------|--------|
| `useEffect` with inline function | `useCallback` + dep | Prevents infinite loop |
```

### Format for Recent Corrections

```markdown
| Date | Issue | Fix | Applies To |
|------|-------|-----|------------|
| 2025-01-15 | Tab opens wrong | Controlled state | UI |
```

## Quality Checklist

Before adding a learning, verify:

- [ ] **Includes "Wrong" example** - Shows what NOT to do
- [ ] **Includes "Right" example** - Shows correct approach
- [ ] **Explains "Why"** - Not just what, but reason
- [ ] **Actionable** - Claude can act on this guidance
- [ ] **Concise** - One learning per entry
- [ ] **Correct location** - Skill-specific vs global

## Example: Adding a Learning

**Scenario:** Discovered that `useEffect` with inline functions causes infinite loops in admin pages.

**Decision:** This affects multiple pages → Global learning

**Add to `.claude/LEARNINGS.md`:**

```markdown
### React/TypeScript

| Learning | Context |
|----------|---------|
| Use `useCallback` for functions in `useEffect` deps | Prevents infinite loops in admin pages |
```

## Workflow Integration

### After Fixing a Bug

1. Ask: "Would this trip up future Claude?"
2. If yes → Add learning to appropriate file
3. Reference the learning in commit message (optional)

### After User Correction

1. Understand WHY they corrected
2. Add learning capturing the "why"
3. Thank user (they taught Claude something)

### After Code Review

1. Note patterns in review feedback
2. Add learnings for non-obvious issues
3. Skip obvious things Claude already knows

---

*This protocol ensures Claude gets smarter over time, avoiding repeated mistakes.*
