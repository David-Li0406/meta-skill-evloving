---
name: step-01-analyze
description: Analyze the error in depth to understand root cause
prev_step: steps/step-00-init.md
next_step: steps/step-02-find-solutions.md
---

# Step 1: Analyze the Error

## MANDATORY EXECUTION RULES (READ FIRST):

- 🛑 NEVER propose solutions in this step
- ✅ ALWAYS gather complete error context before concluding
- 📋 YOU ARE AN INVESTIGATOR, not a fixer
- 💬 FOCUS on understanding the problem only
- 🚫 FORBIDDEN to make code changes

## EXECUTION PROTOCOLS:

- 🎯 Show your analysis reasoning before conclusions
- 💾 Document all findings in `{error_analysis}`
- 📖 Complete investigation before loading next step
- 🚫 FORBIDDEN to load step-02 until analysis is thorough

## CONTEXT BOUNDARIES:

- Variables from step-00: `{error_context}`, `{auto_mode}`
- Don't assume solutions exist yet
- Focus purely on understanding what's wrong

## YOUR TASK:

Investigate the error thoroughly to understand its root cause, affected files, and scope of impact.

---

## EXECUTION SEQUENCE:

### 1. Gather Error Information

**Read the COMPLETE error message first** - don't skim!

- Parse the exact error message and type
- Identify file paths and line numbers from stack trace
- Note any error codes, exit codes, or status

**If no specific error:**

- Ask user to describe exact symptoms
- Check `git status` and `git log --oneline -10` for recent changes
- Look for obvious issues in mentioned files

### 2. Reproduce the Error (CRITICAL)

<critical>
If you cannot reproduce consistently, you cannot verify a fix. This is non-negotiable.
</critical>

**Attempt reproduction:**

- Run the exact command/action that triggers the error
- Document the minimal steps to reproduce
- Note any conditions (environment, data, timing)

**If cannot reproduce:**

- Escalate instrumentation (add targeted logging)
- Check for Heisenbug indicators (timing-sensitive, race condition)
- Ask user for more context about when it occurs

### 3. Form Hypotheses (Ranked)

**List 3-5 possible causes in order of likelihood:**

| Rank        | Hypothesis                | Evidence             | How to Test              |
| ----------- | ------------------------- | -------------------- | ------------------------ |
| Most Likely | _What you think is wrong_ | _What supports this_ | _How to verify/disprove_ |
| Likely      | ...                       | ...                  | ...                      |
| Possible    | ...                       | ...                  | ...                      |

**Test hypotheses systematically** - don't jump to the first idea!

### 4. Investigate the Codebase

**Search for relevant code:**

- Use Grep to find related patterns
- Read files mentioned in error COMPLETELY
- Check imports and dependencies
- Look for similar patterns that work elsewhere

**Build context:**

- What function/component is failing?
- What data flows through this code?
- Check git blame: who changed this recently and why?

### 5. Identify Root Cause

**Validate against hypotheses:**

- Which hypothesis is confirmed/rejected by evidence?
- What is the immediate cause vs. deeper underlying issue?
- Are there related problems?

**Document your analysis with:**

| Field               | Value                          |
| ------------------- | ------------------------------ |
| Error Type          | _Type of error_                |
| Error Message       | _Exact error message_          |
| Reproducible?       | Yes / No                       |
| Reproduction Steps  | _Minimal steps to trigger_     |
| Root Cause          | _What's actually causing this_ |
| Affected Files      | _List of files involved_       |
| Scope               | Localized / Widespread         |
| Complexity          | Simple / Moderate / Complex    |
| Verification Method | _How to verify the fix works_  |

**Hypotheses tested:**

| Hypothesis         | Result               |
| ------------------ | -------------------- |
| _What you thought_ | Confirmed / Rejected |
| ...                | ...                  |

### 6. Ask for Additional Context

**If `{auto_mode}` = true:**
→ Proceed to step-02 automatically

**If `{auto_mode}` = false:**

Present analysis summary, then use **AskUserQuestion** with:

- **Header:** "Context"
- **Question:** "Do you have additional information that could help with the analysis?"
- **Options:**
  1. "No, continue (Recommended)" → Analysis is sufficient, proceed to find solutions
  2. "Yes, I have more info" → Let me provide additional context

**Handle responses:**

- **"No, continue":** Load step-02
- **"Yes, I have more info":** Wait for user input, update `{error_analysis}`, then proceed to step-02

---

## SUCCESS METRICS:

✅ Error reproduced (or documented why it can't be)
✅ 3+ hypotheses formed and tested systematically
✅ Root cause clearly identified with evidence
✅ Affected files documented
✅ Verification method identified for later
✅ `{error_analysis}` state variable populated

## FAILURE MODES:

❌ Jumping to solutions without thorough analysis
❌ Skipping reproduction attempt
❌ Testing only one hypothesis (tunnel vision)
❌ Missing key files or dependencies in investigation
❌ **CRITICAL**: Making code changes in this step

## ANALYSIS PROTOCOLS:

- Read actual error messages, don't assume
- Check git history for recent changes that might have caused this
- Look at test files to understand expected behavior
- Don't skip investigating even if solution seems obvious

---

## NEXT STEP:

After analysis confirmed, load `./step-02-find-solutions.md`

<critical>
Remember: This step is ONLY about analysis - don't fix or propose solutions yet!
</critical>
