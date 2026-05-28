---
name: writing-and-ideation
description: Use this skill when beginning any creative work, including writing new chapters, constructing theoretical frameworks, or modifying argument logic, ensuring a structured approach to ideation and writing.
---

# Writing and Ideation Workflow

## Overview

This skill combines the processes of ideation and writing, allowing for the systematic development of arguments and the creation of isolated writing environments. It emphasizes the importance of verifying claims and structuring arguments before drafting.

## Ideation Process

### Understanding Research Intent

1. **Check Current Project Status**: Review existing drafts, notes, and recent modifications.
2. **Refine Core Arguments**: Ask targeted questions to clarify the research purpose, constraints, and criteria for successful arguments.
3. **Explore Argument Paths**: Propose 2-3 different theoretical perspectives, analyzing their pros and cons.
4. **Document Argument Design**: Write the validated argument design into `docs/plans/YYYY-MM-DD-<topic>-design.md`.

### Key Principles

- **One Question at a Time**: Avoid overwhelming the researcher with multiple questions.
- **Prefer Multiple Choice Questions**: They are easier to answer than open-ended questions.
- **YAGNI (You Aren't Gonna Need It)**: Remove unnecessary arguments and off-topic content.
- **Incremental Validation**: Present the outline in segments and verify logic after each part.

## Writing Process

### Argument-Driven Writing (ADW)

1. **Claim**: Write an unsupported claim that you intend to argue.
   - **Good Example**: "This section will argue that Algorithm A outperforms Algorithm B in handling sparse data."
   - **Bad Example**: "Write about Algorithm A."
   
2. **Verify Claim**: Confirm that there is no supporting evidence in the current draft.
3. **Evidence**: Write the simplest paragraph to support the claim.
   - **Good Example**: "According to the results in Table 3, Algorithm A converges 15% faster than Algorithm B on a 90% sparse dataset."
   - **Bad Example**: "Algorithm A is a great algorithm introduced by Smith et al. in 2020."
   
4. **Verify Evidence**: Ensure the claim is now supported and logically coherent.
5. **Refine**: Optimize wording and clarity only after verification.

### Creating an Isolated Writing Environment

1. **Declare Intent**: Start by stating, "I am using the writing and ideation skill to set up an isolated writing workspace."
2. **Directory Selection**: Check for existing directories and prioritize them.
3. **Security Verification**: Ensure the directory is not ignored by Git before creating a worktree.
4. **Create Worktree**: Use `git worktree add` to create a new branch for writing.
5. **Run Project Setup**: Automatically detect and run appropriate setup for the writing environment (e.g., LaTeX or Markdown).
6. **Baseline Verification**: Run validation scripts to ensure a clean starting state.

## Example Workflow

```
You: I am using the writing and ideation skill to set up an isolated writing workspace.

[Check .worktrees/ - exists]
[Verify ignored - git check-ignore confirms .worktrees/ is ignored]
[Create worktree: git worktree add .worktrees/chapter2 -b draft/chapter2]
[Run baseline check - passed]

Draft workspace ready at /Users/researcher/thesis/.worktrees/chapter2
Baseline check passed
Ready to write Chapter 2
```

## Common Pitfalls

- **Skipping Verification**: Always verify claims and evidence to avoid logical errors.
- **Assuming Directory Locations**: Follow the established priority for directory selection.
- **Continuing After Verification Failure**: Always report failures and seek permission to proceed.

## Integration

- **Callers**: This skill is essential during the ideation phase and when transitioning to writing.
- **Pairing**: Works in conjunction with skills focused on finalization and execution of writing tasks.