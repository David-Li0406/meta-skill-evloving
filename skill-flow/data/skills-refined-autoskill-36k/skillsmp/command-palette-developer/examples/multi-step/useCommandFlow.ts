import { useState, useCallback } from 'react';

export interface Command {
  id: string;
  name: string;
  description?: string;
  icon?: React.ComponentType<{ className?: string }>;
  action?: () => void | Promise<void>;
  nextLevel?: Command[];
}

export interface BreadcrumbItem {
  name: string;
  level: number;
}

export interface UseCommandFlowResult {
  stack: Command[];
  currentLevel: number;
  breadcrumb: BreadcrumbItem[];
  currentCommands: Command[];
  push: (command: Command) => void;
  pop: () => void;
  reset: () => void;
  navigateTo: (level: number) => void;
  executeCommand: (command: Command) => void;
}

/**
 * Custom hook for managing multi-step command flow state
 *
 * Manages a command stack for nested navigation with breadcrumb tracking.
 * Useful for workflows like: Select Repository → Choose Action → Confirm
 *
 * @param rootCommands - Initial commands at level 0
 * @param onCommandExecute - Optional callback when a command is executed
 * @param persistKey - Optional localStorage key for persisting state
 *
 * @returns Command flow state and navigation methods
 *
 * @example
 * ```tsx
 * const { stack, breadcrumb, currentCommands, push, pop, reset } = useCommandFlow(
 *   repositories,
 *   (cmd) => console.log('Executed:', cmd.name),
 *   'repo-workflow'
 * );
 *
 * // Navigate into a level
 * push(selectedRepo);
 *
 * // Go back
 * pop();
 *
 * // Jump to specific level
 * navigateTo(0);
 *
 * // Reset to root
 * reset();
 * ```
 */
export function useCommandFlow(
  rootCommands: Command[],
  onCommandExecute?: (command: Command) => void,
  persistKey?: string
): UseCommandFlowResult {
  // Initialize state from localStorage if persistKey provided
  const [stack, setStack] = useState<Command[]>(() => {
    if (persistKey && typeof window !== 'undefined') {
      const stored = localStorage.getItem(persistKey);
      if (stored) {
        try {
          return JSON.parse(stored);
        } catch {
          return [];
        }
      }
    }
    return [];
  });

  // Persist stack to localStorage when it changes
  const persistStack = useCallback(
    (newStack: Command[]) => {
      if (persistKey && typeof window !== 'undefined') {
        localStorage.setItem(persistKey, JSON.stringify(newStack));
      }
    },
    [persistKey]
  );

  const currentLevel = stack.length;

  // Get current commands based on stack depth
  const currentCommands = stack.length === 0
    ? rootCommands
    : stack[stack.length - 1].nextLevel || [];

  // Generate breadcrumb trail from stack
  const breadcrumb: BreadcrumbItem[] = stack.map((cmd, index) => ({
    name: cmd.name,
    level: index,
  }));

  /**
   * Navigate into a command level
   * Pushes command onto stack and resets search
   */
  const push = useCallback(
    (command: Command) => {
      const newStack = [...stack, command];
      setStack(newStack);
      persistStack(newStack);
    },
    [stack, persistStack]
  );

  /**
   * Navigate back one level
   * Pops last command from stack
   */
  const pop = useCallback(() => {
    if (stack.length > 0) {
      const newStack = stack.slice(0, -1);
      setStack(newStack);
      persistStack(newStack);
    }
  }, [stack, persistStack]);

  /**
   * Reset to root level
   * Clears entire stack
   */
  const reset = useCallback(() => {
    setStack([]);
    persistStack([]);
  }, [persistStack]);

  /**
   * Navigate to specific level in stack
   * @param level - Target level (0-based index)
   */
  const navigateTo = useCallback(
    (level: number) => {
      if (level < 0 || level > stack.length) {
        return;
      }

      if (level === 0) {
        reset();
      } else {
        const newStack = stack.slice(0, level);
        setStack(newStack);
        persistStack(newStack);
      }
    },
    [stack, reset, persistStack]
  );

  /**
   * Execute a command
   * Calls command action and optional callback
   */
  const executeCommand = useCallback(
    (command: Command) => {
      if (command.action) {
        command.action();
      }
      if (onCommandExecute) {
        onCommandExecute(command);
      }
    },
    [onCommandExecute]
  );

  return {
    stack,
    currentLevel,
    breadcrumb,
    currentCommands,
    push,
    pop,
    reset,
    navigateTo,
    executeCommand,
  };
}
