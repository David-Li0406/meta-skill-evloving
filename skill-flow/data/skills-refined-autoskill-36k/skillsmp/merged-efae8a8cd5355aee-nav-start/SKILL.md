---
name: nav-start
description: Load the Navigator documentation navigator to start your development session, resume work, or begin a new feature. Use this skill when the user mentions starting work, resuming after a break, or checking project status.
---

# Navigator Skill

Load the Navigator documentation navigator to start your development session with optimized context.

## When to Invoke

Invoke this skill when the user:
- Says "start my session", "begin work", "start working"
- Says "load the navigator", "show me the docs"
- Asks "what should I work on?"
- Mentions "resume work", "continue from where I left off"
- Asks about project structure or current tasks

**DO NOT invoke** if:
- User already ran `/nav:start` command in this conversation
- Navigator already loaded (check conversation history)
- User is in the middle of implementation (only invoke at session start)

## Execution Steps

### Step 1: Check Navigator Version

Check if the user is running the latest Navigator version:

```bash
# Run version checker (optional - doesn't block session start)
if [ -f "scripts/check-version.sh" ]; then
  bash scripts/check-version.sh

  # Note: Exit code 1 means update available, but don't block session
  # Exit code 0 means up to date
  # Exit code 2 means cannot check (network issue)
fi
```

**Version check behavior**:
- If an update is available: Show notification, continue session
- If up to date: Show ✅, continue session
- If cannot check: Skip silently, continue session

**Never block session start** due to version check.

### Step 1.5: Auto-Update (if enabled)

If auto_update is enabled in config AND an update is available, automatically update Navigator:

```bash
# Get the skill's base directory
SKILL_DIR="${SKILL_BASE_DIR:-$HOME/.claude/plugins/marketplaces/jitd-marketplace/skills/nav-start}"

# Run auto-updater
AUTO_UPDATE_RESULT=$(python3 "$SKILL_DIR/functions/auto_updater.py" 2>/dev/null)
AUTO_UPDATE_STATUS=$(echo "$AUTO_UPDATE_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('status',''))" 2>/dev/null)

case "$AUTO_UPDATE_STATUS" in
  "updated")
    NEW_VERSION=$(echo "$AUTO_UPDATE_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('new_version',''))" 2>/dev/null)
    REQUIRES_RESTART=$(echo "$AUTO_UPDATE_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('requires_restart', False))" 2>/dev/null)
    echo "✅ Auto-updated Navigator to v$NEW_VERSION"
    if [ "$REQUIRES_RESTART" = "True" ]; then
      echo ""
      echo "⚠️  RESTART REQUIRED"
      echo "   Claude Code caches skill paths at session start."
      echo "   Restart Claude Code to load new skills from v$NEW_VERSION."
      echo ""
    fi
    ;;
  "up-to-date")
    # Silently continue
    ;;
  "failed")
    echo "⚠️  Auto-update failed. Run 'nav-upgrade' manually if needed."
    ;;
  "disabled"|"skipped")
    # Silently continue
    ;;
esac
```

**Auto-update behavior**:
- **If updated**: Show "✅ Auto-updated to vX.Y.Z" with restart prompt
- **If up-to-date**: Continue silently
- **If failed**: Show warning "⚠️ Auto-update failed, run nav-upgrade manually"
- **If disabled/skipped**: Continue silently

**IMPORTANT**: When `requires_restart: true`, display:
```
⚠️  RESTART REQUIRED
   Claude Code caches skill paths at session start.
   Restart Claude Code to load new skills from vX.Y.Z.
```

This informs users that mid-session updates require a restart to activate new skills.

### Step 2: Check Navigator Initialization

Check if `.agent/DEVELOPMENT-README.md` exists:

```bash
if [ ! -f ".agent/DEVELOPMENT-README.md" ]; then
  echo "❌ Navigator not initialized in this project"
  echo ""
  echo "Run /nav:init to set up Navigator structure first."
  exit 1
fi
```

If not found, inform the user to run `/nav:init` first.

### Step 3: Load Documentation Navigator

Read the navigator file:

```
Read(
  file_path: ".agent/DEVELOPMENT-README.md"
)
```

This is the lightweight index (~2k tokens) that tells you:
- What documentation exists
- When to load specific docs
- Current task focus
- Project structure overview

### Step 4: Check for Active Context Marker

Check if there's an active marker from previous `/nav:compact`:

```bash
if [ -f ".agent/.context-markers/.active" ]; then
  marker_file=$(cat .agent/.context-markers/.active)
  echo "🔄 Active context marker detected!"
  echo ""
  echo "Marker: $marker_file"
  echo ""
  echo "This marker was saved during your last /nav:compact."
  echo "Load it to continue where you left off?"
  echo ""
  echo "[Y/n]:"
fi
```

If the user confirms (Y or Enter):
- Read the marker file: `Read(file_path: ".agent/.context-markers/{marker_file}")`
- Delete `.active` file: `rm .agent/.context-markers/.active`
- Show confirmation: "✅ Context restored from marker!"

If the user declines (n):
- Delete `.active` file
- Show: "Skipping marker load. You can load it later with /nav:markers"

### Step 5: Load Navigator Configuration

Read configuration:

```
Read(
  file_path: ".agent/.nav-config.json"
)
```

Parse:
- `project_management`: Which PM tool (linear, github, jira, none)
- `task_prefix`: Task ID format (TASK, GH, LIN, etc.)
- `team_chat`: Team notifications (slack, discord, none)
- `tom_features`: ToM configuration (if present, v5.0.0+)

### Step 5.1: Check Version Drift

**Check if project config version matches plugin version**:

```bash
SKILL_DIR="${SKILL_BASE_DIR:-$HOME/.claude/plugins/marketplaces/jitd-marketplace/skills/nav-start}"
DRIFT_RESULT=$(python3 "$SKILL_DIR/functions/auto_updater.py" --check-drift 2>/dev/null || echo '{"has_drift": false}')
HAS_DRIFT=$(echo "$DRIFT_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('has_drift', False))" 2>/dev/null)

if [ "$HAS_DRIFT" = "True" ]; then
  DRIFT_MSG=$(echo "$DRIFT_RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('message', ''))" 2>/dev/null)
  echo ""
  echo "⚠️  VERSION DRIFT DETECTED"
  echo "   $DRIFT_MSG"
  echo ""
fi
```

**Version drift occurs when**:
- Plugin updated but project config wasn't synced
- Manual plugin install without running nav-upgrade
- Project cloned with old config version

**Display warning if drift detected**:
```
⚠️  VERSION DRIFT DETECTED
   Project config (v5.5.0) behind plugin (v5.7.0). Run "update my CLAUDE.md" to sync.
```

This helps users understand why skills may behave unexpectedly.

### Step 5.5: Load User Profile (ToM - Bilateral Modeling) [EXECUTE]

**IMPORTANT**: This step MUST be executed, not just documented.

**Check if user profile exists**:
```bash
if [ -f ".agent/.user-profile.json" ]; then
  echo "📋 User profile found"
else
  echo "No user profile. Using defaults."
fi
```

**If profile exists, READ IT NOW**:
```
Read(
  file_path: ".agent/.user-profile.json"
)
```

**After reading, APPLY these preferences for the session**:

1. **Verbosity** (`preferences.communication.verbosity`):
   - `concise`: Keep responses brief, code-first
   - `balanced`: Normal explanations (default)
   - `detailed`: Thorough explanations with context

2. **Confirmation threshold** (`preferences.communication.confirmation_threshold`):
   - `always`: Show verification checkpoints for all skills
   - `high-stakes`: Only for backend-endpoint, database-migration, frontend-component (default)
   - `never`: Skip verification checkpoints

3. **Frameworks** (`preferences.technical.preferred_frameworks`):
   - Remember for code generation suggestions
   - E.g., ["react", "express"] → prefer these in examples

4. **Corrections** (`corrections[]`):
   - Review recent patterns to avoid repeating mistakes
   - E.g., "REST endpoints use plural nouns" → apply immediately

**Display profile summary in session output**:
```
🧠 Theory of Mind: Active
   Profile: Loaded ({corrections_count} corrections, {goals_count} goals)
   Verbosity: {verbosity}
   Checkpoints: {confirmation_threshold}
```

**If profile doesn't exist**:
```
🧠 Theory of Mind: Active (no profile yet)
   Say "save my preferences" to create one
```

### Step 6: Check PM Tool for Assigned Tasks

**If PM tool is Linear**:
```bash
# Check if Linear MCP available
# Try to list assigned issues
```

**If PM tool is GitHub**:
```bash
gh issue list --assignee @me --limit 10 2>/dev/null
```

**If PM tool is none**:
Skip task checking.

### Step 7: Display Session Statistics (OpenTelemetry)

Run the OpenTelemetry session statistics script:

```bash
# Get the skill's base directory (passed via SKILL_BASE_DIR)
SKILL_DIR="${SKILL_BASE_DIR:-$HOME/.claude/plugins/marketplaces/jitd-marketplace/skills/nav-start}"
python3 "$SKILL_DIR/scripts/otel_session_stats.py"
```

This script:
- **If OTel enabled**: Shows real-time metrics from Claude Code
  - Real token usage (input/output/cache)
  - Cache hit rate (CLAUDE.md caching performance)
  - Session cost (actual USD spent)
  - Active time (seconds of work)
  - Context availability
- **If OTel disabled**: Shows setup instructions
- **If no metrics yet**: Shows "waiting for export" message

**Benefits of OTel integration**:
- Real data (not file-size estimates)
- Cache performance validation
- Cost tracking for ROI measurement
- Official API (won't break on updates)

### Step 8: Display Session Summary

Show this formatted summary:

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║  🚀 Navigator Session Started                        ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

📖 Documentation Navigator: Loaded
🎯 Project Management: [PM tool or "Manual"]
✅ Token Optimization: Active
🧠 Theory of Mind: [Profile status from Step 5.5]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 DOCUMENTATION LOADED (MEASURED)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Navigator (.agent/DEVELOPMENT-README.md):
  Size: [nav_bytes] bytes = [nav_tokens] tokens

CLAUDE.md (auto-loaded):
  Size: [claude_bytes] bytes = [claude_tokens] tokens

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total documentation:     [total_tokens] tokens
Available for work:      [available] tokens ([percent]%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 On-demand loading strategy:
   Load task doc when needed:  +3-5k tokens
   Load system doc if needed:  +4-6k tokens
   Load SOP if helpful:        +2-3k tokens

   Total with all docs:        ~[total + 15]k tokens

   vs Traditional (all upfront): ~150k tokens
   Savings: ~[150 - total - 15]k tokens

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 Navigator WORKFLOW REMINDER

1. Navigator-first loading
   - ✅ Loaded: .agent/DEVELOPMENT-README.md
   - Next: Load ONLY relevant task/system docs

2. Use agents for research
   - Multi-file searches: Use Task agent (saves 60-80% tokens)
   - Code exploration: Use Explore agent
   - NOT manual Read of many files

3. Task documentation
   - After features: Use nav-task-manager skill
   - After bugs: Use nav-sop-creator skill

4. Context management
   - Run nav-compact skill after isolated sub-tasks
   - Context markers save your progress

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[MULTI-CLAUDE WORKFLOWS CHECK - v4.3.0+]

Check if multi-Claude workflows installed:
```bash
if ! command -v navigator-multi-claude.sh &> /dev/null; then
  echo ""
  echo "⚡ Multi-Claude Workflows Available (v4.3.0+)"
  echo ""
  echo "   Enable parallel AI execution for complex tasks."
  echo "   Status: Not installed"
  echo ""
  echo "   Install: 'Install multi-Claude workflows'"
  echo "   Learn more: See RELEASE-NOTES-v4.3.0.md"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fi
```

Only show this prompt:
- If plugin version >= 4.3.0
- If scripts not installed
- Once per session (set flag in memory)

Do NOT show if:
- Scripts already installed
- Plugin version < 4.3.0
- User explicitly dismissed before

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[If tasks found from PM tool, list them here]

[If no tasks found:]
No active tasks found. What would you like to work on?
```

## Predefined Functions

### scripts/otel_session_stats.py

**Purpose**: Display real-time session statistics via OpenTelemetry

**When to call**: After loading navigator, before presenting session summary

**Requirements**:
- CLAUDE_CODE_ENABLE_TELEMETRY=1 (optional - shows setup if disabled)
- Metrics available from current session (shows waiting message if not)

**Execution**:
```bash
SKILL_DIR="${SKILL_BASE_DIR:-$HOME/.claude/plugins/marketplaces/jitd-marketplace/skills/nav-start}"
python3 "$SKILL_DIR/scripts/otel_session_stats.py"
```

**Output**: Formatted statistics with:
- Token usage breakdown (input/output/cache)
- Cache hit rate percentage
- Session cost in USD
- Active time
- Context availability

**Error Handling**:
- If OTel not enabled: Shows setup instructions
- If no metrics yet: Shows "waiting for export" message
- Never crashes - always displays helpful guidance

## Reference Files

This skill uses:
- **otel_session_stats.py**: Real-time session stats via OpenTelemetry
- **.agent/DEVELOPMENT-README.md**: Navigator content
- **.agent/.nav-config.json**: Configuration
- **.agent/.context-markers/.active**: Active marker check

## Error Handling

**Navigator not found**:
```
❌ Navigator not initialized

Run /nav:init to create .agent/ structure first.
```

**PM tool configured but not working**:
```
⚠️  [PM Tool] configured but not accessible

Check authentication or run setup guide.
```

**Config file malformed**:
```
⚠️  .agent/.nav-config.json is invalid JSON

Fix syntax or run /nav:init to regenerate.
```

## Success Criteria

Session start is successful when:
- [ ] Navigator loaded successfully
- [ ] Token usage calculated and displayed
- [ ] PM tool status checked (if configured)
- [ ] User knows what to work on next
- [