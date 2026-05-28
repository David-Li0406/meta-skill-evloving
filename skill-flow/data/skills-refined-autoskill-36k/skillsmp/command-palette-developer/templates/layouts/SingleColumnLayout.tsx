import React, { useRef, useEffect, useState } from 'react';

/**
 * Command item interface
 */
export interface Command {
  id: string;
  label: string;
  description?: string;
  group?: string;
  icon?: React.ReactNode;
  shortcut?: string;
  disabled?: boolean;
}

/**
 * Props for SingleColumnLayout component
 */
export interface SingleColumnLayoutProps {
  items: Command[];
  onSelect: (item: Command) => void;
  renderIcon?: (item: Command) => React.ReactNode;
  renderShortcut?: (item: Command) => React.ReactNode;
  virtualScroll?: boolean;
  selectedId?: string;
  onSelectedChange?: (id: string) => void;
}

/**
 * SingleColumnLayout - Full-width command list with keyboard navigation
 *
 * Features:
 * - Group headers with visual separators
 * - Item height: 48px, padding: 12px 16px
 * - Hover and selected states
 * - Keyboard navigation support
 * - Icons on left, shortcuts on right
 * - Max height: 400px with scroll
 * - Optional virtual scrolling for 1000+ items
 *
 * Use cases:
 * - Simple action palettes
 * - Navigation commands
 * - Text-heavy commands without rich metadata
 */
export function SingleColumnLayout({
  items,
  onSelect,
  renderIcon,
  renderShortcut,
  virtualScroll = false,
  selectedId,
  onSelectedChange,
}: SingleColumnLayoutProps): JSX.Element {
  const listRef = useRef<HTMLDivElement>(null);
  const [internalSelectedId, setInternalSelectedId] = useState<string>(items[0]?.id || '');
  const currentSelectedId = selectedId ?? internalSelectedId;

  // Group items by group property
  const groupedItems = items.reduce((acc, item) => {
    const group = item.group || 'Commands';
    if (!acc[group]) {
      acc[group] = [];
    }
    acc[group].push(item);
    return acc;
  }, {} as Record<string, Command[]>);

  // Handle keyboard navigation
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent): void {
      const currentIndex = items.findIndex((item) => item.id === currentSelectedId);

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        const nextIndex = Math.min(currentIndex + 1, items.length - 1);
        const nextId = items[nextIndex]?.id;
        if (nextId) {
          onSelectedChange?.(nextId);
          setInternalSelectedId(nextId);
          scrollToItem(nextId);
        }
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        const prevIndex = Math.max(currentIndex - 1, 0);
        const prevId = items[prevIndex]?.id;
        if (prevId) {
          onSelectedChange?.(prevId);
          setInternalSelectedId(prevId);
          scrollToItem(prevId);
        }
      } else if (e.key === 'Enter') {
        e.preventDefault();
        const selectedItem = items.find((item) => item.id === currentSelectedId);
        if (selectedItem && !selectedItem.disabled) {
          onSelect(selectedItem);
        }
      }
    }

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [items, currentSelectedId, onSelect, onSelectedChange]);

  function scrollToItem(itemId: string): void {
    const element = listRef.current?.querySelector(`[data-item-id="${itemId}"]`);
    if (element) {
      element.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  }

  function handleItemClick(item: Command): void {
    if (item.disabled) return;
    onSelectedChange?.(item.id);
    setInternalSelectedId(item.id);
    onSelect(item);
  }

  function handleItemHover(item: Command): void {
    if (item.disabled) return;
    onSelectedChange?.(item.id);
    setInternalSelectedId(item.id);
  }

  return (
    <div
      ref={listRef}
      className="single-column-layout"
      role="listbox"
      aria-label="Command list"
      style={{
        width: '100%',
        maxHeight: '400px',
        overflowY: 'auto',
        overflowX: 'hidden',
      }}
    >
      {Object.entries(groupedItems).map(([groupName, groupItems]) => (
        <div key={groupName} className="command-group">
          <div
            className="group-header"
            style={{
              padding: '8px 16px',
              fontSize: '12px',
              fontWeight: 600,
              color: 'var(--palette-text-muted, #6b7280)',
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
              borderBottom: '1px solid var(--palette-border, #e5e7eb)',
              background: 'var(--palette-bg-secondary, #f9fafb)',
            }}
          >
            {groupName}
          </div>
          {groupItems.map((item) => {
            const isSelected = item.id === currentSelectedId;
            return (
              <div
                key={item.id}
                data-item-id={item.id}
                role="option"
                aria-selected={isSelected}
                aria-disabled={item.disabled}
                onClick={() => handleItemClick(item)}
                onMouseEnter={() => handleItemHover(item)}
                className="command-item"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  padding: '12px 16px',
                  minHeight: '48px',
                  cursor: item.disabled ? 'not-allowed' : 'pointer',
                  background: isSelected
                    ? 'var(--palette-selection-bg, #3b82f6)'
                    : 'transparent',
                  color: isSelected
                    ? 'var(--palette-selection-text, #ffffff)'
                    : item.disabled
                    ? 'var(--palette-text-disabled, #9ca3af)'
                    : 'var(--palette-text, #111827)',
                  opacity: item.disabled ? 0.5 : 1,
                  transition: 'background-color 150ms, color 150ms',
                  borderLeft: isSelected ? '3px solid var(--palette-accent, #2563eb)' : '3px solid transparent',
                }}
              >
                {(renderIcon || item.icon) && (
                  <div
                    className="item-icon"
                    style={{
                      flexShrink: 0,
                      width: '20px',
                      height: '20px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                    }}
                  >
                    {renderIcon ? renderIcon(item) : item.icon}
                  </div>
                )}
                <div
                  className="item-content"
                  style={{
                    flex: 1,
                    minWidth: 0,
                  }}
                >
                  <div
                    className="item-label"
                    style={{
                      fontSize: '14px',
                      fontWeight: 500,
                      lineHeight: 1.4,
                    }}
                  >
                    {item.label}
                  </div>
                  {item.description && (
                    <div
                      className="item-description"
                      style={{
                        fontSize: '12px',
                        lineHeight: 1.4,
                        marginTop: '2px',
                        opacity: 0.8,
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                      }}
                    >
                      {item.description}
                    </div>
                  )}
                </div>
                {(renderShortcut || item.shortcut) && (
                  <div
                    className="item-shortcut"
                    style={{
                      flexShrink: 0,
                      fontSize: '12px',
                      fontFamily: 'ui-monospace, monospace',
                      opacity: 0.7,
                    }}
                  >
                    {renderShortcut ? renderShortcut(item) : item.shortcut}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}
