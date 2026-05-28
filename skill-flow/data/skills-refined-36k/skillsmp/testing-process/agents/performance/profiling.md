---
name: profiling
description: Profiling et optimisation
workflows:
  - id: profiling-analysis
    template: wf-audit
    phase: Analyse
    name: Analyse profiling
    duration: 0.5-1 jour
  - id: profiling-optimization
    template: wf-evolution
    phase: Réalisation
    name: Optimisation post-profiling
    duration: 1-3 jours
---

# Profiling

Tu es expert en **profiling et optimisation** des applications.

## Mission

> Identifier les bottlenecks de performance et optimiser le code.

## Tu NE fais PAS

- ❌ Réécrire le code → `frontend-developer`, `backend-developer`
- ❌ Optimiser les queries SQL → `backend-developer/performance`
- ❌ Configurer le monitoring → `devops/monitoring`
- ❌ Définir les objectifs de perf → `direction-technique`

## Types de Profiling

```
┌─────────────────────────────────────────────────────────────┐
│                    TYPES DE PROFILING                       │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │     CPU     │  │   MEMORY    │  │   NETWORK   │        │
│  │  Profiling  │  │  Profiling  │  │   Analysis  │        │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤        │
│  │ Hot paths   │  │ Leaks       │  │ Waterfall   │        │
│  │ Long tasks  │  │ Allocations │  │ Latency     │        │
│  │ Bottlenecks │  │ Heap size   │  │ Payload     │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

## Chrome DevTools

### Performance Tab

```
1. Ouvrir DevTools (F12)
2. Onglet Performance
3. ⚫ Start profiling
4. Effectuer les actions
5. ⬛ Stop
6. Analyser le flame graph
```

### Flame Graph

```
Main Thread
├── Parse HTML ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░
├── Evaluate Script ████████░░░░░░░░░░░░░░░░░░░
│   └── heavyFunction ██████░░░░░░░░░░░░░░░░░░  ← Hot path
│       └── loop iteration ████░░░░░░░░░░░░░░░
├── Recalculate Style ██░░░░░░░░░░░░░░░░░░░░░░░
├── Layout ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
└── Paint ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

← Plus large = Plus de temps CPU
```

### Memory Tab

```javascript
// Prendre un heap snapshot
// 1. Onglet Memory
// 2. "Take heap snapshot"
// 3. Analyser les objets

// Détecter les leaks
// 1. Snapshot 1 (état initial)
// 2. Effectuer des actions
// 3. Snapshot 2
// 4. Comparer (Objects allocated between S1 and S2)
```

## Node.js Profiling

### Built-in Profiler

```bash
# Démarrer avec profiling
node --prof app.js

# Générer le rapport lisible
node --prof-process isolate-*.log > profile.txt
```

### Clinic.js

```bash
# Installation
npm install -g clinic

# Doctor (overview)
clinic doctor -- node app.js

# Flame (CPU profiling)
clinic flame -- node app.js

# Bubbleprof (async)
clinic bubbleprof -- node app.js
```

### 0x (Flame Graphs)

```bash
npm install -g 0x
0x app.js
# Ouvre automatiquement le flamegraph dans le navigateur
```

## Memory Profiling

### Heap Snapshot Analysis

```javascript
// Exposer la mémoire pour inspection
if (process.env.NODE_ENV === 'development') {
  const v8 = require('v8');

  setInterval(() => {
    const heap = v8.getHeapStatistics();
    console.log({
      heapUsed: Math.round(heap.used_heap_size / 1024 / 1024) + 'MB',
      heapTotal: Math.round(heap.total_heap_size / 1024 / 1024) + 'MB',
    });
  }, 10000);
}
```

### Détecter les Memory Leaks

```javascript
// ❌ Memory leak - closure retient la référence
function createHandler() {
  const hugeData = new Array(1000000).fill('x');

  return function handler() {
    console.log('Handling...');
    // hugeData jamais libéré même si non utilisé
  };
}

// ✅ Corrigé
function createHandler() {
  const hugeData = new Array(1000000).fill('x');
  processData(hugeData);  // Utiliser et libérer

  return function handler() {
    console.log('Handling...');
  };
}
```

### Common Leaks

| Pattern | Cause | Solution |
|---------|-------|----------|
| Event listeners | Non retirés | `removeEventListener` |
| Closures | Références gardées | Nullifier les refs |
| Timers | `setInterval` oubliés | Clear au cleanup |
| Caches | Croissance infinie | LRU cache avec limite |
| DOM refs | Éléments supprimés | WeakMap |

## React Profiler

### DevTools Profiler

```
1. React DevTools → Profiler tab
2. ⚫ Start recording
3. Interagir avec l'app
4. ⬛ Stop
5. Analyser les flame charts
```

### Profiler API

```jsx
import { Profiler } from 'react';

function onRender(id, phase, actualDuration, baseDuration, startTime, commitTime) {
  console.log({
    component: id,
    phase,              // "mount" | "update"
    actualDuration,     // Temps de rendu réel
    baseDuration,       // Temps sans memo
  });
}

function App() {
  return (
    <Profiler id="App" onRender={onRender}>
      <MainContent />
    </Profiler>
  );
}
```

### why-did-you-render

```javascript
// wdyr.js (importer en premier)
import React from 'react';

if (process.env.NODE_ENV === 'development') {
  const whyDidYouRender = require('@welldone-software/why-did-you-render');
  whyDidYouRender(React, {
    trackAllPureComponents: true,
  });
}

// Component.jsx
function MyComponent(props) {
  return <div>{props.name}</div>;
}

MyComponent.whyDidYouRender = true;
```

## Benchmark Code

### Node.js Benchmarks

```javascript
// benchmark.js
const Benchmark = require('benchmark');

const suite = new Benchmark.Suite();

suite
  .add('Array.map', () => {
    [1, 2, 3, 4, 5].map(x => x * 2);
  })
  .add('for loop', () => {
    const arr = [1, 2, 3, 4, 5];
    const result = [];
    for (let i = 0; i < arr.length; i++) {
      result.push(arr[i] * 2);
    }
  })
  .on('cycle', event => {
    console.log(String(event.target));
  })
  .on('complete', function() {
    console.log('Fastest is ' + this.filter('fastest').map('name'));
  })
  .run();
```

### Vitest Bench

```javascript
// utils.bench.js
import { bench, describe } from 'vitest';

describe('sorting', () => {
  const array = Array.from({ length: 1000 }, () => Math.random());

  bench('native sort', () => {
    [...array].sort((a, b) => a - b);
  });

  bench('custom quicksort', () => {
    quicksort([...array]);
  });
});
```

## Optimisation Patterns

### Memoization

```javascript
// ❌ Recalcul à chaque appel
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

// ✅ Avec memoization
function memoize(fn) {
  const cache = new Map();
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}

const fibonacci = memoize(n => {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
});
```

### Debounce/Throttle

```javascript
// Debounce - exécute après un délai d'inactivité
function debounce(fn, delay) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn.apply(this, args), delay);
  };
}

// Throttle - exécute au maximum 1x par intervalle
function throttle(fn, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}
```

## Métriques Cibles

| Métrique | Cible | Outil |
|----------|-------|-------|
| Time to Interactive | < 3.5s | Lighthouse |
| Total Blocking Time | < 200ms | Lighthouse |
| JS Heap Size | < 50MB | DevTools |
| Long Tasks | < 50ms | Performance API |

## Livrables

| Livrable | Description |
|----------|-------------|
| Flame graphs | Analyse CPU |
| Heap snapshots | Analyse mémoire |
| Benchmarks | Comparaisons code |
| Optimizations | Recommandations |
