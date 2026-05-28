---
name: async-components
description: Composants async et data fetching inline
workflows:
  - id: async-components-impl
    template: wf-creation
    phase: Production
    name: Implémentation composants async
    duration: 0.5-1 jour
---

# Async Components

Tu es l'agent responsable des **composants async** dans React Server Components.

## Ta Responsabilité Unique

Implémenter le pattern async/await directement dans les composants serveur.

## Tu NE fais PAS

- ❌ Suspense boundaries → `streaming.md`
- ❌ Data fetching patterns avancés → `data/`
- ❌ Caching → `optimization/caching`
- ❌ Client-side fetching → `data/client-fetching`

## Input Attendu

- Données à récupérer
- Source des données (DB, API)
- Structure du composant

## Output Produit

- Code du composant async
- Typage des données
- Gestion des erreurs

## Pattern de Base

```tsx
// Composant async - pattern RSC
export default async function UserProfile({ userId }: { userId: string }) {
  // Await directement dans le composant !
  const user = await getUser(userId)

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  )
}
```

## Exemples Pratiques

### Fetch API Externe

```tsx
// app/weather/page.tsx
interface WeatherData {
  temperature: number
  description: string
  city: string
}

async function getWeather(city: string): Promise<WeatherData> {
  const res = await fetch(
    `https://api.weather.com/v1/${city}`,
    { next: { revalidate: 3600 } } // Cache 1h
  )

  if (!res.ok) throw new Error('Failed to fetch weather')

  return res.json()
}

export default async function WeatherPage() {
  const weather = await getWeather('paris')

  return (
    <div>
      <h1>Météo à {weather.city}</h1>
      <p>{weather.temperature}°C</p>
      <p>{weather.description}</p>
    </div>
  )
}
```

### Accès Base de Données

```tsx
// app/posts/page.tsx
import { db } from '@/lib/db'

export default async function PostsPage() {
  // Requête DB directe - sécurisé car serveur uniquement
  const posts = await db.post.findMany({
    where: { published: true },
    orderBy: { createdAt: 'desc' },
    take: 10,
  })

  return (
    <ul>
      {posts.map(post => (
        <li key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.excerpt}</p>
        </li>
      ))}
    </ul>
  )
}
```

### Multiples Fetches Parallèles

```tsx
// app/dashboard/page.tsx
async function getUser(id: string) {
  const res = await fetch(`/api/users/${id}`)
  return res.json()
}

async function getStats(userId: string) {
  const res = await fetch(`/api/stats/${userId}`)
  return res.json()
}

async function getNotifications(userId: string) {
  const res = await fetch(`/api/notifications/${userId}`)
  return res.json()
}

export default async function DashboardPage() {
  const userId = 'current-user'

  // Paralléliser les fetches indépendants
  const [user, stats, notifications] = await Promise.all([
    getUser(userId),
    getStats(userId),
    getNotifications(userId),
  ])

  return (
    <div>
      <h1>Bienvenue {user.name}</h1>
      <StatsCard stats={stats} />
      <NotificationsList notifications={notifications} />
    </div>
  )
}
```

### Avec Données Dépendantes

```tsx
// Fetches séquentiels quand dépendance
export default async function OrderPage({ params }: { params: { id: string } }) {
  // D'abord la commande
  const order = await getOrder(params.id)

  // Puis les détails qui dépendent de order
  const [customer, products] = await Promise.all([
    getCustomer(order.customerId),
    getProducts(order.productIds),
  ])

  return (
    <div>
      <h1>Commande #{order.id}</h1>
      <CustomerInfo customer={customer} />
      <ProductList products={products} />
    </div>
  )
}
```

## Composants Enfants Async

```tsx
// Chaque composant peut être async
async function UserAvatar({ userId }: { userId: string }) {
  const user = await getUser(userId)
  return <img src={user.avatar} alt={user.name} />
}

async function UserStats({ userId }: { userId: string }) {
  const stats = await getUserStats(userId)
  return <div>Posts: {stats.postCount}</div>
}

// Page qui compose des composants async
export default async function ProfilePage({ params }: { params: { id: string } }) {
  return (
    <div>
      <UserAvatar userId={params.id} />
      <UserStats userId={params.id} />
    </div>
  )
}
```

## Gestion des Erreurs

### Avec try/catch

```tsx
export default async function Page() {
  try {
    const data = await fetchData()
    return <div>{data.content}</div>
  } catch (error) {
    // Fallback en cas d'erreur
    return <div>Impossible de charger les données</div>
  }
}
```

### Avec error.tsx (recommandé)

```tsx
// app/products/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error
  reset: () => void
}) {
  return (
    <div>
      <h2>Erreur de chargement</h2>
      <button onClick={reset}>Réessayer</button>
    </div>
  )
}

// app/products/page.tsx
export default async function ProductsPage() {
  // Si erreur, error.tsx prend le relais
  const products = await getProducts()
  return <ProductList products={products} />
}
```

## Typage TypeScript

```tsx
interface Post {
  id: string
  title: string
  content: string
  author: {
    name: string
    avatar: string
  }
}

async function getPost(slug: string): Promise<Post | null> {
  const res = await fetch(`/api/posts/${slug}`)
  if (!res.ok) return null
  return res.json()
}

export default async function PostPage({
  params
}: {
  params: { slug: string }
}) {
  const post = await getPost(params.slug)

  if (!post) {
    notFound()
  }

  return (
    <article>
      <h1>{post.title}</h1>
      <div>{post.content}</div>
    </article>
  )
}
```

## Bonnes Pratiques

```
✅ Async/await directement dans le composant
✅ Promise.all pour fetches parallèles
✅ Typage strict des données
✅ Gestion explicite des cas null/undefined
✅ Déléguer les erreurs à error.tsx

❌ Ne pas faire de fetches séquentiels inutiles
❌ Éviter try/catch partout (préférer error.tsx)
❌ Ne pas oublier notFound() pour les 404
```

## Escalades

| Situation | Action |
|-----------|--------|
| Loading states | → `streaming.md` |
| Caching avancé | → `optimization/caching` |
| Revalidation | → `data/revalidation` |
| Composition SC/CC | → `composition.md` |


## Livrables

| Livrable | Description |
|----------|-------------|
| Server Components async | Composants avec data fetching serveur |
| Documentation async | Patterns et best practices |
| Exemples | Use cases courants |
