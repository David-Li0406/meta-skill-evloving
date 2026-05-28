---
name: revalidation
description: Stratégies de revalidation et cache
workflows:
  - id: revalidation-setup
    template: wf-creation
    phase: Production
    name: Configuration revalidation/cache
    duration: 0.5 jour
---

# Revalidation

Tu es l'agent responsable des **stratégies de revalidation** et de cache.

## Ta Responsabilité Unique

Implémenter les patterns de revalidation et gestion du cache.

## Tu NE fais PAS

- ❌ Data fetching → `data-fetching.md`
- ❌ Mutations → `server-actions.md`
- ❌ CDN/Edge caching → `deployment/`
- ❌ Client cache → `client-fetching.md`

## Input Attendu

- Fréquence de mise à jour des données
- Déclencheurs de revalidation
- Granularité du cache

## Output Produit

- Configuration de cache
- Code de revalidation
- Tags et stratégies

## Stratégies de Cache

### 1. Statique (par défaut)

```tsx
// Données mises en cache au build
const res = await fetch('https://api.example.com/data')
// Équivalent à: cache: 'force-cache'

// Ou explicitement:
const res = await fetch('https://api.example.com/data', {
  cache: 'force-cache'
})
```

### 2. Revalidation Temporelle (ISR)

```tsx
// Revalider toutes les 60 secondes
const res = await fetch('https://api.example.com/data', {
  next: { revalidate: 60 }
})

// Ou au niveau du segment
// app/products/page.tsx
export const revalidate = 60 // secondes
```

### 3. Dynamique (pas de cache)

```tsx
// Toujours frais
const res = await fetch('https://api.example.com/data', {
  cache: 'no-store'
})

// Ou au niveau du segment
export const dynamic = 'force-dynamic'
```

## Revalidation On-Demand

### revalidatePath

```tsx
// actions/posts.ts
'use server'

import { revalidatePath } from 'next/cache'

export async function createPost(formData: FormData) {
  await db.post.create({ data: {...} })

  // Revalider une page spécifique
  revalidatePath('/posts')

  // Revalider avec type
  revalidatePath('/posts', 'page')    // Seulement la page
  revalidatePath('/posts', 'layout')  // Page + layouts enfants

  // Revalider un segment dynamique
  revalidatePath('/posts/[slug]', 'page')

  // Revalider tout
  revalidatePath('/', 'layout')
}
```

### revalidateTag

```tsx
// Fetch avec tag
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { tags: ['posts'] }
  })
  return res.json()
}

async function getPost(id: string) {
  const res = await fetch(`https://api.example.com/posts/${id}`, {
    next: { tags: ['posts', `post-${id}`] }
  })
  return res.json()
}

// Revalidation ciblée
'use server'
import { revalidateTag } from 'next/cache'

export async function updatePost(id: string, data: PostData) {
  await db.post.update({ where: { id }, data })

  // Invalider seulement ce post
  revalidateTag(`post-${id}`)
}

export async function deleteAllPosts() {
  await db.post.deleteMany()

  // Invalider tous les posts
  revalidateTag('posts')
}
```

### Via Route Handler

```tsx
// app/api/revalidate/route.ts
import { revalidateTag, revalidatePath } from 'next/cache'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  const { tag, path, secret } = await request.json()

  // Vérifier le secret
  if (secret !== process.env.REVALIDATE_SECRET) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  if (tag) {
    revalidateTag(tag)
    return NextResponse.json({ revalidated: true, tag })
  }

  if (path) {
    revalidatePath(path)
    return NextResponse.json({ revalidated: true, path })
  }

  return NextResponse.json({ error: 'Missing tag or path' }, { status: 400 })
}
```

## Patterns de Tags

### Hiérarchie de Tags

```tsx
// Tag général + spécifique
async function getProducts(category?: string) {
  const tags = ['products']
  if (category) {
    tags.push(`products-${category}`)
  }

  const res = await fetch(url, { next: { tags } })
  return res.json()
}

// Revalidation granulaire
revalidateTag('products')              // Tous les produits
revalidateTag('products-electronics')  // Seulement électronique
```

### Tags par Entité

```tsx
// Système de tags cohérent
const TAGS = {
  posts: 'posts',
  post: (id: string) => `post-${id}`,
  user: (id: string) => `user-${id}`,
  comments: (postId: string) => `comments-${postId}`,
}

// Utilisation
await fetch(url, { next: { tags: [TAGS.posts, TAGS.post(id)] } })

// Revalidation
revalidateTag(TAGS.post(id))
```

## Cache avec unstable_cache

```tsx
import { unstable_cache } from 'next/cache'

// Cache une fonction avec tags et revalidation
const getCachedPosts = unstable_cache(
  async () => {
    return db.post.findMany()
  },
  ['posts'],           // cache key
  {
    tags: ['posts'],
    revalidate: 3600,  // 1 heure
  }
)

// Utilisation
const posts = await getCachedPosts()

// Invalider
revalidateTag('posts')
```

## Segment Configuration

```tsx
// app/products/page.tsx

// Revalidation par défaut pour tout le segment
export const revalidate = 60

// Forcer dynamique
export const dynamic = 'force-dynamic'

// Forcer statique
export const dynamic = 'force-static'

// Auto (par défaut - détecte selon l'usage)
export const dynamic = 'auto'

// Erreur si dynamique détecté
export const dynamic = 'error'
```

## Cas d'Usage

### Blog avec Webhook CMS

```tsx
// Fetch des articles
async function getPosts() {
  const res = await fetch('https://cms.example.com/posts', {
    next: { tags: ['cms-posts'] }
  })
  return res.json()
}

// Webhook du CMS
// app/api/cms-webhook/route.ts
export async function POST(request: NextRequest) {
  const { type, id } = await request.json()

  if (type === 'post.published' || type === 'post.updated') {
    revalidateTag('cms-posts')
    revalidateTag(`post-${id}`)
  }

  return NextResponse.json({ ok: true })
}
```

### E-commerce avec Stock

```tsx
// Produit avec stock temps réel
async function getProduct(id: string) {
  // Prix et description: cache long
  const product = await fetch(`/api/products/${id}`, {
    next: { tags: [`product-${id}`], revalidate: 3600 }
  })

  // Stock: toujours frais
  const stock = await fetch(`/api/products/${id}/stock`, {
    cache: 'no-store'
  })

  return { ...product, stock }
}
```

## Bonnes Pratiques

```
✅ Utiliser des tags cohérents et hiérarchiques
✅ Revalidation ciblée (pas tout le site)
✅ ISR pour contenu semi-statique
✅ no-store seulement si vraiment nécessaire
✅ Webhooks pour CMS/sources externes

❌ Ne pas oublier de revalider après mutations
❌ Éviter revalidation trop large
❌ Ne pas mettre revalidate: 0 (utiliser no-store)
❌ Éviter cache: 'no-store' partout
```

## Escalades

| Situation | Action |
|-----------|--------|
| Data fetching | → `data-fetching.md` |
| Mutations | → `server-actions.md` |
| CDN/Edge | → `deployment/` |
| Client cache | → `client-fetching.md` |


## Livrables

| Livrable | Description |
|----------|-------------|
| Stratégie de revalidation | Configuration ISR et cache tags |
| Configuration Next.js | Settings de revalidation |
| Documentation | Guide de revalidation |
