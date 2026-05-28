# Jujutsu Workflow Reference

## Table of Contents
- [Quality Gates](#quality-gates)
- [Working Copy Loop](#working-copy-loop)
- [Stack Management (Deep Edit)](#stack-management-deep-edit)
- [Non-Interactive Splitting](#non-interactive-splitting)
- [GitHub Synchronization](#github-synchronization)
- [Conflict Resolution](#conflict-resolution)
- [Safety & Recovery](#safety--recovery)

---

## Quality Gates

This project uses jj-native quality gates instead of pre-commit hooks.

### Philosophy

| Category | Trigger | Tools | Command |
|----------|---------|-------|---------|
| **A: Formatters** | Anytime, auto-fix | ruff, prettier, buf format | `jj fix` |
| **B: Verifiers** | Before push | linters, type-checkers, tests | `jj secure-push` |

### Formatter Workflow (`jj fix`)

Run frequently while coding to keep files formatted:

```bash
# Format modified files only
jj fix

# Format entire repository
jj fix-all
```

**What runs:** ruff-format, ruff-fix (isort, pyupgrade), prettier (ts/html/scss), buf format (proto)

**How it works:** Configured in `.jj/repo/config.toml` under `[fix.tools]`. Each tool reads from stdin and writes to stdout.

### Quick Quality Check (`jj quality`)

Fast sanity check without running tests:

```bash
jj quality
```

**Runs:** formatters → buf lint → pyright → eslint → prettier check

### Full Verification (`jj secure-push`)

Complete quality gate pipeline before pushing:

```bash
# Push current bookmark
jj secure-push

# Push specific bookmark
jj secure-push --bookmark my-feature

# Push all bookmarks
jj secure-push --all
```

**Pipeline order (fail-fast):**
1. `jj fix` (apply formatters)
2. buf lint, pyright, eslint, prettier check (~30s)
3. Angular production build (~60s)
4. Backend tests, frontend unit tests
5. Playwright component tests
6. E2E tests (conditional)
7. Generated code consistency check
8. Push to remote

**Exit codes:** 0 = pushed, 1 = verification failed (not pushed)

### Configuration

All aliases defined in `.jj/repo/config.toml`:

```toml
# Format modified files
[fix.tools.ruff-format]
command = ["ruff", "format", "--stdin-filename=$path", "-"]
patterns = ["glob:server/**/*.py", ...]

# Verify and push
[aliases]
secure-push = ["util", "exec", "--", "bash", "-c", "..."]
quality = ["util", "exec", "--", "bash", "-c", "..."]
fix-all = ["fix", "--include-unchanged"]
```

---

## Working Copy Loop

### State Verification

Before any task, check the working copy state:

```bash
jj status --no-pager
```

**Parsing:**
- `The working copy has no changes` → Clean slate, proceed with modifications
- `Working copy changes:` with file list → Dirty state, decide to continue or seal

### Describe-then-New Pattern

Preferred over `jj commit` for stacked workflows:

```bash
# 1. Name the current work
jj describe -m "feat: implement retry logic for API client"

# 2. Seal and create new working copy
jj new
```

**Graph transition:**
- Before: `@` (dirty, no description)
- After: New empty `@` → Parent has description

### Amending

No command needed. Simply edit files—jj auto-snapshots into `@`.

To update the message:
```bash
jj describe -m "updated message"
```

---

## Stack Management (Deep Edit)

Navigate to any commit in stack, edit it, and jj auto-rebases descendants.

### Target by Description

```bash
# Find Change ID
jj log -r 'description("Refactor")' --no-graph -T 'change_id "\n"'

# Jump to it
jj edit <change_id>
```

### Make Edits

Edit files normally. Changes auto-snapshot into the targeted commit.

### Return to Tip

```bash
jj edit <tip_bookmark_or_id>
```

### Verify Rebase Success

```bash
jj log -r '::@' --template 'change_id " " conflict "\n"'
```

If `conflict` is `true`, enter [Conflict Resolution](#conflict-resolution) for that commit.

---

## Non-Interactive Splitting

**Constraint:** `jj split` requires TUI—forbidden for agents.

### File-Level Split (squash method)

Move specific files from `@` into parent:

```bash
jj squash --into @- src/style.css
```

Result: Parent gains `style.css` changes; `@` retains only other files.

### Hunk-Level Split (construction method)

When splitting changes within a single file:

```bash
# 1. Record original commit ID
ORIG_ID=$(jj log -r @ --no-graph -T 'change_id')

# 2. Create sibling off parent
jj new @-

# 3. Write file with ONLY first change (e.g., bug fix)
# (agent writes partial content)

# 4. Describe first commit
jj describe -m "fix: resolve critical bug"

# 5. Create child for second change
jj new

# 6. Restore full content from original
jj restore --from $ORIG_ID src/main.rs

# 7. Describe second commit
jj describe -m "feat: add new feature"

# 8. Verify: diff should be empty
jj diff --from $ORIG_ID --to @

# 9. Abandon original
jj abandon $ORIG_ID
```

---

## GitHub Synchronization

### Bookmark Management

Create bookmarks for PR-ready commits:

```bash
# Naming convention: agent/task-<task_id>-<change_id_short>
jj bookmark create agent/task-101-zso -r @
```

### Pushing

```bash
# Single bookmark
jj git push --bookmark agent/task-101-zso

# All bookmarks
jj git push --all
```

### Post-Merge Sync

**Always use rebase-merge on GitHub** (`gh pr merge --rebase`), not squash-merge.

**Why rebase-merge:**
- With jj's workflow, each PR already has a single commit
- Rebase-merge preserves the commit hash, so jj recognizes the commit is now on main
- Squash-merge creates a NEW hash, leaving orphaned "zombie" commits

**After every GitHub merge:**

```bash
# 1. Fetch the merged commit
jj git fetch

# 2. Find remaining unmerged work
jj log -r 'trunk()..visible_heads()' --no-pager

# 3. Rebase remaining stack onto new main
jj rebase -s <next-unmerged-change-id> -d main

# 4. Verify the graph is clean
jj log -r '::@ | main' --no-pager
```

**Example:** Stack was A→B→C, PR for A was merged:
```bash
jj git fetch
jj rebase -s <B-change-id> -d main
# No need to abandon A—jj recognizes it's on main
```

**If squash-merge was used accidentally:**
```bash
# Find zombie commits
jj log -r 'trunk()..visible_heads()' --no-pager
# Abandon the orphaned local commit
jj abandon <zombie-change-id>
```

**Handling conflicts:** If rebase introduces conflicts, resolve them:
```bash
jj resolve --list                           # See conflicted files
jj restore --from main -- <file-path>       # Accept version from main
# Or manually edit the file to resolve
```

---

## Conflict Resolution

jj records conflicts in commits—operations don't halt.

### Identify Conflicts

```bash
jj resolve --list
```

### Resolution Protocol

1. **Read** the conflicted file
2. **Parse** markers: `<<<<<<<`, `|||||||`, `=======`, `>>>>>>>`
3. **Synthesize** correct merged content
4. **Write** clean file (no markers)

### Verify Resolution

```bash
jj status
```

Success: File no longer listed as conflicted; no `(conflict)` tag in `jj log`.

---

## Safety & Recovery

### Undo Last Operation

```bash
jj undo
```

Reverts to state before last graph-mutating command.

### Recover Abandoned Commits

```bash
# Find hidden commits
jj log --hidden -r 'all()' --limit 10

# Resurrect
jj new <lost_change_id>
```

### Find Floating Heads

```bash
jj log -r 'heads(all())'
```

Inspect and rebase valid work back onto main stack if needed.
