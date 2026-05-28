---
name: cdd-implementation-review
description: Use this skill when implementing and reviewing decisions to ensure they meet specified requirements.
---

# CDD Implementation and Review

This skill encompasses both the implementation of decisions and the subsequent review of that implementation to ensure compliance with specified requirements.

## CDD Implementation

### Prerequisites

Before starting the implementation, ensure the following tasks are completed in TodoWrite:

1. [ ] Confirm the existence of `cdd.md` and verify `decisionStatus: DECIDED`.
2. [ ] Change `implementationStatus` to `IN_PROGRESS`.
3. [ ] Break down implementation tasks into specific steps.
4. [ ] Build and test the implementation.
5. [ ] Commit changes to Git (including CDD: `$1`).
6. [ ] Change `implementationStatus` to `IN_REVIEW`.
7. [ ] Request a review from the user.

**Important Rules:**
- Do not change `implementationStatus` to `DONE` within this skill; it can only be changed after review approval.

### Your Task

1. **Load and verify decision:**
   - Locate the `cdd.md` file for `$1`.
   - Verify `decisionStatus: DECIDED`. If not, stop with an error: "Cannot implement - decision not finalized".
   - Confirm with the user before starting implementation.

2. **Read the full specification:**
   - Understand the goal, context, selection, and rejections.

3. **Update implementation status:**
   - Change `implementationStatus` to `IN_PROGRESS`.

4. **Execute implementation:**
   - Follow the selection section strictly and respect all constraints.

5. **Track changed files:**
   - Maintain a list of all files created or modified during implementation.

6. **Create commit when implementation is complete:**
   - Use `git status` to see changed files and generate a commit message in the specified format.
   - Confirm with the user before committing.

7. **Update implementation status to IN_REVIEW:**
   - After a successful commit, change `implementationStatus` to `IN_REVIEW`.

8. **Request review:**
   - Inform the user that implementation is complete and suggest running `/cdd-review-implementation $1`.

## Implementation Review

### Your Task

Conduct an implementation review for decision ID: `$1` after the implementation is marked as `IN_REVIEW`.

1. **Read the Decision Document:**
   - Review `CDD/**/*$1*.cdd.md` to understand the goal, selection, rejections, and any review criteria.

2. **Check for Review Criteria Section:**
   - If present, apply the criteria and document findings.

3. **Locate Implementation:**
   - Preferably use Git commit search to find related commits. If necessary, fallback to searching for deprecated code markers.

4. **Conduct the Review:**
   - Verify alignment with decision requirements, code quality, and architectural/security principles.

5. **Generate Review File:**
   - Create a review file at `CDD/.logs/review/$1-{{YYYYMMDD}}-{{sequence}}.md` using the specified structure.

6. **Update cdd.md:**
   - Add the review to the `reviewHistory` in the YAML frontmatter of `cdd.md`.

7. **Present Results and Update Status:**
   - Show the user the review status, key findings, path to the review file, and confirmation of the update to `cdd.md`.

### Important Notes

- Be thorough but concise in your findings.
- Focus on objective assessments and provide actionable feedback.
- Use checkboxes for findings to enhance readability.