# Navigation Palette Example

Production-ready navigation palette for route/page discovery with recent routes tracking and frequency-based suggestions.

## Features

- **Modal Variant** - Centered overlay triggered by `Cmd+Shift+P` (or `Ctrl+Shift+P` on Windows/Linux)
- **Fuzzy Search** - Search through route names, paths, sections, and descriptions with typo tolerance
- **Recent Routes** - Track and display the last 10 visited routes
- **Frequency Tracking** - Surface most frequently visited routes when palette opens
- **Route Grouping** - Organize routes by section (App, Settings, Admin, Public)
- **Breadcrumb Display** - Show navigation path for nested routes
- **External Link Indication** - Visual indicator for routes that open externally
- **Keyboard Navigation** - Full keyboard support with arrow keys, enter, and escape
- **Persistent Storage** - Recent routes and frequency data saved to localStorage

## Components

### NavigationPalette.tsx

Main palette component with modal layout. Features include:

- Single-column layout optimized for route browsing
- Search input with real-time filtering
- Grouped display by section when not searching
- Recent routes section (shows when no search query)
- Most visited routes section (fallback when no recent routes)
- Keyboard navigation with visual selection highlight
- Footer with keyboard shortcuts reference

**Usage:**

```tsx
import { NavigationPalette, useNavigationPalette } from './NavigationPalette';

function App() {
  const palette = useNavigationPalette();

  return (
    <>
      <button onClick={palette.open}>Open Navigation (⌘⇧P)</button>
      <NavigationPalette isOpen={palette.isOpen} onClose={palette.close} />
    </>
  );
}
```

The `useNavigationPalette` hook automatically sets up the `Cmd+Shift+P` hotkey to toggle the palette.

### RouteResult.tsx

Result item component displaying route information:

- Route icon (emoji for visual identification)
- Route name with search highlighting
- Breadcrumb trail for nested routes (e.g., "App › Users › Profile")
- Section badge with color coding
- Recently visited indicator (⏱️)
- External link indicator (↗)
- Description text

**Props:**

```tsx
interface RouteResultProps {
  route: Route;           // Route object to display
  isRecent?: boolean;     // Show "recently visited" indicator
  searchQuery?: string;   // Query for highlighting matches
}
```

### useRouteSearch.ts

Custom hook managing search logic, history, and frequency tracking:

**Features:**
- Fuzzy matching on route name, path, section, and description
- Weighted scoring (name > path > section > description)
- Recent routes management (max 10, persisted to localStorage)
- Frequency tracking with localStorage persistence
- Most visited routes calculation
- Mock navigation function (replace with real router integration)

**Returns:**

```tsx
interface UseRouteSearchResult {
  routes: Route[];              // Filtered routes based on query
  recentRoutes: Route[];        // Last 10 visited routes
  mostVisitedRoutes: Route[];   // Top 10 by frequency
  searchQuery: string;          // Current search query
  setSearchQuery: (query: string) => void;
  navigate: (route: Route) => void;  // Navigate and track
  clearRecentRoutes: () => void;
}
```

### mock-routes.ts

Mock route data with 50+ realistic app routes:

- **App section**: Dashboard, Users, Projects, Tasks, Messages, Notifications, Calendar
- **Settings section**: Profile, Account, Security, Notifications, Appearance, Team, Billing, Integrations, API
- **Admin section**: User management, Roles, Logs, Audit, Configuration, Database, Monitoring, Backups
- **Public section**: Home, About, Pricing, Features, Documentation, Blog, Contact, Help

**Route interface:**

```tsx
interface Route {
  id: string;           // Unique identifier
  name: string;         // Display name
  path: string;         // URL path (can include :params)
  section: 'App' | 'Settings' | 'Admin' | 'Public';
  icon: string;         // Emoji icon
  description?: string; // Optional description
  external?: boolean;   // Opens externally
  parent?: string;      // Parent route ID for breadcrumbs
}
```

**Utility functions:**

```tsx
getBreadcrumbs(routeId: string, routes: Route[]): Route[]
getSectionLabel(section: Route['section'], routes: Route[]): string
```

## Installation & Integration

### 1. Install Dependencies

This example uses only React and standard browser APIs (no external dependencies required).

### 2. Copy Files

Copy all files from this directory into your project:

```bash
cp NavigationPalette.tsx RouteResult.tsx useRouteSearch.ts mock-routes.ts /path/to/your/components/
```

### 3. Add Tailwind Styles

Ensure your Tailwind configuration includes the necessary utilities. The palette uses:
- Color utilities: `bg-`, `text-`, `border-`
- Dark mode: `dark:` variant
- Layout: `flex`, `grid`, positioning
- Typography: `font-`, `text-` sizes

### 4. Integrate with Your Router

Replace the mock `navigate` function with your actual routing:

**React Router v6:**

```tsx
import { useNavigate } from 'react-router-dom';

// In useRouteSearch.ts, replace the navigate callback:
const reactRouterNavigate = useNavigate();

const navigate = useCallback(
  (route: Route) => {
    reactRouterNavigate(route.path);
    // ... rest of tracking logic
  },
  [reactRouterNavigate, /* other deps */]
);
```

**TanStack Router:**

```tsx
import { useRouter } from '@tanstack/react-router';

const router = useRouter();

const navigate = useCallback(
  (route: Route) => {
    router.navigate({ to: route.path });
    // ... rest of tracking logic
  },
  [router, /* other deps */]
);
```

**Next.js (App Router):**

```tsx
import { useRouter } from 'next/navigation';

const router = useRouter();

const navigate = useCallback(
  (route: Route) => {
    router.push(route.path);
    // ... rest of tracking logic
  },
  [router, /* other deps */]
);
```

### 5. Replace Mock Routes

Replace `mockRoutes` with your actual application routes:

```tsx
// routes.ts
import type { Route } from './mock-routes';

export const appRoutes: Route[] = [
  {
    id: 'dashboard',
    name: 'Dashboard',
    path: '/dashboard',
    section: 'App',
    icon: '📊',
    description: 'View your dashboard',
  },
  // ... your routes
];
```

Then import and use in the palette:

```tsx
import { appRoutes } from './routes';
import { useRouteSearch } from './useRouteSearch';

// In component:
const { routes, ... } = useRouteSearch(appRoutes);
```

## Route Registration Pattern

For dynamic applications, register routes from feature modules:

```tsx
// features/users/routes.ts
export const userRoutes: Route[] = [
  {
    id: 'users-list',
    name: 'Users',
    path: '/users',
    section: 'App',
    icon: '👥',
  },
  // ...
];

// app/routes.ts
import { userRoutes } from '@/features/users/routes';
import { projectRoutes } from '@/features/projects/routes';

export const allRoutes = [
  ...userRoutes,
  ...projectRoutes,
  // ...
];
```

## Customization Guide

### Styling

All styles use Tailwind classes. Customize by modifying class names:

**Section colors:**

```tsx
// In RouteResult.tsx
const sectionColors = {
  App: 'text-blue-600 dark:text-blue-400',
  Settings: 'text-purple-600 dark:text-purple-400',
  Admin: 'text-red-600 dark:text-red-400',
  Public: 'text-green-600 dark:text-green-400',
};
```

**Selected state:**

```tsx
// In NavigationPalette.tsx
className={`... ${
  index === selectedIndex
    ? 'bg-blue-50 dark:bg-blue-900/20'  // Change selection highlight
    : 'hover:bg-gray-50 dark:hover:bg-gray-800'
}`}
```

### Keyboard Shortcut

Change from `Cmd+Shift+P` to another key:

```tsx
// In NavigationPalette.tsx, useNavigationPalette hook
if (e.key === 'K' && (e.metaKey || e.ctrlKey)) {  // Now Cmd+K
  e.preventDefault();
  setIsOpen((prev) => !prev);
}
```

### Recent Routes Limit

Adjust the maximum number of recent routes:

```tsx
// In useRouteSearch.ts
const MAX_RECENT_ROUTES = 20;  // Change from 10 to 20
```

### Storage Keys

Customize localStorage keys to avoid conflicts:

```tsx
// In useRouteSearch.ts
const RECENT_ROUTES_KEY = 'myapp-recent-routes';
const ROUTE_FREQUENCY_KEY = 'myapp-route-frequency';
```

### Search Scoring

Adjust fuzzy search scoring weights:

```tsx
// In useRouteSearch.ts, filteredRoutes calculation
const nameScore = fuzzyScore(query, route.name);
const pathScore = fuzzyScore(query, route.path) * 0.9;  // Increase path weight
const sectionScore = fuzzyScore(query, route.section) * 0.7;  // Increase section weight
```

## Testing

Run tests with Vitest:

```bash
npm test useRouteSearch.test.ts
```

**Test coverage:**
- Route filtering by name, path, section, description
- Fuzzy matching and case insensitivity
- Recent routes tracking and persistence
- Frequency tracking and most visited calculation
- localStorage integration
- Navigation functionality

## Accessibility

The palette follows accessibility best practices:

- **Keyboard Navigation**: Arrow keys, Enter, Escape
- **ARIA Attributes**: `role="dialog"`, `aria-modal`, `role="combobox"`, `role="listbox"`, `role="option"`
- **Focus Management**: Auto-focus search input on open, focus trap within modal
- **Screen Reader Support**: Proper labels and descriptions
- **Color Contrast**: WCAG AA compliant text/background combinations
- **Reduced Motion**: Respects `prefers-reduced-motion` (add transitions conditionally)

## Performance Considerations

- **No virtualization needed**: 50-100 routes perform well without virtual scrolling
- **Memoized search**: `useMemo` prevents unnecessary recalculations
- **Debouncing**: Not needed for local search (instant filtering is better UX)
- **localStorage caching**: Recent/frequency data loaded once on mount

For 1,000+ routes, consider adding:
- Virtual scrolling with `@tanstack/react-virtual`
- Debounced search (300-500ms)
- Lazy loading of route metadata

## Browser Support

- **Modern browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **localStorage**: Required for persistence (gracefully degrades without)
- **Keyboard events**: Standard event handling (works in all modern browsers)

## License

This example is provided as part of the Command Palette Development skill. Use freely in your projects.

## Next Steps

- Integrate with your routing library
- Replace mock routes with real application routes
- Customize styling to match your design system
- Add route permissions/filtering based on user roles
- Implement deep linking (update URL when palette state changes)
- Add route previews (show page content in side panel)
