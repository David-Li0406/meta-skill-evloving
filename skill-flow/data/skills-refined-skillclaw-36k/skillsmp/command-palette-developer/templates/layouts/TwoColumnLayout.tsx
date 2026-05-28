import React, { useState, useRef, useEffect } from 'react';
import type { Command } from './SingleColumnLayout';

/**
 * Props for TwoColumnLayout component
 */
export interface TwoColumnLayoutProps {
  items: Command[];
  onSelect: (item: Command) => void;
  renderPreview: (item: Command | null) => React.ReactNode;
  defaultSplit?: number;
  resizable?: boolean;
}

/**
 * TwoColumnLayout - Split view with list and preview
 *
 * Features:
 * - Split view: 40% list | 60% preview (configurable)
 * - List column shows command items
 * - Preview column shows detailed view
 * - Optional resize handle between columns
 * - Responsive: stacks on mobile (<768px)
 * - Preview updates on selection change
 * - Smooth transition (150ms) on preview change
 *
 * Use cases:
 * - File browsers with preview
 * - Document search with content preview
 * - Repository pickers with details
 */
export function TwoColumnLayout({
  items,
  onSelect,
  renderPreview,
  defaultSplit = 40,
  resizable = false,
}: TwoColumnLayoutProps): JSX.Element {
  const [selectedItem, setSelectedItem] = useState<Command | null>(items[0] || null);
  const [splitPercent, setSplitPercent] = useState(defaultSplit);
  const [isResizing, setIsResizing] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const listRef = useRef<HTMLDivElement>(null);

  // Handle item selection
  function handleItemSelect(item: Command): void {
    setSelectedItem(item);
  }

  function handleItemExecute(item: Command): void {
    onSelect(item);
  }

  // Handle resize
  function handleResizeStart(e: React.MouseEvent): void {
    if (!resizable) return;
    e.preventDefault();
    setIsResizing(true);
  }

  useEffect(() => {
    if (!isResizing) return;

    function handleMouseMove(e: MouseEvent): void {
      if (!containerRef.current) return;
      const containerRect = containerRef.current.getBoundingClientRect();
      const newPercent = ((e.clientX - containerRect.left) / containerRect.width) * 100;
      setSplitPercent(Math.min(Math.max(newPercent, 20), 80));
    }

    function handleMouseUp(): void {
      setIsResizing(false);
    }

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isResizing]);

  // Keyboard navigation
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent): void {
      const currentIndex = items.findIndex((item) => item.id === selectedItem?.id);

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        const nextIndex = Math.min(currentIndex + 1, items.length - 1);
        const nextItem = items[nextIndex];
        if (nextItem) {
          setSelectedItem(nextItem);
          scrollToItem(nextItem.id);
        }
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        const prevIndex = Math.max(currentIndex - 1, 0);
        const prevItem = items[prevIndex];
        if (prevItem) {
          setSelectedItem(prevItem);
          scrollToItem(prevItem.id);
        }
      } else if (e.key === 'Enter' && selectedItem) {
        e.preventDefault();
        if (!selectedItem.disabled) {
          handleItemExecute(selectedItem);
        }
      }
    }

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [items, selectedItem]);

  function scrollToItem(itemId: string): void {
    const element = listRef.current?.querySelector(`[data-item-id="${itemId}"]`);
    if (element) {
      element.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  }

  return (
    <div
      ref={containerRef}
      className="two-column-layout"
      style={{
        display: 'flex',
        width: '100%',
        height: '600px',
        maxHeight: '80vh',
        gap: '1px',
        background: 'var(--palette-separator, #e5e7eb)',
      }}
    >
      {/* Left pane: List */}
      <div
        ref={listRef}
        className="left-pane"
        role="listbox"
        aria-label="Command list"
        style={{
          flex: `0 0 ${splitPercent}%`,
          minWidth: '250px',
          background: 'var(--palette-bg, #ffffff)',
          overflowY: 'auto',
          overflowX: 'hidden',
          borderRight: '1px solid var(--palette-border, #e5e7eb)',
        }}
      >
        {items.map((item) => {
          const isSelected = item.id === selectedItem?.id;
          return (
            <div
              key={item.id}
              data-item-id={item.id}
              role="option"
              aria-selected={isSelected}
              aria-disabled={item.disabled}
              onClick={() => {
                handleItemSelect(item);
              }}
              onDoubleClick={() => {
                if (!item.disabled) {
                  handleItemExecute(item);
                }
              }}
              className="list-item"
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px 16px',
                minHeight: '48px',
                cursor: item.disabled ? 'not-allowed' : 'pointer',
                background: isSelected
                  ? 'var(--palette-selection-bg, #eff6ff)'
                  : 'transparent',
                color: item.disabled
                  ? 'var(--palette-text-disabled, #9ca3af)'
                  : 'var(--palette-text, #111827)',
                borderLeft: isSelected ? '3px solid var(--palette-accent, #3b82f6)' : '3px solid transparent',
                opacity: item.disabled ? 0.5 : 1,
                transition: 'background-color 150ms',
              }}
            >
              {item.icon && (
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
                  {item.icon}
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
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
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
                      color: 'var(--palette-text-muted, #6b7280)',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {item.description}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Resize handle */}
      {resizable && (
        <div
          className="resize-handle"
          onMouseDown={handleResizeStart}
          style={{
            width: '4px',
            cursor: 'col-resize',
            background: isResizing ? 'var(--palette-accent, #3b82f6)' : 'transparent',
            transition: 'background-color 150ms',
            position: 'relative',
            zIndex: 10,
          }}
          aria-label="Resize columns"
        />
      )}

      {/* Right pane: Preview */}
      <div
        className="right-pane preview-panel"
        style={{
          flex: 1,
          minWidth: '300px',
          background: 'var(--palette-bg, #ffffff)',
          overflowY: 'auto',
          padding: '16px',
          transition: 'opacity 150ms',
        }}
      >
        {selectedItem ? (
          renderPreview(selectedItem)
        ) : (
          <div
            className="empty-preview"
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
              color: 'var(--palette-text-muted, #6b7280)',
              fontSize: '14px',
            }}
          >
            Select an item to preview
          </div>
        )}
      </div>

      <style>{`
        @media (max-width: 768px) {
          .two-column-layout {
            flex-direction: column !important;
          }
          .left-pane {
            flex: 0 0 auto !important;
            max-height: 300px;
            border-right: none !important;
            border-bottom: 1px solid var(--palette-border, #e5e7eb);
          }
          .right-pane {
            flex: 1 !important;
            min-height: 300px;
          }
          .resize-handle {
            display: none;
          }
        }
      `}</style>
    </div>
  );
}
