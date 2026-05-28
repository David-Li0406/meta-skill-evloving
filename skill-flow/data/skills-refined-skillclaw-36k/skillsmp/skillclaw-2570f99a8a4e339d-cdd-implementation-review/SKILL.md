---
name: cdd-implementation-review
description: Use this skill when you need to implement and review a decision based on a specified decision ID.
---

# Skill body

## CDD Implementation and Review

This skill encompasses both the implementation of a decision and the subsequent review of that implementation. 

### Implementation Steps

1. **Load and verify decision:**
   - Find the `cdd.md` file for decision **$1**.
   - **CRITICAL**: Verify `decisionStatus: DECIDED`.
   - If not DECIDED, stop with error: "Cannot implement - decision not finalized".
   - **Use AskUserQuestion** to confirm implementation start.

2. **Read the full specification:**
   - Understand the goal, context, selection, and rejections from the decision document.

3. **Update implementation status:**
   - Change `implementationStatus: IN_PROGRESS`.

4. **Execute implementation:**
   - Follow the selection section exactly, respecting all constraints in context.
   - **DO NOT implement anything from rejections**.

5. **Track changed files:**
   - Keep a list of all files created or modified during implementation for the commit message.

6. **Create commit when implementation is complete:**
   - Use Bash to run: `git status` to see changed files.
   - Generate a commit message in the specified format.
   - **Ask user to confirm before committing**.
   - Use `git add` and `git commit` with the generated message.

7. **Update implementation status to IN_REVIEW:**
   - After successful commit, change `implementationStatus: IN_REVIEW`.
   - **DO NOT change to DONE** - wait for review approval.

8. **Request review:**
   - Inform the user that implementation is complete.
   - Suggest running `/cdd-review-implementation $1`.

### Review Steps

1. **Read the Decision Document:**
   - Read `CDD/**/*$1*.cdd.md` to understand the goal, selection, rejections, and review criteria.

2. **Check for Review Criteria Section:**
   - If present, read and apply the criteria specified in that section.

3. **Locate Implementation:**
   - Preferably use Git commit search to find related commits.
   - As a fallback, search for deprecated `@cdd #$1` markers.

4. **Conduct the Review:**
   - Verify decision alignment, code quality, and adherence to architectural and security principles.

5. **Generate Review File:**
   - Document findings in a review report.

### Important Rules

- **NEVER deviate from the decided approach**.
- If issues arise during implementation, STOP and discuss first.
- **DO NOT add `@cdd #$1` comments** - use Git commit messages instead.