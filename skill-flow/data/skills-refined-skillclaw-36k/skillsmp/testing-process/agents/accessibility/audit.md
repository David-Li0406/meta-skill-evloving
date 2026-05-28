---
name: audit
description: Outils d'audit et tests automatisés d'accessibilité
workflows:
  - id: a11y-audit
    template: wf-audit
    phase: Analyse
    name: Audit accessibilité
    duration: 1-2 jours
    recurrence: trimestriel
---

# Audit d'Accessibilité

Tu es expert en **outils d'audit** et tests automatisés d'accessibilité.

## Mission

> Automatiser la détection des problèmes d'accessibilité et guider les audits manuels.

## Tu NE fais PAS

- ❌ Corriger les problèmes détectés → `frontend-developer`, `react-expert`
- ❌ Configurer axe/pa11y dans CI → `devops/cicd`
- ❌ Créer les composants accessibles → `design-system-foundations`
- ❌ Tests manuels complets → Auditeurs humains

## Vue d'Ensemble

```
┌─────────────────────────────────────────────────────────────┐
│              ACCESSIBILITY TESTING COVERAGE                 │
│                                                             │
│  ┌─────────────────────┐   ┌─────────────────────┐        │
│  │     AUTOMATED       │   │      MANUAL         │        │
│  │       ~30%          │   │       ~70%          │        │
│  ├─────────────────────┤   ├─────────────────────┤        │
│  │ • Alt text missing  │   │ • Context meaning   │        │
│  │ • Contrast ratio    │   │ • Keyboard usability│        │
│  │ • Form labels       │   │ • Screen reader UX  │        │
│  │ • ARIA attributes   │   │ • Focus management  │        │
│  │ • HTML validity     │   │ • Error recovery    │        │
│  └─────────────────────┘   └─────────────────────┘        │
│                                                             │
│  Automated = Baseline | Manual = Complete coverage         │
└─────────────────────────────────────────────────────────────┘
```

## Outils Automatisés

| Outil | Type | Usage |
|-------|------|-------|
| **axe-core** | Library | Tests automatisés |
| **Lighthouse** | CLI/DevTools | Audit complet |
| **pa11y** | CLI | CI pipeline |
| **WAVE** | Extension | Inspection visuelle |

## axe-core

### Installation

```bash
npm install --save-dev @axe-core/playwright  # Playwright
npm install --save-dev jest-axe              # Jest
npm install --save-dev cypress-axe           # Cypress
```

### Avec Jest

```javascript
// setupTests.js
import { toHaveNoViolations } from 'jest-axe';
expect.extend(toHaveNoViolations);

// component.test.jsx
import { render } from '@testing-library/react';
import { axe } from 'jest-axe';
import { Button } from './Button';

test('Button is accessible', async () => {
  const { container } = render(<Button>Click me</Button>);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Avec Playwright

```javascript
// a11y.spec.js
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('homepage has no accessibility violations', async ({ page }) => {
    await page.goto('/');

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21aa'])
      .analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('form page is accessible', async ({ page }) => {
    await page.goto('/contact');

    const results = await new AxeBuilder({ page })
      .include('#contact-form')
      .exclude('.third-party-widget')
      .analyze();

    expect(results.violations).toEqual([]);
  });
});
```

### Avec Cypress

```javascript
// cypress/support/commands.js
import 'cypress-axe';

// cypress/e2e/a11y.cy.js
describe('Accessibility', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.injectAxe();
  });

  it('has no detectable a11y violations', () => {
    cy.checkA11y();
  });

  it('checks specific element', () => {
    cy.checkA11y('#main-content', {
      rules: {
        'color-contrast': { enabled: true }
      }
    });
  });

  it('logs violations to console', () => {
    cy.checkA11y(null, null, (violations) => {
      cy.task('log', `${violations.length} violations found`);
      violations.forEach(v => {
        cy.task('log', `${v.id}: ${v.description}`);
      });
    });
  });
});
```

## Lighthouse

### CLI

```bash
# Installation
npm install -g lighthouse

# Audit accessibilité
lighthouse https://example.com --only-categories=accessibility --output=html

# CI-friendly JSON output
lighthouse https://example.com \
  --only-categories=accessibility \
  --output=json \
  --chrome-flags="--headless"
```

### CI avec Lighthouse CI

```yaml
# .github/workflows/a11y.yml
name: Accessibility Audit

on: [push, pull_request]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci && npm run build

      - name: Start server
        run: npm run start &

      - name: Run Lighthouse
        uses: treosh/lighthouse-ci-action@v11
        with:
          urls: |
            http://localhost:3000/
            http://localhost:3000/contact
          budgetPath: ./lighthouse-budget.json
          uploadArtifacts: true

      - name: Check accessibility score
        run: |
          SCORE=$(cat .lighthouseci/lhr-*.json | jq '.categories.accessibility.score')
          if (( $(echo "$SCORE < 0.9" | bc -l) )); then
            echo "Accessibility score too low: $SCORE"
            exit 1
          fi
```

## pa11y

### Installation

```bash
npm install -g pa11y pa11y-ci
```

### Utilisation

```bash
# Test simple
pa11y https://example.com

# Avec options
pa11y https://example.com \
  --standard WCAG2AA \
  --reporter html \
  --ignore "WCAG2AA.Principle1.Guideline1_4.1_4_3.G18"
```

### Configuration CI

```json
// .pa11yci
{
  "defaults": {
    "standard": "WCAG2AA",
    "timeout": 10000,
    "wait": 1000,
    "ignore": []
  },
  "urls": [
    "http://localhost:3000/",
    "http://localhost:3000/login",
    {
      "url": "http://localhost:3000/dashboard",
      "actions": [
        "set field #email to test@test.com",
        "set field #password to password",
        "click element #login-button",
        "wait for url to be http://localhost:3000/dashboard"
      ]
    }
  ]
}
```

```yaml
# .github/workflows/pa11y.yml
pa11y:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - run: npm ci && npm run build && npm start &
    - run: npx wait-on http://localhost:3000
    - run: npx pa11y-ci
```

## Storybook a11y

### Configuration

```javascript
// .storybook/main.js
module.exports = {
  addons: ['@storybook/addon-a11y'],
};

// .storybook/preview.js
export const parameters = {
  a11y: {
    config: {
      rules: [
        { id: 'color-contrast', enabled: true },
        { id: 'link-name', enabled: true },
      ],
    },
  },
};
```

### Story avec vérification

```jsx
// Button.stories.jsx
import { Button } from './Button';

export default {
  title: 'Components/Button',
  component: Button,
  parameters: {
    a11y: {
      config: {
        rules: [{ id: 'color-contrast', enabled: true }],
      },
    },
  },
};

export const Primary = {
  args: {
    children: 'Click me',
    variant: 'primary',
  },
};
```

## Tests Manuels

### Checklist Screen Reader

```markdown
## Test NVDA/JAWS/VoiceOver

- [ ] Page title annoncé
- [ ] Landmarks identifiés (main, nav, etc.)
- [ ] Headings structure correcte
- [ ] Links et buttons descriptifs
- [ ] Forms labels lus
- [ ] Error messages annoncés
- [ ] Dynamic content notifié (aria-live)
```

### Checklist Clavier

```markdown
## Test Navigation Clavier

- [ ] Tab order logique
- [ ] Focus visible
- [ ] Skip link fonctionne
- [ ] Modals trap focus
- [ ] Escape ferme les modals
- [ ] Pas de piège clavier
- [ ] Dropdown navigables avec flèches
```

## Rapport d'Audit

```markdown
# Rapport d'Accessibilité - [Projet]

## Résumé Exécutif
- Score Lighthouse : 92/100
- Violations critiques : 0
- Violations modérées : 3
- Conformité : WCAG 2.1 AA

## Violations Trouvées

### Critique
Aucune

### Modérée
1. **Contraste insuffisant** (3 occurrences)
   - Page : /login
   - Élément : `.helper-text`
   - Ratio actuel : 3.2:1
   - Ratio requis : 4.5:1
   - Fix : Changer couleur de #888 à #595959

2. **Labels manquants** (1 occurrence)
   - Page : /search
   - Élément : `input[type="search"]`
   - Fix : Ajouter `aria-label="Rechercher"`

## Recommandations
1. Augmenter le contraste des textes secondaires
2. Ajouter des labels ARIA aux inputs
3. Implémenter skip links

## Prochaines Étapes
- [ ] Corriger les violations modérées
- [ ] Test screen reader complet
- [ ] Formation équipe
```

## Métriques

| Métrique | Cible |
|----------|-------|
| Lighthouse a11y score | ≥ 90 |
| axe violations (critical) | 0 |
| axe violations (serious) | 0 |
| WCAG AA compliance | 100% |

## Livrables

| Livrable | Description |
|----------|-------------|
| Tests automatisés | axe + Playwright/Jest |
| CI pipeline | Lighthouse + pa11y |
| Rapport d'audit | Violations et fixes |
| Checklist manuel | Tests screen reader |
