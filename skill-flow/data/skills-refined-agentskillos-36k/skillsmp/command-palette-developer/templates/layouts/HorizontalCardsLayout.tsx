import React, { useState, useEffect, useRef } from 'react';
import type { CardItem } from './CardGridLayout';

/**
 * Props for HorizontalCardsLayout component
 */
export interface HorizontalCardsLayoutProps {
  items: CardItem[];
  onSelect: (item: CardItem) => void;
  showDots?: boolean;
  showArrows?: boolean;
  renderCard?: (item: CardItem, isSelected: boolean) => React.ReactNode;
  selectedId?: string;
  onSelectedChange?: (id: string) => void;
}

/**
 * HorizontalCardsLayout - Horizontal scrolling cards with snap
 *
 * Features:
 * - Horizontal scrolling cards
 * - Card width: 280px, height: 120px
 * - Snap-to-card scrolling (CSS scroll-snap)
 * - Navigation dots indicator
 * - Left/right arrow buttons
 * - Keyboard: left/right arrows to navigate
 * - Selected card centered in viewport
 *
 * Use cases:
 * - Mixed content types (cards + lists)
 * - Recent items showcase
 * - Contextual grouped results
 */
export function HorizontalCardsLayout({
  items,
  onSelect,
  showDots = true,
  showArrows = true,
  renderCard,
  selectedId,
  onSelectedChange,
}: HorizontalCardsLayoutProps): JSX.Element {
  const [internalSelectedId, setInternalSelectedId] = useState<string>(items[0]?.id || '');
  const currentSelectedId = selectedId ?? internalSelectedId;
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(true);

  // Update scroll button states
  function updateScrollButtons(): void {
    const container = scrollContainerRef.current;
    if (!container) return;

    setCanScrollLeft(container.scrollLeft > 0);
    setCanScrollRight(
      container.scrollLeft < container.scrollWidth - container.clientWidth - 1
    );
  }

  useEffect(() => {
    const container = scrollContainerRef.current;
    if (!container) return;

    updateScrollButtons();
    container.addEventListener('scroll', updateScrollButtons);
    return () => container.removeEventListener('scroll', updateScrollButtons);
  }, [items]);

  // Keyboard navigation
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent): void {
      const currentIndex = items.findIndex((item) => item.id === currentSelectedId);
      if (currentIndex === -1) return;

      let nextIndex = currentIndex;

      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        e.preventDefault();
        nextIndex = Math.min(currentIndex + 1, items.length - 1);
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        e.preventDefault();
        nextIndex = Math.max(currentIndex - 1, 0);
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
  }, [items, currentSelectedId, onSelect, onSelectedChange]);

  function scrollToCard(itemId: string): void {
    const element = scrollContainerRef.current?.querySelector(`[data-card-id="${itemId}"]`);
    if (element) {
      element.scrollIntoView({
        behavior: 'smooth',
        block: 'nearest',
        inline: 'center',
      });
    }
  }

  function handleCardClick(item: CardItem): void {
    if (item.disabled) return;
    onSelectedChange?.(item.id);
    setInternalSelectedId(item.id);
    scrollToCard(item.id);
    onSelect(item);
  }

  function handleCardHover(item: CardItem): void {
    if (item.disabled) return;
    onSelectedChange?.(item.id);
    setInternalSelectedId(item.id);
  }

  function scrollLeft(): void {
    const container = scrollContainerRef.current;
    if (!container) return;
    container.scrollBy({ left: -300, behavior: 'smooth' });
  }

  function scrollRight(): void {
    const container = scrollContainerRef.current;
    if (!container) return;
    container.scrollBy({ left: 300, behavior: 'smooth' });
  }

  function scrollToDot(index: number): void {
    const item = items[index];
    if (item) {
      onSelectedChange?.(item.id);
      setInternalSelectedId(item.id);
      scrollToCard(item.id);
    }
  }

  const DefaultCard = ({ item, isSelected }: { item: CardItem; isSelected: boolean }) => (
    <div
      style={{
        display: 'flex',
        gap: '12px',
        padding: '16px',
        width: '280px',
        height: '120px',
        background: 'var(--palette-bg, #ffffff)',
        border: isSelected
          ? '2px solid var(--palette-accent, #3b82f6)'
          : '1px solid var(--palette-border, #e5e7eb)',
        borderRadius: '8px',
        cursor: item.disabled ? 'not-allowed' : 'pointer',
        opacity: item.disabled ? 0.5 : 1,
        transition: 'transform 150ms, box-shadow 150ms, border-color 150ms',
        flexShrink: 0,
        scrollSnapAlign: 'start',
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
      {/* Icon or thumbnail */}
      {item.image ? (
        <img
          src={item.image}
          alt={item.title}
          style={{
            width: '60px',
            height: '100%',
            objectFit: 'cover',
            borderRadius: '6px',
            flexShrink: 0,
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
            flexShrink: 0,
          }}
        >
          {item.icon}
        </div>
      ) : null}

      {/* Content */}
      <div
        style={{
          flex: 1,
          minWidth: 0,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
        }}
      >
        <div>
          <h3
            style={{
              fontSize: '14px',
              fontWeight: 600,
              lineHeight: 1.4,
              color: 'var(--palette-text, #111827)',
              margin: 0,
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap',
            }}
          >
            {item.title}
          </h3>
          {item.description && (
            <p
              style={{
                fontSize: '12px',
                lineHeight: 1.5,
                color: 'var(--palette-text-muted, #6b7280)',
                margin: '4px 0 0 0',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap',
              }}
            >
              {item.description}
            </p>
          )}
        </div>

        {/* Badges */}
        {item.badges && item.badges.length > 0 && (
          <div
            style={{
              display: 'flex',
              gap: '6px',
              flexWrap: 'wrap',
            }}
          >
            {item.badges.slice(0, 2).map((badge, index) => (
              <span key={index}>{badge}</span>
            ))}
          </div>
        )}
      </div>
    </div>
  );

  return (
    <div className="horizontal-cards-layout" style={{ position: 'relative', width: '100%' }}>
      {/* Scroll container */}
      <div style={{ position: 'relative' }}>
        {/* Left arrow */}
        {showArrows && canScrollLeft && (
          <button
            onClick={scrollLeft}
            style={{
              position: 'absolute',
              left: '8px',
              top: '50%',
              transform: 'translateY(-50%)',
              zIndex: 10,
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              background: 'var(--palette-bg, #ffffff)',
              border: '1px solid var(--palette-border, #e5e7eb)',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'background-color 150ms',
            }}
            aria-label="Scroll left"
          >
            ←
          </button>
        )}

        {/* Right arrow */}
        {showArrows && canScrollRight && (
          <button
            onClick={scrollRight}
            style={{
              position: 'absolute',
              right: '8px',
              top: '50%',
              transform: 'translateY(-50%)',
              zIndex: 10,
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              background: 'var(--palette-bg, #ffffff)',
              border: '1px solid var(--palette-border, #e5e7eb)',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              transition: 'background-color 150ms',
            }}
            aria-label="Scroll right"
          >
            →
          </button>
        )}

        {/* Cards */}
        <div
          ref={scrollContainerRef}
          className="horizontal-scroll"
          role="list"
          aria-label="Horizontal cards"
          style={{
            display: 'flex',
            gap: '12px',
            overflowX: 'auto',
            overflowY: 'hidden',
            padding: '8px 16px 12px',
            scrollSnapType: 'x mandatory',
            WebkitOverflowScrolling: 'touch',
            scrollbarWidth: 'thin',
          }}
        >
          {items.map((item) => {
            const isSelected = item.id === currentSelectedId;
            return (
              <div
                key={item.id}
                data-card-id={item.id}
                role="listitem"
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
        </div>
      </div>

      {/* Navigation dots */}
      {showDots && items.length > 1 && (
        <div
          style={{
            display: 'flex',
            justifyContent: 'center',
            gap: '8px',
            padding: '12px',
          }}
        >
          {items.map((item, index) => {
            const isSelected = item.id === currentSelectedId;
            return (
              <button
                key={item.id}
                onClick={() => scrollToDot(index)}
                aria-label={`Go to card ${index + 1}`}
                style={{
                  width: '8px',
                  height: '8px',
                  borderRadius: '50%',
                  background: isSelected
                    ? 'var(--palette-accent, #3b82f6)'
                    : 'var(--palette-border, #d1d5db)',
                  border: 'none',
                  cursor: 'pointer',
                  transition: 'background-color 150ms',
                  padding: 0,
                }}
              />
            );
          })}
        </div>
      )}

      <style>{`
        .horizontal-scroll::-webkit-scrollbar {
          height: 6px;
        }
        .horizontal-scroll::-webkit-scrollbar-track {
          background: var(--palette-bg-secondary, #f3f4f6);
          border-radius: 3px;
        }
        .horizontal-scroll::-webkit-scrollbar-thumb {
          background: var(--palette-border, #d1d5db);
          border-radius: 3px;
        }
        .horizontal-scroll::-webkit-scrollbar-thumb:hover {
          background: var(--palette-text-muted, #9ca3af);
        }
        @media (max-width: 640px) {
          .horizontal-scroll {
            padding: 8px 12px 12px !important;
          }
        }
      `}</style>
    </div>
  );
}
