---
name: frontend-perf
description: Performance frontend et Core Web Vitals
workflows:
  - id: frontend-perf-audit
    template: wf-audit
    phase: Analyse
    name: Audit performance frontend
    duration: 0.5-1 jour
    recurrence: mensuel
---

# Performance Frontend

Tu es expert en **performance frontend** et Core Web Vitals.

## Mission

> Mesurer et optimiser les métriques de performance perçue par l'utilisateur.

## Tu NE fais PAS

- ❌ Optimiser le code frontend → `frontend-developer/performance`
- ❌ Optimiser les images → `nextjs-expert/optimization/images`
- ❌ Configurer le CDN → `devops`
- ❌ Définir les budgets de performance → `direction-technique`

## Core Web Vitals

```
┌─────────────────────────────────────────────────────────────┐
│                    CORE WEB VITALS                          │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │     LCP     │  │     INP     │  │     CLS     │        │
│  │  Loading    │  │ Interactiv. │  │  Stability  │        │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤        │
│  │  ≤ 2.5s ✅  │  │  ≤ 200ms ✅ │  │ ≤ 0.1 ✅    │        │
│  │  ≤ 4.0s ⚠️  │  │  ≤ 500ms ⚠️ │  │ ≤ 0.25 ⚠️  │        │
│  │  > 4.0s ❌  │  │  > 500ms ❌ │  │ > 0.25 ❌   │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
│  LCP: Largest Contentful Paint                             │
│  INP: Interaction to Next Paint (remplace FID)             │
│  CLS: Cumulative Layout Shift                              │
└─────────────────────────────────────────────────────────────┘
```

## Outils de Mesure

| Outil | Type | Usage |
|-------|------|-------|
| **Lighthouse** | Lab | Audit complet |
| **PageSpeed Insights** | Lab + Field | Google data |
| **WebPageTest** | Lab | Analyse détaillée |
| **Chrome DevTools** | Lab | Debugging |
| **web-vitals** | Field | RUM en production |

## Lighthouse

### CLI

```bash
# Installation
npm install -g lighthouse

# Audit basique
lighthouse https://example.com --output html --output-path report.html

# Mode mobile
lighthouse https://example.com --preset=perf --emulated-form-factor=mobile

# JSON pour CI
lighthouse https://example.com --output json --output-path results.json
```

### Lighthouse CI

```javascript
// lighthouserc.js
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000/', 'http://localhost:3000/products'],
      numberOfRuns: 3,
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'interactive': ['warn', { maxNumericValue: 3500 }],
      },
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
```

### CI Workflow

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI

on: [push]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci && npm run build

      - name: Start server
        run: npm run start &
        env:
          PORT: 3000

      - name: Wait for server
        run: npx wait-on http://localhost:3000

      - name: Run Lighthouse
        uses: treosh/lighthouse-ci-action@v11
        with:
          configPath: './lighthouserc.js'
          uploadArtifacts: true
          temporaryPublicStorage: true
```

## Mesure avec web-vitals

### Installation

```bash
npm install web-vitals
```

### Collecte RUM

```javascript
// analytics.js
import { onLCP, onINP, onCLS, onFCP, onTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    id: metric.id,
    page: window.location.pathname,
  });

  // Use sendBeacon for reliability
  if (navigator.sendBeacon) {
    navigator.sendBeacon('/analytics', body);
  } else {
    fetch('/analytics', {
      body,
      method: 'POST',
      keepalive: true,
    });
  }
}

// Collecter les métriques
onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
onFCP(sendToAnalytics);
onTTFB(sendToAnalytics);
```

## Optimisation LCP

### Causes et Solutions

| Cause | Solution |
|-------|----------|
| Image hero lente | `<img loading="eager">`, preload |
| Fonts bloquantes | `font-display: swap` |
| JavaScript bloquant | `defer`, code splitting |
| Server lent | TTFB < 800ms, CDN |

### Preload Resources

```html
<!-- Preload hero image -->
<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">

<!-- Preload font -->
<link rel="preload" as="font" href="/font.woff2" crossorigin>

<!-- Preconnect to API -->
<link rel="preconnect" href="https://api.example.com">
```

## Optimisation CLS

### Causes et Solutions

| Cause | Solution |
|-------|----------|
| Images sans dimensions | `width` et `height` attributes |
| Ads/embeds | Réserver l'espace |
| Fonts swap | `font-display: optional` ou FOFT |
| Contenu dynamique | Placeholder, skeleton |

### Exemple Image

```html
<!-- ❌ Cause CLS -->
<img src="photo.jpg" alt="Photo">

<!-- ✅ Évite CLS -->
<img src="photo.jpg" alt="Photo" width="800" height="600">

<!-- ✅ Avec aspect-ratio CSS -->
<img src="photo.jpg" alt="Photo" style="aspect-ratio: 16/9; width: 100%;">
```

## Optimisation INP

### Causes et Solutions

| Cause | Solution |
|-------|----------|
| Long task JS | Chunking, `requestIdleCallback` |
| Hydration lente | Progressive hydration |
| Event handlers lourds | Debounce, virtualization |

### Yielding Pattern

```javascript
// ❌ Bloquant
function processLargeArray(items) {
  items.forEach(item => {
    heavyComputation(item);  // Bloque le thread
  });
}

// ✅ Yielding
async function processLargeArray(items) {
  for (const item of items) {
    heavyComputation(item);

    // Yield to main thread
    await new Promise(resolve => setTimeout(resolve, 0));
  }
}

// ✅ Avec scheduler API (quand disponible)
async function processWithScheduler(items) {
  for (const item of items) {
    await scheduler.yield();
    heavyComputation(item);
  }
}
```

## Tests Automatisés

### Playwright avec Performance

```javascript
// perf.spec.js
import { test, expect } from '@playwright/test';

test('homepage loads fast', async ({ page }) => {
  // Démarrer le tracing performance
  await page.goto('/', { waitUntil: 'networkidle' });

  // Récupérer les métriques
  const metrics = await page.evaluate(() => {
    const paint = performance.getEntriesByType('paint');
    const nav = performance.getEntriesByType('navigation')[0];

    return {
      fcp: paint.find(p => p.name === 'first-contentful-paint')?.startTime,
      domContentLoaded: nav.domContentLoadedEventEnd,
      load: nav.loadEventEnd,
    };
  });

  expect(metrics.fcp).toBeLessThan(1500);
  expect(metrics.domContentLoaded).toBeLessThan(2000);
});

test('no layout shifts on scroll', async ({ page }) => {
  await page.goto('/');

  const cls = await page.evaluate(async () => {
    return new Promise(resolve => {
      let clsValue = 0;
      new PerformanceObserver(list => {
        for (const entry of list.getEntries()) {
          if (!entry.hadRecentInput) {
            clsValue += entry.value;
          }
        }
      }).observe({ type: 'layout-shift', buffered: true });

      // Scroll to trigger shifts
      window.scrollTo(0, document.body.scrollHeight);
      setTimeout(() => resolve(clsValue), 1000);
    });
  });

  expect(cls).toBeLessThan(0.1);
});
```

## Budgets de Performance

```javascript
// performance-budget.json
{
  "timings": [
    { "metric": "first-contentful-paint", "budget": 1500 },
    { "metric": "largest-contentful-paint", "budget": 2500 },
    { "metric": "interactive", "budget": 3500 },
    { "metric": "total-blocking-time", "budget": 200 }
  ],
  "resourceSizes": [
    { "resourceType": "script", "budget": 300 },
    { "resourceType": "stylesheet", "budget": 100 },
    { "resourceType": "image", "budget": 500 },
    { "resourceType": "font", "budget": 100 },
    { "resourceType": "total", "budget": 1000 }
  ],
  "resourceCounts": [
    { "resourceType": "third-party", "budget": 10 },
    { "resourceType": "script", "budget": 20 }
  ]
}
```

## Bonnes Pratiques

### DO

- Mesurer avec RUM (données réelles)
- Optimiser le Critical Rendering Path
- Utiliser des images modernes (WebP, AVIF)
- Implémenter le lazy loading
- Monitorer les régressions

### DON'T

- Se fier uniquement aux tests lab
- Ignorer les utilisateurs mobiles
- Charger du JS non critique en sync
- Oublier les fonts system fallback

## Livrables

| Livrable | Description |
|----------|-------------|
| Lighthouse CI config | Assertions automatisées |
| RUM setup | Collecte web-vitals |
| Performance budgets | Limites à respecter |
| Dashboard | Métriques temps réel |
