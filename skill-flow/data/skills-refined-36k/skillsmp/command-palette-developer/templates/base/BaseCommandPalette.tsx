/**
 * BaseCommandPalette - Core command palette component
 *
 * Provides shared logic for keyboard navigation, command filtering, focus management,
 * and search functionality. Used internally by Modal, Embedded, and Drawer variants.
 *
 * @example
 * ```tsx
 * <BaseCommandPalette
 *   isOpen={true}
 *   onOpenChange={setOpen}
 *   searchQuery={query}
 *   onSearchChange={setQuery}
 *   commands={commands}
 *   onSelect={handleSelect}
 *   placeholder="Search commands..."
 * />
 * ```
 */

import { useEffect, useRef, useState, useMemo } from 'react';
import { Command } from 'cmdk';

/**
 * Command definition with metadata
 */
export interface CommandItem {
  /** Unique command identifier */
  id: string;
  /** Display label shown in results */
  label: string;
  /** Optional description (muted text) */
  description?: string;
  /** Keyboard shortcut (e.g., "command+s") */
  shortcut?: string;
  /** Icon component or emoji */
  icon?: React.ReactNode;
  /** Optional group for organization */
  group?: string;
  /** Search keywords for fuzzy matching */
  keywords?: string[];
  /** Optional badge text (e.g., "New", "Beta") */
  badge?: string;
}

/**
 * Command groups for organization
 */
export interface CommandGroup {
  /** Group identifier */
  id: string;
  /** Display label for group */
  label: string;
  /** Commands in this group */
  commands: CommandItem[];
}

export interface BaseCommandPaletteProps {
  /** Whether palette is open */
  isOpen: boolean;
  /** Callback when open state changes */
  onOpenChange: (open: boolean) => void;
  /** Current search query */
  searchQuery: string;
  /** Callback when search query changes */
  onSearchChange: (query: string) => void;
  /** Flat array of commands or grouped commands */
  commands?: CommandItem[];
  /** Grouped commands (alternative to flat commands) */
  groups?: CommandGroup[];
  /** Callback when command is selected */
  onSelect: (command: CommandItem) => void;
  /** Input placeholder text */
  placeholder?: string;
  /** Optional footer content */
  footer?: React.ReactNode;
  /** Optional empty state content */
  emptyState?: React.ReactNode;
  /** Optional loading state */
  isLoading?: boolean;
  /** Maximum height for results list */
  maxHeight?: string;
}

/**
 * BaseCommandPalette component
 *
 * Handles keyboard navigation (↑↓ arrow keys, Enter, Escape), command filtering
 * with fuzzy search, focus management, and accessible markup.
 */
export function BaseCommandPalette({
  isOpen,
  onOpenChange,
  searchQuery,
  onSearchChange,
  commands = [],
  groups = [],
  onSelect,
  placeholder = 'Search commands...',
  footer,
  emptyState,
  isLoading = false,
  maxHeight = '400px',
}: BaseCommandPaletteProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [selectedValue, setSelectedValue] = useState<string>('');

  // Auto-focus input when opened
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 10);
    }
  }, [isOpen]);

  // Handle ESC key to close
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        e.preventDefault();
        onOpenChange(false);
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onOpenChange]);

  // Compute grouped commands from flat list or use provided groups
  const commandGroups = useMemo(() => {
    if (groups.length > 0) {
      return groups;
    }

    // Group flat commands by their group property
    const grouped = commands.reduce((acc, command) => {
      const groupName = command.group || 'Commands';
      if (!acc[groupName]) {
        acc[groupName] = {
          id: groupName.toLowerCase().replace(/\s+/g, '-'),
          label: groupName,
          commands: [],
        };
      }
      acc[groupName].commands.push(command);
      return acc;
    }, {} as Record<string, CommandGroup>);

    return Object.values(grouped);
  }, [commands, groups]);

  // Handle command selection
  const handleSelect = (value: string) => {
    const command = commands.find((cmd) => cmd.id === value);
    if (command) {
      onSelect(command);
      onOpenChange(false);
      onSearchChange('');
    }
  };

  // Format keyboard shortcut for display
  const formatShortcut = (shortcut: string) => {
    const isMac = /(Mac|iPhone|iPod|iPad)/i.test(navigator.platform);
    return shortcut
      .replace('command', isMac ? '⌘' : 'Ctrl')
      .replace('shift', isMac ? '⇧' : 'Shift')
      .replace('option', isMac ? '⌥' : 'Alt')
      .replace('control', '⌃')
      .replace('enter', '↵')
      .replace('escape', 'Esc')
      .split('+')
      .map((key) => key.trim())
      .join(isMac ? '' : '+');
  };

  return (
    <Command
      value={selectedValue}
      onValueChange={setSelectedValue}
      className="command-palette-base"
      label="Command Palette"
    >
      {/* Search Input */}
      <div className="command-palette-input-wrapper">
        <Command.Input
          ref={inputRef}
          value={searchQuery}
          onValueChange={onSearchChange}
          placeholder={placeholder}
          className="command-palette-input"
          style={{
            width: '100%',
            padding: '12px 16px',
            background: 'var(--palette-bg)',
            color: 'var(--palette-text)',
            border: 'none',
            outline: 'none',
            fontSize: '14px',
            fontFamily: 'inherit',
          }}
        />
      </div>

      {/* Results List */}
      <Command.List
        className="command-palette-list"
        style={{
          maxHeight,
          overflow: 'auto',
          padding: '8px',
        }}
      >
        {/* Loading State */}
        {isLoading && (
          <div
            className="command-palette-loading"
            style={{
              padding: '24px',
              textAlign: 'center',
              color: 'var(--palette-text-muted)',
              fontSize: '14px',
            }}
          >
            Loading...
          </div>
        )}

        {/* Empty State */}
        {!isLoading && (
          <Command.Empty className="command-palette-empty">
            {emptyState || (
              <div
                style={{
                  padding: '24px',
                  textAlign: 'center',
                  color: 'var(--palette-text-muted)',
                  fontSize: '14px',
                }}
              >
                {searchQuery ? (
                  <>
                    <p style={{ marginBottom: '8px' }}>
                      No commands found for "{searchQuery}"
                    </p>
                    <p style={{ fontSize: '12px' }}>
                      Try checking your spelling or using different keywords
                    </p>
                  </>
                ) : (
                  <>
                    <p style={{ marginBottom: '8px' }}>No commands available</p>
                    <p style={{ fontSize: '12px' }}>
                      Try typing to search for commands
                    </p>
                  </>
                )}
              </div>
            )}
          </Command.Empty>
        )}

        {/* Grouped Commands */}
        {!isLoading &&
          commandGroups.map((group) => (
            <Command.Group
              key={group.id}
              heading={group.label}
              className="command-palette-group"
            >
              <div
                className="command-palette-group-heading"
                style={{
                  padding: '6px 8px',
                  fontSize: '12px',
                  fontWeight: 600,
                  color: 'var(--palette-text-muted)',
                  textTransform: 'uppercase',
                  letterSpacing: '0.5px',
                }}
              >
                {group.label}
              </div>

              {group.commands.map((command) => (
                <Command.Item
                  key={command.id}
                  value={command.id}
                  keywords={command.keywords}
                  onSelect={() => handleSelect(command.id)}
                  className="command-palette-item"
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '8px 12px',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    transition: 'background-color 150ms ease',
                  }}
                >
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '12px',
                      flex: 1,
                      minWidth: 0,
                    }}
                  >
                    {/* Icon */}
                    {command.icon && (
                      <div
                        className="command-palette-icon"
                        style={{
                          flexShrink: 0,
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          width: '20px',
                          height: '20px',
                        }}
                      >
                        {command.icon}
                      </div>
                    )}

                    {/* Label and Description */}
                    <div
                      style={{
                        flex: 1,
                        minWidth: 0,
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '2px',
                      }}
                    >
                      <div
                        className="command-palette-label"
                        style={{
                          fontSize: '14px',
                          fontWeight: 500,
                          color: 'var(--palette-text)',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          whiteSpace: 'nowrap',
                        }}
                      >
                        {command.label}
                        {command.badge && (
                          <span
                            className="command-palette-badge"
                            style={{
                              marginLeft: '8px',
                              padding: '2px 6px',
                              background: 'var(--palette-accent)',
                              color: 'white',
                              fontSize: '10px',
                              fontWeight: 600,
                              borderRadius: '4px',
                              textTransform: 'uppercase',
                            }}
                          >
                            {command.badge}
                          </span>
                        )}
                      </div>
                      {command.description && (
                        <div
                          className="command-palette-description"
                          style={{
                            fontSize: '12px',
                            color: 'var(--palette-text-muted)',
                            overflow: 'hidden',
                            textOverflow: 'ellipsis',
                            whiteSpace: 'nowrap',
                          }}
                        >
                          {command.description}
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Keyboard Shortcut */}
                  {command.shortcut && (
                    <div
                      className="command-palette-shortcut"
                      style={{
                        flexShrink: 0,
                        display: 'flex',
                        gap: '4px',
                        fontSize: '12px',
                        fontFamily: 'ui-monospace, monospace',
                        color: 'var(--palette-shortcut-text)',
                      }}
                    >
                      {formatShortcut(command.shortcut)
                        .split('')
                        .map((key, i) => (
                          <kbd
                            key={i}
                            style={{
                              padding: '2px 6px',
                              background: 'var(--palette-shortcut-bg)',
                              border: '1px solid var(--palette-shortcut-border)',
                              borderRadius: '4px',
                              lineHeight: 1,
                            }}
                          >
                            {key}
                          </kbd>
                        ))}
                    </div>
                  )}
                </Command.Item>
              ))}
            </Command.Group>
          ))}
      </Command.List>

      {/* Footer */}
      {footer && (
        <div
          className="command-palette-footer"
          style={{
            padding: '8px 16px',
            borderTop: '1px solid var(--palette-border)',
            background: 'var(--palette-bg-secondary)',
          }}
        >
          {footer}
        </div>
      )}

      {/* Inline Styles for Selected/Hover States */}
      <style>{`
        .command-palette-item[aria-selected="true"] {
          background-color: var(--palette-selection-bg) !important;
        }

        .command-palette-item:hover {
          background-color: var(--palette-hover-bg) !important;
        }

        .command-palette-list::-webkit-scrollbar {
          width: 8px;
        }

        .command-palette-list::-webkit-scrollbar-track {
          background: transparent;
        }

        .command-palette-list::-webkit-scrollbar-thumb {
          background: var(--palette-border);
          border-radius: 4px;
        }

        .command-palette-list::-webkit-scrollbar-thumb:hover {
          background: var(--palette-text-muted);
        }

        @media (prefers-reduced-motion: reduce) {
          .command-palette-item {
            transition: none !important;
          }
        }
      `}</style>
    </Command>
  );
}

/**
 * Default keyboard legend footer component
 */
export function KeyboardLegend() {
  return (
    <div
      style={{
        display: 'flex',
        gap: '16px',
        fontSize: '12px',
        color: 'var(--palette-text-muted)',
      }}
    >
      <span>↑↓ to navigate</span>
      <span>↵ to select</span>
      <span>esc to close</span>
    </div>
  );
}
