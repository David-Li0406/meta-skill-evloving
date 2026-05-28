---
name: vercel
description: Déploiement sur Vercel
workflows:
  - id: vercel-deployment
    template: wf-creation
    phase: Livraison
    name: Déploiement Vercel
    duration: 0.5 jour
---

# Vercel Deployment

Tu es l'agent responsable du **déploiement sur Vercel**.

## Ta Responsabilité Unique

Configurer et optimiser le déploiement Next.js sur Vercel.

## Tu NE fais PAS

- ❌ Self-hosting → `docker.md`
- ❌ Infrastructure AWS/GCP → DevOps
- ❌ CI/CD custom → `ci-cd.md`
- ❌ Code applicatif → Autres agents

## Input Attendu

- Projet Next.js à déployer
- Besoins de configuration
- Domaines et environnements

## Output Produit

- Configuration vercel.json
- Setup projet Vercel
- Optimisations spécifiques

## Déploiement Basique

### Via CLI

```bash
# Installation
npm i -g vercel

# Déploiement
vercel

# Déploiement production
vercel --prod
```

### Via GitHub

```
1. Connecter repo GitHub à Vercel
2. Vercel détecte automatiquement Next.js
3. Push → Build automatique
```

## Configuration vercel.json

### Basique

```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs"
}
```

### Avec Redirections

```json
{
  "redirects": [
    {
      "source": "/old-page",
      "destination": "/new-page",
      "permanent": true
    },
    {
      "source": "/blog/:slug",
      "destination": "/articles/:slug",
      "permanent": false
    }
  ]
}
```

### Avec Headers

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        }
      ]
    },
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "no-store"
        }
      ]
    }
  ]
}
```

### Rewrites

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://api.backend.com/:path*"
    }
  ]
}
```

## Variables d'Environnement

### Via Dashboard

```
Project Settings → Environment Variables
- Development (local preview)
- Preview (PR branches)
- Production (main branch)
```

### Via CLI

```bash
# Ajouter une variable
vercel env add MY_SECRET

# Lister les variables
vercel env ls

# Supprimer
vercel env rm MY_SECRET
```

### Secrets Sensibles

```bash
# Créer un secret partagé
vercel secrets add my-api-key "secret-value"

# Utiliser dans vercel.json
{
  "env": {
    "API_KEY": "@my-api-key"
  }
}
```

## Domaines

### Ajouter un Domaine

```bash
# Via CLI
vercel domains add example.com

# Configurer DNS
vercel dns add example.com A 76.76.21.21
```

### Configuration DNS

```
Type  Name    Value
A     @       76.76.21.21
CNAME www     cname.vercel-dns.com
```

## Edge Functions

```tsx
// app/api/geo/route.ts
export const runtime = 'edge'

export async function GET(request: Request) {
  const country = request.headers.get('x-vercel-ip-country')
  return Response.json({ country })
}
```

## Cron Jobs

```json
// vercel.json
{
  "crons": [
    {
      "path": "/api/cron/daily",
      "schedule": "0 0 * * *"
    },
    {
      "path": "/api/cron/hourly",
      "schedule": "0 * * * *"
    }
  ]
}
```

```tsx
// app/api/cron/daily/route.ts
export async function GET(request: Request) {
  // Vérifier le secret Vercel
  const authHeader = request.headers.get('authorization')
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // Logique cron
  await runDailyTask()

  return Response.json({ success: true })
}
```

## Intégrations

### KV Store

```tsx
import { kv } from '@vercel/kv'

export async function GET() {
  await kv.set('key', 'value')
  const value = await kv.get('key')
  return Response.json({ value })
}
```

### Blob Storage

```tsx
import { put, del } from '@vercel/blob'

export async function POST(request: Request) {
  const { searchParams } = new URL(request.url)
  const filename = searchParams.get('filename')

  const blob = await put(filename, request.body, {
    access: 'public',
  })

  return Response.json(blob)
}
```

### Postgres

```tsx
import { sql } from '@vercel/postgres'

export async function GET() {
  const { rows } = await sql`SELECT * FROM users`
  return Response.json(rows)
}
```

## Optimisations Vercel

### Image Optimization

```js
// next.config.js
module.exports = {
  images: {
    // Utiliser le service Vercel
    unoptimized: false,
    // Domaines externes
    remotePatterns: [
      { hostname: 'images.example.com' }
    ],
  },
}
```

### ISR

```tsx
// Automatiquement géré par Vercel
export const revalidate = 60

// On-demand revalidation via webhook
export async function POST(request: Request) {
  revalidateTag('products')
  return Response.json({ revalidated: true })
}
```

## Preview Deployments

```
Chaque PR crée une preview automatique:
- URL unique par commit
- Variables Preview séparées
- Commentaire automatique sur PR
```

### Protection Preview

```json
// vercel.json
{
  "passwordProtection": {
    "key": "preview-password"
  }
}
```

## Monitoring

### Analytics

```tsx
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

### Speed Insights

```tsx
import { SpeedInsights } from '@vercel/speed-insights/next'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <SpeedInsights />
      </body>
    </html>
  )
}
```

## Bonnes Pratiques

```
✅ Variables d'env par environnement
✅ Headers de sécurité
✅ Analytics et Speed Insights
✅ Preview deployments pour PR
✅ Cron jobs pour tâches planifiées

❌ Ne pas committer de secrets
❌ Éviter builds trop longs (timeout)
❌ Ne pas ignorer les erreurs de build
❌ Éviter trop de rewrites (performance)
```

## Escalades

| Situation | Action |
|-----------|--------|
| Self-hosting | → `docker.md` |
| CI/CD custom | → `ci-cd.md` |
| Variables env | → `environment.md` |
| Performance | → `optimization/` |


## Livrables

| Livrable | Description |
|----------|-------------|
| Configuration Vercel | Déploiement optimisé sur Vercel |
| Documentation deployment | Guide de déploiement |
| CI/CD Vercel | Pipeline automatisé |
