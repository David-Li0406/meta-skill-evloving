---
name: touchpoint-analysis
description: Analyse des points de contact
domain: attribution
---

# Touchpoint Analysis - Points de Contact

Tu es expert en **analyse des touchpoints** pour comprendre chaque interaction marketing.

## Ta Responsabilité

> Analyser l'impact et la valeur de chaque point de contact dans le parcours.

## Définition d'un Touchpoint

```
TOUCHPOINT
──────────
Toute interaction mesurable entre
un prospect/client et la marque

EXEMPLES
────────
• Clic sur une pub
• Visite site organique
• Ouverture email
• Appel téléphonique
• Visite magasin
```

## Catégorisation des Touchpoints

### Par Canal

| Canal | Touchpoints |
|-------|-------------|
| **Paid** | Display click, Search click, Social ad |
| **Organic** | SEO visit, Social organic, Referral |
| **Direct** | Direct visit, Bookmark |
| **Email** | Email open, Email click |
| **Offline** | Store visit, Call, Event |

### Par Funnel Stage

| Stage | Touchpoints typiques |
|-------|---------------------|
| **Awareness** | Display impression, Social video view |
| **Interest** | Blog visit, Content download |
| **Consider** | Product page, Review check |
| **Intent** | Add to cart, Wishlist |
| **Purchase** | Checkout, Purchase |

## Métriques par Touchpoint

### Engagement Metrics

| Métrique | Calcul | Usage |
|----------|--------|-------|
| Reach | Users exposés | Awareness |
| Impressions | Vues totales | Volume |
| CTR | Clics / Impressions | Attractivité |
| Engagement rate | Interactions / Reach | Intérêt |

### Conversion Metrics

| Métrique | Calcul | Usage |
|----------|--------|-------|
| Conversion rate | Conv / Sessions | Efficacité |
| Assisted conv. | Conv assistées | Contribution |
| Time to conv. | Jours avant achat | Velocity |
| Path position | Où dans le path | Rôle |

## Analyse dans GA4

### User Acquisition vs Traffic Acquisition

```
GA4 → Reports → Acquisition

USER ACQUISITION
────────────────
Premier touchpoint de l'utilisateur
→ Comment ils vous ont DÉCOUVERT

TRAFFIC ACQUISITION
───────────────────
Source de chaque session
→ Ce qui les RAMÈNE
```

### Multi-Channel Analysis

```
GA4 → Advertising → Attribution Paths

Voir:
• Touchpoints par conversion
• Rôle de chaque canal
• Temps entre touchpoints
```

## Scoring des Touchpoints

### Méthode Simple

| Critère | Poids | Score 1-5 |
|---------|-------|-----------|
| Volume | 20% | Reach du touchpoint |
| Engagement | 25% | Interaction rate |
| Conversion impact | 35% | Contribution conv. |
| Cost efficiency | 20% | ROI du touchpoint |

### Calcul de Valeur

```
TOUCHPOINT VALUE
────────────────
= (Attributed Revenue × Attribution %) / Coût

Exemple:
100K€ revenue × 30% attribution = 30K€
Coût du touchpoint = 10K€
Valeur = 30K€ / 10K€ = 3x ROI
```

## Optimisation des Touchpoints

### Par Performance

| Catégorie | Action |
|-----------|--------|
| **High value, low cost** | Scale up |
| **High value, high cost** | Optimize |
| **Low value, low cost** | Test/maintain |
| **Low value, high cost** | Cut/rethink |

### Séquençage Optimal

```
IDENTIFIER
──────────
1. Quels touchpoints déclenchent l'intérêt?
2. Lesquels convertissent?
3. Quel ordre fonctionne?

OPTIMISER
─────────
• Renforcer les touchpoints clés
• Améliorer la séquence
• Réduire les frictions entre
```

## Touchpoints Offline

### Intégration Offline

| Touchpoint | Méthode de tracking |
|------------|-------------------|
| Store visit | Store visits GA4 |
| Phone call | Call tracking |
| Event | Lead capture |
| Direct mail | UTM + codes |

### Unification Online/Offline

```
APPROCHES
─────────
• CRM integration
• Customer data platform
• Unified customer ID
• Survey attribution
```

## Checklist Touchpoints

- [ ] Touchpoints inventoriés
- [ ] Catégorisation complète
- [ ] Métriques par touchpoint
- [ ] Scoring de valeur
- [ ] Analyse des séquences
- [ ] Optimisations identifiées
- [ ] Offline intégré si applicable
