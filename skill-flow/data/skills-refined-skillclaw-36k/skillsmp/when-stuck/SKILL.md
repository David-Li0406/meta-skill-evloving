---
name: when-stuck
description: Problem-solving decision tree for when you're blocked. Matches stuck-type to solution strategy.
---

# When Stuck

> **Load this skill** when you've tried something 2+ times and it's not working.

## Diagnosis First

Before trying random fixes, identify your stuck-type:

| Stuck Type | Symptoms | Solution Path |
|------------|----------|---------------|
| **Complexity** | Too many moving parts | Simplify → Isolate → Verify |
| **Understanding** | Don't understand the code | Read → Trace → Ask |
| **Environment** | Works elsewhere, fails here | Compare → Diff → Reset |
| **Edge Case** | Works mostly, fails sometimes | Reproduce → Instrument → Narrow |
| **Integration** | Components work alone, fail together | Mock → Stub → Trace boundaries |

---

## Solution Paths

### 1. Complexity Overwhelm

**Symptoms:** Too many files, unclear flow, can't hold it all in mind

**Solution:**
1. **Simplify**: Remove all optional code, get minimal case
2. **Isolate**: Test ONE component at a time
3. **Verify**: Confirm each piece works before combining
4. **Rebuild**: Add back complexity piece by piece

```
# Strategy: Divide and conquer
1. Comment out everything except the core
2. Verify core works
3. Uncomment one feature at a time
4. Find the breaking feature
5. Fix it in isolation
```

---

### 2. Understanding Gap

**Symptoms:** Don't know what the code does, unclear interfaces

**Solution:**
1. **Read**: Read the actual code, not just descriptions
2. **Trace**: Follow a single request through the system
3. **Log**: Add console.log at every step
4. **Ask**: Delegate to `oracle` for architecture explanation

```
# Strategy: Follow the data
1. Find the entry point
2. console.log("Step 1:", data)
3. Follow each transformation
4. Map the flow on paper
```

---

### 3. Environment Mismatch

**Symptoms:** "Works on my machine", CI fails, dependencies differ

**Solution:**
1. **Compare**: What's different between environments?
2. **Diff**: Check versions, configs, env vars
3. **Reset**: Clean install, fresh clone
4. **Reproduce**: Match the failing environment exactly

```bash
# Strategy: Clean slate
rm -rf node_modules .next dist
bun install
bun run build
```

---

### 4. Edge Case Failure

**Symptoms:** Works 90% of the time, random failures

**Solution:**
1. **Reproduce**: Find the exact conditions that fail
2. **Instrument**: Add detailed logging around failure
3. **Narrow**: Binary search to find the trigger
4. **Fix**: Handle the edge case explicitly

```
# Strategy: Binary search
1. Does it fail with input A? Yes
2. Does it fail with half of A? No
3. Does it fail with 75% of A? Yes
4. ... narrow down to exact failing element
```

---

### 5. Integration Failure

**Symptoms:** Unit tests pass, integration fails

**Solution:**
1. **Mock**: Replace real dependencies with mocks
2. **Stub**: Return known values at boundaries
3. **Trace**: Log at every integration point
4. **Contract**: Verify interfaces match expectations

```
# Strategy: Boundary inspection
1. Log inputs at each service boundary
2. Compare expected vs actual formats
3. Find the mismatch
4. Fix the contract violation
```

---

## Escalation Path

If still stuck after following the appropriate path:

1. **30 min stuck** → Try a different approach entirely
2. **1 hour stuck** → Delegate to `oracle` agent for consultation
3. **2+ hours stuck** → Ask user for guidance or context

---

## Anti-Patterns

| Don't Do This | Do This Instead |
|---------------|-----------------|
| Random changes hoping something works | Systematic isolation |
| Reading more docs without testing | Test first, docs to explain |
| Asking for help immediately | 15 min genuine attempt first |
| Blaming the framework/library | Verify your usage is correct |
| Starting over from scratch | Identify what specifically broke |

---

## Quick Unstick Commands

```bash
# Clean rebuild
rm -rf node_modules dist .next && bun install && bun run build

# Find recent changes
git diff HEAD~5

# Check for type errors
bun run typecheck

# Run specific failing test with verbose
bun test --verbose path/to/failing.test.ts

# Trace function calls
console.log(new Error().stack)
```

---

## Remember

**Being stuck is data.** It tells you:
- Your mental model doesn't match reality
- There's something you don't know yet
- The approach needs adjustment

Stop. Diagnose. Choose the right path. Execute systematically.
