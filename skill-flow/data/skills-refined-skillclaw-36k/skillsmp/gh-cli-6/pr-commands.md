# Pull Request Commands Reference

**Use `--json <fields>` with `--jq` for scriptable output.**

## `gh pr list`

List pull requests in a repository.

```bash
gh pr list
gh pr list --author @me --state open
```

### Filter Flags

| Flag | Description |
|------|-------------|
| `-a, --author` | Filter by author (`@me` for self) |
| `-A, --assignee` | Filter by assignee |
| `-s, --state` | `open`, `closed`, `merged`, `all` (default: `open`) |
| `-B, --base` | Filter by base branch |
| `-H, --head` | Filter by head branch |
| `-l, --label` | Filter by label (repeatable) |
| `-S, --search` | Search query |
| `--draft` | Filter by draft state |
| `-L, --limit` | Maximum number (default: 30) |

### Output Flags

| Flag | Description |
|------|-------------|
| `--json <fields>` | JSON output with fields: `number`, `title`, `state`, `url`, `headRefName`, `baseRefName`, `author`, `labels`, `reviewDecision`, `mergeable`, `additions`, `deletions`, `changedFiles`, `createdAt`, `updatedAt` |
| `-q, --jq` | Filter JSON with jq expression |
| `-w, --web` | Open in browser |

**Examples:**
```bash
# My open PRs
gh pr list --author @me

# PRs needing review
gh pr list --search "review:required"

# JSON output for scripting
gh pr list --json number,title,state --jq '.[] | "\(.number): \(.title)"'
```

---

## `gh pr view`

View a pull request.

```bash
gh pr view <number>
gh pr view              # View PR for current branch
```

| Flag | Description |
|------|-------------|
| `-c, --comments` | View comments |
| `--json <fields>` | JSON output |
| `-w, --web` | Open in browser |

**Examples:**
```bash
gh pr view 123
gh pr view --web
gh pr view 123 --json title,body,reviews
```

---

## `gh pr create`

Create a pull request.

```bash
gh pr create --fill
gh pr create --title "Title" --body "Description"
```

| Flag | Description |
|------|-------------|
| `-t, --title` | PR title |
| `-b, --body` | PR body |
| `-B, --base` | Base branch (default: default branch) |
| `-H, --head` | Head branch (default: current branch) |
| `-f, --fill` | Use commit info for title/body |
| `-d, --draft` | Create as draft |
| `-l, --label` | Add labels (repeatable) |
| `-a, --assignee` | Add assignees (repeatable, `@me` for self) |
| `-r, --reviewer` | Request reviewers (repeatable) |
| `-m, --milestone` | Add milestone |
| `-p, --project` | Add to project |
| `--no-maintainer-edit` | Disable maintainer edits |
| `-w, --web` | Open browser to create |

**Examples:**
```bash
# Quick PR with commit messages
gh pr create --fill

# PR with reviewers
gh pr create --title "Add feature" --body "Details..." --reviewer user1,user2

# Draft PR
gh pr create --fill --draft

# PR to specific base
gh pr create --fill --base develop
```

---

## `gh pr checkout`

Check out a pull request locally.

```bash
gh pr checkout <number>
gh pr checkout <branch>
gh pr checkout <url>
```

| Flag | Description |
|------|-------------|
| `-b, --branch` | Local branch name |
| `--detach` | Checkout as detached HEAD |
| `-f, --force` | Force checkout |
| `--recurse-submodules` | Update submodules |

**Examples:**
```bash
gh pr checkout 123
gh pr checkout 123 -b feature-review
```

---

## `gh pr merge`

Merge a pull request.

```bash
gh pr merge <number>
gh pr merge             # Merge PR for current branch
```

| Flag | Description |
|------|-------------|
| `-m, --merge` | Merge commit |
| `-s, --squash` | Squash and merge |
| `-r, --rebase` | Rebase and merge |
| `--auto` | Enable auto-merge when checks pass |
| `-d, --delete-branch` | Delete branch after merge |
| `--admin` | Merge with admin privileges |
| `-t, --subject` | Commit subject |
| `-b, --body` | Commit body |

**Examples:**
```bash
# Squash merge and delete branch
gh pr merge 123 --squash --delete-branch

# Enable auto-merge
gh pr merge 123 --auto --squash

# Merge with custom message
gh pr merge 123 --merge --subject "feat: add feature"
```

---

## `gh pr close`

Close a pull request without merging.

```bash
gh pr close <number>
```

| Flag | Description |
|------|-------------|
| `-d, --delete-branch` | Delete branch |
| `-c, --comment` | Add closing comment |

---

## `gh pr reopen`

Reopen a closed pull request.

```bash
gh pr reopen <number>
```

---

## `gh pr ready`

Mark a draft PR as ready for review.

```bash
gh pr ready <number>
gh pr ready             # Current branch PR
```

---

## `gh pr review`

Add a review to a pull request.

```bash
gh pr review <number>
```

| Flag | Description |
|------|-------------|
| `-a, --approve` | Approve PR |
| `-r, --request-changes` | Request changes |
| `-c, --comment` | Comment without approval |
| `-b, --body` | Review body |

**Examples:**
```bash
gh pr review 123 --approve
gh pr review 123 --approve --body "LGTM!"
gh pr review 123 --request-changes --body "Please fix..."
```

---

## `gh pr checks`

View CI status for a pull request.

```bash
gh pr checks <number>
gh pr checks            # Current branch PR
```

| Flag | Description |
|------|-------------|
| `--watch` | Watch until checks complete |
| `--fail-fast` | Exit on first failed check |
| `--required` | Only show required checks |
| `--json` | JSON output |

**Examples:**
```bash
# Wait for CI
gh pr checks --watch

# Check required only
gh pr checks --required
```

---

## `gh pr diff`

View PR diff.

```bash
gh pr diff <number>
gh pr diff              # Current branch PR
```

| Flag | Description |
|------|-------------|
| `--color` | Color output: `always`, `never`, `auto` |
| `--patch` | Patch format |
| `--name-only` | Only show file names |

---

## `gh pr edit`

Edit a pull request.

```bash
gh pr edit <number>
```

| Flag | Description |
|------|-------------|
| `-t, --title` | Edit title |
| `-b, --body` | Edit body |
| `-B, --base` | Change base branch |
| `--add-label` | Add labels |
| `--remove-label` | Remove labels |
| `--add-reviewer` | Add reviewers |
| `--remove-reviewer` | Remove reviewers |
| `--add-assignee` | Add assignees |
| `--remove-assignee` | Remove assignees |
| `--milestone` | Set milestone |

---

## `gh pr comment`

Add a comment to a pull request.

```bash
gh pr comment <number> --body "Comment text"
```

| Flag | Description |
|------|-------------|
| `-b, --body` | Comment text |
| `-F, --body-file` | Read from file |
| `--edit-last` | Edit your last comment |
| `-w, --web` | Open browser to comment |

---

## Common Workflows

### Create PR and request review

```bash
gh pr create --fill --reviewer teammate1,teammate2
```

### Check CI and merge when green

```bash
gh pr checks --watch && gh pr merge --squash --delete-branch
```

### Auto-merge when CI passes

```bash
gh pr create --fill
gh pr merge --auto --squash --delete-branch
```

### Review a PR locally

```bash
gh pr checkout 123
# ... test locally ...
gh pr review 123 --approve --body "Tested locally, LGTM"
```
