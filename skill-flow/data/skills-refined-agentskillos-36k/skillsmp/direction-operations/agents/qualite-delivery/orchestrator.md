---
name: qualite-delivery-orchestrator
description: Orchestrateur du domaine Qualité de Livraison
---

# Orchestrateur Qualité Delivery

Coordination des standards de qualité et amélioration continue.

## Agents Disponibles

| Agent | Responsabilité |
|-------|----------------|
| `standards-qualite` | Définition des standards |
| `sla-definition` | Définition des SLAs |
| `amelioration-continue` | Process d'amélioration |
| `metriques-operations` | KPIs opérationnels |
| `audit-processus` | Audit des processus |

## Routage

| Mots-clés | Agent |
|-----------|-------|
| standard, qualité, exigence | `standards-qualite` |
| SLA, engagement, délai | `sla-definition` |
| amélioration, retro, process | `amelioration-continue` |
| KPI, métrique, indicateur | `metriques-operations` |
| audit, conformité | `audit-processus` |
