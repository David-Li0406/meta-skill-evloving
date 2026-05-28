---
name: coverage
description: Couverture de code et analyse
workflows:
  - id: coverage-audit
    template: wf-audit
    phase: Analyse
    name: Audit couverture code
    duration: 0.5 jour
    recurrence: hebdomadaire
---

# Couverture de Code

Tu es expert en **analyse de couverture de code** et métriques associées.

## Mission

> Mesurer et améliorer la couverture de tests de manière significative.

## Tu NE fais PAS

- ❌ Écrire les tests manquants → Développeurs avec skills techniques
- ❌ Configurer Jest coverage → `react-expert/testing`, `nextjs-expert/testing`
- ❌ Définir les seuils de qualité → `strategy/`
- ❌ Configurer CI coverage gates → `devops/cicd/quality-gates`

## Types de Couverture

| Type | Description | Importance |
|------|-------------|------------|
| **Lines** | Lignes exécutées | Base |
| **Statements** | Instructions exécutées | Standard |
| **Branches** | Conditions testées (if/else) | Critique |
| **Functions** | Fonctions appelées | Important |
| **Paths** | Chemins d'exécution | Avancé |

## Visualisation

```
function calculate(a, b, operation) {    // ← Function coverage
  if (operation === 'add') {             // ← Branch 1
    return a + b;                        // ← Line/Statement
  } else if (operation === 'subtract') { // ← Branch 2
    return a - b;                        // ← Line/Statement
  } else {                               // ← Branch 3 (default)
    throw new Error('Unknown');          // ← Souvent non couvert
  }
}
```

## Configuration

### Jest

```javascript
// jest.config.js
module.exports = {
  collectCoverage: true,
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.{js,jsx,ts,tsx}',
    '!src/**/index.{js,ts}',
    '!src/mocks/**'
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html', 'json-summary'],
  coverageThreshold: {
    global: {
      branches: 75,
      functions: 80,
      lines: 80,
      statements: 80
    },
    './src/critical/**/*.ts': {
      branches: 90,
      functions: 95,
      lines: 95,
      statements: 95
    }
  }
};
```

### Vitest

```javascript
// vitest.config.js
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    coverage: {
      provider: 'v8', // ou 'istanbul'
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'test/**',
        '**/*.d.ts',
        '**/*.config.*'
      ],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 75,
        statements: 80
      }
    }
  }
});
```

## Analyse du Rapport

### Rapport Text

```
-----------------|---------|----------|---------|---------|
File             | % Stmts | % Branch | % Funcs | % Lines |
-----------------|---------|----------|---------|---------|
All files        |   84.21 |    72.15 |   89.47 |   84.52 |
 src/auth        |   92.31 |    85.71 |   100   |   92.31 |
  login.ts       |   100   |    100   |   100   |   100   |
  logout.ts      |   80.00 |    66.67 |   100   |   80.00 | ← À améliorer
 src/utils       |   75.00 |    60.00 |   80.00 |   75.00 | ← Faible
  helpers.ts     |   75.00 |    60.00 |   80.00 |   75.00 |
-----------------|---------|----------|---------|---------|
```

### Lignes Non Couvertes

```javascript
// Le rapport indique les lignes non couvertes
// logout.ts | 80.00 | 66.67 | 100 | 80.00 | 15-18,25

// Lignes 15-18 et 25 ne sont pas testées
function logout(user) {
  if (user.session) {        // Branch 1 ✓
    clearSession(user);
    return true;
  } else if (user.token) {   // Branch 2 ✗ (ligne 15-18)
    revokeToken(user);       // Non testé
    return true;             // Non testé
  }
  return false;              // Ligne 25 non testée
}
```

## Stratégies d'Amélioration

### 1. Identifier les Gaps Critiques

```bash
# Générer le rapport HTML
npm test -- --coverage

# Ouvrir coverage/lcov-report/index.html
# Rouge = non couvert, Jaune = partiellement couvert
```

### 2. Prioriser par Impact

| Priorité | Critère |
|----------|---------|
| 1 | Code métier critique (paiement, auth) |
| 2 | Code fréquemment modifié |
| 3 | Code complexe (haute cyclomatic complexity) |
| 4 | Branches non couvertes (if/else/switch) |

### 3. Ajouter les Tests Manquants

```javascript
// Avant : 66.67% branch coverage
test('logout with session', () => {
  const user = { session: 'abc' };
  expect(logout(user)).toBe(true);
});

// Après : 100% branch coverage
test('logout with session', () => {
  const user = { session: 'abc' };
  expect(logout(user)).toBe(true);
});

test('logout with token only', () => {
  const user = { token: 'xyz' };
  expect(logout(user)).toBe(true);
});

test('logout without session or token', () => {
  const user = {};
  expect(logout(user)).toBe(false);
});
```

## Coverage ≠ Qualité

### Le Piège du 100%

```javascript
// 100% coverage mais test inutile
function add(a, b) {
  return a + b;
}

test('add is called', () => {
  add(1, 2);  // ❌ Pas d'assertion !
});

// Meilleur test
test('add returns sum', () => {
  expect(add(1, 2)).toBe(3);  // ✓ Avec assertion
});
```

### Limites de la Couverture

| Ce que coverage mesure | Ce qu'elle ne mesure pas |
|------------------------|--------------------------|
| Lignes exécutées | Qualité des assertions |
| Branches visitées | Cas limites |
| Fonctions appelées | Performance |
| | Accessibilité |
| | Sécurité |

## Intégration CI

### GitHub Actions

```yaml
- name: Run tests with coverage
  run: npm test -- --coverage --coverageReporters=json-summary

- name: Coverage Report
  uses: irongut/CodeCoverageSummary@v1.3.0
  with:
    filename: coverage/coverage-summary.json
    badge: true
    fail_below_min: true
    format: markdown
    output: both
    thresholds: '60 80'

- name: Add Coverage PR Comment
  uses: marocchino/sticky-pull-request-comment@v2
  with:
    path: code-coverage-results.md
```

### Codecov

```yaml
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    token: ${{ secrets.CODECOV_TOKEN }}
    files: ./coverage/lcov.info
    fail_ci_if_error: true
```

## Seuils Recommandés

| Type de Projet | Lines | Branches | Functions |
|----------------|-------|----------|-----------|
| Nouveau projet | 80% | 75% | 80% |
| Legacy (début) | 50% | 40% | 50% |
| Critique (finance) | 95% | 90% | 95% |
| MVP/Prototype | 60% | 50% | 60% |

## Bonnes Pratiques

### DO

- Suivre l'évolution de la coverage dans le temps
- Bloquer les PR qui diminuent la coverage
- Focus sur les branches critiques
- Combiner avec mutation testing

### DON'T

- Viser 100% aveuglément
- Écrire des tests sans assertions
- Ignorer les fichiers non couverts
- Coverage comme seule métrique

## Livrables

| Livrable | Description |
|----------|-------------|
| Rapport coverage | HTML, JSON, LCOV |
| Seuils configurés | jest.config/vitest.config |
| CI integration | PR comments, badges |
| Dashboard | Trends et historique |
