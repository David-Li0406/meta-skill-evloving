---
name: managing-signs
description: Manages learning extraction and sign application workflows. This skill should be used when extracting learnings from session transcripts, reviewing proposed signs, or applying approved learnings to CLAUDE.md files. Triggers on "extract learnings", "review signs", "apply signs", "manage signs", "learning backlog".
---

# Managing Signs

This skill provides workflows for the learning loop - extracting wisdom from session failures and applying them as permanent signs in CLAUDE.md files.

## Capabilities

- Extract learnings from session transcripts
- Manage the learning backlog (add, list, review)
- Apply approved signs to target CLAUDE.md files
- Integrate with sprint workflows for automated extraction

## Quick Start

See the plugin commands for available operations:
- `/m42-signs:add` - Manually add a learning to the backlog
- `/m42-signs:list` - List learnings in the backlog
- `/m42-signs:extract` - Extract learnings from a session transcript
- `/m42-signs:review` - Review and approve/reject learnings
- `/m42-signs:apply` - Apply approved learnings to CLAUDE.md files

## Sprint Workflow Integration

Integrate learning extraction into your sprint workflows for automated capture of development insights.

### Transcript Location

During sprint execution, session transcripts are stored at:
```
.claude/sprints/<sprint-id>/transcripts/<phase>-<step>-<subphase>.jsonl
```

### Template Variables

| Variable | Available In | Description |
|----------|--------------|-------------|
| `{{sprint.id}}` | All phases | Sprint identifier (e.g., `2026-01-18_feature-name`) |
| `{{sprint.name}}` | All phases | Human-readable sprint name |
| `{{step.id}}` | For-each phases | Step identifier (e.g., `step-1`) |
| `{{step.prompt}}` | For-each phases | Step description from SPRINT.yaml |
| `{{phase.id}}` | All phases | Current phase identifier |

### Adding Learning Extraction to a Workflow

Add as a final phase in any sprint workflow:

```yaml
phases:
  # ... your existing phases ...

  - id: learning-extraction
    prompt: |
      Extract learnings from this sprint's development sessions.

      Use /m42-signs:extract to process transcripts at:
      .claude/sprints/{{sprint.id}}/transcripts/

      Use --confidence-min medium to filter low-confidence patterns.
```

### Using the Workflow Templates

Two templates are provided in `assets/`:

1. **learning-extraction-workflow.yaml** - Standalone learning extraction workflow
   ```yaml
   # Reference as a workflow
   - id: learning
     workflow: learning-extraction-workflow
   ```

2. **sprint-with-learning.yaml** - Complete sprint workflow with learning extraction
   ```yaml
   # Use as your sprint workflow
   workflow: sprint-with-learning
   ```

### Example Configuration

Full sprint configuration with learning extraction:

```yaml
# SPRINT.yaml
name: Feature Implementation Sprint
workflow: sprint-with-learning

steps:
  - id: step-1
    prompt: Implement user authentication

  - id: step-2
    prompt: Add authorization middleware

# Learning extraction runs automatically after all steps
```

### Manual Extraction

To manually extract learnings from a specific transcript:

```bash
/m42-signs:extract .claude/sprints/<sprint-id>/transcripts/<file>.jsonl --confidence-min medium
```

### Post-Extraction Review

After extraction completes:
1. Run `/m42-signs:status` to see backlog summary
2. Run `/m42-signs:review` to approve/reject learnings
3. Run `/m42-signs:apply` to apply approved signs to CLAUDE.md files
