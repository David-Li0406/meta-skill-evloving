# Divergent Changes

## Table of Contents
- [What Are Divergent Changes?](#what-are-divergent-changes)
- [Identifying Divergent Changes](#identifying-divergent-changes)
- [Common Causes](#common-causes)
- [Resolution Strategies](#resolution-strategies)
- [Prevention](#prevention)

---

## What Are Divergent Changes?

A divergent change occurs when **multiple visible commits share the same change ID**. In logs, they appear with:
- A change offset suffix (e.g., `mzvwutvl/0`, `mzvwutvl/1`)
- A `divergent` label

**Key insight:** Divergence is not an error—jj continues working normally. However, you cannot reference divergent changes unambiguously by change ID alone.

---

## Identifying Divergent Changes

### Check for Divergent Commits

```bash
# View log and look for "divergent" label or /0, /1 suffixes
jj log --no-pager
```

Divergent commits appear like:
```
◆  mzvwutvl/0  user@example.com  2025-01-15  divergent
│  feat: add feature
◆  mzvwutvl/1  user@example.com  2025-01-15  divergent
│  feat: add feature (different version)
```

### Reference Divergent Commits

Since the change ID is ambiguous, use either:

1. **Commit ID** (full hash): `jj show abc123def`
2. **Change ID with offset**: `jj show mzvwutvl/0` or `jj show mzvwutvl/1`

---

## Common Causes

### 1. Concurrent Edits
Two processes modify the same change simultaneously:
- Running `jj describe` while IDE integration fetches/rebases
- Multiple terminals operating on same change

### 2. Collaborative Conflicts
Another author modifies commits in a branch you've also modified locally:
```bash
# You locally amended change xyz
jj describe -m "new message"

# Someone else also amended xyz and pushed
jj git fetch
# → Now xyz has two visible versions: yours and theirs
```

### 3. Multiple Workspaces
Operating on the same change from different workspaces of the same repository.

### 4. Hidden Commits Becoming Visible
A hidden commit reappears when:
- Someone creates descendants on your hidden commit
- You fetch from a remote that built on hidden commits
- You run `jj edit` or `jj new` on a hidden commit
- A bookmark is added to a hidden commit

---

## Resolution Strategies

### Strategy 1: Abandon Unwanted Version

**When to use:** One version is clearly obsolete or incorrect.

```bash
# First, inspect both versions
jj show mzvwutvl/0
jj show mzvwutvl/1

# Abandon the unwanted one (use commit ID or offset)
jj abandon mzvwutvl/1
```

### Strategy 2: Keep Both as Separate Changes

**When to use:** Both versions have value and should exist independently.

```bash
# Generate new change ID for one of them
jj metaedit --update-change-id mzvwutvl/1
```

This gives the second commit a fresh change ID, making both commits independent.

### Strategy 3: Combine into One

**When to use:** You want to merge content from both versions.

```bash
# Squash source into target
jj squash --from mzvwutvl/1 --into mzvwutvl/0

# The source commit is automatically abandoned
```

### Strategy 4: Leave As-Is

**When to use:** Divergence causes no immediate problems and you'll resolve later.

**Caveat:** You must use offsets or commit IDs to reference these changes until resolved.

---

## Prevention

### Single-Process Operations
Avoid running multiple jj commands simultaneously on the same repository.

### Coordinate with Collaborators
When sharing branches:
1. Communicate before force-pushing amended commits
2. Use bookmarks to track who "owns" which changes

### Prefer Rebase-Merge for PRs
Use `gh pr merge --rebase` instead of squash-merge. Squash-merge creates new commit hashes that can leave local commits orphaned (not divergent, but related cleanup issue).

### Fetch Before Major Operations
```bash
jj git fetch
jj status --no-pager
# Then proceed with edits
```
