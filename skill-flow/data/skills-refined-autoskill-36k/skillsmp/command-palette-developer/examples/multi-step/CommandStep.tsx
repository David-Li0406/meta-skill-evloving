import { Loader2 } from 'lucide-react';
import type { Command } from './useCommandFlow';

export interface CommandStepProps {
  /**
   * Commands to display in this step
   */
  commands: Command[];

  /**
   * Currently selected command ID
   */
  selectedId: string | null;

  /**
   * Called when a command is selected
   */
  onSelect: (command: Command) => void;

  /**
   * Loading state while fetching next level
   */
  isLoading?: boolean;

  /**
   * Step description/title
   */
  description?: string;

  /**
   * Custom empty state message
   */
  emptyMessage?: string;
}

/**
 * Individual step component for multi-step command palette
 *
 * Displays commands for current level with icon, name, and description.
 * Handles command selection and loading states.
 *
 * @example
 * ```tsx
 * <CommandStep
 *   commands={repositories}
 *   selectedId={selected?.id}
 *   onSelect={(repo) => push(repo)}
 *   description="Select a repository"
 * />
 * ```
 */
export function CommandStep({
  commands,
  selectedId,
  onSelect,
  isLoading = false,
  description,
  emptyMessage = 'No commands available',
}: CommandStepProps) {
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
        <p className="mt-4 text-sm text-muted-foreground">Loading commands...</p>
      </div>
    );
  }

  if (commands.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <p className="text-sm text-muted-foreground">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col">
      {description && (
        <div className="border-b px-4 py-3">
          <p className="text-sm text-muted-foreground">{description}</p>
        </div>
      )}
      <div className="max-h-[400px] overflow-y-auto">
        {commands.map((command) => {
          const Icon = command.icon;
          const isSelected = selectedId === command.id;

          return (
            <button
              key={command.id}
              onClick={() => onSelect(command)}
              className={`
                w-full flex items-start gap-3 px-4 py-3 text-left transition-colors
                ${isSelected
                  ? 'bg-accent text-accent-foreground'
                  : 'hover:bg-accent/50'
                }
              `}
            >
              {Icon && (
                <Icon className="mt-0.5 h-5 w-5 shrink-0 text-muted-foreground" />
              )}
              <div className="flex-1 min-w-0">
                <div className="font-medium">{command.name}</div>
                {command.description && (
                  <div className="text-sm text-muted-foreground truncate">
                    {command.description}
                  </div>
                )}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

/**
 * Skeleton loading state for CommandStep
 */
export function CommandStepSkeleton() {
  return (
    <div className="space-y-2 p-4">
      {[...Array(5)].map((_, i) => (
        <div
          key={i}
          className="flex items-start gap-3 rounded-md bg-muted/50 px-4 py-3"
        >
          <div className="h-5 w-5 animate-pulse rounded bg-muted" />
          <div className="flex-1 space-y-2">
            <div className="h-4 w-1/3 animate-pulse rounded bg-muted" />
            <div className="h-3 w-2/3 animate-pulse rounded bg-muted" />
          </div>
        </div>
      ))}
    </div>
  );
}
