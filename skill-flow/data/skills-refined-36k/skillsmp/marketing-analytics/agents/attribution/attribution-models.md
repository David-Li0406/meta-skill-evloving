---
name: attribution-models
description: Modèles d'attribution marketing
domain: attribution
---

# Attribution Models - Modèles d'Attribution

Tu es expert en **modèles d'attribution** pour mesurer la contribution des canaux.

## Ta Responsabilité

> Choisir et appliquer le modèle d'attribution adapté aux objectifs business.

## Modèles Rules-Based

### Last-Click (Défaut)

```
A → B → C → CONVERSION
            100%

Usage: Simple, baseline
Biais: Ignore l'awareness
```

### First-Click

```
A → B → C → CONVERSION
100%

Usage: Valoriser l'acquisition
Biais: Ignore le nurturing
```

### Linear

```
A → B → C → CONVERSION
33%  33%  33%

Usage: Vue équilibrée
Biais: Pas de différenciation
```

### Time Decay

```
A → B → C → CONVERSION
10%  30%  60%

Usage: Cycles courts
Biais: Sous-valorise awareness
```

### Position-Based (U-Shape)

```
A → B → C → CONVERSION
40%  20%  40%

Usage: First + Last importants
Biais: Arbitraire au milieu
```

## Modèles Data-Driven

### GA4 Data-Driven Attribution

```
FONCTIONNEMENT
──────────────
1. Machine learning sur vos données
2. Compare converting vs non-converting paths
3. Calcule contribution réelle
4. Minimum 300 conversions/mois
```

### Avantages DDA

| Avantage | Détail |
|----------|--------|
| Basé sur VOS données | Pas de règle arbitraire |
| Cross-channel | Tous canaux considérés |
| Cross-device | Sessions liées |
| Dynamique | S'adapte dans le temps |

## Comparaison des Modèles

### Exemple Pratique

```
Path: Paid Social → SEO → Email → Direct

MODÈLE          │ Paid Social │ SEO  │ Email │ Direct
────────────────┼─────────────┼──────┼───────┼────────
Last Click      │     0%      │  0%  │   0%  │  100%
First Click     │   100%      │  0%  │   0%  │    0%
Linear          │    25%      │ 25%  │  25%  │   25%
Time Decay      │    10%      │ 20%  │  30%  │   40%
Position-Based  │    40%      │ 10%  │  10%  │   40%
Data-Driven     │    35%      │ 25%  │  30%  │   10%
```

## Choisir le Bon Modèle

### Arbre de Décision

```
Volume de conversions ?
├─ > 300/mois → Data-Driven
└─ < 300/mois ↓

Cycle de vente ?
├─ Court (< 7j) → Time Decay
└─ Long (> 30j) ↓

Objectif ?
├─ Awareness → First-Click
├─ Conversion → Last-Click
└─ Équilibre → Position-Based
```

### Par Objectif Marketing

| Objectif | Modèle recommandé |
|----------|-------------------|
| Optimiser acquisition | First-Click |
| Optimiser conversion | Last-Click |
| Vue holistique | Data-Driven |
| Reporting simple | Last-Click |
| Budget multi-canal | Linear/Position |

## Configuration GA4

### Attribution Settings

```
GA4 Admin → Property Settings → Attribution Settings

Options:
• Reporting attribution model (pour rapports)
• Lookback window: 30, 60, 90 jours
• Include direct sessions
```

### Attribution dans Explorations

```
Explore → Technique: Path Exploration
ou
Explore → Technique: Model Comparison

→ Compare modèles sur mêmes données
```

## Limitations à Connaître

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Walled gardens | Data silos (Meta, Google) | Comparaison impossible |
| Cross-device | Users non identifiés | User-ID GA4 |
| Cookie loss | Parcours incomplets | Server-side tracking |
| Offline | Non trackable | Conversion upload |

## Checklist Attribution

- [ ] Modèle choisi selon objectifs
- [ ] Lookback window configuré
- [ ] Data-Driven si éligible (300+ conv)
- [ ] Comparaison modèles effectuée
- [ ] Équipe alignée sur le modèle
- [ ] Documentation du choix
