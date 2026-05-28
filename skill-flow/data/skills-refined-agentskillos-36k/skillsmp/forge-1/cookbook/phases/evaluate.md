# Evaluate Phase Guide

**Purpose**: Verification - Does output match intent?

## Key Question

Does the implementation satisfy all acceptance criteria from Refine, handle edge cases correctly, and meet security requirements?

## Verification Process

1. **Criteria Check**: Line-by-line against Refine specs
2. **Edge Case Testing**: Both specified AND discovered
3. **Integration Testing**: Components work together
4. **Security Review**: OWASP top 10, auth, data exposure

## Criteria Verification

For each acceptance criterion from Refine:
- [ ] Test exists that verifies the criterion
- [ ] Test passes consistently
- [ ] Behavior matches specification exactly

## Edge Case Testing

Test the edge cases enumerated in Refine:
- Empty/null inputs
- Boundary values
- Invalid inputs
- Timing issues
- Failure scenarios
- Concurrent access

Also test edge cases discovered during Generate.

## Security Review Checklist

- [ ] Input validation (server-side)
- [ ] Parameterized queries (no SQL injection)
- [ ] Authentication on protected endpoints
- [ ] Authorization checks for resources
- [ ] Sensitive data encrypted
- [ ] No secrets in code or logs

## Integration Testing

- [ ] Components communicate correctly
- [ ] Data flows as designed
- [ ] Error handling works across boundaries
- [ ] Performance meets requirements

## Disposition Decisions

| Decision | Meaning | Action |
|----------|---------|--------|
| **Accept** | Meets all criteria | Ship/integrate |
| **Accept with issues** | Works but has minor issues | Document, plan fixes |
| **Revise** | Doesn't meet criteria | Back to Generate |
| **Reject** | Fundamental problems | Back to Orchestrate/Focus |

## When to Revise vs Reject

**Revise** (back to Generate):
- Implementation bug
- Missing edge case handling
- Performance issue fixable in code

**Reject** (back to earlier phase):
- Requirements were wrong
- Architecture doesn't support the feature
- Scope needs to change

## Completion Checklist

- [ ] All criteria verified
- [ ] Edge cases tested
- [ ] Integration tested
- [ ] Security reviewed
- [ ] Disposition decided

## After Evaluate

If **Accept**: Complete the cycle
```bash
uv run forge_cycle.py complete <cycle-id>
```

If **Revise**: Return to Generate with specific feedback

If **Reject**: Return to appropriate earlier phase

Consider running a retrospective:
```bash
uv run forge_learn.py retro
```

## Common Mistakes

- "Looks right" instead of systematic verification
- Skipping edge cases that seem unlikely
- Missing security review
- Not documenting issues found
