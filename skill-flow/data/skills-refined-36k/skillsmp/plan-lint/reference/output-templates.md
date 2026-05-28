# Plan Lint Output Templates

## PASS Response

```markdown
## Plan Lint: PASS

**Blast Radius**: [score] ([low/medium/high])

### Validation Summary
- [x] Primary feature: [name]
- [x] Impacted features: [count] identified
- [x] Invariants: [count] documented
- [x] Test plan: Complete
- [x] Workflow impact: Assessed

### Notes
[Any observations or suggestions, even though plan passes]

### Ready to Implement
Yes - proceed to Gate 2 (execution)
```

## WARN Response

```markdown
## Plan Lint: WARN

**Blast Radius**: [score] ([low/medium/high])

### Issues Found
1. **[Issue Category]**: [Specific problem]
   - Impact: [What could go wrong]
   - Fix: [How to address]

### Validation Summary
- [x] Primary feature: [name]
- [ ] Impacted features: Missing [X, Y]
- [x] Invariants: [count] documented
- [ ] Test plan: Incomplete
- [x] Workflow impact: Assessed

### Recommendation
Address warnings before proceeding.

### Ready to Implement
Conditional - fix warnings first, or proceed with caution
```

## FAIL Response

```markdown
## Plan Lint: FAIL

**Blast Radius**: [score] ([low/medium/high])

### Blocking Issues
1. **[Critical Issue]**: [Specific problem]
   - Why it blocks: [Explanation]
   - Required fix: [What must change]

### Validation Summary
- [ ] Primary feature: Not identified
- [ ] Invariants: None documented
- [x] Test plan: Present

### Required Actions
1. [Specific action to fix issue 1]
2. [Specific action to fix issue 2]

### Ready to Implement
No - must address blocking issues
```
