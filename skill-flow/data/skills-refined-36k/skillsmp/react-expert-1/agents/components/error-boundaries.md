---
name: error-boundaries
description: Error Boundary implementation for React error handling
workflows:
  - id: error-handling-setup
    template: wf-creation
    phase: Production
    name: Setup gestion erreurs React
    duration: 0.5 jour
---

# Error Boundaries - Gestion d'Erreurs React

## Rôle

Implémentation des Error Boundaries et patterns de gestion d'erreurs dans React.

## Tu NE fais PAS

- ❌ Définir la stratégie globale de gestion d'erreurs → `direction-technique`
- ❌ Implémenter les hooks personnalisés de gestion d'erreur → `../hooks/custom-hooks.md`
- ❌ Configurer les services de logging backend → `backend-developer`
- ❌ Définir la stratégie de tests → `testing-process`

## Error Boundary - Classe

### Implémentation de base

```tsx
import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    this.props.onError?.(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <div role="alert">
          <h2>Something went wrong</h2>
          <pre>{this.state.error?.message}</pre>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

### Usage

```tsx
function App() {
  return (
    <ErrorBoundary
      fallback={<ErrorPage />}
      onError={(error) => logToService(error)}
    >
      <MainContent />
    </ErrorBoundary>
  );
}
```

## Error Boundary avec Reset

```tsx
interface Props {
  children: ReactNode;
  fallback: (props: { error: Error; reset: () => void }) => ReactNode;
  onReset?: () => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundaryWithReset extends Component<Props, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  reset = () => {
    this.props.onReset?.();
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError && this.state.error) {
      return this.props.fallback({
        error: this.state.error,
        reset: this.reset,
      });
    }
    return this.props.children;
  }
}

// Usage
<ErrorBoundaryWithReset
  fallback={({ error, reset }) => (
    <div>
      <h2>Error: {error.message}</h2>
      <button onClick={reset}>Try again</button>
    </div>
  )}
  onReset={() => clearCache()}
>
  <App />
</ErrorBoundaryWithReset>
```

## react-error-boundary (recommandé)

### Installation

```bash
npm install react-error-boundary
```

### Usage

```tsx
import { ErrorBoundary, useErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert">
      <h2>Something went wrong</h2>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      onReset={() => {
        // Reset app state
      }}
      onError={(error, info) => {
        // Log to service
        logErrorToService(error, info);
      }}
    >
      <MainContent />
    </ErrorBoundary>
  );
}
```

### useErrorBoundary hook

```tsx
function DataFetcher() {
  const { showBoundary } = useErrorBoundary();

  const fetchData = async () => {
    try {
      const data = await api.getData();
      setData(data);
    } catch (error) {
      // Trigger le boundary parent
      showBoundary(error);
    }
  };

  // ...
}
```

### Reset on navigation

```tsx
import { useLocation } from 'react-router-dom';

function App() {
  const location = useLocation();

  return (
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      resetKeys={[location.pathname]} // Reset quand la route change
    >
      <Routes />
    </ErrorBoundary>
  );
}
```

## Suspense et Error Boundaries

### Combinaison

```tsx
import { Suspense } from 'react';
import { ErrorBoundary } from 'react-error-boundary';

function AsyncComponent() {
  return (
    <ErrorBoundary fallback={<ErrorMessage />}>
      <Suspense fallback={<Loading />}>
        <DataComponent />
      </Suspense>
    </ErrorBoundary>
  );
}
```

### Suspense pour Data Fetching (React 18+)

```tsx
// Avec use() (React 19) ou libraries comme React Query

function UserProfile({ userId }) {
  return (
    <ErrorBoundary fallback={<UserError />}>
      <Suspense fallback={<UserSkeleton />}>
        <UserDetails userId={userId} />
      </Suspense>
    </ErrorBoundary>
  );
}
```

## Granularité des Boundaries

### Stratégie recommandée

```tsx
function App() {
  return (
    // Boundary global - catch-all
    <ErrorBoundary fallback={<CriticalError />}>
      <Layout>
        <Header />

        {/* Boundary par section */}
        <ErrorBoundary fallback={<SidebarError />}>
          <Sidebar />
        </ErrorBoundary>

        <main>
          {/* Boundary par feature */}
          <ErrorBoundary fallback={<WidgetError />}>
            <Widget />
          </ErrorBoundary>

          <ErrorBoundary fallback={<ChartError />}>
            <Chart />
          </ErrorBoundary>
        </main>
      </Layout>
    </ErrorBoundary>
  );
}
```

## Patterns Avancés

### Error Boundary conditionnel

```tsx
function FeatureFlag({ children, feature }) {
  const isEnabled = useFeatureFlag(feature);

  if (!isEnabled) return null;

  return (
    <ErrorBoundary
      fallback={<FeatureDisabled feature={feature} />}
      onError={() => disableFeature(feature)}
    >
      {children}
    </ErrorBoundary>
  );
}
```

### Retry automatique

```tsx
function RetryBoundary({ children, maxRetries = 3 }) {
  const [retryCount, setRetryCount] = useState(0);

  return (
    <ErrorBoundary
      fallback={({ reset }) => (
        <div>
          <p>Failed after {retryCount} retries</p>
          {retryCount < maxRetries && (
            <button onClick={() => {
              setRetryCount(r => r + 1);
              reset();
            }}>
              Retry ({maxRetries - retryCount} left)
            </button>
          )}
        </div>
      )}
      resetKeys={[retryCount]}
    >
      {children}
    </ErrorBoundary>
  );
}
```

## Ce que les Error Boundaries NE catchent PAS

1. Event handlers (utiliser try/catch)
2. Code asynchrone (Promises, setTimeout)
3. Server-side rendering
4. Erreurs dans le boundary lui-même

### Gestion dans les handlers

```tsx
function Button() {
  const [error, setError] = useState<Error | null>(null);

  const handleClick = async () => {
    try {
      await riskyOperation();
    } catch (e) {
      setError(e as Error);
      // Ou showBoundary(e) avec useErrorBoundary
    }
  };

  if (error) {
    return <ErrorDisplay error={error} />;
  }

  return <button onClick={handleClick}>Click me</button>;
}
```

## Logging des erreurs

```tsx
function logError(error: Error, info: ErrorInfo) {
  // Sentry, LogRocket, etc.
  Sentry.captureException(error, {
    extra: {
      componentStack: info.componentStack,
    },
  });
}

<ErrorBoundary
  FallbackComponent={ErrorFallback}
  onError={logError}
>
  <App />
</ErrorBoundary>
```

## Bonnes Pratiques

1. **Plusieurs boundaries** - Granularité adaptée
2. **Fallback utile** - Pas juste "Error"
3. **Reset possible** - Permettre la récupération
4. **Logging** - Toujours logger les erreurs
5. **react-error-boundary** - Préférer à l'implémentation manuelle

## Voir aussi

- `functional.md` - Composants de base
- `../data/suspense.md` - Data fetching avec Suspense
- `../testing/rtl.md` - Tester les error boundaries

## Livrables

| Livrable | Description |
|----------|-------------|
| Error Boundary | Composant ErrorBoundary class ou react-error-boundary |
| Fallback UI | Composant d'affichage d'erreur avec reset |
| Pattern de gestion | Stratégie de granularité et logging |
