# Bug Analysis Reference

## Analysis Criteria

Focus on finding real bugs, not theoretical concerns:

**Logic Errors:**

- Incorrect conditions, off-by-one errors, wrong operators
- Inverted boolean logic, missing negations
- Incorrect loop bounds or termination conditions

**Runtime Errors:**

- Null/undefined access without guards
- Type mismatches and coercion issues
- Uninitialized variables, use before assignment
- Array index out of bounds

**Error Handling:**

- Unhandled exceptions, missing catch blocks
- Silent failures that swallow errors
- Missing error cases in switch/if chains
- Promises without rejection handling

**Race Conditions:**

- Async timing issues, state corruption
- Shared state modifications without synchronization
- Deadlocks and livelocks
- Check-then-act patterns without atomicity

**Resource Leaks:**

- Unclosed file handles, streams, connections
- Memory leaks from retained references
- Connection pool exhaustion
- Event listener accumulation

**Edge Cases:**

- Boundary conditions (empty, max, min values)
- Empty inputs, null collections
- Overflow/underflow scenarios
- Unicode and encoding edge cases

## Severity Guidelines

- **Critical**: Will cause crashes, data loss, or security issues in normal operation
- **High**: Significant functional bugs affecting users under common conditions
- **Medium**: Edge case bugs, minor functional issues, rare conditions
- **Low**: Potential issues, defensive improvements, unlikely scenarios

## Notes

Include in the `notes` field when relevant:

- Steps to reproduce the bug
- Related code paths that may also be affected
- Workarounds currently in place
- Test cases that would catch this bug
