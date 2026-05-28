# Repository Commands Reference

**Use `--json <fields>` with `--jq` for scriptable output.**

## `gh repo view`

View repository information.

```bash
gh repo view
gh repo view owner/repo
```

| Flag | Description |
|------|-------------|
| `--json <fields>` | JSON output with fields: `name`, `owner`, `description`, `url`, `sshUrl`, `defaultBranchRef`, `isPrivate`, `isFork`, `stargazerCount`, `forkCount`, `watchers`, `issues`, `pullRequests`, `languages`, `licenseInfo`, `createdAt`, `pushedAt` |
| `-q, --jq` | Filter JSON |
| `-w, --web` | Open in browser |
| `-b, --branch` | View specific branch |

**Examples:**
```bash
gh repo view
gh repo view --web
gh repo view owner/repo --json name,description,stargazerCount
```

---

## `gh repo clone`

Clone a repository.

```bash
gh repo clone owner/repo
gh repo clone owner/repo <directory>
```

| Flag | Description |
|------|-------------|
| `-u, --upstream-remote-name` | Name for upstream remote (when cloning a fork) |

**Examples:**
```bash
gh repo clone cli/cli
gh repo clone cli/cli gh-cli-source
```

---

## `gh repo create`

Create a new repository.

```bash
gh repo create <name>
gh repo create owner/name
```

| Flag | Description |
|------|-------------|
| `--public` | Public repository |
| `--private` | Private repository |
| `--internal` | Internal repository (enterprise) |
| `-d, --description` | Repository description |
| `-h, --homepage` | Homepage URL |
| `-l, --license` | License (e.g., `mit`, `apache-2.0`, `gpl-3.0`) |
| `-g, --gitignore` | Gitignore template |
| `--disable-issues` | Disable issues |
| `--disable-wiki` | Disable wiki |
| `-c, --clone` | Clone after creating |
| `-s, --source` | Create from local directory |
| `-r, --remote` | Remote name (default: `origin`) |
| `--push` | Push local commits |
| `-t, --team` | Team with access |
| `--add-readme` | Add README file |
| `--template` | Create from template repo |

**Examples:**
```bash
# Create and clone
gh repo create my-project --public --clone --add-readme

# Create from current directory
gh repo create my-project --source . --public --push

# Create from template
gh repo create my-project --template owner/template-repo --clone

# Private with license
gh repo create my-project --private --license mit --description "My project"
```

---

## `gh repo fork`

Fork a repository.

```bash
gh repo fork owner/repo
gh repo fork                # Fork current repo
```

| Flag | Description |
|------|-------------|
| `--clone` | Clone fork locally |
| `--remote` | Add remote for fork |
| `--remote-name` | Name for fork remote (default: `origin`) |
| `--org` | Fork to organization |
| `--fork-name` | Name for forked repo |

**Examples:**
```bash
# Fork and clone
gh repo fork owner/repo --clone

# Fork to org
gh repo fork owner/repo --org my-org --clone
```

---

## `gh repo edit`

Edit repository settings.

```bash
gh repo edit
gh repo edit owner/repo
```

| Flag | Description |
|------|-------------|
| `-d, --description` | Set description |
| `-h, --homepage` | Set homepage |
| `--visibility` | `public`, `private`, `internal` |
| `--default-branch` | Set default branch |
| `--enable-issues` | Enable/disable issues |
| `--enable-wiki` | Enable/disable wiki |
| `--enable-projects` | Enable/disable projects |
| `--enable-discussions` | Enable/disable discussions |
| `--enable-merge-commit` | Allow merge commits |
| `--enable-squash-merge` | Allow squash merge |
| `--enable-rebase-merge` | Allow rebase merge |
| `--enable-auto-merge` | Enable auto-merge |
| `--delete-branch-on-merge` | Delete branches on merge |
| `--allow-forking` | Allow forking (private repos) |
| `--add-topic` | Add topic |
| `--remove-topic` | Remove topic |

**Examples:**
```bash
# Update description
gh repo edit --description "New description"

# Configure merge options
gh repo edit --enable-squash-merge --delete-branch-on-merge

# Add topics
gh repo edit --add-topic golang --add-topic cli
```

---

## `gh repo delete`

Delete a repository.

```bash
gh repo delete owner/repo
```

| Flag | Description |
|------|-------------|
| `--yes` | Skip confirmation |

**Example:**
```bash
gh repo delete owner/repo --yes
```

---

## `gh repo list`

List repositories.

```bash
gh repo list
gh repo list owner
```

| Flag | Description |
|------|-------------|
| `-l, --language` | Filter by language |
| `--source` | Only source repos (not forks) |
| `--fork` | Only forks |
| `--archived` | Show archived |
| `--no-archived` | Hide archived |
| `--visibility` | `public`, `private`, `internal` |
| `-L, --limit` | Maximum number |
| `--json <fields>` | JSON output |
| `-q, --jq` | Filter JSON |

**Examples:**
```bash
gh repo list --language go --limit 10
gh repo list owner --source --json name,stargazerCount
```

---

## `gh repo sync`

Sync a fork with its upstream.

```bash
gh repo sync
gh repo sync owner/repo
```

| Flag | Description |
|------|-------------|
| `-b, --branch` | Branch to sync |
| `-s, --source` | Source repository |
| `--force` | Force sync (may lose commits) |

**Examples:**
```bash
# Sync current repo fork
gh repo sync

# Sync specific branch
gh repo sync --branch main
```

---

## `gh repo archive`

Archive a repository.

```bash
gh repo archive owner/repo
```

| Flag | Description |
|------|-------------|
| `--yes` | Skip confirmation |

---

## `gh repo unarchive`

Unarchive a repository.

```bash
gh repo unarchive owner/repo
```

---

## `gh repo rename`

Rename a repository.

```bash
gh repo rename <new-name>
gh repo rename owner/repo <new-name>
```

| Flag | Description |
|------|-------------|
| `--yes` | Skip confirmation |

---

## `gh repo set-default`

Set default repository for commands.

```bash
gh repo set-default owner/repo
gh repo set-default --view    # View current default
```

---

## `gh repo deploy-key`

Manage deploy keys.

```bash
gh repo deploy-key list
gh repo deploy-key add <key-file> --title "Key name"
gh repo deploy-key delete <key-id>
```

| Flag | Description |
|------|-------------|
| `--allow-write` | Allow write access |

---

## Common Workflows

### Create new project repository

```bash
gh repo create my-project --public --license mit --add-readme --clone
cd my-project
```

### Fork and contribute

```bash
gh repo fork owner/repo --clone
cd repo
gh repo set-default owner/repo  # Set upstream as default for PRs
```

### Sync fork with upstream

```bash
gh repo sync --branch main
git pull
```

### Archive old project

```bash
gh repo edit --description "[ARCHIVED] Old description"
gh repo archive --yes
```
