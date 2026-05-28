# Discovery Patterns

How auto finds work within a single repo context.

## Source Priority

| Priority | Source | Rationale |
|----------|--------|-----------|
| 1 | Linear P1 issues | Explicit high priority |
| 2 | Linear P2 issues | Explicit medium priority |
| 3 | Uncommitted work | Finish what's started |
| 4 | CLAUDE.md TODOs | Documented intentions |
| 5 | Stale branches | Abandoned work to revive or clean |
| 6 | Linear P3+ issues | Backlog items |

## Linear Discovery

```bash
# Get team from .loop.json
TEAM=$(jq -r '.project.team' .loop.json)

# Fetch ready issues
linear issue list --team $TEAM --state "Ready" --json --quiet

# Output structure
{
  "issues": [
    {
      "identifier": "ARB-45",
      "title": "Add notification preferences",
      "priority": 1,
      "state": "Ready",
      "assignee": "luke",
      "labels": ["feature", "notifications"]
    }
  ]
}
```

## CLAUDE.md TODO Discovery

```bash
# Find actionable items
grep -rn "TODO\|FIXME\|HACK" . \
  --include="*.md" \
  --include="CLAUDE.md" \
  --include="AGENTS.md" \
  | grep -v node_modules \
  | grep -v ".git"

# Parse into work items
# Format: file:line:content
# Extract: file, line, action type, description
```

### TODO Classification

| Pattern | Priority | Action |
|---------|----------|--------|
| `TODO(P1):` | 1 | Immediate |
| `FIXME:` | 2 | Bug fix needed |
| `HACK:` | 3 | Technical debt |
| `TODO:` | 4 | General improvement |
| `NOTE:` | - | Skip (informational) |

## Git Status Discovery

```bash
# Uncommitted changes
git status --porcelain

# Parse output
# M  = modified
# A  = added
# D  = deleted
# ?? = untracked

# Decision tree
# - Modified files → "finish this work"
# - Untracked files → "integrate or ignore"
```

## Git Branch Staleness

```bash
# Branches by last commit date
git branch -v --sort=-committerdate

# Identify stale (>7 days)
git for-each-ref --sort=-committerdate refs/heads/ \
  --format='%(refname:short) %(committerdate:relative)' \
  | while read branch date; do
    if [[ "$date" == *"weeks"* ]] || [[ "$date" == *"months"* ]]; then
      echo "STALE: $branch ($date)"
    fi
  done
```

## Git Log Learning

### Quality Patterns

```bash
# Test-to-code ratio in recent commits
git log --stat -30 | grep -E "\.(test|spec)\.(ts|tsx)" | wc -l
git log --stat -30 | grep -E "\.(ts|tsx)" | grep -v test | wc -l

# Commit message patterns
git log --format="%s" -50 | head -20

# Common prefixes
git log --format="%s" -100 | sed 's/:.*//g' | sort | uniq -c | sort -rn
# feat: 45
# fix: 23
# refactor: 12
# test: 10
```

### Trajectory Analysis

```bash
# Hot files (most changed recently)
git log --name-only -50 --format="" | sort | uniq -c | sort -rn | head -10

# Hot directories
git log --name-only -50 --format="" | xargs dirname 2>/dev/null | sort | uniq -c | sort -rn | head -10
```

### Similar Work Lookup

```bash
# Find commits related to current task
KEYWORDS="auth notification preferences"
for kw in $KEYWORDS; do
  git log --all --oneline --grep="$kw" | head -5
done

# Find files changed in those commits
COMMIT=$(git log --all --oneline --grep="$KEYWORD" -1 --format="%H")
git show --name-only $COMMIT
```

## Work Item Schema

```typescript
interface WorkItem {
  id: string;                    // Unique identifier
  source: 'linear' | 'todo' | 'git_status' | 'git_branch';
  priority: number;              // 1-10, higher = more urgent
  title: string;
  description?: string;

  // Source-specific
  linear?: {
    identifier: string;          // ARB-45
    state: string;
    labels: string[];
  };
  todo?: {
    file: string;
    line: number;
    type: 'TODO' | 'FIXME' | 'HACK';
  };
  git?: {
    branch?: string;
    files?: string[];
    last_activity?: string;
  };

  // Computed
  estimated_effort: 'small' | 'medium' | 'large';
  suggested_agent: 'copilot' | 'codex';
}
```

## Effort Estimation

| Signal | Effort | Agent |
|--------|--------|-------|
| Single file change | small | copilot |
| 2-3 files, clear scope | medium | codex |
| 4+ files or unclear | large | codex + review |
| New feature | large | codex |
| Bug fix | small-medium | codex |
| Refactor | medium-large | codex + review |
| Documentation | small | copilot |

## Discovery Output

```json
{
  "session_id": "arbor-20251222-143000-abc1",
  "repo": "arbor",
  "team": "ARB",
  "discovered_at": "2025-12-22T14:30:00Z",
  "work_items": [
    {
      "id": "linear-ARB-45",
      "source": "linear",
      "priority": 1,
      "title": "Add notification preferences",
      "linear": { "identifier": "ARB-45", "state": "Ready" },
      "estimated_effort": "medium",
      "suggested_agent": "codex"
    },
    {
      "id": "todo-convex-auth-42",
      "source": "todo",
      "priority": 4,
      "title": "Refactor useAuth hook",
      "todo": { "file": "CLAUDE.md", "line": 42, "type": "TODO" },
      "estimated_effort": "small",
      "suggested_agent": "copilot"
    }
  ],
  "git_learning": {
    "quality_patterns": ["TDD approach", "feat/fix/refactor prefixes"],
    "hot_areas": ["convex/", "packages/web/src/hooks/"],
    "velocity": "12 commits/week"
  }
}
```
