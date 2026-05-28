---
name: describe-pr
description: Use this skill when you need to generate a comprehensive pull request description following the repository's standard template.
---

# Skill body

## Steps to follow:

1. **Read the PR description template:**
   - First, check if `thoughts/shared/pr_description.md` exists.
   - If it doesn't exist, inform the user they need to create a PR description template at `thoughts/shared/pr_description.md`.
   - Read the template carefully to understand all sections and requirements.

2. **Identify the PR to describe:**
   - Check if the current branch has an associated PR: `gh pr view --json url,number,title,state 2>/dev/null`.
   - If no PR exists for the current branch, or if on main/master, list open PRs: `gh pr list --limit 10 --json number,title,headRefName,author`.
   - Ask the user which PR they want to describe.

3. **Check for existing description:**
   - Check if `thoughts/shared/prs/{number}_description.md` already exists.
   - If it exists, read it and inform the user you'll be updating it.
   - Consider what has changed since the last description was written.

4. **Gather comprehensive PR information:**
   - Get the full PR diff: `gh pr diff {number}`.
   - If you get an error about no default remote repository, instruct the user to run `gh repo set-default` and select the appropriate repository.
   - Get commit history: `gh pr view {number} --json commits`.
   - Review the base branch: `gh pr view {number} --json baseRefName`.
   - Get PR metadata: `gh pr view {number} --json url,title,number,state`.

5. **Analyze the changes thoroughly:**
   - Read through the entire diff carefully.
   - For context, read any files that are referenced but not shown in the diff.
   - Understand the purpose and impact of each change.
   - Identify user-facing changes vs internal implementation details.
   - Look for breaking changes or migration requirements.

6. **Handle verification requirements:**
   - Look for any checklist items in the "How to verify it" section of the template.
   - For each verification step:
     - If it's a command you can run (like `make check test`, `npm test`, etc.), run it.
     - If it passes, mark the checkbox as checked: `- [x]`.
     - If it fails, keep it unchecked and note what failed: `- [ ]`.