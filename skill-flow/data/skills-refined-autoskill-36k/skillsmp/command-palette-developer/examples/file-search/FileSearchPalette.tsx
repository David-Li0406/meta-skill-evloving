// Main file search palette with virtual scrolling and two-column layout

import React, { useRef, useState, useEffect, useCallback } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';
import { useFileSearch } from './useFileSearch';
import { FileResult } from './FileResult';
import { FilePreview } from './FilePreview';
import type { FileItem, FileType } from './types';

interface FileSearchPaletteProps {
  files: FileItem[];
  isOpen?: boolean;
  onClose?: () => void;
  onSelect?: (file: FileItem) => void;
}

const FILE_TYPE_OPTIONS: { label: string; value: FileType }[] = [
  { label: 'TypeScript', value: 'ts' },
  { label: 'TSX', value: 'tsx' },
  { label: 'JavaScript', value: 'js' },
  { label: 'JSX', value: 'jsx' },
  { label: 'JSON', value: 'json' },
  { label: 'Markdown', value: 'md' },
  { label: 'CSS', value: 'css' },
  { label: 'Python', value: 'py' },
  { label: 'Go', value: 'go' },
  { label: 'Rust', value: 'rs' },
];

export function FileSearchPalette({ files, isOpen = true, onClose, onSelect }: FileSearchPaletteProps) {
  const {
    filteredFiles,
    recentFiles,
    searchQuery,
    setSearchQuery,
    filters,
    setFilters,
    isSearching,
  } = useFileSearch({ files });

  const [selectedFile, setSelectedFile] = useState<FileItem | null>(null);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const parentRef = useRef<HTMLDivElement>(null);

  // Determine which files to show
  const displayFiles = isSearching ? filteredFiles : recentFiles;

  // Virtual scrolling setup
  const virtualizer = useVirtualizer({
    count: displayFiles.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 64, // Estimated item height in pixels
    overscan: 10, // Render 10 extra items above/below viewport
  });

  // Focus input on mount
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // Update selected index when filtered files change
  useEffect(() => {
    if (displayFiles.length > 0) {
      const newIndex = Math.min(selectedIndex, displayFiles.length - 1);
      setSelectedIndex(newIndex);
      setSelectedFile(displayFiles[newIndex]);
    } else {
      setSelectedIndex(0);
      setSelectedFile(null);
    }
  }, [displayFiles]);

  // Keyboard navigation
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      switch (e.key) {
        case 'ArrowDown':
          e.preventDefault();
          setSelectedIndex(prev => {
            const next = Math.min(prev + 1, displayFiles.length - 1);
            setSelectedFile(displayFiles[next]);
            return next;
          });
          break;
        case 'ArrowUp':
          e.preventDefault();
          setSelectedIndex(prev => {
            const next = Math.max(prev - 1, 0);
            setSelectedFile(displayFiles[next]);
            return next;
          });
          break;
        case 'Enter':
          e.preventDefault();
          if (selectedFile && onSelect) {
            onSelect(selectedFile);
          }
          break;
        case 'Escape':
          e.preventDefault();
          if (onClose) {
            onClose();
          }
          break;
      }
    },
    [displayFiles, selectedFile, onSelect, onClose]
  );

  // Toggle file type filter
  const toggleTypeFilter = (type: FileType) => {
    const current = filters.types;
    const updated = current.includes(type)
      ? current.filter(t => t !== type)
      : [...current, type];
    setFilters({ types: updated });
  };

  // Handle file selection
  const handleFileClick = (file: FileItem, index: number) => {
    setSelectedIndex(index);
    setSelectedFile(file);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-start justify-center pt-20 z-50">
      <div className="bg-white dark:bg-gray-950 rounded-lg shadow-2xl w-full max-w-6xl max-h-[80vh] flex flex-col overflow-hidden">
        {/* Header */}
        <div className="border-b border-gray-200 dark:border-gray-800 p-4">
          {/* Search input */}
          <input
            ref={inputRef}
            type="text"
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Search files... (Cmd+P)"
            className="w-full px-4 py-3 text-lg bg-transparent border-none outline-none text-gray-900 dark:text-gray-100 placeholder-gray-400"
          />

          {/* Filter bar */}
          <div className="flex items-center gap-2 mt-3 overflow-x-auto pb-2">
            <span className="text-xs text-gray-500 dark:text-gray-400 flex-shrink-0">
              Filter:
            </span>
            {FILE_TYPE_OPTIONS.map(({ label, value }) => (
              <button
                key={value}
                onClick={() => toggleTypeFilter(value)}
                className={`
                  px-3 py-1 text-xs rounded-full flex-shrink-0 transition-colors
                  ${
                    filters.types.includes(value)
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
                  }
                `}
              >
                {label}
              </button>
            ))}

            {/* Sort controls */}
            <div className="flex-1" />
            <select
              value={filters.sortBy}
              onChange={e => setFilters({ sortBy: e.target.value as any })}
              className="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-800 rounded border-none outline-none"
            >
              <option value="name">Name</option>
              <option value="modified">Modified</option>
              <option value="size">Size</option>
            </select>
            <button
              onClick={() => setFilters({ sortOrder: filters.sortOrder === 'asc' ? 'desc' : 'asc' })}
              className="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-800 rounded hover:bg-gray-200 dark:hover:bg-gray-700"
              title={`Sort ${filters.sortOrder === 'asc' ? 'descending' : 'ascending'}`}
            >
              {filters.sortOrder === 'asc' ? '↑' : '↓'}
            </button>
          </div>

          {/* Results count */}
          <div className="text-xs text-gray-500 dark:text-gray-400 mt-2">
            {isSearching ? (
              <>Showing {displayFiles.length} results</>
            ) : (
              <>Recent files ({displayFiles.length})</>
            )}
          </div>
        </div>

        {/* Two-column layout */}
        <div className="flex flex-1 overflow-hidden">
          {/* Left: File list with virtual scrolling */}
          <div className="w-[40%] border-r border-gray-200 dark:border-gray-800 overflow-hidden flex flex-col">
            {displayFiles.length === 0 ? (
              <div className="flex-1 flex items-center justify-center text-gray-400">
                <div className="text-center">
                  <div className="text-4xl mb-2">🔍</div>
                  <p className="text-sm">No files found</p>
                </div>
              </div>
            ) : (
              <div ref={parentRef} className="flex-1 overflow-y-auto">
                <div
                  style={{
                    height: `${virtualizer.getTotalSize()}px`,
                    width: '100%',
                    position: 'relative',
                  }}
                >
                  {virtualizer.getVirtualItems().map(virtualItem => {
                    const file = displayFiles[virtualItem.index];
                    return (
                      <div
                        key={virtualItem.key}
                        style={{
                          position: 'absolute',
                          top: 0,
                          left: 0,
                          width: '100%',
                          height: `${virtualItem.size}px`,
                          transform: `translateY(${virtualItem.start}px)`,
                        }}
                      >
                        <FileResult
                          file={file}
                          isSelected={virtualItem.index === selectedIndex}
                          onClick={() => handleFileClick(file, virtualItem.index)}
                          highlightQuery={searchQuery}
                        />
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>

          {/* Right: Preview panel */}
          <div className="w-[60%] overflow-hidden bg-gray-50 dark:bg-gray-900">
            <FilePreview file={selectedFile} />
          </div>
        </div>

        {/* Footer */}
        <div className="border-t border-gray-200 dark:border-gray-800 p-3 bg-gray-50 dark:bg-gray-900">
          <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
            <div className="flex items-center gap-4">
              <span>
                <kbd className="px-2 py-1 bg-white dark:bg-gray-800 rounded border border-gray-300 dark:border-gray-700">
                  ↑↓
                </kbd>{' '}
                Navigate
              </span>
              <span>
                <kbd className="px-2 py-1 bg-white dark:bg-gray-800 rounded border border-gray-300 dark:border-gray-700">
                  Enter
                </kbd>{' '}
                Select
              </span>
              <span>
                <kbd className="px-2 py-1 bg-white dark:bg-gray-800 rounded border border-gray-300 dark:border-gray-700">
                  Esc
                </kbd>{' '}
                Close
              </span>
            </div>
            <div>
              {selectedIndex + 1} / {displayFiles.length}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Hook to control palette with keyboard shortcut
export function useFileSearchPalette() {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Cmd+P or Ctrl+P
      if ((e.metaKey || e.ctrlKey) && e.key === 'p') {
        e.preventDefault();
        setIsOpen(prev => !prev);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return {
    isOpen,
    open: () => setIsOpen(true),
    close: () => setIsOpen(false),
    toggle: () => setIsOpen(prev => !prev),
  };
}
