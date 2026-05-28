# Maintenance

Documentation, cleanup, refactoring, and optimization.

## Mental Model

Maintenance is about health and hygiene. Keep the codebase clean and working.

```
Codebase: Accumulated code over time
         ↓
Review: Git history, current state, documentation
         ↓
Identify: Stale code, outdated patterns, documentation gaps
         ↓
Clean: Delete unused code, update patterns, improve docs
         ↓
Verify: Nothing broke, tests pass, docs are accurate
```

## Key Principles

### Understand Before Changing
Read git history. Understand why things are the way they are.
- That "weird" code might exist for a reason
- Patterns might have history you don't know
- Delete with confidence, not ignorance

### Delete More Than You Add
The best maintenance removes complexity.
- Delete unused code
- Simplify patterns
- Remove unnecessary abstractions
- Less code is better code

### One Change at a Time
Don't batch unrelated changes.
- Each change should be independently verifiable
- Problems are easier to isolate
- Easier to revert if something breaks

### Preserve Behavior
Unless explicitly changing functionality, behavior should be the same.
- Tests should still pass
- User experience should be unchanged
- APIs should work the same way

### Test After Each Change
Verify nothing broke before moving on.
- Run related tests
- Do quick manual verification
- Don't batch changes then test at the end

## Agent Browser CLI Usage

Verify UI still works after maintenance changes.

**Before changes (baseline):**
```bash
agent-browser open http://localhost:3000
# Document current behavior
agent-browser screenshot before-maintenance.png
```

**After changes (verification):**
```bash
agent-browser open http://localhost:3000
# Verify same behavior
agent-browser screenshot after-maintenance.png
# Compare visually, behavior should match
```

## What to Extract from Users

- Goals for the maintenance work
- Areas of concern or known technical debt
- What should NOT be changed
- Testing requirements
- Documentation needs
- Priority areas
- Success criteria

## Types of Maintenance Work

| Type | Focus |
|------|-------|
| Documentation | README, inline comments, API docs |
| Cleanup | Dead code, unused files, outdated dependencies |
| Refactoring | Pattern updates, structure improvements |
| Optimization | Performance improvements, resource usage |
| Organization | File structure, naming, modularity |

## Red Flags

You're doing it wrong if:
- Changing things "because they're ugly" without clear benefit
- Batching unrelated changes
- Deleting code without verifying it's unused
- Not testing after changes
- Refactoring for hypothetical future needs
- Adding features under the guise of maintenance
- Changing behavior without it being explicitly requested

## Story Structure for Maintenance

Typical maintenance PRD structure:
1. Review current state - git history, code analysis
2. Identify targets - what needs cleaning/updating
3. Execute changes (one at a time) - implement each change
4. Verify each change - tests pass, behavior preserved
5. Final verification - full test suite, browser verification
6. Document - what was done, why, any follow-up
