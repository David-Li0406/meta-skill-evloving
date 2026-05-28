# Issue Commands Reference

**Use `--json <fields>` with `--jq` for scriptable output.**

## `gh issue list`

List issues in a repository.

```bash
gh issue list
gh issue list --assignee @me --state open
```

### Filter Flags

| Flag | Description |
|------|-------------|
| `-a, --assignee` | Filter by assignee (`@me` for self) |
| `-A, --author` | Filter by author |
| `-s, --state` | `open`, `closed`, `all` (default: `open`) |
| `-l, --label` | Filter by label (repeatable) |
| `-m, --milestone` | Filter by milestone |
| `-S, --search` | Search query |
| `--mention` | Filter by mention |
| `-L, --limit` | Maximum number (default: 30) |

### Output Flags

| Flag | Description |
|------|-------------|
| `--json <fields>` | JSON output with fields: `number`, `title`, `state`, `url`, `body`, `author`, `labels`, `assignees`, `milestone`, `comments`, `createdAt`, `updatedAt`, `closedAt` |
| `-q, --jq` | Filter JSON with jq expression |
| `-w, --web` | Open in browser |

**Examples:**
```bash
# My assigned issues
gh issue list --assignee @me

# Issues with label
gh issue list --label bug --label priority-high

# Search issues
gh issue list --search "memory leak"

# JSON for scripting
gh issue list --json number,title,state --jq '.[] | select(.state == "OPEN")'
```

---

## `gh issue view`

View an issue.

```bash
gh issue view <number>
```

| Flag | Description |
|------|-------------|
| `-c, --comments` | View comments |
| `--json <fields>` | JSON output |
| `-w, --web` | Open in browser |

**Examples:**
```bash
gh issue view 123
gh issue view 123 --comments
gh issue view 123 --json title,body,labels
```

---

## `gh issue create`

Create an issue.

```bash
gh issue create --title "Title" --body "Description"
```

| Flag | Description |
|------|-------------|
| `-t, --title` | Issue title |
| `-b, --body` | Issue body |
| `-l, --label` | Add labels (repeatable) |
| `-a, --assignee` | Add assignees (repeatable, `@me` for self) |
| `-m, --milestone` | Add to milestone |
| `-p, --project` | Add to project |
| `-T, --template` | Use issue template |
| `-F, --body-file` | Read body from file |
| `-w, --web` | Open browser to create |

**Examples:**
```bash
# Simple issue
gh issue create --title "Bug: login fails" --body "Steps to reproduce..."

# Issue with metadata
gh issue create --title "Feature request" --body "Details..." --label enhancement --assignee @me

# From template
gh issue create --template bug_report.md
```

---

## `gh issue edit`

Edit an issue.

```bash
gh issue edit <number>
```

| Flag | Description |
|------|-------------|
| `-t, --title` | Edit title |
| `-b, --body` | Edit body |
| `--add-label` | Add labels |
| `--remove-label` | Remove labels |
| `--add-assignee` | Add assignees |
| `--remove-assignee` | Remove assignees |
| `-m, --milestone` | Set milestone |
| `--add-project` | Add to project |
| `--remove-project` | Remove from project |

**Examples:**
```bash
# Update title
gh issue edit 123 --title "New title"

# Add labels
gh issue edit 123 --add-label bug --add-label priority-high

# Change assignee
gh issue edit 123 --remove-assignee old-user --add-assignee new-user
```

---

## `gh issue close`

Close an issue.

```bash
gh issue close <number>
```

| Flag | Description |
|------|-------------|
| `-c, --comment` | Add closing comment |
| `-r, --reason` | `completed` or `not_planned` |

**Examples:**
```bash
gh issue close 123
gh issue close 123 --comment "Fixed in PR #456"
gh issue close 123 --reason not_planned --comment "Won't fix"
```

---

## `gh issue reopen`

Reopen a closed issue.

```bash
gh issue reopen <number>
```

| Flag | Description |
|------|-------------|
| `-c, --comment` | Add comment when reopening |

---

## `gh issue comment`

Add a comment to an issue.

```bash
gh issue comment <number> --body "Comment text"
```

| Flag | Description |
|------|-------------|
| `-b, --body` | Comment text |
| `-F, --body-file` | Read from file |
| `--edit-last` | Edit your last comment |
| `-w, --web` | Open browser to comment |

---

## `gh issue pin`

Pin an issue to the repository.

```bash
gh issue pin <number>
```

---

## `gh issue unpin`

Unpin an issue.

```bash
gh issue unpin <number>
```

---

## `gh issue transfer`

Transfer an issue to another repository.

```bash
gh issue transfer <number> <destination-repo>
```

**Example:**
```bash
gh issue transfer 123 owner/other-repo
```

---

## `gh issue lock`

Lock an issue conversation.

```bash
gh issue lock <number>
```

| Flag | Description |
|------|-------------|
| `-r, --reason` | `off_topic`, `resolved`, `spam`, `too_heated` |

---

## `gh issue unlock`

Unlock an issue conversation.

```bash
gh issue unlock <number>
```

---

## `gh issue delete`

Delete an issue.

```bash
gh issue delete <number>
```

| Flag | Description |
|------|-------------|
| `--yes` | Skip confirmation |

---

## `gh issue develop`

Create a branch linked to an issue.

```bash
gh issue develop <number>
```

| Flag | Description |
|------|-------------|
| `-n, --name` | Branch name |
| `-b, --base` | Base branch |
| `-c, --checkout` | Checkout the branch |
| `-l, --list` | List linked branches |

**Examples:**
```bash
# Create and checkout branch
gh issue develop 123 --checkout

# Custom branch name
gh issue develop 123 --name fix-issue-123 --checkout
```

---

## Common Workflows

### Create issue and assign to self

```bash
gh issue create --title "Task" --body "Description" --assignee @me
```

### Bulk label issues

```bash
# Add label to multiple issues
for i in 1 2 3; do gh issue edit $i --add-label needs-triage; done
```

### Link issue to PR

```bash
# Create branch from issue, then PR
gh issue develop 123 --checkout
# ... make changes ...
gh pr create --fill  # Will auto-link to issue
```

### Search and close stale issues

```bash
# List old issues
gh issue list --search "created:<2023-01-01" --json number,title
```
