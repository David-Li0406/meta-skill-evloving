/**
 * KeyboardShortcutsWrapper - Global keyboard listener and shortcut management
 *
 * Features:
 * - Global keyboard listener
 * - Shortcut registration API
 * - Conflict detection
 * - Platform-aware (Mac vs Windows)
 * - Shortcut display formatting
 * - Enable/disable shortcuts dynamically
 *
 * @example
 * ```tsx
 * const shortcuts: Shortcut[] = [
 *   { id: 'open', keys: 'command+k', handler: () => setOpen(true) },
 *   { id: 'close', keys: 'escape', handler: () => setOpen(false) },
 * ];
 *
 * <KeyboardShortcutsWrapper
 *   shortcuts={shortcuts}
 *   enabled={true}
 *   onTrigger={(id) => console.log(`Triggered: ${id}`)}
 * />
 * ```
 */

import { useEffect, type ReactNode } from 'react';

export interface Shortcut {
  /** Unique identifier for the shortcut */
  id: string;
  /** Key combination (e.g., "command+k", "shift+g then d") */
  keys: string;
  /** Handler function to execute */
  handler: () => void;
  /** Optional description */
  description?: string;
  /** Prevent default browser behavior (default: true) */
  preventDefault?: boolean;
  /** Enable/disable this specific shortcut */
  enabled?: boolean;
}

export interface KeyboardShortcutsWrapperProps {
  /** Array of shortcuts to register */
  shortcuts: Shortcut[];
  /** Enable/disable all shortcuts (default: true) */
  enabled?: boolean;
  /** Callback when a shortcut is triggered */
  onTrigger?: (id: string) => void;
  /** Optional children to render */
  children?: ReactNode;
}

/**
 * Check if running on Mac
 */
const isMac = typeof window !== 'undefined' && /(Mac|iPhone|iPod|iPad)/i.test(navigator.platform);

/**
 * Platform-aware key symbols
 */
export const KeySymbols = {
  command: isMac ? '⌘' : 'Ctrl',
  shift: isMac ? '⇧' : 'Shift',
  option: isMac ? '⌥' : 'Alt',
  control: '⌃',
  enter: '↵',
  delete: '⌫',
  escape: 'Esc',
  up: '↑',
  down: '↓',
  left: '←',
  right: '→',
} as const;

/**
 * Format shortcut keys for display
 *
 * @example
 * formatShortcut('command+shift+p') // → '⌘⇧P'
 */
export function formatShortcut(keys: string): string {
  return keys
    .replace(/command/gi, KeySymbols.command)
    .replace(/shift/gi, KeySymbols.shift)
    .replace(/option|alt/gi, KeySymbols.option)
    .replace(/control/gi, KeySymbols.control)
    .replace(/enter/gi, KeySymbols.enter)
    .replace(/delete/gi, KeySymbols.delete)
    .replace(/escape/gi, KeySymbols.escape)
    .replace(/\+/g, '')
    .toUpperCase();
}

/**
 * Match a keyboard event against a shortcut string
 */
function matchesShortcut(event: KeyboardEvent, shortcut: string): boolean {
  const parts = shortcut.toLowerCase().split('+');
  const key = parts[parts.length - 1];
  const modifiers = parts.slice(0, -1);

  // Check key match
  const eventKey = event.key.toLowerCase();
  const keyMatches = eventKey === key || event.code.toLowerCase() === key.toLowerCase();

  // Check modifier match
  const hasCommand = event.metaKey || event.ctrlKey;
  const hasShift = event.shiftKey;
  const hasAlt = event.altKey;
  const hasControl = event.ctrlKey;

  const needsCommand = modifiers.includes('command') || modifiers.includes('ctrl');
  const needsShift = modifiers.includes('shift');
  const needsAlt = modifiers.includes('alt') || modifiers.includes('option');
  const needsControl = modifiers.includes('control');

  return (
    keyMatches &&
    hasCommand === needsCommand &&
    hasShift === needsShift &&
    hasAlt === needsAlt &&
    (!needsControl || hasControl === needsControl)
  );
}

/**
 * Detect shortcut conflicts
 */
export function detectConflicts(shortcuts: Shortcut[]): Map<string, string[]> {
  const conflicts = new Map<string, string[]>();
  const keyMap = new Map<string, string[]>();

  shortcuts.forEach((shortcut) => {
    const keys = shortcut.keys.toLowerCase();
    if (!keyMap.has(keys)) {
      keyMap.set(keys, []);
    }
    keyMap.get(keys)!.push(shortcut.id);
  });

  keyMap.forEach((ids, keys) => {
    if (ids.length > 1) {
      conflicts.set(keys, ids);
    }
  });

  return conflicts;
}

/**
 * Browser shortcuts to avoid
 */
const BROWSER_SHORTCUTS = new Set([
  'command+p',
  'ctrl+p',
  'command+s',
  'ctrl+s',
  'command+f',
  'ctrl+f',
  'command+t',
  'ctrl+t',
  'command+w',
  'ctrl+w',
  'command+r',
  'ctrl+r',
]);

/**
 * Check if a shortcut conflicts with browser shortcuts
 */
export function conflictsWithBrowser(keys: string): boolean {
  return BROWSER_SHORTCUTS.has(keys.toLowerCase());
}

/**
 * KeyboardShortcutsWrapper component
 *
 * Manages global keyboard shortcuts with conflict detection and platform-aware formatting.
 */
export function KeyboardShortcutsWrapper({
  shortcuts,
  enabled = true,
  onTrigger,
  children,
}: KeyboardShortcutsWrapperProps): JSX.Element {
  useEffect(() => {
    if (!enabled) return;

    // Check for conflicts
    const conflicts = detectConflicts(shortcuts);
    if (conflicts.size > 0) {
      console.warn('Keyboard shortcut conflicts detected:', Object.fromEntries(conflicts));
    }

    // Multi-key sequence support
    let keySequence: string[] = [];
    let sequenceTimeout: NodeJS.Timeout;

    function handleKeyDown(event: KeyboardEvent) {
      // Ignore shortcuts in input fields unless it's Escape
      const target = event.target as HTMLElement;
      const isInput =
        target.tagName === 'INPUT' ||
        target.tagName === 'TEXTAREA' ||
        target.isContentEditable;

      if (isInput && event.key !== 'Escape') {
        return;
      }

      // Check for matching shortcuts
      for (const shortcut of shortcuts) {
        if (shortcut.enabled === false) continue;

        // Handle multi-key sequences (e.g., "g then d")
        if (shortcut.keys.includes(' then ')) {
          const sequence = shortcut.keys.split(' then ');
          const currentKey = event.key.toLowerCase();

          clearTimeout(sequenceTimeout);
          keySequence.push(currentKey);

          const sequenceMatch = sequence.every((key, index) => {
            return keySequence[index]?.toLowerCase() === key.toLowerCase();
          });

          if (sequenceMatch) {
            if (shortcut.preventDefault !== false) {
              event.preventDefault();
            }
            shortcut.handler();
            onTrigger?.(shortcut.id);
            keySequence = [];
          } else {
            // Reset sequence after 1.5s
            sequenceTimeout = setTimeout(() => {
              keySequence = [];
            }, 1500);
          }
        } else {
          // Handle single shortcuts
          if (matchesShortcut(event, shortcut.keys)) {
            if (shortcut.preventDefault !== false) {
              event.preventDefault();
            }
            shortcut.handler();
            onTrigger?.(shortcut.id);
            keySequence = [];
          }
        }
      }
    }

    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      clearTimeout(sequenceTimeout);
    };
  }, [shortcuts, enabled, onTrigger]);

  return <>{children}</>;
}

/**
 * Shortcut display component
 */
export function ShortcutDisplay({ keys, className = '' }: { keys: string; className?: string }): JSX.Element {
  const formatted = formatShortcut(keys);
  const parts = formatted.match(/([⌘⇧⌥⌃↵⌫]|[A-Z0-9]+)/g) || [formatted];

  return (
    <span className={`shortcut-display ${className}`.trim()} style={{ display: 'inline-flex', gap: '2px' }}>
      {parts.map((key, i) => (
        <kbd
          key={i}
          className="shortcut-key"
          style={{
            display: 'inline-block',
            padding: '2px 6px',
            background: 'var(--palette-shortcut-bg)',
            border: '1px solid var(--palette-shortcut-border)',
            borderRadius: '4px',
            fontFamily: 'ui-monospace, monospace',
            fontSize: '12px',
            lineHeight: '1',
            color: 'var(--palette-shortcut-text)',
          }}
        >
          {key}
        </kbd>
      ))}
    </span>
  );
}
