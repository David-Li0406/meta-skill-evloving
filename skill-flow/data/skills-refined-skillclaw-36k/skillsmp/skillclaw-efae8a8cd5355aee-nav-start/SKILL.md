---
name: nav-start
description: Use this skill to load the Navigator documentation when starting a development session, resuming work, or beginning a new feature.
---

# Navigator Skill

Load the Navigator documentation to start your development session with optimized context.

## When to Invoke

Invoke this skill when the user:
- Says "start my session", "begin work", "start working"
- Says "load the navigator", "show me the docs"
- Asks "what should I work on?"
- Mentions "resume work", "continue from where I left off"
- Asks about project structure or current tasks

**DO NOT invoke** if:
- User already ran `/nav:start` command in this conversation
- Navigator is already loaded (check conversation history)
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
```