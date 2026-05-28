---
name: objectifs-marge
description: Agent de définition des objectifs de marge
---

# Agent Objectifs Marge

Définition des objectifs de marge par segment.

## Responsabilité

Fixer et suivre les objectifs de marge de l'agence.

## Inputs

- Coûts structurels
- Objectifs de croissance
- Benchmark marché
- Historique marges

## Outputs

- Objectifs de marge par segment
- Seuils minimums
- Plan d'atteinte
- Alertes si écarts

## Objectifs par Segment

| Segment | Marge Brute Cible | Marge Nette Cible |
|---------|-------------------|-------------------|
| Projets forfait | 45% | 30% |
| Projets régie | 40% | 28% |
| Maintenance | 55% | 40% |
| Conseil | 50% | 35% |
| Formation | 60% | 45% |

## Structure de Coûts

```
Revenus (100%)
├── Coûts directs (55-60%)
│   ├── Salaires production
│   └── Sous-traitance
├── Coûts indirects (15-20%)
│   ├── Commercial
│   ├── Admin
│   └── Direction
└── Marge nette (20-30%)
```

## Seuils d'Alerte

| Niveau | Marge | Action |
|--------|-------|--------|
| 🟢 OK | > 30% | Aucune |
| 🟡 Attention | 25-30% | Surveillance |
| 🟠 Alerte | 20-25% | Plan d'action |
| 🔴 Critique | < 20% | Intervention immédiate |

## Escalade

→ `direction-commerciale/orchestrator` si marge globale < 25%
