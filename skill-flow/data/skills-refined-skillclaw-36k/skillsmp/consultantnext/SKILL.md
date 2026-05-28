---
name: consultant:next
description: "Execute the next recommended action based on project state. Léo analyzes workflow-status and project-path to determine what should happen next."
invocation: user
---

# Next Action

Automatically execute the next recommended workflow based on project state.

## How It Works

1. **Load State**
   - Read workflow-status.yaml
   - Check next_action field

2. **Validate Dependencies**
   - Verify all depends_on workflows are completed
   - Check no blocking checkpoints

3. **Execute**
   - Route to appropriate agent
   - Run the workflow

4. **Update**
   - Mark workflow completed
   - Calculate new next_action

## Decision Logic

```
IF project not initialized:
  → /init

ELSE IF brownfield AND analyze-codebase not done:
  → /analyze-codebase

ELSE IF current phase has pending required workflow:
  → Execute that workflow

ELSE IF current phase complete AND checkpoint not passed:
  → Display checkpoint, wait for approval

ELSE IF current phase complete:
  → Move to next phase, find first workflow

ELSE IF all phases complete:
  → "Projet terminé! 🎉"
```

## Example Flow

```
next_action:
  workflow: "create-story"
  agent: "planner"
  reason: "Specs terminées, créer les stories de développement"
```

User types: `/consultant:next`

Result: Launches consultant-planner with /create-story

## Agent

This skill uses the `consultant-orchestrator` subagent.
