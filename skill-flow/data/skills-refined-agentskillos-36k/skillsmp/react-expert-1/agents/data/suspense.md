---
name: suspense
description: React Suspense for lazy loading and declarative loading states
workflows:
  - id: suspense-impl
    template: wf-evolution
    phase: Réalisation
    name: Implémentation React Suspense
    duration: 0.5-1 jour
---

# React Suspense - Chargement Déclaratif

## Rôle

Implémentation de React Suspense pour le lazy loading, le code splitting et le data fetching.

## Tu NE fais PAS

- ❌ Implémenter les APIs backend → `backend-developer`
- ❌ Configurer les librairies de state management → `../state/`
- ❌ Gérer la gestion d'erreurs (utiliser Error Boundaries) → `../components/error-boundaries.md`
- ❌ Optimiser le bundle côté build → `../performance/code-splitting.md`

## Suspense pour Code Splitting

### React.lazy

```tsx
import { lazy, Suspense } from 'react';

// Import dynamique
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));
const Profile = lazy(() => import('./pages/Profile'));

function App() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </Suspense>
  );
}
```

### Named Exports

```tsx
// lazy ne supporte que les default exports par défaut
// Pour les named exports :
const MyComponent = lazy(() =>
  import('./components/MyComponent').then((module) => ({
    default: module.MyComponent,
  }))
);
```

### Preloading

```tsx
const Dashboard = lazy(() => import('./pages/Dashboard'));

// Preload au hover
function NavLink({ to, children }: NavLinkProps) {
  const preload = () => {
    if (to === '/dashboard') {
      import('./pages/Dashboard');
    }
  };

  return (
    <Link to={to} onMouseEnter={preload}>
      {children}
    </Link>
  );
}
```

## Suspense Boundaries

### Granularité

```tsx
function App() {
  return (
    <Layout>
      {/* Boundary global - catch-all */}
      <Suspense fallback={<PageLoader />}>
        <Header />

        <main>
          {/* Boundaries par section */}
          <Suspense fallback={<SidebarSkeleton />}>
            <Sidebar />
          </Suspense>

          <Suspense fallback={<ContentSkeleton />}>
            <MainContent />
          </Suspense>
        </main>

        <Footer />
      </Suspense>
    </Layout>
  );
}
```

### Fallback progressif

```tsx
function ProductPage({ id }: { id: string }) {
  return (
    <div>
      {/* Contenu principal charge en premier */}
      <Suspense fallback={<ProductSkeleton />}>
        <ProductDetails id={id} />
      </Suspense>

      {/* Contenu secondaire peut attendre */}
      <Suspense fallback={<ReviewsSkeleton />}>
        <ProductReviews id={id} />
      </Suspense>

      {/* Recommandations en dernier */}
      <Suspense fallback={<RecommendationsSkeleton />}>
        <Recommendations id={id} />
      </Suspense>
    </div>
  );
}
```

## Suspense pour Data Fetching

### Avec React Query

```tsx
import { useSuspenseQuery } from '@tanstack/react-query';

function UserProfile({ userId }: { userId: string }) {
  // Pas de isLoading - Suspense gère
  const { data: user } = useSuspenseQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUser(userId),
  });

  return <div>{user.name}</div>;
}

// Usage
function App() {
  return (
    <Suspense fallback={<ProfileSkeleton />}>
      <UserProfile userId="123" />
    </Suspense>
  );
}
```

### Avec SWR

```tsx
import useSWR from 'swr';

function Profile() {
  const { data } = useSWR('/api/user', fetcher, { suspense: true });
  return <div>Hello, {data.name}</div>;
}
```

### Pattern "use" (React 19+)

```tsx
import { use, Suspense } from 'react';

// Promise comme prop
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise);
  return <div>{user.name}</div>;
}

function App() {
  const userPromise = fetchUser('123');

  return (
    <Suspense fallback={<Spinner />}>
      <UserProfile userPromise={userPromise} />
    </Suspense>
  );
}
```

## Error Boundaries + Suspense

### Pattern recommandé

```tsx
import { ErrorBoundary } from 'react-error-boundary';

function AsyncSection({ children }: { children: ReactNode }) {
  return (
    <ErrorBoundary fallback={<ErrorMessage />}>
      <Suspense fallback={<Loading />}>
        {children}
      </Suspense>
    </ErrorBoundary>
  );
}

function App() {
  return (
    <AsyncSection>
      <UserData />
    </AsyncSection>
  );
}
```

### SuspenseList (expérimental)

```tsx
import { SuspenseList, Suspense } from 'react';

function ProfilePage() {
  return (
    <SuspenseList revealOrder="forwards" tail="collapsed">
      <Suspense fallback={<ProfileSkeleton />}>
        <ProfileDetails />
      </Suspense>
      <Suspense fallback={<PostsSkeleton />}>
        <ProfilePosts />
      </Suspense>
      <Suspense fallback={<FriendsSkeleton />}>
        <ProfileFriends />
      </Suspense>
    </SuspenseList>
  );
}
```

## Transitions

### useTransition

```tsx
import { useState, useTransition, Suspense } from 'react';

function TabPanel() {
  const [tab, setTab] = useState('home');
  const [isPending, startTransition] = useTransition();

  const handleTabChange = (newTab: string) => {
    startTransition(() => {
      setTab(newTab);
    });
  };

  return (
    <div>
      <TabButtons
        currentTab={tab}
        onChange={handleTabChange}
        isPending={isPending}
      />

      <div style={{ opacity: isPending ? 0.7 : 1 }}>
        <Suspense fallback={<TabSkeleton />}>
          <TabContent tab={tab} />
        </Suspense>
      </div>
    </div>
  );
}
```

### useDeferredValue

```tsx
import { useState, useDeferredValue, Suspense } from 'react';

function SearchResults() {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);

  const isStale = query !== deferredQuery;

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
      />

      <div style={{ opacity: isStale ? 0.5 : 1 }}>
        <Suspense fallback={<SearchSkeleton />}>
          <Results query={deferredQuery} />
        </Suspense>
      </div>
    </div>
  );
}
```

## Skeleton Components

### Pattern

```tsx
function ProfileSkeleton() {
  return (
    <div className="profile-skeleton animate-pulse">
      <div className="avatar-skeleton" />
      <div className="name-skeleton" />
      <div className="bio-skeleton" />
    </div>
  );
}

// Avec Tailwind
function CardSkeleton() {
  return (
    <div className="border rounded-lg p-4 animate-pulse">
      <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
      <div className="h-4 bg-gray-200 rounded w-1/2" />
    </div>
  );
}
```

### Skeleton générique

```tsx
interface SkeletonProps {
  className?: string;
  width?: string | number;
  height?: string | number;
  rounded?: 'sm' | 'md' | 'lg' | 'full';
}

function Skeleton({
  className = '',
  width,
  height = '1rem',
  rounded = 'md',
}: SkeletonProps) {
  return (
    <div
      className={`bg-gray-200 animate-pulse rounded-${rounded} ${className}`}
      style={{ width, height }}
    />
  );
}

// Usage
function UserSkeleton() {
  return (
    <div className="flex items-center gap-4">
      <Skeleton width={48} height={48} rounded="full" />
      <div>
        <Skeleton width={120} height={16} />
        <Skeleton width={80} height={14} className="mt-2" />
      </div>
    </div>
  );
}
```

## Route-based Code Splitting

```tsx
import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';

// Lazy load toutes les pages
const routes = [
  { path: '/', component: lazy(() => import('./pages/Home')) },
  { path: '/dashboard', component: lazy(() => import('./pages/Dashboard')) },
  { path: '/settings', component: lazy(() => import('./pages/Settings')) },
  { path: '/profile/:id', component: lazy(() => import('./pages/Profile')) },
];

function AppRoutes() {
  return (
    <Suspense fallback={<PageLoader />}>
      <Routes>
        {routes.map(({ path, component: Component }) => (
          <Route key={path} path={path} element={<Component />} />
        ))}
      </Routes>
    </Suspense>
  );
}
```

## Bonnes Pratiques

1. **Boundaries granulaires** - Un par section logique
2. **Skeletons ressemblants** - Même layout que le contenu
3. **Error Boundary** - Toujours avec Suspense
4. **Preload** - Anticiper les navigations
5. **Transitions** - Pour les updates non-urgentes

## Anti-patterns

```tsx
// ❌ Suspense autour de chaque composant
<Suspense><A /></Suspense>
<Suspense><B /></Suspense>
<Suspense><C /></Suspense>

// ✅ Grouper logiquement
<Suspense>
  <Header />
</Suspense>
<Suspense>
  <MainContent />
</Suspense>

// ❌ Fallback vide
<Suspense fallback={null}>

// ✅ Skeleton informatif
<Suspense fallback={<ContentSkeleton />}>
```

## Voir aussi

- `react-query.md` - Data fetching avec Suspense
- `../components/error-boundaries.md` - Gestion d'erreurs
- `../performance/code-splitting.md` - Optimisation bundle

## Livrables

| Livrable | Description |
|----------|-------------|
| Suspense boundaries | Composants avec fallbacks appropriés |
| Skeleton components | UI de chargement représentative du contenu |
| Code splitting | Configuration lazy loading avec React.lazy |
