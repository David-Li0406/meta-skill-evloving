---
name: push-todo
description: |
  Fetch and work on coding tasks captured via voice on the Push iOS app.

  Activate this skill when the user mentions:
  - "Push tasks" or "Push notes" or "Push queue"
  - "Tasks from my phone" or "phone tasks"
  - "Voice notes I captured" or "what did I record"
  - "My voice tasks" or "voice memos"
  - Following up on "[Push]" notification
---

# Push Voice Tasks

Help the user work on coding tasks they captured via voice on their iPhone.

## Overview

Push is a voice-powered todo app. Users capture coding tasks by speaking on their phone, then work on them later in Claude Code. This skill fetches those tasks and helps complete them.

## Project Scoping (Default Behavior)

**By default, only tasks for the CURRENT PROJECT are shown** (based on git remote URL).

| Scenario | Behavior |
|----------|----------|
| In a git repo | Only shows tasks assigned to this repo |
| Not in a git repo | Shows all tasks |
| User wants all tasks | Use `--all-projects` flag |

This means running `/push-todo` in different projects shows different tasks automatically.

### IMPORTANT: No Automatic Fallback

**DO NOT automatically check other projects when there are no tasks for the current project.**

When the script returns "No active tasks for this project":
- Just tell the user: "No active tasks for this project."
- **DO NOT** automatically run `--all-projects` to check other projects
- **DO NOT** offer to check other projects unless the user explicitly asks

The user can explicitly request all projects by saying:
- "Show me tasks from all projects"
- "Check all my projects"
- "Show tasks across all projects"

When user explicitly asks for all projects, use the `--all-projects` flag.

## Architecture: Always Fresh

**Version 4.0:** This skill always fetches fresh data from Supabase. No caching.

| Step | Script | What Happens | Latency |
|------|--------|--------------|---------|
| **Session start** | `check_tasks.py` | Fetches task count from API | ~500ms |
| **User runs /push-todo** | `fetch_task.py` | Fetches fresh tasks from API | ~500ms |

This ensures you always see the latest state from the Push app.

### CLI Options
```bash
fetch_task.py [TASK_NUMBER] [--all-projects] [--pinned] [--json] [--mark-completed ID]
  TASK_NUMBER           Fetch a specific task by number (e.g., 5 or #5) - fast direct lookup
  --all-projects        Show tasks from ALL projects (not just current)
  --pinned              Only show pinned (focused) tasks
  --json                Output raw JSON format
  --mark-completed ID   Mark a task as completed by UUID
```

### Direct Task Lookup (Fast Path)

When the user specifies a task number directly (e.g., `/push-todo 5` or `/push-todo #427`):

1. **Script fetches immediately** - No project filtering, no list scanning
2. **API call goes directly** - Uses `?display_number=N` query param
3. **Returns single task** - Ready to work on instantly

This is the fastest path - use it when the user knows their task number.

## Fetching Tasks

When the user wants to see their tasks, run:

```bash
# Fetch all tasks for current project
python3 "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/fetch_task.py"

# Fetch a specific task by number (fast direct lookup)
python3 "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/fetch_task.py" 427
python3 "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/fetch_task.py" "#427"
```

Note: The script reads the API key from `~/.config/push/config` automatically.

This returns all active tasks for the current project. Present them using the **global display number** (same as shown in the Push app):

```
You have N active tasks from Push:

#427 📌 **[Summary]**
   Details: [First 200 chars of content]

#351 **[Summary]**
   Details: ...

Which task would you like to work on? (Use #N to reference, e.g., /push-todo 427)
```

**IMPORTANT:** Always reference tasks by their global number (`#427`, `#351`, etc.), never by relative position (1st, 2nd). This ensures consistency between the Push app and Claude Code.

## Starting a Task

When the user selects a task (e.g., "#427" or "work on 427"):

1. Find the task by its display number from the fetched list

2. Read the full task details from the script output

3. If project_hint is provided, look for that project's CLAUDE.md

4. Begin working on the task immediately

Note: Users reference tasks by their global number (`#427`), which maps to the task's UUID for API calls.

## Completing a Task

When the task is done, mark it complete with a summary of what was accomplished:

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/fetch_task.py" \
  --mark-completed TASK_ID \
  --completion-comment "Brief summary of work done"
```

### Automatic Completion Summary (Agent Behavior)

**You should ALWAYS include a `--completion-comment` when marking tasks complete.** This is automatic - don't ask the user, just do it. The comment appears in the Push app's timeline, helping the user remember what was done.

Write a good summary:
- **Concise**: 1-2 sentences, under 150 characters
- **Specific**: What changed (files, features, fixes)
- **Past tense**: "Added...", "Fixed...", "Updated...", "Implemented..."

**Examples:**
- "Added dark mode toggle with CSS variables"
- "Fixed race condition in sync service"
- "Refactored auth to use JWT tokens"

Confirm to the user: "Task #N marked complete in Push"

## Reviewing Tasks

When the user runs `/push-todo review`, check recent git activity against active tasks:

1. **Get recent git activity** (run in parallel):
   ```bash
   git log --oneline -5                  # Recent commits
   git diff --name-only HEAD             # Uncommitted changes
   ```

2. **Fetch active tasks**:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/fetch_task.py" --json
   ```

3. **Match semantically** - Compare commit messages and changed files against task summaries. Look for obvious matches only.

4. **Present findings**:
   ```
   Based on recent git activity, these tasks appear complete:

   #427 "Add dark mode toggle" → matches commit "Added dark mode with CSS vars"
   #351 "Fix sync race condition" → matches uncommitted changes in SyncService.swift

   Mark these as complete? (y/n)
   ```

5. **On confirmation** - Mark each with `--mark-completed` and auto-generate completion comment from the matching commit/change.

**Keep it simple:** Only match obvious semantic overlaps. Don't analyze file contents or grep the codebase - that's the main agent's job.

## Connect Mode (Doctor Flow)

When `/push-todo connect` is invoked, run a comprehensive health check. This is the ONE command users need to run - it handles everything.

### Full Doctor Flow

Execute these steps **in order**. Stop early if a critical issue needs user action.

#### Step 1: Check Plugin Version

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/connect.py" --check-version
```

> **Note:** `$CLAUDE_PLUGIN_ROOT` is set by Claude Code to the plugin's directory. Falls back to `~/.claude/skills/push-todo` for development.

**JSON Response:**
```json
{
  "status": "up_to_date" | "update_available" | "unknown",
  "local_version": "1.2.6",
  "remote_version": "1.3.0",
  "message": "Update available: 1.2.6 → 1.3.0"
}
```

**If `update_available`:**
1. Tell the user: "A new version of the Push plugin is available (1.2.6 → 1.3.0). Would you like me to update?"
2. **Wait for user confirmation** (semantic response like "yes", "sure", "go ahead")
3. If confirmed, run update:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/connect.py" --update
   ```
4. Handle update result:
   - `"status": "success"` → Continue to Step 2
   - `"status": "manual_required"` → Tell user to run the command in `"command"` field, also mention the `"hint"` for enabling auto-updates, then continue
   - `"status": "failed"` → Warn user, but continue
   - `"status": "skipped"` → Continue silently (marketplace with auto-update ON, or development installs)

**If `up_to_date` or `unknown`:** Continue silently.

#### Step 2: Validate API Key

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/connect.py" --validate-key
```

**JSON Response:**
```json
{
  "status": "valid" | "invalid" | "revoked" | "missing" | "error",
  "message": "API key is valid",
  "email": "user@example.com"
}
```

**If `missing` or `invalid` or `revoked`:**
1. Tell the user: "Your Push connection needs to be set up. I'll open a browser for Sign in with Apple."
2. Run full connect (opens browser):
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/connect.py"
   ```
3. After auth completes, continue to Step 3.

**If `valid`:** Continue to Step 3 with existing credentials.

**If `error`:** Warn user about network issue, but continue.

#### Step 3: Register Project with Keywords

1. **Read CLAUDE.md** to understand the project context

2. **Generate keywords** - Extract 5-15 relevant keywords:
   - Project name and aliases
   - Key technologies (e.g., "swift", "swiftui", "supabase")
   - Domain terms (e.g., "voice", "todo", "sync")
   - Keep keywords lowercase, comma-separated

3. **Generate description** - Concise 1-sentence (<100 chars)

4. **Run connect with generated values**:
   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/connect.py" \
     --keywords "keyword1,keyword2,keyword3" \
     --description "Short project description"
   ```

**Example for Push project:**
```bash
python3 "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/connect.py" \
  --keywords "push,voice,todo,whisper,ios,swift,swiftui,swiftdata,cloudkit,realtime,supabase" \
  --description "Voice-powered todo app for iOS with realtime sync"
```

### Why This Matters

- **Version check:** Ensures users have latest bug fixes
- **API validation:** Catches revoked keys before tasks fail
- **Keywords:** Help AI route voice tasks to the correct project

Users only need to remember one command: `/push-todo connect`

## Task Fields

Each task includes:
- `display_number`: **Global task number** (e.g., 427) - use this to reference tasks (`#427`)
- `id`: UUID for API calls (used internally for mark-completed)
- `summary`: Brief description (AI-generated from voice)
- `content`: Full normalized content from voice note
- `transcript`: Original voice transcript (if user wants raw input)
- `project_hint`: Human-readable project name (e.g., "Push", "AppleWhisper")
- `git_remote`: Normalized git remote URL for project scoping (e.g., "github.com/user/repo")
- `is_focused`: Boolean indicating if the task is pinned/focused (prioritized)
- `created_at`: When the task was captured

**Global Numbers:** Every task has a permanent `display_number` that matches the Push app. Always use `#N` format when referencing tasks.

**Pinned Tasks:** Tasks marked as pinned in the Push app will appear with a 📌 indicator and are automatically sorted to the top of the list. Use `--pinned` to filter to only pinned tasks.

## Updates

Updates are handled via the doctor flow in `/push-todo connect`.

Both curl and marketplace install use the same plugin system, so updates work identically:

| Setting | Update Method | Doctor Flow Behavior |
|---------|---------------|---------------------|
| **Auto-update ON** | Automatic at startup | Skips silently |
| **Auto-update OFF** | `claude plugin update push-todo@push-todo-cli` | Shows command + hint to enable auto-update |

> **Note:** "Development" installs (symlinks) are internal only for plugin maintainers, not a user scenario.

### Legacy Migration (Pre-1.4.0 Installs)

Users who installed before version 1.4.0 (when curl created a skill instead of a plugin) are automatically migrated:

1. User runs `/push-todo connect`
2. Connect detects "legacy" install (files in `~/.claude/skills/`)
3. Update runs NEW install.sh → installs via marketplace CLI
4. Plugin is now installed in `~/.claude/plugins/cache/`
5. **Next run:** Claude Code uses the PLUGIN, detection returns "marketplace"

Old files in `~/.claude/skills/push-todo/` become orphaned. Users see a hint to clean them up:
```bash
rm -rf ~/.claude/skills/push-todo
```

### Auto-Update Detection

The connect script reads `~/.claude/plugins/known_marketplaces.json` and checks the `autoUpdate` field. Third-party marketplaces default to auto-update OFF.

**Important:** Claude Code does NOT notify users about updates when auto-update is disabled. The doctor flow fills this gap by checking versions and guiding users to update.

**Manual update check:**
```bash
python3 "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/connect.py" --check-version
python3 "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/push-todo}/scripts/connect.py" --update
```

## Error Handling

If the API returns an error:
- Check if PUSH_API_KEY is set in ~/.config/push/config
- Suggest: "Run `/push-todo connect` to configure your Push connection"
