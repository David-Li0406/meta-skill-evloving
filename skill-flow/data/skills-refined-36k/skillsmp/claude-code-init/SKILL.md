---
name: claude-code-init
description: Initialize a Claude Code session with PACK context for multi-agent collaboration
metadata:
  short-description: Bootstrap Claude Code session
---

# Claude Code Session Bootstrap

## When to use

Use this skill when starting a new Claude Code session to ensure proper context loading for multi-agent collaboration. This aligns Claude Code with the PACK framework conventions.

## Procedure

1. Verify the `.agent/` directory exists in your project:

   ```bash
   ls -la .agent/
   ```

   If missing, deploy the kit first:

   ```bash
   python3 deploy_agent_kit.py --dest .
   ```

2. Create or update your `CLAUDE.md` file at the project root with PACK context:

   ```markdown
   # CLAUDE.md

   ## Agent Role

   You are operating as part of a multi-agent collaboration system (PACK).

   ## Required Context

   Load these files at session start:
   - `.agent/AGENTS.md` - Agent roster and coordination rules
   - `.agent/ai/prompts/multi_agent_orchestration_system.md` - Shared protocol

   ## Communication Conventions

   Use these prefixes in responses:
   - `Decision: ...` - A commitment or approval made
   - `Action: ...` - A concrete next step to take
   - `Question: ...` - Something requiring human decision

   ## Handoff Protocol

   When finishing work, log the handoff:
   ```bash
   python3 .agent/tools/utilities/update_agent_conversation_log.py \
     --agent claude_code \
     --summary "What was done" \
     --handoff <next_agent_or_human>
   ```

   ## Task Status Markers

   - `[ ]` Pending - Available for pickup
   - `[/]` In Progress - Currently working
   - `[x]` Complete - Verified and done
   - `[-]` Blocked - Needs human decision
   ```

3. Create the local session log if not present:

   ```bash
   cp .agent/conversation.compact.md.template conversation.compact.md
   ```

4. Review the current task state:

   ```bash
   cat .agent/task.md 2>/dev/null || echo "No active task"
   cat .agent/docs/agent_handoffs/agent_conversation_log.md | tail -50
   ```

5. (Optional) If resuming from another agent's work, check the handoff log for context.

## Inputs and outputs

- Inputs: Project with `.agent/` directory deployed
- Outputs: `CLAUDE.md` configured, session log created, context loaded

## Constraints

- Claude Code reads `CLAUDE.md` automatically at session start
- Keep `CLAUDE.md` concise - it's loaded on every interaction
- The session log (`conversation.compact.md`) is gitignored

## Examples

```bash
# Quick bootstrap
$claude-code-init

# Verify context is loaded
cat CLAUDE.md
```
