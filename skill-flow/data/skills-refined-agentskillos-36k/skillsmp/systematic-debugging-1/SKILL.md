---
name: systematic-debugging
description: 4-phase debugging framework preventing "guess-and-check" fixing. Load when debugging fails or for complex bug investigation.
---

# Systematic Debugging

> **THE IRON LAW:** NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

## When to Activate

- Bug fix attempt has failed 2+ times
- Error message is cryptic or misleading
- Issue spans multiple components
- User explicitly requests thorough debugging

---

## Phase 1: Reproduce Consistently

**Goal:** Trigger the bug reliably before any investigation.

```
1. Create minimal reproduction case
2. Document exact steps to trigger
3. Note: Does it happen 100% or intermittently?
4. If intermittent → add logging to catch it
```

**STOP if you cannot reproduce.** Never guess at bugs you can't see.

---

## Phase 2: Isolate the Failure Point

**Goal:** Find EXACTLY where bad data or behavior originates.

### Backward Tracing Technique

1. Start at the error (where symptom appears)
2. Trace data backward through the call stack
3. At each layer, verify: Is the data correct here?
4. Continue until you find where good data becomes bad

```typescript
// Add instrumentation at boundaries
console.log('[Layer 1] Input:', JSON.stringify(data))
// ... processing ...
console.log('[Layer 1] Output:', JSON.stringify(result))
```

### Multi-Component Investigation

For issues spanning services/modules:

| Tool | Use For |
|------|---------|
| `grep` | Find all usages of the variable/function |
| `lsp_find_references` | Trace call hierarchy |
| `git log -S "pattern"` | Find when code was introduced |
| `git blame` | Who changed this and why |

---

## Phase 3: Single Hypothesis Testing

**Goal:** Form ONE specific theory, test minimally.

### The Scientific Method

1. **Hypothesis:** "The bug occurs because X"
2. **Prediction:** "If I change Y, behavior should become Z"
3. **Test:** Make the minimal change to test prediction
4. **Verify:** Does the prediction hold?

```
✅ GOOD: "The empty string comes from line 42 where we default to ''"
❌ BAD: "Maybe it's a caching issue? Let me try clearing the cache..."
```

### The 3-Fix Rule

> If 3+ fix attempts fail, STOP and question fundamental assumptions.

- Is the bug where you think it is?
- Are you fixing the symptom or root cause?
- Do you fully understand the system?

Consider escalating: `task(agent="oracle", prompt="Debug analysis...")`

---

## Phase 4: Verify the Fix

**Goal:** Confirm the fix works and doesn't break other things.

### Required Evidence

- [ ] **Reproduction Test:** Original bug no longer triggers
- [ ] **Regression Test:** Add test case that would catch this bug
- [ ] **Side Effects:** Run existing tests, check related functionality
- [ ] **Type Safety:** `lsp_diagnostics` clean on changed files

```bash
# Run tests on affected areas
bun test src/affected-module/
```

---

## Anti-Patterns (NEVER DO THESE)

| Anti-Pattern | Why It's Wrong |
|--------------|----------------|
| "Quick fix for now, investigate later" | Later never comes; tech debt compounds |
| "Just try changing X and see if it works" | Guess-and-check wastes time, hides root cause |
| "It works on my machine" | Environment differences ARE the bug |
| Fixing where error appears | Symptom ≠ Cause; trace backward |
| Multiple changes at once | Can't isolate which change fixed it |
| Deleting failing tests | Hiding the problem, not fixing it |

---

## Defense in Depth (Prevention)

After fixing, consider adding guards to prevent recurrence:

```typescript
// Layer 1: Parse at boundary
const validatedInput = parseInput(rawInput) // throws if invalid

// Layer 2: Runtime assertion
assert(value !== undefined, 'Value should never be undefined here')

// Layer 3: Type narrowing
if (!isValidState(state)) {
  throw new Error(`Invalid state: ${JSON.stringify(state)}`)
}
```

---

## Debugging Checklist

Before claiming "fixed":

- [ ] Can reproduce the original bug? (Phase 1)
- [ ] Know the exact line where bad data originates? (Phase 2)
- [ ] Single hypothesis tested and confirmed? (Phase 3)
- [ ] Regression test added? (Phase 4)
- [ ] All existing tests pass? (Phase 4)
- [ ] `lsp_diagnostics` clean? (Phase 4)
