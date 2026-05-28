---
name: problem-solving
description: Root cause analysis instead of workarounds. Use when debugging fails after 2-3 attempts, when adding sleep/retry hacks, or when same fix "almost works". Stops wasteful iteration and finds real solutions.
---

# Problem-Solving: Root Cause Analysis

## When This Skill Activates

Use this methodology when:
- Third attempt at fixing something doesn't work
- Adding sleep, retry, or delay hacks
- Solution "partially works" or "works sometimes"
- Same problem keeps coming back
- User says "stop adding workarounds" or similar

## The Anti-Pattern: Workaround Loop

```
Problem → Quick fix → Doesn't work → Add delay → Doesn't work →
Add more code → Partially works → Add hack → Breaks something else → ...
```

**STOP when you recognize this pattern.**

## The Framework

### Phase 1: STOP

When third attempt fails, **stop coding immediately**.

Ask yourself:
- Do I understand WHY it doesn't work?
- Am I adding code to SOLVE or to BYPASS?

If answer is "bypass" → proceed to Phase 2.

### Phase 2: Find the DIFFERENCE

If something works in one context but not another, find the key difference.

**Create a comparison table:**

| Aspect | Working Case | Broken Case |
|--------|--------------|-------------|
| Input data | ? | ? |
| State | ? | ? |
| Environment | ? | ? |
| Timing | ? | ? |

**Key insight:** The difference points to the cause.

### Phase 3: Ask WHY, not HOW

Transform your question:

| BAD (HOW) | GOOD (WHY) |
|-----------|------------|
| "How to make regex work?" | "Why does regex work for '3pm' but not '3 pm'?" |
| "How to fix timeout?" | "Why does API timeout only for certain requests?" |
| "How to prevent re-run?" | "Why does function run twice?" |

### Phase 4: Read the Source

Documentation is often incomplete. Read actual code:

1. **Library code** - How does httpx handle timeouts?
2. **Your code** - What state changes affect behavior?
3. **Integration points** - Where do they interact?

```bash
# Search for relevant patterns
grep -r "async def" src/core/
grep -r "timeout" src/
```

### Phase 5: Hypothesis → Test

Formulate testable hypothesis:

**Template:** "If [X] is the cause, then [Y] should fix it"

**Example:**
- Hypothesis: "If regex doesn't handle optional space, adding `\s*` should fix it"
- Test: Update pattern, run test cases
- Result: Works!

**Important:** Test with MINIMAL change. Don't add new features while testing.

### Phase 6: Remove, Don't Add

**Good solutions usually REMOVE code, not add it.**

| Approach | Code Change | Result |
|----------|-------------|--------|
| Workaround | +50 lines (retries, try-except everywhere) | Fragile |
| Root cause fix | -20 lines (fix the actual pattern) | Robust |

## Quick Checklist

Before adding ANY workaround code, answer:

```
[ ] I understand the ROOT CAUSE
[ ] I compared working vs broken cases
[ ] I read relevant source code
[ ] My fix REMOVES complexity (or adds minimal)
[ ] I can explain WHY this fixes it (not just THAT it works)
```

## Python-Specific Patterns

### Async Issues

When async code behaves unexpectedly:

```python
# BAD: Adding arbitrary sleep
await asyncio.sleep(0.1)  # "makes it work"

# GOOD: Understand the race condition
# Why does order matter? What's being awaited?
```

### Regex Issues

When regex "partially works":

```python
# BAD: Adding more patterns
patterns = [r"\d+pm", r"\d+ pm", r"\d+\s*pm", ...]  # Growing list

# GOOD: One robust pattern
pattern = r"\d+\s*(?:am|pm)"  # Handles all spacing
```

## Signs You're On the Right Track

- Solution is SIMPLER than the problem seemed
- You can explain it in one sentence
- Code got shorter, not longer
- No "magic numbers" (arbitrary delays, retries)
- Works consistently, not "most of the time"
