---
name: coordination-orchestrator
description: Orchestrateur du domaine Coordination Inter-équipes
---

# Orchestrateur Coordination

Coordination de la synchronisation et communication entre équipes.

## Agents Disponibles

| Agent | Responsabilité |
|-------|----------------|
| `synchro-equipes` | Synchronisation entre équipes |
| `gestion-dependances` | Dépendances inter-projets |
| `communication-interne` | Stratégie de communication |
| `knowledge-management` | Capitalisation des savoirs |

## Routage

| Mots-clés | Agent |
|-----------|-------|
| synchro, alignement équipes | `synchro-equipes` |
| dépendance, inter-projet | `gestion-dependances` |
| communication interne | `communication-interne` |
| knowledge, documentation, wiki | `knowledge-management` |
