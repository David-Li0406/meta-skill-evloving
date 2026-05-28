// File result component with icon and metadata display

import React from 'react';
import type { FileItem } from './types';

interface FileResultProps {
  file: FileItem;
  isSelected?: boolean;
  onClick?: () => void;
  highlightQuery?: string;
}

// File type to icon mapping
function getFileIcon(type: string): string {
  const iconMap: Record<string, string> = {
    // JavaScript/TypeScript
    js: '📄',
    ts: '📘',
    tsx: '⚛️',
    jsx: '⚛️',

    // Web
    html: '🌐',
    css: '🎨',
    scss: '🎨',

    // Data
    json: '📋',
    yaml: '📋',
    yml: '📋',
    xml: '📋',
    toml: '📋',

    // Documentation
    md: '📝',
    txt: '📝',

    // Images
    png: '🖼️',
    jpg: '🖼️',
    jpeg: '🖼️',
    svg: '🎨',
    gif: '🖼️',

    // Documents
    pdf: '📕',

    // Scripts
    sh: '⚙️',
    bash: '⚙️',

    // Programming languages
    py: '🐍',
    go: '🐹',
    rs: '🦀',
    c: '©️',
    cpp: '©️',
    java: '☕',
    rb: '💎',
    php: '🐘',
  };

  return iconMap[type] || '📄';
}

// Format file size
function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  return `${(bytes / (1024 * 1024 * 1024)).toFixed(1)} GB`;
}

// Format modified time
function formatModifiedTime(date: Date): string {
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffSeconds = Math.floor(diffMs / 1000);
  const diffMinutes = Math.floor(diffSeconds / 60);
  const diffHours = Math.floor(diffMinutes / 60);
  const diffDays = Math.floor(diffHours / 24);
  const diffMonths = Math.floor(diffDays / 30);

  if (diffSeconds < 60) return 'just now';
  if (diffMinutes < 60) return `${diffMinutes}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 30) return `${diffDays}d ago`;
  if (diffMonths < 12) return `${diffMonths}mo ago`;
  return date.toLocaleDateString();
}

// Format absolute time for tooltip
function formatAbsoluteTime(date: Date): string {
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

// Truncate path intelligently
function truncatePath(path: string, maxLength: number = 60): string {
  if (path.length <= maxLength) return path;

  const parts = path.split('/');
  if (parts.length <= 2) return path;

  // Keep first and last parts, show ... in middle
  const first = parts[0];
  const last = parts[parts.length - 1];
  const middle = parts.slice(1, -1);

  let result = `${first}/`;
  let remainingLength = maxLength - first.length - last.length - 5; // 5 for "/.../

  if (remainingLength > 0) {
    const middleParts = [];
    for (const part of middle) {
      if (part.length + 1 <= remainingLength) {
        middleParts.push(part);
        remainingLength -= part.length + 1;
      } else {
        break;
      }
    }
    if (middleParts.length > 0) {
      result += middleParts.join('/') + '/';
    }
  }

  result += `.../${last}`;
  return result;
}

// Highlight matching characters
function highlightText(text: string, query: string): React.ReactNode {
  if (!query) return text;

  const queryLower = query.toLowerCase();
  const textLower = text.toLowerCase();
  const result: React.ReactNode[] = [];

  let lastIndex = 0;
  let queryIndex = 0;

  for (let i = 0; i < text.length && queryIndex < queryLower.length; i++) {
    if (textLower[i] === queryLower[queryIndex]) {
      // Add text before match
      if (i > lastIndex) {
        result.push(<span key={`text-${lastIndex}`}>{text.substring(lastIndex, i)}</span>);
      }

      // Add highlighted character
      result.push(
        <span key={`match-${i}`} className="bg-yellow-200 dark:bg-yellow-800">
          {text[i]}
        </span>
      );

      queryIndex++;
      lastIndex = i + 1;
    }
  }

  // Add remaining text
  if (lastIndex < text.length) {
    result.push(<span key={`text-${lastIndex}`}>{text.substring(lastIndex)}</span>);
  }

  return <>{result}</>;
}

export function FileResult({ file, isSelected = false, onClick, highlightQuery }: FileResultProps) {
  const icon = getFileIcon(file.type);
  const size = formatFileSize(file.size);
  const modifiedRelative = formatModifiedTime(file.modified);
  const modifiedAbsolute = formatAbsoluteTime(file.modified);
  const displayPath = truncatePath(file.path, 70);

  return (
    <div
      className={`
        flex items-center gap-3 px-4 py-2.5 cursor-pointer
        hover:bg-gray-100 dark:hover:bg-gray-800
        transition-colors duration-150
        ${isSelected ? 'bg-blue-50 dark:bg-blue-900/30 border-l-2 border-blue-500' : ''}
      `}
      onClick={onClick}
      role="option"
      aria-selected={isSelected}
    >
      {/* File icon */}
      <span className="text-2xl flex-shrink-0" aria-hidden="true">
        {icon}
      </span>

      {/* File info */}
      <div className="flex-1 min-w-0">
        {/* File name */}
        <div className="font-medium text-sm text-gray-900 dark:text-gray-100 truncate">
          {highlightQuery ? highlightText(file.name, highlightQuery) : file.name}
        </div>

        {/* File path */}
        <div className="text-xs text-gray-500 dark:text-gray-400 truncate">
          {highlightQuery ? highlightText(displayPath, highlightQuery) : displayPath}
        </div>
      </div>

      {/* Metadata */}
      <div className="flex items-center gap-3 text-xs text-gray-500 dark:text-gray-400 flex-shrink-0">
        {/* File size */}
        <span className="hidden sm:inline">{size}</span>

        {/* Modified time with tooltip */}
        <span
          className="hidden md:inline"
          title={modifiedAbsolute}
        >
          {modifiedRelative}
        </span>
      </div>
    </div>
  );
}

// Compact variant for mobile
export function FileResultCompact({ file, isSelected = false, onClick }: FileResultProps) {
  const icon = getFileIcon(file.type);

  return (
    <div
      className={`
        flex items-center gap-2 px-3 py-2 cursor-pointer
        hover:bg-gray-100 dark:hover:bg-gray-800
        ${isSelected ? 'bg-blue-50 dark:bg-blue-900/30' : ''}
      `}
      onClick={onClick}
    >
      <span className="text-xl" aria-hidden="true">{icon}</span>
      <div className="flex-1 min-w-0">
        <div className="text-sm font-medium truncate">{file.name}</div>
        <div className="text-xs text-gray-500 truncate">{formatFileSize(file.size)}</div>
      </div>
    </div>
  );
}
