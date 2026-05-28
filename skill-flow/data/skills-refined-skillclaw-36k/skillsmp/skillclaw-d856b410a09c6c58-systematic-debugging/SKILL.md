---
name: systematic-debugging
description: Use this skill when you need to systematically identify and resolve complex bugs, intermittent failures, or perform root cause analysis.
---

# Systematic Debugging

This skill provides a structured approach to debugging, helping you identify the root cause of complex issues through a systematic five-step process.

## 🎯 When to Use

**Use this skill when**:
- You encounter vague or unclear error messages.
- The problem is intermittent or difficult to reproduce.
- Multiple attempts to resolve the issue have failed.
- You need to conduct a deep analysis to identify the root cause.

**Do not use this skill when**:
- There is a clear error message that can be quickly diagnosed.
- The issue can be resolved through rapid troubleshooting techniques.

## Debugging Process

1. **Define the Problem**
   - Clearly describe the issue, removing vague statements.
   - Use the following template:
     ```
     - What action: ___________
     - Expected result: ___________
     - Actual result: ___________
     - Frequency: Always / Intermittent (___%) / Difficult to reproduce
     - Environment: OS/version/dependencies
     ```

2. **Isolate the Scope**
   - Narrow down the problem area to reduce variables.
   - Use methods like binary search or control variables to identify where the issue lies.

3. **List Hypotheses**
   - Generate a list of possible causes, ordered by probability.
   - Example hypothesis table:
     ```
     | Hypothesis      | Probability | Verification Method | Status     |
     |-----------------|-------------|---------------------|------------|
     | Network timeout  | High        | Check network logs   | Unverified |
     | Memory leak      | Medium      | Check memory usage   | Unverified |
     | Race condition    | Low         | Test with locks      | Unverified |
     ```

4. **Validate Hypotheses**
   - Design experiments to confirm or eliminate hypotheses.
   - Ensure each experiment tests only one hypothesis at a time.

5. **Confirm Root Cause**
   - Once the root cause is identified, implement a fix and verify that the issue is resolved.

## Common Checkpoints
- Ensure the problem has been reproduced with minimal input.
- Verify key hypotheses before proceeding with fixes.
- Conduct regression testing after applying fixes to confirm resolution.

## Tools and Techniques
- Use logging tools to track key paths and states.
- For database issues, utilize query analysis tools to check for performance bottlenecks.
- In frontend applications, leverage UI hints to display critical states instead of relying solely on console logs.

## Checklist
- [ ] Problem has been reproduced and minimized.
- [ ] Key hypotheses have been validated.
- [ ] Regression testing has been completed successfully.