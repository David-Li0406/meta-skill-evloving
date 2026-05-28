import * as React from 'react';
import { cn } from '@/lib/utils';
import { LucideIcon, ExternalLink, Clock } from 'lucide-react';

export interface NavigationResultProps {
  route: {
    icon?: LucideIcon;
    name: string;
    path: string;
    section?: string;
    recent?: boolean;
    external?: boolean;
  };
  selected: boolean;
  onClick: () => void;
}

// Format breadcrumb trail from path
const formatBreadcrumb = (path: string): string[] => {
  return path
    .split('/')
    .filter((segment) => segment.length > 0)
    .map((segment) => {
      // Capitalize first letter and replace hyphens/underscores with spaces
      return segment
        .replace(/[-_]/g, ' ')
        .split(' ')
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
    });
};

// Truncate path if too long
const truncatePath = (path: string, maxLength: number = 60): string => {
  if (path.length <= maxLength) return path;
  const parts = path.split('/');
  if (parts.length <= 3) return path;

  return `/${parts[1]}/.../${parts[parts.length - 1]}`;
};

export function NavigationResult({
  route,
  selected,
  onClick,
}: NavigationResultProps) {
  const { icon: Icon, name, path, section, recent, external } = route;
  const breadcrumbs = formatBreadcrumb(path);

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
      {/* Icon or breadcrumb indicator */}
      <div className="flex-shrink-0">
        {Icon ? (
          <div className="w-9 h-9 flex items-center justify-center rounded bg-muted/50">
            <Icon className="w-4 h-4 text-foreground" />
          </div>
        ) : (
          <div className="w-9 h-9 flex items-center justify-center rounded bg-gradient-to-br from-primary/20 to-primary/10">
            <span className="text-xs font-medium text-primary">
              {breadcrumbs[0]?.[0] || '/'}
            </span>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        {/* Route name - Primary text */}
        <div className="flex items-center gap-2">
          <span className="font-medium text-sm truncate">{name}</span>

          {/* Recent indicator */}
          {recent && (
            <span className="flex-shrink-0">
              <Clock className="w-3 h-3 text-muted-foreground" />
            </span>
          )}

          {/* External link indicator */}
          {external && (
            <span className="flex-shrink-0">
              <ExternalLink className="w-3 h-3 text-muted-foreground" />
            </span>
          )}
        </div>

        {/* Route path - Secondary text */}
        <div
          className="text-xs text-muted-foreground truncate font-mono"
          title={path}
        >
          {truncatePath(path)}
        </div>

        {/* Parent section (if provided) */}
        {section && (
          <div className="text-xs text-muted-foreground/75 mt-0.5">
            <span className="truncate">{section}</span>
          </div>
        )}
      </div>

      {/* Breadcrumb trail (visual only) */}
      {breadcrumbs.length > 1 && (
        <div className="flex-shrink-0 hidden sm:flex items-center gap-1 text-xs text-muted-foreground">
          {breadcrumbs.slice(0, 3).map((crumb, index) => (
            <React.Fragment key={index}>
              {index > 0 && <span>/</span>}
              <span className="truncate max-w-[80px]">{crumb}</span>
            </React.Fragment>
          ))}
          {breadcrumbs.length > 3 && (
            <>
              <span>/</span>
              <span>...</span>
            </>
          )}
        </div>
      )}
    </button>
  );
}

// Skeleton loading state
export function NavigationResultSkeleton() {
  return (
    <div className="flex items-center gap-3 px-3 py-2 h-14 animate-pulse">
      <div className="w-9 h-9 rounded bg-muted" />
      <div className="flex-1 space-y-2">
        <div className="h-3 w-40 bg-muted rounded" />
        <div className="h-2.5 w-56 bg-muted rounded" />
      </div>
      <div className="hidden sm:flex gap-1">
        <div className="h-2.5 w-16 bg-muted rounded" />
        <div className="h-2.5 w-16 bg-muted rounded" />
      </div>
    </div>
  );
}
