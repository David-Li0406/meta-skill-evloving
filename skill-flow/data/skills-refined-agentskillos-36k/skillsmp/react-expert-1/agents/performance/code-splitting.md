---
name: code-splitting
description: Lazy loading and bundle optimization with React.lazy
workflows:
  - id: code-splitting-setup
    template: wf-evolution
    phase: Réalisation
    name: Setup code splitting
    duration: 0.5-1 jour
---

# Code Splitting - Lazy Loading et Optimisation Bundle

## Rôle

Réduction de la taille du bundle initial avec le code splitting et le lazy loading.

## Tu NE fais PAS

- ❌ Optimiser le backend ou les APIs → `backend-developer`
- ❌ Implémenter les corrections (juste identifier et conseiller) → développeur
- ❌ Gérer la configuration webpack/vite avancée → `devops`
- ❌ Optimiser les re-renders → `memoization.md`

## React.lazy

### Syntaxe de base

```tsx
import { lazy, Suspense } from 'react';

// Import dynamique
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));
const Profile = lazy(() => import('./pages/Profile'));

function App() {
  return (
    <Suspense fallback={<PageLoader />}>
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
const MyComponent = lazy(() =>
  import('./components/MyComponent').then((module) => ({
    default: module.MyComponent,
  }))
);

// Ou exporter un helper
function lazyNamed<T extends React.ComponentType<any>>(
  factory: () => Promise<{ [key: string]: T }>,
  name: string
) {
  return lazy(() =>
    factory().then((module) => ({ default: module[name] }))
  );
}

const MyComponent = lazyNamed(
  () => import('./components'),
  'MyComponent'
);
```

## Route-based Splitting

### Pattern recommandé

```tsx
import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';

// Lazy load toutes les pages
const routes = [
  { path: '/', element: lazy(() => import('./pages/Home')) },
  { path: '/about', element: lazy(() => import('./pages/About')) },
  { path: '/dashboard/*', element: lazy(() => import('./pages/Dashboard')) },
  { path: '/settings', element: lazy(() => import('./pages/Settings')) },
];

function AppRoutes() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Routes>
        {routes.map(({ path, element: Element }) => (
          <Route key={path} path={path} element={<Element />} />
        ))}
      </Routes>
    </Suspense>
  );
}
```

### Nested Routes

```tsx
// pages/Dashboard/index.tsx
import { lazy, Suspense } from 'react';
import { Routes, Route, Outlet } from 'react-router-dom';

const Overview = lazy(() => import('./Overview'));
const Analytics = lazy(() => import('./Analytics'));
const Reports = lazy(() => import('./Reports'));

function DashboardLayout() {
  return (
    <div className="dashboard">
      <Sidebar />
      <main>
        <Suspense fallback={<SectionLoader />}>
          <Outlet />
        </Suspense>
      </main>
    </div>
  );
}

export default function Dashboard() {
  return (
    <Routes>
      <Route element={<DashboardLayout />}>
        <Route index element={<Overview />} />
        <Route path="analytics" element={<Analytics />} />
        <Route path="reports" element={<Reports />} />
      </Route>
    </Routes>
  );
}
```

## Component-based Splitting

### Modales et Drawers

```tsx
import { lazy, Suspense, useState } from 'react';

// Lazy load les modales
const SettingsModal = lazy(() => import('./SettingsModal'));
const ProfileEditor = lazy(() => import('./ProfileEditor'));

function App() {
  const [showSettings, setShowSettings] = useState(false);

  return (
    <div>
      <button onClick={() => setShowSettings(true)}>Settings</button>

      {showSettings && (
        <Suspense fallback={<ModalSkeleton />}>
          <SettingsModal onClose={() => setShowSettings(false)} />
        </Suspense>
      )}
    </div>
  );
}
```

### Composants lourds

```tsx
// Lazy load éditeur WYSIWYG, charts, etc.
const RichTextEditor = lazy(() => import('./RichTextEditor'));
const DataVisualization = lazy(() => import('./DataVisualization'));

function ArticleEditor() {
  return (
    <div>
      <Suspense fallback={<EditorSkeleton />}>
        <RichTextEditor />
      </Suspense>
    </div>
  );
}
```

## Preloading

### Sur événement

```tsx
const Dashboard = lazy(() => import('./Dashboard'));

function Navigation() {
  const preloadDashboard = () => {
    // Précharger au hover
    import('./Dashboard');
  };

  return (
    <nav>
      <Link
        to="/dashboard"
        onMouseEnter={preloadDashboard}
        onFocus={preloadDashboard}
      >
        Dashboard
      </Link>
    </nav>
  );
}
```

### Avec hook

```tsx
function usePreload(importFn: () => Promise<any>) {
  const preloaded = useRef(false);

  const preload = useCallback(() => {
    if (!preloaded.current) {
      importFn();
      preloaded.current = true;
    }
  }, [importFn]);

  return preload;
}

// Usage
function NavLink({ to, importFn, children }) {
  const preload = usePreload(importFn);

  return (
    <Link to={to} onMouseEnter={preload}>
      {children}
    </Link>
  );
}

<NavLink to="/dashboard" importFn={() => import('./Dashboard')}>
  Dashboard
</NavLink>
```

### Preload conditionnel

```tsx
// Preload après le chargement initial
useEffect(() => {
  // Attendre que l'app soit interactive
  const timer = setTimeout(() => {
    import('./Dashboard');
    import('./Settings');
  }, 2000);

  return () => clearTimeout(timer);
}, []);
```

## Vite / Webpack Hints

### Magic Comments (Webpack)

```tsx
// Nommer le chunk
const Dashboard = lazy(() =>
  import(/* webpackChunkName: "dashboard" */ './Dashboard')
);

// Prefetch
const Settings = lazy(() =>
  import(/* webpackPrefetch: true */ './Settings')
);

// Preload
const Profile = lazy(() =>
  import(/* webpackPreload: true */ './Profile')
);
```

### Vite

```tsx
// Vite génère automatiquement des chunks
// Le nom du chunk est basé sur le chemin du fichier

// Rollup options dans vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          charts: ['recharts', 'd3'],
        },
      },
    },
  },
});
```

## Error Boundaries

### Gérer les erreurs de chargement

```tsx
import { ErrorBoundary } from 'react-error-boundary';

function ChunkErrorFallback({ error, resetErrorBoundary }) {
  // Erreur de chargement de chunk (souvent après deploy)
  if (error.name === 'ChunkLoadError') {
    return (
      <div>
        <p>A new version is available.</p>
        <button onClick={() => window.location.reload()}>
          Refresh
        </button>
      </div>
    );
  }

  return (
    <div>
      <p>Something went wrong.</p>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary FallbackComponent={ChunkErrorFallback}>
      <Suspense fallback={<PageLoader />}>
        <Routes />
      </Suspense>
    </ErrorBoundary>
  );
}
```

## Analyse du Bundle

### Vite

```bash
npm install -D rollup-plugin-visualizer
```

```ts
// vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    react(),
    visualizer({ open: true }),
  ],
});
```

### Webpack

```bash
npm install -D webpack-bundle-analyzer
```

```js
// webpack.config.js
const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin(),
  ],
};
```

## Patterns Avancés

### Library Splitting

```tsx
// Lazy load les gros packages
const Chart = lazy(async () => {
  const { Chart } = await import('chart.js');
  const { Line } = await import('react-chartjs-2');
  // Register Chart.js components
  Chart.register(...);
  return { default: Line };
});
```

### Feature Flags

```tsx
const ExperimentalFeature = lazy(() =>
  import('./ExperimentalFeature')
);

function App() {
  const { isEnabled } = useFeatureFlag('experimental');

  return (
    <div>
      {isEnabled && (
        <Suspense fallback={<Loader />}>
          <ExperimentalFeature />
        </Suspense>
      )}
    </div>
  );
}
```

## Bonnes Pratiques

1. **Route-based d'abord** - Plus gros impact
2. **Composants lourds** - Modales, éditeurs, charts
3. **Précharger** - Sur hover/focus pour UX fluide
4. **Suspense boundaries** - Granularité appropriée
5. **Analyser** - Vérifier les chunks générés

## Voir aussi

- `memoization.md` - Optimisation runtime
- `../data/suspense.md` - Data fetching
- `../components/error-boundaries.md` - Gestion d'erreurs

## Livrables

| Livrable | Description |
|----------|-------------|
| Configuration lazy loading | Code React.lazy avec Suspense boundaries |
| Stratégie de splitting | Plan route-based et component-based |
| Analyse bundle | Rapport avec webpack-bundle-analyzer ou visualizer |
