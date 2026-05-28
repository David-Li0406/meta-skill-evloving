// Unit tests for actions registry

import { describe, it, expect, beforeEach } from 'vitest';
import {
  registerCommand,
  unregisterCommand,
  getCommands,
  getCommandsByCategory,
  searchCommands,
  enableCommand,
  disableCommand,
  clearCommands,
  registerMultiple,
  actionsRegistry,
} from './actions-registry';
import type { AppAction } from './actions-registry';

describe('ActionsRegistry', () => {
  const mockAction1: AppAction = {
    id: 'test-action-1',
    name: 'Test Action 1',
    description: 'First test action',
    category: 'Actions',
    action: () => console.log('Action 1 executed'),
  };

  const mockAction2: AppAction = {
    id: 'test-action-2',
    name: 'Go to Dashboard',
    description: 'Navigate to dashboard',
    category: 'Navigation',
    action: () => console.log('Action 2 executed'),
  };

  const mockAction3: AppAction = {
    id: 'test-action-3',
    name: 'Create Project',
    description: 'Create a new project',
    category: 'Create',
    action: () => console.log('Action 3 executed'),
  };

  beforeEach(() => {
    clearCommands();
  });

  describe('registerCommand', () => {
    it('should register a new command', () => {
      registerCommand(mockAction1);
      const commands = getCommands();

      expect(commands).toHaveLength(1);
      expect(commands[0]).toEqual(mockAction1);
    });

    it('should overwrite existing command with same id', () => {
      registerCommand(mockAction1);

      const updatedAction = {
        ...mockAction1,
        name: 'Updated Action',
      };

      registerCommand(updatedAction);
      const commands = getCommands();

      expect(commands).toHaveLength(1);
      expect(commands[0].name).toBe('Updated Action');
    });
  });

  describe('unregisterCommand', () => {
    it('should remove a command by id', () => {
      registerCommand(mockAction1);
      registerCommand(mockAction2);

      unregisterCommand('test-action-1');
      const commands = getCommands();

      expect(commands).toHaveLength(1);
      expect(commands[0].id).toBe('test-action-2');
    });

    it('should not throw when unregistering non-existent command', () => {
      expect(() => unregisterCommand('non-existent')).not.toThrow();
    });
  });

  describe('getCommands', () => {
    it('should return empty array when no commands registered', () => {
      const commands = getCommands();
      expect(commands).toEqual([]);
    });

    it('should return all registered commands', () => {
      registerCommand(mockAction1);
      registerCommand(mockAction2);
      registerCommand(mockAction3);

      const commands = getCommands();
      expect(commands).toHaveLength(3);
    });
  });

  describe('getCommandsByCategory', () => {
    it('should group commands by category', () => {
      registerCommand(mockAction1);
      registerCommand(mockAction2);
      registerCommand(mockAction3);

      const grouped = getCommandsByCategory();

      expect(grouped.Actions).toHaveLength(1);
      expect(grouped.Navigation).toHaveLength(1);
      expect(grouped.Create).toHaveLength(1);
      expect(grouped.Settings).toHaveLength(0);
      expect(grouped.Help).toHaveLength(0);
    });

    it('should return empty arrays for all categories when no commands', () => {
      const grouped = getCommandsByCategory();

      expect(grouped.Actions).toEqual([]);
      expect(grouped.Navigation).toEqual([]);
      expect(grouped.Create).toEqual([]);
      expect(grouped.Settings).toEqual([]);
      expect(grouped.Help).toEqual([]);
    });
  });

  describe('searchCommands', () => {
    beforeEach(() => {
      registerCommand(mockAction1);
      registerCommand(mockAction2);
      registerCommand(mockAction3);
    });

    it('should return all commands when query is empty', () => {
      const results = searchCommands('');
      expect(results).toHaveLength(3);
    });

    it('should filter commands by name', () => {
      const results = searchCommands('dashboard');
      expect(results).toHaveLength(1);
      expect(results[0].id).toBe('test-action-2');
    });

    it('should filter commands by description', () => {
      const results = searchCommands('navigate');
      expect(results).toHaveLength(1);
      expect(results[0].id).toBe('test-action-2');
    });

    it('should filter commands by category', () => {
      const results = searchCommands('create');
      expect(results).toHaveLength(1);
      expect(results[0].id).toBe('test-action-3');
    });

    it('should be case insensitive', () => {
      const results = searchCommands('DASHBOARD');
      expect(results).toHaveLength(1);
      expect(results[0].id).toBe('test-action-2');
    });

    it('should prioritize name matches over description matches', () => {
      const actionWithMatchInName: AppAction = {
        id: 'name-match',
        name: 'Project Manager',
        description: 'Manage your projects',
        category: 'Actions',
        action: () => {},
      };

      const actionWithMatchInDesc: AppAction = {
        id: 'desc-match',
        name: 'File Browser',
        description: 'Browse project files',
        category: 'Actions',
        action: () => {},
      };

      registerCommand(actionWithMatchInName);
      registerCommand(actionWithMatchInDesc);

      const results = searchCommands('project');

      expect(results[0].id).toBe('name-match');
      expect(results[1].id).toBe('desc-match');
    });

    it('should return empty array when no matches found', () => {
      const results = searchCommands('nonexistent');
      expect(results).toEqual([]);
    });
  });

  describe('enableCommand and disableCommand', () => {
    beforeEach(() => {
      registerCommand(mockAction1);
    });

    it('should disable a command', () => {
      disableCommand('test-action-1');
      const commands = getCommands();

      expect(commands[0].disabled).toBe(true);
    });

    it('should enable a command', () => {
      disableCommand('test-action-1');
      enableCommand('test-action-1');
      const commands = getCommands();

      expect(commands[0].disabled).toBe(false);
    });

    it('should not throw when enabling/disabling non-existent command', () => {
      expect(() => enableCommand('non-existent')).not.toThrow();
      expect(() => disableCommand('non-existent')).not.toThrow();
    });
  });

  describe('registerMultiple', () => {
    it('should register multiple commands at once', () => {
      registerMultiple([mockAction1, mockAction2, mockAction3]);
      const commands = getCommands();

      expect(commands).toHaveLength(3);
    });

    it('should handle empty array', () => {
      registerMultiple([]);
      const commands = getCommands();

      expect(commands).toEqual([]);
    });
  });

  describe('clearCommands', () => {
    it('should remove all commands', () => {
      registerCommand(mockAction1);
      registerCommand(mockAction2);
      registerCommand(mockAction3);

      clearCommands();
      const commands = getCommands();

      expect(commands).toEqual([]);
    });
  });

  describe('actionsRegistry singleton', () => {
    it('should expose the same instance across imports', () => {
      registerCommand(mockAction1);

      // Access through singleton
      const commandsFromSingleton = actionsRegistry.getCommands();
      const commandsFromFunction = getCommands();

      expect(commandsFromSingleton).toEqual(commandsFromFunction);
    });
  });
});
