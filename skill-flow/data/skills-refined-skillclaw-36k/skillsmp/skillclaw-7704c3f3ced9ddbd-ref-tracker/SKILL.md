---
name: ref-tracker
description: Use this skill when you need to automatically track research sources and major prompts in your project documentation, especially when specific tracking files are present.
---

# Reference Tracker Skill

Automatically track research sources and major prompts for academic and project documentation.

## When to Activate

This skill activates automatically when:
1. User runs the `/track:init` command.
2. You notice `CLAUDE_SOURCES.md` or `CLAUDE_PROMPTS.md` files in the project.

Once activated, check `./.claude/.ref-autotrack` to determine if auto-tracking is enabled.

## Activation Check

**Before any tracking operation:**

1. Check if `./.claude/.ref-autotrack` exists:
   - If it exists → auto-tracking is enabled, proceed with tracking.
   - If missing → auto-tracking is disabled, skip tracking.

2. Read `./.claude/.ref-config` for verbosity settings:
   ```
   PROMPTS_VERBOSITY=major|all|minimal|off
   SOURCES_VERBOSITY=all|off
   ```

## About the .ref-autotrack File

**Location:** `./.claude/.ref-autotrack`

**Purpose:** Marker file that enables/disables automatic tracking.

**Contents:** Contains explanatory comments for other Claude sessions:
```
# Auto-tracking marker for ref-tracker plugin
# Presence = enabled | Absence = disabled
# Managed by: /track:auto command
# See: /track:help for details
```

**Created by:** `/track:auto` or `/track:auto on` command.

**Managed by:** `/track:auto` command (toggles on/off, or explicit on/off).

**NOT created by:** `/track:init` - tracking starts disabled.

**If you find this file:** The project has reference tracking initialized. Use the ref-tracker skill to automatically log research sources and major prompts according to the verbosity configuration in `./.claude/.ref-config`.

## Tracking Rules

When auto-tracking is enabled (`.ref-autotrack` exists), automatically track:

### CLAUDE_SOURCES.md
Track **after every**:
- WebSearch operation
- WebFetch operation
- Local documentation search (Grep/Read for docs, API references)

**Respect SOURCES_VERBOSITY:**
- `all` (default) → Track all operations.
- `off` → Skip.