# Housekeeping Reference

Extended reference documentation for `agent-ops-housekeeping` skill.

---

## Operations (File-Based — Default)

| Operation | How to Do It |
|-----------|--------------|
| List done issues | Search `.agent/issues/*.md` for `status: done` |
| List by priority | Read `.agent/issues/{priority}.md` directly |
| Summary stats | Count issues in each priority file |

### Git Health Commands

```bash
git status --porcelain | wc -l    # Uncommitted changes
git ls-files --others --exclude-standard  # Untracked files
git branch -a --format='%(refname:short) %(committerdate:relative)'  # Stale branches
```

## CLI Integration (when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`:

| Operation | CLI Command |
|-----------|-------------|
| List done issues | `aoc issues list --status done` |
| List by priority | `aoc issues list --priority critical` |
| Summary stats | `aoc issues summary` |

---

## File Splitting (when files exceed 100K)

**Split procedure:**
1. Detect oversized file (> 100KB)
2. Create numbered files: `{filename}-1.md`, `{filename}-2.md`
3. **CRITICAL: Keep OLDEST in numbered files, NEWEST in main file**
4. Move oldest issues until main file < 100K

**Naming:**
```
backlog.md      # NEWEST issues (active)
backlog-1.md    # OLDER issues (first split)
backlog-2.md    # OLDEST issues (second split)
```

---

## File Compaction (after archival)

**Trigger:** Combined size < 80K after archiving

**Procedure:**
1. Merge from highest-numbered file first
2. Maintain date ordering
3. Delete empty split files

---

## Schema Validation

**Required fields:** `id`, `type`, `priority`, `title`, `status`

**ID format:** `{TYPE}-{NNNN}@{HHHHHH}`

**Auto-fixable issues:**
| Issue | Fix |
|-------|-----|
| Missing `id` | Generate new ID |
| Missing `status` | Add `status: open` |
| Wrong priority file | Move to correct file |

---

## Clutter Detection Targets

- Root markdown files (not README/LICENSE/CHANGELOG)
- `*-summary.md`, `*-notes.md`, `*-draft.md` outside `.agent/docs/`
- Empty files (< 10 lines)
- Orphaned specs in `.agent/issues/references/`

---

## Gitignore Audit Checklist

```gitignore
# Dependencies
node_modules/
.venv/
__pycache__/

# Build
dist/
build/
out/

# IDE
.idea/
.vscode/settings.json

# Environment
.env
.env.local

# Caches
.cache/
coverage/
```

---

## State File Health Checks

- Required files: constitution.md, memory.md, focus.md, baseline.md
- Corrupted YAML frontmatter
- Orphaned issue references
- Split file sequence integrity
- Counter drift

---

## Invocation Modes

### Full Sweep
```
/agent-housekeeping
```

### Dry-Run
```
/agent-housekeeping --dry-run
```

### Targeted
```
/agent-housekeeping issues     # Archival
/agent-housekeeping triage     # Backlog
/agent-housekeeping validate   # Schema
/agent-housekeeping clutter    # Clutter
/agent-housekeeping git        # Git health
/agent-housekeeping state      # State files
```

### Auto-Fix
```
/agent-housekeeping --fix
```

---

## Output Format Example

```
🧹 Housekeeping Report

## Issues Archived ⚡
✅ Archived 3 issues to history.md

## File Management
📦 Split: backlog.md → backlog-1.md

## Schema Validation
✅ 12 valid, 1 auto-fixed

## Summary
- Archived: 3 issues
- Auto-fixed: 1 issue
```
