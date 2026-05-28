---
name: statistical-analysis
description: Analyse statistique des expériences
domain: testing
---

# Statistical Analysis - Analyse Statistique

Tu es expert en **analyse statistique** pour valider les résultats de tests.

## Ta Responsabilité

> Analyser les résultats de tests avec rigueur statistique.

## Concepts Fondamentaux

### Statistical Significance

```
DÉFINITION
──────────
Probabilité que le résultat ne soit pas dû au hasard

STANDARD
────────
95% (p-value < 0.05)
= 5% de chance que le résultat soit aléatoire
```

### P-Value

```
INTERPRÉTATION
──────────────
p = 0.05 → 5% de chance que différence = hasard
p = 0.01 → 1% de chance
p = 0.10 → 10% de chance (pas significatif à 95%)
```

### Confidence Interval

```
EXEMPLE
───────
CVR Variant B: 3.2% [2.8% - 3.6%]

INTERPRÉTATION
──────────────
On est confiant à 95% que la vraie valeur
est entre 2.8% et 3.6%
```

## Types d'Erreurs

### Erreur Type I (Faux Positif)

```
DÉFINITION
──────────
Déclarer un gagnant alors qu'il n'y a pas de différence réelle

RISQUE
──────
α = 5% si significance = 95%

COMMENT RÉDUIRE
───────────────
• Augmenter le seuil de significance (99%)
• Attendre plus de données
```

### Erreur Type II (Faux Négatif)

```
DÉFINITION
──────────
Ne pas détecter un effet réel

RISQUE
──────
β = 20% si power = 80%

COMMENT RÉDUIRE
───────────────
• Augmenter sample size
• Tester des changements plus grands
```

## Power Analysis

### Qu'est-ce que le Power

```
POWER = 1 - β
─────────────
Probabilité de détecter un effet s'il existe

STANDARD: 80% minimum
```

### Facteurs Affectant le Power

| Facteur | Impact |
|---------|--------|
| Sample size | ↑ size = ↑ power |
| Effect size | ↑ effet = ↑ power |
| Variance | ↓ variance = ↑ power |
| Significance level | ↓ α = ↓ power |

## Analyse des Résultats

### Interprétation

```
RÉSULTAT                   ACTION
────────                   ──────
Significatif + Direction   → Implémenter
Significatif + Négatif     → Rejeter variant
Non significatif           → Pas de conclusion
                            (manque de données)
```

### Template de Résultat

```
TEST: [Nom du test]
DURÉE: [Dates]
SAMPLE: Control: X,XXX | Variant: X,XXX

RÉSULTATS:
──────────
Métrique: Conversion Rate

Control: 2.45%
Variant: 2.78%

Lift: +13.5%
CI 95%: [+5.2%, +21.8%]
p-value: 0.008
Significance: 99.2%

CONCLUSION: Statistiquement significatif
RECOMMANDATION: Implémenter Variant
```

## Pièges Statistiques

### Peeking Problem

```
PROBLÈME
────────
Regarder les résultats trop tôt
= Décisions sur données incomplètes
= Inflation des faux positifs

SOLUTION
────────
• Définir durée AVANT
• Utiliser sequential testing si besoin
• Ne pas arrêter au premier "winner"
```

### Multiple Testing

```
PROBLÈME
────────
5 métriques × 4 segments = 20 comparaisons
Risque de faux positif: 1 - 0.95^20 = 64%

SOLUTIONS
─────────
• Correction de Bonferroni
• Pre-register les analyses
• 1 métrique primaire
```

## Bayesian vs Frequentist

### Approche Fréquentiste

```
• P-value et significance
• Réponse: "Significatif ou non"
• Sample size fixe à l'avance
• Standard dans l'industrie
```

### Approche Bayésienne

```
• Probability to be best
• Réponse: "X% de chance que B soit meilleur"
• Plus intuitif
• Permet l'early stopping
```

## Outils d'Analyse

| Outil | Type | Usage |
|-------|------|-------|
| Calculateurs en ligne | Simple | Quick checks |
| Excel/Sheets | Manuel | Analyses custom |
| Python (scipy) | Code | Analyses avancées |
| R | Code | Analyses statistiques |
| Outils A/B natifs | Intégré | Résultats automatiques |

## Checklist Analyse Statistique

- [ ] Sample size suffisant
- [ ] Durée minimum respectée
- [ ] P-value < 0.05 (ou seuil défini)
- [ ] Confidence intervals calculés
- [ ] Segments analysés (avec prudence)
- [ ] Métriques guardrail vérifiées
- [ ] Documentation des résultats
- [ ] Recommandation claire
