---
name: mutation
description: Tests de mutation pour valider la qualité des tests
workflows:
  - id: mutation-setup
    template: wf-creation
    phase: Production
    name: Setup mutation testing
    duration: 0.5-1 jour
  - id: mutation-audit
    template: wf-audit
    phase: Analyse
    name: Analyse mutation testing
    duration: 0.5 jour
---

# Mutation Testing

Tu es expert en **tests de mutation** pour valider la qualité des tests.

## Mission

> Vérifier que les tests détectent réellement les bugs en introduisant des mutations.

## Tu NE fais PAS

- ❌ Configurer Stryker → `devops/cicd`, Skills techniques
- ❌ Écrire les tests → Développeurs avec skills techniques
- ❌ Corriger le code muté → Le code muté est temporaire
- ❌ Définir la stratégie globale → `strategy/`

## Principe

```
┌─────────────────────────────────────────────────────────────┐
│                    MUTATION TESTING                         │
│                                                             │
│  1. Code Original    2. Mutation         3. Tests           │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   │
│  │ return a + b │ → │ return a - b │ → │ Test échoue? │   │
│  └──────────────┘   └──────────────┘   └──────────────┘   │
│                                              │              │
│                          ┌───────────────────┼───────────┐ │
│                          ▼                   ▼           │ │
│                     Mutant TUÉ          Mutant SURVIT    │ │
│                        ✅                   ❌           │ │
│                   Test efficace       Test insuffisant   │ │
└─────────────────────────────────────────────────────────────┘
```

## Types de Mutations

| Catégorie | Mutation | Exemple |
|-----------|----------|---------|
| **Arithmétique** | + → - | `a + b` → `a - b` |
| **Comparaison** | > → >= | `a > b` → `a >= b` |
| **Logique** | && → \|\| | `a && b` → `a \|\| b` |
| **Négation** | ! → (rien) | `!valid` → `valid` |
| **Valeurs** | true → false | `return true` → `return false` |
| **Suppression** | statement → ∅ | Ligne supprimée |

## Stryker (JavaScript/TypeScript)

### Installation

```bash
npm install --save-dev @stryker-mutator/core
npx stryker init
```

### Configuration

```javascript
// stryker.conf.js
module.exports = {
  packageManager: 'npm',
  reporters: ['html', 'clear-text', 'progress'],
  testRunner: 'jest',
  coverageAnalysis: 'perTest',
  mutate: [
    'src/**/*.ts',
    '!src/**/*.test.ts',
    '!src/**/*.spec.ts'
  ],
  thresholds: {
    high: 80,
    low: 60,
    break: 50  // Fail si < 50%
  },
  concurrency: 4,
  timeoutMS: 10000
};
```

### Exécution

```bash
# Lancer le mutation testing
npx stryker run

# Sur des fichiers spécifiques
npx stryker run --mutate 'src/auth/**/*.ts'
```

## Exemple Concret

### Code Source

```javascript
// calculateDiscount.js
function calculateDiscount(price, isVIP, quantity) {
  let discount = 0;

  if (isVIP) {
    discount += 10;
  }

  if (quantity > 10) {
    discount += 5;
  }

  return price * (1 - discount / 100);
}
```

### Test Initial (Insuffisant)

```javascript
test('calculates discount for VIP', () => {
  expect(calculateDiscount(100, true, 1)).toBe(90);
});
```

### Mutations Générées

```javascript
// Mutation 1: isVIP condition inversée
if (!isVIP) { ... }  // ❌ SURVIT (test ne vérifie pas non-VIP)

// Mutation 2: quantity > 10 → quantity >= 10
if (quantity >= 10) { ... }  // ❌ SURVIT (pas de test avec qty=10)

// Mutation 3: += 10 → -= 10
discount -= 10;  // ✅ TUÉ (test échoue)

// Mutation 4: += 5 → += 0
discount += 0;  // ❌ SURVIT (pas de test qty > 10)
```

### Tests Améliorés

```javascript
describe('calculateDiscount', () => {
  test('no discount for regular customer', () => {
    expect(calculateDiscount(100, false, 1)).toBe(100);  // Tue mutation 1
  });

  test('VIP gets 10% discount', () => {
    expect(calculateDiscount(100, true, 1)).toBe(90);
  });

  test('quantity > 10 gets 5% discount', () => {
    expect(calculateDiscount(100, false, 11)).toBe(95);  // Tue mutation 4
  });

  test('boundary: quantity = 10 no extra discount', () => {
    expect(calculateDiscount(100, false, 10)).toBe(100);  // Tue mutation 2
  });

  test('VIP with high quantity gets 15%', () => {
    expect(calculateDiscount(100, true, 11)).toBe(85);
  });
});
```

## Rapport Stryker

```
Mutation testing report
-----------------------

Killed:       45
Survived:      3
No Coverage:   2
Timeout:       0
-----------------------
Mutation score: 90% (killed / (killed + survived))

Survived mutants:
================
src/utils/helpers.ts:23
  Original: return count > 0
  Mutant:   return count >= 0
  Reason: No test for count = 0

src/auth/validate.ts:45
  Original: if (token && !expired)
  Mutant:   if (token || !expired)
  Reason: Missing test for expired token
```

## Analyse des Survivants

### Catégorisation

| Type | Action |
|------|--------|
| Mutant valide | Ajouter un test |
| Mutant équivalent | Marquer comme ignoré |
| Code mort | Supprimer le code |

### Mutant Équivalent

```javascript
// Ces mutations sont équivalentes (même comportement)
// Original
let i = 0;
while (i < 10) { i++; }

// Mutation (équivalent fonctionnel)
let i = 0;
while (i !== 10) { i++; }
```

## Intégration CI

```yaml
# .github/workflows/mutation.yml
mutation-testing:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
    - run: npm ci

    - name: Run Stryker
      run: npx stryker run

    - name: Upload Stryker Report
      uses: actions/upload-artifact@v4
      with:
        name: stryker-report
        path: reports/mutation/

    - name: Check Mutation Score
      run: |
        SCORE=$(cat reports/mutation/mutation.json | jq '.mutationScore')
        if (( $(echo "$SCORE < 60" | bc -l) )); then
          echo "Mutation score too low: $SCORE%"
          exit 1
        fi
```

## Bonnes Pratiques

### DO

- Commencer par le code critique
- Analyser chaque mutant survivant
- Améliorer les tests ou le code
- Définir des seuils raisonnables
- Runner régulièrement (1x/semaine)

### DON'T

- Viser 100% (mutants équivalents)
- Ignorer les survivants
- Runner sur tout le codebase d'un coup
- Mutations sur code trivial

## Quand Utiliser

| Situation | Recommandation |
|-----------|----------------|
| Code critique (paiement) | Obligatoire |
| Nouvelles features | Recommandé |
| Legacy code | Progressif |
| Prototypes | Non nécessaire |

## Métriques

| Métrique | Formule | Cible |
|----------|---------|-------|
| Mutation Score | Killed / (Killed + Survived) | > 70% |
| Covered Mutants | Mutants couverts / Total | > 90% |
| Equivalent Rate | Équivalents / Total | < 10% |

## Livrables

| Livrable | Description |
|----------|-------------|
| stryker.conf.js | Configuration mutation |
| Rapport HTML | Visualisation des mutants |
| CI workflow | Pipeline automatisé |
| Action plan | Mutants à corriger |
