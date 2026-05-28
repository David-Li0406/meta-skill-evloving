---
name: context-restores
description: reads and loads conversation context from ".claude/context" directory
allowed-tools: Read
argument-hint: [filename]
---

# /context-restores

Load conversation context from a previous session stored in the `.claude/context`
directory at repository root.

## Task

Read "{repo_root}/.claude/context/{filename}" where filename is `$ARGUMENTS`.

- Sanitize filename: use basename only (reject paths containing `/` or `..`)
- If file exists: read and internalize content for session reference
- If file not found: inform user with full path, continue normally

## Success Criteria

Context successfully loaded when you can answer questions about the previous
session based on file contents.
