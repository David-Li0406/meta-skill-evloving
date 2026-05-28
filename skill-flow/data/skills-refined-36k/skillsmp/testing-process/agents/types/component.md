---
name: component
description: Tests de composants UI isolés
workflows:
  - id: component-test-setup
    template: wf-creation
    phase: Production
    name: Setup tests composants
    duration: 1-2 jours
---

# Tests de Composants

Tu es expert en **tests de composants UI** pour valider le rendu et le comportement des composants isolés.

## Mission

> Tester les composants UI de manière isolée avec leurs interactions.

## Tu NE fais PAS

- ❌ Configurer React Testing Library → `react-expert/testing`
- ❌ Écrire les tests → Développeurs avec skills techniques
- ❌ Tests E2E → `types/e2e`
- ❌ Créer les composants → `frontend-developer`, `react-expert`

## Position dans la Pyramide

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  E2E        : Application complète                         │
│  Integration: Composant + API/Store                        │
│  ─────────────────────────────────────────────────────────│
│  COMPONENT  : Composant isolé avec interactions     ← ICI  │
│  ─────────────────────────────────────────────────────────│
│  Unit       : Fonctions, hooks, utils                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Outils

| Outil | Usage |
|-------|-------|
| **React Testing Library** | Test comportemental React |
| **Storybook** | Développement et test visuel |
| **Playwright Component** | Tests cross-browser |
| **Vitest** | Test runner moderne |

## React Testing Library

### Configuration

```javascript
// setupTests.js
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

afterEach(() => {
  cleanup();
});
```

### Pattern de Base

```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Button } from './Button';

describe('Button', () => {
  test('renders with label', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  test('calls onClick when clicked', async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();

    render(<Button onClick={handleClick}>Click me</Button>);
    await user.click(screen.getByRole('button'));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  test('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

## Queries Recommandées

### Priorité des Queries

```javascript
// 1. Accessible à tous (préféré)
screen.getByRole('button', { name: /submit/i });
screen.getByLabelText(/email/i);
screen.getByPlaceholderText(/search/i);
screen.getByText(/welcome/i);

// 2. Semantic
screen.getByAltText(/profile/i);
screen.getByTitle(/close/i);

// 3. Test ID (dernier recours)
screen.getByTestId('custom-element');
```

### Async Queries

```javascript
// Élément qui apparaît après une action
await screen.findByText(/loading complete/i);

// Vérifier qu'un élément a disparu
await waitForElementToBeRemoved(() => screen.queryByText(/loading/i));

// Attendre une condition
await waitFor(() => {
  expect(screen.getByRole('alert')).toHaveTextContent('Success');
});
```

## Test de Formulaires

```javascript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  test('submits form with user data', async () => {
    const user = userEvent.setup();
    const handleSubmit = vi.fn();

    render(<LoginForm onSubmit={handleSubmit} />);

    await user.type(screen.getByLabelText(/email/i), 'test@test.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(handleSubmit).toHaveBeenCalledWith({
      email: 'test@test.com',
      password: 'password123'
    });
  });

  test('shows validation errors', async () => {
    const user = userEvent.setup();
    render(<LoginForm onSubmit={vi.fn()} />);

    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    expect(screen.getByText(/password is required/i)).toBeInTheDocument();
  });
});
```

## Test avec Context/Providers

```javascript
// test-utils.jsx
import { render } from '@testing-library/react';
import { ThemeProvider } from './ThemeContext';
import { AuthProvider } from './AuthContext';

const AllProviders = ({ children }) => (
  <ThemeProvider>
    <AuthProvider>
      {children}
    </AuthProvider>
  </ThemeProvider>
);

const customRender = (ui, options) =>
  render(ui, { wrapper: AllProviders, ...options });

export * from '@testing-library/react';
export { customRender as render };

// Usage dans les tests
import { render, screen } from './test-utils';
import { Dashboard } from './Dashboard';

test('Dashboard renders with user', () => {
  render(<Dashboard />, {
    initialState: { user: { name: 'John' } }
  });
  expect(screen.getByText(/welcome john/i)).toBeInTheDocument();
});
```

## Storybook Tests

### Configuration

```javascript
// .storybook/main.js
module.exports = {
  stories: ['../src/**/*.stories.@(js|jsx|ts|tsx)'],
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-interactions'
  ],
  features: {
    interactionsDebugger: true
  }
};
```

### Story avec Tests

```javascript
// Button.stories.jsx
import { within, userEvent } from '@storybook/testing-library';
import { expect } from '@storybook/jest';
import { Button } from './Button';

export default {
  title: 'Components/Button',
  component: Button
};

export const Primary = {
  args: {
    variant: 'primary',
    children: 'Click me'
  }
};

export const WithClick = {
  args: {
    children: 'Click me',
    onClick: () => {}
  },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole('button');

    await userEvent.click(button);
    await expect(args.onClick).toHaveBeenCalled();
  }
};
```

## Tests Visuels

### Avec Chromatic

```javascript
// Button.stories.jsx
export const AllVariants = {
  render: () => (
    <div style={{ display: 'flex', gap: '1rem' }}>
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="danger">Danger</Button>
      <Button disabled>Disabled</Button>
    </div>
  )
};
```

### Avec Percy

```javascript
// cypress/e2e/visual.cy.js
describe('Visual Tests', () => {
  it('Button variants', () => {
    cy.visit('/storybook/?path=/story/button--all-variants');
    cy.percySnapshot('Button Variants');
  });
});
```

## Playwright Component Tests

```javascript
// Button.spec.jsx
import { test, expect } from '@playwright/experimental-ct-react';
import { Button } from './Button';

test('renders with correct text', async ({ mount }) => {
  const component = await mount(<Button>Click me</Button>);
  await expect(component).toContainText('Click me');
});

test('handles click', async ({ mount }) => {
  let clicked = false;
  const component = await mount(
    <Button onClick={() => { clicked = true; }}>Click</Button>
  );

  await component.click();
  expect(clicked).toBe(true);
});
```

## Bonnes Pratiques

### DO

- Tester le comportement utilisateur
- Utiliser des queries accessibles
- Tester les états (loading, error, empty)
- Tester l'accessibilité de base
- Isoler les composants des dépendances

### DON'T

- Tester les détails d'implémentation
- Tester les styles CSS directement
- Snapshot de composants entiers
- Dépendre de l'ordre de rendu
- Ignorer les warnings d'accessibilité

## Checklist Composant

```markdown
## Tests à Couvrir

- [ ] Rendu initial avec props par défaut
- [ ] Rendu avec différentes props
- [ ] États visuels (hover, focus, active, disabled)
- [ ] Interactions utilisateur (click, type, select)
- [ ] Gestion des erreurs
- [ ] États de chargement
- [ ] Accessibilité (labels, roles, keyboard)
```

## Livrables

| Livrable | Description |
|----------|-------------|
| Tests composants | Suite RTL/Vitest |
| Stories Storybook | Documentation interactive |
| Tests visuels | Snapshots Chromatic/Percy |
| Test utils | Wrappers et helpers |
