/**
 * Shared TypeScript type definitions for command palette components
 *
 * Comprehensive type safety for all command palette variants.
 */

/**
 * Platform detection for keyboard shortcuts
 */
export type Platform = 'mac' | 'windows' | 'linux' | 'ios' | 'android';

/**
 * Theme modes supported by command palette
 */
export type Theme = 'light' | 'dark' | 'system';

/**
 * Resolved theme (system theme converted to light/dark)
 */
export type ResolvedTheme = 'light' | 'dark';

/**
 * Keyboard modifier keys
 */
export type ModifierKey = 'command' | 'ctrl' | 'shift' | 'alt' | 'option';

/**
 * Keyboard shortcut definition
 */
export interface KeyboardShortcut {
  /** Main key (e.g., 'k', 'enter', 'escape') */
  key: string;
  /** Modifier keys pressed with main key */
  modifiers: ModifierKey[];
  /** Human-readable label (e.g., '⌘K' or 'Ctrl+K') */
  label: string;
}

/**
 * Command execution result
 */
export interface CommandResult {
  /** Whether command executed successfully */
  success: boolean;
  /** Optional success/error message */
  message?: string;
  /** Optional data returned by command */
  data?: unknown;
  /** Optional error if command failed */
  error?: Error;
}

/**
 * Command handler function
 */
export type CommandHandler = () => void | Promise<void> | CommandResult | Promise<CommandResult>;

/**
 * Command with handler
 */
export interface CommandWithHandler {
  /** Command metadata */
  command: import('./BaseCommandPalette').CommandItem;
  /** Handler function to execute */
  handler: CommandHandler;
}

/**
 * Filter function for commands
 */
export type CommandFilter = (command: import('./BaseCommandPalette').CommandItem) => boolean;

/**
 * Sort function for commands
 */
export type CommandSort = (
  a: import('./BaseCommandPalette').CommandItem,
  b: import('./BaseCommandPalette').CommandItem
) => number;

/**
 * Command palette state
 */
export interface CommandPaletteState {
  /** Whether palette is currently open */
  isOpen: boolean;
  /** Current search query */
  searchQuery: string;
  /** Currently selected command ID */
  selectedCommandId: string | null;
  /** Recent command IDs (most recent first) */
  recentCommandIds: string[];
  /** Pinned command IDs */
  pinnedCommandIds: string[];
  /** Command execution frequency (id -> count) */
  commandFrequency: Record<string, number>;
}

/**
 * Command palette configuration
 */
export interface CommandPaletteConfig {
  /** Maximum number of recent commands to track */
  maxRecentCommands?: number;
  /** Whether to track command frequency */
  trackFrequency?: boolean;
  /** Whether to show keyboard shortcuts */
  showShortcuts?: boolean;
  /** Whether to show command descriptions */
  showDescriptions?: boolean;
  /** Whether to show command icons */
  showIcons?: boolean;
  /** Whether to group commands */
  groupCommands?: boolean;
  /** Custom empty state message */
  emptyStateMessage?: string;
  /** Custom loading message */
  loadingMessage?: string;
  /** Animation duration in milliseconds */
  animationDuration?: number;
  /** Whether to close on command selection */
  closeOnSelect?: boolean;
}

/**
 * Command palette analytics event
 */
export interface CommandPaletteEvent {
  /** Event type */
  type: 'open' | 'close' | 'search' | 'select' | 'cancel';
  /** Timestamp of event */
  timestamp: number;
  /** Search query (for search events) */
  query?: string;
  /** Selected command (for select events) */
  commandId?: string;
  /** Time spent searching (for select/cancel events) */
  duration?: number;
}

/**
 * Command palette analytics
 */
export interface CommandPaletteAnalytics {
  /** Track when palette is opened */
  onOpen?: () => void;
  /** Track when palette is closed */
  onClose?: () => void;
  /** Track search queries */
  onSearch?: (query: string) => void;
  /** Track command selections */
  onSelect?: (commandId: string) => void;
  /** Track when user cancels without selection */
  onCancel?: () => void;
}

/**
 * Command palette storage interface
 */
export interface CommandPaletteStorage {
  /** Get item from storage */
  getItem: (key: string) => string | null | Promise<string | null>;
  /** Set item in storage */
  setItem: (key: string, value: string) => void | Promise<void>;
  /** Remove item from storage */
  removeItem: (key: string) => void | Promise<void>;
  /** Clear all items */
  clear: () => void | Promise<void>;
}

/**
 * Command category metadata
 */
export interface CommandCategory {
  /** Category identifier */
  id: string;
  /** Display label */
  label: string;
  /** Optional icon */
  icon?: React.ReactNode;
  /** Optional description */
  description?: string;
  /** Display order (lower = higher priority) */
  order?: number;
}

/**
 * Command palette theme colors
 */
export interface CommandPaletteTheme {
  /** Primary background color */
  bg: string;
  /** Secondary background color */
  bgSecondary: string;
  /** Selection background color */
  selectionBg: string;
  /** Hover background color */
  hoverBg: string;
  /** Primary text color */
  text: string;
  /** Muted text color */
  textMuted: string;
  /** Placeholder text color */
  textPlaceholder: string;
  /** Border color */
  border: string;
  /** Separator color */
  separator: string;
  /** Accent color */
  accent: string;
  /** Accent hover color */
  accentHover: string;
  /** Shadow color */
  shadow: string;
  /** Large shadow color */
  shadowLg: string;
  /** Keyboard shortcut background */
  shortcutBg: string;
  /** Keyboard shortcut text */
  shortcutText: string;
  /** Keyboard shortcut border */
  shortcutBorder: string;
}

/**
 * Validation result for commands
 */
export interface CommandValidation {
  /** Whether command is valid */
  valid: boolean;
  /** Validation errors */
  errors: string[];
  /** Validation warnings */
  warnings: string[];
}

/**
 * Command execution context
 */
export interface CommandContext {
  /** Current user */
  user?: unknown;
  /** Current route/page */
  route?: string;
  /** Additional context data */
  data?: Record<string, unknown>;
}

import React from 'react';
