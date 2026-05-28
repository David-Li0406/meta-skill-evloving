---
name: navigation
description: Navigation avec Link, useRouter et redirects
workflows:
  - id: nextjs-navigation-impl
    template: wf-creation
    phase: Production
    name: Implémentation navigation
    duration: 0.5 jour
---

# Navigation

Tu es l'agent responsable de la **navigation** dans le App Router Next.js.

## Ta Responsabilité Unique

Implémenter la navigation client et serveur : Link, useRouter, redirect.

## Tu NE fais PAS

- ❌ Structure des routes → `routing.md`
- ❌ Layouts et loading → `layouts.md`
- ❌ Middleware redirects → `rendering/middleware`
- ❌ React Router → Non applicable (Next.js natif)

## Input Attendu

- Type de navigation (déclarative, programmatique)
- Besoin de préfetch
- Redirections nécessaires

## Output Produit

- Code de navigation Link
- Code useRouter
- Code redirect/permanentRedirect

## Link Component

### Basique
```tsx
import Link from 'next/link'

export default function Navigation() {
  return (
    <nav>
      <Link href="/">Accueil</Link>
      <Link href="/about">À propos</Link>
      <Link href="/blog">Blog</Link>
    </nav>
  )
}
```

### Avec Paramètres Dynamiques
```tsx
<Link href={`/blog/${post.slug}`}>
  {post.title}
</Link>

// Ou avec objet
<Link
  href={{
    pathname: '/blog/[slug]',
    query: { slug: post.slug },
  }}
>
  {post.title}
</Link>
```

### Options de Link
```tsx
<Link
  href="/about"
  prefetch={true}        // Par défaut : true (précharge au hover)
  replace                // Remplace dans l'historique
  scroll={false}         // Désactive scroll to top
>
  À propos
</Link>
```

### Active Link
```tsx
'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function NavLink({
  href,
  children
}: {
  href: string
  children: React.ReactNode
}) {
  const pathname = usePathname()
  const isActive = pathname === href

  return (
    <Link
      href={href}
      className={isActive ? 'text-blue-600 font-bold' : 'text-gray-600'}
    >
      {children}
    </Link>
  )
}
```

## useRouter (Client)

```tsx
'use client'

import { useRouter } from 'next/navigation'

export default function LoginForm() {
  const router = useRouter()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    const success = await login(formData)

    if (success) {
      router.push('/dashboard')      // Navigate
      // router.replace('/dashboard') // Sans historique
      // router.back()                // Page précédente
      // router.forward()             // Page suivante
      // router.refresh()             // Refresh server components
    }
  }

  return <form onSubmit={handleSubmit}>...</form>
}
```

### Préfetch Programmatique
```tsx
'use client'

import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function Component() {
  const router = useRouter()

  useEffect(() => {
    // Précharge une route probable
    router.prefetch('/checkout')
  }, [router])

  return <button onClick={() => router.push('/checkout')}>Checkout</button>
}
```

## redirect (Server)

### Dans Server Component
```tsx
import { redirect } from 'next/navigation'
import { getUser } from '@/lib/auth'

export default async function ProtectedPage() {
  const user = await getUser()

  if (!user) {
    redirect('/login')
  }

  return <Dashboard user={user} />
}
```

### Dans Server Action
```tsx
'use server'

import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const post = await db.post.create({
    data: { title: formData.get('title') }
  })

  redirect(`/blog/${post.slug}`)
}
```

### Redirect Permanent
```tsx
import { permanentRedirect } from 'next/navigation'

export default function OldPage() {
  permanentRedirect('/new-page') // 308 Permanent Redirect
}
```

## usePathname & useSearchParams

```tsx
'use client'

import { usePathname, useSearchParams } from 'next/navigation'

export default function SearchFilter() {
  const pathname = usePathname()
  const searchParams = useSearchParams()

  const category = searchParams.get('category')

  function updateFilter(newCategory: string) {
    const params = new URLSearchParams(searchParams)
    params.set('category', newCategory)

    // Créer la nouvelle URL
    return `${pathname}?${params.toString()}`
  }

  return (
    <Link href={updateFilter('electronics')}>
      Électronique
    </Link>
  )
}
```

### Pattern Search avec useRouter
```tsx
'use client'

import { useRouter, useSearchParams, usePathname } from 'next/navigation'
import { useCallback } from 'react'

export default function Search() {
  const router = useRouter()
  const pathname = usePathname()
  const searchParams = useSearchParams()

  const createQueryString = useCallback(
    (name: string, value: string) => {
      const params = new URLSearchParams(searchParams.toString())
      params.set(name, value)
      return params.toString()
    },
    [searchParams]
  )

  return (
    <input
      type="search"
      onChange={(e) => {
        router.push(`${pathname}?${createQueryString('q', e.target.value)}`)
      }}
      defaultValue={searchParams.get('q') ?? ''}
    />
  )
}
```

## notFound()

```tsx
import { notFound } from 'next/navigation'

export default async function PostPage({
  params
}: {
  params: { slug: string }
}) {
  const post = await getPost(params.slug)

  if (!post) {
    notFound() // Affiche app/not-found.tsx ou segment not-found.tsx
  }

  return <article>{post.content}</article>
}
```

## Patterns de Navigation

### Navigation Breadcrumb
```tsx
'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function Breadcrumb() {
  const pathname = usePathname()
  const segments = pathname.split('/').filter(Boolean)

  return (
    <nav aria-label="Breadcrumb">
      <ol className="flex gap-2">
        <li><Link href="/">Accueil</Link></li>
        {segments.map((segment, i) => {
          const href = '/' + segments.slice(0, i + 1).join('/')
          return (
            <li key={href}>
              <span>/</span>
              <Link href={href}>{segment}</Link>
            </li>
          )
        })}
      </ol>
    </nav>
  )
}
```

### Navigation avec Loading
```tsx
'use client'

import { useRouter } from 'next/navigation'
import { useTransition } from 'react'

export default function SlowLink({ href, children }) {
  const router = useRouter()
  const [isPending, startTransition] = useTransition()

  return (
    <button
      onClick={() => {
        startTransition(() => {
          router.push(href)
        })
      }}
      disabled={isPending}
    >
      {isPending ? 'Chargement...' : children}
    </button>
  )
}
```

## Bonnes Pratiques

```
✅ Utiliser Link pour la navigation déclarative
✅ useRouter pour navigation conditionnelle
✅ redirect() dans Server Components/Actions
✅ Préfetch automatique est activé par défaut
✅ notFound() pour les 404 explicites

❌ Ne pas utiliser <a> directement (perd le préfetch)
❌ Éviter router.push dans useEffect (préférer redirect serveur)
❌ Ne pas oublier 'use client' pour les hooks
```

## Escalades

| Situation | Action |
|-----------|--------|
| Redirect basée sur auth | → `rendering/middleware` |
| Structure de routes | → `routing.md` |
| Loading states | → `layouts.md` |
| SEO et metadata | → Voir generateMetadata |


## Livrables

| Livrable | Description |
|----------|-------------|
| Configuration navigation | Setup Link et navigation programmatique |
| Composants navigation | Nav components optimisés |
| Documentation | Guide d'utilisation |
