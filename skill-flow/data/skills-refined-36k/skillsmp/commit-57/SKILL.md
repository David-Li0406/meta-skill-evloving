---
name: commit
description: Create a well-structured git commit with descriptive message and push to GitHub. Automatically detects nested repos and commits to the correct repository.
user-invocable: true
---

# Smart Commit for Nested Repos

This skill handles git commits in a workspace with multiple nested repositories. It detects which repo(s) have changes and commits to the correct one(s).

## Core Principle

**Commit to the repo you're working in, not the parent.** In a nested repo structure, changes should be committed to the repository that owns those files.

## Procedure

### Step 1: Detect Repository Structure

Run this command to find all git repos in the workspace:

```bash
find "e:/Vibe Coding" -name ".git" -type d 2>/dev/null | head -20
```

Or on Windows:

```bash
dir /s /b /ad "e:\Vibe Coding\.git" 2>nul
```

### Step 2: Identify Changed Files

For each potential repo, check for changes:

```bash
cd "<repo-path>" && git status --short
```

### Step 3: Determine Which Repo to Commit

**Decision tree:**

1. **If user specified a folder** → Commit to that folder's repo (or nearest parent repo)

2. **If changes exist in only ONE repo** → Commit to that repo

3. **If changes exist in MULTIPLE repos** → Ask user which to commit:
   - List each repo with its changes
   - Offer options: commit one, commit all, or specify

4. **If the working directory is inside a nested repo** → Default to that repo

### Step 4: Ask Clarifying Questions (If Needed)

Use the AskUserQuestion tool when:

- Multiple repos have changes
- Unclear which repo the user intended
- Changes span both parent and child repos

Example question:
```
I found changes in multiple repositories:

1. **e:\Vibe Coding** (root) - 3 files changed
2. **e:\Vibe Coding\CoffeeCup** - 1 file changed
3. **e:\Vibe Coding\Consulting** - 2 files changed

Which would you like to commit?
- [ ] Root repo only
- [ ] CoffeeCup only
- [ ] Consulting only
- [ ] All repos separately
```

### Step 5: Execute Commit

For each repo being committed:

1. **Check status:**
   ```bash
   cd "<repo-path>" && git status
   ```

2. **Review changes:**
   ```bash
   cd "<repo-path>" && git diff
   cd "<repo-path>" && git diff --cached
   ```

3. **Check recent commit style:**
   ```bash
   cd "<repo-path>" && git log --oneline -5
   ```

4. **Stage changes:**
   ```bash
   cd "<repo-path>" && git add <files>
   ```

5. **Create commit with descriptive message:**
   ```bash
   cd "<repo-path>" && git commit -m "$(cat <<'EOF'
   <title>

   <body>

   Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
   EOF
   )"
   ```

6. **Push to remote (if exists):**
   ```bash
   cd "<repo-path>" && git push origin <branch>
   ```

### Step 6: Handle Repos Without Remotes

If a repo has no remote configured:

```bash
git remote -v
```

If empty, inform the user:
> "Committed locally to `<repo>`. No remote configured - changes not pushed."

## Commit Message Guidelines

- **Title:** Imperative mood, max 50 chars (e.g., "Add include/exclude checkbox to Risk Register")
- **Body:** Explain what and why, not how
- **Footer:** Always include `Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>`

## Known Nested Repos in This Workspace

| Path | Remote | Notes |
|------|--------|-------|
| `e:\Vibe Coding` | Vibecode101 | Root/parent repo |
| `e:\Vibe Coding\CoffeeCup` | CoffeeCup | Dashboard templates |
| `e:\Vibe Coding\Consulting` | (none) | Consulting materials |
| `e:\Vibe Coding\VibeCoded-Ebook` | (check) | E-book project |
| `e:\Vibe Coding\Marketing_Manager` | (check) | Marketing SaaS |
| `e:\Vibe Coding\Interloquial_Experiment` | (check) | Research platform |
| `e:\Vibe Coding\VibeCoding-Ebook-Marketing` | (check) | Marketing site |

## Safety Rules

- **NEVER** use `git commit --amend` unless explicitly requested
- **NEVER** use `git push --force` unless explicitly requested
- **NEVER** commit files that look like secrets (`.env`, `credentials.json`, etc.)
- **ALWAYS** show what will be committed before committing
- **ALWAYS** check for a remote before attempting to push

## Example Scenarios

### Scenario 1: Working in CoffeeCup folder
User runs `/commit` while editing `CoffeeCup/Risk/index.html`

→ Detect that CoffeeCup has its own `.git`
→ Commit to CoffeeCup repo, not root

### Scenario 2: Working in root on skills
User runs `/commit` after editing `.claude/skills/commit/SKILL.md`

→ This file is in root repo (no nested repo above it)
→ Commit to root repo

### Scenario 3: Changes in multiple places
User runs `/commit` after editing both `CoffeeCup/Risk/index.html` and `.claude/skills/q/SKILL.md`

→ Ask user which repo(s) to commit
→ Execute commits separately for each chosen repo

## Output Format

After successful commit(s), report:

```
✓ Committed to <repo-name> (<branch>)
  <commit-hash> <commit-title>
  → Pushed to origin/<branch>

[or if no remote]
  → Committed locally (no remote configured)
```
