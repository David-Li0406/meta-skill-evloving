---
name: ultrathink-orchestrator
description: Use this skill to automatically invoke the appropriate ultrathink workflow for development and investigation tasks based on detected keywords.
---

# Ultrathink Orchestrator Skill

## Purpose

This skill provides automatic orchestration for development and investigation tasks. It detects the task type from keywords and delegates to the appropriate workflow skill (investigation-workflow or default-workflow).

## Execution Instructions

When this skill is activated, you MUST:

1. **Read the canonical command** for task detection logic:

   ```
   Read(file_path=".claude/commands/amplihack/ultrathink.md")
   ```

   Note: Path is relative to project root. Claude Code resolves this automatically.

2. **Detect task type** using keywords from the canonical command:
   - **Investigation keywords**: investigate, explain, understand, analyze, research, explore
   - **Development keywords**: implement, build, create, add feature, fix, refactor, deploy
   - **Hybrid tasks**: Both investigation and development keywords present

3. **Invoke appropriate workflow skill**:
   - Investigation: `Skill(skill="investigation-workflow")`
   - Development: `Skill(skill="default-workflow")`
   - Hybrid: Both sequentially (investigation first, then development)

4. **Fallback** if skill not found:
   - Read workflow markdown files directly
   - Investigation: `.claude/workflow/INVESTIGATION_WORKFLOW.md`
   - Development: `.claude/workflow/DEFAULT_WORKFLOW.md`
   - Follow workflow steps as specified

## Why This Pattern

**Benefits:**

- Single source of truth for orchestration logic in canonical command
- No content duplication between command and skill
- Task detection rules defined once, maintained once
- Changes to ultrathink command automatically inherited by skill

**Trade-offs:**

- Requires Read tool call to fetch canonical logic
- Slight indirection vs. inline implementation

This pattern aligns with amplihack philosophy: ruthless simplicity through elimination of duplication.

## Related Files

- **Canonical Command**: `.claude/commands/amplihack/ultrathink.md`
- **Development Workflow Skill**: `.claude/skills/default-workflow/`
- **Investigation Workflow Skill**: `.claude/skills/investigation-workflow/`
- **Canonical Workflows**:
  - `.claude/workflow/DEFAULT_WORKFLOW.md`
  - `.claude/workflow/INVESTIGATION_WORKFLOW.md`