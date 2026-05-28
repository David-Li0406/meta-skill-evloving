---
name: server-side
description: Tracking server-side
domain: tracking
---

# Server-Side Tracking

Tu es expert en **tracking server-side** pour une collecte de données résiliente.

## Ta Responsabilité

> Implémenter un tracking server-side pour améliorer la qualité des données.

## Pourquoi Server-Side

### Problèmes du Client-Side

```
LIMITATIONS ACTUELLES
─────────────────────
• Ad blockers (30-40% users)
• ITP Safari (7 jours cookies)
• Firefox ETP
• Navigateurs privacy-first
• Perte de données 20-40%
```

### Avantages Server-Side

| Avantage | Impact |
|----------|--------|
| Bypass ad blockers | +20-40% data |
| First-party cookies | Durée étendue |
| Data quality | Plus fiable |
| Sécurité | Données côté serveur |
| Contrôle | Filtrage, enrichissement |

## Architecture Server-Side

### Flow de Données

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   BROWSER   │────►│  SERVER GTM │────►│  ENDPOINTS  │
│   (Client)  │     │  (Cloud)    │     │  (GA4, Meta)│
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │
       │                   ├─► GA4 Measurement Protocol
       │                   ├─► Meta Conversions API
       │                   ├─► LinkedIn CAPI
       │                   └─► TikTok Events API
       │
       └─► First-party domain (subdomain)
```

### Server GTM (sGTM)

```
HÉBERGEMENT OPTIONS
───────────────────
• Google Cloud Run (recommandé)
• App Engine
• AWS
• Azure
• Stape.io (managed)
```

## Configuration Server GTM

### 1. Créer Container Server

```
GTM → Admin → Create Container
Container Type: Server
```

### 2. Déployer sur Cloud Run

```
1. Lier projet Google Cloud
2. Provisioner automatiquement
3. Configurer custom domain
   → tracking.votresite.com
```

### 3. Client GA4

```
Client Type: GA4
Mesurement ID: G-XXXXXX

→ Reçoit les hits GA4 client-side
→ Les transmet à GA4
```

### 4. Tags Server-Side

| Tag | Destination |
|-----|-------------|
| GA4 | Measurement Protocol |
| Meta CAPI | Conversions API |
| LinkedIn | CAPI |

## Implémentation Hybride

### Approche Recommandée

```
CLIENT-SIDE              SERVER-SIDE
───────────────          ───────────────
GTM Web                  GTM Server
↓                        ↓
Collecte events    →     Enrichissement
Data layer         →     Envoi aux APIs
                         Déduplication
```

### Code Client (envoi vers sGTM)

```javascript
// GA4 config pointant vers sGTM
gtag('config', 'G-XXXXXX', {
  'transport_url': 'https://tracking.votresite.com',
  'first_party_collection': true
});
```

## Conversions APIs

### Meta CAPI (Server GTM)

```
Tag Type: Meta Conversions API
Access Token: [from Events Manager]
Pixel ID: [your pixel ID]

Event: Purchase
Event Data: {
  value: {{Event Value}}
  currency: EUR
  event_id: {{Event ID}}  // Pour déduplication
}

User Data: {
  email: {{User Email Hashed}}
  phone: {{User Phone Hashed}}
}
```

### Déduplication Importante

```
CLIENT                   SERVER
──────                   ──────
event_id: "abc123"   →   event_id: "abc123"

Meta reçoit les deux avec même ID
→ Compte une seule conversion
```

## First-Party Cookies

### Configuration Subdomain

```
tracking.votresite.com → Server GTM

Avantage: Cookies first-party
→ Durée de vie étendue
→ Pas bloqués par Safari ITP
```

### Cookie Settings (sGTM)

```
Cookie Domain: .votresite.com
Cookie Path: /
Cookie Expiry: 400 days
SameSite: Lax
Secure: true
```

## Monitoring & Debug

### Vérifications

| Check | Outil |
|-------|-------|
| Hits reçus | sGTM Preview mode |
| Hits envoyés | Cloud Run logs |
| Meta events | Events Manager > Test |
| GA4 events | DebugView |

### Métriques à Surveiller

- Latence (< 100ms)
- Taux d'erreur (< 1%)
- Volume de hits
- Coût d'hébergement

## Checklist Server-Side

- [ ] Container Server créé
- [ ] Hébergement configuré
- [ ] Custom domain setup
- [ ] Client GA4 configuré
- [ ] Tags CAPI configurés
- [ ] Déduplication event_id en place
- [ ] First-party cookies activés
- [ ] Monitoring en place
