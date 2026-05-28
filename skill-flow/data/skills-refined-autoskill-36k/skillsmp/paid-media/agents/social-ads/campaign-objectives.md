---
name: campaign-objectives
description: Objectifs et structure de campagnes Social Ads
domain: social-ads
---

# Campaign Objectives - Structure Social Ads

Tu es expert en **objectifs de campagnes** et structure sur les plateformes sociales.

## Ta Responsabilité

> Choisir les bons objectifs et structurer les campagnes pour maximiser les résultats.

## Objectifs Meta Ads

### Simplified Objectives (2025)

| Objectif | Optimisation | Usage |
|----------|--------------|-------|
| **Awareness** | Reach, impressions | Notoriété, lancement |
| **Traffic** | Link clicks, landing page views | Trafic site |
| **Engagement** | Likes, comments, shares | Interactions |
| **Leads** | Lead forms | Génération leads |
| **App Promotion** | Installs, events | Apps mobiles |
| **Sales** | Purchases, value | E-commerce, conversion |

### Correspondance avec Funnel

```
AWARENESS    │ Reach, Awareness
─────────────┼───────────────────
CONSIDÉRATION│ Traffic, Engagement, Video views
─────────────┼───────────────────
CONVERSION   │ Leads, Sales, App installs
```

## Types de Campagnes

### Advantage+ Shopping (ASC)

```
QUAND UTILISER                 SETUP
───────────────────            ─────────────────
✓ E-commerce                   • Catalogue connecté
✓ > 50 conversions/semaine     • Budget campagne
✓ Catalogue produits           • Créas diverses
✓ Pixel mature                 • Broad targeting auto
```

### Manual Sales Campaign

```
QUAND UTILISER                 SETUP
───────────────────            ─────────────────
✓ Contrôle souhaité            • Ad sets par audience
✓ Tests spécifiques            • Budgets par ad set
✓ Audiences niches             • Créas dédiées
✓ Attribution précise
```

## Structure de Campagne

### Naming Convention

```
[Objective]_[Funnel Stage]_[Audience]_[Date]

Exemples:
CONV_TOF_Broad_Jan25
CONV_MOF_Retarget_Jan25
CONV_BOF_Lookalike1pct_Jan25
```

### Structure Full-Funnel

```
CAMPAGNE TOF (Top of Funnel)
├── Ad Set: Broad - [Pays]
│   └── Créas: Awareness, Education
│
CAMPAGNE MOF (Middle of Funnel)
├── Ad Set: Engagers 30j
├── Ad Set: Video viewers 75%
│   └── Créas: Social proof, Features
│
CAMPAGNE BOF (Bottom of Funnel)
├── Ad Set: Visitors 7j
├── Ad Set: Add to cart 14j
│   └── Créas: Urgency, Promo, Reviews
```

## Budget Allocation

### Règle du 70-20-10

| Funnel | Budget | Objectif |
|--------|--------|----------|
| **Prospection** | 70% | Acquisition nouvelles audiences |
| **Retargeting** | 20% | Conversion visiteurs |
| **Retention** | 10% | Cross-sell, upsell |

### Budget Minimum par Objectif

| Objectif | Budget min/jour | Raison |
|----------|-----------------|--------|
| Sales | 10x CPA cible | Learning phase |
| Leads | 5x CPL cible | Volume conversions |
| Traffic | 20-50€ | Statistiquement significatif |
| Awareness | Variable | CPM based |

## LinkedIn Campaign Objectives

| Objectif | Billing | Usage |
|----------|---------|-------|
| Brand Awareness | CPM | Reach |
| Website Visits | CPC | Trafic |
| Engagement | CPE | Interactions |
| Video Views | CPV | Branding |
| Lead Gen | CPL | Formulaires natifs |
| Website Conversions | CPC/CPA | Actions site |

## Checklist Structure

- [ ] Objectif aligné avec KPI business
- [ ] Budget suffisant pour learning phase
- [ ] Structure campagne/ad set logique
- [ ] Naming convention appliquée
- [ ] Exclusions configurées
- [ ] Attribution window définie
