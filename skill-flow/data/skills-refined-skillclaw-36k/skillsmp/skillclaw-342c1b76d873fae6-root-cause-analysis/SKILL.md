---
name: root-cause-analysis
description: Use this skill when diagnosing failures, investigating incidents, or determining the root cause of issues to prevent recurrence.
---

# Skill body

## Steps for Root Cause Analysis

1. **Identify Symptoms**
   - Document the exact manifestation of the problem.

2. **Gather Context**
   - Answer core questions:
     - When did the issue start?
     - Can it be reproduced consistently?
     - What recent changes occurred (deployments, configurations, etc.)?
     - What previous attempts have been made to fix it?
     - What constraints exist (time, resources)?

3. **Assess Confidence Levels**
   - Use the following thresholds to determine the next steps:
     - **0-2**: Symptom unclear or can't reproduce - continue gathering information.
     - **3**: Good context, some gaps - begin hypothesis formation.
     - **4+**: Clear picture - proceed to investigation.

4. **Formulate Hypotheses**
   - Create 2-4 competing theories based on gathered evidence.
   - Ensure hypotheses are:
     - Testable
     - Falsifiable
     - Specific
     - Plausible

5. **Gather Evidence**
   - Collect observations in the following categories:
     - **Error Manifestation**: Symptoms, messages, states.
     - **Reproduction Steps**: Minimal sequence to trigger the issue.
     - **System State**: Logs, variables, configuration at failure time.
     - **Environment**: Versions, platform, dependencies.
     - **Timing**: Document when the issue started.

6. **Eliminate Hypotheses**
   - Test each hypothesis against the evidence collected.
   - Eliminate those that do not hold up under scrutiny.

7. **Identify Root Cause**
   - Determine the verified root cause based on the remaining hypotheses.

8. **Implement Fix**
   - Develop and apply a solution to address the root cause.

9. **Prevent Recurrence**
   - Document findings and solutions to prevent similar issues in the future.

## When to Use
- Diagnosing system failures or unexpected behavior.
- Investigating incidents or outages.
- Finding the actual cause versus surface symptoms.
- Any situation where "why did this happen?" needs answering.

## Not for
- Known issues with documented fixes.
- Simple configuration errors.
- Guessing without evidence.