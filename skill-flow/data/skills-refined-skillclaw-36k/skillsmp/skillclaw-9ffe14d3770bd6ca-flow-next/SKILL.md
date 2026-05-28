---
name: flow-next
description: Use this skill to manage tasks and epics in the `.flow/` directory, including creating tasks, viewing their status, and managing epics.
---

# Flow-Next Task Management

Quick task operations in `.flow/`. For planning features use `/flow-next:plan`, for executing use `/flow-next:work`.

## Setup

**CRITICAL: flowctl is BUNDLED — NOT installed globally.** `which flowctl` will fail (expected). Always use:

```bash
FLOWCTL="${CLAUDE_PLUGIN_ROOT}/scripts/flowctl"
```

Then run commands with `$FLOWCTL <command>`.

**Discover all commands/options:**
```bash
$FLOWCTL --help
$FLOWCTL <command> --help   # e.g., $FLOWCTL task --help
```

## Quick Reference

```bash
# Check if .flow exists
$FLOWCTL detect --json

# Initialize (if needed)
$FLOWCTL init --json

# List everything (epics + tasks grouped)
$FLOWCTL list --json

# List all epics
$FLOWCTL epics --json

# List all tasks (or filter by epic/status)
$FLOWCTL tasks --json
$FLOWCTL tasks --epic fn-1 --json
$FLOWCTL tasks --status todo --json

# View epic with all tasks
$FLOWCTL show fn-1 --json
$FLOWCTL cat fn-1              # Spec markdown

# View single task
$FLOWCTL show fn-1.2 --json
$FLOWCTL cat fn-1.2            # Task spec

# What's ready to work on?
$FLOWCTL ready --epic fn-1 --json

# Create task under existing epic
$FLOWCTL task create --epic fn-1 --title "Fix bug X" --json

# Set task description (from file)
echo "Description here" > /tmp/desc.md
$FLOWCTL task set-description fn-1.2 --file /tmp/desc.md --json

# Set acceptance criteria (from file)
echo "- [ ] Criterion 1" > /tmp/accept.md
$FLOWCTL task set-acceptance fn-1.2 --file /tmp/accept.md --json

# Start working on task
$FLOWCTL start fn-1.2 --json

# Mark task done
echo "What was done" > /tmp/summary.md
echo '{"commits":["abc123"],"tests":["npm test"],"prs":[]}' > /tmp/evidence.json
$FLOWCTL done fn-1.2 --summary-file /tmp/summary.md --evidence-json /tmp/evidence.json --json

# Validate structure
$FLOWCTL validate --epic fn-1 --json
$FLOWCTL validate --all --json
```

## Common Patterns

### "Add a task for X"

1. Find relevant epic:
   ```bash
   # List all epics
   $FLOWCTL epics --json

   # Or show a specific epic to check its scope
   $FLOWCTL show fn-1 --json
   ```

2. Create task:
   ```bash
   $FLOWCTL task create --epic fn-N --title "Short title" --json
   ```

3. Add description:
   ```bash
   $FLOWCTL task set-description fn-1.2 --file /tmp/desc.md --json
   ```
   
4. Set acceptance criteria:
   ```bash
   $FLOWCTL task set-acceptance fn-1.2 --file /tmp/accept.md --json
   ```