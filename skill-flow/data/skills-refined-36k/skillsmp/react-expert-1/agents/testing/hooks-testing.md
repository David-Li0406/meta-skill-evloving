---
name: hooks-testing
description: Testing custom hooks with renderHook
workflows:
  - id: hooks-testing-setup
    template: wf-creation
    phase: Production
    name: Setup tests hooks
    duration: 0.5 jour
---

# Hooks Testing - Tests de Custom Hooks

## Rôle

Implémentation de tests pour les custom hooks React avec `@testing-library/react`.

## Tu NE fais PAS

- ❌ Définir la stratégie de tests → `testing-process`
- ❌ Écrire le code applicatif (hooks) à tester → développeur
- ❌ Tester les composants (utiliser RTL) → `rtl.md`
- ❌ Définir les processus de CI/CD → `devops`

## Installation

```bash
npm install -D @testing-library/react
```

## renderHook

### Test de base

```tsx
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('initializes with default value', () => {
    const { result } = renderHook(() => useCounter());

    expect(result.current.count).toBe(0);
  });

  it('initializes with provided value', () => {
    const { result } = renderHook(() => useCounter(10));

    expect(result.current.count).toBe(10);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });

  it('decrements count', () => {
    const { result } = renderHook(() => useCounter(10));

    act(() => {
      result.current.decrement();
    });

    expect(result.current.count).toBe(9);
  });
});
```

## act()

### Mises à jour synchrones

```tsx
import { renderHook, act } from '@testing-library/react';
import { useToggle } from './useToggle';

describe('useToggle', () => {
  it('toggles value', () => {
    const { result } = renderHook(() => useToggle(false));

    expect(result.current.value).toBe(false);

    // Wrapper les updates dans act()
    act(() => {
      result.current.toggle();
    });

    expect(result.current.value).toBe(true);

    act(() => {
      result.current.toggle();
    });

    expect(result.current.value).toBe(false);
  });
});
```

### Mises à jour asynchrones

```tsx
import { renderHook, waitFor } from '@testing-library/react';
import { useFetch } from './useFetch';

describe('useFetch', () => {
  it('fetches data', async () => {
    const { result } = renderHook(() => useFetch('/api/users'));

    // Initial state
    expect(result.current.isLoading).toBe(true);
    expect(result.current.data).toBeNull();

    // Wait for fetch to complete
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.data).toEqual([{ id: 1, name: 'John' }]);
  });

  it('handles errors', async () => {
    server.use(
      http.get('/api/users', () => {
        return HttpResponse.error();
      })
    );

    const { result } = renderHook(() => useFetch('/api/users'));

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.error).toBeTruthy();
  });
});
```

## Test avec Props Changeantes

### rerender()

```tsx
import { renderHook } from '@testing-library/react';
import { useDebounce } from './useDebounce';

describe('useDebounce', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('debounces value changes', () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      { initialProps: { value: 'initial', delay: 500 } }
    );

    expect(result.current).toBe('initial');

    // Change value
    rerender({ value: 'updated', delay: 500 });

    // Not updated yet
    expect(result.current).toBe('initial');

    // Advance timers
    act(() => {
      vi.advanceTimersByTime(500);
    });

    // Now updated
    expect(result.current).toBe('updated');
  });
});
```

## Test avec Providers

### Wrapper option

```tsx
import { renderHook } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useUser } from './useUser';

describe('useUser', () => {
  const createWrapper = () => {
    const queryClient = new QueryClient({
      defaultOptions: {
        queries: { retry: false },
      },
    });

    return function Wrapper({ children }: { children: React.ReactNode }) {
      return (
        <QueryClientProvider client={queryClient}>
          {children}
        </QueryClientProvider>
      );
    };
  };

  it('fetches user data', async () => {
    const { result } = renderHook(() => useUser('123'), {
      wrapper: createWrapper(),
    });

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.user).toEqual({
      id: '123',
      name: 'John Doe',
    });
  });
});
```

### Multiple Providers

```tsx
function createTestWrapper() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });

  return function TestWrapper({ children }: { children: React.ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        <ThemeProvider>
          <AuthProvider>
            {children}
          </AuthProvider>
        </ThemeProvider>
      </QueryClientProvider>
    );
  };
}
```

## Test de useEffect

```tsx
import { renderHook } from '@testing-library/react';
import { useDocumentTitle } from './useDocumentTitle';

describe('useDocumentTitle', () => {
  const originalTitle = document.title;

  afterEach(() => {
    document.title = originalTitle;
  });

  it('sets document title', () => {
    renderHook(() => useDocumentTitle('New Title'));

    expect(document.title).toBe('New Title');
  });

  it('updates title when value changes', () => {
    const { rerender } = renderHook(
      ({ title }) => useDocumentTitle(title),
      { initialProps: { title: 'First Title' } }
    );

    expect(document.title).toBe('First Title');

    rerender({ title: 'Second Title' });

    expect(document.title).toBe('Second Title');
  });

  it('restores title on unmount', () => {
    const { unmount } = renderHook(() => useDocumentTitle('Test'));

    expect(document.title).toBe('Test');

    unmount();

    expect(document.title).toBe(originalTitle);
  });
});
```

## Test de useRef

```tsx
import { renderHook } from '@testing-library/react';
import { usePrevious } from './usePrevious';

describe('usePrevious', () => {
  it('returns undefined on first render', () => {
    const { result } = renderHook(() => usePrevious(1));

    expect(result.current).toBeUndefined();
  });

  it('returns previous value after update', () => {
    const { result, rerender } = renderHook(
      ({ value }) => usePrevious(value),
      { initialProps: { value: 1 } }
    );

    expect(result.current).toBeUndefined();

    rerender({ value: 2 });
    expect(result.current).toBe(1);

    rerender({ value: 3 });
    expect(result.current).toBe(2);
  });
});
```

## Test de useCallback/useMemo

```tsx
import { renderHook } from '@testing-library/react';
import { useStableCallback } from './useStableCallback';

describe('useStableCallback', () => {
  it('returns stable reference', () => {
    const callback = vi.fn();

    const { result, rerender } = renderHook(
      ({ cb }) => useStableCallback(cb),
      { initialProps: { cb: callback } }
    );

    const firstRef = result.current;

    rerender({ cb: vi.fn() }); // New callback

    // Reference should be the same
    expect(result.current).toBe(firstRef);
  });

  it('calls the latest callback', () => {
    const callback1 = vi.fn();
    const callback2 = vi.fn();

    const { result, rerender } = renderHook(
      ({ cb }) => useStableCallback(cb),
      { initialProps: { cb: callback1 } }
    );

    result.current();
    expect(callback1).toHaveBeenCalled();

    rerender({ cb: callback2 });

    result.current();
    expect(callback2).toHaveBeenCalled();
  });
});
```

## Test avec Timers

```tsx
import { renderHook, act } from '@testing-library/react';
import { useInterval } from './useInterval';

describe('useInterval', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('calls callback at interval', () => {
    const callback = vi.fn();

    renderHook(() => useInterval(callback, 1000));

    expect(callback).not.toHaveBeenCalled();

    act(() => {
      vi.advanceTimersByTime(1000);
    });
    expect(callback).toHaveBeenCalledTimes(1);

    act(() => {
      vi.advanceTimersByTime(1000);
    });
    expect(callback).toHaveBeenCalledTimes(2);
  });

  it('clears interval on unmount', () => {
    const callback = vi.fn();

    const { unmount } = renderHook(() => useInterval(callback, 1000));

    unmount();

    act(() => {
      vi.advanceTimersByTime(5000);
    });

    expect(callback).not.toHaveBeenCalled();
  });

  it('pauses when delay is null', () => {
    const callback = vi.fn();

    const { rerender } = renderHook(
      ({ delay }) => useInterval(callback, delay),
      { initialProps: { delay: 1000 as number | null } }
    );

    act(() => {
      vi.advanceTimersByTime(1000);
    });
    expect(callback).toHaveBeenCalledTimes(1);

    rerender({ delay: null });

    act(() => {
      vi.advanceTimersByTime(5000);
    });
    expect(callback).toHaveBeenCalledTimes(1); // Still 1
  });
});
```

## Bonnes Pratiques

1. **act() pour les updates** - Toujours wrapper les mutations d'état
2. **waitFor pour async** - Attendre les effets asynchrones
3. **Wrapper avec providers** - Quand le hook les nécessite
4. **Fake timers** - Pour les hooks avec delays/intervals
5. **Cleanup** - Reset les mocks et timers

## Voir aussi

- `rtl.md` - Tests de composants
- `mocking.md` - Mocks et stubs
- `../hooks/custom-hooks.md` - Création de hooks

## Livrables

| Livrable | Description |
|----------|-------------|
| Tests fichiers | Fichiers .test.tsx avec renderHook |
| Wrappers setup | Configuration wrapper avec providers |
| Patterns d'usage | Best practices act, waitFor, rerender |
