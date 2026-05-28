---
name: consultant:init
description: "Initialize a new B2B consulting project. Creates project structure, config, and initial context files."
invocation: user
---

# Initialize Project

Set up a new consulting project with all necessary files and configuration.

## What This Creates

```
_consultant/
├── config.yaml           # Project configuration
├── project-context.md    # Project "bible"
├── workflow-status.yaml  # Progress tracking
├── project-path.yaml     # Phase definitions
├── sprint-status.yaml    # Sprint tracking
├── agents/               # Agent definitions
├── skills/               # Skill definitions
├── templates/            # Document templates
├── output/               # Generated deliverables
└── stories/              # User stories
```

## Process

1. **Gather project info:**
   - Project name
   - Client name
   - Project type (greenfield/brownfield)
   - Brief description

2. **Create configuration:**
   - Set consultant identity from global config or prompt
   - Configure rates
   - Set language preferences

3. **Initialize state files:**
   - Empty project-context.md ready for Discovery
   - workflow-status.yaml at phase 0 or 1
   - sprint-status.yaml with empty sprint

4. **Detect project type:**
   - Greenfield: Start at Discovery
   - Brownfield: Start at Analysis (analyze-codebase)

## After Initialization

Next step will be:
- **Greenfield**: `/clarify` or `/frame` (Discovery phase)
- **Brownfield**: `/analyze-codebase` (Analysis phase)

## Agent

This skill uses the `consultant-orchestrator` subagent.
