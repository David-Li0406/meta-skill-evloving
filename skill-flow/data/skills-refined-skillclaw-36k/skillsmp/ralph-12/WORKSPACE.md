# Ralph Workspace Isolation

Ralph is project/workspace-specific. Each project has its own:
- Analysis cache
- Guardrails (accumulated)
- Task history
- Memory context

## Workspace Detection

```bash
# Find project root (git root or directory with package.json/go.mod/etc.)
get_project_root() {
  # Try git root first
  git rev-parse --show-toplevel 2>/dev/null && return

  # Fall back to marker files
  local dir="$PWD"
  while [ "$dir" != "/" ]; do
    for marker in package.json go.mod pyproject.toml Cargo.toml; do
      [ -f "$dir/$marker" ] && echo "$dir" && return
    done
    dir="$(dirname "$dir")"
  done

  # Default to current directory
  echo "$PWD"
}

# Get project identifier (for memory tagging)
get_project_id() {
  local root=$(get_project_root)
  local name=$(basename "$root")
  local hash=$(echo "$root" | md5sum | cut -c1-8)
  echo "${name}-${hash}"
}
```

## Project Structure

```
my-project/                    ← Project root
├── .ralph/                    ← Ralph workspace (project-specific)
│   ├── analysis-meta.json     ← Project analysis cache
│   ├── project-context.md     ← Cached base analysis
│   ├── goal-context.md        ← Current goal context
│   ├── guardrails.md          ← Accumulated guardrails
│   ├── task.md                ← Current tasks
│   ├── prompt.md              ← Static prompt
│   ├── history/               ← Past Ralph runs
│   │   ├── 2026-01-20-auth-fix.md
│   │   └── 2026-01-21-rate-limit.md
│   └── activity.log           ← Current run log
├── src/
├── tests/
└── package.json
```

## analysis-meta.json (Project-Specific)

```json
{
  "version": "1.0",
  "workspace": {
    "projectId": "my-app-a1b2c3d4",
    "projectName": "my-app",
    "projectRoot": "/Users/dev/projects/my-app",
    "detectedAt": "2026-01-20T10:00:00Z"
  },
  "analysis": {
    "created": "2026-01-20T10:00:00Z",
    "lastUpdated": "2026-01-22T15:30:00Z",
    "packageJsonHash": "abc123",
    "stack": "Next.js + Prisma + TypeScript"
  },
  "runs": [
    {
      "goal": "fix auth bug",
      "date": "2026-01-20T10:00:00Z",
      "tasksCompleted": 4,
      "guardrailsLearned": 2
    },
    {
      "goal": "add rate limiting",
      "date": "2026-01-21T14:00:00Z",
      "tasksCompleted": 3,
      "guardrailsLearned": 1
    }
  ],
  "guardrails": {
    "fromProject": 3,
    "fromMemory": 2,
    "learned": 3
  }
}
```

---

## Memory Integration (Project-Tagged)

### Storing Learnings

When `/ralph summary` stores learnings, tag with project:

```bash
cd $CLAUDE_PROJECT_DIR/opc && PYTHONPATH=. uv run python scripts/core/store_learning.py \
  --session-id "ralph-$(get_project_id)-$(date +%s)" \
  --type WORKING_SOLUTION \
  --content "{guardrail content}" \
  --context "Project: {project_name}, Goal: {goal}" \
  --tags "ralph,{project_name},{goal_keywords}" \
  --confidence medium
```

### Recalling Learnings

When setting up Ralph, recall project-specific learnings:

```bash
# Project-specific recall
cd $CLAUDE_PROJECT_DIR/opc && PYTHONPATH=. uv run python scripts/core/recall_learnings.py \
  --query "{project_name} {goal}" --k 5

# Will match learnings tagged with this project
```

---

## Guardrails Isolation

Guardrails are stored in `.ralph/guardrails.md` (project root):

```markdown
# Guardrails for my-app

Project: my-app
Root: /Users/dev/projects/my-app

## Project Patterns
{detected from this project's codebase}

## From Memory
{learnings tagged with this project}

## Learned from Previous Runs

### Run: fix auth bug (2026-01-20)
- Always invalidate tokens on password change
- Check passwordChangedAt before token refresh

### Run: add rate limiting (2026-01-21)
- Use Redis for rate limit state (not memory)
- Rate limit key format: `ratelimit:{userId}:{endpoint}`

---

## Learned This Run
{current run guardrails}
```

---

## History Preservation

After each Ralph run, archive the task file:

```bash
# Archive completed run
archive_ralph_run() {
  local goal="$1"
  local date=$(date +%Y-%m-%d)
  local slug=$(echo "$goal" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | cut -c1-30)

  mkdir -p .ralph/history
  cp .ralph/task.md ".ralph/history/${date}-${slug}.md"

  # Update analysis-meta.json with run info
  # ...
}
```

History allows:
- See what Ralph has done on this project
- Reference past approaches
- Track guardrails origin

---

## Cross-Project Isolation

Each project is fully isolated:

```
~/projects/
├── app-a/
│   └── .ralph/          ← app-a's Ralph workspace
│       ├── guardrails.md   (app-a specific)
│       └── analysis-meta.json
│
├── app-b/
│   └── .ralph/          ← app-b's Ralph workspace
│       ├── guardrails.md   (app-b specific)
│       └── analysis-meta.json
│
└── app-c/
    └── .ralph/          ← app-c's Ralph workspace
        └── ...
```

**No cross-contamination:**
- Guardrails from app-a don't affect app-b
- Analysis cache is per-project
- Memory learnings tagged with project ID

---

## Clorch Integration

When Clorch runs `/ralph`:

1. **Detect workspace**
   ```bash
   PROJECT_ROOT=$(get_project_root)
   PROJECT_ID=$(get_project_id)
   RALPH_DIR="$PROJECT_ROOT/.ralph"
   ```

2. **Check for existing Ralph workspace**
   ```bash
   if [ -d "$RALPH_DIR" ]; then
     # Existing workspace - incremental update
     echo "Found Ralph workspace for $(basename $PROJECT_ROOT)"
   else
     # New workspace - full setup
     mkdir -p "$RALPH_DIR/history"
   fi
   ```

3. **Load project-specific context**
   - Read existing guardrails
   - Check analysis cache freshness
   - Recall project-tagged memories

4. **Store project-specific outputs**
   - All files go to `$RALPH_DIR/`
   - Learnings tagged with `$PROJECT_ID`

---

## Workspace Commands

```bash
# Check Ralph workspace status
/ralph workspace

# Output:
# Ralph Workspace: my-app
# Root: /Users/dev/projects/my-app
# Runs: 3
# Guardrails: 8 (3 project, 2 memory, 3 learned)
# Last run: 2026-01-21 (add rate limiting)

# Clear workspace (fresh start)
/ralph workspace --clear

# Export workspace (for sharing)
/ralph workspace --export
```

---

## Environment Variables

Ralph respects these environment variables:

| Variable | Purpose | Default |
|----------|---------|---------|
| `RALPH_DIR` | Override .ralph location | `{project_root}/.ralph` |
| `RALPH_PROJECT_ID` | Override project ID | Auto-detected |
| `RALPH_NO_CACHE` | Disable analysis cache | `false` |
| `RALPH_NO_MEMORY` | Disable memory integration | `false` |
