import * as React from 'react';
import { cn } from '@/lib/utils';

export interface PersonResultProps {
  person: {
    avatar?: string;
    name: string;
    role: string;
    status?: 'online' | 'offline' | 'away';
    metadata?: {
      email?: string;
      department?: string;
      location?: string;
    };
  };
  selected: boolean;
  onClick: () => void;
}

export function PersonResult({ person, selected, onClick }: PersonResultProps) {
  const { avatar, name, role, status, metadata } = person;

  // Generate initials fallback from name
  const getInitials = (name: string): string => {
    return name
      .split(' ')
      .map((part) => part[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  const statusColors = {
    online: 'bg-green-500',
    offline: 'bg-gray-400',
    away: 'bg-amber-500',
  };

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
      {/* Avatar or Initials */}
      <div className="relative flex-shrink-0">
        <div
          className={cn(
            'w-10 h-10 rounded-full flex items-center justify-center',
            'font-medium text-sm',
            avatar
              ? 'bg-transparent'
              : 'bg-gradient-to-br from-primary/20 to-primary/10 text-primary'
          )}
        >
          {avatar ? (
            <img
              src={avatar}
              alt={`${name}'s avatar`}
              className="w-full h-full rounded-full object-cover"
            />
          ) : (
            getInitials(name)
          )}
        </div>

        {/* Status indicator */}
        {status && (
          <div
            className={cn(
              'absolute bottom-0 right-0 w-3 h-3 rounded-full border-2 border-background',
              statusColors[status]
            )}
            aria-label={`Status: ${status}`}
          />
        )}
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        {/* Name - Primary text */}
        <div className="font-semibold text-sm truncate">{name}</div>

        {/* Role - Secondary text */}
        <div className="text-xs text-muted-foreground truncate">{role}</div>

        {/* Optional metadata */}
        {metadata && (
          <div className="flex gap-2 text-xs text-muted-foreground/75 truncate mt-0.5">
            {metadata.email && <span>{metadata.email}</span>}
            {metadata.department && (
              <>
                {metadata.email && <span>•</span>}
                <span>{metadata.department}</span>
              </>
            )}
            {metadata.location && (
              <>
                {(metadata.email || metadata.department) && <span>•</span>}
                <span>{metadata.location}</span>
              </>
            )}
          </div>
        )}
      </div>
    </button>
  );
}

// Skeleton loading state
export function PersonResultSkeleton() {
  return (
    <div className="flex items-center gap-3 px-3 py-2 h-14 animate-pulse">
      <div className="w-10 h-10 rounded-full bg-muted" />
      <div className="flex-1 space-y-2">
        <div className="h-3 w-32 bg-muted rounded" />
        <div className="h-2.5 w-24 bg-muted rounded" />
      </div>
    </div>
  );
}
