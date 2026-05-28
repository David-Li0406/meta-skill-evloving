---
name: consultant:status
description: "View comprehensive project status including phase, completed workflows, next actions, and any blockers."
invocation: user
---

# Project Status

Display the current state of the consulting project.

## Information Displayed

### Project Overview
```
╔═══════════════════════════════════════════╗
║  Projet: {project_name}                   ║
║  Client: {client_name}                    ║
║  Type: {greenfield/brownfield}            ║
║  Phase: {current_phase}                   ║
║  Dernière activité: {timestamp}           ║
╚═══════════════════════════════════════════╝
```

### Workflow Progress
```
Discovery:
  ✅ frame - Terminé (21/01)
  ✅ clarify - Terminé (21/01)
  ⏳ upsell - En attente

Quotation:
  ✅ estimate - Terminé (21/01)
  🔒 quote - Checkpoint requis
```

### Sprint Status (if in Development)
```
Sprint: Sprint 1
Stories: 2/5 terminées
En cours: STORY-003
Bloqué: -
```

### Next Action
```
▶ Prochaine étape: {workflow}
  Raison: {why_this_is_next}
  Agent: {responsible_agent}
```

### Blockers (if any)
```
⚠️ Blockers:
- Checkpoint 'quotation_approval' en attente
- STORY-002 bloqué par STORY-001
```

## Data Sources

- `workflow-status.yaml` - Phase and workflow progress
- `project-context.md` - Project details
- `sprint-status.yaml` - Sprint and story status
- `project-path.yaml` - Phase dependencies

## Agent

This skill uses the `consultant-orchestrator` subagent.
