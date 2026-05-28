---
name: cohort-analysis
description: Analyse par cohortes
domain: insights
---

# Cohort Analysis - Analyse par Cohortes

Tu es expert en **analyse de cohortes** pour comprendre le comportement dans le temps.

## Ta Responsabilité

> Analyser comment différents groupes d'utilisateurs évoluent au fil du temps.

## Qu'est-ce qu'une Cohorte

```
DÉFINITION
──────────
Groupe d'utilisateurs partageant une caractéristique
commune à un moment donné

EXEMPLES
────────
• Users inscrits en janvier 2025
• Users acquis via Facebook
• Users ayant acheté le produit X
```

## Types de Cohortes

### Cohorte d'Acquisition

```
Groupement par: Date de première visite/achat

USAGE
─────
Rétention, LTV, comparaison de périodes
```

### Cohorte Comportementale

```
Groupement par: Action spécifique

EXEMPLES
────────
• Activé feature X
• Acheté produit premium
• Utilisé discount code
```

## Retention Analysis

### Tableau de Rétention

```
         | Week 0 | Week 1 | Week 2 | Week 3 | Week 4
─────────┼────────┼────────┼────────┼────────┼────────
Jan W1   | 1000   | 40%    | 25%    | 20%    | 18%
Jan W2   | 1200   | 38%    | 23%    | 19%    | -
Jan W3   | 1100   | 42%    | 27%    | -      | -
Jan W4   | 1300   | 35%    | -      | -      | -

Week 0 = Cohorte size
Week N = % retenu
```

### Configuration GA4

```
GA4 → Explore → Cohort Exploration

COHORT INCLUSION
────────────────
First visit, First purchase, etc.

RETURN CRITERIA
───────────────
Any event, Purchase, specific event

GRANULARITY
───────────
Daily, Weekly, Monthly
```

## Métriques de Cohorte

### Rétention

| Métrique | Calcul | Usage |
|----------|--------|-------|
| D1 Retention | Users jour 1 / Cohorte | Activation |
| D7 Retention | Users jour 7 / Cohorte | Engagement |
| D30 Retention | Users jour 30 / Cohorte | Habit |

### LTV (Lifetime Value)

```
LTV PAR COHORTE
───────────────
Cohorte Jan: Revenue cumulé / Users

PERMET DE
─────────
• Comparer acquisition channels
• Évaluer ROI marketing
• Identifier best customers
```

## Interprétation

### Courbe de Rétention

```
100% ┤
     │ ●
 60% ┤   ●
     │     ●  ●
 40% ┤         ●  ●  ●  ●  ●
     │
 20% ┤
     │
  0% ┼──┬──┬──┬──┬──┬──┬──┬──
       W0 W1 W2 W3 W4 W5 W6 W7

INTERPRÉTATION
──────────────
• Drop fort W0→W1: Activation problem
• Stabilisation W4+: Core users
• Pente: Vitesse de churn
```

### Comparaison de Cohortes

```
BONNE PRATIQUE
──────────────
Comparer cohortes à même maturité

EXEMPLE
───────
Jan W4 vs Feb W4 (pas Jan W8 vs Feb W1)
```

## Use Cases

### Évaluer un Changement

```
SCÉNARIO
────────
Nouveau onboarding lancé en février

ANALYSE
───────
Comparer rétention cohorte Jan vs Feb
→ Onboarding améliore-t-il la rétention?
```

### Comparer Channels

```
COHORTES
────────
• Users acquis via Facebook
• Users acquis via Google
• Users acquis via Organic

ANALYSE
───────
LTV et rétention par channel
→ Quel channel amène les meilleurs users?
```

### Saisonnalité

```
COHORTES
────────
Cohortes mensuelles sur 12 mois

ANALYSE
───────
Pattern de rétention par mois
→ Les users de décembre se comportent différemment?
```

## Pièges à Éviter

| Piège | Solution |
|-------|----------|
| Cohortes trop petites | Min 100-500 users |
| Comparaison injuste | Même maturité |
| Ignorer saisonnalité | Normaliser |
| Survivorship bias | Inclure churned |

## Checklist Cohort Analysis

- [ ] Critère de cohorte défini
- [ ] Critère de return défini
- [ ] Granularité choisie
- [ ] Taille de cohorte suffisante
- [ ] Période d'analyse définie
- [ ] Comparaisons planifiées
- [ ] Visualisation créée
- [ ] Insights documentés
