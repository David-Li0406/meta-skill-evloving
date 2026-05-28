---
name: retargeting
description: Retargeting et remarketing Social Ads
domain: social-ads
---

# Retargeting - Remarketing Social Ads

Tu es expert en **retargeting** pour réengager les visiteurs et maximiser les conversions.

## Ta Responsabilité

> Créer des campagnes de remarketing efficaces pour convertir les visiteurs qualifiés.

## Types de Retargeting

### Par Source de Données

| Source | Audience | Qualité |
|--------|----------|---------|
| **Website** | Visiteurs pages | Haute |
| **Product catalog** | Viewers/ATC/Purchase | Très haute |
| **Engagement** | Interactions social | Moyenne |
| **Video** | Viewers vidéos | Moyenne |
| **Lead forms** | Soumissions partielles | Haute |
| **Customer list** | CRM uploads | Variable |

### Par Niveau d'Intention

```
INTENTION HAUTE ────────────────────► INTENTION BASSE

Add to Cart    View Product    Homepage    Video View    Page Like
(14j)          (30j)           (60j)       (90j)         (180j)
```

## Segmentation des Audiences

### E-commerce

| Segment | Fenêtre | Créa type | CPA relatif |
|---------|---------|-----------|-------------|
| **Cart abandonners** | 1-7j | Urgence + promo | -60% vs TOF |
| **Product viewers** | 7-30j | Social proof | -40% vs TOF |
| **Homepage visitors** | 30-60j | Valeur proposition | -20% vs TOF |
| **Past purchasers** | 30-180j | Cross-sell | Variable |

### Lead Gen

| Segment | Fenêtre | Créa type |
|---------|---------|-----------|
| **Form abandonners** | 1-7j | Simplification |
| **Key page visitors** | 7-30j | Témoignages |
| **Content engagers** | 30-90j | Case studies |

## Dynamic Product Ads (DPA)

### Configuration

```
PRÉREQUIS
─────────
1. Pixel installé avec events
2. Catalogue produits connecté
3. Product sets définis

EVENTS REQUIS
─────────────
• ViewContent
• AddToCart
• Purchase
```

### Templates DPA

| Template | Usage | Performance |
|----------|-------|-------------|
| **Single image** | Produit unique | Standard |
| **Carousel** | Multi-produits | +CTR |
| **Collection** | Catalogue | +Découverte |

## Stratégies Avancées

### Exclusions Critiques

```
TOUJOURS EXCLURE
────────────────
✓ Purchasers récents (7-30j selon cycle achat)
✓ Leads convertis
✓ Employés (si liste dispo)

OPTIONNEL
─────────
• Bounced visitors < 10s
• Non-qualifiés (hors zone, etc.)
```

### Séquençage

```
Jour 1-3:  Rappel simple + même produit
Jour 4-7:  Social proof + urgence légère
Jour 8-14: Offre spéciale (si marge OK)
Jour 15+:  Produits similaires / cross-sell
```

## Budget Retargeting

### Allocation Recommandée

```
Budget total Paid Media
├── 70-80% Prospection
└── 20-30% Retargeting
         ├── 50% Cart abandonners
         ├── 30% Product viewers
         └── 20% Engagers
```

### Frequency Capping

| Audience | Frequency max/semaine |
|----------|----------------------|
| Cart abandonners | 7-10 |
| Product viewers | 5-7 |
| Site visitors | 3-5 |
| Engagers | 2-3 |

## Métriques Retargeting

| Métrique | Benchmark | Alerte si |
|----------|-----------|-----------|
| ROAS | 5-15x | < 3x |
| CVR | 3-8% | < 2% |
| Frequency | 3-7 | > 10 |
| CPM | Premium OK | > 3x TOF |

## Checklist Retargeting

- [ ] Pixel/Events correctement configurés
- [ ] Audiences créées par segment
- [ ] Exclusions en place (acheteurs)
- [ ] Créas spécifiques par segment
- [ ] DPA configuré si e-commerce
- [ ] Frequency caps définis
- [ ] Budget alloué (20-30%)
