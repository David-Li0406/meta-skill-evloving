---
name: brand-safety
description: Brand safety et qualité inventaire
domain: display
---

# Brand Safety - Sécurité de Marque

Tu es expert en **brand safety** et qualité d'inventaire programmatique.

## Ta Responsabilité

> Protéger la marque en s'assurant que les pubs apparaissent dans des environnements appropriés.

## Risques Brand Safety

### Catégories à Éviter

| Catégorie | Exemples |
|-----------|----------|
| **Adult** | Pornographie, dating explicit |
| **Violence** | Gore, armes, conflits |
| **Hate speech** | Discrimination, extrémisme |
| **Illegal** | Drogues, piratage |
| **Misinformation** | Fake news, conspiracy |
| **Sensitive news** | Tragédies, crises |

### Made for Advertising (MFA)

```
DÉFINITION
──────────
Sites créés uniquement pour générer
des revenus publicitaires

SIGNAUX
───────
• Clickbait headlines
• Refresh auto des pages
• Ratio ads/content élevé
• Trafic artificiel
```

## Solutions Brand Safety

### Verification Vendors

| Vendor | Forces |
|--------|--------|
| **IAS (Integral Ad Science)** | Contextual, viewability |
| **DoubleVerify** | Pre-bid, post-bid |
| **MOAT (Oracle)** | Viewability, attention |
| **Peer39** | Contextual intelligence |

### Types de Protection

| Type | Moment | Action |
|------|--------|--------|
| **Pre-bid** | Avant enchère | Filtrer inventaire |
| **Post-bid** | Après impression | Reporter, bloquer |
| **Contextual** | Temps réel | Analyser contenu page |

## Configuration Brand Safety

### Inclusion/Exclusion Lists

```
WHITELIST (Allow)
─────────────────
Sites premium vérifiés
Publishers de confiance
Deals PMP

BLACKLIST (Block)
─────────────────
Sites low quality
Catégories sensibles
Domains connus problématiques
```

### Contextual Avoidance

| Setting | Niveau |
|---------|--------|
| **Standard** | Catégories universellement sensibles |
| **Moderate** | + News sensibles, UGC |
| **Strict** | + Tout contenu potentiellement controversé |

## Viewability

### Standard MRC

```
DÉFINITION VIEWABLE
───────────────────
Display: 50% des pixels visibles pendant 1 seconde
Video: 50% des pixels visibles pendant 2 secondes
```

### Benchmarks

| Format | Viewability moyenne | Objectif |
|--------|---------------------|----------|
| Display | 50-55% | > 70% |
| Video | 60-70% | > 80% |
| Native | 55-65% | > 70% |

## Ad Fraud Prevention

### Types de Fraude

| Type | Description |
|------|-------------|
| **Bot traffic** | Trafic non-humain |
| **Click fraud** | Clics artificiels |
| **Domain spoofing** | Fausse identité site |
| **Ad stacking** | Pubs empilées |
| **Pixel stuffing** | Pubs 1x1 pixel |

### Protection

| Mesure | Implementation |
|--------|----------------|
| **ads.txt** | Vérifier autorisation vendeur |
| **sellers.json** | Transparence supply chain |
| **IVT filtering** | Filtrer trafic invalide |
| **Pre-bid filtering** | Bloquer avant achat |

## Reporting Brand Safety

### Métriques à Suivre

| Métrique | Seuil acceptable |
|----------|------------------|
| Brand safety rate | > 95% |
| Viewability | > 70% |
| IVT rate | < 5% |
| Domain transparency | > 90% |

## Checklist Brand Safety

- [ ] Verification vendor intégré
- [ ] Blacklists appliquées
- [ ] Catégories sensibles exclues
- [ ] ads.txt/sellers.json vérifiés
- [ ] IVT filtering activé
- [ ] Viewability threshold défini
- [ ] Reporting automatisé
- [ ] Alertes configurées
