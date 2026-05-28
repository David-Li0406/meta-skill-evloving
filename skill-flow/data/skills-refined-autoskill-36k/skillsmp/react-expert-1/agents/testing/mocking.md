---
name: mocking
description: Mocks, spies, and MSW for testing
workflows:
  - id: mocking-setup
    template: wf-creation
    phase: Production
    name: Setup mocking MSW
    duration: 0.5-1 jour
---

# Mocking - Mocks, Spies et MSW

## Rôle

Implémentation de mocks pour les tests React : modules, providers, API avec MSW.

## Tu NE fais PAS

- ❌ Définir la stratégie de tests → `testing-process`
- ❌ Écrire le code applicatif à tester → développeur
- ❌ Implémenter le backend réel → `backend-developer`
- ❌ Définir les processus de CI/CD → `devops`

## Vitest/Jest Mocks

### Mock de module

```tsx
// Mock complet
vi.mock('./api', () => ({
  fetchUser: vi.fn(),
  updateUser: vi.fn(),
}));

// Mock partiel
vi.mock('./utils', async () => {
  const actual = await vi.importActual('./utils');
  return {
    ...actual,
    formatDate: vi.fn(() => '2024-01-01'),
  };
});
```

### Mock de fonction

```tsx
import { vi } from 'vitest';

// Créer un mock
const mockFn = vi.fn();
const mockFnWithReturn = vi.fn(() => 'default');
const mockFnWithImpl = vi.fn((x: number) => x * 2);

// Configurer les retours
mockFn.mockReturnValue('value');
mockFn.mockReturnValueOnce('first').mockReturnValueOnce('second');
mockFn.mockResolvedValue({ data: 'async' });
mockFn.mockRejectedValue(new Error('fail'));

// Assertions
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledTimes(2);
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
expect(mockFn).toHaveBeenLastCalledWith('lastArg');
expect(mockFn).toHaveBeenNthCalledWith(1, 'firstArg');

// Reset
mockFn.mockClear(); // Clear calls
mockFn.mockReset(); // Clear calls + implementation
mockFn.mockRestore(); // Restore original (spies)
```

### Spy

```tsx
const user = {
  getName: () => 'John',
};

const spy = vi.spyOn(user, 'getName');
spy.mockReturnValue('Jane');

expect(user.getName()).toBe('Jane');
expect(spy).toHaveBeenCalled();

spy.mockRestore();
expect(user.getName()).toBe('John');
```

## Mock de Hooks

### useNavigate (React Router)

```tsx
const mockNavigate = vi.fn();

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  };
});

describe('Component with navigation', () => {
  beforeEach(() => {
    mockNavigate.mockClear();
  });

  it('navigates on click', async () => {
    const user = userEvent.setup();
    render(<MyComponent />);

    await user.click(screen.getByRole('button', { name: /go home/i }));

    expect(mockNavigate).toHaveBeenCalledWith('/home');
  });
});
```

### useParams

```tsx
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useParams: () => ({ id: '123' }),
  };
});
```

## Mock de Providers

### Context Mock

```tsx
import { createContext, useContext } from 'react';

// Context original
const AuthContext = createContext<AuthContextType | null>(null);

// Test avec mock
describe('ProtectedRoute', () => {
  const mockUser = { id: '1', name: 'John' };

  function renderWithAuth(ui: React.ReactElement, user = mockUser) {
    return render(
      <AuthContext.Provider value={{ user, login: vi.fn(), logout: vi.fn() }}>
        {ui}
      </AuthContext.Provider>
    );
  }

  it('shows content for authenticated user', () => {
    renderWithAuth(<ProtectedRoute><Dashboard /></ProtectedRoute>);
    expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
  });

  it('redirects unauthenticated user', () => {
    renderWithAuth(<ProtectedRoute><Dashboard /></ProtectedRoute>, null);
    expect(mockNavigate).toHaveBeenCalledWith('/login');
  });
});
```

### Query Client Mock

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        gcTime: Infinity,
      },
    },
  });
}

function renderWithQuery(ui: React.ReactElement) {
  const testQueryClient = createTestQueryClient();
  return render(
    <QueryClientProvider client={testQueryClient}>
      {ui}
    </QueryClientProvider>
  );
}
```

## MSW - Mock Service Worker

### Installation

```bash
npm install -D msw
```

### Setup

```tsx
// src/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/users', () => {
    return HttpResponse.json([
      { id: '1', name: 'John' },
      { id: '2', name: 'Jane' },
    ]);
  }),

  http.get('/api/users/:id', ({ params }) => {
    return HttpResponse.json({
      id: params.id,
      name: 'John Doe',
      email: 'john@example.com',
    });
  }),

  http.post('/api/users', async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json(
      { id: '3', ...body },
      { status: 201 }
    );
  }),

  http.delete('/api/users/:id', () => {
    return new HttpResponse(null, { status: 204 });
  }),
];
```

### Setup Server

```tsx
// src/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

### Configuration Tests

```tsx
// src/test/setup.ts
import { server } from '../mocks/server';

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Usage dans les tests

```tsx
import { server } from '../mocks/server';
import { http, HttpResponse } from 'msw';

describe('UserList', () => {
  it('displays users', async () => {
    render(<UserList />);

    expect(await screen.findByText('John')).toBeInTheDocument();
    expect(screen.getByText('Jane')).toBeInTheDocument();
  });

  it('handles error', async () => {
    // Override pour ce test
    server.use(
      http.get('/api/users', () => {
        return HttpResponse.json(
          { message: 'Server error' },
          { status: 500 }
        );
      })
    );

    render(<UserList />);

    expect(await screen.findByText(/error/i)).toBeInTheDocument();
  });

  it('handles loading state', () => {
    // Delay pour voir le loading
    server.use(
      http.get('/api/users', async () => {
        await delay(100);
        return HttpResponse.json([]);
      })
    );

    render(<UserList />);

    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });
});
```

### Patterns MSW Avancés

```tsx
// Réponse conditionnelle
http.get('/api/users', ({ request }) => {
  const url = new URL(request.url);
  const status = url.searchParams.get('status');

  if (status === 'active') {
    return HttpResponse.json([{ id: '1', name: 'Active User' }]);
  }

  return HttpResponse.json([]);
});

// Compteur d'appels
let callCount = 0;
http.get('/api/data', () => {
  callCount++;
  return HttpResponse.json({ calls: callCount });
});

// Network error
http.get('/api/data', () => {
  return HttpResponse.error();
});

// Delay
import { delay } from 'msw';
http.get('/api/data', async () => {
  await delay(1000);
  return HttpResponse.json({ data: 'delayed' });
});
```

## Mock de Window/Document

```tsx
// localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
};

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// matchMedia
Object.defineProperty(window, 'matchMedia', {
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// IntersectionObserver
const mockIntersectionObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));

window.IntersectionObserver = mockIntersectionObserver;
```

## Bonnes Pratiques

1. **MSW pour les APIs** - Plus réaliste que vi.mock
2. **Reset après chaque test** - Éviter les interférences
3. **Mock au bon niveau** - Préférer les boundaries
4. **Éviter les mocks excessifs** - Tests fragiles
5. **Type les mocks** - Cohérence avec le code

## Anti-patterns

```tsx
// ❌ Mock de tout
vi.mock('react', () => ({ useState: vi.fn() }));

// ❌ Mock d'implémentation interne
vi.mock('./Component', () => ({
  Component: () => <div>Mocked</div>,
}));

// ✅ Mock des dépendances externes
vi.mock('./api');
// Et utiliser MSW pour les vraies requêtes
```

## Voir aussi

- `rtl.md` - Tests de composants
- `hooks-testing.md` - Tests de hooks
- `../data/react-query.md` - Data fetching

## Livrables

| Livrable | Description |
|----------|-------------|
| MSW handlers | Configuration mocks API avec handlers MSW |
| Mock setup | Configuration vi.mock pour modules et hooks |
| Testing utilities | Helpers pour providers et context mocks |
