# Start Working on a Ticket

Creates a new git worktree for a Jira ticket with automatic setup.

## Input

User provides either:
- Jira URL: `https://vuoriclothing.atlassian.net/browse/TDE-7379`
- Ticket ID: `TDE-7379`

## Steps

### 1. Parse Ticket ID

Extract the ticket ID from URL or use directly.

### 2. Fetch Ticket Details

```
mcp__atlassian__getJiraIssue with:
- cloudId: vuoriclothing.atlassian.net
- issueIdOrKey: <ticket-id>
```

Extract:
- `fields.summary` - ticket title
- `fields.status.name` - current status (to check if already "In Development")

### 3. Generate Branch Name

Pattern: `feat/TDE-XXXX-short-description`

Rules for short description:
- Convert summary to lowercase kebab-case
- Keep to 3-5 words max
- Remove filler words (the, a, an, for, to, etc.)

### 4. Check for Existing

```bash
git branch -a | grep <branch-name>
git worktree list | grep <ticket-id>
```

If exists, inform user and ask how to proceed.

### 5. Create Worktree

```bash
cd ~/Vuori/cascade
git fetch origin
git worktree add ~/Vuori/cascade-worktrees/<worktree-name> -b <branch-name> origin/main
```

Worktree name: `TDE-XXXX-short-description` (branch name without `feat/`)

### 6. Setup Environment

```bash
cp ~/Vuori/cascade/.env ~/Vuori/cascade-worktrees/<worktree-name>/
cd ~/Vuori/cascade-worktrees/<worktree-name> && npm install
```

Note: npm install may take several minutes.

### 7. Move Ticket to "In Development"

If the ticket is not already in "In Development" status, transition it:

1. Get available transitions: `mcp__atlassian__getTransitionsForJiraIssue`
2. Find the transition ID for "In Development"
3. Execute transition: `mcp__atlassian__transitionJiraIssue`

Skip this step if the ticket is already in "In Development" status.

### 8. Provide Summary

```
Created worktree for TDE-7379: "Optimize Lytics Tag Loading"

- Directory: ~/Vuori/cascade-worktrees/TDE-7379-optimize-lytics-loading
- Branch: feat/TDE-7379-optimize-lytics-loading
- Ticket status: Moved to "In Development"
- Setup: Ready (npm install complete)

To start working:
  cd ~/Vuori/cascade-worktrees/TDE-7379-optimize-lytics-loading && claude
```
