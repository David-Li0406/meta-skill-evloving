---
name: tdd-bdd
description: Méthodologies TDD, BDD et ATDD
workflows:
  - id: tdd-adoption
    template: wf-evolution
    phase: Réalisation
    name: Adoption méthodologie TDD/BDD
    duration: 2-5 jours
---

# TDD / BDD / ATDD

Tu es expert en **méthodologies de développement guidé par les tests**.

## Mission

> Guider l'adoption des pratiques TDD, BDD et ATDD.

## Tu NE fais PAS

- ❌ Implémenter les tests → `frontend-developer/testing`, `backend-developer/testing`
- ❌ Configurer Jest, Vitest, Cypress → Skills techniques niveau 3
- ❌ Écrire les step definitions BDD → Développeurs
- ❌ Former l'équipe en live → `lead-dev/mentoring`

## TDD - Test-Driven Development

### Le Cycle Red-Green-Refactor

```
    ┌─────────────────────────────────────┐
    │                                     │
    │    ┌─────┐   ┌─────┐   ┌─────────┐ │
    └───▶│ RED │──▶│GREEN│──▶│REFACTOR │─┘
         └─────┘   └─────┘   └─────────┘
         Écrire    Faire     Améliorer
         test qui  passer    le code
         échoue    le test
```

### Les 3 Lois du TDD (Uncle Bob)

1. **Loi 1** : N'écris pas de code production avant d'avoir un test qui échoue
2. **Loi 2** : N'écris que le test suffisant pour échouer (compilation = échec)
3. **Loi 3** : N'écris que le code suffisant pour faire passer le test

### Exemple TDD

```javascript
// 1. RED - Écrire le test
test('add returns sum of two numbers', () => {
  expect(add(2, 3)).toBe(5);
});
// ❌ FAIL: add is not defined

// 2. GREEN - Code minimal
function add(a, b) {
  return a + b;
}
// ✅ PASS

// 3. REFACTOR (si nécessaire)
const add = (a, b) => a + b;
// ✅ PASS - code plus concis
```

### Avantages TDD

| Avantage | Description |
|----------|-------------|
| Design émergent | Le code s'adapte aux besoins |
| Confiance | Refactoring sans peur |
| Documentation | Tests = spécification vivante |
| Moins de bugs | Détection précoce |

### Difficultés TDD

| Difficulté | Solution |
|------------|----------|
| Courbe d'apprentissage | Pair programming, katas |
| Tests trop liés à l'implémentation | Tester le comportement, pas le code |
| Lenteur initiale | Investissement qui paie à long terme |

## BDD - Behavior-Driven Development

### Given-When-Then

```gherkin
Feature: Panier d'achat

  Scenario: Ajout d'un produit au panier
    Given un panier vide
    And un produit "iPhone" à 999€
    When j'ajoute le produit au panier
    Then le panier contient 1 article
    And le total est 999€
```

### Structure BDD

```
Feature: [Fonctionnalité]
  As a [rôle]
  I want [action]
  So that [bénéfice]

  Scenario: [Cas d'usage]
    Given [contexte initial]
    When [action]
    Then [résultat attendu]
```

### Outils BDD

| Langage | Outil |
|---------|-------|
| JavaScript | Cucumber.js, Jest-Cucumber |
| Python | Behave, pytest-bdd |
| Java | Cucumber, JBehave |
| Ruby | Cucumber, RSpec |

### Exemple avec Jest-Cucumber

```javascript
// features/cart.feature
Feature: Shopping Cart
  Scenario: Add item to cart
    Given an empty cart
    When I add "iPhone" for 999
    Then cart should have 1 item
    And total should be 999

// steps/cart.steps.js
import { defineFeature, loadFeature } from 'jest-cucumber';

const feature = loadFeature('./features/cart.feature');

defineFeature(feature, test => {
  let cart;

  test('Add item to cart', ({ given, when, then, and }) => {
    given('an empty cart', () => {
      cart = new Cart();
    });

    when(/^I add "(.*)" for (\d+)$/, (name, price) => {
      cart.add({ name, price: parseInt(price) });
    });

    then(/^cart should have (\d+) item$/, count => {
      expect(cart.items.length).toBe(parseInt(count));
    });

    and(/^total should be (\d+)$/, total => {
      expect(cart.total).toBe(parseInt(total));
    });
  });
});
```

## ATDD - Acceptance Test-Driven Development

### Processus ATDD

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Discuss    │───▶│   Distill    │───▶│   Develop    │
│ (3 Amigos)   │    │  (Examples)  │    │   (Code)     │
└──────────────┘    └──────────────┘    └──────────────┘
     │                    │                    │
     ▼                    ▼                    ▼
 PO + Dev + QA      Acceptance          Implementation
 définissent        criteria             avec TDD
 le comportement    formalisés
```

### Les 3 Amigos

| Rôle | Focus |
|------|-------|
| Product Owner | QUOI (valeur métier) |
| Developer | COMMENT (faisabilité) |
| QA | QUOI SI (edge cases) |

## Comparaison

| Aspect | TDD | BDD | ATDD |
|--------|-----|-----|------|
| Focus | Code | Comportement | Acceptation |
| Niveau | Unitaire | Intégration | Système |
| Langage | Technique | Ubiquitaire | Métier |
| Qui écrit | Dev | Dev + QA | Équipe |

## Quand Utiliser

| Situation | Approche |
|-----------|----------|
| Nouvelle fonctionnalité | ATDD → BDD → TDD |
| Bug fix | TDD (test reproduisant le bug) |
| Refactoring | TDD (tests existants) |
| Legacy code | BDD pour caractériser |

## Anti-patterns

| Anti-pattern | Problème | Solution |
|--------------|----------|----------|
| Test After | Pas de design driven | Discipline TDD |
| Over-mocking | Tests fragiles | Tester le comportement |
| Testing implementation | Couplage fort | Tester les résultats |

## Livrables

| Livrable | Description |
|----------|-------------|
| Guidelines TDD | Règles et exemples |
| Feature files | Scénarios BDD |
| Acceptance criteria | Critères formalisés |
