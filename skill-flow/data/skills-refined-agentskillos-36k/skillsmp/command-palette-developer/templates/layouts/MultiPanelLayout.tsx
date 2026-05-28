import React, { useState, useEffect, useRef, useMemo } from 'react';
import type { Command } from './SingleColumnLayout';

/**
 * Filter option interface
 */
export interface Filter {
  id: string;
  label: string;
  type: 'checkbox' | 'radio';
  options: FilterOption[];
  value?: string | string[];
}

export interface FilterOption {
  id: string;
  label: string;
  count?: number;
}

/**
 * Props for MultiPanelLayout component
 */
export interface MultiPanelLayoutProps {
  items: Command[];
  filters: Filter[];
  onFilterChange: (filterId: string, value: string | string[]) => void;
  renderDetails: (item: Command | null) => React.ReactNode;
  onSelect: (item: Command) => void;
}

/**
 * MultiPanelLayout - Three-panel layout for complex filtering
 *
 * Features:
 * - Three panels: filters (left 25%) | results (center 50%) | details (right 25%)
 * - Filter panel with checkboxes and radio groups
 * - Collapsible side panels
 * - Responsive: collapses to tabs/modals on mobile
 * - Panel state persisted in localStorage
 *
 * Use cases:
 * - Complex filtering interfaces
 * - Data tables with details
 * - Admin dashboards
 * - Advanced search interfaces
 */
export function MultiPanelLayout({
  items,
  filters,
  onFilterChange,
  renderDetails,
  onSelect,
}: MultiPanelLayoutProps): JSX.Element {
  const [selectedItem, setSelectedItem] = useState<Command | null>(null);
  const [filterPanelCollapsed, setFilterPanelCollapsed] = useState(false);
  const [detailsPanelCollapsed, setDetailsPanelCollapsed] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [showFilterModal, setShowFilterModal] = useState(false);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const resultsRef = useRef<HTMLDivElement>(null);

  // Load panel state from localStorage
  useEffect(() => {
    const savedState = localStorage.getItem('multi-panel-state');
    if (savedState) {
      try {
        const { filterCollapsed, detailsCollapsed } = JSON.parse(savedState);
        setFilterPanelCollapsed(filterCollapsed ?? false);
        setDetailsPanelCollapsed(detailsCollapsed ?? false);
      } catch {
        // Ignore parse errors
      }
    }
  }, []);

  // Save panel state to localStorage
  useEffect(() => {
    localStorage.setItem(
      'multi-panel-state',
      JSON.stringify({
        filterCollapsed: filterPanelCollapsed,
        detailsCollapsed: detailsPanelCollapsed,
      })
    );
  }, [filterPanelCollapsed, detailsPanelCollapsed]);

  // Handle responsive breakpoints
  useEffect(() => {
    function handleResize(): void {
      setIsMobile(window.innerWidth < 768);
    }
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  // Keyboard navigation
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent): void {
      const currentIndex = items.findIndex((item) => item.id === selectedItem?.id);

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        const nextIndex = currentIndex === -1 ? 0 : Math.min(currentIndex + 1, items.length - 1);
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
      } else if (e.key === 'Enter' && selectedItem && !selectedItem.disabled) {
        e.preventDefault();
        onSelect(selectedItem);
      }
    }

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [items, selectedItem, onSelect]);

  function scrollToItem(itemId: string): void {
    const element = resultsRef.current?.querySelector(`[data-item-id="${itemId}"]`);
    if (element) {
      element.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  }

  function handleItemClick(item: Command): void {
    setSelectedItem(item);
    if (isMobile) {
      setShowDetailsModal(true);
    }
  }

  function handleItemExecute(item: Command): void {
    if (!item.disabled) {
      onSelect(item);
    }
  }

  const FilterPanel = () => (
    <aside
      className="filter-panel"
      style={{
        display: filterPanelCollapsed && !isMobile ? 'none' : 'flex',
        flexDirection: 'column',
        width: isMobile ? '100%' : '240px',
        background: 'var(--palette-bg, #ffffff)',
        borderRight: isMobile ? 'none' : '1px solid var(--palette-border, #e5e7eb)',
        overflowY: 'auto',
        padding: '16px',
      }}
    >
      <h3
        style={{
          fontSize: '14px',
          fontWeight: 600,
          marginBottom: '16px',
          color: 'var(--palette-text, #111827)',
        }}
      >
        Filters
      </h3>
      {filters.map((filter) => (
        <div
          key={filter.id}
          className="filter-group"
          style={{ marginBottom: '20px' }}
        >
          <div
            style={{
              fontSize: '12px',
              fontWeight: 600,
              marginBottom: '8px',
              color: 'var(--palette-text-muted, #6b7280)',
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
            }}
          >
            {filter.label}
          </div>
          {filter.options.map((option) => (
            <label
              key={option.id}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '6px 0',
                cursor: 'pointer',
                fontSize: '14px',
              }}
            >
              <input
                type={filter.type}
                name={filter.id}
                value={option.id}
                checked={
                  filter.type === 'radio'
                    ? filter.value === option.id
                    : Array.isArray(filter.value) && filter.value.includes(option.id)
                }
                onChange={(e) => {
                  if (filter.type === 'radio') {
                    onFilterChange(filter.id, e.target.value);
                  } else {
                    const currentValues = (filter.value as string[]) || [];
                    const newValues = e.target.checked
                      ? [...currentValues, option.id]
                      : currentValues.filter((v) => v !== option.id);
                    onFilterChange(filter.id, newValues);
                  }
                }}
                style={{ cursor: 'pointer' }}
              />
              <span style={{ flex: 1 }}>{option.label}</span>
              {option.count !== undefined && (
                <span
                  style={{
                    fontSize: '12px',
                    color: 'var(--palette-text-muted, #6b7280)',
                  }}
                >
                  {option.count}
                </span>
              )}
            </label>
          ))}
        </div>
      ))}
    </aside>
  );

  const DetailsPanel = () => (
    <aside
      className="details-panel"
      style={{
        display: detailsPanelCollapsed && !isMobile ? 'none' : 'flex',
        flexDirection: 'column',
        width: isMobile ? '100%' : '360px',
        background: 'var(--palette-bg, #ffffff)',
        borderLeft: isMobile ? 'none' : '1px solid var(--palette-border, #e5e7eb)',
        overflowY: 'auto',
        padding: '16px',
      }}
    >
      {renderDetails(selectedItem)}
    </aside>
  );

  if (isMobile) {
    return (
      <>
        <div className="multi-panel-mobile" style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
          {/* Filter toggle button */}
          <button
            onClick={() => setShowFilterModal(true)}
            style={{
              padding: '12px 16px',
              borderBottom: '1px solid var(--palette-border, #e5e7eb)',
              background: 'var(--palette-bg, #ffffff)',
              textAlign: 'left',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: 500,
            }}
          >
            Filters ({filters.reduce((acc, f) => acc + (Array.isArray(f.value) ? f.value.length : f.value ? 1 : 0), 0)})
          </button>

          {/* Results */}
          <div
            ref={resultsRef}
            className="results-panel"
            style={{
              flex: 1,
              overflowY: 'auto',
              background: 'var(--palette-bg, #ffffff)',
            }}
          >
            {items.map((item) => {
              const isSelected = item.id === selectedItem?.id;
              return (
                <div
                  key={item.id}
                  data-item-id={item.id}
                  onClick={() => handleItemClick(item)}
                  style={{
                    padding: '12px 16px',
                    borderBottom: '1px solid var(--palette-border, #e5e7eb)',
                    background: isSelected ? 'var(--palette-selection-bg, #eff6ff)' : 'transparent',
                    cursor: 'pointer',
                  }}
                >
                  <div style={{ fontSize: '14px', fontWeight: 500 }}>{item.label}</div>
                  {item.description && (
                    <div style={{ fontSize: '12px', color: 'var(--palette-text-muted, #6b7280)', marginTop: '4px' }}>
                      {item.description}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Filter modal */}
        {showFilterModal && (
          <div
            className="modal-overlay"
            onClick={() => setShowFilterModal(false)}
            style={{
              position: 'fixed',
              inset: 0,
              background: 'rgba(0, 0, 0, 0.5)',
              display: 'flex',
              alignItems: 'flex-end',
              zIndex: 1000,
            }}
          >
            <div
              onClick={(e) => e.stopPropagation()}
              style={{
                width: '100%',
                maxHeight: '80vh',
                background: 'var(--palette-bg, #ffffff)',
                borderRadius: '16px 16px 0 0',
                overflowY: 'auto',
              }}
            >
              <FilterPanel />
              <button
                onClick={() => setShowFilterModal(false)}
                style={{
                  width: '100%',
                  padding: '16px',
                  background: 'var(--palette-accent, #3b82f6)',
                  color: 'white',
                  fontWeight: 500,
                  cursor: 'pointer',
                }}
              >
                Apply Filters
              </button>
            </div>
          </div>
        )}

        {/* Details modal */}
        {showDetailsModal && (
          <div
            className="modal-overlay"
            onClick={() => setShowDetailsModal(false)}
            style={{
              position: 'fixed',
              inset: 0,
              background: 'rgba(0, 0, 0, 0.5)',
              display: 'flex',
              alignItems: 'flex-end',
              zIndex: 1000,
            }}
          >
            <div
              onClick={(e) => e.stopPropagation()}
              style={{
                width: '100%',
                maxHeight: '80vh',
                background: 'var(--palette-bg, #ffffff)',
                borderRadius: '16px 16px 0 0',
                overflowY: 'auto',
              }}
            >
              <DetailsPanel />
            </div>
          </div>
        )}
      </>
    );
  }

  return (
    <div
      className="multi-panel-layout"
      style={{
        display: 'grid',
        gridTemplateColumns: `${filterPanelCollapsed ? '0' : '240px'} 1fr ${detailsPanelCollapsed ? '0' : '360px'}`,
        gap: '1px',
        width: '100%',
        height: '600px',
        maxHeight: '80vh',
        background: 'var(--palette-separator, #e5e7eb)',
      }}
    >
      <FilterPanel />

      {/* Center: Results */}
      <div
        ref={resultsRef}
        className="results-panel"
        role="listbox"
        style={{
          background: 'var(--palette-bg, #ffffff)',
          overflowY: 'auto',
          position: 'relative',
        }}
      >
        <div
          style={{
            position: 'sticky',
            top: 0,
            padding: '12px 16px',
            background: 'var(--palette-bg-secondary, #f9fafb)',
            borderBottom: '1px solid var(--palette-border, #e5e7eb)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            zIndex: 10,
          }}
        >
          <span style={{ fontSize: '14px', fontWeight: 500 }}>
            {items.length} results
          </span>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              onClick={() => setFilterPanelCollapsed(!filterPanelCollapsed)}
              style={{
                padding: '4px 8px',
                fontSize: '12px',
                cursor: 'pointer',
                background: 'transparent',
                border: '1px solid var(--palette-border, #e5e7eb)',
                borderRadius: '4px',
              }}
            >
              {filterPanelCollapsed ? 'Show' : 'Hide'} Filters
            </button>
            <button
              onClick={() => setDetailsPanelCollapsed(!detailsPanelCollapsed)}
              style={{
                padding: '4px 8px',
                fontSize: '12px',
                cursor: 'pointer',
                background: 'transparent',
                border: '1px solid var(--palette-border, #e5e7eb)',
                borderRadius: '4px',
              }}
            >
              {detailsPanelCollapsed ? 'Show' : 'Hide'} Details
            </button>
          </div>
        </div>
        {items.map((item) => {
          const isSelected = item.id === selectedItem?.id;
          return (
            <div
              key={item.id}
              data-item-id={item.id}
              role="option"
              aria-selected={isSelected}
              onClick={() => handleItemClick(item)}
              onDoubleClick={() => handleItemExecute(item)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '12px 16px',
                minHeight: '48px',
                cursor: item.disabled ? 'not-allowed' : 'pointer',
                background: isSelected ? 'var(--palette-selection-bg, #eff6ff)' : 'transparent',
                borderLeft: isSelected ? '3px solid var(--palette-accent, #3b82f6)' : '3px solid transparent',
                opacity: item.disabled ? 0.5 : 1,
              }}
            >
              {item.icon && (
                <div style={{ flexShrink: 0, width: '20px', height: '20px' }}>
                  {item.icon}
                </div>
              )}
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: '14px', fontWeight: 500 }}>{item.label}</div>
                {item.description && (
                  <div
                    style={{
                      fontSize: '12px',
                      color: 'var(--palette-text-muted, #6b7280)',
                      marginTop: '2px',
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

      <DetailsPanel />
    </div>
  );
}
