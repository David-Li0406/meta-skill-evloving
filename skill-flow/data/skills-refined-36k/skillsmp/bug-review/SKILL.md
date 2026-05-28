---
name: bug-review
description: This skill should be used when the user asks to "find bugs", "check for bugs", "review for errors", "find logical errors", "check for null references", "find edge cases", "check for race conditions", "debug this code", or wants to identify potential bugs in code.
version: 3.1.1
---

# Bug Detection Code Review Skill

Identify logical errors, null reference issues, race conditions, off-by-one errors, and other potential bugs through targeted bug-focused code review.

## When to Use

Use this skill to:
- Hunt for bugs and errors in code
- Check for null reference and undefined values
- Analyze race conditions
- Detect off-by-one errors
- Identify edge cases
- Find type coercion bugs
- Verify async/await correctness

## Process Overview

1. **Determine scope** - Identify code requiring bug review
2. **Gather context** - Collect project type, related tests, and AI instructions
3. **Launch bug agent** - Execute thorough mode, then gaps mode
4. **Validate findings** - Filter theoretical bugs from results
5. **Report results** - Generate output with reproduction conditions

For detailed procedures on steps 1, 2, 4, and 5, see `${CLAUDE_PLUGIN_ROOT}/shared/skill-common-workflow.md`.

---

## Bug-Specific Configuration

### Agent Parameters

- **Agent:** `${CLAUDE_PLUGIN_ROOT}/agents/bug-detection-agent.md`
- **Model:** Opus (for thorough bug detection)
- **Modes:** thorough (first pass), gaps (second pass)

### Bug Categories Checked

**Null/Undefined References (Major to Critical):**
- Accessing properties on potentially null objects
- Missing null checks after database lookups
- Optional chaining gaps
- Nullable type misuse

**Off-by-One Errors (Minor to Major):**
- Array index bounds (`<=` vs `<`)
- Fence post errors in counting
- Pagination calculations
- Loop termination conditions

**Async/Promise Issues (Major to Critical):**
- Unhandled promise rejections
- Race conditions between async operations
- Floating promises (missing await)
- TOCTOU (time-of-check to time-of-use)

**Type Coercion Bugs (Major):**
- Loose equality (`==`) vs strict (`===`)
- String/number confusion
- Truthy/falsy misunderstandings
- Type narrowing gaps

**State Management (Major to Critical):**
- Mutating shared objects
- Stale closure captures
- React state update issues
- Redux action misuse

**Error Handling (Major):**
- Swallowed exceptions
- Wrong error type caught
- Missing error propagation
- Incomplete cleanup in finally

---

## Auto-Validated Patterns

These high-confidence patterns skip validation:

| Pattern | Description |
|---------|-------------|
| `empty_catch_block` | `catch (e) { }` with no handling |
| `missing_await` | async call without await |
| `null_dereference` | Access after optional chain or guard |

---

## Bug Investigation Mode

When investigating a specific bug:
- Ask for reproduction steps or stack trace
- Focus on code paths mentioned in error
- Include related error handling code
- Read recent git commits touching affected files

---

## Bug-Specific False Positives

Do NOT flag:
- Guarded elsewhere (null check happens in caller)
- Framework guarantee (framework ensures non-null)
- Intentional behavior (bug is expected behavior)
- Unreachable conditions (requires impossible state)
- Test-only code (bugs in test helpers less critical)
- Theoretical bugs requiring unrealistic preconditions

---

## Reproduction Conditions

For each bug, describe:

- **Preconditions**: What state must exist?
- **Trigger**: What action causes the bug?
- **Frequency**: How often can this occur?
- **Impact**: What goes wrong?

Example: "When two users simultaneously withdraw from the same account (concurrent requests), and the balance check passes for both before either write completes, the second write overwrites the first, resulting in only one deduction being recorded."

---

## Example Output

See `examples/example-output.md` for a sample showing:
- Race condition with transaction fix
- Null reference with optional chaining fix
- Unhandled promise with try/catch fix

---

## Additional Resources

### Reference Files

For detailed bug patterns:
- **`references/common-bugs.md`** - Null references, race conditions, async issues, type coercion, error handling

### Related Components

- **Agent Definition:** `${CLAUDE_PLUGIN_ROOT}/agents/bug-detection-agent.md`
- **Subagent Type:** `code-review:bug-detection-agent` (for Task tool invocation)
- **Language checks:** `${CLAUDE_PLUGIN_ROOT}/languages/nodejs.md`, `${CLAUDE_PLUGIN_ROOT}/languages/dotnet.md`
- **Common workflow:** `${CLAUDE_PLUGIN_ROOT}/shared/skill-common-workflow.md`
