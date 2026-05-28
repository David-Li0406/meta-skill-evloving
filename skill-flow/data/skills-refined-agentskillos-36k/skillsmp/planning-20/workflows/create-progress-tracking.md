# Workflow: Create Progress Tracking

**Input**: PRD or Implementation Plan

## Delegation

This workflow delegates to the **artifact-tracking** skill.

Progress tracking and context artifacts have specific optimizations and structures defined in the artifact-tracking skill. Do NOT create these files directly from the planning skill.

## How to Use

When progress tracking is needed:

1. Invoke the artifact-tracking skill
2. Provide the PRD or Implementation Plan path
3. The artifact-tracking skill will create properly structured files at:
   - `.claude/progress/[feature-name]/all-phases-progress.md`
   - Or phase-specific progress files as needed

## Why Delegate?

The artifact-tracking skill provides:
- YAML+Markdown hybrid format with 95% token reduction
- Proper task breakdown with subagent assignments
- Status tracking (pending, in-progress, completed, blocked)
- Session handoff generation
- Validation against schema

## Quick Reference

```bash
# User invokes artifact-tracking skill
User: "Create progress tracking for the advanced-filtering PRD"

# Or use the skill directly
/artifact-tracking CREATE progress for advanced-filtering
```

## Related

- **artifact-tracking skill**: Primary skill for progress artifacts
- **Implementation Plan**: Source for task breakdown
- **PRD**: Source for feature scope and acceptance criteria

[Return to Planning Skill](../SKILL.md)
