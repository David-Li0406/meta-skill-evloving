// App-wide action palette with keyboard shortcuts and command grouping

import React, { useState, useEffect, useRef, useMemo } from 'react';
import { ActionResult } from './ActionResult';
import { searchCommands, getCommandsByCategory } from './actions-registry';
import type { AppAction } from './actions-registry';

interface ActionPaletteProps {
  isOpen: boolean;
  onClose: () => void;
}

export function ActionPalette({ isOpen, onClose }: ActionPaletteProps): React.ReactElement | null {
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const filteredActions = useMemo(() => {
    return searchCommands(query);
  }, [query]);

  const groupedActions = useMemo(() => {
    if (query) {
      // When searching, don't group - show flat list
      return { 'Search Results': filteredActions };
    }

    // When not searching, group by category
    const commandsByCategory = getCommandsByCategory();

    // Filter out empty categories
    return Object.entries(commandsByCategory).reduce((acc, [category, actions]) => {
      if (actions.length > 0) {
        acc[category] = actions;
      }
      return acc;
    }, {} as Record<string, AppAction[]>);
  }, [query, filteredActions]);

  const flatActions = useMemo(() => {
    return Object.values(groupedActions).flat();
  }, [groupedActions]);

  // Reset selection when results change
  useEffect(() => {
    setSelectedIndex(0);
  }, [filteredActions]);

  // Focus input when opened
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 10);
    } else {
      setQuery('');
      setSelectedIndex(0);
    }
  }, [isOpen]);

  // Keyboard navigation
  useEffect(() => {
    if (!isOpen) return;

    function handleKeyDown(e: KeyboardEvent): void {
      switch (e.key) {
        case 'ArrowDown':
          e.preventDefault();
          setSelectedIndex((prev) => Math.min(prev + 1, flatActions.length - 1));
          break;

        case 'ArrowUp':
          e.preventDefault();
          setSelectedIndex((prev) => Math.max(prev - 1, 0));
          break;

        case 'Enter':
          e.preventDefault();
          executeSelectedAction();
          break;

        case 'Escape':
          e.preventDefault();
          onClose();
          break;

        case 'Home':
          e.preventDefault();
          setSelectedIndex(0);
          break;

        case 'End':
          e.preventDefault();
          setSelectedIndex(flatActions.length - 1);
          break;
      }

      // Handle Cmd+1-9 for quick actions
      if ((e.metaKey || e.ctrlKey) && e.key >= '1' && e.key <= '9') {
        e.preventDefault();
        const index = parseInt(e.key, 10) - 1;
        if (index < flatActions.length) {
          executeAction(flatActions[index]);
        }
      }

      // Handle Cmd+Backspace to clear search
      if ((e.metaKey || e.ctrlKey) && e.key === 'Backspace') {
        e.preventDefault();
        setQuery('');
      }
    }

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, flatActions, selectedIndex, onClose]);

  function executeSelectedAction(): void {
    const action = flatActions[selectedIndex];
    if (action && !action.disabled) {
      executeAction(action);
    }
  }

  function executeAction(action: AppAction): void {
    action.action();
    onClose();
  }

  function handleActionClick(action: AppAction): void {
    if (!action.disabled) {
      executeAction(action);
    }
  }

  // Scroll selected item into view
  useEffect(() => {
    if (!isOpen) return;

    const selectedElement = containerRef.current?.querySelector(
      `[data-action-index="${selectedIndex}"]`
    );

    if (selectedElement) {
      selectedElement.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  }, [selectedIndex, isOpen]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center pt-[20vh] bg-black/50"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="action-palette-title"
    >
      <div
        className="w-full max-w-2xl bg-white dark:bg-gray-900 rounded-lg shadow-2xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
        ref={containerRef}
      >
        <h2 id="action-palette-title" className="sr-only">
          Action Palette
        </h2>

        {/* Search Input */}
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <input
            ref={inputRef}
            type="text"
            placeholder="Search actions..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="
              w-full px-4 py-3 text-lg
              bg-transparent
              border-0 outline-none
              text-gray-900 dark:text-gray-100
              placeholder-gray-400 dark:placeholder-gray-500
            "
            role="combobox"
            aria-expanded={isOpen}
            aria-controls="action-results"
            aria-activedescendant={`action-${selectedIndex}`}
            aria-autocomplete="list"
          />
        </div>

        {/* Results */}
        <div
          id="action-results"
          className="max-h-[60vh] overflow-y-auto"
          role="listbox"
        >
          {flatActions.length === 0 ? (
            <div className="px-4 py-8 text-center text-gray-500 dark:text-gray-400">
              No actions found
            </div>
          ) : (
            <>
              {Object.entries(groupedActions).map(([category, actions]) => (
                <div key={category}>
                  {/* Category Header */}
                  {!query && (
                    <div className="px-4 py-2 text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-800/50">
                      {category}
                    </div>
                  )}

                  {/* Actions in Category */}
                  {actions.map((action) => {
                    const actionIndex = flatActions.indexOf(action);
                    const isSelected = actionIndex === selectedIndex;

                    return (
                      <div
                        key={action.id}
                        data-action-index={actionIndex}
                        role="option"
                        id={`action-${actionIndex}`}
                        aria-selected={isSelected}
                      >
                        <ActionResult
                          action={action}
                          isSelected={isSelected}
                          onClick={() => handleActionClick(action)}
                        />
                      </div>
                    );
                  })}
                </div>
              ))}
            </>
          )}
        </div>

        {/* Footer with keyboard hints */}
        <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
          <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
            <div className="flex items-center gap-4">
              <span className="flex items-center gap-1">
                <kbd className="px-1.5 py-0.5 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded text-xs">↑</kbd>
                <kbd className="px-1.5 py-0.5 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded text-xs">↓</kbd>
                <span className="ml-1">navigate</span>
              </span>
              <span className="flex items-center gap-1">
                <kbd className="px-1.5 py-0.5 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded text-xs">↵</kbd>
                <span className="ml-1">select</span>
              </span>
              <span className="flex items-center gap-1">
                <kbd className="px-1.5 py-0.5 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded text-xs">esc</kbd>
                <span className="ml-1">close</span>
              </span>
            </div>
            <div className="flex items-center gap-1">
              <kbd className="px-1.5 py-0.5 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded text-xs">⌘</kbd>
              <kbd className="px-1.5 py-0.5 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded text-xs">1-9</kbd>
              <span className="ml-1">quick select</span>
            </div>
          </div>
        </div>
      </div>

      {/* Screen reader announcement */}
      <div role="status" aria-live="polite" aria-atomic="true" className="sr-only">
        {flatActions.length} {flatActions.length === 1 ? 'action' : 'actions'} available
        {query && ` for "${query}"`}
      </div>
    </div>
  );
}

// Utility class for screen reader only content
const srOnlyStyles = `
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
  }
`;

// Inject styles
if (typeof document !== 'undefined') {
  const styleEl = document.createElement('style');
  styleEl.textContent = srOnlyStyles;
  document.head.appendChild(styleEl);
}
