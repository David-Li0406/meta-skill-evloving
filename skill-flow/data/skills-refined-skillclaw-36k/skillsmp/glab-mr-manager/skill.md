---
name: glab-mr-manager
description: Manage GitLab Merge Requests - create, review, approve, merge, and full MR lifecycle
---

# GitLab MR Manager Skill Instructions

Use the `glab` CLI to manage GitLab Merge Requests. This skill covers the complete MR lifecycle from creation to merge.

## Pre-Flight Check

Verify glab is installed and authenticated:

```bash
command -v glab &>/dev/null && echo "glab: installed ($(glab version 2>/dev/null | head -1))" || echo "glab: NOT INSTALLED"; glab auth status 2>&1 | head -3
```

**If glab is not installed**, guide the user:
```bash
brew install glab
```

**If not authenticated**, guide the user through authentication (see Setup section).

## Setup

### Option 1: Interactive OAuth (Recommended for gitlab.com)

```bash
glab auth login
```

Follow the prompts to authenticate via browser.

### Option 2: Personal Access Token

**Step 1:** Create token at GitLab → Settings → Access Tokens
- Required scopes: `api`, `write_repository`

**Step 2:** Add to shell profile:
```bash
printf '\nexport GITLAB_TOKEN="your-token-here"\nexport GITLAB_HOST="gitlab.com"  # or your self-hosted instance\n' >> ~/.zshrc && source ~/.zshrc
```

**Step 3:** Verify:
```bash
source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null; echo "GITLAB_HOST: ${GITLAB_HOST:-(not set)}"; echo "GITLAB_TOKEN: ${GITLAB_TOKEN:+set}"
```

### Option 3: Authenticate with Token Directly

```bash
glab auth login --hostname gitlab.com --token YOUR_TOKEN
```

For self-hosted GitLab:
```bash
glab auth login --hostname gitlab.example.com --token YOUR_TOKEN
```

Do NOT ask users to paste tokens directly in chat—tokens should stay in their shell profile or be entered via glab auth.

## Data Storage

For operations requiring cached data (large MR lists, API responses), store in `.claude/skills/glab/`:

**First-time setup:**
```bash
mkdir -p .claude/skills/glab && echo '*' > .claude/skills/glab/.gitignore
```

## MR Lifecycle Operations

### 1. Create MR

**From current branch (interactive):**
```bash
glab mr create
```

**With all details (non-interactive):**
```bash
glab mr create --fill --title "feat: add new feature" --description "Description here" --target-branch main
```

**Useful flags:**
| Flag | Description |
|------|-------------|
| `--fill` | Use commit info for title/description |
| `--fill-commit-body` | Include all commit messages in description |
| `-t, --title` | MR title |
| `-d, --description` | MR description |
| `-b, --target-branch` | Target branch (default: repo default) |
| `-s, --source-branch` | Source branch (default: current branch) |
| `-a, --assignee` | Assign to username(s) |
| `-r, --reviewer` | Request review from username(s) |
| `-l, --label` | Add labels |
| `--draft` / `--wip` | Create as draft MR |
| `--squash-before-merge` | Enable squash on merge |
| `-y, --yes` | Skip confirmation prompts |
| `-w, --web` | Open in browser after creation |

**Examples:**
```bash
# Quick MR with auto-filled info
glab mr create --fill --yes

# Draft MR with reviewers
glab mr create --fill --draft --reviewer "username1,username2"

# MR with labels and assignee
glab mr create --fill --label "bug,priority::high" --assignee "@me"

# Open in browser to add more details
glab mr create --fill --web
```

**Output:** Report MR number and URL: `Created !123: https://gitlab.com/group/project/-/merge_requests/123`

### 2. List MRs

**Your MRs:**
```bash
glab mr list --author="@me"
```

**MRs assigned to you:**
```bash
glab mr list --assignee="@me"
```

**MRs awaiting your review:**
```bash
glab mr list --reviewer="@me"
```

**Filter by state:**
```bash
glab mr list --state=opened    # opened, closed, merged, all
```

**Filter by labels:**
```bash
glab mr list --label="bug,priority::high"
```

**Search MRs:**
```bash
glab mr list --search="authentication"
```

**Output format:** Present as table with MR number, title, author, and state.

### 3. View MR Details

**View specific MR:**
```bash
glab mr view 123
```

**View in browser:**
```bash
glab mr view 123 --web
```

**View current branch's MR:**
```bash
glab mr view
```

**Output format:**
```
!123: MR Title Here
State: open | Author: username | Created: 2024-01-15
Target: main ← feature-branch
Labels: bug, priority::high
Assignees: user1, user2
Reviewers: reviewer1

Description:
[description text]

URL: https://gitlab.com/group/project/-/merge_requests/123
```

### 4. Checkout MR Locally

**Checkout MR branch:**
```bash
glab mr checkout 123
```

**Shorthand:**
```bash
glab co 123
```

**Checkout with specific branch name:**
```bash
glab mr checkout 123 --branch my-local-branch
```

This creates a local branch tracking the MR's source branch for review/testing.

### 5. View MR Diff

**View changes:**
```bash
glab mr diff 123
```

**View in browser:**
```bash
glab mr diff 123 --web
```

### 6. Add Comments/Notes

**Add comment:**
```bash
glab mr note 123 --message "Your comment here"
```

**Multi-line comment (use quotes):**
```bash
glab mr note 123 --message "Line 1
Line 2
Line 3"
```

**For complex comments, use heredoc:**
```bash
glab mr note 123 --message "$(cat <<'EOF'
## Review Notes

- Point 1
- Point 2

LGTM!
EOF
)"
```

### 7. Approve MR

**Approve:**
```bash
glab mr approve 123
```

**Approve current branch's MR:**
```bash
glab mr approve
```

**Revoke approval:**
```bash
glab mr revoke 123
```

### 8. Update MR

**Update title:**
```bash
glab mr update 123 --title "New title"
```

**Update description:**
```bash
glab mr update 123 --description "New description"
```

**Add/change labels:**
```bash
glab mr update 123 --label "label1,label2"
```

**Remove labels:**
```bash
glab mr update 123 --unlabel "old-label"
```

**Change assignees:**
```bash
glab mr update 123 --assignee "username1,username2"
```

**Unassign:**
```bash
glab mr update 123 --unassign "username"
```

**Add reviewers:**
```bash
glab mr update 123 --reviewer "reviewer1"
```

**Change target branch:**
```bash
glab mr update 123 --target-branch develop
```

**Mark as ready (remove draft):**
```bash
glab mr update 123 --ready
```

**Mark as draft:**
```bash
glab mr update 123 --draft
```

**Lock discussion:**
```bash
glab mr update 123 --lock-discussion
```

### 9. Rebase MR

**Rebase onto target branch:**
```bash
glab mr rebase 123
```

This triggers a server-side rebase. Useful when target branch has new commits.

### 10. Merge MR

**Simple merge:**
```bash
glab mr merge 123
```

**Merge with squash:**
```bash
glab mr merge 123 --squash
```

**Merge with custom squash message:**
```bash
glab mr merge 123 --squash --squash-message "feat: implement feature X"
```

**Merge with rebase:**
```bash
glab mr merge 123 --rebase
```

**Merge when pipeline succeeds:**
```bash
glab mr merge 123 --when-pipeline-succeeds
```

**Delete source branch after merge:**
```bash
glab mr merge 123 --remove-source-branch
```

**Combined (common pattern):**
```bash
glab mr merge 123 --squash --remove-source-branch --when-pipeline-succeeds
```

### 11. Close/Reopen MR

**Close without merging:**
```bash
glab mr close 123
```

**Reopen closed MR:**
```bash
glab mr reopen 123
```

### 12. Delete MR

**Delete MR (cannot be undone):**
```bash
glab mr delete 123
```

### 13. View Related Issues

**List issues that will be closed:**
```bash
glab mr issues 123
```

### 14. Subscribe/Unsubscribe

**Subscribe to notifications:**
```bash
glab mr subscribe 123
```

**Unsubscribe:**
```bash
glab mr unsubscribe 123
```

### 15. Create Todo Item

**Add MR to your GitLab todo list:**
```bash
glab mr todo 123
```

## Advanced: Direct API Access

For operations not covered by glab commands, use the API directly:

**Get MR details as JSON:**
```bash
glab api projects/:id/merge_requests/123 | jq '.'
```

**IMPORTANT: Two Types of MR Comments**

GitLab has two types of comments:
1. **Inline/Diff comments** - attached to specific code lines (returned by `/discussions`)
2. **General notes** - not attached to code (returned by `/notes`)

**Get ALL MR comments (inline + general) - USE THIS FIRST:**
```bash
glab api "projects/:id/merge_requests/123/notes" | jq '[.[] | select(.system == false) | {body: .body, author: .author.username, created: .created_at}]'
```

**Get inline comments only (with file/line info):**
```bash
glab api "projects/:id/merge_requests/123/discussions" | jq '[.[] | select(.notes[0].type == "DiffNote") | {file: .notes[0].position.new_path, line: .notes[0].position.new_line, body: .notes[0].body, resolved: .notes[0].resolved}]'
```

**Best practice:** When reviewing MR feedback, always fetch from `/notes` endpoint first to ensure you get ALL comments, then use `/discussions` if you need file/line locations for inline comments.

**Get MR approvals:**
```bash
glab api "projects/:id/merge_requests/123/approvals" | jq '{approved: .approved, approvers: [.approved_by[].user.username]}'
```

**Get MR changes (diff as JSON):**
```bash
glab api "projects/:id/merge_requests/123/changes" | jq '.changes[] | {file: .new_path, diff: .diff}'
```

**Reply to a discussion:**
```bash
glab api "projects/:id/merge_requests/123/discussions/DISCUSSION_ID/notes" -X POST -f "body=Your reply here"
```

**Note:** `:id` is automatically replaced with current project ID when in a git repo.

## Working with Other Repositories

**Specify repository:**
```bash
glab mr list -R owner/repo
glab mr view 123 -R group/subgroup/project
```

**Full URL also works:**
```bash
glab mr view 123 -R https://gitlab.com/group/project
```

## Error Handling

| Error | Fix |
|-------|-----|
| "could not determine base URL" | Run command inside a git repo or use `-R` flag |
| "401 Unauthorized" | Re-authenticate: `glab auth login` |
| "403 Forbidden" | User lacks permission for this action |
| "404 Not Found" | Check MR number and repository |
| "Merge request is not open" | MR already merged or closed |
| "Pipeline must succeed" | Wait for CI or use `--when-pipeline-succeeds` |
| "Merge blocked" | Resolve conflicts or required approvals |
| "glab not found" | Install: `brew install glab` |

## Output Guidelines

1. **Be concise**: Show key fields, not raw output
2. **Include MR URL**: Always provide clickable link
3. **Show state clearly**: open/merged/closed with visual indicator
4. **List labels/assignees**: When relevant to user's query
5. **Pipeline status**: Mention if blocking merge

## Common Workflows

### Quick MR from Feature Branch
```bash
git checkout -b feature/my-feature
# ... make changes, commit ...
git push -u origin feature/my-feature
glab mr create --fill --yes
```

### Review and Merge Flow
```bash
glab mr list --reviewer="@me"          # See MRs to review
glab mr checkout 123                    # Checkout locally
glab mr diff 123                        # Review changes
glab mr approve 123                     # Approve
glab mr merge 123 --squash --remove-source-branch  # Merge
```

### Draft to Ready Flow
```bash
glab mr create --fill --draft           # Create as draft
# ... iterate on changes ...
glab mr update 123 --ready              # Mark ready for review
```

## URL Parsing

Extract MR numbers from URLs:

| URL Pattern | MR Number Location |
|-------------|-------------------|
| `.../merge_requests/123` | After `/merge_requests/` |
| `.../-/merge_requests/123` | After `/-/merge_requests/` |
| `!123` in text | After `!` |
