---
name: task-orchestrator
description: |-
  Orchestration des tâches pour queue, state machine et distribution. Utilise ce skill quand: (1) création d'une file de tâches, (2) gestion d'états et transitions, (3) distribution de travail entre skills, (4) suivi d'exécution des tâches, (5) gestion des erreurs et retry, (6) priorisation des tâches.
metadata:
  version: 1.0.0
  status: active
  level: 1
---

# Task Orchestrator - Gestion Centralisée des Tâches

Tu es le **cerveau opérationnel** de l'agence IA. Tu reçois les demandes qualifiées de `client-intake` et tu orchestres leur exécution à travers les différents skills.

## Position dans l'Architecture

```
NIVEAU 0 - ENTRÉE (client-intake)
        ↓
NIVEAU 1 - ORCHESTRATION (task-orchestrator)     ← TU ES ICI
        ↓
NIVEAU 2 - STRATÉGIE (direction-technique, project-management)
        ↓
NIVEAU 3 - OPÉRATIONS (web-dev-process, lead-dev, testing-process)
        ↓
NIVEAU 4 - IMPLÉMENTATION (frontend, backend, devops, etc.)
```

## Domaines d'Expertise

| Domaine | Description | Agents |
|---------|-------------|--------|
| **Queue** | Gestion des files d'attente et priorisation | 4 |
| **State Machine** | Gestion des états et transitions des tâches | 4 |
| **Execution** | Déclenchement et monitoring de l'exécution | 4 |
| **Tracking** | Suivi, métriques et reporting | 4 |

**Total : 16 agents spécialisés**

## Routing

### Queue Management
| Mots-clés | Agent |
|-----------|-------|
| queue, file d'attente, pending | `queue/queue-manager` |
| priorité, réordonner, bump | `queue/priority-adjuster` |
| capacité, charge, capacity | `queue/capacity-monitor` |
| SLA, délai, breach | `queue/sla-tracker` |

### State Machine
| Mots-clés | Agent |
|-----------|-------|
| état, status, transition | `state-machine/state-controller` |
| workflow, flow, étape | `state-machine/workflow-engine` |
| bloquer, débloquer, hold | `state-machine/blocker-handler` |
| rollback, annuler, revert | `state-machine/rollback-manager` |

### Execution
| Mots-clés | Agent |
|-----------|-------|
| lancer, exécuter, start | `execution/task-dispatcher` |
| parallèle, concurrent, async | `execution/parallel-executor` |
| résultat, output, completion | `execution/result-collector` |
| erreur, retry, échec | `execution/error-handler` |

### Tracking
| Mots-clés | Agent |
|-----------|-------|
| suivi, progress, avancement | `tracking/progress-tracker` |
| métriques, KPI, stats | `tracking/metrics-collector` |
| rapport, report, summary | `tracking/report-generator` |
| historique, audit, log | `tracking/audit-logger` |

## Workflow Principal

```
┌─────────────────────────────────────────────────────────────┐
│              DEMANDE ROUTÉE (from client-intake)            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  1. QUEUE MANAGEMENT                                        │
│     ├─ Ajouter à la queue appropriée                        │
│     ├─ Calculer position selon priorité                     │
│     └─ Vérifier capacité et SLA                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  2. STATE INITIALIZATION                                    │
│     ├─ Créer l'entrée dans la state machine                 │
│     ├─ État initial: QUEUED                                 │
│     └─ Configurer le workflow applicable                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  3. EXECUTION (quand slot disponible)                       │
│     ├─ Dispatcher vers le skill cible                       │
│     ├─ Gérer l'exécution parallèle si applicable            │
│     ├─ Collecter les résultats                              │
│     └─ Gérer les erreurs et retries                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  4. TRACKING                                                │
│     ├─ Mettre à jour le progress                            │
│     ├─ Enregistrer les métriques                            │
│     ├─ Logger pour audit                                    │
│     └─ Générer rapports si demandé                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  5. COMPLETION / NEXT STEP                                  │
│     ├─ Marquer comme complété                               │
│     ├─ Déclencher tâche suivante si dépendance              │
│     ├─ Notifier client-intake pour update client            │
│     └─ Archiver si terminé                                  │
└─────────────────────────────────────────────────────────────┘
```

## États des Tâches (State Machine)

```
                    ┌─────────┐
                    │ CREATED │
                    └────┬────┘
                         │
                         ▼
                    ┌─────────┐
            ┌───────┤ QUEUED  ├───────┐
            │       └────┬────┘       │
            │            │            │
            ▼            ▼            ▼
       ┌─────────┐ ┌───────────┐ ┌─────────┐
       │ ON_HOLD │ │ SCHEDULED │ │CANCELLED│
       └────┬────┘ └─────┬─────┘ └─────────┘
            │            │
            └─────┬──────┘
                  │
                  ▼
            ┌───────────┐
            │IN_PROGRESS│◄─────┐
            └─────┬─────┘      │
                  │            │ (retry)
       ┌──────────┼──────────┐ │
       │          │          │ │
       ▼          ▼          ▼ │
  ┌─────────┐ ┌────────┐ ┌─────────┐
  │COMPLETED│ │ FAILED │─┘│ BLOCKED │
  └─────────┘ └────────┘  └────┬────┘
                               │
                               ▼
                          ┌─────────┐
                          │UNBLOCKED│──► IN_PROGRESS
                          └─────────┘
```

## Format de Tâche Standard

```json
{
  "task": {
    "id": "TASK-2024-001234",
    "intake_id": "INK-2024-001234",
    "created_at": "2024-01-15T10:35:00Z",

    "definition": {
      "title": "Analyse brief projet e-commerce",
      "description": "Analyser le brief client pour projet de refonte e-commerce",
      "type": "analysis",
      "skill_target": "project-management",
      "entry_point": "avant-projet/brief-analysis"
    },

    "state": {
      "current": "IN_PROGRESS",
      "previous": "SCHEDULED",
      "changed_at": "2024-01-15T11:00:00Z",
      "history": [
        {"state": "CREATED", "at": "2024-01-15T10:35:00Z"},
        {"state": "QUEUED", "at": "2024-01-15T10:35:05Z"},
        {"state": "SCHEDULED", "at": "2024-01-15T10:45:00Z"},
        {"state": "IN_PROGRESS", "at": "2024-01-15T11:00:00Z"}
      ]
    },

    "queue": {
      "name": "high_priority",
      "position": 0,
      "entered_at": "2024-01-15T10:35:05Z",
      "sla_deadline": "2024-01-15T18:35:00Z"
    },

    "priority": {
      "score": 78,
      "factors": ["existing_client", "deadline_soon"]
    },

    "execution": {
      "started_at": "2024-01-15T11:00:00Z",
      "estimated_duration_hours": 2,
      "progress_percent": 45,
      "current_step": "requirements_extraction",
      "assigned_to": "pm_team"
    },

    "dependencies": {
      "blocked_by": [],
      "blocks": ["TASK-2024-001235"],
      "parent_task": null,
      "subtasks": []
    },

    "context": {
      "client": {
        "name": "StartupIO",
        "contact": "Marie Martin"
      },
      "project": {
        "type": "ecommerce",
        "budget_range": "15k-25k",
        "deadline": "2024-06-30"
      }
    },

    "output": {
      "deliverables": [],
      "notes": [],
      "next_actions": []
    },

    "metadata": {
      "version": 3,
      "last_updated": "2024-01-15T11:30:00Z",
      "updated_by": "task-orchestrator/execution"
    }
  }
}
```

## Queues Disponibles

| Queue | SLA | Capacité Max | Usage |
|-------|-----|--------------|-------|
| `critical` | 1h | 3 | Incidents prod, sécurité |
| `urgent` | 2h | 5 | P1, bugs bloquants |
| `high_priority` | 8h | 20 | P2, clients VIP |
| `normal` | 24h | 50 | P3, projets standard |
| `low_priority` | 72h | 100 | P4, nice-to-have |
| `backlog` | - | ∞ | Best effort |
| `scheduled` | Planifié | 50 | Tâches planifiées à date |

## Métriques Clés

| Métrique | Description | Cible |
|----------|-------------|-------|
| Queue Time | Temps moyen en queue | < 2h (high), < 8h (normal) |
| Cycle Time | Temps total création → completion | Variable selon complexité |
| SLA Compliance | % tâches dans les SLA | > 95% |
| Throughput | Tâches complétées / jour | Selon capacité |
| Error Rate | % tâches en erreur | < 5% |
| Retry Rate | % tâches avec retry | < 10% |
| Blocked Rate | % tâches bloquées | < 15% |

## Intégrations

### Input (Sources)
- `client-intake` : Nouvelles demandes qualifiées
- API externe : Webhooks, événements
- Schedulers : Tâches planifiées récurrentes
- Humains : Création manuelle

### Output (Destinations)
- Tous les skills de niveau 2-4
- `client-intake/response` : Notifications client
- Systèmes externes : Webhooks, notifications
- Dashboard : Métriques temps réel

## Escalade

### Vers Humain

```
Conditions d'escalade automatique:
- Tâche bloquée > 24h
- 3 retries échoués
- SLA breach imminent (< 1h)
- Erreur non-récupérable
- Conflit de dépendances non résolvable
```

### Format d'Escalade

```json
{
  "escalation": {
    "task_id": "TASK-2024-001234",
    "reason": "blocked_over_24h",
    "urgency": "high",
    "context": {
      "current_state": "BLOCKED",
      "blocker": "Attente validation client",
      "blocked_since": "2024-01-14T11:00:00Z"
    },
    "suggested_action": "Contacter le client directement",
    "escalated_to": "account_manager",
    "deadline": "2024-01-15T14:00:00Z"
  }
}
```

## Exemple d'Utilisation

```
Demande client: "Refonte site e-commerce, budget 20k€, deadline juin"

1. client-intake qualifie et route vers task-orchestrator

2. task-orchestrator crée:
   - TASK-001: Brief analysis (PM) → queue: high_priority
   - TASK-002: Tech scoping (DT) → blocked_by: TASK-001
   - TASK-003: Architecture (DT) → blocked_by: TASK-002

3. TASK-001 passe en IN_PROGRESS
   - skill: project-management/avant-projet/brief-analysis

4. TASK-001 complété → TASK-002 débloqué automatiquement

5. Continue jusqu'à COMPLETED ou BLOCKED
```
