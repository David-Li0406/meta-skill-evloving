# Keyboard Navigation

Complete keyboard interaction patterns, shortcuts, focus management, and accessibility for command palettes.

## Essential Keyboard Shortcuts

### Core Navigation

| Key | Action | Required |
|-----|--------|----------|
| ⌘K / Ctrl+K | Toggle palette open/close | ✓ Yes |
| ESC | Close palette | ✓ Yes |
| ↑ / ↓ | Navigate results | ✓ Yes |
| Enter | Execute selected command | ✓ Yes |
| Tab | Next interactive element | ✓ Yes |
| Shift+Tab | Previous interactive element | ✓ Yes |

### Enhanced Navigation

| Key | Action | Optional |
|-----|--------|----------|
| ⌘+Backspace | Clear search query | Recommended |
| ⌘+↑ / ⌘+↓ | Jump to first/last result | Nice to have |
| Page Up/Down | Scroll results by page | Nice to have |
| Home / End | Jump to first/last result | Nice to have |
| ⌘+1-9 | Execute result by number (Raycast style) | Power user |

### Multi-Key Sequences

**"G then D" pattern** (Vi/Raycast style):
```typescript
let keySequence: string[] = [];
let sequenceTimeout: NodeJS.Timeout;

function handleKeyPress(key: string) {
  clearTimeout(sequenceTimeout);
  keySequence.push(key);

  // Check for matches
  const sequence = keySequence.join(' then ');
  const command = commands.find(cmd => cmd.shortcut === sequence);

  if (command) {
    executeCommand(command);
    keySequence = [];
  } else {
    // Reset after 1.5s
    sequenceTimeout = setTimeout(() => {
      keySequence = [];
    }, 1500);
  }
}
```

## Focus Management

### Focus Trap

Prevent tab focus from leaving palette while open:

```typescript
import { useEffect, useRef } from 'react';

function useFocusTrap(isOpen: boolean) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen) return;

    const container = containerRef.current;
    if (!container) return;

    const focusableElements = container.querySelectorAll(
      'a, button, input, textarea, select, [tabindex]:not([tabindex="-1"])'
    );

    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

    function handleTab(e: KeyboardEvent) {
      if (e.key !== 'Tab') return;

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      }
    }

    container.addEventListener('keydown', handleTab);
    firstElement?.focus();

    return () => container.removeEventListener('keydown', handleTab);
  }, [isOpen]);

  return containerRef;
}
```

### Auto-Focus Input

```typescript
function CommandPalette({ isOpen }: { isOpen: boolean }) {
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      // Small delay ensures palette is rendered
      setTimeout(() => inputRef.current?.focus(), 10);
    }
  }, [isOpen]);

  return <input ref={inputRef} />;
}
```

### Restore Focus on Close

```typescript
function useRestoreFocus(isOpen: boolean) {
  const previousActiveElement = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      previousActiveElement.current = document.activeElement as HTMLElement;
    } else if (previousActiveElement.current) {
      previousActiveElement.current.focus();
      previousActiveElement.current = null;
    }
  }, [isOpen]);
}
```

## Shortcut Display Formatting

### Platform-Aware Display

```typescript
const isMac = /(Mac|iPhone|iPod|iPad)/i.test(navigator.platform);

const symbols = {
  command: isMac ? '⌘' : 'Ctrl',
  shift: isMac ? '⇧' : 'Shift',
  option: isMac ? '⌥' : 'Alt',
  control: '⌃',
  enter: '↵',
  delete: '⌫',
  escape: 'Esc',
};

function formatShortcut(shortcut: string): string {
  return shortcut
    .replace('command', symbols.command)
    .replace('shift', symbols.shift)
    .replace('option', symbols.option)
    .replace('enter', symbols.enter);
}

// Usage: formatShortcut('command+shift+p') → '⌘⇧P'
```

### Shortcut Component

```tsx
function Shortcut({ keys }: { keys: string }) {
  const formatted = formatShortcut(keys);
  const parts = formatted.split('+');

  return (
    <span className="shortcut">
      {parts.map((key, i) => (
        <kbd key={i} className="key">
          {key}
        </kbd>
      ))}
    </span>
  );
}

// CSS
.shortcut {
  display: inline-flex;
  gap: 2px;
}

.key {
  display: inline-block;
  padding: 2px 6px;
  background: var(--palette-shortcut-bg);
  border: 1px solid var(--palette-shortcut-border);
  border-radius: 4px;
  font-family: ui-monospace, monospace;
  font-size: 12px;
  line-height: 1;
}
```

## Keyboard Shortcut Hook

```typescript
// utilities/keyboard-shortcuts.ts

export function useKeyboardShortcut(
  shortcut: string,
  handler: () => void,
  options: { enabled?: boolean; preventDefault?: boolean } = {}
) {
  const { enabled = true, preventDefault = true } = options;

  useEffect(() => {
    if (!enabled) return;

    function handleKeyDown(e: KeyboardEvent) {
      const matches = matchesShortcut(e, shortcut);
      if (matches) {
        if (preventDefault) e.preventDefault();
        handler();
      }
    }

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [shortcut, handler, enabled, preventDefault]);
}

function matchesShortcut(event: KeyboardEvent, shortcut: string): boolean {
  const parts = shortcut.toLowerCase().split('+');
  const key = parts[parts.length - 1];
  const modifiers = parts.slice(0, -1);

  // Check key match
  const keyMatches = event.key.toLowerCase() === key;

  // Check modifier match
  const hasCommand = event.metaKey || event.ctrlKey;
  const hasShift = event.shiftKey;
  const hasAlt = event.altKey;

  const needsCommand = modifiers.includes('command') || modifiers.includes('ctrl');
  const needsShift = modifiers.includes('shift');
  const needsAlt = modifiers.includes('alt') || modifiers.includes('option');

  return (
    keyMatches &&
    hasCommand === needsCommand &&
    hasShift === needsShift &&
    hasAlt === needsAlt
  );
}

// Usage
function MyComponent() {
  useKeyboardShortcut('command+k', () => setOpen(true));
  useKeyboardShortcut('escape', () => setOpen(false));
}
```

## Keyboard Legend Footer

```tsx
function KeyboardLegend() {
  return (
    <footer className="keyboard-legend">
      <div className="legend-item">
        <Shortcut keys="↑↓" /> to navigate
      </div>
      <div className="legend-item">
        <Shortcut keys="↵" /> to select
      </div>
      <div className="legend-item">
        <Shortcut keys="esc" /> to close
      </div>
      <div className="legend-item">
        <Shortcut keys="command+1-9" /> quick actions
      </div>
    </footer>
  );
}

// CSS
.keyboard-legend {
  display: flex;
  gap: 16px;
  padding: 8px 16px;
  border-top: 1px solid var(--palette-border);
  background: var(--palette-bg-secondary);
  font-size: 12px;
  color: var(--palette-text-muted);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
}
```

## Accessibility Attributes

### ARIA for Command Palette

```tsx
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="palette-title"
  aria-describedby="palette-description"
>
  <h2 id="palette-title" className="sr-only">
    Command Palette
  </h2>
  <p id="palette-description" className="sr-only">
    Search and execute commands. Use arrow keys to navigate, Enter to select.
  </p>

  <input
    role="combobox"
    aria-expanded={isOpen}
    aria-controls="results-list"
    aria-activedescendant={selectedId}
    aria-autocomplete="list"
  />

  <ul role="listbox" id="results-list">
    <li
      role="option"
      id="command-1"
      aria-selected={selected === 'command-1'}
    >
      Command 1
    </li>
  </ul>
</div>
```

### Screen Reader Announcements

```tsx
function ResultsAnnouncement({ count, query }: { count: number; query: string }) {
  return (
    <div role="status" aria-live="polite" aria-atomic="true" className="sr-only">
      {query && `${count} result${count !== 1 ? 's' : ''} found for "${query}"`}
      {!query && count === 0 && 'No results'}
    </div>
  );
}

// .sr-only utility (screen reader only)
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

## Conflict Prevention

### Checking for Conflicts

```typescript
function checkShortcutConflicts(shortcuts: string[]): string[] {
  const conflicts: string[] = [];
  const browserShortcuts = [
    'command+p', // Print
    'command+s', // Save
    'command+f', // Find
    'command+t', // New Tab
    'command+w', // Close Tab
  ];

  shortcuts.forEach(shortcut => {
    if (browserShortcuts.includes(shortcut)) {
      conflicts.push(shortcut);
    }
  });

  return conflicts;
}
```

### Safe Shortcuts

**Recommended:**
- ⌘K, ⌘+Shift+P (palette trigger)
- ⌘/, ⌘+Shift+K (alternative triggers)
- ⌘+Backspace (clear)
- ⌘+1-9 (quick actions)
- G then D, G then H (sequences)

**Avoid:**
- ⌘P (conflicts with print)
- ⌘S (conflicts with save)
- ⌘F (conflicts with find)
- ⌘T, ⌘W (browser tabs)
- ⌘R (refresh)
