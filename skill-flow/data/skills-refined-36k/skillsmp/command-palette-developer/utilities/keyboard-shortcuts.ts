// Keyboard shortcut utilities

import { useEffect } from 'react';

export interface KeyBinding {
  key: string;
  meta?: boolean;
  ctrl?: boolean;
  shift?: boolean;
  alt?: boolean;
}

export function parseShortcut(shortcut: string): KeyBinding {
  const parts = shortcut.toLowerCase().split('+');
  const key = parts[parts.length - 1];

  return {
    key,
    meta: parts.includes('command') || parts.includes('meta'),
    ctrl: parts.includes('ctrl'),
    shift: parts.includes('shift'),
    alt: parts.includes('alt') || parts.includes('option'),
  };
}

export function matchesShortcut(event: KeyboardEvent, shortcut: string): boolean {
  const binding = parseShortcut(shortcut);

  const keyMatches = event.key.toLowerCase() === binding.key;
  const metaMatches = (event.metaKey || event.ctrlKey) === (binding.meta || binding.ctrl || false);
  const shiftMatches = event.shiftKey === (binding.shift || false);
  const altMatches = event.altKey === (binding.alt || false);

  return keyMatches && metaMatches && shiftMatches && altMatches;
}

export function useKeyboardShortcut(
  shortcut: string,
  handler: () => void,
  options: { enabled?: boolean; preventDefault?: boolean } = {}
) {
  const { enabled = true, preventDefault = true } = options;

  useEffect(() => {
    if (!enabled) return;

    function handleKeyDown(e: KeyboardEvent) {
      if (matchesShortcut(e, shortcut)) {
        if (preventDefault) e.preventDefault();
        handler();
      }
    }

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [shortcut, handler, enabled, preventDefault]);
}

export function formatShortcut(shortcut: string): string {
  const isMac = /(Mac|iPhone|iPod|iPad)/i.test(navigator.platform);

  return shortcut
    .replace(/command/gi, isMac ? '⌘' : 'Ctrl')
    .replace(/shift/gi, isMac ? '⇧' : 'Shift')
    .replace(/option/gi, isMac ? '⌥' : 'Alt')
    .replace(/alt/gi, isMac ? '⌥' : 'Alt')
    .replace(/enter/gi, '↵')
    .replace(/escape/gi, 'Esc')
    .replace(/delete/gi, '⌫')
    .replace(/\+/g, isMac ? '' : '+');
}
