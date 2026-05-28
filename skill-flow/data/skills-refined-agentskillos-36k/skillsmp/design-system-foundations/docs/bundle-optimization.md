# Bundle Optimization

Guide pour optimiser la taille du bundle et les performances de chargement du design system.

## Tree-Shaking des Composants React

### ✅ Bonnes pratiques d'import

```tsx
// ✅ BON: Named imports - permet le tree-shaking
import { Button, Input } from '@design-system/components';

// ✅ BON: Import direct depuis le module
import { Button } from '@design-system/components/Button';
import { Input } from '@design-system/components/Input';

// ❌ MAUVAIS: Import * - inclut tout le package
import * as Components from '@design-system/components';

// ❌ MAUVAIS: Import default puis destructure
import Components from '@design-system/components';
const { Button, Input } = Components;
```

### Configuration package.json

```json
{
  "name": "@design-system/components",
  "sideEffects": false,
  "exports": {
    ".": {
      "import": "./dist/esm/index.js",
      "require": "./dist/cjs/index.js",
      "types": "./dist/types/index.d.ts"
    },
    "./Button": {
      "import": "./dist/esm/Button/index.js",
      "require": "./dist/cjs/Button/index.js",
      "types": "./dist/types/Button/index.d.ts"
    }
  }
}
```

### Barrel File Optimisé

```ts
// ❌ MAUVAIS: Re-export tout (empêche tree-shaking)
export * from './Button';
export * from './Input';
export * from './Modal';

// ✅ BON: Named re-exports explicites
export { Button } from './Button';
export type { ButtonProps } from './Button';
export { Input } from './Input';
export type { InputProps } from './Input';
```

## Code-Splitting par Route

### React.lazy pour les composants lourds

```tsx
import { lazy, Suspense } from 'react';

// Lazy load des composants complexes
const Modal = lazy(() => import('@design-system/components/Modal'));
const DataTable = lazy(() => import('@design-system/components/DataTable'));
const RichTextEditor = lazy(() => import('@design-system/components/RichTextEditor'));

function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <Modal isOpen={showModal}>
        <DataTable data={data} />
      </Modal>
    </Suspense>
  );
}
```

### Composants à toujours lazy-loader

| Composant | Raison | Taille typique |
|-----------|--------|----------------|
| Modal/Dialog | DOM Portal, focus trap | ~15-25 KB |
| DataTable | Virtualisation, tri | ~30-50 KB |
| DatePicker | Calendrier, i18n | ~20-40 KB |
| RichTextEditor | WYSIWYG engine | ~100+ KB |
| Charts | D3/Recharts | ~50-100 KB |
| Maps | Mapbox/Leaflet | ~100+ KB |

### Composants à charger immédiatement

```tsx
// Ces composants sont petits et utilisés partout
// Ne pas les lazy-loader
import { Button, Input, Label, Badge, Spinner } from '@design-system/components';
```

## CSS Loading Strategy

### Architecture CSS en couches

```
┌─────────────────────────────────────────────────────────────────────┐
│                     CSS LOADING PRIORITY                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  CRITICAL (inline dans <head>)              ~3-5 KB                 │
│  ├── CSS Reset/Normalize                                            │
│  ├── CSS Custom Properties (tokens)                                 │
│  ├── Typography base                                                │
│  └── Layout primitives (container, grid)                            │
│                                                                      │
│  ABOVE-THE-FOLD (preload)                   ~10-20 KB               │
│  ├── Header/Navigation                                              │
│  ├── Hero section                                                   │
│  └── Buttons, Inputs (CTA)                                          │
│                                                                      │
│  DEFERRED (lazy-load)                       Variable                │
│  ├── Footer                                                         │
│  ├── Modal/Dialog                                                   │
│  ├── Forms complexes                                                │
│  └── Components below-the-fold                                      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Critical CSS Extraction

```html
<!DOCTYPE html>
<html>
<head>
  <!-- Critical CSS inline -->
  <style>
    /* tokens.css - ~2KB */
    :root {
      --color-primary: #2563eb;
      --color-background: #ffffff;
      --color-foreground: #18181b;
      --font-sans: 'Inter', system-ui, sans-serif;
      --space-4: 1rem;
      --radius-md: 0.5rem;
    }

    /* reset.css - ~1KB */
    *, *::before, *::after { box-sizing: border-box; margin: 0; }
    body { font-family: var(--font-sans); line-height: 1.5; }

    /* layout.css - ~1KB */
    .container { max-width: 1280px; margin: 0 auto; padding: 0 1rem; }
  </style>

  <!-- Non-critical CSS: preload puis load -->
  <link rel="preload" href="/css/components.css" as="style" />
  <link rel="stylesheet" href="/css/components.css" />
</head>
</html>
```

### CSS-in-JS avec extraction

```tsx
// Avec styled-components ou emotion
// Configuration babel pour extraction statique

// babel.config.js
module.exports = {
  presets: ['@babel/preset-react'],
  plugins: [
    ['babel-plugin-styled-components', {
      ssr: true,
      displayName: process.env.NODE_ENV !== 'production',
      pure: true,
    }],
  ],
};
```

### CSS Modules avec Critical Extraction

```js
// next.config.js (Next.js example)
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});

module.exports = withBundleAnalyzer({
  experimental: {
    optimizeCss: true, // Enables critters for critical CSS
  },
});
```

### Stratégie de chargement par composant

```tsx
// Component avec styles lazy-loadés
import { useState, useEffect } from 'react';

function Modal({ children, isOpen }: ModalProps) {
  const [stylesLoaded, setStylesLoaded] = useState(false);

  useEffect(() => {
    if (isOpen && !stylesLoaded) {
      // Charge les styles uniquement quand nécessaire
      import('./Modal.css').then(() => setStylesLoaded(true));
    }
  }, [isOpen, stylesLoaded]);

  if (!isOpen) return null;

  return (
    <div className={stylesLoaded ? 'modal' : 'modal-loading'}>
      {children}
    </div>
  );
}
```

## Analyse du Bundle

### Outils recommandés

```bash
# webpack-bundle-analyzer
npm install --save-dev webpack-bundle-analyzer
npx webpack --profile --json > stats.json
npx webpack-bundle-analyzer stats.json

# source-map-explorer (pour CRA/Vite)
npm install --save-dev source-map-explorer
npx source-map-explorer build/static/js/*.js

# Next.js built-in
ANALYZE=true npm run build

# Vite
npm install --save-dev rollup-plugin-visualizer
```

### Budget de taille recommandé

| Type | Budget | Critique |
|------|--------|----------|
| JS Initial | < 100 KB (gzip) | > 200 KB |
| CSS Initial | < 30 KB (gzip) | > 50 KB |
| Total Initial | < 150 KB (gzip) | > 300 KB |
| Largest Chunk | < 50 KB (gzip) | > 100 KB |

### Configuration bundler

```js
// vite.config.js
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Vendor chunks
          'react-vendor': ['react', 'react-dom'],
          'ui-vendor': ['framer-motion', '@radix-ui/react-dialog'],

          // Design system chunks
          'ds-foundations': [
            '@design-system/tokens',
            '@design-system/utils',
          ],
          'ds-atoms': [
            '@design-system/components/Button',
            '@design-system/components/Input',
            '@design-system/components/Badge',
          ],
          'ds-molecules': [
            '@design-system/components/Card',
            '@design-system/components/Modal',
          ],
        },
      },
    },
  },
};
```

## Font Optimization

### Subset et Preload

```html
<!-- Preload uniquement les fonts critiques -->
<link
  rel="preload"
  href="/fonts/inter-400-latin.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>

<!-- Variable font (toutes les weights en un fichier) -->
<link
  rel="preload"
  href="/fonts/inter-variable.woff2"
  as="font"
  type="font/woff2"
  crossorigin
/>
```

### Self-hosted vs CDN

```css
/* Self-hosted (recommandé) - contrôle total */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-variable.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
}

/* Google Fonts avec display=swap */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
```

## Icons Optimization

### SVG Sprite vs Individual Icons

```tsx
// ❌ MAUVAIS: Importer tous les icons
import * as Icons from 'lucide-react'; // ~500KB

// ✅ BON: Import individuel
import { ChevronDown, Search, X } from 'lucide-react'; // ~3KB

// ✅ MIEUX: SVG Sprite
<svg>
  <use href="/icons.svg#chevron-down" />
</svg>
```

### Icon Component optimisé

```tsx
// Lazy-load icons par catégorie
const NavigationIcons = lazy(() => import('./icons/navigation'));
const ActionIcons = lazy(() => import('./icons/actions'));

// Ou utiliser un sprite généré au build
// avec svg-sprite-loader ou vite-plugin-svg-icons
```

## Checklist Bundle Optimization

### JavaScript
- [ ] Named imports pour tous les composants
- [ ] `sideEffects: false` dans package.json
- [ ] Code-splitting avec React.lazy pour composants > 10KB
- [ ] Chunks séparés pour vendors et design system
- [ ] Analyse régulière avec bundle analyzer

### CSS
- [ ] Critical CSS inline dans `<head>` (tokens, reset, layout)
- [ ] Preload pour CSS above-the-fold
- [ ] Lazy-load pour composants below-the-fold
- [ ] PurgeCSS pour supprimer le CSS non utilisé

### Fonts
- [ ] Subsets (latin uniquement si suffisant)
- [ ] Variable fonts si > 3 weights utilisés
- [ ] Preload pour font principale
- [ ] font-display: swap

### Icons
- [ ] Import individuel (pas de `import *`)
- [ ] SVG sprite pour > 10 icons
- [ ] Lazy-load par catégorie si > 50 icons

### Monitoring
- [ ] Budget de taille défini et surveillé
- [ ] Lighthouse CI dans le pipeline
- [ ] Alertes si bundle dépasse le budget
