---
name: workflow-creator
description: >
  Skill to teach the agent how to create new Antigravity workflows.
  Trigger: Use this skill when the user wants to automate a repetitive task using an Antigravity workflow.
---

# Workflow Creator Skill

This skill allows the agent to create structured workflows for Antigravity.

## Workflow Format
Workflows are markdown files in `.agent/workflows/` that follow this structure:

\`\`\`markdown
---
description: [short title]
---
# Workflow: [Name]

[Steps...]
// turbo
[Step that involves a run_command can be auto-run if annotated with // turbo]
\`\`\`

## Process
1. **Define Task**: Identify the sequence of steps.
2. **Create File**: `.agent/workflows/<workflow-name>.md`
3. **Annotate**: Use `// turbo` for safe command steps.
4. **Register**: Mention the workflow in the project documentation.
