// Centralized action registry for managing app commands

import type { LucideIcon } from 'lucide-react';

export interface AppAction {
  id: string;
  name: string;
  description?: string;
  icon?: LucideIcon;
  shortcut?: string;
  category: 'Navigation' | 'Actions' | 'Create' | 'Settings' | 'Help';
  action: () => void | Promise<void>;
  disabled?: boolean;
  destructive?: boolean;
}

export interface ActionCategory {
  name: string;
  actions: AppAction[];
}

class ActionsRegistry {
  private actions: Map<string, AppAction> = new Map();

  registerCommand(action: AppAction): void {
    if (this.actions.has(action.id)) {
      console.warn(`Action with id "${action.id}" already registered. Overwriting.`);
    }
    this.actions.set(action.id, action);
  }

  unregisterCommand(id: string): void {
    this.actions.delete(id);
  }

  getCommands(): AppAction[] {
    return Array.from(this.actions.values());
  }

  getCommandsByCategory(): Record<string, AppAction[]> {
    const commandsByCategory: Record<string, AppAction[]> = {
      Navigation: [],
      Actions: [],
      Create: [],
      Settings: [],
      Help: [],
    };

    this.actions.forEach((action) => {
      commandsByCategory[action.category].push(action);
    });

    return commandsByCategory;
  }

  getCommandById(id: string): AppAction | undefined {
    return this.actions.get(id);
  }

  searchCommands(query: string): AppAction[] {
    if (!query) {
      return this.getCommands();
    }

    const normalizedQuery = query.toLowerCase();

    return this.getCommands().filter((action) => {
      const nameMatch = action.name.toLowerCase().includes(normalizedQuery);
      const descriptionMatch = action.description?.toLowerCase().includes(normalizedQuery);
      const categoryMatch = action.category.toLowerCase().includes(normalizedQuery);

      return nameMatch || descriptionMatch || categoryMatch;
    }).sort((a, b) => {
      // Prioritize name matches over description matches
      const aNameMatch = a.name.toLowerCase().includes(normalizedQuery);
      const bNameMatch = b.name.toLowerCase().includes(normalizedQuery);

      if (aNameMatch && !bNameMatch) return -1;
      if (!aNameMatch && bNameMatch) return 1;

      return 0;
    });
  }

  enableCommand(id: string): void {
    const action = this.actions.get(id);
    if (action) {
      action.disabled = false;
    }
  }

  disableCommand(id: string): void {
    const action = this.actions.get(id);
    if (action) {
      action.disabled = true;
    }
  }

  clear(): void {
    this.actions.clear();
  }

  registerMultiple(actions: AppAction[]): void {
    actions.forEach((action) => this.registerCommand(action));
  }
}

// Singleton instance
export const actionsRegistry = new ActionsRegistry();

// Convenience exports
export const registerCommand = (action: AppAction): void =>
  actionsRegistry.registerCommand(action);

export const unregisterCommand = (id: string): void =>
  actionsRegistry.unregisterCommand(id);

export const getCommands = (): AppAction[] =>
  actionsRegistry.getCommands();

export const getCommandsByCategory = (): Record<string, AppAction[]> =>
  actionsRegistry.getCommandsByCategory();

export const searchCommands = (query: string): AppAction[] =>
  actionsRegistry.searchCommands(query);

export const enableCommand = (id: string): void =>
  actionsRegistry.enableCommand(id);

export const disableCommand = (id: string): void =>
  actionsRegistry.disableCommand(id);

export const clearCommands = (): void =>
  actionsRegistry.clear();

export const registerMultiple = (actions: AppAction[]): void =>
  actionsRegistry.registerMultiple(actions);
