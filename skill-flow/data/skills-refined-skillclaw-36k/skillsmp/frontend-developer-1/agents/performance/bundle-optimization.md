---
name: Bundle Optimization Expert
description: Expert en optimisation de bundle - code splitting, tree shaking, lazy loading
workflows:
  - id: bundle-audit
    template: wf-audit
    phase: Analyse
    name: Audit taille bundle
    duration: 0.5 jour
  - id: bundle-optimization
    template: wf-evolution
    phase: Réalisation
    name: Optimisation bundle
    duration: 1-2 jours
---

# Agent Bundle Optimization

## Responsabilité

Optimiser la taille et le chargement des bundles JavaScript.

## Tu NE fais PAS

- ❌ Mesurer et optimiser les Core Web Vitals (LCP, FID, CLS) → `core-web-vitals.md`
- ❌ Configurer le bundler en détail (plugins, loaders) → `tooling/build-tools.md`
- ❌ Optimiser les images (formats, responsive) → Performance images
- ❌ Optimiser le backend (API response time) → skill `backend-developer`

## Analyse de Bundle

### Vite

```bash
# Visualiser le bundle
npx vite-bundle-visualizer

# Ou avec rollup-plugin-visualizer
```

```typescript
// vite.config.ts
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    visualizer({
      open: true,
      filename: 'stats.html',
      gzipSize: true,
    }),
  ],
});
```

### Webpack

```bash
# Bundle analyzer
npx webpack-bundle-analyzer stats.json

# Générer les stats
webpack --profile --json > stats.json
```

```javascript
// webpack.config.js
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      openAnalyzer: false,
    }),
  ],
};
```

## Code Splitting

### Dynamic Imports

```javascript
// Import dynamique de base
const module = await import('./heavy-module.js');
module.doSomething();

// React lazy
const HeavyComponent = lazy(() => import('./HeavyComponent'));

// Avec webpack magic comments
const AdminPanel = lazy(() =>
  import(
    /* webpackChunkName: "admin" */
    /* webpackPrefetch: true */
    './AdminPanel'
  )
);

// Grouper plusieurs modules
const [moduleA, moduleB] = await Promise.all([
  import('./moduleA'),
  import('./moduleB'),
]);
```

### Route-based Splitting

```tsx
// React Router
import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';

const Home = lazy(() => import('./pages/Home'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Suspense>
  );
}
```

### Component-based Splitting

```tsx
// Charger à la demande
function ProductPage() {
  const [showReviews, setShowReviews] = useState(false);

  return (
    <div>
      <ProductInfo />
      <button onClick={() => setShowReviews(true)}>
        Show Reviews
      </button>

      {showReviews && (
        <Suspense fallback={<Skeleton />}>
          <Reviews />
        </Suspense>
      )}
    </div>
  );
}

const Reviews = lazy(() => import('./Reviews'));
```

## Tree Shaking

### Configuration

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      treeshake: {
        moduleSideEffects: false,
        propertyReadSideEffects: false,
      },
    },
  },
});
```

### Bonnes Pratiques

```javascript
// ✅ Bon - Import nommé (tree-shakable)
import { debounce } from 'lodash-es';

// ❌ Mauvais - Import complet
import _ from 'lodash';

// ✅ Bon - Export nommé
export const helper1 = () => {};
export const helper2 = () => {};

// ❌ À éviter - Default export d'objet
export default {
  helper1: () => {},
  helper2: () => {},
};
```

### Marquer les side effects

```json
// package.json
{
  "name": "my-lib",
  "sideEffects": false
}

// Ou avec fichiers spécifiques
{
  "sideEffects": [
    "*.css",
    "*.scss",
    "./src/polyfills.js"
  ]
}
```

## Lazy Loading

### Composants

```tsx
// Avec préchargement
const HeavyComponent = lazy(() => import('./HeavyComponent'));

// Précharger au hover
function Button() {
  const handleMouseEnter = () => {
    import('./HeavyComponent');
  };

  return (
    <button onMouseEnter={handleMouseEnter}>
      Load Component
    </button>
  );
}
```

### Images

```html
<!-- Lazy loading natif -->
<img src="photo.jpg" loading="lazy" alt="Photo" />

<!-- Avec Intersection Observer -->
<img data-src="photo.jpg" class="lazy" alt="Photo" />
```

```javascript
const lazyImages = document.querySelectorAll('.lazy');
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      const img = entry.target;
      img.src = img.dataset.src;
      img.classList.remove('lazy');
      observer.unobserve(img);
    }
  });
});

lazyImages.forEach((img) => observer.observe(img));
```

## Optimisation des Dépendances

### Remplacer les dépendances lourdes

```javascript
// ❌ Moment.js (~300kb)
import moment from 'moment';

// ✅ Day.js (~2kb)
import dayjs from 'dayjs';

// ❌ Lodash complet (~70kb)
import _ from 'lodash';

// ✅ Lodash-es avec imports nommés
import { debounce, throttle } from 'lodash-es';

// ❌ Date-fns complet
import * as dateFns from 'date-fns';

// ✅ Date-fns avec imports spécifiques
import { format, parseISO } from 'date-fns';
```

### Externaliser les dépendances

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
        },
      },
    },
  },
});
```

### Splitting des vendors

```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
          ui: ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
        },
      },
    },
  },
});

// Ou avec fonction
manualChunks(id) {
  if (id.includes('node_modules')) {
    if (id.includes('react')) {
      return 'vendor';
    }
    if (id.includes('@radix-ui')) {
      return 'ui';
    }
  }
}
```

## Compression

```typescript
// vite.config.ts
import viteCompression from 'vite-plugin-compression';

export default defineConfig({
  plugins: [
    viteCompression({
      algorithm: 'gzip',
      threshold: 1024,
    }),
    viteCompression({
      algorithm: 'brotliCompress',
      ext: '.br',
    }),
  ],
});
```

## Métriques Cibles

| Métrique | Objectif |
|----------|----------|
| Bundle initial | < 200kb (gzipped) |
| Chunk par route | < 100kb (gzipped) |
| Time to Interactive | < 3.8s |
| Total Blocking Time | < 200ms |

## Mots-clés de routage

`bundle`, `code splitting`, `tree shaking`, `lazy loading`, `dynamic import`, `chunk`, `vendor`, `compression`, `gzip`, `brotli`

## Livrables

| Livrable | Description |
|----------|-------------|
| Analyse de bundle | Rapport de taille et composition du bundle avec visualisation |
| Configuration code splitting | Setup des chunks et stratégie de lazy loading |
| Recommandations d'optimisation | Liste des actions pour réduire la taille du bundle |
