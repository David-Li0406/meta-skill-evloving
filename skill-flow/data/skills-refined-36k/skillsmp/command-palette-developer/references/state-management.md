# State Management with Zustand

Command palette state management patterns using Zustand for UI state and Tanstack Query for server state.

## Why Zustand

- **Lightweight:** ~1KB minzipped
- **No boilerplate:** No providers, actions, reducers
- **TypeScript-first:** Excellent type inference
- **Devtools:** Redux DevTools integration
- **React-agnostic:** Works outside components

## Command Palette Store

```typescript
// providers/CommandProvider.tsx
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';

interface Command {
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

  // Computed
  filteredCommands: () => Command[];
  groupedCommands: () => Record<string, Command[]>;
}

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

        setSearchQuery: (query) => set({ searchQuery: query }),

        setSelectedId: (id) => set({ selectedId: id }),

        registerCommand: (command) =>
          set((state) => ({
            commands: [...state.commands, command],
          })),

        unregisterCommand: (id) =>
          set((state) => ({
            commands: state.commands.filter((cmd) => cmd.id !== id),
          })),

        registerMultiple: (commands) =>
          set((state) => ({
            commands: [...state.commands, ...commands],
          })),

        addToRecent: (id) =>
          set((state) => {
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
          })),

        popCommand: () =>
          set((state) => ({
            commandStack: state.commandStack.slice(0, -1),
            searchQuery: '',
          })),

        clearStack: () => set({ commandStack: [] }),

        // Computed selectors
        filteredCommands: () => {
          const { commands, searchQuery, favorites, recentCommands } = get();
          if (!searchQuery) return commands;

          const query = searchQuery.toLowerCase();
          return commands
            .filter((cmd) => {
              const labelMatch = cmd.label.toLowerCase().includes(query);
              const keywordMatch = cmd.keywords.some((kw) =>
                kw.toLowerCase().includes(query)
              );
              return labelMatch || keywordMatch;
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
      }),
      {
        name: 'command-palette-storage',
        partialize: (state) => ({
          // Only persist these fields
          recentCommands: state.recentCommands,
          favorites: state.favorites,
        }),
      }
    )
  )
);

// Convenience hooks
export function useCommandPalette() {
  return {
    isOpen: useCommandStore((state) => state.isOpen),
    setOpen: useCommandStore((state) => state.setOpen),
    toggle: useCommandStore((state) => state.toggle),
  };
}

export function useCommandRegistry() {
  return {
    register: useCommandStore((state) => state.registerCommand),
    unregister: useCommandStore((state) => state.unregisterCommand),
    registerMultiple: useCommandStore((state) => state.registerMultiple),
  };
}

export function useCommands() {
  return useCommandStore((state) => state.filteredCommands());
}

export function useGroupedCommands() {
  return useCommandStore((state) => state.groupedCommands());
}
```

## Using the Store

### Registering Commands

```typescript
function MyFeature() {
  const registry = useCommandRegistry();

  useEffect(() => {
    const commands: Command[] = [
      {
        id: 'create-task',
        label: 'Create Task',
        keywords: ['new', 'task', 'add'],
        icon: PlusIcon,
        shortcut: 'command+n',
        group: 'Actions',
        onSelect: () => navigate('/tasks/new'),
      },
      {
        id: 'view-dashboard',
        label: 'View Dashboard',
        keywords: ['home', 'dashboard', 'overview'],
        shortcut: 'g then d',
        group: 'Navigation',
        onSelect: () => navigate('/'),
      },
    ];

    registry.registerMultiple(commands);

    // Cleanup on unmount
    return () => {
      commands.forEach((cmd) => registry.unregister(cmd.id));
    };
  }, [registry]);

  return <div>Feature content</div>;
}
```

### Opening/Closing Palette

```typescript
function App() {
  const { isOpen, toggle } = useCommandPalette();

  useKeyboardShortcut('command+k', toggle);

  return (
    <>
      <button onClick={toggle}>Open Palette</button>
      {isOpen && <CommandPalette />}
    </>
  );
}
```

### Rendering Commands

```typescript
function CommandList() {
  const groupedCommands = useGroupedCommands();
  const selectedId = useCommandStore((state) => state.selectedId);
  const setSelectedId = useCommandStore((state) => state.setSelectedId);

  return (
    <Command.List>
      {Object.entries(groupedCommands).map(([group, commands]) => (
        <Command.Group key={group} heading={group}>
          {commands.map((cmd) => (
            <Command.Item
              key={cmd.id}
              value={cmd.id}
              onSelect={() => {
                cmd.onSelect();
                useCommandStore.getState().addToRecent(cmd.id);
                useCommandStore.getState().setOpen(false);
              }}
            >
              {cmd.icon && <cmd.icon />}
              <span>{cmd.label}</span>
              {cmd.shortcut && <Shortcut keys={cmd.shortcut} />}
            </Command.Item>
          ))}
        </Command.Group>
      ))}
    </Command.List>
  );
}
```

## Integrating Tanstack Query

For server-side search and data fetching, use Tanstack Query alongside Zustand:

```typescript
// hooks/useServerSearch.ts
import { useQuery } from '@tanstack/react-query';
import { useCommandStore } from '../providers/CommandProvider';

export function useServerSearch() {
  const searchQuery = useCommandStore((state) => state.searchQuery);

  return useQuery({
    queryKey: ['command-search', searchQuery],
    queryFn: async () => {
      if (!searchQuery) return [];
      const response = await fetch(`/api/search?q=${searchQuery}`);
      return response.json();
    },
    enabled: searchQuery.length > 2, // Only search when 3+ characters
    staleTime: 5 * 60 * 1000, // Cache for 5 minutes
  });
}

// Usage in component
function ServerSearchResults() {
  const { data: results, isLoading } = useServerSearch();

  if (isLoading) return <Command.Loading>Searching...</Command.Loading>;

  return (
    <Command.Group heading="Server Results">
      {results?.map((result) => (
        <Command.Item key={result.id}>{result.label}</Command.Item>
      ))}
    </Command.Group>
  );
}
```

See `references/server-side-search.md` for complete Tanstack Query patterns.

## Multi-Step Commands

```typescript
function MultiStepPalette() {
  const commandStack = useCommandStore((state) => state.commandStack);
  const pushCommand = useCommandStore((state) => state.pushCommand);
  const popCommand = useCommandStore((state) => state.popCommand);

  const currentLevel = commandStack.length;

  // Example: Repository → Action workflow
  if (currentLevel === 0) {
    return <RepositoryList onSelect={(repo) => pushCommand(repo)} />;
  }

  if (currentLevel === 1) {
    const selectedRepo = commandStack[0];
    return (
      <>
        <Breadcrumb>
          <button onClick={popCommand}>{selectedRepo.label}</button>
        </Breadcrumb>
        <ActionList repository={selectedRepo} />
      </>
    );
  }

  return null;
}
```

## Performance Optimization

### Selectors to Prevent Re-renders

```typescript
// Bad: Subscribes to entire store
const store = useCommandStore();

// Good: Subscribe only to needed values
const isOpen = useCommandStore((state) => state.isOpen);
const commands = useCommandStore((state) => state.commands);

// Best: Use computed selectors
const commands = useCommandStore((state) => state.filteredCommands());
```

### Shallow Equality

```typescript
import { shallow } from 'zustand/shallow';

// Only re-render if isOpen or searchQuery change
const { isOpen, searchQuery } = useCommandStore(
  (state) => ({ isOpen: state.isOpen, searchQuery: state.searchQuery }),
  shallow
);
```

## See Also

- **Server-Side Search:** `references/server-side-search.md`
- **Testing:** `references/testing.md`
- **Keyboard Navigation:** `references/keyboard-navigation.md`
