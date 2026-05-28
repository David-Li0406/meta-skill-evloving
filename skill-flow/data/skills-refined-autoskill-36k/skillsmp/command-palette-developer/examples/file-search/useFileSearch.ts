// Custom hook for file search logic

import { useState, useMemo, useEffect } from 'react';
import type { FileItem, FileType, FileSearchFilters } from './types';
import { fuzzyScore } from '../../utilities/fuzzy-search';

interface UseFileSearchOptions {
  files: FileItem[];
  initialRecentFiles?: FileItem[];
}

interface UseFileSearchReturn {
  filteredFiles: FileItem[];
  recentFiles: FileItem[];
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  filters: FileSearchFilters;
  setFilters: (filters: Partial<FileSearchFilters>) => void;
  totalCount: number;
  isSearching: boolean;
}

const RECENT_FILES_KEY = 'file-search-recent';
const MAX_RECENT_FILES = 10;

// Get recent files from localStorage
function loadRecentFiles(): FileItem[] {
  try {
    const stored = localStorage.getItem(RECENT_FILES_KEY);
    if (!stored) return [];

    const parsed = JSON.parse(stored);
    // Convert date strings back to Date objects
    return parsed.map((file: any) => ({
      ...file,
      modified: new Date(file.modified),
    }));
  } catch {
    return [];
  }
}

// Save recent files to localStorage
function saveRecentFiles(files: FileItem[]): void {
  try {
    localStorage.setItem(RECENT_FILES_KEY, JSON.stringify(files.slice(0, MAX_RECENT_FILES)));
  } catch {
    // Ignore storage errors
  }
}

// Add file to recent files list
function addToRecentFiles(file: FileItem, currentRecent: FileItem[]): FileItem[] {
  // Remove if already exists
  const filtered = currentRecent.filter(f => f.id !== file.id);
  // Add to front
  return [file, ...filtered].slice(0, MAX_RECENT_FILES);
}

// Fuzzy search implementation with scoring
function fuzzySearchFiles(query: string, files: FileItem[]): FileItem[] {
  if (!query.trim()) return files;

  const queryLower = query.toLowerCase();

  // Score each file
  const scored = files.map(file => {
    const nameScore = fuzzyScore(queryLower, file.name.toLowerCase());
    const pathScore = fuzzyScore(queryLower, file.path.toLowerCase()) * 0.8; // Path matches slightly lower weight
    const totalScore = Math.max(nameScore, pathScore);

    return { file, score: totalScore };
  });

  // Filter out non-matches and sort by score
  return scored
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .map(item => item.file);
}

// Filter files by type
function filterByType(files: FileItem[], types: FileType[]): FileItem[] {
  if (types.length === 0) return files;
  return files.filter(file => types.includes(file.type));
}

// Sort files
function sortFiles(files: FileItem[], sortBy: 'name' | 'modified' | 'size', sortOrder: 'asc' | 'desc'): FileItem[] {
  const sorted = [...files].sort((a, b) => {
    let comparison = 0;

    switch (sortBy) {
      case 'name':
        comparison = a.name.localeCompare(b.name);
        break;
      case 'modified':
        comparison = a.modified.getTime() - b.modified.getTime();
        break;
      case 'size':
        comparison = a.size - b.size;
        break;
    }

    return sortOrder === 'asc' ? comparison : -comparison;
  });

  return sorted;
}

export function useFileSearch({ files, initialRecentFiles = [] }: UseFileSearchOptions): UseFileSearchReturn {
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFiltersState] = useState<FileSearchFilters>({
    types: [],
    sortBy: 'name',
    sortOrder: 'asc',
  });
  const [recentFiles, setRecentFiles] = useState<FileItem[]>(() => {
    const loaded = loadRecentFiles();
    return loaded.length > 0 ? loaded : initialRecentFiles;
  });

  // Update localStorage when recent files change
  useEffect(() => {
    saveRecentFiles(recentFiles);
  }, [recentFiles]);

  // Update filters (partial update)
  const setFilters = (partial: Partial<FileSearchFilters>) => {
    setFiltersState(prev => ({ ...prev, ...partial }));
  };

  // Track if search is in progress
  const isSearching = searchQuery.trim().length > 0;

  // Filter and sort files
  const filteredFiles = useMemo(() => {
    // Start with fuzzy search
    let result = fuzzySearchFiles(searchQuery, files);

    // Apply type filters
    result = filterByType(result, filters.types);

    // Apply sorting
    result = sortFiles(result, filters.sortBy, filters.sortOrder);

    return result;
  }, [files, searchQuery, filters]);

  // Public method to add to recent files (called when user selects a file)
  const markAsRecent = (file: FileItem) => {
    setRecentFiles(prev => addToRecentFiles(file, prev));
  };

  return {
    filteredFiles,
    recentFiles,
    searchQuery,
    setSearchQuery,
    filters,
    setFilters,
    totalCount: files.length,
    isSearching,
  };
}

// Export helper for external use
export function useFileSearchWithRecent(options: UseFileSearchOptions) {
  const result = useFileSearch(options);

  return {
    ...result,
    markAsRecent: (file: FileItem) => {
      const currentRecent = result.recentFiles;
      const updated = addToRecentFiles(file, currentRecent);
      saveRecentFiles(updated);
    },
  };
}
