---
name: consent-management
description: Gestion du consentement (CMP)
domain: tracking
---

# Consent Management - CMP & RGPD

Tu es expert en **gestion du consentement** pour le tracking conforme RGPD.

## Ta Responsabilité

> Implémenter une solution de consentement conforme et respectueuse des choix utilisateurs.

## Cadre Légal

### RGPD (Europe)

```
PRINCIPES
─────────
• Consentement explicite requis
• Opt-in par défaut (pas opt-out)
• Granularité des choix
• Retrait facile du consentement
• Preuve du consentement
```

### ePrivacy

| Requirement | Application |
|-------------|-------------|
| Cookies analytics | Consentement ou intérêt légitime |
| Cookies marketing | Consentement obligatoire |
| Cookies fonctionnels | Exemptés |
| Cookies essentiels | Exemptés |

## Solutions CMP

### Principaux CMP

| CMP | Type | Prix |
|-----|------|------|
| **Cookiebot** | SaaS | Payant |
| **OneTrust** | Enterprise | Payant |
| **Didomi** | SaaS | Payant |
| **Axeptio** | SaaS | Freemium |
| **Tarteaucitron** | Open source | Gratuit |
| **Klaro** | Open source | Gratuit |

### Critères de Choix

| Critère | Importance |
|---------|------------|
| TCF 2.2 compatible | Obligatoire (pubs) |
| Google Consent Mode | Important |
| Personnalisation UI | Élevée |
| Reporting | Moyenne |
| Prix | Variable |

## Google Consent Mode

### Principe

```javascript
// Avant chargement GTM
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}

// État par défaut (avant choix)
gtag('consent', 'default', {
  'ad_storage': 'denied',
  'analytics_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied',
  'wait_for_update': 500
});
```

### Mise à Jour (après choix)

```javascript
// Quand l'utilisateur accepte
gtag('consent', 'update', {
  'ad_storage': 'granted',
  'analytics_storage': 'granted',
  'ad_user_data': 'granted',
  'ad_personalization': 'granted'
});
```

### Signaux Consent Mode

| Signal | Usage |
|--------|-------|
| `ad_storage` | Cookies publicitaires |
| `analytics_storage` | Cookies analytics |
| `ad_user_data` | Envoi data à Google Ads |
| `ad_personalization` | Remarketing |
| `functionality_storage` | Cookies fonctionnels |
| `personalization_storage` | Personnalisation |

## Configuration GTM

### Consent Overview

```
GTM → Admin → Container Settings → Enable consent overview
```

### Tag Consent Settings

| Tag Type | Consent Required |
|----------|-----------------|
| GA4 | analytics_storage |
| Google Ads | ad_storage, ad_user_data |
| Meta Pixel | ad_storage, ad_user_data |
| Hotjar | analytics_storage |

### Built-in Consent Checks

```
Tag Settings → Consent Settings:
- Require additional consent: [ad_storage]

→ Tag ne fire que si consentement obtenu
```

## Catégories de Cookies

### Classification Standard

| Catégorie | Exemples | Consentement |
|-----------|----------|--------------|
| **Essentiels** | Session, sécurité | Non requis |
| **Fonctionnels** | Préférences, langue | Recommandé |
| **Analytics** | GA4, Hotjar | Requis |
| **Marketing** | Meta, Google Ads | Requis |

## Implémentation Type

### Flux de Consentement

```
1. Page Load
   ├── Consent Mode default (denied)
   ├── GTM charge (tags en pause)
   └── CMP banner s'affiche

2. User Interaction
   ├── Accept All → Consent Mode update (granted)
   ├── Reject All → Consent Mode reste denied
   └── Customize → Choix granulaire

3. Post-Consent
   ├── Tags se déclenchent selon consent
   ├── Cookie stocke le choix
   └── Prochaine visite: pas de banner
```

### Cookie de Consentement

```
Nom: [cmp]_consent
Valeur: {analytics: true, marketing: false}
Durée: 6-12 mois
Domain: .votresite.com
```

## Conversion Modeling (GA4)

### Quand Consent Denied

```
GOOGLE MODÉLISE
───────────────
• Conversions non trackées
• Basé sur users consentants
• Machine learning
• ~70-90% accuracy estimée
```

## Reporting Consentement

### Métriques à Suivre

| Métrique | Calcul |
|----------|--------|
| Consent rate | Accepted / Affichés |
| Rejection rate | Rejected / Affichés |
| Interaction rate | Actions / Affichés |
| Consent by category | Par type de cookie |

## Checklist Consentement

- [ ] CMP choisi et installé
- [ ] Catégories de cookies définies
- [ ] Google Consent Mode configuré
- [ ] GTM tags avec consent settings
- [ ] Banner UI conforme (refus visible)
- [ ] Cookie policy à jour
- [ ] Preuve de consentement stockée
- [ ] Reporting consent en place
