/**
 * Constants and default configurations for command palette components
 *
 * Centralized configuration values for consistency across all variants.
 */

import type { CommandPaletteConfig, CommandPaletteTheme } from './types';

/**
 * Default animation duration in milliseconds
 */
export const DEFAULT_ANIMATION_DURATION = 300;

/**
 * Default animation duration for reduced motion
 */
export const REDUCED_MOTION_DURATION = 0;

/**
 * Default offset for embedded palette (distance from trigger)
 */
export const DEFAULT_EMBEDDED_OFFSET = 8;

/**
 * Default max width for embedded palette
 */
export const DEFAULT_EMBEDDED_MAX_WIDTH = 400;

/**
 * Default width for drawer (left/right positions)
 */
export const DEFAULT_DRAWER_WIDTH = '400px';

/**
 * Default height for drawer (top/bottom positions)
 */
export const DEFAULT_DRAWER_HEIGHT = '60vh';

/**
 * Default max height for results list
 */
export const DEFAULT_MAX_HEIGHT = '400px';

/**
 * Default max width for modal
 */
export const DEFAULT_MODAL_MAX_WIDTH = '640px';

/**
 * Default placeholder text
 */
export const DEFAULT_PLACEHOLDER = 'Search commands...';

/**
 * Default loading message
 */
export const DEFAULT_LOADING_MESSAGE = 'Loading...';

/**
 * Default empty state message
 */
export const DEFAULT_EMPTY_MESSAGE = 'No commands found';

/**
 * Default empty state help text
 */
export const DEFAULT_EMPTY_HELP = 'Try checking your spelling or using different keywords';

/**
 * Default number of recent commands to track
 */
export const DEFAULT_MAX_RECENT_COMMANDS = 10;

/**
 * Z-index for backdrop overlay
 */
export const BACKDROP_Z_INDEX = 9999;

/**
 * Z-index for floating elements
 */
export const FLOATING_Z_INDEX = 10000;

/**
 * Keyboard shortcuts
 */
export const KEYBOARD_SHORTCUTS = {
  /** Primary shortcut to open palette */
  TOGGLE: 'command+k',
  /** Alternative shortcut */
  TOGGLE_ALT: 'command+/',
  /** Close palette */
  CLOSE: 'escape',
  /** Navigate up */
  NAV_UP: 'arrowup',
  /** Navigate down */
  NAV_DOWN: 'arrowdown',
  /** Select command */
  SELECT: 'enter',
  /** Clear search */
  CLEAR: 'command+backspace',
  /** Jump to first result */
  JUMP_FIRST: 'command+arrowup',
  /** Jump to last result */
  JUMP_LAST: 'command+arrowdown',
} as const;

/**
 * Keyboard symbols for display
 */
export const KEYBOARD_SYMBOLS = {
  command: '⌘',
  ctrl: 'Ctrl',
  shift: '⇧',
  option: '⌥',
  alt: 'Alt',
  enter: '↵',
  escape: 'Esc',
  backspace: '⌫',
  delete: '⌦',
  arrowup: '↑',
  arrowdown: '↓',
  arrowleft: '←',
  arrowright: '→',
} as const;

/**
 * Platform detection regex patterns
 */
export const PLATFORM_PATTERNS = {
  mac: /(Mac|iPhone|iPod|iPad)/i,
  windows: /Win/i,
  linux: /Linux/i,
  ios: /(iPhone|iPod|iPad)/i,
  android: /Android/i,
} as const;

/**
 * Default command palette configuration
 */
export const DEFAULT_CONFIG: Required<CommandPaletteConfig> = {
  maxRecentCommands: DEFAULT_MAX_RECENT_COMMANDS,
  trackFrequency: true,
  showShortcuts: true,
  showDescriptions: true,
  showIcons: true,
  groupCommands: true,
  emptyStateMessage: DEFAULT_EMPTY_MESSAGE,
  loadingMessage: DEFAULT_LOADING_MESSAGE,
  animationDuration: DEFAULT_ANIMATION_DURATION,
  closeOnSelect: true,
};

/**
 * Light theme color palette
 */
export const LIGHT_THEME: CommandPaletteTheme = {
  bg: '#ffffff',
  bgSecondary: '#f9fafb',
  selectionBg: '#eff6ff',
  hoverBg: '#f3f4f6',
  text: '#111827',
  textMuted: '#6b7280',
  textPlaceholder: '#9ca3af',
  border: '#e5e7eb',
  separator: '#f3f4f6',
  accent: '#3b82f6',
  accentHover: '#2563eb',
  shadow: 'rgba(0, 0, 0, 0.1)',
  shadowLg: 'rgba(0, 0, 0, 0.15)',
  shortcutBg: '#f3f4f6',
  shortcutText: '#374151',
  shortcutBorder: '#d1d5db',
};

/**
 * Dark theme color palette
 */
export const DARK_THEME: CommandPaletteTheme = {
  bg: '#1f2937',
  bgSecondary: '#111827',
  selectionBg: '#374151',
  hoverBg: '#2d3748',
  text: '#f9fafb',
  textMuted: '#9ca3af',
  textPlaceholder: '#6b7280',
  border: '#374151',
  separator: '#2d3748',
  accent: '#60a5fa',
  accentHover: '#3b82f6',
  shadow: 'rgba(0, 0, 0, 0.3)',
  shadowLg: 'rgba(0, 0, 0, 0.5)',
  shortcutBg: '#374151',
  shortcutText: '#d1d5db',
  shortcutBorder: '#4b5563',
};

/**
 * CSS custom property names
 */
export const CSS_VARIABLES = {
  BG: '--palette-bg',
  BG_SECONDARY: '--palette-bg-secondary',
  SELECTION_BG: '--palette-selection-bg',
  HOVER_BG: '--palette-hover-bg',
  TEXT: '--palette-text',
  TEXT_MUTED: '--palette-text-muted',
  TEXT_PLACEHOLDER: '--palette-text-placeholder',
  BORDER: '--palette-border',
  SEPARATOR: '--palette-separator',
  ACCENT: '--palette-accent',
  ACCENT_HOVER: '--palette-accent-hover',
  SHADOW: '--palette-shadow',
  SHADOW_LG: '--palette-shadow-lg',
  SHORTCUT_BG: '--palette-shortcut-bg',
  SHORTCUT_TEXT: '--palette-shortcut-text',
  SHORTCUT_BORDER: '--palette-shortcut-border',
} as const;

/**
 * Local storage keys
 */
export const STORAGE_KEYS = {
  THEME: 'command-palette:theme',
  RECENT_COMMANDS: 'command-palette:recent',
  PINNED_COMMANDS: 'command-palette:pinned',
  FREQUENCY: 'command-palette:frequency',
  STATE: 'command-palette:state',
} as const;

/**
 * Animation class names
 */
export const ANIMATION_CLASSES = {
  FADE_IN: 'palette-fade-in',
  FADE_OUT: 'palette-fade-out',
  SLIDE_UP: 'palette-slide-up',
  SLIDE_DOWN: 'palette-slide-down',
  SLIDE_LEFT: 'palette-slide-left',
  SLIDE_RIGHT: 'palette-slide-right',
  SCALE_IN: 'palette-scale-in',
  SCALE_OUT: 'palette-scale-out',
} as const;

/**
 * ARIA labels for accessibility
 */
export const ARIA_LABELS = {
  DIALOG: 'Command Palette',
  INPUT: 'Search commands',
  LISTBOX: 'Command results',
  OPTION: 'Command option',
  CLOSE: 'Close palette',
  LOADING: 'Loading commands',
  EMPTY: 'No results',
} as const;

/**
 * Breakpoints for responsive design
 */
export const BREAKPOINTS = {
  MOBILE: 640,
  TABLET: 768,
  DESKTOP: 1024,
  WIDE: 1280,
} as const;

/**
 * Timing constants
 */
export const TIMING = {
  /** Debounce delay for search input */
  SEARCH_DEBOUNCE: 150,
  /** Auto-focus delay after open */
  FOCUS_DELAY: 10,
  /** Animation frame duration */
  FRAME_DURATION: 16,
  /** Keyboard sequence timeout */
  SEQUENCE_TIMEOUT: 1500,
} as const;

/**
 * Virtualization constants
 */
export const VIRTUALIZATION = {
  /** Item height in pixels */
  ITEM_HEIGHT: 48,
  /** Overscan count (render extra items) */
  OVERSCAN: 5,
  /** Threshold to enable virtualization */
  THRESHOLD: 100,
} as const;

/**
 * Accessibility constants
 */
export const A11Y = {
  /** Focus trap selector */
  FOCUSABLE_ELEMENTS: 'a, button, input, textarea, select, [tabindex]:not([tabindex="-1"])',
  /** Live region politeness */
  LIVE_REGION_POLITE: 'polite',
  /** Live region assertive */
  LIVE_REGION_ASSERTIVE: 'assertive',
} as const;

/**
 * Development mode flag
 */
export const IS_DEV = process.env.NODE_ENV === 'development';

/**
 * Debug logging enabled
 */
export const DEBUG = IS_DEV && typeof window !== 'undefined' && (window as any).__PALETTE_DEBUG__;
