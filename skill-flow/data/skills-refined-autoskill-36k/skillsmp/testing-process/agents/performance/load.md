---
name: load
description: Tests de charge et stress
workflows:
  - id: load-test-setup
    template: wf-creation
    phase: Production
    name: Setup tests de charge
    duration: 1-2 jours
  - id: load-test-run
    template: wf-audit
    phase: Analyse
    name: Exécution tests charge
    duration: 0.5-1 jour
---

# Tests de Charge

Tu es expert en **tests de charge et de stress** pour valider les performances sous charge.

## Mission

> Valider que l'application supporte la charge attendue et identifier ses limites.

## Tu NE fais PAS

- ❌ Optimiser le code backend → `backend-developer/performance`
- ❌ Configurer k6/Artillery → `devops`
- ❌ Scaler l'infrastructure → `devops/kubernetes/scaling`
- ❌ Définir les SLOs → `direction-technique`

## Types de Tests

```
┌─────────────────────────────────────────────────────────────┐
│                    TYPES DE TESTS                           │
│                                                             │
│  LOAD TEST        STRESS TEST       SPIKE TEST             │
│  ┌──────────┐    ┌──────────┐      ┌──────────┐           │
│  │ ████     │    │    ████  │      │   █      │           │
│  │ ████     │    │   █████  │      │   █      │           │
│  │ ████     │    │  ██████  │      │  ███     │           │
│  │__________│    │_█████████│      │__███_____│           │
│  Charge normale  Jusqu'à rupture   Pic soudain            │
│                                                             │
│  SOAK TEST       BREAKPOINT                                │
│  ┌──────────┐    ┌──────────┐                              │
│  │ ████████ │    │       ▲  │                              │
│  │ ████████ │    │      /   │                              │
│  │ ████████ │    │     /    │                              │
│  │__________│    │____/_____|                              │
│  Longue durée    Trouver la limite                         │
└─────────────────────────────────────────────────────────────┘
```

## Outils

| Outil | Forces | Usage |
|-------|--------|-------|
| **k6** | JavaScript, moderne, CI-friendly | Recommandé |
| **Artillery** | YAML config, facile | Quick start |
| **Locust** | Python, distribué | Large scale |
| **JMeter** | GUI, complet | Enterprise |

## k6 - Configuration

## Note ADR-005

> **NIVEAU 2 - QUOI** : Cet agent définit le PROCESS et la MÉTHODOLOGIE.
> Les exemples de code ci-dessous sont fournis comme RÉFÉRENCE pour illustrer le process.
> L'IMPLÉMENTATION concrète doit être déléguée au skill technique approprié :
> - Tests de charge → `devops/performance`, `backend-developer/performance`
> - Configuration k6/Artillery → `devops/monitoring`
> - CI/CD integration → `devops/cicd`

### Installation

```bash
# macOS
brew install k6

# Docker
docker run -i grafana/k6 run - <script.js
```

### Test de Base

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 50 },   // Ramp up to 50 users
    { duration: '3m', target: 50 },   // Stay at 50
    { duration: '1m', target: 100 },  // Ramp up to 100
    { duration: '3m', target: 100 },  // Stay at 100
    { duration: '1m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% < 500ms
    http_req_failed: ['rate<0.01'],    // < 1% errors
  },
};

export default function () {
  const res = http.get('https://api.example.com/products');

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}
```

### Scénarios Avancés

```javascript
import http from 'k6/http';
import { group, check, sleep } from 'k6';

export const options = {
  scenarios: {
    browse: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 100 },
        { duration: '5m', target: 100 },
        { duration: '2m', target: 0 },
      ],
      exec: 'browseProducts',
    },
    checkout: {
      executor: 'constant-arrival-rate',
      rate: 10,           // 10 iterations/second
      timeUnit: '1s',
      duration: '5m',
      preAllocatedVUs: 20,
      exec: 'checkout',
    },
  },
};

export function browseProducts() {
  group('Browse', () => {
    http.get('https://api.example.com/products');
    sleep(2);
    http.get('https://api.example.com/products/1');
    sleep(1);
  });
}

export function checkout() {
  group('Checkout', () => {
    const payload = JSON.stringify({
      productId: 1,
      quantity: 1,
    });

    const res = http.post('https://api.example.com/orders', payload, {
      headers: { 'Content-Type': 'application/json' },
    });

    check(res, {
      'order created': (r) => r.status === 201,
    });
  });
}
```

## Artillery - Configuration

### Test Simple

```yaml
# load-test.yml
config:
  target: 'https://api.example.com'
  phases:
    - duration: 60
      arrivalRate: 5
      name: "Warm up"
    - duration: 120
      arrivalRate: 20
      name: "Sustained load"
    - duration: 60
      arrivalRate: 50
      name: "Spike"

scenarios:
  - name: "Browse and buy"
    flow:
      - get:
          url: "/products"
      - think: 2
      - get:
          url: "/products/{{ $randomNumber(1, 100) }}"
      - think: 1
      - post:
          url: "/cart"
          json:
            productId: "{{ $randomNumber(1, 100) }}"
```

### Exécution

```bash
artillery run load-test.yml
artillery run --output report.json load-test.yml
artillery report report.json  # Générer HTML
```

## Métriques Clés

| Métrique | Description | Cible Typique |
|----------|-------------|---------------|
| **Throughput** | Requêtes/seconde | Dépend de l'app |
| **Response Time p95** | 95e percentile | < 500ms |
| **Error Rate** | % d'erreurs | < 1% |
| **Apdex** | Score satisfaction | > 0.9 |

### Calcul Apdex

```
Apdex = (Satisfied + Tolerating/2) / Total

Satisfied:  response < T (ex: 500ms)
Tolerating: T < response < 4T
Frustrated: response > 4T
```

## Patterns de Test

### Test de Capacité

```javascript
// Trouver la limite
export const options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '2m', target: 200 },
    { duration: '2m', target: 300 },
    { duration: '2m', target: 400 },
    { duration: '2m', target: 500 },
    // Continuer jusqu'à dégradation
  ],
  thresholds: {
    http_req_duration: ['p(99)<1000'],
  },
};
```

### Test de Soak (Endurance)

```javascript
// Tester la stabilité sur la durée
export const options = {
  stages: [
    { duration: '5m', target: 100 },   // Ramp up
    { duration: '4h', target: 100 },   // 4 heures à charge normale
    { duration: '5m', target: 0 },     // Ramp down
  ],
};
```

## Intégration CI

```yaml
# .github/workflows/load-test.yml
name: Load Test

on:
  schedule:
    - cron: '0 2 * * *'  # Chaque nuit
  workflow_dispatch:

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run k6 load test
        uses: grafana/k6-action@v0.3.1
        with:
          filename: tests/load/api.js
          flags: --out json=results.json

      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: k6-results
          path: results.json

      - name: Check thresholds
        run: |
          if grep -q '"thresholds":{"passed":false}' results.json; then
            echo "Performance thresholds failed!"
            exit 1
          fi
```

## Bonnes Pratiques

### DO

- Tester avec des données réalistes
- Monitorer les ressources serveur (CPU, RAM)
- Tester depuis plusieurs régions
- Documenter les baselines
- Automatiser les tests de régression

### DON'T

- Tester sur production sans précautions
- Ignorer les erreurs applicatives
- Utiliser des timeouts trop courts
- Oublier le warmup
- Comparer des environnements différents

## Analyse des Résultats

```
     ✓ status is 200
     ✓ response time < 500ms

     checks...............: 99.82% ✓ 19964 ✗ 36
     data_received........: 47 MB  157 kB/s
     data_sent............: 1.8 MB 6.0 kB/s
     http_req_blocked.....: avg=1.2ms  p(95)=3.5ms
     http_req_connecting..: avg=0.8ms  p(95)=2.1ms
     http_req_duration....: avg=127ms  p(95)=298ms  ← OK < 500ms
     http_req_failed......: 0.36%  ✓ 36   ✗ 9964
     http_req_receiving...: avg=0.3ms  p(95)=0.8ms
     http_req_sending.....: avg=0.1ms  p(95)=0.3ms
     http_req_waiting.....: avg=126ms  p(95)=297ms
     http_reqs............: 10000  33.33/s
     vus..................: 100    min=0   max=100
     vus_max..............: 100    min=100 max=100
```

## Livrables

| Livrable | Description |
|----------|-------------|
| Scripts k6/Artillery | Tests de charge automatisés |
| Baselines | Métriques de référence |
| Rapport | Analyse des résultats |
| CI workflow | Tests automatisés |
