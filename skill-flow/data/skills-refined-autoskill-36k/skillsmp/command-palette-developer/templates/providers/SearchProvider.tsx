/**
 * SearchProvider - Search history management
 *
 * Features:
 * - Search history tracking
 * - Max history: 10 items
 * - Deduplicate history
 * - Persist to localStorage
 * - Clear history functionality
 *
 * @example
 * ```tsx
 * // In App.tsx
 * import { SearchProvider } from './providers/SearchProvider';
 *
 * function App() {
 *   return (
 *     <SearchProvider>
 *       <YourApp />
 *     </SearchProvider>
 *   );
 * }
 *
 * // In any component
 * const { history, addToHistory, clearHistory } = useSearchHistory();
 * ```
 */

import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface SearchState {
  // State
  history: string[];
  currentQuery: string;

  // Actions
  addToHistory: (query: string) => void;
  removeFromHistory: (query: string) => void;
  clearHistory: () => void;
  setQuery: (query: string) => void;

  // Computed
  getFilteredHistory: (query: string) => string[];
}

const MAX_HISTORY_LENGTH = 10;

/**
 * Search history Zustand store
 */
export const useSearchStore = create<SearchState>()(
  devtools(
    persist(
      (set, get) => ({
        // Initial state
        history: [],
        currentQuery: '',

        // Actions
        addToHistory: (query) => {
          const trimmed = query.trim();

          // Don't add empty queries
          if (!trimmed) return;

          // Don't add queries shorter than 2 characters
          if (trimmed.length < 2) return;

          set((state) => {
            // Remove if already in history (to move to front)
            const filtered = state.history.filter((item) => item !== trimmed);

            // Add to front and limit to MAX_HISTORY_LENGTH
            return {
              history: [trimmed, ...filtered].slice(0, MAX_HISTORY_LENGTH),
            };
          });
        },

        removeFromHistory: (query) =>
          set((state) => ({
            history: state.history.filter((item) => item !== query),
          })),

        clearHistory: () => set({ history: [] }),

        setQuery: (query) => set({ currentQuery: query }),

        // Computed
        getFilteredHistory: (query) => {
          const { history } = get();

          if (!query) return history;

          const lowercaseQuery = query.toLowerCase();
          return history.filter((item) =>
            item.toLowerCase().includes(lowercaseQuery)
          );
        },
      }),
      {
        name: 'search-history-storage',
        partialize: (state) => ({
          history: state.history,
        }),
      }
    ),
    { name: 'SearchHistory' }
  )
);

/**
 * Hook for search history
 */
export function useSearchHistory() {
  return {
    history: useSearchStore((state) => state.history),
    currentQuery: useSearchStore((state) => state.currentQuery),
    addToHistory: useSearchStore((state) => state.addToHistory),
    removeFromHistory: useSearchStore((state) => state.removeFromHistory),
    clearHistory: useSearchStore((state) => state.clearHistory),
    setQuery: useSearchStore((state) => state.setQuery),
    getFilteredHistory: useSearchStore((state) => state.getFilteredHistory),
  };
}

/**
 * Hook for current query state
 */
export function useSearchQuery() {
  return {
    query: useSearchStore((state) => state.currentQuery),
    setQuery: useSearchStore((state) => state.setQuery),
  };
}

/**
 * Hook for filtered history based on current query
 */
export function useFilteredSearchHistory(query: string) {
  return useSearchStore((state) => state.getFilteredHistory(query));
}

/**
 * SearchProvider component for context initialization
 */
export function SearchProvider({ children }: { children: React.ReactNode }): JSX.Element {
  return <>{children}</>;
}

/**
 * Hook for search suggestions (combines history with autocomplete)
 */
export function useSearchSuggestions(query: string, suggestions: string[] = []): string[] {
  const history = useFilteredSearchHistory(query);

  // Combine history and suggestions, prioritizing history
  const combined = [...new Set([...history, ...suggestions])];

  // Filter by query
  if (!query) return combined.slice(0, 5);

  const lowercaseQuery = query.toLowerCase();
  return combined
    .filter((item) => item.toLowerCase().includes(lowercaseQuery))
    .slice(0, 5);
}

/**
 * Hook for managing search session
 */
export function useSearchSession() {
  const { query, setQuery, addToHistory } = useSearchHistory();

  const startSearch = (initialQuery: string = '') => {
    setQuery(initialQuery);
  };

  const executeSearch = (searchQuery: string) => {
    addToHistory(searchQuery);
  };

  const clearSearch = () => {
    setQuery('');
  };

  return {
    query,
    startSearch,
    executeSearch,
    clearSearch,
  };
}
