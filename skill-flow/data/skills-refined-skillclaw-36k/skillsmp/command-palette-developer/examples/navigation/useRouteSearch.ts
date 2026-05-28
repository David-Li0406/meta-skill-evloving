import { useState, useMemo, useCallback, useEffect } from 'react';
import type { Route } from './mock-routes';

const RECENT_ROUTES_KEY = 'navigation-palette-recent-routes';
const ROUTE_FREQUENCY_KEY = 'navigation-palette-route-frequency';
const MAX_RECENT_ROUTES = 10;

interface RouteFrequency {
  [routeId: string]: number;
}

interface UseRouteSearchResult {
  routes: Route[];
  recentRoutes: Route[];
  mostVisitedRoutes: Route[];
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  navigate: (route: Route) => void;
  clearRecentRoutes: () => void;
}

/**
 * Fuzzy match helper
 */
function fuzzyMatch(query: string, target: string): boolean {
  const queryLower = query.toLowerCase();
  const targetLower = target.toLowerCase();
  let queryIndex = 0;

  for (let i = 0; i < targetLower.length && queryIndex < queryLower.length; i++) {
    if (targetLower[i] === queryLower[queryIndex]) {
      queryIndex++;
    }
  }

  return queryIndex === queryLower.length;
}

/**
 * Fuzzy score for ranking
 */
function fuzzyScore(query: string, target: string): number {
  if (!query) return 0;

  const queryLower = query.toLowerCase();
  const targetLower = target.toLowerCase();

  // Exact match gets highest score
  if (targetLower === queryLower) return 1000;

  // Prefix match gets high score
  if (targetLower.startsWith(queryLower)) return 900;

  // Word boundary match
  const words = targetLower.split(/[\s/-]+/);
  for (const word of words) {
    if (word.startsWith(queryLower)) return 800;
  }

  // Fuzzy match score
  let score = 0;
  let queryIndex = 0;
  let lastMatchIndex = -1;

  for (let i = 0; i < targetLower.length && queryIndex < queryLower.length; i++) {
    if (targetLower[i] === queryLower[queryIndex]) {
      // Consecutive matches get bonus
      const gap = lastMatchIndex >= 0 ? i - lastMatchIndex : 0;
      score += gap === 1 ? 10 : 5;

      queryIndex++;
      lastMatchIndex = i;
    }
  }

  return queryIndex === queryLower.length ? score : 0;
}

/**
 * Load recent routes from localStorage
 */
function loadRecentRoutes(): string[] {
  try {
    const stored = localStorage.getItem(RECENT_ROUTES_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
}

/**
 * Save recent routes to localStorage
 */
function saveRecentRoutes(routeIds: string[]): void {
  try {
    localStorage.setItem(RECENT_ROUTES_KEY, JSON.stringify(routeIds));
  } catch {
    // Fail silently if localStorage is not available
  }
}

/**
 * Load route frequency from localStorage
 */
function loadRouteFrequency(): RouteFrequency {
  try {
    const stored = localStorage.getItem(ROUTE_FREQUENCY_KEY);
    return stored ? JSON.parse(stored) : {};
  } catch {
    return {};
  }
}

/**
 * Save route frequency to localStorage
 */
function saveRouteFrequency(frequency: RouteFrequency): void {
  try {
    localStorage.setItem(ROUTE_FREQUENCY_KEY, JSON.stringify(frequency));
  } catch {
    // Fail silently if localStorage is not available
  }
}

/**
 * Hook for route search with recent routes tracking and frequency-based suggestions
 */
export function useRouteSearch(allRoutes: Route[]): UseRouteSearchResult {
  const [searchQuery, setSearchQuery] = useState('');
  const [recentRouteIds, setRecentRouteIds] = useState<string[]>([]);
  const [routeFrequency, setRouteFrequency] = useState<RouteFrequency>({});

  // Load persisted data on mount
  useEffect(() => {
    setRecentRouteIds(loadRecentRoutes());
    setRouteFrequency(loadRouteFrequency());
  }, []);

  // Filter and score routes based on search query
  const filteredRoutes = useMemo(() => {
    if (!searchQuery.trim()) {
      return allRoutes;
    }

    const query = searchQuery.trim();

    return allRoutes
      .map((route) => {
        // Calculate scores for different fields
        const nameScore = fuzzyScore(query, route.name);
        const pathScore = fuzzyScore(query, route.path) * 0.8; // Path slightly less important
        const sectionScore = fuzzyScore(query, route.section) * 0.6;
        const descriptionScore = route.description
          ? fuzzyScore(query, route.description) * 0.4
          : 0;

        // Take the highest score
        const score = Math.max(nameScore, pathScore, sectionScore, descriptionScore);

        return { route, score };
      })
      .filter(({ score }) => score > 0)
      .sort((a, b) => {
        // Sort by score first
        if (b.score !== a.score) {
          return b.score - a.score;
        }

        // Then by frequency
        const freqA = routeFrequency[a.route.id] || 0;
        const freqB = routeFrequency[b.route.id] || 0;
        return freqB - freqA;
      })
      .map(({ route }) => route);
  }, [allRoutes, searchQuery, routeFrequency]);

  // Get recent routes (exclude non-existent routes)
  const recentRoutes = useMemo(() => {
    const routeMap = new Map(allRoutes.map((r) => [r.id, r]));
    return recentRouteIds
      .map((id) => routeMap.get(id))
      .filter((route): route is Route => route !== undefined);
  }, [allRoutes, recentRouteIds]);

  // Get most visited routes
  const mostVisitedRoutes = useMemo(() => {
    const routeMap = new Map(allRoutes.map((r) => [r.id, r]));

    return Object.entries(routeFrequency)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 10)
      .map(([id]) => routeMap.get(id))
      .filter((route): route is Route => route !== undefined);
  }, [allRoutes, routeFrequency]);

  // Navigate to a route (updates recent and frequency)
  const navigate = useCallback(
    (route: Route) => {
      // Mock navigation - in real app, use React Router's navigate()
      console.log('Navigating to:', route.path);

      // Update recent routes
      const updatedRecent = [
        route.id,
        ...recentRouteIds.filter((id) => id !== route.id),
      ].slice(0, MAX_RECENT_ROUTES);

      setRecentRouteIds(updatedRecent);
      saveRecentRoutes(updatedRecent);

      // Update frequency
      const updatedFrequency = {
        ...routeFrequency,
        [route.id]: (routeFrequency[route.id] || 0) + 1,
      };

      setRouteFrequency(updatedFrequency);
      saveRouteFrequency(updatedFrequency);
    },
    [recentRouteIds, routeFrequency]
  );

  // Clear recent routes
  const clearRecentRoutes = useCallback(() => {
    setRecentRouteIds([]);
    saveRecentRoutes([]);
  }, []);

  return {
    routes: filteredRoutes,
    recentRoutes,
    mostVisitedRoutes,
    searchQuery,
    setSearchQuery,
    navigate,
    clearRecentRoutes,
  };
}
