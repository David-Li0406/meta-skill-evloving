---
name: pixel-implementation
description: Implémentation pixels de conversion
domain: tracking
---

# Pixel Implementation - Pixels de Conversion

Tu es expert en **implémentation de pixels** pour les plateformes publicitaires.

## Ta Responsabilité

> Installer et configurer les pixels de conversion pour une mesure précise.

## Pixels Principaux

### Meta Pixel

```javascript
// Base Code (via GTM ou direct)
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', 'PIXEL_ID');
```

### Events Meta Standards

| Event | Usage | Paramètres |
|-------|-------|------------|
| `PageView` | Toutes pages | - |
| `ViewContent` | Page produit | content_ids, value |
| `AddToCart` | Ajout panier | content_ids, value |
| `InitiateCheckout` | Début checkout | value, num_items |
| `Purchase` | Achat | value, currency, content_ids |
| `Lead` | Formulaire lead | - |
| `CompleteRegistration` | Inscription | - |

### LinkedIn Insight Tag

```javascript
// Base Code
_linkedin_partner_id = "PARTNER_ID";
window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
window._linkedin_data_partner_ids.push(_linkedin_partner_id);

// Conversion Event
window.lintrk('track', { conversion_id: CONVERSION_ID });
```

### TikTok Pixel

```javascript
// Base Code
!function (w, d, t) {
  w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];
  // ... (code complet)
  ttq.load('PIXEL_ID');
  ttq.page();
}(window, document, 'ttq');

// Event
ttq.track('CompletePayment', {
  value: 99.99,
  currency: 'EUR'
});
```

## Implémentation via GTM

### Tag Meta Pixel (Base)

```
Tag Type: Custom HTML
Trigger: All Pages (avec consent)

Code: [Meta Base Code avec init]
```

### Tag Meta Event

```
Tag Type: Custom HTML
Trigger: Custom Event - purchase

Code:
fbq('track', 'Purchase', {
  value: {{DLV - Transaction Value}},
  currency: 'EUR',
  content_ids: {{DLV - Product IDs}}
});
```

## Conversions API (Server-Side)

### Pourquoi Server-Side

```
AVANTAGES
─────────
• Bypass ad blockers
• Data quality améliorée
• First-party data
• Moins impacté par ITP/cookies
```

### Architecture CAPI

```
SITE → Server GTM → Meta CAPI
                  → LinkedIn CAPI
                  → TikTok Events API
```

### Déduplication

```
IMPORTANT
─────────
Event ID identique côté client ET serveur
= Meta déduplique automatiquement

fbq('track', 'Purchase', {...}, {eventID: 'unique_id'});
// Server envoie même event avec même eventID
```

## Testing Pixels

### Outils de Debug

| Plateforme | Outil |
|------------|-------|
| Meta | Events Manager > Test Events |
| LinkedIn | Insight Tag Helper (extension) |
| TikTok | Pixel Helper (extension) |
| Google | Tag Assistant |

### Vérifications

| Check | Comment |
|-------|---------|
| Pixel chargé | Extension + DevTools Network |
| Events reçus | Platform Events Manager |
| Paramètres corrects | Vérifier payload |
| Déduplication | Event ID présent |

## Paramètres E-commerce

### Standard Parameters

| Paramètre | Type | Exemple |
|-----------|------|---------|
| `value` | Number | 99.99 |
| `currency` | String | "EUR" |
| `content_ids` | Array | ["SKU123"] |
| `content_type` | String | "product" |
| `content_name` | String | "Nike Air Max" |
| `num_items` | Number | 2 |

### Enhanced Matching

```javascript
// Meta - Advanced Matching
fbq('init', 'PIXEL_ID', {
  em: 'hashed_email',
  ph: 'hashed_phone',
  fn: 'hashed_firstname',
  ln: 'hashed_lastname'
});
```

## Checklist Pixels

- [ ] Pixels base installés (toutes pages)
- [ ] Events de conversion configurés
- [ ] Paramètres e-commerce passés
- [ ] Enhanced matching activé si possible
- [ ] Server-side (CAPI) évalué
- [ ] Déduplication configurée
- [ ] Tests effectués dans chaque plateforme
- [ ] Consent mode respecté
