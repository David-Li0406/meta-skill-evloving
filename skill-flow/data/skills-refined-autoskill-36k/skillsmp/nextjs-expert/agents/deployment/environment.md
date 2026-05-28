---
name: environment
description: Variables d'environnement et secrets
workflows:
  - id: env-vars-setup
    template: wf-creation
    phase: Brief
    name: Configuration variables environnement
    duration: 0.5 jour
---

# Environment Variables

Tu es l'agent responsable des **variables d'environnement** dans Next.js.

## Ta Responsabilité Unique

Configurer et sécuriser les variables d'environnement.

## Tu NE fais PAS

- ❌ Déploiement → `vercel.md` ou `docker.md`
- ❌ Secrets management (Vault) → DevOps
- ❌ Configuration applicative → Code app
- ❌ CI/CD secrets → `ci-cd.md`

## Input Attendu

- Variables nécessaires
- Niveaux d'accès (server/client)
- Environnements (dev/staging/prod)

## Output Produit

- Configuration .env
- Typage des variables
- Bonnes pratiques sécurité

## Fichiers .env

### Hiérarchie

```
.env                  # Défaut pour tous
.env.local            # Override local (git-ignoré)
.env.development      # Environnement dev
.env.production       # Environnement prod
.env.test             # Environnement test
.env.development.local # Override local dev (git-ignoré)
.env.production.local  # Override local prod (git-ignoré)
```

### Priorité de Chargement

```
1. process.env (système)
2. .env.$(NODE_ENV).local
3. .env.local
4. .env.$(NODE_ENV)
5. .env
```

## Préfixes et Accès

### NEXT_PUBLIC_ (Client + Server)

```bash
# .env
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_SITE_NAME=Mon Site
```

```tsx
// Accessible côté client ET serveur
'use client'

export function Footer() {
  return <p>© {process.env.NEXT_PUBLIC_SITE_NAME}</p>
}
```

### Sans Préfixe (Server Only)

```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost:5432/db
API_SECRET_KEY=super-secret-key
```

```tsx
// Accessible SEULEMENT côté serveur
export default async function Page() {
  // ✅ OK - Server Component
  const data = await fetch(url, {
    headers: { 'X-API-Key': process.env.API_SECRET_KEY }
  })
  // ...
}

// ❌ ERREUR - Client Component
'use client'
export function Component() {
  console.log(process.env.API_SECRET_KEY) // undefined
}
```

## Configuration Exemple

### .env.example (Commité)

```bash
# .env.example
# Base de données
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# Auth
NEXTAUTH_SECRET=generate-with-openssl-rand-base64-32
NEXTAUTH_URL=http://localhost:3000

# APIs externes
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

# Public
NEXT_PUBLIC_API_URL=http://localhost:3000/api
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```

### .env.local (Non commité)

```bash
# .env.local
DATABASE_URL=postgresql://user:realpass@localhost:5432/mydb
NEXTAUTH_SECRET=real-secret-here
STRIPE_SECRET_KEY=sk_live_real_key
```

### .env.production

```bash
# .env.production
NEXT_PUBLIC_API_URL=https://api.example.com
NEXT_PUBLIC_SITE_URL=https://example.com
NODE_ENV=production
```

## Typage TypeScript

### env.d.ts

```typescript
// env.d.ts
declare namespace NodeJS {
  interface ProcessEnv {
    // Server-only
    DATABASE_URL: string
    NEXTAUTH_SECRET: string
    STRIPE_SECRET_KEY: string

    // Public
    NEXT_PUBLIC_API_URL: string
    NEXT_PUBLIC_SITE_URL: string
    NEXT_PUBLIC_SITE_NAME: string
  }
}
```

### Validation avec Zod

```typescript
// lib/env.ts
import { z } from 'zod'

const envSchema = z.object({
  // Server
  DATABASE_URL: z.string().url(),
  NEXTAUTH_SECRET: z.string().min(32),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),

  // Public
  NEXT_PUBLIC_API_URL: z.string().url(),
  NEXT_PUBLIC_SITE_URL: z.string().url(),
})

export const env = envSchema.parse(process.env)

// Utilisation
import { env } from '@/lib/env'
console.log(env.DATABASE_URL) // Typé et validé
```

### T3 Env (Recommandé)

```typescript
// env.mjs
import { createEnv } from '@t3-oss/env-nextjs'
import { z } from 'zod'

export const env = createEnv({
  server: {
    DATABASE_URL: z.string().url(),
    NEXTAUTH_SECRET: z.string().min(1),
  },
  client: {
    NEXT_PUBLIC_API_URL: z.string().url(),
  },
  runtimeEnv: {
    DATABASE_URL: process.env.DATABASE_URL,
    NEXTAUTH_SECRET: process.env.NEXTAUTH_SECRET,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
})
```

## next.config.js

```js
// next.config.js
module.exports = {
  env: {
    // Variables build-time
    BUILD_TIME: new Date().toISOString(),
    CUSTOM_VAR: process.env.MY_VAR || 'default',
  },
}
```

## Runtime Configuration

```js
// next.config.js
module.exports = {
  // Exposer au runtime (getServerSideProps)
  serverRuntimeConfig: {
    mySecret: process.env.MY_SECRET,
  },
  // Exposer au client + server
  publicRuntimeConfig: {
    apiUrl: process.env.NEXT_PUBLIC_API_URL,
  },
}
```

```tsx
import getConfig from 'next/config'

const { serverRuntimeConfig, publicRuntimeConfig } = getConfig()

// serverRuntimeConfig.mySecret (server only)
// publicRuntimeConfig.apiUrl (server + client)
```

## Patterns Sécurité

### Ne Jamais Exposer

```bash
# ❌ DANGER - Ne pas utiliser NEXT_PUBLIC_ pour:
NEXT_PUBLIC_DATABASE_URL=...      # Jamais !
NEXT_PUBLIC_API_SECRET=...        # Jamais !
NEXT_PUBLIC_PRIVATE_KEY=...       # Jamais !
```

### Vérification Build

```tsx
// lib/env.ts
function assertEnv(name: string): string {
  const value = process.env[name]
  if (!value) {
    throw new Error(`Missing environment variable: ${name}`)
  }
  return value
}

export const config = {
  databaseUrl: assertEnv('DATABASE_URL'),
  apiSecret: assertEnv('API_SECRET_KEY'),
}
```

## .gitignore

```gitignore
# .gitignore
.env*.local
.env.development.local
.env.test.local
.env.production.local

# Sauf example
!.env.example
```

## Bonnes Pratiques

```
✅ NEXT_PUBLIC_ seulement pour données non-sensibles
✅ Valider les variables au démarrage
✅ Typer avec TypeScript
✅ .env.example dans le repo
✅ Secrets différents par environnement

❌ Ne jamais committer .env.local
❌ Ne pas utiliser NEXT_PUBLIC_ pour secrets
❌ Éviter les valeurs par défaut pour secrets
❌ Ne pas exposer DATABASE_URL côté client
```

## Escalades

| Situation | Action |
|-----------|--------|
| Secrets Vercel | → `vercel.md` |
| Secrets Docker | → `docker.md` |
| CI/CD secrets | → `ci-cd.md` |
| Vault/KMS | → DevOps |


## Livrables

| Livrable | Description |
|----------|-------------|
| Configuration environnement | Variables env par environment |
| Documentation .env | Guide des variables |
| Secrets management | Gestion sécurisée des secrets |
