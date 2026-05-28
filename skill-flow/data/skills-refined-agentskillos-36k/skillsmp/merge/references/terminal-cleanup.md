# Terminal Cleanup via TabzChrome API

Before merging a feature branch, always kill the worker terminal first.

## API Details

```
TABZ_API="http://localhost:8129"
TOKEN=$(cat /tmp/tabz-auth-token)
```

## Find Worker Session by Issue ID

Workers are named by their issue ID:

```bash
# Get agent ID by name (issue ID)
AGENT_ID=$(curl -s "$TABZ_API/api/agents" | jq -r --arg id "$ISSUE_ID" \
  '.data[] | select(.name == $id) | .id')
```

## Kill Worker Terminal

```bash
# Kill via API (not tmux directly)
[ -n "$AGENT_ID" ] && curl -s -X DELETE "$TABZ_API/api/agents/$AGENT_ID" \
  -H "X-Auth-Token: $TOKEN"
```

## Complete Cleanup Sequence

1. **Kill terminal** - API call above
2. **Merge branch** - `git merge feature/$ISSUE_ID --no-edit`
3. **Remove worktree** - `git worktree remove .worktrees/$ISSUE_ID --force`
4. **Delete branch** - `git branch -d feature/$ISSUE_ID`
5. **Sync beads** - `bd sync && git push`

## One-Command Alternative

For full cleanup with checkpoints:

```bash
./plugins/conductor/scripts/finalize-issue.sh "$ISSUE_ID"
```

This handles: checkpoints → capture → kill terminal → merge → cleanup → sync/push
