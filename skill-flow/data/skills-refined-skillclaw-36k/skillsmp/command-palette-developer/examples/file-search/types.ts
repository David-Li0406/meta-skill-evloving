// Type definitions for file search example

export type FileType =
  | 'js' | 'ts' | 'tsx' | 'jsx'
  | 'json' | 'md' | 'css' | 'scss'
  | 'html' | 'svg' | 'png' | 'jpg'
  | 'pdf' | 'txt' | 'yaml' | 'yml'
  | 'toml' | 'xml' | 'sh' | 'py'
  | 'go' | 'rs' | 'c' | 'cpp'
  | 'java' | 'rb' | 'php' | 'unknown';

export interface FileItem {
  id: string;
  name: string;
  path: string;
  type: FileType;
  size: number; // bytes
  modified: Date;
  content?: string; // Optional preview content
}

export interface FileSearchFilters {
  types: FileType[];
  sortBy: 'name' | 'modified' | 'size';
  sortOrder: 'asc' | 'desc';
}

export interface FileSearchState {
  searchQuery: string;
  filters: FileSearchFilters;
  selectedFile: FileItem | null;
  recentFiles: FileItem[];
}

export type ViewState = 'loading' | 'error' | 'empty' | 'ready';
