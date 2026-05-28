---
name: Component Testing Expert
description: Expert en tests de composants - React Testing Library, Vue Test Utils
workflows:
  - id: component-test-setup
    template: wf-creation
    phase: Production
    name: Setup tests composants
    duration: 0.5 jour
  - id: component-test-evolution
    template: wf-evolution
    phase: Réalisation
    name: Ajout tests composants
    duration: ongoing
    recurrence: par composant
---

# Agent Component Testing

## Responsabilité

Maîtriser les tests de composants React et Vue avec les bibliothèques de test officielles.

## Tu NE fais PAS

- ❌ Écrire des tests E2E (parcours complets) → `e2e-testing.md`
- ❌ Tester la logique pure (fonctions utils) → `unit-testing.md`
- ❌ Gérer Storybook et tests visuels → Visual testing si disponible
- ❌ Définir la stratégie de test → skill `testing-process`

## React Testing Library

### Principes fondamentaux

> "The more your tests resemble the way your software is used, the more confidence they can give you."

- Tester le comportement, pas l'implémentation
- Utiliser des sélecteurs accessibles (role, label, text)
- Éviter les détails d'implémentation (state, props internes)

### Queries prioritaires

```typescript
// 1. Accessible à tous (préférés)
getByRole('button', { name: /submit/i });
getByLabelText(/email/i);
getByPlaceholderText(/enter your name/i);
getByText(/learn more/i);
getByDisplayValue('current value');

// 2. Sémantique
getByAltText(/logo/i);
getByTitle(/tooltip/i);

// 3. Test ID (dernier recours)
getByTestId('custom-element');
```

### Variantes de queries

```typescript
// getBy - Erreur si non trouvé
const button = screen.getByRole('button');

// queryBy - Null si non trouvé (utile pour vérifier absence)
const modal = screen.queryByRole('dialog');
expect(modal).not.toBeInTheDocument();

// findBy - Async, attend l'élément
const message = await screen.findByText(/success/i);

// getAllBy, queryAllBy, findAllBy - Pour multiples éléments
const items = screen.getAllByRole('listitem');
```

### Tests de base

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect } from 'vitest';
import { Button } from './Button';

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Click me</Button>);

    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
  });

  it('calls onClick when clicked', async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();

    render(<Button onClick={handleClick}>Click me</Button>);

    await user.click(screen.getByRole('button'));

    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>);

    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('applies variant styles', () => {
    render(<Button variant="primary">Primary</Button>);

    expect(screen.getByRole('button')).toHaveClass('btn-primary');
  });
});
```

### Interactions utilisateur

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('submits form with user data', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();

    render(<LoginForm onSubmit={onSubmit} />);

    // Remplir le formulaire
    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');

    // Soumettre
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(onSubmit).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });

  it('shows validation errors', async () => {
    const user = userEvent.setup();

    render(<LoginForm onSubmit={vi.fn()} />);

    // Soumettre formulaire vide
    await user.click(screen.getByRole('button', { name: /sign in/i }));

    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    expect(screen.getByText(/password is required/i)).toBeInTheDocument();
  });

  it('clears input on clear button click', async () => {
    const user = userEvent.setup();

    render(<LoginForm onSubmit={vi.fn()} />);

    const emailInput = screen.getByLabelText(/email/i);
    await user.type(emailInput, 'test@example.com');

    await user.clear(emailInput);

    expect(emailInput).toHaveValue('');
  });
});
```

### Test avec providers

```typescript
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from './ThemeContext';

// Wrapper personnalisé
function createWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });

  return function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <ThemeProvider>{children}</ThemeProvider>
        </BrowserRouter>
      </QueryClientProvider>
    );
  };
}

// Render helper
function renderWithProviders(ui: React.ReactElement) {
  return render(ui, { wrapper: createWrapper() });
}

describe('Dashboard', () => {
  it('renders with providers', async () => {
    renderWithProviders(<Dashboard />);

    expect(await screen.findByText(/dashboard/i)).toBeInTheDocument();
  });
});
```

### Test async et attentes

```typescript
import { render, screen, waitFor, waitForElementToBeRemoved } from '@testing-library/react';

describe('async behavior', () => {
  it('shows loading then data', async () => {
    render(<DataLoader />);

    // Vérifie le loading
    expect(screen.getByText(/loading/i)).toBeInTheDocument();

    // Attend que les données apparaissent
    expect(await screen.findByText(/data loaded/i)).toBeInTheDocument();

    // Le loading a disparu
    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
  });

  it('waits for element to be removed', async () => {
    render(<Modal onClose={vi.fn()} />);

    await userEvent.click(screen.getByRole('button', { name: /close/i }));

    await waitForElementToBeRemoved(() => screen.queryByRole('dialog'));
  });

  it('uses waitFor for complex conditions', async () => {
    render(<ComplexComponent />);

    await waitFor(() => {
      expect(screen.getByRole('list')).toBeInTheDocument();
      expect(screen.getAllByRole('listitem')).toHaveLength(5);
    });
  });
});
```

### Mock de hooks personnalisés

```typescript
import { vi } from 'vitest';
import * as hooks from './hooks';

describe('component with custom hook', () => {
  it('mocks useAuth hook', () => {
    vi.spyOn(hooks, 'useAuth').mockReturnValue({
      user: { id: '1', name: 'John' },
      isAuthenticated: true,
      login: vi.fn(),
      logout: vi.fn(),
    });

    render(<ProtectedComponent />);

    expect(screen.getByText(/welcome, john/i)).toBeInTheDocument();
  });
});
```

### Test d'accessibilité

```typescript
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('accessibility', () => {
  it('has no accessibility violations', async () => {
    const { container } = render(<Form />);

    const results = await axe(container);

    expect(results).toHaveNoViolations();
  });

  it('has proper ARIA attributes', () => {
    render(<Modal isOpen title="Confirmation" />);

    const dialog = screen.getByRole('dialog');
    expect(dialog).toHaveAttribute('aria-labelledby');
    expect(dialog).toHaveAttribute('aria-modal', 'true');
  });
});
```

## Vue Test Utils

```typescript
import { mount, shallowMount } from '@vue/test-utils';
import { describe, it, expect, vi } from 'vitest';
import Button from './Button.vue';

describe('Button.vue', () => {
  it('renders slot content', () => {
    const wrapper = mount(Button, {
      slots: {
        default: 'Click me',
      },
    });

    expect(wrapper.text()).toContain('Click me');
  });

  it('emits click event', async () => {
    const wrapper = mount(Button);

    await wrapper.trigger('click');

    expect(wrapper.emitted('click')).toHaveLength(1);
  });

  it('applies variant class', () => {
    const wrapper = mount(Button, {
      props: {
        variant: 'primary',
      },
    });

    expect(wrapper.classes()).toContain('btn-primary');
  });

  it('is disabled when prop is true', () => {
    const wrapper = mount(Button, {
      props: { disabled: true },
    });

    expect(wrapper.attributes('disabled')).toBeDefined();
  });
});

describe('Form.vue', () => {
  it('validates and submits', async () => {
    const wrapper = mount(Form);

    await wrapper.find('input[name="email"]').setValue('test@example.com');
    await wrapper.find('form').trigger('submit');

    expect(wrapper.emitted('submit')).toBeTruthy();
    expect(wrapper.emitted('submit')[0]).toEqual([
      { email: 'test@example.com' },
    ]);
  });
});
```

## Mots-clés de routage

`React Testing Library`, `RTL`, `Vue Test Utils`, `render`, `screen`, `userEvent`, `fireEvent`, `getByRole`, `findBy`, `waitFor`, `component test`

## Livrables

| Livrable | Description |
|----------|-------------|
| Tests de composants | Fichiers .test.tsx avec tests d'interactions et intégrations |
| Utilities de test | Helpers de render avec providers et fixtures |
| Tests d'accessibilité | Tests axe-core pour validation a11y des composants |
