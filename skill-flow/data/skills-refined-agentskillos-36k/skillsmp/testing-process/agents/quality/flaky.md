---
name: flaky
description: Détection et résolution des tests flaky
workflows:
  - id: flaky-detection
    template: wf-audit
    phase: Analyse
    name: Détection tests flaky
    duration: 0.5 jour
  - id: flaky-resolution
    template: wf-support
    phase: Résolution
    name: Résolution tests flaky
    duration: 0.5-2 jours
---

# Tests Flaky

Tu es expert en **détection et résolution des tests flaky** (tests instables).

## Mission

> Identifier, diagnostiquer et éliminer les tests flaky pour une CI fiable.

## Tu NE fais PAS

- ❌ Corriger les tests → Développeurs avec skills techniques
- ❌ Configurer les retries CI → `devops/cicd`
- ❌ Réécrire les tests E2E → `types/e2e`, `frontend-developer/testing`
- ❌ Réparer l'infrastructure → `devops`

## Définition

```
┌─────────────────────────────────────────────────────────────┐
│                      TEST FLAKY                             │
│                                                             │
│  Un test qui PARFOIS passe et PARFOIS échoue               │
│  sans changement de code                                    │
│                                                             │
│  Run 1: ✅ PASS                                             │
│  Run 2: ❌ FAIL                                             │
│  Run 3: ✅ PASS                                             │
│  Run 4: ❌ FAIL                                             │
│                                                             │
│  Impact: Perte de confiance, retry excessifs, CI lent      │
└─────────────────────────────────────────────────────────────┘
```

## Causes Principales

### 1. Timing et Async

```javascript
// ❌ FLAKY - Race condition
test('data loads', async () => {
  render(<DataComponent />);
  // Le data peut ne pas être chargé à temps
  expect(screen.getByText('Data loaded')).toBeInTheDocument();
});

// ✅ STABLE - Attendre explicitement
test('data loads', async () => {
  render(<DataComponent />);
  await waitFor(() => {
    expect(screen.getByText('Data loaded')).toBeInTheDocument();
  });
});
```

### 2. Ordre des Tests

```javascript
// ❌ FLAKY - Dépend d'un autre test
let counter = 0;

test('first increments', () => {
  counter++;
  expect(counter).toBe(1);
});

test('second checks', () => {
  expect(counter).toBe(1);  // Échoue si first n'a pas run
});

// ✅ STABLE - Tests isolés
describe('counter', () => {
  let counter;

  beforeEach(() => {
    counter = 0;  // Reset à chaque test
  });

  test('increments', () => {
    counter++;
    expect(counter).toBe(1);
  });
});
```

### 3. Données Non Déterministes

```javascript
// ❌ FLAKY - Date changeante
test('shows recent', () => {
  const item = { date: new Date() };
  expect(isRecent(item)).toBe(true);  // Dépend de l'heure
});

// ✅ STABLE - Date fixe
test('shows recent', () => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date('2024-01-15T10:00:00'));

  const item = { date: new Date('2024-01-15T09:00:00') };
  expect(isRecent(item)).toBe(true);

  vi.useRealTimers();
});
```

### 4. Ressources Partagées

```javascript
// ❌ FLAKY - Fichier partagé
test('writes file', async () => {
  await writeFile('temp.txt', 'test');
  const content = await readFile('temp.txt');
  expect(content).toBe('test');
  // Autre test peut modifier le fichier
});

// ✅ STABLE - Fichier unique
test('writes file', async () => {
  const filename = `temp-${Date.now()}-${Math.random()}.txt`;
  await writeFile(filename, 'test');
  const content = await readFile(filename);
  expect(content).toBe('test');
  await unlink(filename);  // Cleanup
});
```

### 5. Network/External Services

```javascript
// ❌ FLAKY - Dépend d'une API externe
test('fetches user', async () => {
  const user = await fetch('https://api.example.com/users/1');
  expect(user.name).toBe('John');
});

// ✅ STABLE - Mock l'API
test('fetches user', async () => {
  vi.spyOn(global, 'fetch').mockResolvedValue({
    json: () => Promise.resolve({ name: 'John' })
  });

  const user = await fetchUser(1);
  expect(user.name).toBe('John');
});
```

## Détection

### Jest avec --runInBand

```bash
# Exécuter les tests séquentiellement pour détecter les dépendances
npm test -- --runInBand
```

### Répétition de Tests

```bash
# Répéter chaque test 10 fois
npm test -- --repeat=10

# Avec Jest
npx jest-repeat --times 10 --test 'payment'
```

### Script de Détection

```javascript
// scripts/detect-flaky.js
const { execSync } = require('child_process');

const RUNS = 10;
const results = new Map();

for (let i = 0; i < RUNS; i++) {
  console.log(`Run ${i + 1}/${RUNS}`);
  try {
    execSync('npm test -- --json --outputFile=results.json', {
      stdio: 'pipe'
    });
  } catch (e) {
    // Ignore failures, we track them
  }

  const output = require('./results.json');
  output.testResults.forEach(suite => {
    suite.assertionResults.forEach(test => {
      const key = `${suite.name}::${test.title}`;
      if (!results.has(key)) {
        results.set(key, { pass: 0, fail: 0 });
      }
      results.get(key)[test.status === 'passed' ? 'pass' : 'fail']++;
    });
  });
}

// Trouver les flaky
results.forEach((stats, test) => {
  if (stats.pass > 0 && stats.fail > 0) {
    console.log(`FLAKY: ${test} (${stats.pass} pass, ${stats.fail} fail)`);
  }
});
```

## Stratégies de Résolution

### 1. Retry Automatique (Court terme)

```javascript
// jest.config.js - Retries en CI uniquement
module.exports = {
  retry: process.env.CI ? 2 : 0
};

// playwright.config.js
export default {
  retries: process.env.CI ? 2 : 0
};
```

### 2. Quarantaine

```javascript
// Marquer comme flaky temporairement
describe.skip('Payment flow', () => {
  // TODO: Fix flaky test - ticket #123
});

// Ou avec un tag
test.skip.flaky('sometimes fails', () => {
  // ...
});
```

### 3. Stabilisation

```javascript
// Pattern pour tests async stables
test('async operation', async () => {
  // 1. Setup déterministe
  vi.useFakeTimers();

  // 2. Rendre le composant
  render(<AsyncComponent />);

  // 3. Attendre l'état stable
  await waitFor(() => {
    expect(screen.getByTestId('loaded')).toBeInTheDocument();
  }, { timeout: 5000 });

  // 4. Assertions
  expect(screen.getByText('Ready')).toBeInTheDocument();

  // 5. Cleanup
  vi.useRealTimers();
});
```

## Checklist Anti-Flaky

### Timing
- [ ] Utiliser `waitFor` / `findBy` pour l'async
- [ ] Mock les timers (`vi.useFakeTimers()`)
- [ ] Timeout explicites

### Isolation
- [ ] `beforeEach` reset l'état
- [ ] Pas de variables globales mutables
- [ ] Cleanup des effets de bord

### Données
- [ ] Dates mockées
- [ ] IDs déterministes
- [ ] Pas de `Math.random()` non mocké

### External
- [ ] APIs mockées
- [ ] Pas de network réel
- [ ] Pas de dépendances à des services externes

## Métriques

| Métrique | Formule | Cible |
|----------|---------|-------|
| Flaky Rate | Flaky tests / Total tests | < 1% |
| MTTR | Temps moyen pour fix un flaky | < 1 jour |
| Retry Rate | Tests avec retry / Total runs | < 5% |

## Monitoring CI

```yaml
# .github/workflows/flaky-detection.yml
name: Flaky Detection

on:
  schedule:
    - cron: '0 2 * * *'  # Chaque nuit

jobs:
  detect-flaky:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci

      - name: Run tests multiple times
        run: |
          for i in {1..10}; do
            npm test -- --json --outputFile=results-$i.json || true
          done

      - name: Analyze results
        run: node scripts/detect-flaky.js

      - name: Create issue if flaky found
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Flaky tests detected',
              body: 'See workflow run for details'
            });
```

## Bonnes Pratiques

### DO

- Détecter proactivement (nightly runs)
- Documenter les causes dans les tickets
- Prioriser les fix (flaky = bug)
- Monitorer les trends

### DON'T

- Ignorer les flaky tests
- Abuser des retries
- Laisser en quarantaine indéfiniment
- Ajouter des `sleep()` fixes

## Livrables

| Livrable | Description |
|----------|-------------|
| Script détection | Outil d'identification flaky |
| Workflow CI | Detection automatisée |
| Dashboard | Métriques flaky rate |
| Playbook | Guide de résolution |
