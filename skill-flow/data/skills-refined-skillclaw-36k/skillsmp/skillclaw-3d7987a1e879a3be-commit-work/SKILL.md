---
name: commit-work
description: Use this skill when you need to create high-quality git commits by reviewing and staging intended changes, splitting them into logical commits, and writing clear commit messages.
---

# Commit work

## Goal
Make commits that are easy to review and safe to ship:
- Only intended changes are included.
- Commits are logically scoped (split when needed).
- Commit messages describe what changed and why.

## Inputs to ask for (if missing)
- Single commit or multiple commits? (If unsure: default to multiple small commits when there are unrelated changes.)
- Commit style: Conventional Commits are required.
- Any rules: max subject length, required scopes.

## Workflow (checklist)
1. Inspect the working tree before staging:
   - `git status`
   - `git diff` (unstaged)
   - If many changes: `git diff --stat`
2. Decide commit boundaries (split if needed):
   - Split by: feature vs refactor, backend vs frontend, formatting vs logic, tests vs prod code, dependency bumps vs behavior changes.
   - If changes are mixed in one file, plan to use patch staging.
3. Stage only what belongs in the next commit:
   - Prefer patch staging for mixed changes: `git add -p`
   - To unstage a hunk/file: `git restore --staged -p` or `git restore --staged <path>`
4. Review what will actually be committed:
   - `git diff --cached`
   - Sanity checks:
     - No secrets or tokens.
     - No accidental debug logging.
     - No unrelated formatting churn.
5. Describe the staged change in 1-2 sentences (before writing the message):
   - "What changed?" + "Why?"
   - If you cannot describe it cleanly, the commit is probably too big or mixed; go back to step 2.
6. Write the commit message:
   - Use Conventional Commits (required):
     - `type(scope): short summary`
     - Blank line
     - Body (what/why, not implementation diary)
     - Footer (BREAKING CHANGE) if needed
   - Prefer an editor for multi-line messages: `git commit -v`
   - Use a commit message template if helpful.
7. Run the smallest relevant verification:
   - Run the repo's fastest meaningful check (unit tests, lint, or build) before moving on.
8. Repeat for the next commit until the working tree is clean.

## Deliverable
Provide:
- The final commit message(s).
- A short summary per commit (what/why).
- The commands used to stage/review (at minimum: `git diff --cached`, plus any tests run).