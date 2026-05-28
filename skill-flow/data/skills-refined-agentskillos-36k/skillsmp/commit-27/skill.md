---
name: commit
description: Analyze changes and create modular, conventional commits with clear messages
disable-model-invocation: true
argument-hint: [--staged | --all]
allowed-tools: Read, Bash
---

# Commit Skill

Analyze code changes, group them into logical commits, and create conventional commit messages with clear subjects and informative bodies.

---

## Pre-Flight Check

Verify git repository and current state:

```bash
git rev-parse --is-inside-work-tree 2>/dev/null && echo "Git repo: yes" || echo "Git repo: NO"
git status --porcelain | head -1 | grep -q . && echo "Changes: yes" || echo "Changes: NO"
```

**If not a git repository:** Inform user and exit.
**If no changes:** Inform user "Working tree clean. Nothing to commit." and exit.

---

## Phase 1: Gather Changes

### Step 1.1: Assess Current State

```bash
# Overview
git status --short

# Staged changes
git diff --cached --stat

# Unstaged changes
git diff --stat

# Untracked files
git ls-files --others --exclude-standard
```

### Step 1.2: Get Detailed Diffs

```bash
# Staged diff (always needed)
git diff --cached

# Unstaged diff (if --all flag or user wants to include)
git diff
```

### Step 1.3: Build File List

For each changed file, capture:
- File path
- Change type (A=added, M=modified, D=deleted, R=renamed)
- Staged vs unstaged
- Lines added/removed

---

## Phase 2: Analyze and Group Changes

### Grouping Priority

| Priority | Criterion | Example |
|----------|-----------|---------|
| 1 | Feature cohesion | All files for "add user auth" |
| 2 | Directory scope | All changes in `auth/` module |
| 3 | Change type | Tests, docs, configs separate |
| 4 | Dependency order | Interface before implementation |

### Commit Type Detection

| Signal | Type | Example |
|--------|------|---------|
| New functionality | `feat` | `feat(auth): add OAuth2 login` |
| Bug fix, error correction | `fix` | `fix(api): handle null response` |
| `.md`, `README`, `docs/` | `docs` | `docs: update install guide` |
| Test files (`.test.ts`, `_test.go`, `spec.`) | `test` | `test(auth): add login tests` |
| `package.json`, `Cargo.toml`, build configs | `build` | `build: upgrade to Node 20` |
| `.github/workflows/`, `Jenkinsfile`, CI configs | `ci` | `ci: add GitHub Actions` |
| Formatting, whitespace only | `style` | `style: apply prettier` |
| Restructure without behavior change | `refactor` | `refactor: extract helper` |
| Performance improvement | `perf` | `perf: add query index` |
| `.gitignore`, tooling, maintenance | `chore` | `chore: update gitignore` |

### Grouping Rules

1. **Atomic commits** - Each commit = one logical change
2. **Self-contained** - Commit should not break the build
3. **Reviewable** - Changes understandable in isolation

### Grouping Decisions

| Scenario | Decision |
|----------|----------|
| Feature + its tests | **One commit** - tests are part of feature |
| Feature + unrelated fix | **Two commits** - separate concerns |
| Refactor + dependent feature | **Two commits** - refactor first |
| Multiple unrelated fixes | **Multiple commits** - one per fix |
| Formatting + logic changes | **Two commits** - style first |

---

## Phase 3: Present Commit Plan

### Commit Message Format

**Subject line:**
- Format: `type(scope): description`
- Max 72 characters (aim for 50)
- Imperative mood ("add" not "added")
- No period at end
- Capitalize first letter after colon

**Body:**
- Blank line after subject
- Wrap at 72 characters
- Explain WHY, not just WHAT
- Include context not obvious from diff
- Reference issues if applicable (`Refs: #123`)
- **NEVER add Co-Authored-By tags for AI/Claude** - only human co-authors

### Output Format

Present plan to user:

```markdown
# Commit Plan

## Summary
- Commits proposed: [N]
- Files to commit: [N]
- Total: +[N] / -[N] lines

---

## Commit 1 of N

**Message:**
```
type(scope): subject line here

Body explaining why this change was made.
Context that won't be obvious later.

Refs: #123
```

**Files:**
| File | Change | Lines |
|------|--------|-------|
| path/to/file.ts | Modified | +45, -12 |

---

## Commit 2 of N
[...]

---

**Proceed?** [Y/n/edit]
```

---

## GATE: User Approval

**STOP and wait for explicit user confirmation before executing any commits.**

| Response | Action |
|----------|--------|
| "Y" / "yes" / "proceed" | Execute commits |
| "n" / "no" / "abort" | Cancel, no changes made |
| "edit" | Ask what to modify, re-present plan |
| Specific feedback | Incorporate changes, re-present |

---

## Phase 4: Execute Commits

### For Each Planned Commit

**Step 4.1: Stage files**
```bash
git add path/to/file1.ts path/to/file2.ts
```

**Step 4.2: Create commit with HEREDOC**
```bash
git commit -m "$(cat <<'EOF'
type(scope): subject line

Body explaining the change.
Why this was needed.

Refs: #123
EOF
)"
```

**Step 4.3: Verify**
```bash
git log -1 --oneline
```

### After All Commits

Report summary:

```markdown
# Commits Created

| # | Hash | Message |
|---|------|---------|
| 1 | abc1234 | feat(auth): add OAuth2 login |
| 2 | def5678 | test(auth): add OAuth2 tests |

**Remaining unstaged:** [N files]
**Ready to push:** `git push`
```

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "not a git repository" | Not in git repo | Inform user, exit |
| "nothing to commit" | No changes | Inform user, exit gracefully |
| "pre-commit hook failed" | Hook rejected | Show hook output, suggest fixes |
| "merge conflict" | Unresolved conflicts | List files, abort |
| "pathspec did not match" | File not found | Re-gather changes |

### Recovery

If commit fails mid-execution:
1. Report which commits succeeded (with hashes)
2. Report which commit failed and why
3. Remaining files stay in their staged/unstaged state
4. Suggest: "Fix the issue and run `/commit` again"

---

## Usage

```
/commit              # Analyze all changes, propose commits
/commit --staged     # Only commit currently staged changes
/commit --all        # Include untracked files
```

### Examples

**Mixed feature and fix:**
```
$ /commit
# Proposes:
# 1. feat(search): add fuzzy matching
# 2. fix(api): handle timeout errors
```

**Single atomic change:**
```
$ /commit --staged
# Proposes:
# 1. refactor(utils): extract date formatter
```
