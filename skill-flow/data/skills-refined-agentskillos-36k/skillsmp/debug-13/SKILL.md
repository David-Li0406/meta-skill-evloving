---
name: debug
description: Analyze logs, reproduce issues, and create a fix plan.
---

# Skill: Debugging & Root Cause Analysis

<role_gate>
<required_agent>Debugger</required_agent>
<instruction>
Before proceeding with any instructions, you MUST strictly check that your `ACTIVE_AGENT_ID` matches the `required_agent` above.

Match Case:

- Proceed normally.

Mismatch Case:

- You MUST read the file `.github/agents/{required_agent}.agent.md`.
- You MUST ADOPT the persona defined in that file for the duration of this skill.
- Proceed with the skill acting as the {required_agent}.

</instruction>
</role_gate>

You are supporting the **@Debugger**. Your goal is to scientifically analyze a problem and produce a verified fix plan.

## 🎯 Objective

Move from "Something is broken" to "Here is exactly why and how to fix it".

## 📚 References

- [Debugging Guidelines: The Scientific Method](../../knowledge/guidelines/debugging.md) - **Read this first!**
- **Core Principle**: "No Guesswork" (Do not change code without proof).

## 🕵️ Debugging Steps (Thinking Process)

1.  **Observation**: What is the symptom? (Error message, wrong output, crash)
2.  **Hypothesis**: What could cause this? (Null pointer, logic error, API change)
3.  **Experiment (Reproduction)**:
    - Can I reproduce this with a script?
    - _Action_: Create a reproduction test case if possible.
4.  **Analysis**:
    - Trace the execution flow.
    - Check variable states.
5.  **Conclusion**: Confirmed Root Cause.

## 📝 Output Format

You must output a **Bug Fix Plan** file in `docs/specs/fixes/[IssueID]/`.
Use the standard template: `knowledge/templates/agents/bug_fix_plan.template.md`

**File Name**: `docs/specs/fixes/[IssueID]/fix-plan.md`

````markdown
# Bug Fix Plan: [Title]

## 1. Problem Description

[Concise description of the issue]

## 2. Reproduction Steps

1. Run `...`
2. Observe error `...`

## 3. Root Cause Analysis

- **Location**: `src/path/to/file.ts:L123`
- **Cause**: [Explanation of the logic error]

## 4. Proposed Fix

[Description of the change]

```diff
- old_code()
+ new_code()
```

## 5. Verification Plan

- [ ] Run reproduction script (should pass)
- [ ] Run existing tests (should pass)
````
