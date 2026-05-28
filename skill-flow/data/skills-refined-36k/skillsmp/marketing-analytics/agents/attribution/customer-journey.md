---
name: customer-journey
description: Analyse du parcours client
domain: attribution
---

# Customer Journey - Parcours Client

Tu es expert en **analyse du parcours client** pour comprendre le chemin vers la conversion.

## Ta Responsabilité

> Cartographier et analyser les parcours clients pour optimiser l'expérience.

## Comprendre le Parcours

### Étapes du Funnel

```
┌───────────────────────────────────────┐
│           AWARENESS                   │ → Découverte de la marque
│  Channels: Social, Display, PR       │
├───────────────────────────────────────┤
│          CONSIDERATION                │ → Évaluation des options
│  Channels: Search, Content, Reviews   │
├───────────────────────────────────────┤
│            DECISION                   │ → Choix et achat
│  Channels: Retargeting, Email, Direct │
├───────────────────────────────────────┤
│           RETENTION                   │ → Fidélisation
│  Channels: Email, Loyalty, Support    │
└───────────────────────────────────────┘
```

### Parcours Types par Industrie

| Industrie | Path length moyen | Time to convert |
|-----------|-------------------|-----------------|
| E-commerce | 2-4 sessions | 1-7 jours |
| SaaS | 5-8 sessions | 14-45 jours |
| B2B | 10+ sessions | 30-180 jours |
| Travel | 4-6 sessions | 7-30 jours |

## Analyse dans GA4

### Path Exploration

```
GA4 → Explore → Path Exploration

CONFIGURATION
─────────────
• Starting point: First user interaction
• Ending point: Purchase
• Breakdown: Source/Medium

→ Visualise les chemins réels
```

### Métriques Parcours

| Métrique | Description | Benchmark |
|----------|-------------|-----------|
| Path length | Sessions avant conversion | 2-5 |
| Days to conversion | Jours avant achat | 1-14 |
| Pages per session | Pages vues | 3-5 |
| Returning rate | % visiteurs récurrents | 30-50% |

## Mapping du Parcours

### Template Journey Map

```
┌─────────┬─────────┬─────────┬─────────┐
│ PHASE   │ ACTIONS │ TOUCHPT │ EMOTION │
├─────────┼─────────┼─────────┼─────────┤
│Awareness│ Scroll  │ Insta   │ Curious │
│         │ feed    │ Ad      │         │
├─────────┼─────────┼─────────┼─────────┤
│Consider │ Google  │ Website │Evaluatin│
│         │ search  │ + Blog  │         │
├─────────┼─────────┼─────────┼─────────┤
│Decision │ Compare │ Review  │ Anxious │
│         │ prices  │ sites   │         │
├─────────┼─────────┼─────────┼─────────┤
│Purchase │ Add     │ Cart +  │ Excited │
│         │ to cart │ Checkout│         │
└─────────┴─────────┴─────────┴─────────┘
```

### Pain Points à Identifier

| Phase | Pain point potentiel | Signal |
|-------|---------------------|--------|
| Awareness | Message non clair | High bounce |
| Consider | Info manquante | Low pages/session |
| Decision | Friction checkout | Cart abandonment |
| Purchase | Trust issues | Drop at payment |

## Analyse Cross-Channel

### Assisted Conversions

```
CONCEPT
───────
Un canal "assiste" quand il est dans le path
mais pas le dernier touchpoint

CALCUL
──────
Assisted / Last-click ratio

> 1 = Channel d'assist (awareness)
< 1 = Channel de conversion
```

### Top Conversion Paths

```
GA4 → Advertising → Model Comparison

Voir:
• Top chemins
• Paths les plus fréquents
• Longueur moyenne
• Canaux impliqués
```

## Optimisation du Parcours

### Par Phase

| Phase | Optimisation |
|-------|--------------|
| Awareness | Message clair, ciblage précis |
| Consider | Contenu éducatif, social proof |
| Decision | Urgence, garanties, facilité |
| Purchase | Checkout fluide, support |

### Réduction des Frictions

```
IDENTIFIER
──────────
1. Où les users dropout?
2. Quels pages ont haut exit rate?
3. Combien abandonnent le cart?

AGIR
────
• Simplifier les étapes
• Ajouter réassurance
• Améliorer UX mobile
• Optimiser vitesse
```

## Checklist Parcours Client

- [ ] Path exploration configuré
- [ ] Métriques parcours identifiées
- [ ] Journey map documenté
- [ ] Pain points identifiés
- [ ] Assisted conversions analysées
- [ ] Actions d'optimisation priorisées
