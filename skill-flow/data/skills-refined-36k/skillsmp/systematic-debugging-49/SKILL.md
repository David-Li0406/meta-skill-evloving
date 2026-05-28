---
name: systematic-debugging
description: Four-phase debugging methodology for finding and fixing bugs. Use when debugging issues, investigating errors, fixing crashes, or troubleshooting problems.
context: fork
agent: Explore
---

# Systematic Debugging

A structured approach to finding and fixing bugs in any codebase.

## The Four Phases

```
Reproduce → Isolate → Identify → Fix → Verify
```

## Phase 1: Reproduce

**Goal**: Reliably trigger the bug

### Steps

1. **Get the exact symptoms**
   - What error message appears?
   - What behavior is wrong?
   - What behavior is expected?

2. **Find reproduction steps**
   - What inputs trigger it?
   - What state is required?
   - Is it consistent or intermittent?

3. **Create minimal reproduction**
   - Smallest test case that fails
   - Remove unrelated code/data
   - Document exact steps

## Phase 2: Isolate

**Goal**: Narrow down where the bug occurs

### Techniques

#### Binary Search
Cut the problem space in half repeatedly.

#### Add Logging
```
log("Login handler called", email)
log("User found", user.id if user else None)
log("Password check", password_matches)
```

#### Check Recent Changes
```bash
git log --oneline -20
git bisect start
```

## Phase 3: Identify

**Goal**: Find the root cause

### Ask "Why?" Five Times

1. Why does login fail? → Password check returns false
2. Why does password check return false? → Hash comparison doesn't match
3. Why doesn't hash match? → Comparing plain text to hash
4. Why comparing plain to hash? → Password isn't hashed before comparison
5. Why isn't password hashed? → Missing hash call in auth service

## Phase 4: Fix & Verify

**Goal**: Fix the bug and prove it's fixed

1. **Write a test first** - Test that fails without fix
2. **Make the minimal change** - Fix only the bug
3. **Verify reproduction test passes**
4. **Check for regressions** - All existing tests pass

## Debugging Checklist

```markdown
## Bug: [Description]

### Reproduction
- [ ] Can reproduce consistently
- [ ] Have minimal test case

### Isolation
- [ ] Narrowed to specific area
- [ ] Identified failing component

### Identification
- [ ] Found root cause
- [ ] Can explain why it happens

### Fix
- [ ] Test written that catches bug
- [ ] Minimal fix implemented
- [ ] All tests pass
- [ ] No regressions
```
