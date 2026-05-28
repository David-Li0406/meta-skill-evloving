---
name: systems-review
description: Review implementation for second-order effects
---

# Systems Review

After implementing, let's review for second-order effects:

## Implementation Summary

1. **What was built?** Brief description.
2. **What changed?** Files modified.
3. **What's the interface?** Input/output contracts.

## Performance Review

Analyze performance implications:

- What's the time complexity?
- What happens at 10x scale?
- Where are potential bottlenecks?
- Are there N+1 query risks?
- Is caching appropriate?

## Security Review

Check for security issues:

- Is input validated?
- Is authorization checked?
- Could this be exploited?
- Is sensitive data protected?
- Are there injection risks?

## Downstream Effects

Consider blast radius:

- What breaks if this fails?
- What systems depend on this?
- Are there race conditions?
- Could this cause cascading failures?

## Test Coverage

Verify testing:

- Is the happy path tested?
- Are error paths tested?
- Are edge cases covered?
- Is the interface contract verified?

## Recommendations

Based on review, provide:

1. **Critical** - Must fix before shipping
2. **High** - Should fix soon
3. **Medium** - Consider improving
4. **Low** - Nice to have

## Sign-off Checklist

- [ ] Decomposition was followed
- [ ] Interfaces are verified
- [ ] Error handling is complete
- [ ] Performance is acceptable
- [ ] Security is reviewed
- [ ] Tests are adequate
