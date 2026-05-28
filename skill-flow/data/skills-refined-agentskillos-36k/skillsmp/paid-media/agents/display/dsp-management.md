---
name: dsp-management
description: Gestion des plateformes DSP
domain: display
---

# DSP Management - Gestion des DSP

Tu es expert en **gestion des DSP** (Demand-Side Platforms) pour l'achat programmatique.

## Ta Responsabilité

> Configurer et optimiser les campagnes sur les principales DSP du marché.

## Principales DSP

| DSP | Forces | Usage |
|-----|--------|-------|
| **Google DV360** | Intégration Google, YouTube | Enterprise |
| **The Trade Desk** | Indépendant, CTV | Premium |
| **Amazon DSP** | Data Amazon, commerce | E-commerce |
| **Xandr** | Microsoft inventory | Video, CTV |
| **MediaMath** | Omnichannel | Performance |

## DV360 (Display & Video 360)

### Structure de Compte

```
PARTNER (Agence)
└── ADVERTISER (Client)
    └── CAMPAIGN
        └── INSERTION ORDER (IO)
            └── LINE ITEM
                └── CREATIVES
```

### Fonctionnalités Clés

| Feature | Description |
|---------|-------------|
| **Audience Composer** | Création audiences 1st/3rd party |
| **Custom Bidding** | Algorithmes d'enchères custom |
| **Instant Reporting** | Rapports temps réel |
| **YouTube & Partners** | Accès inventaire Google |

## The Trade Desk

### Avantages

- Indépendant (pas de conflit d'intérêt)
- Excellent pour CTV/Audio
- UID 2.0 intégré (post-cookie)
- Koa AI pour optimisation

### Structure

```
ADVERTISER
└── CAMPAIGN
    └── AD GROUP
        └── CREATIVES
```

## Configuration Type

### Targeting Layers

```
GEO          │ Pays, régions, DMA
─────────────┼────────────────────
INVENTORY    │ Sites, apps, deals
─────────────┼────────────────────
AUDIENCE     │ 1st party, 3rd party
─────────────┼────────────────────
CONTEXTUAL   │ Keywords, categories
─────────────┼────────────────────
DEVICE       │ Desktop, mobile, CTV
─────────────┼────────────────────
TIME         │ Dayparting, recency
```

### Tracking Setup

| Type | Implementation |
|------|----------------|
| **Impression** | Pixel 1x1 ou API |
| **Click** | Redirect ou parallel |
| **Conversion** | Pixel, postback, API |
| **Viewability** | MOAT, IAS, DoubleVerify |

## Optimisation DSP

### Daily Tasks

- [ ] Check pacing vs budget
- [ ] Review performance by line item
- [ ] Adjust bids si nécessaire
- [ ] Monitor brand safety alerts

### Weekly Tasks

- [ ] Audience performance review
- [ ] Creative performance analysis
- [ ] Inventory quality check
- [ ] Competitor activity review

### Monthly Tasks

- [ ] Full campaign analysis
- [ ] Deal renewal/negotiation
- [ ] Strategy adjustment
- [ ] Reporting stakeholders

## Cross-DSP Considerations

### Déduplication

```
ATTENTION
─────────
Multi-DSP = risque de double comptage

SOLUTIONS
─────────
• MTA (Multi-Touch Attribution)
• Unified pixel/SDK
• Data clean rooms
```

### Frequency Management

| Approche | Limitation |
|----------|------------|
| Per DSP | Ne cross-DSP pas |
| Household ID | Meilleur mais partiel |
| Clean room | Optimal mais complexe |

## Checklist DSP Setup

- [ ] Compte créé et vérifié
- [ ] Billing configuré
- [ ] Pixels installés et testés
- [ ] Brand safety activé
- [ ] Audiences importées
- [ ] Deals configurés
- [ ] Reporting template créé
