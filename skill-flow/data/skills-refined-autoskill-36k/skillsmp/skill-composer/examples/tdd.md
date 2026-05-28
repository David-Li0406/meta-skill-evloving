# Example: Test-Driven Development

**Source**: https://github.com/obra/superpowers/tree/main/skills/test-driven-development
**Pattern**: Strict methodology enforcement with rationalization pre-emption
**Use case**: Ensuring tests validate behavior by requiring failure first

## Key Sections from SKILL.md

### The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

### Red-Green-Refactor Cycle

Includes **Graphviz dot diagram** showing the full cycle with verification steps.

### Good vs Bad Examples

Uses `<Good>` and `<Bad>` tags for code examples:

```typescript
<Good>
test('retries failed operations 3 times', async () => {
  // Clear name, tests real behavior, one thing
});
</Good>

<Bad>
test('retry works', async () => {
  // Vague name, tests mock not code
});
</Bad>
```

### Common Rationalizations Table

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |

### Red Flags Section

- Code before test
- Test passes immediately
- Can't explain why test failed
- "Just this once" rationalization

**Action**: Delete code and begin TDD cycle fresh.

### Verification Checklist

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)

### When Stuck Table

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write wished-for API. Write assertion first. |
| Test too complicated | Design too complicated. Simplify interface. |
| Must mock everything | Code too coupled. Use dependency injection. |

## Analysis

**What makes this work**:

1. **Iron Law**: Single unbreakable rule that anchors everything
2. **Rationalization tables**: Pre-empts common excuses with counters
3. **Visual examples**: `<Good>` and `<Bad>` tags make patterns clear
4. **Graphviz diagram**: Visual flow of the RED-GREEN-REFACTOR cycle
5. **Verification checklist**: Concrete completion criteria
6. **Red flags**: Observable signals for self-monitoring
7. **When Stuck table**: Solutions for common blockers

## Unique Features

**Graphviz Diagram**:
Actual dot code embedded in skill showing the cycle with decision diamonds and feedback loops.

**Rationalization Pre-emption**:
Extensive section addressing every common excuse:
- "Too simple to test"
- "I'll write tests after"
- "Already manually tested it"
- "Deleting X hours is wasteful"
- "TDD is dogmatic"

Each excuse gets a "Reality" counter-argument.

**Mandatory Verification Steps**:
Not just "write test" - must "Verify RED" and "Verify GREEN" as separate mandatory steps.

**"Why Order Matters" Section**:
Philosophical explanation of why test-first vs test-after matters.

## Pattern Type

**Discipline enforcement** - Uses multiple techniques:
- Iron Law (unbreakable rule)
- Rationalization tables (address excuses)
- Verification checklists (concrete steps)
- Red flags (self-monitoring)
- Visual diagrams (process flow)

## Key Takeaways

1. **Multiple enforcement mechanisms** - Iron Law + tables + checklists + red flags
2. **Pre-empt rationalizations** - Address excuses before they arise
3. **Visual aids help** - Graphviz diagram shows process flow
4. **Good/Bad examples** - `<Good>` and `<Bad>` tags make patterns concrete
5. **Verification as separate steps** - Not just "write test" but "verify it fails correctly"
6. **Solution tables** - "When Stuck" provides actionable solutions
7. **Mandatory deletion** - No grandfathering code written before tests
