# GitLab MR Manager Skill

Manage GitLab Merge Requests from Claude Code using the glab CLI.

## Setup

### 1. Install glab

```bash
brew install glab
```

### 2. Authenticate

**For gitlab.com:**
```bash
glab auth login
```

**For self-hosted GitLab:**
```bash
glab auth login --hostname gitlab.example.com
```

**Or via environment variable (add to `~/.zshrc`):**
```bash
printf '\nexport GITLAB_TOKEN="your-token-here"\nexport GITLAB_HOST="gitlab.com"\n' >> ~/.zshrc && source ~/.zshrc
```

Create token at: GitLab → Settings → Access Tokens (scopes: `api`, `write_repository`)

### 3. Verify

```bash
glab auth status
```

## Usage

```
/glab create MR from current branch
/glab list my open MRs
/glab view !123
/glab checkout !123 for review
/glab approve !123
/glab merge !123 with squash
/glab add comment to !123: your comment here
```

Or describe what you need naturally - the skill handles the glab commands.

## Operations

| Command | Description |
|---------|-------------|
| create | Create new MR from branch |
| list | List MRs (filter by author/assignee/reviewer) |
| view | View MR details |
| checkout | Checkout MR branch locally |
| diff | View MR changes |
| note | Add comment to MR |
| approve | Approve MR |
| revoke | Revoke approval |
| update | Modify MR (title, labels, assignees, etc.) |
| rebase | Rebase MR onto target |
| merge | Merge MR |
| close | Close MR without merging |
| reopen | Reopen closed MR |

## MR Lifecycle

```
create → review → approve → merge
   ↓        ↓        ↓
 draft → update → rebase
```

1. **Create**: `glab mr create --fill`
2. **Review**: `glab mr checkout`, `glab mr diff`
3. **Comment**: `glab mr note`
4. **Approve**: `glab mr approve`
5. **Merge**: `glab mr merge --squash --remove-source-branch`

## Common Patterns

**Quick MR:**
```bash
glab mr create --fill --yes
```

**Draft MR with reviewers:**
```bash
glab mr create --fill --draft --reviewer "username"
```

**Review workflow:**
```bash
glab mr list --reviewer="@me"
glab mr checkout 123
glab mr approve 123
glab mr merge 123 --squash
```

## Requirements

- `glab` — install: `brew install glab`
- `jq` (optional, for API parsing) — install: `brew install jq`

## Troubleshooting

| Error | Fix |
|-------|-----|
| "glab not found" | `brew install glab` |
| 401 Unauthorized | `glab auth login` |
| 403 Forbidden | Check permissions in GitLab |
| "not a git repository" | Run inside repo or use `-R owner/repo` |
| Pipeline blocking merge | Use `--when-pipeline-succeeds` flag |
