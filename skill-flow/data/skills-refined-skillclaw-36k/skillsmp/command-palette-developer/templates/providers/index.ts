/**
 * Provider components index
 *
 * Barrel export for all provider components and hooks.
 */

export {
  useCommandStore,
  useCommandPalette,
  useCommandRegistry,
  useCommands,
  useGroupedCommands,
  useRecentCommands,
  useFavoriteCommands,
  useCommandStack,
  useSearchState,
  useSelectionState,
  type Command,
} from './CommandProvider';

export {
  ThemeProvider,
  useTheme,
  useThemeStore,
  useSystemTheme,
  useReducedMotion,
  useHighContrast,
  getThemeScript,
  type Theme,
  type ResolvedTheme,
} from './ThemeProvider';

export {
  SearchProvider,
  useSearchHistory,
  useSearchQuery,
  useFilteredSearchHistory,
  useSearchSuggestions,
  useSearchSession,
  useSearchStore,
} from './SearchProvider';
