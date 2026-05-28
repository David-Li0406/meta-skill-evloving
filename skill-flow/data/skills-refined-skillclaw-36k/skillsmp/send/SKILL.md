---
name: send
description: Send context to parent, child, or sibling session before switching
argument-hint: <direction> [subject] [path]
allowed-tools: Bash, Write
disable-model-invocation: true
---

## Current Project State (Auto-Captured)

**Timestamp**: !`date '+%Y-%m-%d %H:%M:%S'`
**Working Directory**: !`pwd`
**Git Branch**: !`git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "Not in git repo"`
**Git Status**: !`git status --short 2>/dev/null | head -10 || echo "No changes"`
**Last Commit**: !`git log -1 --oneline 2>/dev/null || echo "No commits"`

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

# send - Send context to child, parent, or sibling session

Create a context handoff file for transitioning between sessions.

## Usage

```
/context:send child [subject] [path]
/context:send parent [subject] [path]
/context:send sibling [subject] [path]
```

**IMPORTANT: Direction is REQUIRED.** Must be one of: `parent`, `child`, or `sibling`.

**Direction is REQUIRED** - must be first argument: `parent`, `child`, or `sibling`

Subject and path are optional:
- **subject**: Claude will infer from current conversation context if not provided
- **path**: Defaults to `/tmp/claude-ctx/` if not provided

## What it does

1. **Validates direction** - Errors if direction is not parent|child|sibling
2. Check "Context Directory" status above (from dynamic injection)
3. Create directory only if status shows "Does not exist - will create"
4. If creating directory, generates minimal README.md:
   ```markdown
   # Claude Context Handoff Directory

   This is an **ephemeral directory** for Claude Code session context handoff. Created by claude slash commands. '/context:send' and '/context:receive'.
   ```
5. Determines direction flow based on argument
6. **Auto-captures project state** (timestamp, git branch, working dir, git status)
7. If subject provided, creates `{path}/ctx-{direction}-{subject}.md`
8. If no subject, infers from current conversation context and creates file with inferred name
9. Path defaults to `/tmp/claude-ctx/` but can be customized
10. Uses `cat > filename.md << 'EOF'` to clear file and write context
11. Includes:
    - Direction and timestamp (auto-captured)
    - Current situation and context
    - Decisions made and work completed
    - Blockers and next actions
    - Files modified
    - Git state (auto-captured)
12. Shows clear "next steps" for user

**File naming pattern:**
- `/context:send child` → `/tmp/claude-ctx/ctx-parent-to-child-{inferred-subject}.md`
- `/context:send parent` → `/tmp/claude-ctx/ctx-child-to-parent-{inferred-subject}.md`
- `/context:send sibling` → `/tmp/claude-ctx/ctx-sibling-to-sibling-{inferred-subject}.md`

## Example: Sending to Child with Subject

```
/context:send child database-migration

✓ Context prepared for child session
  File: /tmp/claude-ctx/ctx-parent-to-child-database-migration.md

Next steps:
1. Start child session for focused work
2. In new session, run: /context:receive parent
```

## Example: Sending to Parent (Subject Inferred)

```
/context:send parent

✓ Context prepared for parent session
  File: /tmp/claude-ctx/ctx-child-to-parent-api-implementation.md

Next steps:
1. Exit this session
2. Resume parent session
3. In parent session, run: /context:receive child
```

## Example: Sending to Sibling Session

```
/context:send sibling parallel-task

✓ Context prepared for sibling session
  File: /tmp/claude-ctx/ctx-sibling-to-sibling-parallel-task.md

Next steps:
1. Start sibling session for parallel work
2. In new session, run: /context:receive sibling parallel-task
```

## Example: Custom Path

```
/context:send child feature-work ~/Documents/context/

✓ Context prepared for child session
  File: ~/Documents/context/ctx-parent-to-child-feature-work.md

Next steps:
1. Start child session
2. In new session, run: /context:receive parent feature-work ~/Documents/context/
```

## Example: Missing Direction (Error)

```
/context:send database-work

✗ Error: Must specify direction: parent, child, or sibling
  Usage: /context:send <parent|child|sibling> [subject] [path]
```

## Context File Contents

The context file should include:

### Current Situation
- What work is being done
- Why the handoff is happening
- What the next session needs to focus on

### Decisions Made
- Key technical choices
- Trade-offs considered
- Rationale for decisions

### Work Completed
- What has been implemented
- Files created/modified
- Tests written
- Commits made

### Blockers & Issues
- Problems encountered
- Questions that arose
- Things to investigate

### Next Actions
- What should happen next
- Specific tasks for the receiving session
- Dependencies or prerequisites

## Implementation Pattern

**Create directory if needed:**

```bash
# Check if directory exists, create only if needed
[[ -d /tmp/claude-ctx ]] || {
    mkdir -p /tmp/claude-ctx
    cat > /tmp/claude-ctx/README.md << 'EOF'
# Claude Context Handoff Directory

This is an **ephemeral directory** for Claude Code session context handoff. Created by claude slash commands. '/context:send' and '/context:receive'.
EOF
}
```

**Write context file:**

Use heredoc to write context file:

```bash
cat > /tmp/claude-ctx/ctx-parent-to-child-{subject}.md << 'EOF'
# Context: Parent → Child

[Context content here]
EOF
```

This pattern clears the file first, preventing accumulation of old context.

## When to use

- Before starting a child session from parent
- Before returning to parent after completing child work
- When switching between hierarchy levels
- When starting a sibling session for parallel work
- When context needs to be passed between sessions

## Related commands

- `/context:receive` - Receive context from parent/child session
