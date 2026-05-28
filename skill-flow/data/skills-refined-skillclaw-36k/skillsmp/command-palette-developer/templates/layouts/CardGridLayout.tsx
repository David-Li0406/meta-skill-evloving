import React, { useState, useEffect, useRef } from 'react';

/**
 * Card item interface with rich metadata
 */
export interface CardItem {
  id: string;
  title: string;
  description?: string;
  image?: string;
  icon?: React.ReactNode;
  badges?: React.ReactNode[];
  metadata?: Record<string, React.ReactNode>;
  disabled?: boolean;
}

/**
 * Props for CardGridLayout component
 */
export interface CardGridLayoutProps {
  items: CardItem[];
  columns?: number;
  onSelect: (item: CardItem) => void;
  renderCard?: (item: CardItem, isSelected: boolean) => React.ReactNode;
  selectedId?: string;
  onSelectedChange?: (id: string) => void;
}

/**
 * CardGridLayout - Responsive grid of cards
 *
 * Features:
 * - Responsive grid: 2-4 columns based on width
 * - Card size: min 200px × 180px
 * - Grid gap: 16px
 * - Card hover: shadow + scale(1.02)
 * - Card selected: accent border (2px)
 * - Grid-aware keyboard navigation (arrow keys)
 * - Image thumbnail support
 *
 * Use cases:
 * - Extension stores
 * - Plugin browsers
 * - Visual galleries
 * - Items with images and rich metadata
 */
export function CardGridLayout({
  items,
  columns,
  onSelect,
  renderCard,
  selectedId,
  onSelectedChange,
}: CardGridLayoutProps): JSX.Element {
  const [internalSelectedId, setInternalSelectedId] = useState<string>(items[0]?.id || '');
  const currentSelectedId = selectedId ?? internalSelectedId;
  const gridRef = useRef<HTMLDivElement>(null);
  const [columnCount, setColumnCount] = useState(columns || 3);

  // Calculate responsive column count
  useEffect(() => {
    if (columns) {
      setColumnCount(columns);
      return;
    }

    function calculateColumns(): void {
      const width = window.innerWidth;
      if (width < 640) {
        setColumnCount(1);
      } else if (width < 1024) {
        setColumnCount(2);
      } else if (width < 1280) {
        setColumnCount(3);
      } else {
        setColumnCount(4);
      }
    }

    calculateColumns();
    window.addEventListener('resize', calculateColumns);
    return () => window.removeEventListener('resize', calculateColumns);
  }, [columns]);

  // Grid-aware keyboard navigation
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent): void {
      const currentIndex = items.findIndex((item) => item.id === currentSelectedId);
      if (currentIndex === -1) return;

      let nextIndex = currentIndex;

      if (e.key === 'ArrowRight') {
        e.preventDefault();
        nextIndex = Math.min(currentIndex + 1, items.length - 1);
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        nextIndex = Math.max(currentIndex - 1, 0);
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        nextIndex = Math.min(currentIndex + columnCount, items.length - 1);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        nextIndex = Math.max(currentIndex - columnCount, 0);
      } else if (e.key === 'Enter') {
        e.preventDefault();
        const selectedItem = items[currentIndex];
        if (selectedItem && !selectedItem.disabled) {
          onSelect(selectedItem);
        }
        return;
      } else if (e.key === 'Home') {
        e.preventDefault();
        nextIndex = 0;
      } else if (e.key === 'End') {
        e.preventDefault();
        nextIndex = items.length - 1;
      } else {
        return;
      }

      const nextId = items[nextIndex]?.id;
      if (nextId) {
        onSelectedChange?.(nextId);
        setInternalSelectedId(nextId);
        scrollToCard(nextId);
      }
    }

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [items, currentSelectedId, columnCount, onSelect, onSelectedChange]);

  function scrollToCard(itemId: string): void {
    const element = gridRef.current?.querySelector(`[data-card-id="${itemId}"]`);
    if (element) {
      element.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  }

  function handleCardClick(item: CardItem): void {
    if (item.disabled) return;
    onSelectedChange?.(item.id);
    setInternalSelectedId(item.id);
    onSelect(item);
  }

  function handleCardHover(item: CardItem): void {
    if (item.disabled) return;
    onSelectedChange?.(item.id);
    setInternalSelectedId(item.id);
  }

  const DefaultCard = ({ item, isSelected }: { item: CardItem; isSelected: boolean }) => (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        gap: '12px',
        padding: '16px',
        minHeight: '180px',
        background: 'var(--palette-bg, #ffffff)',
        border: isSelected
          ? '2px solid var(--palette-accent, #3b82f6)'
          : '1px solid var(--palette-border, #e5e7eb)',
        borderRadius: '8px',
        cursor: item.disabled ? 'not-allowed' : 'pointer',
        opacity: item.disabled ? 0.5 : 1,
        transition: 'transform 150ms, box-shadow 150ms, border-color 150ms',
        transform: isSelected ? 'scale(1.02)' : 'scale(1)',
        boxShadow: isSelected
          ? '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)'
          : '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
      }}
      onMouseEnter={(e) => {
        if (!item.disabled) {
          e.currentTarget.style.transform = 'scale(1.02)';
          e.currentTarget.style.boxShadow =
            '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)';
        }
      }}
      onMouseLeave={(e) => {
        if (!isSelected) {
          e.currentTarget.style.transform = 'scale(1)';
          e.currentTarget.style.boxShadow =
            '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)';
        }
      }}
    >
      {/* Image or icon */}
      {item.image ? (
        <img
          src={item.image}
          alt={item.title}
          style={{
            width: '100%',
            height: '100px',
            objectFit: 'cover',
            borderRadius: '6px',
          }}
        />
      ) : item.icon ? (
        <div
          style={{
            width: '48px',
            height: '48px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'var(--palette-bg-secondary, #f3f4f6)',
            borderRadius: '8px',
          }}
        >
          {item.icon}
        </div>
      ) : null}

      {/* Title */}
      <h3
        style={{
          fontSize: '14px',
          fontWeight: 600,
          lineHeight: 1.4,
          color: 'var(--palette-text, #111827)',
          margin: 0,
        }}
      >
        {item.title}
      </h3>

      {/* Description */}
      {item.description && (
        <p
          style={{
            fontSize: '12px',
            lineHeight: 1.5,
            color: 'var(--palette-text-muted, #6b7280)',
            margin: 0,
            flex: 1,
            overflow: 'hidden',
            display: '-webkit-box',
            WebkitLineClamp: 2,
            WebkitBoxOrient: 'vertical',
          }}
        >
          {item.description}
        </p>
      )}

      {/* Badges */}
      {item.badges && item.badges.length > 0 && (
        <div
          style={{
            display: 'flex',
            gap: '6px',
            flexWrap: 'wrap',
          }}
        >
          {item.badges.map((badge, index) => (
            <span key={index}>{badge}</span>
          ))}
        </div>
      )}

      {/* Metadata */}
      {item.metadata && Object.keys(item.metadata).length > 0 && (
        <div
          style={{
            display: 'flex',
            gap: '12px',
            fontSize: '12px',
            color: 'var(--palette-text-muted, #6b7280)',
            paddingTop: '8px',
            borderTop: '1px solid var(--palette-border, #e5e7eb)',
          }}
        >
          {Object.entries(item.metadata).map(([key, value]) => (
            <div key={key} style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              {value}
            </div>
          ))}
        </div>
      )}
    </div>
  );

  return (
    <div
      ref={gridRef}
      className="card-grid-layout"
      role="grid"
      aria-label="Card grid"
      style={{
        display: 'grid',
        gridTemplateColumns: `repeat(${columnCount}, minmax(200px, 1fr))`,
        gap: '16px',
        padding: '16px',
        maxHeight: '600px',
        overflowY: 'auto',
        width: '100%',
      }}
    >
      {items.map((item) => {
        const isSelected = item.id === currentSelectedId;
        return (
          <div
            key={item.id}
            data-card-id={item.id}
            role="gridcell"
            aria-selected={isSelected}
            aria-disabled={item.disabled}
            onClick={() => handleCardClick(item)}
            onMouseEnter={() => handleCardHover(item)}
            tabIndex={isSelected ? 0 : -1}
          >
            {renderCard ? renderCard(item, isSelected) : <DefaultCard item={item} isSelected={isSelected} />}
          </div>
        );
      })}

      <style>{`
        @media (max-width: 1024px) {
          .card-grid-layout {
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)) !important;
          }
        }
        @media (max-width: 640px) {
          .card-grid-layout {
            grid-template-columns: 1fr !important;
          }
        }
      `}</style>
    </div>
  );
}
