---
name: Session Management
description: This skill should be used when the user asks to "resume session", "save state", "restore context", "view session history", "create checkpoint", or when the /resume command is invoked. Provides session state tracking, automatic checkpointing, and seamless session resumption across Claude Code sessions.
version: 1.0.0
---

# Session Management Skill

## Purpose

Track session state across Claude Code sessions to enable seamless work resumption. Automatically capture edited files, todos, phase progress, and plan state. Create checkpoints at regular intervals and restore full context when returning to a project.

## Core Concepts

### Session State

A session state snapshot includes:
- **Timestamp** - When the state was captured
- **Edited files** - Files modified during session (from git)
- **Todos** - Current task list and completion status
- **Phase context** - Current phase name and completion percentage
- **Plan state** - Active plan file and task progress (if in plan mode)
- **Chunk context** - Current chunk being worked on
- **Session ID** - Unique identifier for this session

### Session History

Maintain a rolling history of the last 30 sessions with:
- Session ID and timestamp
- Duration and activity summary
- Files edited count
- Phase progress made
- Completion checkmarks

### Checkpoint Strategies

Three checkpoint triggers:
1. **Automatic** - Every 15 minutes via context-tracker agent
2. **Manual** - User-initiated with explicit save command
3. **Event-driven** - On phase completion, Stop hook, session end

## When to Use

Use session management when:
- User explicitly requests state save or restore with /resume
- SessionStart hook triggers (auto-load previous context)
- Stop hook triggers (auto-save current state)
- User asks about "last session", "what was I working on", "session history"
- Switching between multiple projects
- Long-running work spanning multiple Claude Code sessions

## State Capture Process

### Step 1: Identify Edited Files

Extract files modified since last checkpoint using git:

```bash
# Files with uncommitted changes
git diff --name-only HEAD

# Files in staging area
git diff --name-only --cached

# Untracked files
git ls-files --others --exclude-standard

# Combine and deduplicate
{
  git diff --name-only HEAD
  git diff --name-only --cached
  git ls-files --others --exclude-standard
} | sort -u > .claude/.last-edited-files.txt
```

**Limit to relevant files:**
- Exclude node_modules, target, venv, build artifacts
- Limit to 50 most recently modified files
- Store full paths relative to project root

### Step 2: Capture Todo State

Read current todo list if present:

```bash
# Extract todos from context (if accessible)
# This is typically managed by Claude Code's todo system
# Store in session state as JSON array

TODO_STATE=$(cat <<'EOF'
{
  "todos": [
    {
      "content": "Implement user authentication",
      "status": "in_progress",
      "activeForm": "Implementing authentication"
    },
    {
      "content": "Write tests for auth module",
      "status": "pending",
      "activeForm": "Writing auth tests"
    }
  ],
  "completion_percentage": 45
}
EOF
)
```

**Include:**
- All todos with current status (pending, in_progress, completed)
- Overall completion percentage
- Most recent active task

### Step 3: Capture Phase Context

Determine current phase from chunks or plan:

```bash
# Read current chunk if exists
if [ -f ".claude/.current-chunk.json" ]; then
  CURRENT_PHASE=$(jq -r '.phase_name' .claude/.current-chunk.json)
  PHASE_COMPLETION=$(jq -r '.completion' .claude/.current-chunk.json)
else
  CURRENT_PHASE="unknown"
  PHASE_COMPLETION=0
fi
```

**Store:**
- Phase name (e.g., "Phase 3: API Integration")
- Completion percentage (0-100)
- Phase description or goal
- Chunk ID if chunked workflow

### Step 4: Capture Plan State

If plan mode is active, capture plan progress:

```bash
# Check for active plan
PLAN_DIR="/root/.claude/plans"
if [ -d "$PLAN_DIR" ]; then
  # Find most recent plan file
  PLAN_FILE=$(ls -t "$PLAN_DIR"/*.md 2>/dev/null | head -1)

  if [ -n "$PLAN_FILE" ]; then
    PLAN_NAME=$(basename "$PLAN_FILE" .md)
    # Extract task completion from plan file
    TOTAL_TASKS=$(grep -c '^- \[' "$PLAN_FILE" || echo 0)
    COMPLETED_TASKS=$(grep -c '^- \[x\]' "$PLAN_FILE" || echo 0)
    PLAN_PROGRESS=$((COMPLETED_TASKS * 100 / TOTAL_TASKS))
  fi
fi
```

**Include:**
- Plan file name
- Total tasks vs completed tasks
- Plan progress percentage
- Last modified timestamp

### Step 5: Generate Session State JSON

Create `.claude/.project-state.json`:

```json
{
  "session_id": "session_2026-01-22_15-30",
  "timestamp": "2026-01-22T15:30:00Z",
  "project_root": "/home/ubuntu/qenex",
  "edited_files": [
    "src/api/auth.py",
    "tests/test_auth.py",
    "README.md"
  ],
  "todos": [
    {
      "content": "Implement user authentication",
      "status": "in_progress",
      "activeForm": "Implementing authentication"
    }
  ],
  "phase": {
    "name": "Phase 3: API Integration",
    "completion": 65,
    "chunk_id": "chunk_api_auth"
  },
  "plan": {
    "file": "joyful-juggling-scone.md",
    "total_tasks": 24,
    "completed_tasks": 16,
    "progress": 67
  },
  "session_duration_minutes": 45,
  "checkpoint_reason": "automatic"
}
```

**Write atomically:**
```bash
# Write to temp file, then move
echo "$STATE_JSON" > .claude/.project-state.json.tmp
mv .claude/.project-state.json.tmp .claude/.project-state.json
```

## Session History Management

### Append to History

Add current session to `.claude/.session-history.json`:

```bash
# Read existing history
HISTORY=$(cat .claude/.session-history.json 2>/dev/null || echo "[]")

# Create new entry
NEW_ENTRY=$(cat <<EOF
{
  "session_id": "session_2026-01-22_15-30",
  "timestamp": "2026-01-22T15:30:00Z",
  "duration_minutes": 45,
  "edited_files_count": 3,
  "phase": "Phase 3: API Integration",
  "phase_progress": 65,
  "todos_completed": 2,
  "checkpoint_reason": "Stop hook"
}
EOF
)

# Append to history array (keeping last 30)
echo "$HISTORY" | jq ". += [$NEW_ENTRY] | .[-30:]" > \
  .claude/.session-history.json.tmp
mv .claude/.session-history.json.tmp .claude/.session-history.json
```

### Session History Format

```json
[
  {
    "session_id": "session_2026-01-22_15-30",
    "timestamp": "2026-01-22T15:30:00Z",
    "duration_minutes": 45,
    "edited_files_count": 3,
    "phase": "Phase 3: API Integration",
    "phase_progress": 65,
    "todos_completed": 2,
    "checkpoint_reason": "Stop hook"
  },
  {
    "session_id": "session_2026-01-22_10-00",
    "timestamp": "2026-01-22T10:00:00Z",
    "duration_minutes": 120,
    "edited_files_count": 8,
    "phase": "Phase 2: Database Setup",
    "phase_progress": 100,
    "todos_completed": 5,
    "checkpoint_reason": "phase_complete"
  }
]
```

**Keep last 30 sessions** - Rotate older entries automatically

## Session Restoration Process

### Load Previous State

When user invokes /resume or SessionStart hook triggers:

```bash
# Check if state file exists
if [ ! -f ".claude/.project-state.json" ]; then
  echo "No previous session found"
  exit 0
fi

# Read state
STATE=$(cat .claude/.project-state.json)

# Extract key information
SESSION_ID=$(echo "$STATE" | jq -r '.session_id')
TIMESTAMP=$(echo "$STATE" | jq -r '.timestamp')
EDITED_FILES=$(echo "$STATE" | jq -r '.edited_files[]')
CURRENT_PHASE=$(echo "$STATE" | jq -r '.phase.name')
PHASE_COMPLETION=$(echo "$STATE" | jq -r '.phase.completion')

# Calculate session age
LAST_SESSION=$(date -d "$TIMESTAMP" +%s)
NOW=$(date +%s)
AGE_SECONDS=$((NOW - LAST_SESSION))
AGE_HOURS=$((AGE_SECONDS / 3600))
```

### Display Resume Prompt

Format session context for user:

```
═══════════════════════════════════════════════
  Resuming Project: QENEX Trading Platform
═══════════════════════════════════════════════

Last session: 2 hours ago
Session ID: session_2026-01-22_15-30
Duration: 45 minutes

Phase: Phase 3: API Integration (65% complete)
Files edited:
  • src/api/auth.py
  • tests/test_auth.py
  • README.md

Active todos:
  ⏳ Implement user authentication (in progress)
  ⏳ Write tests for auth module (pending)

Plan: joyful-juggling-scone.md (67% complete - 16/24 tasks)

───────────────────────────────────────────────

To restore full context:
  /resume              - Load all files and context
  /resume --files      - Load edited files only
  /resume --history    - View session history

Continue where you left off!
```

### Auto-Load Files

When /resume is invoked, automatically load recently edited files:

```bash
# Read edited files from state
EDITED_FILES=$(jq -r '.edited_files[]' .claude/.project-state.json)

# Load top N files (configurable, default 5)
echo "$EDITED_FILES" | head -5 | while read -r file; do
  if [ -f "$file" ]; then
    echo "Loading: $file"
    # Claude Code will read these files
  fi
done
```

**Load strategy:**
- Prioritize most recently edited files
- Load max 5 files automatically (user configurable)
- Skip files that no longer exist
- Warn about uncommitted changes

## Integration with Other Components

### Hooks

**SessionStart hook** - Automatically show resume prompt:
```bash
# Check for previous state
if [ -f ".claude/.project-state.json" ]; then
  # Display resume information
  echo "Previous session detected. Type /resume to restore context."
fi
```

**Stop hook** - Automatically save state:
```bash
# Capture current state
# Update .project-state.json
# Append to session history
```

### Commands

**`/resume` command** - Restore session context:
- Read `.project-state.json`
- Display session summary
- Auto-load edited files
- Restore chunk/phase context

**`/context-summary` command** - Show current session:
- Display session age
- Show edited files count
- Current phase and progress

### Agents

**`context-tracker` agent** - Autonomous checkpointing:
- Runs every 15 minutes
- Captures state automatically
- Updates session history
- Monitors for significant changes

## Checkpoint Configuration

Configure checkpoint behavior in `.claude/project-context.local.md`:

```yaml
---
# Session management
auto_resume_on_start: true
save_state_on_stop: true
max_session_history: 30
checkpoint_interval: 15  # minutes

# Resume behavior
auto_load_files_on_resume: true
max_auto_load_files: 5
show_session_age_warning: true
stale_session_threshold_hours: 24
---
```

## Performance Considerations

**State file size:**
- Target: <10 KB per state file
- Session history: <50 KB for 30 sessions
- Limit edited files to 50 most recent
- Truncate long file paths if needed

**Save operations:**
- Atomic writes (temp file + move)
- Backup previous state before overwrite
- Validate JSON before writing
- Handle permission errors gracefully

## Error Handling

**Missing state files:**
```bash
if [ ! -f ".claude/.project-state.json" ]; then
  echo "No previous session found. This is your first session."
  exit 0
fi
```

**Corrupted state:**
```bash
if ! jq '.' .claude/.project-state.json >/dev/null 2>&1; then
  echo "Warning: Session state corrupted. Using backup if available."
  if [ -f ".claude/.project-state.json.bak" ]; then
    cp .claude/.project-state.json.bak .claude/.project-state.json
  fi
fi
```

**Git unavailable:**
```bash
if ! command -v git &>/dev/null; then
  echo "Warning: git not found. Skipping file tracking."
  EDITED_FILES=[]
else
  EDITED_FILES=$(git diff --name-only HEAD)
fi
```

## Additional Resources

### Reference Files

For detailed implementation guidance:
- **`references/state-format.md`** - Complete state JSON schema
- **`references/history-management.md`** - Session history rotation and queries
- **`references/restoration-strategies.md`** - Context loading approaches

### Example Files

Working examples in `examples/`:
- **`sample-state.json`** - Complete session state example
- **`session-history-example.json`** - Sample session history

### Utility Scripts

Helper scripts in `scripts/`:
- **`save-state.sh`** - Capture current session state (implemented in hooks/)
- **`restore-state.sh`** - Load previous session context
- **`session-history.py`** - Query and manage session history
