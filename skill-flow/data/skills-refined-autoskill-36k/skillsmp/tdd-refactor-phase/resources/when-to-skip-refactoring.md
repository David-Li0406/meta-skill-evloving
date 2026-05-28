# When to Skip Refactoring
**Version:** {{VERSION}}

Decision criteria for determining when to skip the REFACTOR phase in TDD.

---

## The Skip Decision

**Golden Rule:** Refactoring is optional. Tests passing is mandatory.

Skip refactoring when the cost/risk outweighs the benefit for the current iteration.

---

## Time Constraints

### Skip When:
- Sprint deadline is imminent
- Critical bug fix needs deployment
- Demo or release is hours away
- Time box for feature has expired

### Don't Skip When:
- "No time" is just an excuse for technical debt
- Code will be touched again soon
- Skipping creates compound problems

### Decision Framework
```
Time available > 15 minutes → Consider refactoring
Time available < 15 minutes → Skip, create tech debt ticket
Deadline today → Skip unless critical clarity issue
```

---

## Code Stability

### Skip When:
- Code is unlikely to change again
- Feature is temporary/experimental
- Area is scheduled for replacement
- One-off script or utility

### Don't Skip When:
- Code is in active development path
- Multiple developers will touch it
- It's core business logic
- Tests will rely on this code

### Stability Assessment
| Code Type | Refactor Priority |
|-----------|------------------|
| Core domain logic | High |
| Shared utilities | High |
| Feature-specific code | Medium |
| One-off scripts | Low |
| Deprecated code | Skip |

---

## Risk Assessment

### High Risk - Consider Skipping:
- Refactoring touches many files
- Complex interdependencies
- No comprehensive test coverage
- Team unfamiliar with area
- Production incident ongoing

### Low Risk - Proceed:
- Change is localized
- Good test coverage exists
- Simple, mechanical transformation
- Team knows the code well

### Risk Matrix
```
High Impact + Low Confidence → Skip
High Impact + High Confidence → Careful refactor
Low Impact + Low Confidence → Skip
Low Impact + High Confidence → Refactor
```

---

## Code Smell Severity

### Must Refactor (Don't Skip):
- Security vulnerabilities
- Data corruption risks
- Memory leaks
- Blocking bugs

### Should Refactor:
- Duplicated logic (3+ occurrences)
- Functions > 50 lines
- Deeply nested conditionals
- Misleading names

### Can Skip:
- Minor naming improvements
- Style preferences
- Premature abstractions
- "Nicer" but not clearer

---

## Quick Decision Checklist

Before skipping, verify:
- [ ] Tests are passing and comprehensive
- [ ] Code is readable enough for next developer
- [ ] No obvious bugs or security issues
- [ ] Tech debt is documented if significant

### Skip Signals
- ✓ Code works and is reasonably clear
- ✓ Improvement is cosmetic only
- ✓ Time pressure is real and justified
- ✓ Risk of breaking something is high

### Don't Skip Signals
- ✗ You don't understand what you wrote
- ✗ Copy-paste created duplication
- ✗ Names are misleading
- ✗ Next feature will touch this code

---

## Documenting Skipped Refactoring

When you skip, document:
```
// TODO: Refactor - [what needs improving]
// Skipped: [date] - [reason]
```

Or create a tech debt ticket with:
- What refactoring was skipped
- Why it was skipped
- Suggested approach when addressed
- Priority/impact assessment
