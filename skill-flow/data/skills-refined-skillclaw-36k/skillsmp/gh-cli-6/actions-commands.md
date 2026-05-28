# GitHub Actions Commands Reference

**Use `--json <fields>` with `--jq` for scriptable output.**

## Workflow Runs

### `gh run list`

List recent workflow runs.

```bash
gh run list
gh run list --workflow build.yml
```

| Flag | Description |
|------|-------------|
| `-w, --workflow` | Filter by workflow name or file |
| `-b, --branch` | Filter by branch |
| `-u, --user` | Filter by user who triggered |
| `-s, --status` | Filter: `queued`, `in_progress`, `completed`, `waiting`, `requested`, `pending` |
| `-c, --commit` | Filter by commit SHA |
| `-e, --event` | Filter by event: `push`, `pull_request`, `schedule`, etc. |
| `-a, --actor` | Filter by actor |
| `-L, --limit` | Maximum number (default: 20) |
| `--json <fields>` | JSON with: `databaseId`, `name`, `displayTitle`, `status`, `conclusion`, `workflowName`, `headBranch`, `headSha`, `event`, `createdAt`, `updatedAt`, `url` |
| `-q, --jq` | Filter JSON |

**Examples:**
```bash
# Recent runs
gh run list --limit 10

# Failed runs
gh run list --status completed --json databaseId,conclusion --jq '.[] | select(.conclusion == "failure")'

# Runs for specific workflow
gh run list --workflow ci.yml --branch main
```

---

### `gh run view`

View a workflow run.

```bash
gh run view <run-id>
gh run view              # Select interactively
```

| Flag | Description |
|------|-------------|
| `--log` | View full log |
| `--log-failed` | View log for failed steps only |
| `-j, --job` | View specific job |
| `--exit-status` | Exit with run's status code |
| `--json <fields>` | JSON output |
| `-w, --web` | Open in browser |

**Examples:**
```bash
gh run view 123456789
gh run view 123456789 --log-failed
gh run view 123456789 --job "Build"
```

---

### `gh run watch`

Watch a run until completion.

```bash
gh run watch <run-id>
gh run watch             # Watch most recent
```

| Flag | Description |
|------|-------------|
| `-i, --interval` | Refresh interval in seconds |
| `--exit-status` | Exit with run's status code |

**Examples:**
```bash
# Watch and fail if run fails
gh run watch --exit-status

# Watch specific run
gh run watch 123456789
```

---

### `gh run rerun`

Rerun a workflow run.

```bash
gh run rerun <run-id>
```

| Flag | Description |
|------|-------------|
| `--failed` | Only rerun failed jobs |
| `-j, --job` | Rerun specific job |
| `-d, --debug` | Enable debug logging |

**Examples:**
```bash
gh run rerun 123456789
gh run rerun 123456789 --failed
gh run rerun 123456789 --debug
```

---

### `gh run cancel`

Cancel a workflow run.

```bash
gh run cancel <run-id>
```

---

### `gh run download`

Download artifacts from a run.

```bash
gh run download <run-id>
```

| Flag | Description |
|------|-------------|
| `-n, --name` | Artifact name pattern |
| `-D, --dir` | Download directory |
| `-p, --pattern` | Glob pattern for artifact names |

**Examples:**
```bash
gh run download 123456789
gh run download 123456789 --name "build-*" --dir ./artifacts
```

---

### `gh run delete`

Delete a workflow run.

```bash
gh run delete <run-id>
```

---

## Workflows

### `gh workflow list`

List workflows in the repository.

```bash
gh workflow list
```

| Flag | Description |
|------|-------------|
| `-a, --all` | Include disabled workflows |
| `-L, --limit` | Maximum number |
| `--json <fields>` | JSON with: `id`, `name`, `path`, `state` |
| `-q, --jq` | Filter JSON |

---

### `gh workflow view`

View workflow details.

```bash
gh workflow view <workflow-id|name|file>
```

| Flag | Description |
|------|-------------|
| `-r, --ref` | Branch/tag for workflow file |
| `-w, --web` | Open in browser |
| `-y, --yaml` | View workflow YAML |

**Examples:**
```bash
gh workflow view ci.yml
gh workflow view ci.yml --yaml
```

---

### `gh workflow run`

Manually trigger a workflow.

```bash
gh workflow run <workflow>
gh workflow run <workflow> --ref <branch>
```

| Flag | Description |
|------|-------------|
| `-r, --ref` | Branch or tag |
| `-F, --field` | Input field: `key=value` (string) |
| `-f, --raw-field` | Input field: `key=value` (no JSON parsing) |
| `--json` | JSON input from stdin |

**Examples:**
```bash
# Trigger on branch
gh workflow run deploy.yml --ref main

# With inputs
gh workflow run deploy.yml -F environment=production -F version=1.2.3

# From JSON
echo '{"environment":"staging"}' | gh workflow run deploy.yml --json
```

---

### `gh workflow enable`

Enable a workflow.

```bash
gh workflow enable <workflow>
```

---

### `gh workflow disable`

Disable a workflow.

```bash
gh workflow disable <workflow>
```

---

## Cache Management

### `gh cache list`

List Actions caches.

```bash
gh cache list
```

| Flag | Description |
|------|-------------|
| `-k, --key` | Filter by key prefix |
| `-B, --ref` | Filter by ref |
| `-L, --limit` | Maximum number |
| `-O, --order` | Order: `last_accessed_at`, `size_in_bytes` |
| `-S, --sort` | Sort: `asc`, `desc` |
| `--json <fields>` | JSON output |

---

### `gh cache delete`

Delete Actions caches.

```bash
gh cache delete <cache-id>
gh cache delete --all
```

| Flag | Description |
|------|-------------|
| `-a, --all` | Delete all caches |
| `-k, --key` | Delete by key prefix |
| `-B, --ref` | Delete by ref |

---

## Common Workflows

### Wait for CI on PR

```bash
# Get run ID for current PR/branch
RUN_ID=$(gh run list --branch $(git branch --show-current) --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch $RUN_ID --exit-status
```

### Rerun failed jobs

```bash
gh run rerun --failed
```

### Trigger deploy workflow

```bash
gh workflow run deploy.yml -F environment=production -F version=$(git describe --tags)
```

### View failed step logs

```bash
gh run view --log-failed
```

### Download latest artifact

```bash
RUN_ID=$(gh run list --workflow build.yml --status completed --limit 1 --json databaseId --jq '.[0].databaseId')
gh run download $RUN_ID --name build-artifact
```

### Clear all caches

```bash
gh cache delete --all
```
