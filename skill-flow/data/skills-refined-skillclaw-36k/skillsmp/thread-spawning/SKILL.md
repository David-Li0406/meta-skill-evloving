---
name: Thread Spawning
description: Spawn new Claude/Gemini threads in specific folders. Use this when users want to work on specific projects.
allowed-tools: [SpawnThread]
---

# Thread Spawning Skill

This skill allows you to create new AI threads in specific folders for dedicated project work.

## When to Use

Use this skill when:
- User asks you to open a folder or project in a dedicated thread
- User wants to clone a repository and work on it
- User asks to "open claude/gemini in [folder]"
- User needs a separate conversation for a specific project

## Actions

### Spawn Thread

Creates a new Discord thread with a CLI session in the specified folder.

**Usage**:
```bash
/path/to/bin/spawn-thread.sh "<folder_path>" "<cli_type>" "<initial_message>"
```

**Arguments**:
- `folder_path` - Absolute path or path relative to default workspace
- `cli_type` - "claude", "gemini", or "auto" (uses first available CLI)
- `initial_message` - Optional first message to send to the new session

**Examples**:

```bash
# Open a project in a new thread
/path/to/bin/spawn-thread.sh "/Users/user/projects/myapp" "auto" "Let's review the codebase"

# Clone and open in new thread
git clone https://github.com/user/repo /tmp/repo
/path/to/bin/spawn-thread.sh "/tmp/repo" "claude" "Explore this project structure"
```

## Notes

- The new thread will appear as a Discord thread in the runner's channel
- Each spawned thread is independent - it has its own conversation context
- The CLI in the new thread can use the discord-integration skill to communicate
