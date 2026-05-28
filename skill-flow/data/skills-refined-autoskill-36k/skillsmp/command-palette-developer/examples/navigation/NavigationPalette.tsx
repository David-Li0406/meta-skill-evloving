import { useState, useEffect, useRef } from 'react';
import { RouteResult } from './RouteResult';
import { mockRoutes } from './mock-routes';
import { useRouteSearch } from './useRouteSearch';
import type { Route } from './mock-routes';

interface NavigationPaletteProps {
  isOpen: boolean;
  onClose: () => void;
}

/**
 * Navigation palette for route/page discovery with search history and frequency tracking
 *
 * Features:
 * - Modal overlay with backdrop (Cmd+Shift+P)
 * - Fuzzy search through routes
 * - Recently visited routes section
 * - Most visited routes tracking
 * - Route grouping by section
 * - Breadcrumb display for nested routes
 * - External link indication
 * - Keyboard navigation (arrow keys, enter, escape)
 */
export function NavigationPalette({ isOpen, onClose }: NavigationPaletteProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [selectedIndex, setSelectedIndex] = useState(0);

  const {
    routes,
    recentRoutes,
    mostVisitedRoutes,
    searchQuery,
    setSearchQuery,
    navigate,
    clearRecentRoutes,
  } = useRouteSearch(mockRoutes);

  // Group routes by section when not searching
  const groupedRoutes =
    searchQuery.trim() === ''
      ? mockRoutes.reduce(
          (acc, route) => {
            if (!acc[route.section]) {
              acc[route.section] = [];
            }
            acc[route.section].push(route);
            return acc;
          },
          {} as Record<Route['section'], Route[]>
        )
      : null;

  // Determine what to show
  const showRecent = !searchQuery.trim() && recentRoutes.length > 0;
  const showMostVisited =
    !searchQuery.trim() && !showRecent && mostVisitedRoutes.length > 0;
  const showGrouped = !searchQuery.trim() && !showRecent && !showMostVisited;
  const showFiltered = searchQuery.trim() !== '';

  // Get total visible routes for keyboard navigation
  const visibleRoutes = showFiltered ? routes : mockRoutes;

  // Reset selection when routes change
  useEffect(() => {
    setSelectedIndex(0);
  }, [searchQuery, routes]);

  // Focus input when opened
  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
      setSearchQuery('');
      setSelectedIndex(0);
    }
  }, [isOpen, setSearchQuery]);

  // Keyboard navigation
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setSelectedIndex((prev) => (prev + 1) % visibleRoutes.length);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setSelectedIndex(
          (prev) => (prev - 1 + visibleRoutes.length) % visibleRoutes.length
        );
      } else if (e.key === 'Enter') {
        e.preventDefault();
        const selectedRoute = visibleRoutes[selectedIndex];
        if (selectedRoute) {
          navigate(selectedRoute);
          onClose();
        }
      } else if (e.key === 'Escape') {
        e.preventDefault();
        onClose();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, selectedIndex, visibleRoutes, navigate, onClose]);

  // Handle route selection
  const handleSelectRoute = (route: Route) => {
    navigate(route);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Modal */}
      <div
        className="fixed inset-0 z-50 flex items-start justify-center pt-[20vh] px-4"
        role="dialog"
        aria-modal="true"
        aria-label="Navigation Palette"
      >
        <div className="bg-white dark:bg-gray-900 rounded-lg shadow-2xl w-full max-w-2xl overflow-hidden border border-gray-200 dark:border-gray-700">
          {/* Search input */}
          <div className="flex items-center gap-3 px-4 py-3 border-b border-gray-200 dark:border-gray-700">
            <span className="text-gray-400" aria-hidden="true">
              🔍
            </span>
            <input
              ref={inputRef}
              type="text"
              className="flex-1 bg-transparent border-none outline-none text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500"
              placeholder="Search routes or type a path..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              role="combobox"
              aria-expanded="true"
              aria-controls="routes-list"
              aria-activedescendant={`route-${selectedIndex}`}
            />
            {searchQuery && (
              <button
                type="button"
                onClick={() => setSearchQuery('')}
                className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                aria-label="Clear search"
              >
                ✕
              </button>
            )}
          </div>

          {/* Results */}
          <div
            className="max-h-[60vh] overflow-y-auto"
            id="routes-list"
            role="listbox"
          >
            {/* Recent routes section */}
            {showRecent && (
              <div>
                <div className="flex items-center justify-between px-4 py-2 bg-gray-50 dark:bg-gray-800 sticky top-0">
                  <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Recently Visited
                  </h3>
                  <button
                    type="button"
                    onClick={clearRecentRoutes}
                    className="text-xs text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                  >
                    Clear
                  </button>
                </div>
                {recentRoutes.map((route, index) => (
                  <button
                    key={route.id}
                    type="button"
                    id={`route-${index}`}
                    role="option"
                    aria-selected={index === selectedIndex}
                    className={`w-full text-left transition-colors ${
                      index === selectedIndex
                        ? 'bg-blue-50 dark:bg-blue-900/20'
                        : 'hover:bg-gray-50 dark:hover:bg-gray-800'
                    }`}
                    onClick={() => handleSelectRoute(route)}
                    onMouseEnter={() => setSelectedIndex(index)}
                  >
                    <RouteResult route={route} isRecent searchQuery={searchQuery} />
                  </button>
                ))}
              </div>
            )}

            {/* Most visited routes section */}
            {showMostVisited && (
              <div>
                <div className="px-4 py-2 bg-gray-50 dark:bg-gray-800 sticky top-0">
                  <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Most Visited
                  </h3>
                </div>
                {mostVisitedRoutes.map((route, index) => (
                  <button
                    key={route.id}
                    type="button"
                    id={`route-${index}`}
                    role="option"
                    aria-selected={index === selectedIndex}
                    className={`w-full text-left transition-colors ${
                      index === selectedIndex
                        ? 'bg-blue-50 dark:bg-blue-900/20'
                        : 'hover:bg-gray-50 dark:hover:bg-gray-800'
                    }`}
                    onClick={() => handleSelectRoute(route)}
                    onMouseEnter={() => setSelectedIndex(index)}
                  >
                    <RouteResult route={route} searchQuery={searchQuery} />
                  </button>
                ))}
              </div>
            )}

            {/* Grouped routes (when no search query) */}
            {showGrouped &&
              groupedRoutes &&
              (['App', 'Settings', 'Admin', 'Public'] as const).map((section) => {
                const sectionRoutes = groupedRoutes[section] || [];
                if (sectionRoutes.length === 0) return null;

                return (
                  <div key={section}>
                    <div className="px-4 py-2 bg-gray-50 dark:bg-gray-800 sticky top-0">
                      <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                        {section} ({sectionRoutes.length})
                      </h3>
                    </div>
                    {sectionRoutes.map((route) => {
                      const routeIndex = mockRoutes.findIndex((r) => r.id === route.id);
                      return (
                        <button
                          key={route.id}
                          type="button"
                          id={`route-${routeIndex}`}
                          role="option"
                          aria-selected={routeIndex === selectedIndex}
                          className={`w-full text-left transition-colors ${
                            routeIndex === selectedIndex
                              ? 'bg-blue-50 dark:bg-blue-900/20'
                              : 'hover:bg-gray-50 dark:hover:bg-gray-800'
                          }`}
                          onClick={() => handleSelectRoute(route)}
                          onMouseEnter={() => setSelectedIndex(routeIndex)}
                        >
                          <RouteResult route={route} searchQuery={searchQuery} />
                        </button>
                      );
                    })}
                  </div>
                );
              })}

            {/* Filtered routes (when searching) */}
            {showFiltered && routes.length > 0 && (
              <div>
                <div className="px-4 py-2 bg-gray-50 dark:bg-gray-800 sticky top-0">
                  <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    {routes.length} {routes.length === 1 ? 'Result' : 'Results'}
                  </h3>
                </div>
                {routes.map((route, index) => (
                  <button
                    key={route.id}
                    type="button"
                    id={`route-${index}`}
                    role="option"
                    aria-selected={index === selectedIndex}
                    className={`w-full text-left transition-colors ${
                      index === selectedIndex
                        ? 'bg-blue-50 dark:bg-blue-900/20'
                        : 'hover:bg-gray-50 dark:hover:bg-gray-800'
                    }`}
                    onClick={() => handleSelectRoute(route)}
                    onMouseEnter={() => setSelectedIndex(index)}
                  >
                    <RouteResult route={route} searchQuery={searchQuery} />
                  </button>
                ))}
              </div>
            )}

            {/* No results */}
            {showFiltered && routes.length === 0 && (
              <div className="px-4 py-12 text-center text-gray-500 dark:text-gray-400">
                <div className="text-4xl mb-3">🔍</div>
                <p className="font-medium">No routes found</p>
                <p className="text-sm mt-1">Try a different search term</p>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="px-4 py-2 bg-gray-50 dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
            <div className="flex items-center gap-4">
              <span>
                <kbd className="px-1.5 py-0.5 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded text-xs">
                  ↑↓
                </kbd>{' '}
                Navigate
              </span>
              <span>
                <kbd className="px-1.5 py-0.5 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded text-xs">
                  ↵
                </kbd>{' '}
                Select
              </span>
              <span>
                <kbd className="px-1.5 py-0.5 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded text-xs">
                  Esc
                </kbd>{' '}
                Close
              </span>
            </div>
            <span className="text-gray-400">
              {visibleRoutes.length} routes available
            </span>
          </div>
        </div>
      </div>
    </>
  );
}

/**
 * Hook to manage navigation palette state
 */
export function useNavigationPalette() {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Cmd+Shift+P or Ctrl+Shift+P
      if (e.key === 'P' && (e.metaKey || e.ctrlKey) && e.shiftKey) {
        e.preventDefault();
        setIsOpen((prev) => !prev);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  return {
    isOpen,
    open: () => setIsOpen(true),
    close: () => setIsOpen(false),
    toggle: () => setIsOpen((prev) => !prev),
  };
}
