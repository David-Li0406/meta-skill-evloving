---
name: receive-context
description: Use this skill to receive context from a parent, child, or sibling session for effective session handoff.
---

# Receiving Context

**Received At**: !`date '+%Y-%m-%d %H:%M:%S'`  
**Context Directory**: !`[[ -d /tmp/claude-ctx ]] && echo "Exists" || echo "Does not exist - will create"`

---

**Note**: If `/tmp/claude-ctx/` does not exist, create it with:
```bash
mkdir -p /tmp/claude-ctx
cat > /tmp/claude-ctx/README.md << 'EOF'
# Claude Context Handoff Directory

This is an **ephemeral directory** for Claude Code session context handoff. Created by claude slash commands. '/context:send' and '/context:receive'.
EOF
```

---

# receive - Receive context from parent, child, or sibling session

Read and integrate context from session handoff files.

## Usage

```
/context:receive parent [subject] [path]
/context:receive child [subject] [path]
/context:receive sibling [subject] [path]
```

**IMPORTANT: Direction is REQUIRED.** Must be one of: `parent`, `child`, or `sibling`.

Subject and path are optional:
- **subject**: Claude will infer from context if not provided.
- **path**: Defaults to `/tmp/claude-ctx/` if not provided.

## What it does

1. **Validates direction** - Errors if direction is not parent|child|sibling.
2. Checks "Context Directory" status.
3. Creates directory only if it does not exist.
4. If creating directory, generates a minimal README.md.
5. Determines direction flow based on argument.
6. **Records received timestamp** (auto-captured).
7. If subject provided, looks for `{path}/ctx-{direction}-{subject}.md`.
8. If no subject, uses wildcard: `{path}/ctx-{direction}-*.md` **sorted by newest first**.
9. Reads and displays context file with **original timestamp** from sender.
10. Integrates context into current session understanding.

**Important:** When using wildcard (no subject), files are sorted by modification time with **newest first**, ensuring you get the most recent context.

**File patterns:**
- `/context:receive parent` → looks for `/tmp/claude-ctx/ctx-parent-to-child-*.md`
- `/context:receive child` → looks for `/tmp/claude-ctx/ctx-child-to-parent-*.md`
- `/context:receive sibling` → looks for `/tmp/claude-ctx/ctx-sibling-to-sibling-*.md`

## Examples

### Receiving from Parent (Wildcard)

```
/context:receive parent

✓ Searching for context files: /tmp/claude-ctx/ctx-parent-to-child-*.md (newest first)
✓ Found: /tmp/claude-ctx/ctx-parent-to-child-database-migration.md (modified 2 minutes ago)

[Context displayed with parent session details]

Ready to begin focused work based on parent's context!
```

### Receiving from Child with Subject

```
/context:receive child api-implementation

✓ Context received from child session
  File: /tmp/claude-ctx/ctx-child-to-parent-api-implementation.md

[Context displayed with completed work summary]

Child session completed. Integrating results back.
```

### Receiving from Sibling

```
/context:receive sibling parallel-task

✓ Context received from sibling session
  File: /tmp/claude-ctx/ctx-sibling-to-sibling-parallel-task.md

[Context displayed with parallel work details]

Sibling session completed. Integrating parallel work.
```

### Custom Path

```
/context:receive parent database-work ~/Documents/context/

✓ Context received from parent session
  File: ~/Documents/context/ctx-parent-to-child-database-work.md

[Context displayed]
```

### Missing Direction (Error)

```
/context:receive database-work

✗ Error: Must specify direction: parent, child, or sibling
  Usage: /context:receive <parent|child|sibling> [subject] [path]
```

## What gets loaded

- **Context file content**: Decisions, work done, blockers, next actions.
- **Handoff metadata**: Why the handoff occurred, what was planned.
- **Related context**: Key information needed to continue.

## When to use

- Immediately after starting a new child session from parent.
- After resuming parent session when child is complete.
- When starting a sibling session and receiving context from another sibling.
- To understand what happened in related sessions.

## Related commands

- `/context:send` - Send context to parent/child before switching.