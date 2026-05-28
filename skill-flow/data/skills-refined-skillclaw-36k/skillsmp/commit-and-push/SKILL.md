---
name: commit-and-push
description: Commit staged changes and push to the remote using conventional commits with GPG signing. Use when you need to commit and push work, create a PR if missing, and wait for Gemini review before addressing feedback.
---

# Commit and Push

Commit staged changes, push the branch, create a PR if needed, and handle initial Gemini review.

## Setup

Determine the repository for all `gh` commands:

```bash
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
```

Always pass `-R "$REPO"` to `gh` commands.

## Workflow

1. Check branch:
   - If on `main`, create a new branch named for the change.
   - After creating/switching, update the VS Code title:

   ```bash
   setVscodeTitle.sh
   ```

2. Analyze changes:
   - Run `git status` and `git diff --staged` to confirm what will be committed.
   - If tooling reports actions but `git status` shows no unexpected changes, proceed without asking about generated files.

3. Commit format:
   - Follow `CLAUDE.md` commit guidelines (conventional commits, GPG signed with 5s timeout, no co-author lines, no footers).
   - Do not bump versions here.

4. Push:
   - Push the current branch to the remote after the commit.
   - The pre-push hook runs full builds and tests; set a long timeout and do not assume timeouts mean failure.

5. Open PR:
   - If no PR exists, create one with `gh pr create`.
   - Do not include auto-close keywords (`Closes`, `Fixes`, `Resolves`).
   - Use the Claude-style PR body format and include the evaluated agent id.

   Compute the agent id:

   ```bash
   AGENT_ID=$(basename "$(git rev-parse --show-toplevel)")
   ```

   PR body template (fill in real bullets, keep section order):

   ```bash
   PR_BODY=$(cat <<EOF
   ## Summary
   - <verb-led, concrete change>
   - <second concrete change if needed>

   ## Testing
   - <command run or "not run (reason)">

   ## Issue
   - #<issue-number>

   Agent: ${AGENT_ID}
   EOF
   )
   ```

   If there is no associated issue, replace the `## Issue` section with:

   ```text
   ## Related
   - <link or short reference>
   ```

   - After creating the PR, run `setVscodeTitle.sh`.

6. Wait for Gemini:
   - Wait 60 seconds for Gemini Code Assist to review.

7. Address feedback:
   - Run `/address-gemini-feedback` for unresolved comments.
   - Reply to Gemini using the REST API comment reply endpoint, not `gh pr review`.
   - Always include `@gemini-code-assist` in replies.

## Token Efficiency

Suppress stdout on git commit and push:

```bash
git commit -S -m "message" >/dev/null
git push >/dev/null
```

Do not run `git commit` or `git push` without stdout suppression.
