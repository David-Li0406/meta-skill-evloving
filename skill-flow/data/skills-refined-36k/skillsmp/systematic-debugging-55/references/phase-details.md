# Phase Details

Expanded procedures for each debugging phase.

## Phase 1: Root Cause Investigation (Expanded)

### Reading Error Messages

- Don't skip past errors or warnings
- Read stack traces completely
- Note line numbers, file paths, error codes
- Error messages often contain the exact solution

### Reproducing Consistently

- Can it be triggered reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible → gather more data, avoid guessing

### Checking Recent Changes

- What changed that could cause this?
- Git diff, recent commits
- New dependencies, config changes
- Environmental differences

### Gathering Evidence in Multi-Component Systems

When system has multiple components (CI → build → signing, API → service → database):

**BEFORE proposing fixes, add diagnostic instrumentation:**

```bash
# Layer 1: Workflow
echo "=== Secrets available in workflow: ==="
echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

# Layer 2: Build script
echo "=== Env vars in build script: ==="
env | grep IDENTITY || echo "IDENTITY not in environment"

# Layer 3: Signing script
echo "=== Keychain state: ==="
security list-keychains
security find-identity -v

# Layer 4: Actual signing
codesign --sign "$IDENTITY" --verbose=4 "$APP"
```

For each component boundary:

- Log what data enters component
- Log what data exits component
- Verify environment/config propagation
- Check state at each layer

Run once to gather evidence showing WHERE it breaks, THEN investigate.

### Tracing Data Flow

When error is deep in call stack, use **root-cause-tracing** skill:

- Where does bad value originate?
- What called this with bad value?
- Keep tracing up until finding the source
- Fix at source, not at symptom

## Phase 2: Pattern Analysis (Expanded)

### Finding Working Examples

- Locate similar working code in same codebase
- What works that's similar to what's broken?

### Comparing Against References

- If implementing pattern, read reference implementation COMPLETELY
- Don't skim - read every line
- Understand the pattern fully before applying

### Identifying Differences

- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

### Understanding Dependencies

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

## Phase 3: Hypothesis and Testing (Expanded)

### Forming Single Hypothesis

- State clearly: "I think X is the root cause because Y"
- Write it down
- Be specific, not vague

### Testing Minimally

- Make the SMALLEST possible change to test hypothesis
- One variable at a time
- Don't fix multiple things at once

### When Understanding Is Incomplete

- State "I don't understand X"
- Avoid pretending to know
- Ask for help
- Research more

## Phase 4: Implementation (Expanded)

### Creating Failing Test Case

- Simplest possible reproduction
- Automated test if possible
- One-off test script if no framework
- MUST have before fixing
- Use **dev-workflow:test-driven-development** skill

### Implementing Single Fix

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

### Verifying Fix

- Test passes now?
- No other tests broken?
- Issue actually resolved?

**If Fix Doesn't Work:**

- STOP
- Count: How many fixes have been tried?
- If < 3: Return to Phase 1, re-analyze with new information
- If ≥ 3: Question architecture (see below)

## Questioning Architecture (3+ Failed Fixes)

**Pattern indicating architectural problem:**

- Each fix reveals new shared state/coupling/problem in different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**

- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor architecture vs. continue fixing symptoms?

**Discuss before attempting more fixes.**

This is NOT a failed hypothesis - this is a wrong architecture.

## When Process Reveals "No Root Cause"

If systematic investigation reveals issue is truly environmental, timing-dependent, or external:

1. The process is complete
2. Document what was investigated
3. Implement appropriate handling (retry, timeout, error message)
4. Add monitoring/logging for future investigation

**But:** 95% of "no root cause" cases are incomplete investigation.
