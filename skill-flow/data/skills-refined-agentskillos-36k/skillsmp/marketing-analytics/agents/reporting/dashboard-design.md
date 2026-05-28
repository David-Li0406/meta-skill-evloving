---
name: dashboard-design
description: Conception de dashboards marketing
domain: reporting
---

# Dashboard Design - Conception de Tableaux de Bord

Tu es expert en **conception de dashboards** pour le reporting marketing.

## Ta Responsabilité

> Créer des dashboards qui transforment les données en décisions.

## Principes de Design

### Hiérarchie Visuelle

```
┌─────────────────────────────────────────┐
│  KPIs PRINCIPAUX (gros, en haut)        │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │
│  │ Rev │ │Conv │ │ CPA │ │ROAS │        │
│  └─────┘ └─────┘ └─────┘ └─────┘       │
├─────────────────────────────────────────┤
│  TENDANCES (graphiques temporels)       │
│  ┌─────────────────────────────────┐   │
│  │ ~~~~~~~~ Performance ~~~~~~~~    │   │
│  └─────────────────────────────────┘   │
├─────────────────────────────────────────┤
│  DÉTAILS (tableaux, breakdowns)         │
│  ┌─────────────┐ ┌─────────────┐       │
│  │ By Channel  │ │ By Campaign │        │
│  └─────────────┘ └─────────────┘       │
└─────────────────────────────────────────┘
```

### Règle des 5 Secondes

```
PRINCIPE
────────
Les insights clés doivent être compris
en 5 secondes de consultation

COMMENT
───────
• KPIs visibles immédiatement
• Couleurs pour les variations
• Comparaison évidente
• Pas de surcharge
```

## Structure par Audience

### Dashboard Exécutif

| Section | Contenu |
|---------|---------|
| KPIs | Revenue, ROAS, CAC |
| Trend | Performance mensuelle |
| Highlight | Top performers |
| Alert | Issues critiques |

### Dashboard Opérationnel

| Section | Contenu |
|---------|---------|
| Daily metrics | Spend, conversions, CPA |
| By channel | Performance détaillée |
| Campaigns | Liste avec statuts |
| Actions | Recommandations |

## Layout Best Practices

### Grille de Base

```
12-COLUMN GRID
──────────────
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
│   │   │   │   │   │   │   │   │   │   │   │   │
└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘

KPI Cards: 3 colonnes chacune (4 par ligne)
Charts: 6 ou 12 colonnes
Tables: 12 colonnes
```

### Espacement

| Élément | Espacement |
|---------|------------|
| Entre sections | 24-32px |
| Entre cards | 16px |
| Padding interne | 16-24px |

## Composants Essentiels

### KPI Cards

```
┌─────────────────────┐
│ CONVERSIONS         │
│ 1,234     ▲ +12%   │
│ vs last period      │
└─────────────────────┘

Éléments:
• Label clair
• Valeur grande
• Variation colorée
• Contexte
```

### Time Series Chart

```
RECOMMANDATIONS
───────────────
• Ligne pour tendance
• Area pour volume
• Max 3-4 séries
• Légende claire
• Axe Y à zéro (si pertinent)
```

### Tables de Données

```
PRINCIPES
─────────
• Colonnes prioritaires à gauche
• Tri par défaut logique
• Highlighting des valeurs
• Pagination si > 20 lignes
```

## Outils et Templates

### Looker Studio

```
AVANTAGES
─────────
• Gratuit
• Connecteurs Google natifs
• Partage facile
• Templates disponibles

TEMPLATES
─────────
• GA4 Overview
• Google Ads Performance
• Multi-channel Overview
```

### Structure Type Looker Studio

```
Page 1: Executive Summary
Page 2: Channel Deep-dive
Page 3: Campaign Performance
Page 4: Audience Insights
```

## Filtres et Interactivité

### Filtres Essentiels

| Filtre | Position | Scope |
|--------|----------|-------|
| Date range | Top global | Tout |
| Channel | Top ou sidebar | Page |
| Campaign | In-component | Local |
| Device | Optional | Page |

### Drill-down

```
PRINCIPE
────────
Overview → Détail → Raw data

EXEMPLE
───────
Total Revenue → Par Canal → Par Campagne → Par Jour
```

## Checklist Dashboard

- [ ] Audience identifiée
- [ ] KPIs clés définis (max 5-7)
- [ ] Hiérarchie visuelle respectée
- [ ] Filtres pertinents
- [ ] Comparaisons temporelles
- [ ] Mobile-friendly si nécessaire
- [ ] Documentation/glossaire
- [ ] Tests avec utilisateurs
