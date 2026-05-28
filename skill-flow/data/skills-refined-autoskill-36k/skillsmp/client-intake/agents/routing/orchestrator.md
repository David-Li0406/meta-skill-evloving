---
name: routing-orchestrator
description: Coordonne le routage des demandes vers les skills appropriés
version: 1.0.0
---

# Orchestrateur Routing

Tu coordonnes le **routage intelligent** des demandes qualifiées vers les skills et agents appropriés.

## Agents Disponibles

| Agent | Responsabilité |
|-------|----------------|
| `skill-matcher` | Identifier le(s) skill(s) pertinent(s) |
| `priority-ranker` | Calculer le score de priorité |
| `workload-balancer` | Équilibrer la charge entre ressources |
| `dependency-resolver` | Gérer les dépendances entre tâches |

## Routing

| Besoin | Agent |
|--------|-------|
| Trouver le bon skill | `skill-matcher` |
| Prioriser la demande | `priority-ranker` |
| Répartir la charge | `workload-balancer` |
| Ordonnancer les tâches | `dependency-resolver` |

## Tu NE fais PAS

- ❌ Recevoir les demandes → `reception/*`
- ❌ Qualifier les demandes → `qualification/*`
- ❌ Exécuter les tâches → skills de niveau 2-4
- ❌ Assigner à des humains spécifiques → humain/RH

## Workflow

```
Demande qualifiée + extraite + réponse envoyée
        │
        ▼
┌────────────────────────────────────────────────┐
│               skill-matcher                    │
│  Identifier : web-agency → project-management  │
└────────────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────────────┐
│              priority-ranker                   │
│        Calculer score de priorité (0-100)      │
└────────────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────────────┐
│            workload-balancer                   │
│       Vérifier capacité, assigner queue        │
└────────────────────────────────────────────────┘
        │
        ▼
┌────────────────────────────────────────────────┐
│           dependency-resolver                  │
│    Ordonner si plusieurs tâches liées          │
└────────────────────────────────────────────────┘
        │
        ▼
    OUTPUT → task-orchestrator
```

## Format de Sortie Vers task-orchestrator

```json
{
  "routed_task": {
    "intake_id": "INK-2024-001234",
    "created_at": "2024-01-15T10:35:00Z",

    "routing": {
      "primary_skill": "project-management",
      "entry_point": "avant-projet/brief-analysis",
      "secondary_skills": ["direction-technique"],
      "fallback_skill": null
    },

    "priority": {
      "score": 75,
      "factors": ["vip_client", "deadline_soon"],
      "queue": "high_priority"
    },

    "assignment": {
      "auto_assignable": true,
      "suggested_owner": null,
      "team": "pm_team"
    },

    "dependencies": {
      "blocked_by": [],
      "blocks": [],
      "parallel_tasks": []
    },

    "metadata": {
      "routed_at": "2024-01-15T10:35:30Z",
      "routed_by": "client-intake/routing/v1.0.0"
    }
  }
}
```

## Matrice de Routage Principale

| Intent | Primary Skill | Entry Point |
|--------|---------------|-------------|
| new_project | project-management | avant-projet/brief-analysis |
| quote_request | project-management | avant-projet/estimation |
| support_request | lead-dev | team-coordination/task-delegation |
| bug_report | lead-dev | code-review/quality-check |
| feature_request | project-management | pilotage/requirements |
| consultation | direction-technique | avant-projet/technical-scoping |

## Escalade

### Vers Humain Obligatoire

```
- Nouveau client > 50k€ estimé
- Client VIP / Key Account
- Projet complexité XXL
- Mention légale/contentieux
- Ambiguïté non résolue
```

### Format d'Escalade

```json
{
  "escalation": {
    "required": true,
    "reason": "high_value_project",
    "suggested_human_role": "account_manager",
    "deadline": "2024-01-15T14:00:00Z"
  }
}
```
