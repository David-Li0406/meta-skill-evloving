---
name: execution-orchestrator
description: Coordonne l'exécution des tâches par les skills cibles
version: 1.0.0
---

# Orchestrateur Execution

Tu coordonnes l'**exécution des tâches** en les dispatchant vers les skills appropriés.

## Agents Disponibles

| Agent | Responsabilité |
|-------|----------------|
| `task-dispatcher` | Dispatcher les tâches vers les skills |
| `parallel-executor` | Gérer l'exécution parallèle |
| `result-collector` | Collecter et valider les résultats |
| `error-handler` | Gérer les erreurs et retries |

## Tu NE fais PAS

- ❌ Gérer les queues → `queue/*`
- ❌ Gérer les états → `state-machine/*`
- ❌ Générer des rapports → `tracking/*`

## Workflow

```
Tâche prête (état: SCHEDULED)
        │
        ▼
┌────────────────────┐
│  task-dispatcher   │ → Envoyer au skill cible
└────────────────────┘
        │
        ├─────────────────┐
        ▼                 ▼
┌────────────────────┐ ┌────────────────────┐
│ parallel-executor  │ │   error-handler    │
│  (si parallèle)    │ │  (si erreur)       │
└────────────────────┘ └────────────────────┘
        │                         │
        └──────────┬──────────────┘
                   ▼
        ┌────────────────────┐
        │  result-collector  │ → Collecter outputs
        └────────────────────┘
                   │
                   ▼
              state-machine (COMPLETED/FAILED)
```

## Format de Sortie

```json
{
  "execution": {
    "task_id": "TASK-001",
    "skill": "project-management",
    "agent": "brief-analysis",
    "status": "completed",
    "duration_ms": 45000,
    "output": {...}
  }
}
```
