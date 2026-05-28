import * as React from 'react';
import { cn } from '@/lib/utils';
import { LucideIcon } from 'lucide-react';

export interface ActionResultProps {
  action: {
    icon: LucideIcon;
    name: string;
    description: string;
    shortcut?: string;
    disabled?: boolean;
    destructive?: boolean;
  };
  selected: boolean;
  onClick: () => void;
}

// Format keyboard shortcut with platform-aware symbols
const formatShortcut = (shortcut: string): string => {
  const isMac =
    typeof navigator !== 'undefined' && navigator.platform.startsWith('Mac');

  return shortcut
    .replace(/Cmd|Command/gi, isMac ? '⌘' : 'Ctrl')
    .replace(/Ctrl/g, isMac ? '^' : 'Ctrl')
    .replace(/Alt/g, isMac ? '⌥' : 'Alt')
    .replace(/Shift/g, isMac ? '⇧' : 'Shift')
    .replace(/Enter|Return/g, '↵')
    .replace(/Backspace/g, '⌫')
    .replace(/Delete/g, '⌦')
    .replace(/Escape|Esc/g, '⎋')
    .replace(/ArrowUp|Up/g, '↑')
    .replace(/ArrowDown|Down/g, '↓')
    .replace(/ArrowLeft|Left/g, '←')
    .replace(/ArrowRight|Right/g, '→');
};

// Split shortcut into individual keys for display
const parseShortcut = (shortcut: string): string[] => {
  return formatShortcut(shortcut).split('+');
};

export function ActionResult({ action, selected, onClick }: ActionResultProps) {
  const { icon: Icon, name, description, shortcut, disabled, destructive } =
    action;

  return (
    <button
      type="button"
      role="option"
      aria-selected={selected}
      aria-disabled={disabled}
      onClick={onClick}
      disabled={disabled}
      className={cn(
        'w-full flex items-center gap-3 px-3 py-2 text-left',
        'transition-colors duration-150 ease-out',
        'focus:outline-none min-h-[3rem]',
        disabled
          ? 'opacity-50 cursor-not-allowed'
          : selected
            ? destructive
              ? 'bg-destructive/10 text-destructive'
              : 'bg-primary/10 text-primary'
            : destructive
              ? 'hover:bg-destructive/5 text-destructive/90'
              : 'hover:bg-muted/50 text-foreground'
      )}
    >
      {/* Action icon */}
      <div className="flex-shrink-0">
        <div
          className={cn(
            'w-8 h-8 flex items-center justify-center rounded',
            destructive ? 'bg-destructive/10' : 'bg-muted/50'
          )}
        >
          <Icon
            className={cn(
              'w-4 h-4',
              destructive ? 'text-destructive' : 'text-foreground'
            )}
          />
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        {/* Action name - Primary text */}
        <div className="font-medium text-sm">{name}</div>

        {/* Description - Secondary text */}
        <div className="text-xs text-muted-foreground truncate">
          {description}
        </div>
      </div>

      {/* Keyboard shortcut */}
      {shortcut && (
        <div className="flex-shrink-0 flex items-center gap-1" aria-label={`Shortcut: ${shortcut}`}>
          {parseShortcut(shortcut).map((key, index) => (
            <React.Fragment key={index}>
              {index > 0 && (
                <span className="text-xs text-muted-foreground">+</span>
              )}
              <kbd
                className={cn(
                  'inline-flex items-center justify-center',
                  'min-w-6 h-6 px-1.5 rounded',
                  'text-xs font-mono font-medium',
                  'border border-border bg-muted/50 text-foreground shadow-sm'
                )}
              >
                {key}
              </kbd>
            </React.Fragment>
          ))}
        </div>
      )}
    </button>
  );
}

// Skeleton loading state
export function ActionResultSkeleton() {
  return (
    <div className="flex items-center gap-3 px-3 py-2 min-h-[3rem] animate-pulse">
      <div className="w-8 h-8 rounded bg-muted" />
      <div className="flex-1 space-y-2">
        <div className="h-3 w-32 bg-muted rounded" />
        <div className="h-2.5 w-48 bg-muted rounded" />
      </div>
      <div className="flex gap-1">
        <div className="w-6 h-6 bg-muted rounded" />
        <div className="w-6 h-6 bg-muted rounded" />
      </div>
    </div>
  );
}
