import * as React from 'react';
import { cn } from '@/lib/utils';
import {
  FileText,
  FileCode,
  FileJson,
  FileImage,
  FileVideo,
  FileArchive,
  File,
} from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

export interface FileResultProps {
  file: {
    name: string;
    path: string;
    type: string;
    size: number;
    modified: Date;
    thumbnail?: string;
  };
  selected: boolean;
  onClick: () => void;
}

// Map file extensions to icons
const getFileIcon = (type: string) => {
  const ext = type.toLowerCase();

  if (['js', 'ts', 'jsx', 'tsx', 'py', 'rs', 'go', 'java'].includes(ext)) {
    return FileCode;
  }
  if (['json', 'yaml', 'yml', 'toml', 'xml'].includes(ext)) {
    return FileJson;
  }
  if (['png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'].includes(ext)) {
    return FileImage;
  }
  if (['mp4', 'mov', 'avi', 'mkv', 'webm'].includes(ext)) {
    return FileVideo;
  }
  if (['zip', 'tar', 'gz', 'rar', '7z'].includes(ext)) {
    return FileArchive;
  }
  if (['txt', 'md', 'doc', 'docx', 'pdf'].includes(ext)) {
    return FileText;
  }

  return File;
};

// Format file size (bytes to KB, MB, GB)
const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  if (bytes < 1024 * 1024 * 1024)
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  return `${(bytes / (1024 * 1024 * 1024)).toFixed(1)} GB`;
};

// Format relative time
const formatRelativeTime = (date: Date): string => {
  try {
    return formatDistanceToNow(date, { addSuffix: true });
  } catch {
    return 'Unknown';
  }
};

// Truncate path from the middle to fit space
const truncatePath = (path: string, maxLength: number = 50): string => {
  if (path.length <= maxLength) return path;

  const start = Math.ceil(maxLength / 2) - 2;
  const end = Math.floor(maxLength / 2) - 2;

  return `${path.slice(0, start)}...${path.slice(-end)}`;
};

export function FileResult({ file, selected, onClick }: FileResultProps) {
  const { name, path, type, size, modified, thumbnail } = file;
  const Icon = getFileIcon(type);

  return (
    <button
      type="button"
      role="option"
      aria-selected={selected}
      onClick={onClick}
      className={cn(
        'w-full flex items-center gap-3 px-3 py-2 text-left',
        'transition-colors duration-150 ease-out',
        'focus:outline-none h-14',
        selected
          ? 'bg-primary/10 text-primary'
          : 'hover:bg-muted/50 text-foreground'
      )}
    >
      {/* File icon or thumbnail */}
      <div className="flex-shrink-0">
        {thumbnail ? (
          <img
            src={thumbnail}
            alt={name}
            className="w-10 h-10 rounded object-cover"
            loading="lazy"
          />
        ) : (
          <div className="w-10 h-10 flex items-center justify-center rounded bg-muted">
            <Icon className="w-5 h-5 text-muted-foreground" />
          </div>
        )}
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        {/* File name - Primary text */}
        <div className="font-medium text-sm truncate">{name}</div>

        {/* File path - Secondary text */}
        <div className="text-xs text-muted-foreground truncate" title={path}>
          {truncatePath(path)}
        </div>

        {/* Metadata - Size and modified date */}
        <div className="flex gap-2 text-xs text-muted-foreground/75 mt-0.5">
          <span>{formatFileSize(size)}</span>
          <span>•</span>
          <span>{formatRelativeTime(modified)}</span>
        </div>
      </div>

      {/* File extension badge */}
      <div className="flex-shrink-0">
        <span
          className={cn(
            'inline-flex items-center justify-center',
            'px-2 py-0.5 rounded text-xs font-mono',
            'bg-muted/50 text-muted-foreground uppercase'
          )}
        >
          {type}
        </span>
      </div>
    </button>
  );
}

// Skeleton loading state
export function FileResultSkeleton() {
  return (
    <div className="flex items-center gap-3 px-3 py-2 h-14 animate-pulse">
      <div className="w-10 h-10 rounded bg-muted" />
      <div className="flex-1 space-y-2">
        <div className="h-3 w-40 bg-muted rounded" />
        <div className="h-2.5 w-56 bg-muted rounded" />
        <div className="h-2 w-32 bg-muted rounded" />
      </div>
      <div className="w-10 h-5 bg-muted rounded" />
    </div>
  );
}
