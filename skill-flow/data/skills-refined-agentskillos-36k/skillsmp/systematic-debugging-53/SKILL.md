---
name: systematic-debugging
description: Systematic 4-phase debugging process for finding root causes
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: debugging
---

## What I Do

- Guide systematic root cause analysis
- Prevent shotgun debugging (random changes hoping something works)
- Document findings for future reference
- Ensure fixes actually solve the problem

## When to Use Me

Use this skill when:
- Encountering unexpected behavior
- Tests are failing
- Production issues need investigation
- After 2+ failed fix attempts

## The 4-Phase Process

### Phase 1: REPRODUCE

**Goal:** Reliably trigger the bug

```
1. Get exact steps to reproduce
2. Identify the minimal reproduction case
3. Document environment details (OS, versions, config)
4. Create a failing test if possible
```

**Questions to answer:**
- Can you reproduce it consistently?
- What's the minimum setup needed?
- Does it happen in all environments?

### Phase 2: ISOLATE

**Goal:** Narrow down the location

```
1. Binary search through the codebase
2. Add strategic logging/breakpoints
3. Check recent changes (git blame, git bisect)
4. Eliminate possibilities systematically
```

**Techniques:**
- `git bisect` - Find the commit that introduced the bug
- Comment out code sections
- Add assertions to verify assumptions
- Check input/output at each step

### Phase 3: IDENTIFY

**Goal:** Find the root cause (not just symptoms)

```
1. Understand WHY it's happening, not just WHAT
2. Trace the data flow
3. Check assumptions about state
4. Look for edge cases
```

**Common root causes:**
- Incorrect assumptions about input
- Race conditions
- State mutation
- Off-by-one errors
- Null/undefined handling
- Type coercion issues

### Phase 4: FIX & VERIFY

**Goal:** Fix minimally and prove it works

```
1. Write a failing test that reproduces the bug
2. Make the minimal fix
3. Run the test - it must pass
4. Run full test suite - no regressions
5. Document the fix
```

**Rules:**
- Fix ONE thing at a time
- Don't refactor while fixing
- Verify the fix actually solves the reported issue
- Add tests to prevent regression

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Shotgun debugging | Random changes, unclear if fixed | Follow the 4 phases |
| Fixing symptoms | Bug returns later | Find root cause |
| Changing multiple things | Can't tell what fixed it | One change at a time |
| No reproduction test | Bug can return | Always add a test |
| Skipping verification | Fix may be incomplete | Test thoroughly |

## When to Escalate

After 3 failed fix attempts:
1. STOP further changes
2. Document what you've tried
3. Revert to last known working state
4. Ask for help with full context
