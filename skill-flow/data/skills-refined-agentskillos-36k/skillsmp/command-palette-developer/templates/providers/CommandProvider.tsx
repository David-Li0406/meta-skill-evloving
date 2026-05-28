/**
 * CommandProvider - Zustand store for command palette state
 *
 * Features:
 * - Command registry: register/unregister commands dynamically
 * - Grouped commands by category
 * - Recent commands tracking (localStorage)
 * - Multi-step command stack
 * - Search query management
 * - Selection state
 *
 * @example
 * ```tsx
 * // In App.tsx
 * import { CommandProvider } from './providers/CommandProvider';
 *
 * function App() {
 *   return (
 *     <CommandProvider>
 *       <YourApp />
 *     </CommandProvider>
 *   );
 * }
 *
 * // In any component
 * const { isOpen, setOpen } = useCommandStore();
 * const commands = useCommands();
 * const recentCommands = useRecentCommands();
 * ```
 */

import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

export interface Command {
  id: string;
  label: string;
  description?: string;
  keywords: string[];
  icon?: React.ComponentType;
  shortcut?: string;
  group?: string;
  onSelect: () => void | Promise<void>;
}

interface CommandPaletteState {
  // Visibility
  isOpen: boolean;
  setOpen: (open: boolean) => void;
  toggle: () => void;

  // Search
  searchQuery: string;
  setSearchQuery: (query: string) => void;

  // Selection
  selectedId: string | null;
  setSelectedId: (id: string | null) => void;

  // Commands
  commands: Command[];
  registerCommand: (command: Command) => void;
  unregisterCommand: (id: string) => void;
  registerMultiple: (commands: Command[]) => void;
  clearCommands: () => void;

  // History
  recentCommands: string[]; // Command IDs
  addToRecent: (id: string) => void;
  clearRecent: () => void;

  // Favorites
  favorites: string[]; // Command IDs
  toggleFavorite: (id: string) => void;

  // Multi-step
  commandStack: Command[];
  pushCommand: (command: Command) => void;
  popCommand: () => void;
  clearStack: () => void;

  // Computed selectors
  filteredCommands: () => Command[];
  groupedCommands: () => Record<string, Command[]>;
  getRecentCommandsData: () => Command[];
  getFavoriteCommandsData: () => Command[];
}

/**
 * Command palette Zustand store
 */
export const useCommandStore = create<CommandPaletteState>()(
  devtools(
    persist(
      (set, get) => ({
        // Initial state
        isOpen: false,
        searchQuery: '',
        selectedId: null,
        commands: [],
        recentCommands: [],
        favorites: [],
        commandStack: [],

        // Actions
        setOpen: (open) => set({ isOpen: open }),
        toggle: () => set((state) => ({ isOpen: !state.isOpen })),

        setSearchQuery: (query) => set({ searchQuery: query, selectedId: null }),

        setSelectedId: (id) => set({ selectedId: id }),

        registerCommand: (command) =>
          set((state) => {
            // Prevent duplicates
            const exists = state.commands.some((cmd) => cmd.id === command.id);
            if (exists) {
              console.warn(`Command with id "${command.id}" already exists`);
              return state;
            }
            return {
              commands: [...state.commands, command],
            };
          }),

        unregisterCommand: (id) =>
          set((state) => ({
            commands: state.commands.filter((cmd) => cmd.id !== id),
          })),

        registerMultiple: (commands) =>
          set((state) => {
            // Filter out duplicates
            const existingIds = new Set(state.commands.map((cmd) => cmd.id));
            const newCommands = commands.filter((cmd) => !existingIds.has(cmd.id));
            return {
              commands: [...state.commands, ...newCommands],
            };
          }),

        clearCommands: () => set({ commands: [] }),

        addToRecent: (id) =>
          set((state) => {
            // Remove if already in recent, then add to front
            const filtered = state.recentCommands.filter((cmdId) => cmdId !== id);
            return {
              recentCommands: [id, ...filtered].slice(0, 10), // Keep last 10
            };
          }),

        clearRecent: () => set({ recentCommands: [] }),

        toggleFavorite: (id) =>
          set((state) => ({
            favorites: state.favorites.includes(id)
              ? state.favorites.filter((fav) => fav !== id)
              : [...state.favorites, id],
          })),

        pushCommand: (command) =>
          set((state) => ({
            commandStack: [...state.commandStack, command],
            searchQuery: '', // Reset search
            selectedId: null,
          })),

        popCommand: () =>
          set((state) => ({
            commandStack: state.commandStack.slice(0, -1),
            searchQuery: '',
            selectedId: null,
          })),

        clearStack: () => set({ commandStack: [], searchQuery: '', selectedId: null }),

        // Computed selectors
        filteredCommands: () => {
          const { commands, searchQuery, favorites, recentCommands } = get();

          if (!searchQuery) {
            return commands;
          }

          const query = searchQuery.toLowerCase();
          return commands
            .filter((cmd) => {
              const labelMatch = cmd.label.toLowerCase().includes(query);
              const descriptionMatch = cmd.description?.toLowerCase().includes(query);
              const keywordMatch = cmd.keywords.some((kw) =>
                kw.toLowerCase().includes(query)
              );
              return labelMatch || descriptionMatch || keywordMatch;
            })
            .sort((a, b) => {
              // Sort: favorites first, then recent, then alphabetical
              const aFav = favorites.includes(a.id);
              const bFav = favorites.includes(b.id);
              if (aFav && !bFav) return -1;
              if (!aFav && bFav) return 1;

              const aRecent = recentCommands.indexOf(a.id);
              const bRecent = recentCommands.indexOf(b.id);
              if (aRecent !== -1 && bRecent === -1) return -1;
              if (aRecent === -1 && bRecent !== -1) return 1;
              if (aRecent !== -1 && bRecent !== -1) return aRecent - bRecent;

              // Exact match comes first
              const aExact = a.label.toLowerCase() === query;
              const bExact = b.label.toLowerCase() === query;
              if (aExact && !bExact) return -1;
              if (!aExact && bExact) return 1;

              return a.label.localeCompare(b.label);
            });
        },

        groupedCommands: () => {
          const commands = get().filteredCommands();
          return commands.reduce((groups, cmd) => {
            const group = cmd.group || 'Other';
            if (!groups[group]) groups[group] = [];
            groups[group].push(cmd);
            return groups;
          }, {} as Record<string, Command[]>);
        },

        getRecentCommandsData: () => {
          const { commands, recentCommands } = get();
          return recentCommands
            .map((id) => commands.find((cmd) => cmd.id === id))
            .filter(Boolean) as Command[];
        },

        getFavoriteCommandsData: () => {
          const { commands, favorites } = get();
          return favorites
            .map((id) => commands.find((cmd) => cmd.id === id))
            .filter(Boolean) as Command[];
        },
      }),
      {
        name: 'command-palette-storage',
        partialize: (state) => ({
          // Only persist these fields
          recentCommands: state.recentCommands,
          favorites: state.favorites,
        }),
      }
    ),
    { name: 'CommandPalette' }
  )
);

/**
 * Hook for command palette visibility
 */
export function useCommandPalette() {
  return {
    isOpen: useCommandStore((state) => state.isOpen),
    setOpen: useCommandStore((state) => state.setOpen),
    toggle: useCommandStore((state) => state.toggle),
  };
}

/**
 * Hook for command registry
 */
export function useCommandRegistry() {
  return {
    register: useCommandStore((state) => state.registerCommand),
    unregister: useCommandStore((state) => state.unregisterCommand),
    registerMultiple: useCommandStore((state) => state.registerMultiple),
    clear: useCommandStore((state) => state.clearCommands),
  };
}

/**
 * Hook for filtered commands
 */
export function useCommands() {
  return useCommandStore((state) => state.filteredCommands());
}

/**
 * Hook for grouped commands
 */
export function useGroupedCommands() {
  return useCommandStore((state) => state.groupedCommands());
}

/**
 * Hook for recent commands
 */
export function useRecentCommands() {
  return {
    recent: useCommandStore((state) => state.getRecentCommandsData()),
    addToRecent: useCommandStore((state) => state.addToRecent),
    clearRecent: useCommandStore((state) => state.clearRecent),
  };
}

/**
 * Hook for favorite commands
 */
export function useFavoriteCommands() {
  return {
    favorites: useCommandStore((state) => state.getFavoriteCommandsData()),
    toggleFavorite: useCommandStore((state) => state.toggleFavorite),
    isFavorite: (id: string) => useCommandStore((state) => state.favorites.includes(id)),
  };
}

/**
 * Hook for command stack (multi-step commands)
 */
export function useCommandStack() {
  return {
    stack: useCommandStore((state) => state.commandStack),
    push: useCommandStore((state) => state.pushCommand),
    pop: useCommandStore((state) => state.popCommand),
    clear: useCommandStore((state) => state.clearStack),
    depth: useCommandStore((state) => state.commandStack.length),
  };
}

/**
 * Hook for search state
 */
export function useSearchState() {
  return {
    query: useCommandStore((state) => state.searchQuery),
    setQuery: useCommandStore((state) => state.setSearchQuery),
  };
}

/**
 * Hook for selection state
 */
export function useSelectionState() {
  return {
    selectedId: useCommandStore((state) => state.selectedId),
    setSelectedId: useCommandStore((state) => state.setSelectedId),
  };
}
