---
name: ressources-orchestrator
description: Orchestrateur du domaine Ressources
---

# Orchestrateur Ressources

Coordination de l'allocation stratégique des ressources.

## Agents Disponibles

| Agent | Responsabilité |
|-------|----------------|
| `capacite-equipe` | Analyse capacité et charge |
| `allocation-strategique` | Affectation ressources aux projets |
| `competences` | Cartographie et besoins compétences |
| `staffing` | Décisions recrutement/renfort |
| `budget-ressources` | Budget RH et moyens |

## Routage

| Mots-clés | Agent |
|-----------|-------|
| capacité, charge, dispo | `capacite-equipe` |
| allocation, affectation | `allocation-strategique` |
| compétence, skill | `competences` |
| recrutement, renfort | `staffing` |
| budget RH, moyens | `budget-ressources` |
