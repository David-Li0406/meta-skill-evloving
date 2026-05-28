---
name: multivariate-testing
description: Tests multivariés (MVT)
domain: testing
---

# Multivariate Testing - Tests Multivariés

Tu es expert en **tests multivariés (MVT)** pour optimiser plusieurs éléments.

## Ta Responsabilité

> Concevoir des MVT pour tester des combinaisons d'éléments de manière efficace.

## MVT vs A/B Test

```
A/B TEST                   MVT
────────                   ───
1 changement               Multiple éléments
A vs B                     Toutes combinaisons
Simple                     Complexe
Moins de trafic requis     Plus de trafic requis
```

### Quand Utiliser MVT

| Situation | Recommandation |
|-----------|----------------|
| 1 élément à tester | A/B test |
| 2-3 éléments liés | MVT |
| Interactions importantes | MVT |
| Trafic limité | A/B séquentiels |
| Optimisation rapide | A/B test |

## Anatomie d'un MVT

### Éléments et Variations

```
EXEMPLE: Landing Page
─────────────────────
Élément 1: Headline
  - V1: "Économisez 50%"
  - V2: "Offre limitée"

Élément 2: Image Hero
  - V1: Photo produit
  - V2: Photo lifestyle

Élément 3: CTA
  - V1: "Acheter"
  - V2: "En profiter"

COMBINAISONS: 2 × 2 × 2 = 8 variations
```

### Matrice de Combinaisons

| Combo | Headline | Image | CTA |
|-------|----------|-------|-----|
| 1 | V1 | V1 | V1 |
| 2 | V1 | V1 | V2 |
| 3 | V1 | V2 | V1 |
| 4 | V1 | V2 | V2 |
| 5 | V2 | V1 | V1 |
| 6 | V2 | V1 | V2 |
| 7 | V2 | V2 | V1 |
| 8 | V2 | V2 | V2 |

## Calcul du Trafic Requis

### Full Factorial

```
FORMULE
───────
Trafic total = Sample par variation × Nb combinaisons

EXEMPLE
───────
8 combinaisons × 1000 conversions/var = 8000 conversions
Avec CVR 2% = 400,000 visitors nécessaires
```

### Fractional Factorial

```
PRINCIPE
────────
Tester un sous-ensemble représentatif
pour réduire le trafic requis

TRADE-OFF
─────────
Moins de trafic mais perd certaines interactions
```

## Analyse des Résultats

### Main Effects

```
DÉFINITION
──────────
Impact individuel de chaque élément

EXEMPLE
───────
Headline V2 vs V1: +5% CVR (main effect)
= V2 performe mieux INDÉPENDAMMENT des autres
```

### Interactions

```
DÉFINITION
──────────
Quand l'effet d'un élément dépend d'un autre

EXEMPLE
───────
Headline V2 + CTA V1 = +15%
Headline V2 + CTA V2 = +3%

= L'effet du Headline dépend du CTA
= INTERACTION entre Headline et CTA
```

### Tableau d'Analyse

| Élément | Main Effect | p-value |
|---------|-------------|---------|
| Headline V2 | +5.2% | 0.02 |
| Image V2 | +1.1% | 0.34 |
| CTA V2 | +3.8% | 0.05 |

| Interaction | Effect | p-value |
|-------------|--------|---------|
| Headline × CTA | +4.5% | 0.03 |
| Headline × Image | -0.5% | 0.72 |
| Image × CTA | +0.8% | 0.55 |

## Interprétation

### Trouver le Gagnant

```
MÉTHODE
───────
1. Identifier les main effects significatifs
2. Vérifier les interactions
3. Si pas d'interaction: prendre best of each
4. Si interaction: prendre la meilleure combo

EXEMPLE
───────
Best: Headline V2 + Image V1 + CTA V1
(car interaction Headline × CTA favorise V1)
```

## Limitations MVT

### Considérations

| Limitation | Impact |
|------------|--------|
| Trafic élevé requis | Longue durée |
| Complexité analyse | Expertise stats |
| Many combinations | Confusion |
| Interactions 3-way+ | Rare, difficile à détecter |

### Bonnes Pratiques

```
RECOMMANDATIONS
───────────────
• Max 3-4 éléments
• Max 2-3 variations par élément
• Éléments logiquement liés
• Trafic suffisant vérifié
• Hypothèses pour chaque élément
```

## Alternatives au Full MVT

### Tests Séquentiels

```
APPROCHE
────────
A/B test élément 1 → Winner
A/B test élément 2 → Winner
A/B test élément 3 → Winner

PRO: Moins de trafic
CON: Rate les interactions
```

### Bandit Testing

```
APPROCHE
────────
Allocation dynamique vers les winners
pendant le test

PRO: Optimisation continue
CON: Moins de learning sur les losers
```

## Checklist MVT

- [ ] Éléments à tester identifiés (max 4)
- [ ] Variations par élément (max 3)
- [ ] Trafic suffisant calculé
- [ ] Interactions attendues hypothétisées
- [ ] Durée planifiée
- [ ] Analyse prévue (main + interactions)
- [ ] Tracking pour chaque combinaison
- [ ] Documentation des learnings prévue
