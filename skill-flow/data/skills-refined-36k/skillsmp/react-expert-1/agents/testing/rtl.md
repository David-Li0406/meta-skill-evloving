---
name: rtl
description: React Testing Library for component testing
workflows:
  - id: rtl-setup
    template: wf-creation
    phase: Production
    name: Setup React Testing Library
    duration: 0.5 jour
---

# React Testing Library - Tests de Composants

## Rôle

Implémentation de tests de composants React avec React Testing Library (RTL).

## Tu NE fais PAS

- ❌ Définir la stratégie de tests (pyramide, couverture) → `testing-process`
- ❌ Écrire le code applicatif à tester → développeur
- ❌ Définir les processus de CI/CD → `devops`
- ❌ Implémenter des tests E2E → `frontend-developer`

## Installation

```bash
npm install -D @testing-library/react @testing-library/jest-dom @testing-library/user-event
npm install -D vitest jsdom  # ou jest
```

## Configuration

### Vitest

```tsx
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: './src/test/setup.ts',
  },
});
```

### Setup

```tsx
// src/test/setup.ts
import '@testing-library/jest-dom';
import { cleanup } from '@testing-library/react';
import { afterEach } from 'vitest';

afterEach(() => {
  cleanup();
});
```

## Queries

### Priorité (accessible)

```tsx
// 1. getByRole - Préféré (accessible)
getByRole('button', { name: /submit/i })
getByRole('textbox', { name: /email/i })
getByRole('heading', { level: 1 })

// 2. getByLabelText - Formulaires
getByLabelText(/email/i)

// 3. getByPlaceholderText
getByPlaceholderText('Enter your email')

// 4. getByText - Contenu textuel
getByText(/welcome/i)

// 5. getByDisplayValue - Valeurs input
getByDisplayValue('john@example.com')

// 6. getByAltText - Images
getByAltText('Profile picture')

// 7. getByTitle
getByTitle('Close')

// 8. getByTestId - Dernier recours
getByTestId('custom-element')
```

### Types de queries

```tsx
// getBy - Synchrone, throw si absent
const button = screen.getByRole('button');

// queryBy - Synchrone, retourne null si absent
const button = screen.queryByRole('button');
expect(button).not.toBeInTheDocument();

// findBy - Asynchrone, attend jusqu'à timeout
const button = await screen.findByRole('button');

// getAllBy, queryAllBy, findAllBy - Multiples
const buttons = screen.getAllByRole('button');
```

## Test de Base

```tsx
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
});
```

## User Events

### Setup

```tsx
import userEvent from '@testing-library/user-event';

// Toujours setup au début du test
const user = userEvent.setup();
```

### Interactions

```tsx
// Click
await user.click(element);
await user.dblClick(element);
await user.tripleClick(element);

// Typing
await user.type(input, 'Hello');
await user.clear(input);
await user.type(input, 'New text');

// Keyboard
await user.keyboard('{Enter}');
await user.keyboard('{Shift>}A{/Shift}'); // Shift+A

// Selection
await user.selectOptions(select, ['option1', 'option2']);

// Hover
await user.hover(element);
await user.unhover(element);

// Tab
await user.tab();
await user.tab({ shift: true }); // Shift+Tab

// Clipboard
await user.copy();
await user.paste();
```

## Tests de Formulaire

```tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('submits the form with entered values', async () => {
    const user = userEvent.setup();
    const onSubmit = vi.fn();

    render(<LoginForm onSubmit={onSubmit} />);

    // Remplir le formulaire
    await user.type(screen.getByLabelText(/email/i), 'john@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');

    // Soumettre
    await user.click(screen.getByRole('button', { name: /submit/i }));

    // Vérifier
    expect(onSubmit).toHaveBeenCalledWith({
      email: 'john@example.com',
      password: 'password123',
    });
  });

  it('shows validation errors', async () => {
    const user = userEvent.setup();

    render(<LoginForm onSubmit={vi.fn()} />);

    // Soumettre sans remplir
    await user.click(screen.getByRole('button', { name: /submit/i }));

    // Vérifier les erreurs
    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    expect(screen.getByText(/password is required/i)).toBeInTheDocument();
  });
});
```

## Tests Asynchrones

```tsx
import { render, screen, waitFor } from '@testing-library/react';

describe('AsyncComponent', () => {
  it('loads and displays data', async () => {
    render(<UserProfile userId="123" />);

    // Attendre le chargement
    expect(screen.getByText(/loading/i)).toBeInTheDocument();

    // Attendre les données
    const name = await screen.findByText('John Doe');
    expect(name).toBeInTheDocument();
  });

  it('shows error on failure', async () => {
    // Mock d'une erreur
    server.use(
      http.get('/api/user/:id', () => {
        return HttpResponse.error();
      })
    );

    render(<UserProfile userId="123" />);

    // Attendre l'erreur
    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });
});
```

## Test avec Providers

```tsx
// test/utils.tsx
import { render, RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';

interface WrapperProps {
  children: React.ReactNode;
}

function AllProviders({ children }: WrapperProps) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {children}
      </BrowserRouter>
    </QueryClientProvider>
  );
}

function customRender(
  ui: React.ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) {
  return render(ui, { wrapper: AllProviders, ...options });
}

export * from '@testing-library/react';
export { customRender as render };
```

### Usage

```tsx
import { render, screen } from '@/test/utils';

describe('App', () => {
  it('renders with providers', () => {
    render(<App />);
    // ...
  });
});
```

## Assertions

### jest-dom

```tsx
// Présence
expect(element).toBeInTheDocument();
expect(element).not.toBeInTheDocument();

// Visibilité
expect(element).toBeVisible();
expect(element).not.toBeVisible();

// Contenu
expect(element).toHaveTextContent('Hello');
expect(element).toHaveTextContent(/hello/i);

// Attributs
expect(element).toHaveAttribute('href', '/home');
expect(element).toHaveClass('active');
expect(element).toHaveStyle({ color: 'red' });

// Formulaires
expect(input).toHaveValue('text');
expect(input).toBeChecked();
expect(input).toBeDisabled();
expect(input).toBeRequired();
expect(input).toBeInvalid();
expect(input).toHaveFocus();
```

## Debug

```tsx
// Afficher le DOM
screen.debug();
screen.debug(element);

// Logger les rôles accessibles
screen.logTestingPlaygroundURL();

// Prettier output
import { prettyDOM } from '@testing-library/react';
console.log(prettyDOM(element));
```

## Bonnes Pratiques

1. **Queries accessibles** - Role > Text > TestId
2. **userEvent** - Préférer à fireEvent
3. **Comportement utilisateur** - Tester ce que l'utilisateur voit/fait
4. **Custom render** - Avec providers
5. **Async queries** - findBy pour le contenu async

## Anti-patterns

```tsx
// ❌ Tester l'implémentation
expect(component.state.count).toBe(1);

// ✅ Tester le comportement
expect(screen.getByText('Count: 1')).toBeInTheDocument();

// ❌ getByTestId partout
getByTestId('submit-button')

// ✅ getByRole
getByRole('button', { name: /submit/i })

// ❌ waitFor inutile
await waitFor(() => {
  expect(screen.getByText('Hello')).toBeInTheDocument();
});

// ✅ findBy directement
expect(await screen.findByText('Hello')).toBeInTheDocument();
```

## Voir aussi

- `hooks-testing.md` - Tests de hooks
- `mocking.md` - Mocks et MSW
- `../components/forms.md` - Composants formulaire

## Livrables

| Livrable | Description |
|----------|-------------|
| Tests fichiers | Fichiers .test.tsx avec describe/it/expect |
| Mocks setup | Configuration custom render avec providers |
| Utilities testing | Helpers pour queries et assertions |
