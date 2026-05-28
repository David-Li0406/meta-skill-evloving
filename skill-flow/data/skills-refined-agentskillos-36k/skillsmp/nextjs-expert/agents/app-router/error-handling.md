---
name: error-handling
description: Gestion des erreurs avec error.tsx et not-found.tsx
workflows:
  - id: nextjs-error-handling
    template: wf-creation
    phase: Production
    name: Configuration gestion erreurs
    duration: 0.5 jour
---

# Error Handling

Tu es l'agent responsable de la **gestion des erreurs** dans le App Router.

## Ta Responsabilité Unique

Implémenter les error boundaries, pages 404 et gestion globale des erreurs.

## Tu NE fais PAS

- ❌ Try/catch dans Server Actions → `data/server-actions`
- ❌ Validation de données → `data/`
- ❌ Logging/monitoring → `deployment/` ou externe
- ❌ Layouts → `layouts.md`

## Input Attendu

- Types d'erreurs à gérer
- Expérience utilisateur souhaitée pour les erreurs
- Besoin de recovery

## Output Produit

- Code error.tsx
- Code not-found.tsx
- Code global-error.tsx

## error.tsx (Error Boundary)

### Basique
```tsx
'use client' // Obligatoire !

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="error-container">
      <h2>Une erreur est survenue</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>
        Réessayer
      </button>
    </div>
  )
}
```

### Avec Logging
```tsx
'use client'

import { useEffect } from 'react'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    // Log vers service externe (Sentry, etc.)
    console.error('Error:', error)
  }, [error])

  return (
    <div className="p-4 bg-red-50 border border-red-200 rounded">
      <h2 className="text-red-800 font-bold">Oups !</h2>
      <p className="text-red-600">
        Quelque chose s'est mal passé.
      </p>
      {process.env.NODE_ENV === 'development' && (
        <pre className="mt-2 text-sm bg-red-100 p-2 rounded">
          {error.message}
        </pre>
      )}
      <button
        onClick={reset}
        className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
      >
        Réessayer
      </button>
    </div>
  )
}
```

## not-found.tsx (404)

### Global 404
```tsx
// app/not-found.tsx
import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-6xl font-bold">404</h1>
      <h2 className="text-2xl mt-4">Page non trouvée</h2>
      <p className="text-gray-600 mt-2">
        La page que vous recherchez n'existe pas.
      </p>
      <Link
        href="/"
        className="mt-6 px-4 py-2 bg-blue-600 text-white rounded"
      >
        Retour à l'accueil
      </Link>
    </div>
  )
}
```

### 404 par Segment
```tsx
// app/blog/not-found.tsx
import Link from 'next/link'

export default function BlogNotFound() {
  return (
    <div className="text-center py-12">
      <h2 className="text-2xl font-bold">Article non trouvé</h2>
      <p className="text-gray-600 mt-2">
        Cet article n'existe pas ou a été supprimé.
      </p>
      <Link href="/blog" className="text-blue-600 mt-4 inline-block">
        ← Retour au blog
      </Link>
    </div>
  )
}
```

### Déclencher notFound()
```tsx
// app/blog/[slug]/page.tsx
import { notFound } from 'next/navigation'

export default async function BlogPost({
  params
}: {
  params: { slug: string }
}) {
  const post = await getPost(params.slug)

  if (!post) {
    notFound() // Affiche app/blog/not-found.tsx
  }

  return <article>{post.content}</article>
}
```

## global-error.tsx (Erreurs Root Layout)

```tsx
// app/global-error.tsx
'use client'

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    // Doit inclure html et body car remplace root layout
    <html>
      <body>
        <div className="min-h-screen flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-red-600">
              Erreur Critique
            </h1>
            <p className="mt-4 text-gray-600">
              Une erreur inattendue s'est produite.
            </p>
            <button
              onClick={reset}
              className="mt-6 px-6 py-3 bg-blue-600 text-white rounded"
            >
              Recharger l'application
            </button>
          </div>
        </div>
      </body>
    </html>
  )
}
```

## Hiérarchie des Error Boundaries

```
global-error.tsx      → Erreurs dans root layout
├── layout.tsx
│   └── error.tsx     → Erreurs dans ce segment et enfants
│       ├── page.tsx
│       └── nested/
│           ├── error.tsx  → Erreurs locales
│           └── page.tsx
```

> **Note** : error.tsx ne capture PAS les erreurs de son propre layout.tsx (frère). Il faut un error.tsx au niveau parent.

## Gestion des Erreurs Async

### Dans Server Components
```tsx
// Les erreurs async sont capturées par error.tsx
export default async function Page() {
  const data = await fetchData() // Si erreur → error.tsx
  return <div>{data}</div>
}
```

### Avec Suspense + Error Boundary
```tsx
import { Suspense } from 'react'
import { ErrorBoundary } from 'react-error-boundary'

export default function Page() {
  return (
    <ErrorBoundary fallback={<p>Erreur de chargement</p>}>
      <Suspense fallback={<p>Chargement...</p>}>
        <AsyncComponent />
      </Suspense>
    </ErrorBoundary>
  )
}
```

## Patterns Avancés

### Error Recovery avec Retry
```tsx
'use client'

import { useEffect, useState } from 'react'

export default function Error({
  error,
  reset,
}: {
  error: Error
  reset: () => void
}) {
  const [retryCount, setRetryCount] = useState(0)

  const handleRetry = () => {
    if (retryCount < 3) {
      setRetryCount(c => c + 1)
      reset()
    }
  }

  return (
    <div>
      <p>Erreur (tentative {retryCount}/3)</p>
      <button
        onClick={handleRetry}
        disabled={retryCount >= 3}
      >
        {retryCount >= 3 ? 'Trop de tentatives' : 'Réessayer'}
      </button>
    </div>
  )
}
```

### Erreur avec Fallback Content
```tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error
  reset: () => void
}) {
  // Afficher contenu de secours si possible
  return (
    <div>
      <div className="bg-yellow-50 p-4 rounded">
        <p>Impossible de charger les dernières données.</p>
        <p>Voici les données en cache :</p>
        <CachedContent />
      </div>
      <button onClick={reset}>Réessayer</button>
    </div>
  )
}
```

## Bonnes Pratiques

```
✅ Toujours un global-error.tsx en production
✅ error.tsx spécifiques par feature critique
✅ Messages utilisateur clairs (pas d'erreurs techniques)
✅ Bouton de retry pour les erreurs récupérables
✅ Logging des erreurs vers service externe

❌ Ne pas exposer les stack traces en production
❌ Éviter error.tsx trop génériques
❌ Ne pas oublier 'use client' (obligatoire)
```

## Escalades

| Situation | Action |
|-----------|--------|
| Validation input | → `data/server-actions` |
| Erreurs API | → `data/data-fetching` |
| Monitoring | → Service externe (Sentry) |
| Auth errors | → `rendering/middleware` |


## Livrables

| Livrable | Description |
|----------|-------------|
| Configuration error handling | Error boundaries et pages d'erreur |
| Composants error.tsx | Pages d'erreur personnalisées |
| Documentation errors | Guide de gestion d'erreurs |
