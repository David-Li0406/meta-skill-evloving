---
name: claude-code-handoff
description: Hand off work from Claude Code to another agent or human with proper logging
metadata:
  short-description: Handoff from Claude Code
---

# Claude Code Handoff

## When to use

Use this skill when Claude Code has completed a unit of work and needs to hand off to another agent (Gemini auditor, human reviewer, etc.) or when pausing work that will be resumed later.

## Procedure

1. Summarize the work completed (max 3 bullets):
   - What changed
   - What was tested/verified
   - What remains

2. Identify the next agent or human who should pick up:
   - `human` - Requires human decision or review
   - `gemini_auditor` - Needs architectural review before proceeding
   - `ag` / `builder` - Ready for implementation
   - `reviewer` - Ready for code review
   - `docs` - Needs documentation updates

3. Log the handoff using the CLI tool:

   ```bash
   python3 .agent/tools/utilities/update_agent_conversation_log.py \
     --agent claude_code \
     --summary "Brief description of what was done" \
     --handoff <next_agent> \
     --task "Specific follow-up task 1" \
     --task "Specific follow-up task 2" \
     --reference "path/to/changed/file.py" \
     --reference "path/to/another/file.py" \
     --context <setup|feature|bugfix|refactor|docs> \
     --status <ready|blocked|wip>
   ```

4. If handing off to Gemini auditor, ensure task and plan files are current:

   ```bash
   # Update task definition
   cat > .agent/task.md << 'EOF'
   # Current Task
   [Objective]

   ## Acceptance Criteria
   - [ ] Criteria 1
   - [ ] Criteria 2
   EOF

   # Update implementation plan
   cat > .agent/implementation_plan.md << 'EOF'
   # Implementation Plan
   [Overview]

   ## Steps
   1. [ ] Step 1
   2. [ ] Step 2
   EOF
   ```

5. If blocked, clearly state what is needed:

   ```bash
   python3 .agent/tools/utilities/update_agent_conversation_log.py \
     --agent claude_code \
     --summary "Blocked: Need clarification on X" \
     --handoff human \
     --status blocked \
     --note "Specific question that needs answering"
   ```

## Inputs and outputs

- Inputs: Completed work, knowledge of next steps
- Outputs: Handoff entry in agent_conversation_log.md, updated task/plan files if needed

## Constraints

- Always include at least one `--reference` for changed files
- Keep summary to one sentence
- Tasks should be actionable and specific
- Use `--status blocked` only when truly blocked

## Examples

```bash
# Simple handoff to human
python3 .agent/tools/utilities/update_agent_conversation_log.py \
  --agent claude_code \
  --summary "Implemented user auth with JWT tokens" \
  --handoff human \
  --task "Review security of token handling" \
  --reference "src/auth.py"

# Handoff to Gemini auditor
python3 .agent/tools/utilities/update_agent_conversation_log.py \
  --agent claude_code \
  --summary "Drafted implementation plan for caching layer" \
  --handoff gemini_auditor \
  --context feature \
  --reference ".agent/implementation_plan.md"

# Blocked handoff
python3 .agent/tools/utilities/update_agent_conversation_log.py \
  --agent claude_code \
  --summary "Blocked: Database schema unclear" \
  --handoff human \
  --status blocked \
  --note "Need to know if users table should have soft deletes"
```
