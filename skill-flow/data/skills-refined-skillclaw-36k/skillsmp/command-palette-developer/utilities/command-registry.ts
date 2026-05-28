// Command registry for managing palette commands

import { fuzzyMatch, fuzzyScore } from './fuzzy-search';

export interface Command {
  id: string;
  label: string;
  description?: string;
  keywords: string[];
  icon?: React.ComponentType;
  shortcut?: string;
  group?: string;
  onSelect: () => void | Promise<void>;
}

export interface CommandProvider {
  id: string;
  name: string;
  getCommands(): Command[] | Promise<Command[]>;
  onEnable?(): void;
  onDisable?(): void;
}

export class CommandRegistry {
  private commands = new Map<string, Command>();
  private providers = new Map<string, CommandProvider>();

  register(command: Command): void {
    this.commands.set(command.id, command);
  }

  unregister(id: string): void {
    this.commands.delete(id);
  }

  registerMultiple(commands: Command[]): void {
    commands.forEach((cmd) => this.register(cmd));
  }

  search(query: string): Command[] {
    if (!query) {
      return Array.from(this.commands.values());
    }

    const results = Array.from(this.commands.values())
      .map((cmd) => {
        const labelScore = fuzzyScore(query, cmd.label);
        const keywordScore = Math.max(
          ...cmd.keywords.map((kw) => fuzzyScore(query, kw))
        );
        const score = Math.max(labelScore, keywordScore);

        return { command: cmd, score };
      })
      .filter(({ score }) => score > 0)
      .sort((a, b) => b.score - a.score)
      .map(({ command }) => command);

    return results;
  }

  getGroups(): Record<string, Command[]> {
    const groups: Record<string, Command[]> = {};

    this.commands.forEach((cmd) => {
      const group = cmd.group || 'Other';
      if (!groups[group]) groups[group] = [];
      groups[group].push(cmd);
    });

    return groups;
  }

  registerProvider(provider: CommandProvider): void {
    this.providers.set(provider.id, provider);
    provider.onEnable?.();
  }

  unregisterProvider(id: string): void {
    const provider = this.providers.get(id);
    provider?.onDisable?.();
    this.providers.delete(id);
  }

  async getAllCommands(): Promise<Command[]> {
    const providerCommands = await Promise.all(
      Array.from(this.providers.values()).map((p) => p.getCommands())
    );

    const allCommands = [
      ...Array.from(this.commands.values()),
      ...providerCommands.flat(),
    ];

    return allCommands;
  }
}
