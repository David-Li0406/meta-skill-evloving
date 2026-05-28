# Bug Fixing

Investigating and fixing bugs, regressions, and unexpected behavior.

## Mental Model

Bug fixing is investigation work. You're a detective, not a repairman.

```
Report: "Login doesn't work"
         ↓
Clarify: What exactly happens? Error message? Blank screen? Wrong redirect?
         ↓
Reproduce: Follow exact steps to see the bug yourself
         ↓
Investigate: Why is this happening? Find the root cause.
         ↓
Fix: Make minimal, targeted changes
         ↓
Verify: Same steps, bug is gone, nothing else broke
```

## Key Principles

### Understand Expected vs. Actual
Before investigating, be crystal clear:
- What should happen?
- What is actually happening?
- When did this start (if known)?

### Reproduce First
You cannot fix what you cannot see.
- Get exact reproduction steps
- Verify you can reproduce the bug
- If you can't reproduce it, you need more information

### No Speculation
Don't guess at the cause.
- Investigate until you find it
- Add logging if needed
- Use debugger if needed
- Trace the code path
- Verify your hypothesis before making changes

### Minimal Fixes
Change only what's necessary.
- Don't refactor surrounding code
- Don't add "improvements"
- Don't fix unrelated issues you notice
- One bug, one fix

### Verify Thoroughly
Confirm the fix works.
- Use the exact same reproduction steps
- Verify the expected behavior now occurs
- Run related tests
- Check for regressions

## Agent Browser CLI Usage

Browser verification is critical for UI bugs.

**Reproducing the bug:**
```bash
agent-browser open http://localhost:3000/buggy-page
# Follow exact reproduction steps
agent-browser click @element
agent-browser fill "[name='field']" "trigger value"
agent-browser screenshot bug-state.png  # Document the bug
```

**Verifying the fix:**
```bash
# Same exact steps should now work
agent-browser open http://localhost:3000/buggy-page
agent-browser click @element
agent-browser fill "[name='field']" "trigger value"
agent-browser screenshot fixed-state.png  # Should show correct behavior
```

## What to Extract from Users

- Exact reproduction steps
- Expected behavior vs. actual behavior
- When it started (recent changes?)
- Environment details (browser, OS, user type)
- Frequency (always, sometimes, specific conditions)
- Error messages or logs
- Impact and urgency
- Related recent changes or deployments

## Red Flags

You're doing it wrong if:
- "Let me just try this and see if it works"
- Making changes without reproducing the bug first
- Can't explain why the fix should work
- Multiple unrelated changes in one fix
- Haven't verified with original reproduction steps
- Saying "I think I found it" instead of "I verified the cause"

## Story Structure for Bug Fixes

Typical bug fix PRD structure:
1. Reproduce the bug - verify reproduction steps work
2. Investigate root cause - find actual cause, not symptom
3. Implement fix - minimal, targeted change
4. Verify fix - reproduction steps now show correct behavior
5. Run related tests - ensure no regressions
6. Document - what was wrong, what fixed it
