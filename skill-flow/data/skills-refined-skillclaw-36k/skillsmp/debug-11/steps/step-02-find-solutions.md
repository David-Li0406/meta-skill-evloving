---
name: step-02-find-solutions
description: Research and identify potential solutions to the error
prev_step: steps/step-01-analyze.md
next_step: steps/step-03-propose.md
---

# Step 2: Find Solutions

## MANDATORY EXECUTION RULES (READ FIRST):

- 🛑 NEVER implement solutions in this step
- ✅ ALWAYS find at least 2-3 potential solutions
- 📋 YOU ARE A RESEARCHER, not an implementer
- 💬 FOCUS on identifying options only
- 🚫 FORBIDDEN to modify any files

## EXECUTION PROTOCOLS:

- 🎯 Research thoroughly before listing solutions
- 💾 Document each solution with pros/cons in `{solutions}`
- 📖 Complete solution research before loading next step
- 🚫 FORBIDDEN to load step-03 until multiple solutions identified

## CONTEXT BOUNDARIES:

- Variables from previous steps: `{error_context}`, `{auto_mode}`, `{error_analysis}`
- Use analysis to guide solution research
- Don't assume one solution is best yet

## YOUR TASK:

Research and identify multiple potential solutions to the error, documenting trade-offs for each.

---

## Available State

From previous steps:

| Variable           | Description                                          |
| ------------------ | ---------------------------------------------------- |
| `{error_context}`  | Original error description                           |
| `{auto_mode}`      | Skip confirmations flag                              |
| `{error_analysis}` | Analysis from step 1 with root cause, affected files |

---

## EXECUTION SEQUENCE:

### 1. Review Analysis

**Load from `{error_analysis}`:**

- Root cause identified
- Affected files list
- Error complexity

### 2. Research Solutions

**For each potential fix approach:**

**Search codebase for patterns:**

- How are similar issues handled elsewhere?
- Are there existing utilities or helpers to use?
- What patterns does the codebase follow?

**Consider solution types:**

1. **Quick fix** - Minimal change to resolve immediate issue
2. **Proper fix** - Address root cause properly
3. **Refactor fix** - Improve architecture while fixing

### 3. Document Solutions

**For each solution found (minimum 2, ideally 3-4), document:**

#### Solution 1: _Name_

| Field               | Value                     |
| ------------------- | ------------------------- |
| **Approach**        | _What this solution does_ |
| **Files to modify** | _file1, file2, ..._       |
| **Effort**          | Low / Medium / High       |
| **Risk**            | Low / Medium / High       |
| **Recommended?**    | Yes / No                  |

**Pros:**

- Advantage 1
- Advantage 2

**Cons:**

- Disadvantage 1

_(Repeat for each solution)_

### 4. Rank Solutions

**Determine recommendation based on:**

- Balance of effort vs. completeness
- Risk of introducing new bugs
- Alignment with codebase patterns
- Long-term maintainability

**Mark ONE solution as recommended**

### 5. Proceed to Proposal

→ Proceed directly to step-03 (no confirmation needed)

---

## SUCCESS METRICS:

✅ At least 2 distinct solutions identified
✅ Each solution has pros/cons documented
✅ Effort and risk assessed for each
✅ One solution marked as recommended
✅ `{solutions}` state variable populated

## FAILURE MODES:

❌ Only finding one solution
❌ Missing pros/cons analysis
❌ Not identifying affected files for each solution
❌ **CRITICAL**: Implementing any solution in this step

## RESEARCH PROTOCOLS:

- Check how similar code handles edge cases
- Look for tests that might guide the solution
- Consider backwards compatibility
- Don't overlook simple solutions

---

## NEXT STEP:

After solutions documented, load `./step-03-propose.md`

<critical>
Remember: This step is ONLY about finding options - don't implement or choose yet!
</critical>
