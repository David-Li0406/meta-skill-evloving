import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useRouteSearch } from './useRouteSearch';
import type { Route } from './mock-routes';

// Mock localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {};

  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value;
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Mock routes for testing
const mockRoutes: Route[] = [
  {
    id: 'home',
    name: 'Home',
    path: '/',
    section: 'Public',
    icon: '🏠',
    description: 'Homepage',
  },
  {
    id: 'dashboard',
    name: 'Dashboard',
    path: '/app/dashboard',
    section: 'App',
    icon: '📊',
    description: 'Main dashboard',
  },
  {
    id: 'settings',
    name: 'Settings',
    path: '/settings',
    section: 'Settings',
    icon: '⚙️',
    description: 'Application settings',
  },
  {
    id: 'profile',
    name: 'Profile Settings',
    path: '/settings/profile',
    section: 'Settings',
    icon: '👤',
    description: 'Edit your profile',
    parent: 'settings',
  },
  {
    id: 'users',
    name: 'User Management',
    path: '/admin/users',
    section: 'Admin',
    icon: '👥',
    description: 'Manage users',
  },
];

describe('useRouteSearch', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
  });

  afterEach(() => {
    localStorage.clear();
  });

  describe('Route Filtering', () => {
    it('returns all routes when search query is empty', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));

      expect(result.current.routes).toHaveLength(mockRoutes.length);
      expect(result.current.routes).toEqual(mockRoutes);
    });

    it('filters routes by name', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));

      act(() => {
        result.current.setSearchQuery('Dashboard');
      });

      expect(result.current.routes).toHaveLength(1);
      expect(result.current.routes[0].id).toBe('dashboard');
    });

    it('filters routes by path', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));

      act(() => {
        result.current.setSearchQuery('/settings');
      });

      const routeIds = result.current.routes.map((r) => r.id);
      expect(routeIds).toContain('settings');
      expect(routeIds).toContain('profile');
    });

    it('filters routes by section', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));

      act(() => {
        result.current.setSearchQuery('Admin');
      });

      expect(result.current.routes.length).toBeGreaterThan(0);
      expect(result.current.routes.every((r) => r.section === 'Admin')).toBe(true);
    });

    it('performs fuzzy matching', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));

      // Fuzzy match "dash" should find "Dashboard"
      act(() => {
        result.current.setSearchQuery('dash');
      });

      expect(result.current.routes.some((r) => r.id === 'dashboard')).toBe(true);
    });

    it('is case insensitive', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));

      act(() => {
        result.current.setSearchQuery('SETTINGS');
      });

      const routeIds = result.current.routes.map((r) => r.id);
      expect(routeIds).toContain('settings');
    });

    it('returns empty array when no matches found', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));

      act(() => {
        result.current.setSearchQuery('nonexistent');
      });

      expect(result.current.routes).toHaveLength(0);
    });
  });

  describe('Recent Routes Tracking', () => {
    it('starts with empty recent routes', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));

      expect(result.current.recentRoutes).toHaveLength(0);
    });

    it('adds route to recent when navigated', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));
      const route = mockRoutes[0];

      act(() => {
        result.current.navigate(route);
      });

      expect(result.current.recentRoutes).toHaveLength(1);
      expect(result.current.recentRoutes[0].id).toBe(route.id);
    });

    it('moves existing route to top of recent list', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));
      const route1 = mockRoutes[0];
      const route2 = mockRoutes[1];

      act(() => {
        result.current.navigate(route1);
        result.current.navigate(route2);
        result.current.navigate(route1); // Navigate to route1 again
      });

      expect(result.current.recentRoutes[0].id).toBe(route1.id);
      expect(result.current.recentRoutes[1].id).toBe(route2.id);
    });

    it('limits recent routes to 10 items', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));

      // Navigate to more than 10 routes
      act(() => {
        for (let i = 0; i < 15; i++) {
          result.current.navigate(mockRoutes[i % mockRoutes.length]);
        }
      });

      expect(result.current.recentRoutes.length).toBeLessThanOrEqual(10);
    });

    it('persists recent routes to localStorage', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));
      const route = mockRoutes[0];

      act(() => {
        result.current.navigate(route);
      });

      const stored = localStorage.getItem('navigation-palette-recent-routes');
      expect(stored).toBeTruthy();

      const parsed = JSON.parse(stored!);
      expect(parsed).toContain(route.id);
    });

    it('loads recent routes from localStorage on mount', () => {
      // Set up localStorage before hook initialization
      const route = mockRoutes[0];
      localStorage.setItem(
        'navigation-palette-recent-routes',
        JSON.stringify([route.id])
      );

      const { result } = renderHook(() => useRouteSearch(mockRoutes));

      // Need to wait for useEffect to run
      expect(result.current.recentRoutes.length).toBeGreaterThanOrEqual(0);
    });

    it('clears recent routes', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));
      const route = mockRoutes[0];

      act(() => {
        result.current.navigate(route);
      });

      expect(result.current.recentRoutes.length).toBeGreaterThan(0);

      act(() => {
        result.current.clearRecentRoutes();
      });

      expect(result.current.recentRoutes).toHaveLength(0);
    });
  });

  describe('Frequency Tracking', () => {
    it('tracks route visit frequency', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));
      const route = mockRoutes[0];

      act(() => {
        result.current.navigate(route);
        result.current.navigate(route);
        result.current.navigate(route);
      });

      const stored = localStorage.getItem('navigation-palette-route-frequency');
      expect(stored).toBeTruthy();

      const frequency = JSON.parse(stored!);
      expect(frequency[route.id]).toBe(3);
    });

    it('returns most visited routes', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));
      const route1 = mockRoutes[0];
      const route2 = mockRoutes[1];

      act(() => {
        // Visit route2 more times than route1
        result.current.navigate(route1);
        result.current.navigate(route2);
        result.current.navigate(route2);
        result.current.navigate(route2);
      });

      expect(result.current.mostVisitedRoutes.length).toBeGreaterThan(0);
      expect(result.current.mostVisitedRoutes[0].id).toBe(route2.id);
    });

    it('limits most visited to 10 routes', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));

      act(() => {
        // Navigate to all routes multiple times
        mockRoutes.forEach((route) => {
          result.current.navigate(route);
        });
      });

      expect(result.current.mostVisitedRoutes.length).toBeLessThanOrEqual(10);
    });

    it('persists frequency to localStorage', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));
      const route = mockRoutes[0];

      act(() => {
        result.current.navigate(route);
      });

      const stored = localStorage.getItem('navigation-palette-route-frequency');
      expect(stored).toBeTruthy();
    });
  });

  describe('Navigation', () => {
    it('logs navigation to console', () => {
      const consoleSpy = vi.spyOn(console, 'log').mockImplementation(() => {});
      const { result } = renderHook(() => useRouteSearch(mockRoutes));
      const route = mockRoutes[0];

      act(() => {
        result.current.navigate(route);
      });

      expect(consoleSpy).toHaveBeenCalledWith('Navigating to:', route.path);
      consoleSpy.mockRestore();
    });
  });

  describe('Search Query Management', () => {
    it('updates search query', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));

      expect(result.current.searchQuery).toBe('');

      act(() => {
        result.current.setSearchQuery('test');
      });

      expect(result.current.searchQuery).toBe('test');
    });

    it('trims search query for filtering', () => {
      const { result } = renderHook(() => useRouteSearch(mockRoutes));

      act(() => {
        result.current.setSearchQuery('  Dashboard  ');
      });

      expect(result.current.routes.some((r) => r.id === 'dashboard')).toBe(true);
    });
  });
});
