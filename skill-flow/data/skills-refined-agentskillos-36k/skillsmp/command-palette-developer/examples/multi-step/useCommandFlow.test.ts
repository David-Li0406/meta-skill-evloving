import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useCommandFlow, type Command } from './useCommandFlow';

describe('useCommandFlow', () => {
  // Mock localStorage
  const localStorageMock = (() => {
    let store: Record<string, string> = {};
    return {
      getItem: (key: string) => store[key] || null,
      setItem: (key: string, value: string) => {
        store[key] = value;
      },
      clear: () => {
        store = {};
      },
    };
  })();

  beforeEach(() => {
    Object.defineProperty(window, 'localStorage', {
      value: localStorageMock,
      writable: true,
    });
    localStorageMock.clear();
  });

  // Test command tree
  const mockCommands: Command[] = [
    {
      id: 'cmd1',
      name: 'Command 1',
      description: 'First command',
      nextLevel: [
        {
          id: 'cmd1-1',
          name: 'Command 1.1',
          action: vi.fn(),
        },
        {
          id: 'cmd1-2',
          name: 'Command 1.2',
          action: vi.fn(),
        },
      ],
    },
    {
      id: 'cmd2',
      name: 'Command 2',
      action: vi.fn(),
    },
  ];

  describe('Initialization', () => {
    it('should initialize with empty stack', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      expect(result.current.stack).toEqual([]);
      expect(result.current.currentLevel).toBe(0);
      expect(result.current.breadcrumb).toEqual([]);
      expect(result.current.currentCommands).toEqual(mockCommands);
    });

    it('should initialize with root commands', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      expect(result.current.currentCommands).toEqual(mockCommands);
    });
  });

  describe('Stack Operations', () => {
    it('should push command onto stack', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      act(() => {
        result.current.push(mockCommands[0]);
      });

      expect(result.current.stack).toEqual([mockCommands[0]]);
      expect(result.current.currentLevel).toBe(1);
      expect(result.current.currentCommands).toEqual(mockCommands[0].nextLevel);
    });

    it('should pop command from stack', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      act(() => {
        result.current.push(mockCommands[0]);
      });

      expect(result.current.currentLevel).toBe(1);

      act(() => {
        result.current.pop();
      });

      expect(result.current.stack).toEqual([]);
      expect(result.current.currentLevel).toBe(0);
      expect(result.current.currentCommands).toEqual(mockCommands);
    });

    it('should handle pop on empty stack', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      act(() => {
        result.current.pop();
      });

      expect(result.current.stack).toEqual([]);
      expect(result.current.currentLevel).toBe(0);
    });

    it('should reset stack to root', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      act(() => {
        result.current.push(mockCommands[0]);
        result.current.push(mockCommands[0].nextLevel![0]);
      });

      expect(result.current.currentLevel).toBe(2);

      act(() => {
        result.current.reset();
      });

      expect(result.current.stack).toEqual([]);
      expect(result.current.currentLevel).toBe(0);
    });

    it('should push multiple levels', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      act(() => {
        result.current.push(mockCommands[0]);
      });

      expect(result.current.currentLevel).toBe(1);

      act(() => {
        result.current.push(mockCommands[0].nextLevel![0]);
      });

      expect(result.current.currentLevel).toBe(2);
      expect(result.current.stack.length).toBe(2);
    });
  });

  describe('Breadcrumb Generation', () => {
    it('should generate empty breadcrumb at root', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      expect(result.current.breadcrumb).toEqual([]);
    });

    it('should generate breadcrumb from stack', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      act(() => {
        result.current.push(mockCommands[0]);
      });

      expect(result.current.breadcrumb).toEqual([
        { name: 'Command 1', level: 0 },
      ]);
    });

    it('should generate multi-level breadcrumb', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      act(() => {
        result.current.push(mockCommands[0]);
        result.current.push(mockCommands[0].nextLevel![0]);
      });

      expect(result.current.breadcrumb).toEqual([
        { name: 'Command 1', level: 0 },
        { name: 'Command 1.1', level: 1 },
      ]);
    });
  });

  describe('Navigation', () => {
    it('should navigate to specific level', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      act(() => {
        result.current.push(mockCommands[0]);
        result.current.push(mockCommands[0].nextLevel![0]);
      });

      expect(result.current.currentLevel).toBe(2);

      act(() => {
        result.current.navigateTo(1);
      });

      expect(result.current.currentLevel).toBe(1);
      expect(result.current.stack.length).toBe(1);
    });

    it('should navigate to root level (0)', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      act(() => {
        result.current.push(mockCommands[0]);
      });

      act(() => {
        result.current.navigateTo(0);
      });

      expect(result.current.currentLevel).toBe(0);
      expect(result.current.stack).toEqual([]);
    });

    it('should handle invalid level navigation', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      act(() => {
        result.current.push(mockCommands[0]);
      });

      const initialLevel = result.current.currentLevel;

      act(() => {
        result.current.navigateTo(-1);
      });

      expect(result.current.currentLevel).toBe(initialLevel);

      act(() => {
        result.current.navigateTo(99);
      });

      expect(result.current.currentLevel).toBe(initialLevel);
    });
  });

  describe('Command Execution', () => {
    it('should execute command action', () => {
      const onExecute = vi.fn();
      const { result } = renderHook(() =>
        useCommandFlow(mockCommands, onExecute)
      );

      const command = mockCommands[1];

      act(() => {
        result.current.executeCommand(command);
      });

      expect(command.action).toHaveBeenCalledTimes(1);
      expect(onExecute).toHaveBeenCalledWith(command);
    });

    it('should handle command without action', () => {
      const onExecute = vi.fn();
      const { result } = renderHook(() =>
        useCommandFlow(mockCommands, onExecute)
      );

      const commandWithoutAction: Command = {
        id: 'no-action',
        name: 'No Action',
      };

      act(() => {
        result.current.executeCommand(commandWithoutAction);
      });

      expect(onExecute).toHaveBeenCalledWith(commandWithoutAction);
    });

    it('should work without onExecute callback', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      const command = mockCommands[1];

      expect(() => {
        act(() => {
          result.current.executeCommand(command);
        });
      }).not.toThrow();

      expect(command.action).toHaveBeenCalledTimes(1);
    });
  });

  describe('State Persistence', () => {
    it('should persist stack to localStorage', () => {
      const persistKey = 'test-flow';
      const { result } = renderHook(() =>
        useCommandFlow(mockCommands, undefined, persistKey)
      );

      act(() => {
        result.current.push(mockCommands[0]);
      });

      const stored = localStorage.getItem(persistKey);
      expect(stored).toBeTruthy();
      expect(JSON.parse(stored!)).toEqual([mockCommands[0]]);
    });

    it('should restore stack from localStorage', () => {
      const persistKey = 'test-flow';

      // Set initial state
      localStorage.setItem(persistKey, JSON.stringify([mockCommands[0]]));

      const { result } = renderHook(() =>
        useCommandFlow(mockCommands, undefined, persistKey)
      );

      expect(result.current.stack).toEqual([mockCommands[0]]);
      expect(result.current.currentLevel).toBe(1);
    });

    it('should handle invalid localStorage data', () => {
      const persistKey = 'test-flow';

      // Set invalid JSON
      localStorage.setItem(persistKey, 'invalid-json');

      const { result } = renderHook(() =>
        useCommandFlow(mockCommands, undefined, persistKey)
      );

      expect(result.current.stack).toEqual([]);
    });

    it('should not persist without persistKey', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      act(() => {
        result.current.push(mockCommands[0]);
      });

      // Check that nothing was stored
      expect(Object.keys(localStorageMock.getItem).length).toBe(0);
    });

    it('should update localStorage on reset', () => {
      const persistKey = 'test-flow';
      const { result } = renderHook(() =>
        useCommandFlow(mockCommands, undefined, persistKey)
      );

      act(() => {
        result.current.push(mockCommands[0]);
      });

      expect(localStorage.getItem(persistKey)).toBeTruthy();

      act(() => {
        result.current.reset();
      });

      const stored = localStorage.getItem(persistKey);
      expect(stored).toBeTruthy();
      expect(JSON.parse(stored!)).toEqual([]);
    });
  });

  describe('Current Commands', () => {
    it('should return root commands at level 0', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      expect(result.current.currentCommands).toEqual(mockCommands);
    });

    it('should return nextLevel commands at level 1', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      act(() => {
        result.current.push(mockCommands[0]);
      });

      expect(result.current.currentCommands).toEqual(mockCommands[0].nextLevel);
    });

    it('should return empty array if no nextLevel', () => {
      const commandWithoutNext: Command = {
        id: 'no-next',
        name: 'No Next Level',
      };

      const { result } = renderHook(() =>
        useCommandFlow([commandWithoutNext])
      );

      act(() => {
        result.current.push(commandWithoutNext);
      });

      expect(result.current.currentCommands).toEqual([]);
    });
  });

  describe('Edge Cases', () => {
    it('should handle empty root commands', () => {
      const { result } = renderHook(() => useCommandFlow([]));

      expect(result.current.currentCommands).toEqual([]);
      expect(result.current.stack).toEqual([]);
    });

    it('should handle command without nextLevel at intermediate level', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      const terminalCommand: Command = {
        id: 'terminal',
        name: 'Terminal',
        action: vi.fn(),
      };

      act(() => {
        result.current.push(terminalCommand);
      });

      expect(result.current.currentCommands).toEqual([]);
      expect(result.current.currentLevel).toBe(1);
    });

    it('should maintain stack integrity across multiple operations', () => {
      const { result } = renderHook(() => useCommandFlow(mockCommands));

      act(() => {
        result.current.push(mockCommands[0]);
        result.current.push(mockCommands[0].nextLevel![0]);
        result.current.pop();
        result.current.push(mockCommands[0].nextLevel![1]);
      });

      expect(result.current.stack).toEqual([
        mockCommands[0],
        mockCommands[0].nextLevel![1],
      ]);
      expect(result.current.currentLevel).toBe(2);
    });
  });
});
