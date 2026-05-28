# Routing Guide

React Router implementation with traditional routing, lazy loading, and protected routes.

---

## React Router Overview

**React Router v6** with traditional routing:
- Routes defined in `App.tsx`
- Protected routes with `AuthContext`
- Lazy loading for code splitting
- Type-safe navigation with hooks
- Programmatic navigation support

---

## Route Setup

### Basic App.tsx Structure

```tsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { lazy, Suspense } from 'react';
import { SuspenseLoader } from '@/components/SuspenseLoader';

// Lazy load pages
const HomePage = lazy(() => import('@/pages/HomePage'));
const GamesPage = lazy(() => import('@/pages/GamesPage'));
const GamePage = lazy(() => import('@/pages/GamePage'));
const LoginPage = lazy(() => import('@/pages/LoginPage'));

function App() {
    return (
        <BrowserRouter>
            <Suspense fallback={<SuspenseLoader />}>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/games" element={
                        <ProtectedRoute>
                            <GamesPage />
                        </ProtectedRoute>
                    } />
                    <Route path="/games/:id" element={
                        <ProtectedRoute>
                            <GamePage />
                        </ProtectedRoute>
                    } />
                    <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
            </Suspense>
        </BrowserRouter>
    );
}
```

---

## Protected Routes

### ProtectedRoute Component

```tsx
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/contexts/AuthContext';

interface ProtectedRouteProps {
    children: React.ReactNode;
    requireAdmin?: boolean;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
    children,
    requireAdmin = false
}) => {
    const { user, isCheckingAuth } = useAuth();
    const location = useLocation();

    if (isCheckingAuth) {
        return <SuspenseLoader />;
    }

    if (!user) {
        // Redirect to login, saving the attempted location
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    if (requireAdmin && user.role !== 'admin') {
        return <Navigate to="/unauthorized" replace />;
    }

    return <>{children}</>;
};
```

### Usage

```tsx
// In App.tsx
<Route path="/admin" element={
    <ProtectedRoute requireAdmin>
        <AdminDashboard />
    </ProtectedRoute>
} />

<Route path="/profile" element={
    <ProtectedRoute>
        <UserProfile />
    </ProtectedRoute>
} />
```

---

## Navigation Patterns

### useNavigate Hook

```tsx
import { useNavigate } from 'react-router-dom';

export const GameList: React.FC = () => {
    const navigate = useNavigate();

    const handleGameClick = (gameId: string) => {
        navigate(`/games/${gameId}`);
    };

    const handleCreateGame = () => {
        navigate('/games/new');
    };

    // Navigate with state
    const handleEditGame = (game: Game) => {
        navigate(`/games/${game.id}/edit`, {
            state: { game }
        });
    };

    // Replace history entry
    const handleCancel = () => {
        navigate(-1); // Go back
    };

    return (
        <div>
            <Button onClick={handleCreateGame}>New Game</Button>
            {/* ... */}
        </div>
    );
};
```

### Link Component

```tsx
import { Link, NavLink } from 'react-router-dom';

export const Navigation: React.FC = () => {
    return (
        <nav className="flex gap-4">
            {/* Basic link */}
            <Link to="/" className="text-primary hover:underline">
                Home
            </Link>

            {/* NavLink with active state */}
            <NavLink
                to="/games"
                className={({ isActive }) =>
                    isActive
                        ? "text-primary font-bold"
                        : "text-text-primary hover:text-primary"
                }
            >
                Games
            </NavLink>

            {/* Link with state */}
            <Link
                to="/messages"
                state={{ from: 'navigation' }}
            >
                Messages
            </Link>
        </nav>
    );
};
```

---

## Route Parameters

### Using useParams

```tsx
import { useParams, Navigate } from 'react-router-dom';
import { useSuspenseQuery } from '@tanstack/react-query';

interface GamePageParams {
    id: string;
}

export const GamePage: React.FC = () => {
    const { id } = useParams<GamePageParams>();

    if (!id) {
        return <Navigate to="/games" replace />;
    }

    const { data: game } = useSuspenseQuery({
        queryKey: ['game', id],
        queryFn: () => api.games.getById(id),
    });

    return (
        <div>
            <h1>{game.name}</h1>
            {/* ... */}
        </div>
    );
};
```

### Query Parameters

```tsx
import { useSearchParams } from 'react-router-dom';

export const GamesPage: React.FC = () => {
    const [searchParams, setSearchParams] = useSearchParams();

    const filter = searchParams.get('filter') || 'all';
    const page = parseInt(searchParams.get('page') || '1', 10);

    const handleFilterChange = (newFilter: string) => {
        setSearchParams(prev => {
            prev.set('filter', newFilter);
            prev.set('page', '1'); // Reset to page 1
            return prev;
        });
    };

    return (
        <div>
            <select
                value={filter}
                onChange={(e) => handleFilterChange(e.target.value)}
            >
                <option value="all">All Games</option>
                <option value="active">Active</option>
                <option value="completed">Completed</option>
            </select>
            {/* ... */}
        </div>
    );
};
```

---

## Lazy Loading Routes

### Pattern for Page Components

```tsx
// pages/GamePage.tsx
import React from 'react';

const GamePage: React.FC = () => {
    return (
        <div>
            {/* Page content */}
        </div>
    );
};

// Default export for lazy loading
export default GamePage;

// App.tsx
const GamePage = lazy(() => import('@/pages/GamePage'));
```

### Route-Level Code Splitting

```tsx
// App.tsx with multiple lazy-loaded sections
function App() {
    return (
        <BrowserRouter>
            <Routes>
                {/* Public routes */}
                <Route path="/" element={
                    <Suspense fallback={<SuspenseLoader />}>
                        <HomePage />
                    </Suspense>
                } />

                {/* Auth routes */}
                <Route path="/auth/*" element={
                    <Suspense fallback={<SuspenseLoader />}>
                        <AuthRoutes />
                    </Suspense>
                } />

                {/* Game routes */}
                <Route path="/games/*" element={
                    <Suspense fallback={<SuspenseLoader />}>
                        <GameRoutes />
                    </Suspense>
                } />
            </Routes>
        </BrowserRouter>
    );
}
```

---

## Nested Routes

### Layout Routes

```tsx
// layouts/DashboardLayout.tsx
import { Outlet } from 'react-router-dom';

export const DashboardLayout: React.FC = () => {
    return (
        <div className="flex h-screen">
            <Sidebar />
            <main className="flex-1 overflow-auto">
                <Outlet /> {/* Nested routes render here */}
            </main>
        </div>
    );
};

// App.tsx
<Route path="/dashboard" element={<DashboardLayout />}>
    <Route index element={<DashboardHome />} />
    <Route path="stats" element={<StatsPage />} />
    <Route path="settings" element={<SettingsPage />} />
</Route>
```

### Route Groups

```tsx
// routes/GameRoutes.tsx
export const GameRoutes: React.FC = () => {
    return (
        <Routes>
            <Route path="/" element={<GamesListPage />} />
            <Route path="/new" element={<CreateGamePage />} />
            <Route path="/:id" element={<GamePage />} />
            <Route path="/:id/edit" element={<EditGamePage />} />
            <Route path="/:id/players" element={<GamePlayersPage />} />
        </Routes>
    );
};
```

---

## Navigation Guards

### Redirect After Login

```tsx
// LoginPage.tsx
import { useNavigate, useLocation } from 'react-router-dom';

export const LoginPage: React.FC = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { login } = useAuth();

    const from = location.state?.from?.pathname || '/dashboard';

    const handleLogin = async (credentials: LoginCredentials) => {
        try {
            await login(credentials);
            // Redirect to where they came from or dashboard
            navigate(from, { replace: true });
        } catch (error) {
            // Handle error
        }
    };

    return (
        <form onSubmit={handleLogin}>
            {/* Login form */}
        </form>
    );
};
```

### Prompt Before Navigation

```tsx
import { useBeforeUnload } from 'react-router-dom';

export const EditGamePage: React.FC = () => {
    const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);

    // Browser prompt
    useBeforeUnload(
        useCallback(
            (e) => {
                if (hasUnsavedChanges) {
                    e.preventDefault();
                    e.returnValue = '';
                }
            },
            [hasUnsavedChanges]
        )
    );

    return (
        <div>
            {/* Edit form */}
        </div>
    );
};
```

---

## Error Boundaries

### Route Error Handling

```tsx
// components/RouteError.tsx
import { useRouteError, isRouteErrorResponse } from 'react-router-dom';

export const RouteError: React.FC = () => {
    const error = useRouteError();

    if (isRouteErrorResponse(error)) {
        if (error.status === 404) {
            return (
                <div className="text-center py-12">
                    <h1>Page Not Found</h1>
                    <Link to="/">Go Home</Link>
                </div>
            );
        }

        if (error.status === 401) {
            return <Navigate to="/login" replace />;
        }
    }

    return (
        <div className="text-center py-12">
            <h1>Something went wrong</h1>
            <Link to="/">Go Home</Link>
        </div>
    );
};

// App.tsx
<Route
    path="/games/:id"
    element={<GamePage />}
    errorElement={<RouteError />}
/>
```

---

## Best Practices

### DO ✅

- Use lazy loading for all page components
- Wrap lazy components in Suspense boundaries
- Use protected routes for authenticated pages
- Handle loading states with SuspenseLoader
- Use type-safe params with TypeScript
- Provide fallback routes for 404s
- Save location state for login redirects

### DON'T ❌

- Don't nest Suspense boundaries unnecessarily
- Don't use window.location for navigation
- Don't forget to handle undefined params
- Don't use route paths as strings (create constants)
- Don't forget error boundaries for routes

---

## Common Patterns

### Route Constants

```tsx
// constants/routes.ts
export const ROUTES = {
    HOME: '/',
    LOGIN: '/login',
    GAMES: '/games',
    GAME_DETAIL: (id: string) => `/games/${id}`,
    GAME_EDIT: (id: string) => `/games/${id}/edit`,
    USER_PROFILE: (id: string) => `/users/${id}`,
} as const;

// Usage
navigate(ROUTES.GAME_DETAIL(gameId));
<Link to={ROUTES.GAMES}>All Games</Link>
```

### Breadcrumbs

```tsx
import { useMatches } from 'react-router-dom';

export const Breadcrumbs: React.FC = () => {
    const matches = useMatches();

    const breadcrumbs = matches
        .filter((match) => Boolean(match.handle?.crumb))
        .map((match) => match.handle.crumb);

    return (
        <nav className="flex gap-2">
            {breadcrumbs.map((crumb, index) => (
                <span key={index}>
                    {index > 0 && ' > '}
                    {crumb}
                </span>
            ))}
        </nav>
    );
};
```

---

## Migration from TanStack Router

If migrating from TanStack Router:

1. Replace `createFileRoute` with Route components
2. Move route files to pages directory
3. Update imports from `@tanstack/react-router` to `react-router-dom`
4. Replace loader patterns with React Query in components
5. Update navigation from `router.navigate` to `navigate` hook
