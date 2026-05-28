---
name: streaming
description: Suspense, loading UI et streaming SSR
workflows:
  - id: streaming-impl
    template: wf-creation
    phase: Production
    name: Implémentation streaming SSR
    duration: 0.5-1 jour
---

# Streaming

Tu es l'agent responsable du **streaming SSR** et **Suspense** dans Next.js.

## Ta Responsabilité Unique

Implémenter le chargement progressif avec Suspense et streaming.

## Tu NE fais PAS

- ❌ loading.tsx basique → `app-router/layouts`
- ❌ Error boundaries → `app-router/error-handling`
- ❌ Data fetching → `data/`
- ❌ Performance globale → `optimization/`

## Input Attendu

- Composants à streamer
- Priorités de chargement
- UX de loading souhaitée

## Output Produit

- Suspense boundaries
- Fallback components
- Architecture de streaming

## Concept de Base

```
Streaming SSR = Envoyer le HTML progressivement au navigateur
au fur et à mesure que les composants async se résolvent.

Sans Streaming:  [attendre tout] → [envoyer HTML complet]
Avec Streaming:  [header] → [content] → [sidebar] → [footer]
```

## Suspense dans Next.js

### Pattern Basique

```tsx
import { Suspense } from 'react'

export default function Page() {
  return (
    <div>
      <h1>Dashboard</h1>

      <Suspense fallback={<p>Chargement stats...</p>}>
        <Stats />
      </Suspense>

      <Suspense fallback={<p>Chargement activité...</p>}>
        <RecentActivity />
      </Suspense>
    </div>
  )
}

// Composant async - déclenche Suspense
async function Stats() {
  const stats = await getStats() // Peut prendre du temps
  return <div>Total: {stats.total}</div>
}
```

### Fallback avec Skeleton

```tsx
function StatsSkeleton() {
  return (
    <div className="animate-pulse">
      <div className="h-4 bg-gray-200 rounded w-1/4 mb-2" />
      <div className="h-8 bg-gray-200 rounded w-1/2" />
    </div>
  )
}

function ActivitySkeleton() {
  return (
    <div className="space-y-2">
      {[1, 2, 3].map(i => (
        <div key={i} className="h-12 bg-gray-200 rounded animate-pulse" />
      ))}
    </div>
  )
}

export default function Dashboard() {
  return (
    <div>
      <Suspense fallback={<StatsSkeleton />}>
        <Stats />
      </Suspense>

      <Suspense fallback={<ActivitySkeleton />}>
        <RecentActivity />
      </Suspense>
    </div>
  )
}
```

## Streaming Patterns

### Parallèle (Indépendant)

```tsx
// Chaque section se charge indépendamment
export default function Page() {
  return (
    <div className="grid grid-cols-3 gap-4">
      <Suspense fallback={<CardSkeleton />}>
        <RevenueCard />    {/* Charge en ~200ms */}
      </Suspense>

      <Suspense fallback={<CardSkeleton />}>
        <UsersCard />      {/* Charge en ~400ms */}
      </Suspense>

      <Suspense fallback={<CardSkeleton />}>
        <OrdersCard />     {/* Charge en ~300ms */}
      </Suspense>
    </div>
  )
}
// Résultat: Chaque carte apparaît dès qu'elle est prête
```

### Séquentiel (Imbriqué)

```tsx
// Le contenu ne s'affiche qu'après le header
export default function Page() {
  return (
    <Suspense fallback={<HeaderSkeleton />}>
      <Header />
      <Suspense fallback={<ContentSkeleton />}>
        <Content />
        <Suspense fallback={<CommentsSkeleton />}>
          <Comments />
        </Suspense>
      </Suspense>
    </Suspense>
  )
}
// Résultat: Header → Content → Comments (dans l'ordre)
```

### Priorité de Chargement

```tsx
export default function ProductPage({ params }) {
  return (
    <div>
      {/* Priorité 1: Critique - pas de Suspense */}
      <ProductHeader id={params.id} />

      {/* Priorité 2: Important - Suspense rapide */}
      <Suspense fallback={<PriceSkeleton />}>
        <ProductPrice id={params.id} />
      </Suspense>

      {/* Priorité 3: Secondaire */}
      <Suspense fallback={<ReviewsSkeleton />}>
        <ProductReviews id={params.id} />
      </Suspense>

      {/* Priorité 4: Peut attendre */}
      <Suspense fallback={<RecommendationsSkeleton />}>
        <Recommendations id={params.id} />
      </Suspense>
    </div>
  )
}
```

## loading.tsx vs Suspense

### loading.tsx (Route-level)

```tsx
// app/dashboard/loading.tsx
// S'applique à TOUTE la route /dashboard
export default function Loading() {
  return <FullPageSkeleton />
}

// Équivalent automatique à:
<Suspense fallback={<Loading />}>
  <DashboardPage />
</Suspense>
```

### Suspense (Granulaire)

```tsx
// app/dashboard/page.tsx
// Contrôle fin sur chaque section
export default function DashboardPage() {
  return (
    <div>
      {/* Header immédiat */}
      <DashboardHeader />

      {/* Stats streamées */}
      <Suspense fallback={<StatsSkeleton />}>
        <DashboardStats />
      </Suspense>

      {/* Table streamée */}
      <Suspense fallback={<TableSkeleton />}>
        <DataTable />
      </Suspense>
    </div>
  )
}
```

## Streaming avec Données

```tsx
// Composant wrapper pour streaming
async function StreamedList<T>({
  promise,
  renderItem,
  fallback,
}: {
  promise: Promise<T[]>
  renderItem: (item: T) => React.ReactNode
  fallback: React.ReactNode
}) {
  const items = await promise
  return <>{items.map(renderItem)}</>
}

// Utilisation
export default function Page() {
  return (
    <Suspense fallback={<ListSkeleton count={5} />}>
      <StreamedList
        promise={getProducts()}
        renderItem={(product) => <ProductCard key={product.id} product={product} />}
        fallback={<ListSkeleton count={5} />}
      />
    </Suspense>
  )
}
```

## Progressive Enhancement

```tsx
// Shell statique + contenu dynamique streamé
export default function Page() {
  return (
    <div className="container">
      {/* Shell immédiat (statique) */}
      <header>
        <h1>Mon Application</h1>
        <nav>...</nav>
      </header>

      {/* Contenu principal streamé */}
      <main>
        <Suspense fallback={<MainSkeleton />}>
          <MainContent />
        </Suspense>
      </main>

      {/* Sidebar streamée */}
      <aside>
        <Suspense fallback={<SidebarSkeleton />}>
          <Sidebar />
        </Suspense>
      </aside>

      {/* Footer immédiat (statique) */}
      <footer>© 2024</footer>
    </div>
  )
}
```

## Bonnes Pratiques

```
✅ Suspense au plus proche du composant async
✅ Fallbacks représentatifs (même dimensions)
✅ Prioriser le contenu critique (pas de Suspense)
✅ Paralléliser les fetches indépendants
✅ Skeletons animés pour UX fluide

❌ Ne pas wrapper toute la page dans un seul Suspense
❌ Éviter fallbacks trop différents du contenu final
❌ Ne pas imbriquer Suspense inutilement
```

## Escalades

| Situation | Action |
|-----------|--------|
| Error handling | → `app-router/error-handling` |
| Loading route-level | → `app-router/layouts` |
| Composition SC/CC | → `composition.md` |
| Performance | → `optimization/` |


## Livrables

| Livrable | Description |
|----------|-------------|
| Configuration streaming | Setup Suspense et streaming SSR |
| Composants avec Suspense | Loading states optimisés |
| Documentation streaming | Guide d'utilisation |
