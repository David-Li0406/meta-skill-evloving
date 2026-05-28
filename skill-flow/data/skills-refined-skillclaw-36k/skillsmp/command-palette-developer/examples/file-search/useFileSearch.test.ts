// Unit tests for useFileSearch hook

import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useFileSearch } from './useFileSearch';
import type { FileItem } from './types';

// Mock localStorage
const localStorageMock = (() => {
  let store: Record<string, string> = {};

  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Sample test data
const mockFiles: FileItem[] = [
  {
    id: '1',
    name: 'App.tsx',
    path: 'src/App.tsx',
    type: 'tsx',
    size: 5000,
    modified: new Date('2024-01-15'),
  },
  {
    id: '2',
    name: 'index.ts',
    path: 'src/index.ts',
    type: 'ts',
    size: 2000,
    modified: new Date('2024-01-10'),
  },
  {
    id: '3',
    name: 'utils.ts',
    path: 'src/utils/utils.ts',
    type: 'ts',
    size: 3000,
    modified: new Date('2024-01-20'),
  },
  {
    id: '4',
    name: 'Button.tsx',
    path: 'src/components/Button.tsx',
    type: 'tsx',
    size: 4000,
    modified: new Date('2024-01-18'),
  },
  {
    id: '5',
    name: 'styles.css',
    path: 'src/styles.css',
    type: 'css',
    size: 1000,
    modified: new Date('2024-01-12'),
  },
];

describe('useFileSearch', () => {
  beforeEach(() => {
    localStorageMock.clear();
  });

  afterEach(() => {
    localStorageMock.clear();
  });

  describe('Basic functionality', () => {
    it('should return all files when no search query', () => {
      const { result } = renderHook(() =>
        useFileSearch({ files: mockFiles })
      );

      expect(result.current.filteredFiles).toHaveLength(5);
      expect(result.current.searchQuery).toBe('');
    });

    it('should filter files by search query', () => {
      const { result } = renderHook(() =>
        useFileSearch({ files: mockFiles })
      );

      act(() => {
        result.current.setSearchQuery('App');
      });

      expect(result.current.filteredFiles).toHaveLength(1);
      expect(result.current.filteredFiles[0].name).toBe('App.tsx');
    });

    it('should perform fuzzy search', () => {
      const { result } = renderHook(() =>
        useFileSearch({ files: mockFiles })
      );

      act(() => {
        result.current.setSearchQuery('btn'); // Should match Button
      });

      expect(result.current.filteredFiles.length).toBeGreaterThan(0);
      expect(result.current.filteredFiles[0].name).toBe('Button.tsx');
    });

    it('should search in file path', () => {
      const { result } = renderHook(() =>
        useFileSearch({ files: mockFiles })
      );

      act(() => {
        result.current.setSearchQuery('components');
      });

      expect(result.current.filteredFiles).toHaveLength(1);
      expect(result.current.filteredFiles[0].path).toContain('components');
    });
  });

  describe('Filtering by type', () => {
    it('should filter by file type', () => {
      const { result } = renderHook(() =>
        useFileSearch({ files: mockFiles })
      );

      act(() => {
        result.current.setFilters({ types: ['tsx'] });
      });

      expect(result.current.filteredFiles).toHaveLength(2);
      expect(result.current.filteredFiles.every(f => f.type === 'tsx')).toBe(true);
    });

    it('should filter by multiple file types', () => {
      const { result } = renderHook(() =>
        useFileSearch({ files: mockFiles })
      );

      act(() => {
        result.current.setFilters({ types: ['tsx', 'css'] });
      });

      expect(result.current.filteredFiles).toHaveLength(3);
    });

    it('should combine search query and type filter', () => {
      const { result } = renderHook(() =>
        useFileSearch({ files: mockFiles })
      );

      act(() => {
        result.current.setSearchQuery('s');
        result.current.setFilters({ types: ['ts'] });
      });

      // Should match utils.ts and index.ts, but filter to only .ts files
      const tsFiles = result.current.filteredFiles;
      expect(tsFiles.every(f => f.type === 'ts')).toBe(true);
    });
  });

  describe('Sorting', () => {
    it('should sort by name ascending', () => {
      const { result } = renderHook(() =>
        useFileSearch({ files: mockFiles })
      );

      act(() => {
        result.current.setFilters({ sortBy: 'name', sortOrder: 'asc' });
      });

      const names = result.current.filteredFiles.map(f => f.name);
      expect(names).toEqual([...names].sort());
    });

    it('should sort by name descending', () => {
      const { result } = renderHook(() =>
        useFileSearch({ files: mockFiles })
      );

      act(() => {
        result.current.setFilters({ sortBy: 'name', sortOrder: 'desc' });
      });

      const names = result.current.filteredFiles.map(f => f.name);
      expect(names).toEqual([...names].sort().reverse());
    });

    it('should sort by size ascending', () => {
      const { result } = renderHook(() =>
        useFileSearch({ files: mockFiles })
      );

      act(() => {
        result.current.setFilters({ sortBy: 'size', sortOrder: 'asc' });
      });

      const sizes = result.current.filteredFiles.map(f => f.size);
      for (let i = 1; i < sizes.length; i++) {
        expect(sizes[i]).toBeGreaterThanOrEqual(sizes[i - 1]);
      }
    });

    it('should sort by modified date descending', () => {
      const { result } = renderHook(() =>
        useFileSearch({ files: mockFiles })
      );

      act(() => {
        result.current.setFilters({ sortBy: 'modified', sortOrder: 'desc' });
      });

      const dates = result.current.filteredFiles.map(f => f.modified.getTime());
      for (let i = 1; i < dates.length; i++) {
        expect(dates[i]).toBeLessThanOrEqual(dates[i - 1]);
      }
    });
  });

  describe('Recent files', () => {
    it('should initialize with provided recent files', () => {
      const recentFiles = [mockFiles[0], mockFiles[1]];
      const { result } = renderHook(() =>
        useFileSearch({ files: mockFiles, initialRecentFiles: recentFiles })
      );

      expect(result.current.recentFiles).toHaveLength(2);
    });

    it('should persist recent files to localStorage', () => {
      const recentFiles = [mockFiles[0]];
      renderHook(() =>
        useFileSearch({ files: mockFiles, initialRecentFiles: recentFiles })
      );

      const stored = localStorageMock.getItem('file-search-recent');
      expect(stored).toBeTruthy();
      expect(JSON.parse(stored!)).toHaveLength(1);
    });

    it('should load recent files from localStorage', () => {
      // Pre-populate localStorage
      localStorageMock.setItem(
        'file-search-recent',
        JSON.stringify([mockFiles[2]])
      );

      const { result } = renderHook(() =>
        useFileSearch({ files: mockFiles })
      );

      expect(result.current.recentFiles).toHaveLength(1);
      expect(result.current.recentFiles[0].id).toBe('3');
    });
  });

  describe('Search state', () => {
    it('should track isSearching state', () => {
      const { result } = renderHook(() =>
        useFileSearch({ files: mockFiles })
      );

      expect(result.current.isSearching).toBe(false);

      act(() => {
        result.current.setSearchQuery('test');
      });

      expect(result.current.isSearching).toBe(true);
    });

    it('should return total file count', () => {
      const { result } = renderHook(() =>
        useFileSearch({ files: mockFiles })
      );

      expect(result.current.totalCount).toBe(5);
    });
  });

  describe('Performance', () => {
    it('should handle large file lists efficiently', () => {
      const largeFileList: FileItem[] = Array.from({ length: 10000 }, (_, i) => ({
        id: `file-${i}`,
        name: `file-${i}.ts`,
        path: `src/file-${i}.ts`,
        type: 'ts',
        size: 1000 * i,
        modified: new Date(),
      }));

      const startTime = performance.now();

      const { result } = renderHook(() =>
        useFileSearch({ files: largeFileList })
      );

      act(() => {
        result.current.setSearchQuery('file-5');
      });

      const endTime = performance.now();
      const duration = endTime - startTime;

      // Should complete in reasonable time (< 100ms)
      expect(duration).toBeLessThan(100);
      expect(result.current.filteredFiles.length).toBeGreaterThan(0);
    });
  });
});
