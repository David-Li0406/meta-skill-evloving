---
name: clean-copy
description: Reimplement the current branch on a new branch with clean, narrative-quality git commit history suitable for reviewer comprehension. Use when you want to clean up messy commit history before opening a PR.
disable-model-invocation: true
---

Reimplement the current branch on a new branch with a clean, narrative-quality
git commit history suitable for reviewer comprehension.

### Steps

1. **Validate the source branch**
   - Ensure the current branch has no merge conflicts, uncommitted changes, or
     other issues.
   - Confirm it is up to date with `main`.
   - Store the current branch name for reference.

2. **Analyze the diff**
   - Study all changes between the current branch and `main`.
   - Form a clear understanding of the final intended state.
   - Note which files changed and the logical groupings of changes.

3. **Create the clean branch**
   - Create a new branch named `{branch_name}-clean` from `main` (not from
     the current branch).
   - This ensures a fresh starting point for clean commits.

4. **Plan the commit storyline**
   - Break the implementation down into a sequence of self-contained steps.
   - Each step should reflect a logical stage of development, as if writing a
     tutorial.
   - Order commits so each builds naturally on the previous.

5. **Reimplement the work**
   - Recreate the changes in the clean branch, committing step by step
     according to your plan.
   - Each commit must:
     - Introduce a single coherent idea.
     - Include a clear commit message and description.
     - Be atomic: tests should pass (when possible) at each commit.

6. **Verify correctness**
   - Confirm that the final state of `{branch_name}-clean` exactly matches the
     final state of the original branch.
   - Run: `git diff {original_branch}..{branch_name}-clean` (should be empty).
   - Use `--no-verify` only when necessary to bypass known issues.

