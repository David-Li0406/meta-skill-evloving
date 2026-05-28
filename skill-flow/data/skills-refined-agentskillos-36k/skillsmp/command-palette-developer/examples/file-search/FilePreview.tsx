// File preview panel component

import React, { useState } from 'react';
import type { FileItem } from './types';

interface FilePreviewProps {
  file: FileItem | null;
}

// Determine if file type is previewable as code
function isCodeFile(type: string): boolean {
  const codeTypes = [
    'js', 'ts', 'tsx', 'jsx',
    'json', 'css', 'scss', 'html',
    'md', 'txt', 'yaml', 'yml',
    'toml', 'xml', 'sh', 'py',
    'go', 'rs', 'c', 'cpp',
    'java', 'rb', 'php',
  ];
  return codeTypes.includes(type);
}

// Determine if file type is an image
function isImageFile(type: string): boolean {
  return ['png', 'jpg', 'jpeg', 'svg', 'gif'].includes(type);
}

// Format file size
function formatFileSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  return `${(bytes / (1024 * 1024 * 1024)).toFixed(1)} GB`;
}

// Format date
function formatDate(date: Date): string {
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

// Copy to clipboard utility
async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    return false;
  }
}

// Code preview with syntax highlighting (simplified - in production use Prism or Highlight.js)
function CodePreview({ content, language }: { content: string; language: string }) {
  const lines = content.split('\n').slice(0, 50); // Show first 50 lines
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    const success = await copyToClipboard(content);
    if (success) {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="relative">
      <div className="absolute top-2 right-2 z-10">
        <button
          onClick={handleCopy}
          className="px-3 py-1 text-xs bg-gray-800 text-white rounded hover:bg-gray-700 transition-colors"
          title="Copy code"
        >
          {copied ? '✓ Copied' : 'Copy'}
        </button>
      </div>
      <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm font-mono">
        <code className={`language-${language}`}>
          {lines.map((line, i) => (
            <div key={i} className="table-row">
              <span className="table-cell pr-4 text-gray-500 text-right select-none">
                {i + 1}
              </span>
              <span className="table-cell">{line || ' '}</span>
            </div>
          ))}
        </code>
      </pre>
      {content.split('\n').length > 50 && (
        <div className="text-xs text-gray-500 mt-2">
          Showing first 50 lines of {content.split('\n').length} total
        </div>
      )}
    </div>
  );
}

// Image preview
function ImagePreview({ file }: { file: FileItem }) {
  return (
    <div className="flex flex-col items-center justify-center p-8 bg-gray-50 dark:bg-gray-900 rounded-lg">
      <div className="text-6xl mb-4">🖼️</div>
      <p className="text-sm text-gray-600 dark:text-gray-400">
        Image preview: {file.name}
      </p>
      <p className="text-xs text-gray-500 mt-2">
        {formatFileSize(file.size)}
      </p>
      <p className="text-xs text-gray-400 mt-4">
        In a real implementation, image would be loaded from file system
      </p>
    </div>
  );
}

// PDF preview
function PDFPreview({ file }: { file: FileItem }) {
  return (
    <div className="flex flex-col items-center justify-center p-8 bg-gray-50 dark:bg-gray-900 rounded-lg">
      <div className="text-6xl mb-4">📕</div>
      <p className="text-sm text-gray-600 dark:text-gray-400">
        PDF document: {file.name}
      </p>
      <p className="text-xs text-gray-500 mt-2">
        {formatFileSize(file.size)}
      </p>
      <p className="text-xs text-gray-400 mt-4">
        In a real implementation, PDF thumbnail would be shown
      </p>
    </div>
  );
}

// Generic preview for unsupported types
function UnsupportedPreview({ file }: { file: FileItem }) {
  return (
    <div className="flex flex-col items-center justify-center p-8 bg-gray-50 dark:bg-gray-900 rounded-lg h-full">
      <div className="text-6xl mb-4">📄</div>
      <p className="text-sm text-gray-600 dark:text-gray-400">
        Preview not available
      </p>
      <p className="text-xs text-gray-500 mt-2">
        {file.type.toUpperCase()} files cannot be previewed
      </p>
    </div>
  );
}

// Empty state
function EmptyPreview() {
  return (
    <div className="flex flex-col items-center justify-center h-full text-gray-400">
      <div className="text-6xl mb-4">📂</div>
      <p className="text-sm">Select a file to preview</p>
    </div>
  );
}

export function FilePreview({ file }: FilePreviewProps) {
  const [pathCopied, setPathCopied] = useState(false);

  if (!file) {
    return <EmptyPreview />;
  }

  const handleCopyPath = async () => {
    const success = await copyToClipboard(file.path);
    if (success) {
      setPathCopied(true);
      setTimeout(() => setPathCopied(false), 2000);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* File metadata header */}
      <div className="border-b border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-950">
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <h3 className="font-semibold text-lg text-gray-900 dark:text-gray-100 truncate">
              {file.name}
            </h3>
            <div className="flex items-center gap-2 mt-1">
              <button
                onClick={handleCopyPath}
                className="text-xs text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 flex items-center gap-1 transition-colors"
                title="Copy path"
              >
                <span className="truncate max-w-md">{file.path}</span>
                <span>{pathCopied ? '✓' : '📋'}</span>
              </button>
            </div>
          </div>
        </div>

        {/* Metadata grid */}
        <div className="grid grid-cols-2 gap-4 mt-4 text-sm">
          <div>
            <span className="text-gray-500 dark:text-gray-400">Type:</span>
            <span className="ml-2 font-medium text-gray-900 dark:text-gray-100">
              {file.type.toUpperCase()}
            </span>
          </div>
          <div>
            <span className="text-gray-500 dark:text-gray-400">Size:</span>
            <span className="ml-2 font-medium text-gray-900 dark:text-gray-100">
              {formatFileSize(file.size)}
            </span>
          </div>
          <div className="col-span-2">
            <span className="text-gray-500 dark:text-gray-400">Modified:</span>
            <span className="ml-2 font-medium text-gray-900 dark:text-gray-100">
              {formatDate(file.modified)}
            </span>
          </div>
        </div>
      </div>

      {/* File content preview */}
      <div className="flex-1 overflow-y-auto p-4">
        {isCodeFile(file.type) && file.content ? (
          <CodePreview content={file.content} language={file.type} />
        ) : isImageFile(file.type) ? (
          <ImagePreview file={file} />
        ) : file.type === 'pdf' ? (
          <PDFPreview file={file} />
        ) : (
          <UnsupportedPreview file={file} />
        )}
      </div>
    </div>
  );
}
