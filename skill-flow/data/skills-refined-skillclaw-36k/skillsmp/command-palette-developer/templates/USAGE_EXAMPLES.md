# Usage Examples

Real-world examples of combining features and providers to build complete command palettes.

## Example 1: Basic Command Palette

Simple palette with search and keyboard shortcuts.

```tsx
import { useState } from 'react';
import {
  useCommandPalette,
  useCommands,
  useCommandRegistry,
} from './providers';
import { KeyboardShortcutsWrapper } from './features';

function CommandPalette() {
  const { isOpen, setOpen } = useCommandPalette();
  const commands = useCommands();
  const { register } = useCommandRegistry();

  // Register commands
  useEffect(() => {
    register({
      id: 'create-task',
      label: 'Create Task',
      keywords: ['new', 'task'],
      shortcut: 'command+n',
      group: 'Actions',
      onSelect: () => navigate('/tasks/new'),
    });
  }, [register]);

  const shortcuts = [
    { id: 'open', keys: 'command+k', handler: () => setOpen(true) },
    { id: 'close', keys: 'escape', handler: () => setOpen(false) },
  ];

  return (
    <KeyboardShortcutsWrapper shortcuts={shortcuts}>
      {isOpen && (
        <div className="command-palette">
          <input type="search" placeholder="Search commands..." />
          <div className="commands">
            {commands.map((cmd) => (
              <button key={cmd.id} onClick={cmd.onSelect}>
                {cmd.label}
              </button>
            ))}
          </div>
        </div>
      )}
    </KeyboardShortcutsWrapper>
  );
}
```

## Example 2: Palette with Virtual Scrolling

Handle 10,000+ commands with smooth performance.

```tsx
import { VirtualScrollWrapper } from './features';
import { useCommands } from './providers';

function LargeCommandList() {
  const commands = useCommands(); // Returns all filtered commands

  return (
    <VirtualScrollWrapper
      items={commands}
      renderItem={(cmd) => (
        <div className="command-item" onClick={cmd.onSelect}>
          {cmd.icon && <cmd.icon />}
          <div>
            <div className="label">{cmd.label}</div>
            {cmd.description && (
              <div className="description">{cmd.description}</div>
            )}
          </div>
        </div>
      )}
      estimatedHeight={48}
      containerHeight={400}
      overscan={5}
    />
  );
}
```

## Example 3: Server-Side Search Palette

Search a remote API with debouncing and caching.

```tsx
import { useState } from 'react';
import {
  ServerSearchWrapper,
  SearchLoadingSkeleton,
  SearchErrorState,
  SearchEmptyState,
} from './features';
import { useSearchHistory } from './providers';

function ServerSearchPalette() {
  const [query, setQuery] = useState('');
  const { addToHistory } = useSearchHistory();

  const searchFn = async (q: string) => {
    const response = await fetch(`/api/commands/search?q=${encodeURIComponent(q)}`);
    if (!response.ok) throw new Error('Search failed');
    return response.json();
  };

  return (
    <div className="palette">
      <input
        type="search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search commands..."
      />

      <ServerSearchWrapper
        query={query}
        searchFn={searchFn}
        debounceMs={300}
        cacheTime={5 * 60 * 1000}
        onError={(error) => console.error('Search error:', error)}
      >
        {({ data, isLoading, isError, error, refetch }) => (
          <>
            {isLoading && <SearchLoadingSkeleton count={5} />}

            {isError && <SearchErrorState error={error!} onRetry={refetch} />}

            {data && data.length === 0 && <SearchEmptyState query={query} />}

            {data && data.length > 0 && (
              <div className="results">
                {data.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => {
                      addToHistory(query);
                      item.onSelect();
                    }}
                  >
                    {item.label}
                  </button>
                ))}
              </div>
            )}
          </>
        )}
      </ServerSearchWrapper>
    </div>
  );
}
```

## Example 4: Multi-Step Palette

Navigate through nested command menus.

```tsx
import { useCommandStack, useCommands } from './providers';

function MultiStepPalette() {
  const { stack, push, pop, depth } = useCommandStack();
  const commands = useCommands();

  // Current level determines what to show
  if (depth === 0) {
    // Root level: show all repositories
    return (
      <div className="palette">
        <div className="breadcrumb">Select Repository</div>
        {commands
          .filter((cmd) => cmd.group === 'repositories')
          .map((repo) => (
            <button
              key={repo.id}
              onClick={() => push(repo)}
            >
              {repo.label}
            </button>
          ))}
      </div>
    );
  }

  if (depth === 1) {
    // Second level: show actions for selected repo
    const selectedRepo = stack[0];
    return (
      <div className="palette">
        <div className="breadcrumb">
          <button onClick={pop}>← Back</button>
          <span>{selectedRepo.label}</span>
        </div>
        {commands
          .filter((cmd) => cmd.group === 'actions')
          .map((action) => (
            <button
              key={action.id}
              onClick={() => {
                action.onSelect();
                // Clear stack after action
                useCommandStore.getState().clearStack();
              }}
            >
              {action.label}
            </button>
          ))}
      </div>
    );
  }

  return null;
}
```

## Example 5: Themed Palette with Toggle

Full-featured palette with theme switching.

```tsx
import {
  ThemeProvider,
  CommandProvider,
  SearchProvider,
  useTheme,
  useCommandPalette,
} from './providers';
import { ThemeToggle, KeyboardShortcutsWrapper } from './features';

function App() {
  return (
    <ThemeProvider>
      <CommandProvider>
        <SearchProvider>
          <ThemedApp />
        </SearchProvider>
      </CommandProvider>
    </ThemeProvider>
  );
}

function ThemedApp() {
  const { theme, resolvedTheme } = useTheme();
  const { isOpen, setOpen } = useCommandPalette();

  const shortcuts = [
    { id: 'palette', keys: 'command+k', handler: () => setOpen(true) },
    { id: 'close', keys: 'escape', handler: () => setOpen(false) },
  ];

  return (
    <KeyboardShortcutsWrapper shortcuts={shortcuts}>
      <div className="app">
        <header>
          <h1>My App</h1>
          <ThemeToggle position="right" showLabel={true} />
        </header>

        {isOpen && (
          <div className="palette-overlay" onClick={() => setOpen(false)}>
            <div
              className="palette"
              onClick={(e) => e.stopPropagation()}
              style={{
                background: 'var(--palette-bg)',
                border: '1px solid var(--palette-border)',
                color: 'var(--palette-text)',
              }}
            >
              <CommandPaletteContent />
            </div>
          </div>
        )}
      </div>
    </KeyboardShortcutsWrapper>
  );
}
```

## Example 6: Recent & Favorite Commands

Show frequently used commands at the top.

```tsx
import { useRecentCommands, useFavoriteCommands, useCommands } from './providers';

function SmartCommandList() {
  const { recent } = useRecentCommands();
  const { favorites, toggleFavorite, isFavorite } = useFavoriteCommands();
  const allCommands = useCommands();

  return (
    <div className="command-list">
      {/* Favorites section */}
      {favorites.length > 0 && (
        <div className="section">
          <h3>Favorites</h3>
          {favorites.map((cmd) => (
            <CommandItem
              key={cmd.id}
              command={cmd}
              isFavorite={true}
              onToggleFavorite={() => toggleFavorite(cmd.id)}
            />
          ))}
        </div>
      )}

      {/* Recent section */}
      {recent.length > 0 && (
        <div className="section">
          <h3>Recent</h3>
          {recent.slice(0, 5).map((cmd) => (
            <CommandItem
              key={cmd.id}
              command={cmd}
              isFavorite={isFavorite(cmd.id)}
              onToggleFavorite={() => toggleFavorite(cmd.id)}
            />
          ))}
        </div>
      )}

      {/* All commands section */}
      <div className="section">
        <h3>All Commands</h3>
        {allCommands.map((cmd) => (
          <CommandItem
            key={cmd.id}
            command={cmd}
            isFavorite={isFavorite(cmd.id)}
            onToggleFavorite={() => toggleFavorite(cmd.id)}
          />
        ))}
      </div>
    </div>
  );
}

function CommandItem({
  command,
  isFavorite,
  onToggleFavorite,
}: {
  command: Command;
  isFavorite: boolean;
  onToggleFavorite: () => void;
}) {
  return (
    <div className="command-item">
      <button onClick={command.onSelect}>{command.label}</button>
      <button
        onClick={onToggleFavorite}
        className="favorite-btn"
        aria-label={isFavorite ? 'Remove from favorites' : 'Add to favorites'}
      >
        {isFavorite ? '★' : '☆'}
      </button>
    </div>
  );
}
```

## Example 7: Search History Autocomplete

Show previous searches as suggestions.

```tsx
import { useState } from 'react';
import { useSearchHistory, useSearchSuggestions } from './providers';

function SearchWithHistory() {
  const [query, setQuery] = useState('');
  const { addToHistory, clearHistory } = useSearchHistory();
  const suggestions = useSearchSuggestions(query);

  const handleSubmit = (searchQuery: string) => {
    addToHistory(searchQuery);
    performSearch(searchQuery);
  };

  return (
    <div className="search-container">
      <input
        type="search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter') {
            handleSubmit(query);
          }
        }}
        placeholder="Search..."
      />

      {/* Show suggestions when typing */}
      {query && suggestions.length > 0 && (
        <div className="suggestions">
          {suggestions.map((suggestion) => (
            <button
              key={suggestion}
              onClick={() => {
                setQuery(suggestion);
                handleSubmit(suggestion);
              }}
            >
              🕐 {suggestion}
            </button>
          ))}
        </div>
      )}

      {/* Clear history button */}
      <button onClick={clearHistory} className="clear-history">
        Clear Search History
      </button>
    </div>
  );
}
```

## Example 8: Grouped Commands with Icons

Organize commands by category with visual indicators.

```tsx
import { useGroupedCommands } from './providers';
import { ShortcutDisplay } from './features';

function GroupedCommandList() {
  const grouped = useGroupedCommands();

  return (
    <div className="grouped-commands">
      {Object.entries(grouped).map(([group, commands]) => (
        <div key={group} className="command-group">
          <h3 className="group-heading">{group}</h3>
          <div className="group-commands">
            {commands.map((cmd) => (
              <button
                key={cmd.id}
                className="command-item"
                onClick={cmd.onSelect}
              >
                {cmd.icon && <cmd.icon className="command-icon" />}
                <div className="command-content">
                  <div className="command-label">{cmd.label}</div>
                  {cmd.description && (
                    <div className="command-description">{cmd.description}</div>
                  )}
                </div>
                {cmd.shortcut && (
                  <ShortcutDisplay keys={cmd.shortcut} className="command-shortcut" />
                )}
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
```

## Example 9: Complete Production Palette

Combines all features into a full implementation.

```tsx
import { useState, useEffect } from 'react';
import {
  ThemeProvider,
  CommandProvider,
  SearchProvider,
  useCommandPalette,
  useCommands,
  useRecentCommands,
  useCommandRegistry,
} from './providers';
import {
  VirtualScrollWrapper,
  ServerSearchWrapper,
  KeyboardShortcutsWrapper,
  ThemeToggle,
  ShortcutDisplay,
} from './features';

// Main app wrapper
function App() {
  return (
    <ThemeProvider>
      <CommandProvider>
        <SearchProvider>
          <AppContent />
        </SearchProvider>
      </CommandProvider>
    </ThemeProvider>
  );
}

function AppContent() {
  const { isOpen, setOpen } = useCommandPalette();

  const shortcuts = [
    { id: 'open', keys: 'command+k', handler: () => setOpen(true) },
    { id: 'close', keys: 'escape', handler: () => setOpen(false) },
  ];

  return (
    <KeyboardShortcutsWrapper shortcuts={shortcuts}>
      <div className="app">
        <Header />
        <MainContent />
        {isOpen && <CommandPaletteModal />}
      </div>
    </KeyboardShortcutsWrapper>
  );
}

function Header() {
  return (
    <header>
      <h1>My App</h1>
      <ThemeToggle position="right" showLabel />
    </header>
  );
}

function CommandPaletteModal() {
  const { setOpen } = useCommandPalette();
  const [query, setQuery] = useState('');
  const { addToRecent } = useRecentCommands();

  const handleSelect = (command: Command) => {
    addToRecent(command.id);
    command.onSelect();
    setOpen(false);
  };

  return (
    <div className="palette-overlay" onClick={() => setOpen(false)}>
      <div className="palette" onClick={(e) => e.stopPropagation()}>
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search commands..."
          className="palette-input"
          autoFocus
        />

        <ServerSearchWrapper
          query={query}
          searchFn={searchCommands}
          debounceMs={300}
        >
          {({ data, isLoading }) => (
            <>
              {isLoading && <div className="loading">Searching...</div>}
              {data && (
                <VirtualScrollWrapper
                  items={data}
                  renderItem={(cmd) => (
                    <button
                      className="command-item"
                      onClick={() => handleSelect(cmd)}
                    >
                      {cmd.icon && <cmd.icon />}
                      <div>
                        <div className="label">{cmd.label}</div>
                        {cmd.description && (
                          <div className="description">{cmd.description}</div>
                        )}
                      </div>
                      {cmd.shortcut && <ShortcutDisplay keys={cmd.shortcut} />}
                    </button>
                  )}
                  containerHeight={400}
                  estimatedHeight={48}
                />
              )}
            </>
          )}
        </ServerSearchWrapper>
      </div>
    </div>
  );
}

async function searchCommands(query: string) {
  const response = await fetch(`/api/commands/search?q=${query}`);
  return response.json();
}
```

## Styling Examples

### CSS Variables for Theming

```css
/* globals.css */
:root {
  --palette-bg: #ffffff;
  --palette-text: #111827;
  --palette-border: #e5e7eb;
  --palette-selection-bg: #eff6ff;
  --palette-accent: #3b82f6;
}

[data-theme="dark"] {
  --palette-bg: #1f2937;
  --palette-text: #f9fafb;
  --palette-border: #374151;
  --palette-selection-bg: #374151;
  --palette-accent: #60a5fa;
}
```

### Palette Styles

```css
.palette {
  background: var(--palette-bg);
  border: 1px solid var(--palette-border);
  border-radius: 12px;
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.1);
  max-width: 640px;
  width: 100%;
  max-height: 500px;
}

.palette-input {
  width: 100%;
  padding: 16px;
  border: none;
  border-bottom: 1px solid var(--palette-border);
  background: transparent;
  color: var(--palette-text);
  font-size: 16px;
}

.command-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border: none;
  background: transparent;
  color: var(--palette-text);
  cursor: pointer;
  text-align: left;
  width: 100%;
}

.command-item:hover {
  background: var(--palette-selection-bg);
}
```

These examples demonstrate how to combine the feature components and providers to build production-ready command palettes with various capabilities.
