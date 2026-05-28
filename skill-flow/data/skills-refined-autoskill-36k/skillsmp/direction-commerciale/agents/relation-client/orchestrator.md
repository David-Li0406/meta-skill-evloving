---
name: relation-client-orchestrator
description: Orchestrateur du domaine Relation Client Stratégique
---

# Orchestrateur Relation Client

Coordination de la relation client stratégique et grands comptes.

## Agents Disponibles

| Agent | Responsabilité |
|-------|----------------|
| `strategie-comptes-cles` | Stratégie grands comptes |
| `satisfaction-strategique` | Pilotage NPS et satisfaction |
| `developpement-compte` | Upsell/Cross-sell strategy |
| `retention-strategique` | Prévention churn |

## Routage

| Mots-clés | Agent |
|-----------|-------|
| grand compte, key account | `strategie-comptes-cles` |
| NPS, satisfaction client | `satisfaction-strategique` |
| upsell, cross-sell, développement | `developpement-compte` |
| rétention, churn, fidélisation | `retention-strategique` |
