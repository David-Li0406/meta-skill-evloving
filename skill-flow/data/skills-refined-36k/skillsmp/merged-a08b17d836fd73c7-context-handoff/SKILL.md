---
name: context-handoff
description: Use this skill to send and receive context between parent, child, or sibling sessions for effective session management.
---

# Context Handoff

This skill allows you to send and receive context between different sessions, ensuring smooth transitions and continuity of work.

## Sending Context

### Usage

```
/context:send <direction> [subject] [path]
```

**Direction is REQUIRED** and must be one of: `parent`, `child`, or `sibling`.

- **subject**: Optional. Claude will infer from current conversation context if not provided.
- **path**: Optional. Defaults to `/tmp/claude-ctx/` if not provided.

### What it does

1. **Validates direction** - Errors if direction is not parent|child|sibling.
2. Checks if the context directory exists and creates it if necessary.
3. Auto-captures project state (timestamp, git branch, working directory, git status).
4. Creates a context file named `{path}/ctx-{direction}-{subject}.md` or infers the name if no subject is provided.
5. Writes context details including:
   - Direction and timestamp
   - Current situation and context
   - Decisions made and work completed
   - Blockers and next actions
   - Files modified and git state
6. Displays next steps for the user.

### Example: Sending to Child with Subject

```
/context:send child database-migration

✓ Context prepared for child session
  File: /tmp/claude-ctx/ctx-parent-to-child-database-migration.md

Next steps:
1. Start child session for focused work
2. In new session, run: /context:receive parent
```

### Example: Missing Direction (Error)

```
/context:send database-work

✗ Error: Must specify direction: parent, child, or sibling
  Usage: /context:send <parent|child|sibling> [subject] [path]
```

## Receiving Context

### Usage

```
/context:receive <direction> [subject] [path]
```

**Direction is REQUIRED** and must be one of: `parent`, `child`, or `sibling`.

- **subject**: Optional. Claude will infer from context if not provided.
- **path**: Optional. Defaults to `/tmp/claude-ctx/` if not provided.

### What it does

1. **Validates direction** - Errors if direction is not parent|child|sibling.
2. Checks if the context directory exists and creates it if necessary.
3. Determines the direction flow based on the argument.
4. Records the received timestamp.
5. Reads and displays the context file with the original timestamp from the sender.
6. Integrates the context into the current session understanding.

### Example: Receiving from Parent (Wildcard)

```
/context:receive parent

✓ Searching for context files: /tmp/claude-ctx/ctx-parent-to-child-*.md (newest first)
✓ Found: /tmp/claude-ctx/ctx-parent-to-child-database-migration.md (modified 2 minutes ago)

[Context displayed with parent session details]

Ready to begin focused work based on parent's context!
```

### Example: Missing Direction (Error)

```
/context:receive database-work

✗ Error: Must specify direction: parent, child, or sibling
  Usage: /context:receive <parent|child|sibling> [subject] [path]
```

## When to Use

- Before starting a child session from parent.
- Before returning to parent after completing child work.
- When switching between hierarchy levels.
- When starting a sibling session for parallel work.
- To understand what happened in related sessions.

## Related Commands

- `/context:send` - Send context to parent/child before switching.