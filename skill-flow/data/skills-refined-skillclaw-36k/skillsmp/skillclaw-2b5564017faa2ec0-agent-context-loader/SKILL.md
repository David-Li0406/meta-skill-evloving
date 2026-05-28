---
name: agent-context-loader
description: Use this skill when you want to automatically load agent-specific instructions from AGENTS.md files into Claude Code's context, enhancing specialized agent behaviors during your sessions.
---

# Agent Context Auto-Loader

**⚡ This skill activates AUTOMATICALLY - no user action required!**

## Purpose

This skill makes Claude Code recognize and load `AGENTS.md` files with the same priority as `CLAUDE.md` files, enabling specialized agent-specific instructions for your projects.

## How It Works

### Automatic Trigger Conditions

This skill automatically activates when:
1. **Starting a new Claude Code session** in any directory
2. **Changing directories** during a session (via `cd` or file operations)
3. **Any other agent skill is invoked** (ensures agent context is loaded first)
4. **User explicitly requests**: "load agent context", "check for AGENTS.md", or "read agent rules"

### Execution Flow

When triggered, Claude Code will:

1. **Check for AGENTS.md**: Look for `./AGENTS.md` in the current working directory
2. **Read the file** (if it exists): Use the Read tool to load full content
3. **Incorporate into context**: Treat AGENTS.md rules as session-level instructions
4. **Announce loading**: Confirm with user: "📋 Loaded agent-specific context from AGENTS.md"
5. **Apply for session**: Follow these rules for all subsequent operations

### Priority and Conflict Resolution

- **AGENTS.md supplements CLAUDE.md**: Both are active simultaneously
- **In case of conflicts**: AGENTS.md takes precedence for agent-specific behaviors
- **Scope**: AGENTS.md applies to agent workflows; CLAUDE.md applies to general project context

## Expected Behavior

### If AGENTS.md exists:
```
📋 Loaded agent-specific context from AGENTS.md

Following specialized agent rules for this session:
- [rule 1 from AGENTS.md]
- [rule 2 from AGENTS.md]
...
```

### If AGENTS.md doesn't exist:
```
No AGENTS.md found - using standard CLAUDE.md context only
```

## User Experience

**Fully Automatic** (preferred):
- Install plugin → AGENTS.md loads automatically → Agent rules active → No user action needed

**Manual Invocation** (fallback):
```bash
# You can manually invoke the loading of agent context if needed.
```