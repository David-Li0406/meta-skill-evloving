import { useEffect, useState } from 'react';
import { ChevronRight, X } from 'lucide-react';
import { Dialog, DialogContent } from '@/components/ui/dialog';
import { Command, CommandInput, CommandList } from '@/components/ui/command';
import { CommandStep } from './CommandStep';
import { useCommandFlow, type Command as CommandType } from './useCommandFlow';
import { cn } from '@/lib/utils';

export interface MultiStepPaletteProps {
  /**
   * Whether the palette is open
   */
  open: boolean;

  /**
   * Callback when open state changes
   */
  onOpenChange: (open: boolean) => void;

  /**
   * Root commands to display at level 0
   */
  rootCommands: CommandType[];

  /**
   * Optional callback when command is executed
   */
  onCommandExecute?: (command: CommandType) => void;

  /**
   * Optional localStorage key for persisting state
   */
  persistKey?: string;

  /**
   * Custom placeholder text
   */
  placeholder?: string;
}

/**
 * Multi-step command palette with breadcrumb navigation (Raycast-style)
 *
 * Features:
 * - Command stack: root → level 1 → level 2
 * - Breadcrumb trail at top showing navigation path
 * - Back navigation: Backspace or ESC in empty search
 * - Dynamic commands based on previous selection
 * - Smooth transition between levels with slide animation
 * - State persistence across palette close/open
 *
 * @example
 * ```tsx
 * const { open, setOpen } = useCommandPalette();
 *
 * <MultiStepPalette
 *   open={open}
 *   onOpenChange={setOpen}
 *   rootCommands={repositories}
 *   onCommandExecute={(cmd) => console.log('Executed:', cmd.name)}
 *   persistKey="repo-workflow"
 * />
 * ```
 */
export function MultiStepPalette({
  open,
  onOpenChange,
  rootCommands,
  onCommandExecute,
  persistKey,
  placeholder = 'Search or select a command...',
}: MultiStepPaletteProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [isNavigating, setIsNavigating] = useState(false);

  const {
    stack,
    currentLevel,
    breadcrumb,
    currentCommands,
    push,
    pop,
    reset,
    navigateTo,
    executeCommand,
  } = useCommandFlow(rootCommands, onCommandExecute, persistKey);

  // Filter commands based on search query
  const filteredCommands = searchQuery
    ? currentCommands.filter((cmd) => {
        const query = searchQuery.toLowerCase();
        return (
          cmd.name.toLowerCase().includes(query) ||
          cmd.description?.toLowerCase().includes(query)
        );
      })
    : currentCommands;

  // Auto-select first command when list changes
  useEffect(() => {
    if (filteredCommands.length > 0) {
      setSelectedId(filteredCommands[0].id);
    } else {
      setSelectedId(null);
    }
  }, [filteredCommands]);

  // Clear search when dialog closes or level changes
  useEffect(() => {
    if (!open) {
      setSearchQuery('');
    }
  }, [open]);

  useEffect(() => {
    setSearchQuery('');
  }, [currentLevel]);

  // Handle command selection
  const handleSelect = (command: CommandType) => {
    setIsNavigating(true);

    // If command has next level, navigate into it
    if (command.nextLevel && command.nextLevel.length > 0) {
      push(command);
    } else {
      // Execute terminal command and close palette
      executeCommand(command);
      onOpenChange(false);
      reset();
    }

    setTimeout(() => setIsNavigating(false), 300);
  };

  // Handle keyboard shortcuts
  const handleKeyDown = (e: React.KeyboardEvent) => {
    // Backspace with empty search goes back
    if (e.key === 'Backspace' && !searchQuery && currentLevel > 0) {
      e.preventDefault();
      pop();
    }

    // Escape with empty search goes back, otherwise clears search
    if (e.key === 'Escape') {
      if (searchQuery) {
        e.preventDefault();
        setSearchQuery('');
      } else if (currentLevel > 0) {
        e.preventDefault();
        pop();
      }
    }

    // Enter executes selected command
    if (e.key === 'Enter' && selectedId) {
      e.preventDefault();
      const selected = filteredCommands.find((cmd) => cmd.id === selectedId);
      if (selected) {
        handleSelect(selected);
      }
    }

    // Arrow keys for navigation
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      const currentIndex = filteredCommands.findIndex(
        (cmd) => cmd.id === selectedId
      );

      if (e.key === 'ArrowDown') {
        const nextIndex = (currentIndex + 1) % filteredCommands.length;
        setSelectedId(filteredCommands[nextIndex].id);
      } else {
        const prevIndex =
          currentIndex <= 0 ? filteredCommands.length - 1 : currentIndex - 1;
        setSelectedId(filteredCommands[prevIndex].id);
      }
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl p-0 gap-0">
        <Command
          className="rounded-lg border-0 shadow-none"
          onKeyDown={handleKeyDown}
        >
          {/* Breadcrumb Header */}
          {currentLevel > 0 && (
            <div className="flex items-center gap-2 border-b px-4 py-2 text-sm text-muted-foreground">
              <button
                onClick={() => navigateTo(0)}
                className="hover:text-foreground transition-colors"
              >
                Home
              </button>
              {breadcrumb.map((crumb, index) => (
                <div key={crumb.level} className="flex items-center gap-2">
                  <ChevronRight className="h-3 w-3" />
                  <button
                    onClick={() => navigateTo(index + 1)}
                    className={cn(
                      'hover:text-foreground transition-colors',
                      index === breadcrumb.length - 1 && 'font-medium text-foreground'
                    )}
                  >
                    {crumb.name}
                  </button>
                </div>
              ))}
              <button
                onClick={() => reset()}
                className="ml-auto hover:text-foreground transition-colors"
                title="Reset to root"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          )}

          {/* Search Input */}
          <CommandInput
            placeholder={placeholder}
            value={searchQuery}
            onValueChange={setSearchQuery}
            className="border-0"
          />

          {/* Command List */}
          <CommandList>
            <div
              className={cn(
                'transition-opacity duration-200',
                isNavigating ? 'opacity-0' : 'opacity-100'
              )}
            >
              <CommandStep
                commands={filteredCommands}
                selectedId={selectedId}
                onSelect={handleSelect}
                description={
                  currentLevel === 0
                    ? 'Select an item to continue'
                    : currentLevel === 1
                    ? 'Choose an action'
                    : 'Confirm your choice'
                }
                emptyMessage={
                  searchQuery
                    ? `No commands found for "${searchQuery}"`
                    : 'No commands available'
                }
              />
            </div>
          </CommandList>

          {/* Footer Help Text */}
          <div className="border-t px-4 py-2 text-xs text-muted-foreground flex items-center justify-between">
            <div className="flex items-center gap-4">
              <span>
                <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground">
                  ↑↓
                </kbd>{' '}
                navigate
              </span>
              <span>
                <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground">
                  Enter
                </kbd>{' '}
                select
              </span>
              {currentLevel > 0 && (
                <span>
                  <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground">
                    Backspace
                  </kbd>{' '}
                  back
                </span>
              )}
            </div>
            <div>
              Level {currentLevel + 1} of 3
            </div>
          </div>
        </Command>
      </DialogContent>
    </Dialog>
  );
}
