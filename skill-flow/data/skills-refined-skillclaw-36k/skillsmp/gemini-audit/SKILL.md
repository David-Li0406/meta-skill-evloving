---
name: gemini-audit
description: Run audit workflow via Gemini CLI to validate task and plan alignment
metadata:
  short-description: Audit task via Gemini
---

# Gemini Audit Workflow

## When to use

Use this skill when you need an independent review of a task and its implementation plan before proceeding with execution. The auditor will validate alignment, flag concerns, and provide an APPROVE/REJECT decision.

## Procedure

1. Ensure `.agent/task.md` contains the current task definition:
   ```markdown
   # Current Task
   [Objective description]

   ## Acceptance Criteria
   - [ ] Criteria 1
   - [ ] Criteria 2
   ```

2. Ensure `.agent/implementation_plan.md` contains the proposed plan:
   ```markdown
   # Implementation Plan
   [Plan overview]

   ## Steps
   1. [ ] Step 1
   2. [ ] Step 2
   ```

3. Run the audit using the CLI tool:
   ```bash
   python3 .agent/tools/utilities/gemini_audit.py --auto
   ```
   Or use the shell script:
   ```bash
   ./.agent/tools/bin/audit_task.sh
   ```

4. Review the decision in the output:
   - `APPROVE`: Plan aligns with task, proceed with implementation
   - `REJECT`: Issues found, address before proceeding
   - `NEEDS_INFO`: Clarification required, update task or plan

5. The audit result is automatically appended to:
   `.agent/docs/agent_handoffs/agent_conversation_log.md`

## Inputs and outputs

- Inputs: `.agent/task.md`, `.agent/implementation_plan.md`
- Outputs: Decision (APPROVE/REJECT/NEEDS_INFO), log entry appended

## Constraints

- Requires Gemini CLI initialized (run `$gemini-cli-init` first)
- Auditor will not generate code, only critique
- One audit per task/plan pair recommended before implementation

## Examples

```bash
# Quick audit with defaults
python3 .agent/tools/utilities/gemini_audit.py --auto

# Explicit file paths
python3 .agent/tools/utilities/gemini_audit.py \
  --task .agent/task.md \
  --plan .agent/implementation_plan.md

# Shell script (uses defaults)
./.agent/tools/bin/audit_task.sh
```
