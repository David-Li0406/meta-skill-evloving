# Other Commands Reference

## Releases

### `gh release list`

List releases.

```bash
gh release list
```

| Flag | Description |
|------|-------------|
| `-L, --limit` | Maximum number |
| `--exclude-drafts` | Exclude drafts |
| `--exclude-pre-releases` | Exclude pre-releases |
| `--json <fields>` | JSON output |

---

### `gh release view`

View a release.

```bash
gh release view <tag>
gh release view           # Latest release
```

| Flag | Description |
|------|-------------|
| `--json <fields>` | JSON output |
| `-w, --web` | Open in browser |

---

### `gh release create`

Create a release.

```bash
gh release create <tag>
gh release create <tag> <files...>
```

| Flag | Description |
|------|-------------|
| `-t, --title` | Release title |
| `-n, --notes` | Release notes |
| `-F, --notes-file` | Read notes from file |
| `--generate-notes` | Auto-generate notes |
| `-d, --draft` | Create as draft |
| `-p, --prerelease` | Mark as pre-release |
| `--target` | Target branch/commit |
| `--latest` | Mark as latest (default: auto) |
| `--discussion-category` | Create discussion |

**Examples:**
```bash
# Simple release
gh release create v1.0.0 --generate-notes

# With assets
gh release create v1.0.0 ./dist/*.tar.gz --title "v1.0.0" --notes "Release notes..."

# Draft pre-release
gh release create v2.0.0-beta.1 --prerelease --draft
```

---

### `gh release download`

Download release assets.

```bash
gh release download <tag>
gh release download       # Latest release
```

| Flag | Description |
|------|-------------|
| `-p, --pattern` | Asset name pattern |
| `-D, --dir` | Download directory |
| `-A, --archive` | Download source: `zip` or `tar.gz` |
| `--skip-existing` | Skip existing files |

---

### `gh release delete`

Delete a release.

```bash
gh release delete <tag>
```

| Flag | Description |
|------|-------------|
| `--yes` | Skip confirmation |
| `--cleanup-tag` | Delete associated tag |

---

### `gh release edit`

Edit a release.

```bash
gh release edit <tag>
```

| Flag | Description |
|------|-------------|
| `--tag` | Rename tag |
| `-t, --title` | Edit title |
| `-n, --notes` | Edit notes |
| `--draft` | Set draft state |
| `--prerelease` | Set prerelease state |
| `--latest` | Set as latest |

---

### `gh release upload`

Upload assets to a release.

```bash
gh release upload <tag> <files...>
```

| Flag | Description |
|------|-------------|
| `--clobber` | Overwrite existing assets |

---

## Gists

### `gh gist list`

List your gists.

```bash
gh gist list
```

| Flag | Description |
|------|-------------|
| `--public` | Public only |
| `--secret` | Secret only |
| `-L, --limit` | Maximum number |

---

### `gh gist view`

View a gist.

```bash
gh gist view <id|url>
```

| Flag | Description |
|------|-------------|
| `-f, --filename` | View specific file |
| `-r, --raw` | Raw content |
| `-w, --web` | Open in browser |

---

### `gh gist create`

Create a gist.

```bash
gh gist create <files...>
gh gist create -          # From stdin
```

| Flag | Description |
|------|-------------|
| `-d, --desc` | Description |
| `-f, --filename` | Filename (for stdin) |
| `-p, --public` | Public gist |
| `-w, --web` | Open in browser |

**Examples:**
```bash
gh gist create script.sh --public --desc "Useful script"
cat file.txt | gh gist create -f output.txt
```

---

### `gh gist edit`

Edit a gist.

```bash
gh gist edit <id>
```

| Flag | Description |
|------|-------------|
| `-a, --add` | Add file |
| `-d, --desc` | Edit description |
| `-f, --filename` | Edit specific file |

---

### `gh gist delete`

Delete a gist.

```bash
gh gist delete <id>
```

---

### `gh gist clone`

Clone a gist.

```bash
gh gist clone <id> [directory]
```

---

### `gh gist rename`

Rename a file in a gist.

```bash
gh gist rename <id> <old-name> <new-name>
```

---

## API

### `gh api`

Make authenticated GitHub API requests.

```bash
gh api <endpoint>
```

| Flag | Description |
|------|-------------|
| `-X, --method` | HTTP method (default: GET) |
| `-H, --header` | Add header |
| `-F, --field` | Add field: `key=value` (typed) |
| `-f, --raw-field` | Add field: `key=value` (string) |
| `--input` | Read body from file |
| `-q, --jq` | Filter JSON response |
| `-t, --template` | Format with Go template |
| `-p, --paginate` | Paginate results |
| `--cache` | Cache response duration |
| `--hostname` | GitHub hostname |
| `-i, --include` | Include response headers |
| `--silent` | No output |

**Examples:**
```bash
# Get user info
gh api user

# Get repo info
gh api repos/owner/repo

# Create issue
gh api repos/owner/repo/issues -X POST -f title="Bug" -f body="Description"

# GraphQL query
gh api graphql -f query='{ viewer { login } }'

# Paginate results
gh api repos/owner/repo/issues --paginate --jq '.[].title'

# With template
gh api repos/owner/repo --template '{{.full_name}}: {{.stargazers_count}} stars'
```

---

## Search

### `gh search repos`

Search repositories.

```bash
gh search repos <query>
```

| Flag | Description |
|------|-------------|
| `--language` | Filter by language |
| `--owner` | Filter by owner |
| `--topic` | Filter by topic |
| `--visibility` | `public`, `private`, `internal` |
| `--archived` | Include archived |
| `--stars` | Star count: `>1000`, `100..500` |
| `--forks` | Fork count |
| `--created` | Creation date |
| `--pushed` | Last push date |
| `--license` | License type |
| `-L, --limit` | Maximum results |
| `--json` | JSON output |
| `--order` | `asc` or `desc` |
| `--sort` | `stars`, `forks`, `updated`, `help-wanted-issues` |

**Examples:**
```bash
gh search repos cli --language go --stars ">1000"
gh search repos "machine learning" --sort stars --limit 10
```

---

### `gh search code`

Search code.

```bash
gh search code <query>
```

| Flag | Description |
|------|-------------|
| `--repo` | Search in repo |
| `--language` | Filter by language |
| `--filename` | Filter by filename |
| `--extension` | Filter by extension |
| `--path` | Filter by path |
| `-L, --limit` | Maximum results |
| `--json` | JSON output |
| `-w, --web` | Open in browser |

**Examples:**
```bash
gh search code "func main" --language go --repo owner/repo
gh search code "TODO" --filename "*.py" --repo owner/repo
```

---

### `gh search issues`

Search issues.

```bash
gh search issues <query>
```

| Flag | Description |
|------|-------------|
| `--repo` | Search in repo |
| `--owner` | Filter by owner |
| `--state` | `open`, `closed` |
| `--assignee` | Filter by assignee |
| `--author` | Filter by author |
| `--label` | Filter by label |
| `--language` | Filter by repo language |
| `--created` | Creation date |
| `--updated` | Update date |
| `-L, --limit` | Maximum results |
| `--json` | JSON output |

---

### `gh search prs`

Search pull requests.

```bash
gh search prs <query>
```

Same flags as `gh search issues`, plus:

| Flag | Description |
|------|-------------|
| `--merged` | Merge date |
| `--merged-at` | Merged at date |
| `--draft` | Draft state |
| `--review` | Review status |
| `--review-requested` | Review requested from |

---

### `gh search commits`

Search commits.

```bash
gh search commits <query>
```

| Flag | Description |
|------|-------------|
| `--repo` | Search in repo |
| `--owner` | Filter by owner |
| `--author` | Filter by author |
| `--committer` | Filter by committer |
| `--author-date` | Author date |
| `--committer-date` | Committer date |
| `-L, --limit` | Maximum results |
| `--json` | JSON output |

---

## Authentication

### `gh auth login`

Authenticate with GitHub.

```bash
gh auth login
```

| Flag | Description |
|------|-------------|
| `-h, --hostname` | GitHub hostname |
| `-s, --scopes` | Additional scopes |
| `-w, --web` | Web-based auth |
| `--with-token` | Read token from stdin |
| `-p, --git-protocol` | `https` or `ssh` |
| `--insecure-storage` | Don't use system keyring |

**Examples:**
```bash
# Interactive login
gh auth login

# Login with token
echo $GITHUB_TOKEN | gh auth login --with-token

# Enterprise
gh auth login --hostname github.example.com
```

---

### `gh auth logout`

Log out of GitHub.

```bash
gh auth logout
```

---

### `gh auth status`

View authentication status.

```bash
gh auth status
```

| Flag | Description |
|------|-------------|
| `-t, --show-token` | Display token |

---

### `gh auth token`

Print authentication token.

```bash
gh auth token
```

---

### `gh auth refresh`

Refresh authentication.

```bash
gh auth refresh
```

| Flag | Description |
|------|-------------|
| `-s, --scopes` | Additional scopes |
| `--remove-scopes` | Remove scopes |

---

### `gh auth setup-git`

Configure git to use gh for auth.

```bash
gh auth setup-git
```

---

## Secrets and Variables

### `gh secret list`

List secrets.

```bash
gh secret list
gh secret list --org <org>
gh secret list --env <environment>
```

---

### `gh secret set`

Set a secret.

```bash
gh secret set <name>
gh secret set <name> --body <value>
```

| Flag | Description |
|------|-------------|
| `-b, --body` | Secret value |
| `-f, --env-file` | Load from env file |
| `-e, --env` | Environment secret |
| `-o, --org` | Organization secret |
| `-v, --visibility` | `all`, `private`, `selected` |
| `-r, --repos` | Repos for selected visibility |

**Examples:**
```bash
echo "value" | gh secret set SECRET_NAME
gh secret set SECRET_NAME --body "value"
gh secret set SECRET_NAME --env production
```

---

### `gh secret delete`

Delete a secret.

```bash
gh secret delete <name>
```

---

### `gh variable list`

List variables.

```bash
gh variable list
gh variable list --env <environment>
```

---

### `gh variable set`

Set a variable.

```bash
gh variable set <name> --body <value>
```

---

### `gh variable delete`

Delete a variable.

```bash
gh variable delete <name>
```

---

## Labels

### `gh label list`

List labels.

```bash
gh label list
```

| Flag | Description |
|------|-------------|
| `-L, --limit` | Maximum number |
| `--json` | JSON output |
| `-S, --search` | Search query |

---

### `gh label create`

Create a label.

```bash
gh label create <name>
```

| Flag | Description |
|------|-------------|
| `-c, --color` | Color (hex without #) |
| `-d, --description` | Description |
| `-f, --force` | Update if exists |

---

### `gh label edit`

Edit a label.

```bash
gh label edit <name>
```

| Flag | Description |
|------|-------------|
| `-n, --name` | New name |
| `-c, --color` | New color |
| `-d, --description` | New description |

---

### `gh label delete`

Delete a label.

```bash
gh label delete <name>
```

---

### `gh label clone`

Clone labels from another repo.

```bash
gh label clone <source-repo>
```

| Flag | Description |
|------|-------------|
| `-f, --force` | Overwrite existing |

---

## Miscellaneous

### `gh status`

View your GitHub status (notifications, PRs, issues).

```bash
gh status
```

| Flag | Description |
|------|-------------|
| `-o, --org` | Filter by organization |
| `-e, --exclude` | Exclude repos |

---

### `gh config`

Manage gh configuration.

```bash
gh config get <key>
gh config set <key> <value>
gh config list
```

**Common keys:**
- `git_protocol`: `https` or `ssh`
- `editor`: Default editor
- `prompt`: Enable prompts
- `pager`: Pager program
- `browser`: Default browser

---

### `gh alias`

Create command aliases.

```bash
gh alias set <alias> <command>
gh alias list
gh alias delete <alias>
```

**Examples:**
```bash
gh alias set pv 'pr view'
gh alias set co 'pr checkout'
gh alias set bugs 'issue list --label bug'
```

---

### `gh extension`

Manage gh extensions.

```bash
gh extension list
gh extension install <repo>
gh extension upgrade <name>
gh extension remove <name>
gh extension search <query>
```

---

### `gh ssh-key`

Manage SSH keys.

```bash
gh ssh-key list
gh ssh-key add <key-file> --title "Key name"
gh ssh-key delete <key-id>
```

---

### `gh gpg-key`

Manage GPG keys.

```bash
gh gpg-key list
gh gpg-key add <key-file>
gh gpg-key delete <key-id>
```
