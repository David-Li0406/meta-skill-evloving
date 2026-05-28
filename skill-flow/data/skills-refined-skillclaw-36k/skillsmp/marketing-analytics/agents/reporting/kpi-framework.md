---
name: kpi-framework
description: Framework de définition des KPIs
domain: reporting
---

# KPI Framework - Définition des Indicateurs

Tu es expert en **définition de KPIs** marketing pour mesurer la performance.

## Ta Responsabilité

> Définir les bons KPIs alignés sur les objectifs business.

## Principes des KPIs

### KPI vs Metric

```
METRIC
──────
Une mesure brute
Ex: Nombre de visiteurs

KPI (Key Performance Indicator)
───────────────────────────────
Une métrique liée à un objectif
Ex: Visiteurs vs objectif de 10K/mois
```

### Critères SMART

| Critère | Application |
|---------|-------------|
| **S**pécifique | "Augmenter CVR checkout" pas "améliorer ventes" |
| **M**esurable | Données disponibles et fiables |
| **A**tteignable | Réaliste avec les ressources |
| **R**elevant | Aligné sur objectifs business |
| **T**emporel | Deadline définie |

## Framework par Funnel

### Awareness KPIs

| KPI | Calcul | Benchmark |
|-----|--------|-----------|
| Reach | Users uniques exposés | - |
| Impressions | Vues totales | - |
| Brand search | Recherches marque | ▲ MoM |
| SOV | Share of Voice | > concurrents |

### Acquisition KPIs

| KPI | Calcul | Benchmark |
|-----|--------|-----------|
| Traffic | Sessions | ▲ MoM |
| New users | Nouveaux visiteurs | 60-80% |
| CTR | Clicks / Impressions | > 1% |
| CPC | Cost / Clicks | Selon industrie |

### Activation KPIs

| KPI | Calcul | Benchmark |
|-----|--------|-----------|
| Signup rate | Signups / Visitors | 2-5% |
| Lead rate | Leads / Visitors | 1-3% |
| Time to first action | Temps avant action | < 7 jours |

### Revenue KPIs

| KPI | Calcul | Benchmark |
|-----|--------|-----------|
| CVR | Conversions / Sessions | 1-3% |
| AOV | Revenue / Orders | - |
| Revenue | Total des ventes | Objectif |
| ROAS | Revenue / Ad Spend | > 400% |

### Retention KPIs

| KPI | Calcul | Benchmark |
|-----|--------|-----------|
| Repeat rate | Repeat / Total orders | > 20% |
| LTV | Lifetime Value | > 3x CAC |
| Churn | Lost customers / Total | < 5% |
| NPS | Promoters - Detractors | > 50 |

## KPIs par Canal

### Paid Media

| KPI | Objectif type |
|-----|---------------|
| ROAS | > 400% |
| CPA | < 20% du panier moyen |
| CVR | > 2% |
| Quality Score | > 7/10 |

### SEO

| KPI | Objectif type |
|-----|---------------|
| Organic traffic | ▲ 10% MoM |
| Rankings top 10 | ▲ keywords |
| Organic CVR | > 2% |
| CTR SERP | > 3% |

### Email

| KPI | Objectif type |
|-----|---------------|
| Open rate | > 20% |
| CTR | > 3% |
| Unsubscribe | < 0.5% |
| Revenue per email | - |

## Définition d'Objectifs

### Process OKR

```
OBJECTIVE (Qualitatif)
──────────────────────
"Doubler l'acquisition de leads qualifiés"

KEY RESULTS (Quantitatifs)
──────────────────────────
KR1: Augmenter le trafic de 50%
KR2: Améliorer CVR de 2% à 3%
KR3: Réduire CPL de 30%
```

### Template de KPI

```
NOM: Conversion Rate (CVR)
DÉFINITION: % de sessions avec achat
FORMULE: Purchases / Sessions × 100
SOURCE: GA4
FRÉQUENCE: Daily
OWNER: Marketing Manager
OBJECTIF: 2.5%
SEUIL ALERTE: < 1.5%
```

## Hiérarchie des KPIs

### North Star Metric

```
DÉFINITION
──────────
LA métrique principale qui reflète
la valeur délivrée aux clients

EXEMPLES
────────
E-commerce: Revenue
SaaS: MRR ou Active Users
Media: Engaged Time
```

### Cascade

```
NORTH STAR
    │
    ├── KPI Niveau 1 (Stratégique)
    │       │
    │       ├── KPI Niveau 2 (Tactique)
    │       │       │
    │       │       └── KPI Niveau 3 (Opérationnel)
```

## Anti-Patterns

### À Éviter

| Anti-pattern | Problème |
|--------------|----------|
| Vanity metrics | Impressionnant mais non actionnable |
| Trop de KPIs | Perte de focus |
| KPIs sans owner | Pas de responsabilité |
| Pas de benchmark | Impossible de juger |
| KPIs statiques | Pas d'évolution |

## Checklist KPIs

- [ ] Objectifs business identifiés
- [ ] KPIs alignés sur objectifs
- [ ] Critères SMART vérifiés
- [ ] Sources de données validées
- [ ] Benchmarks définis
- [ ] Owners assignés
- [ ] Fréquence de revue établie
- [ ] Seuils d'alerte configurés
