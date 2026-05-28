# Command Palette Plugin System

Extensibility patterns for third-party command providers.

## Command Provider Interface

```typescript
interface CommandProvider {
  id: string;
  name: string;
  getCommands(): Command[] | Promise<Command[]>;
  onEnable?(): void;
  onDisable?(): void;
}

class CommandRegistry {
  private providers = new Map<string, CommandProvider>();

  registerProvider(provider: CommandProvider) {
    this.providers.set(provider.id, provider);
    provider.onEnable?.();
  }

  unregisterProvider(id: string) {
    const provider = this.providers.get(id);
    provider?.onDisable?.();
    this.providers.delete(id);
  }

  async getAllCommands(): Promise<Command[]> {
    const commands = await Promise.all(
      Array.from(this.providers.values()).map((p) => p.getCommands())
    );
    return commands.flat();
  }
}
```

## Creating a Provider

```typescript
const gitProvider: CommandProvider = {
  id: 'git-commands',
  name: 'Git Commands',

  getCommands: () => [
    {
      id: 'git-commit',
      label: 'Git: Commit',
      keywords: ['git', 'commit', 'save'],
      onSelect: () => execGitCommit(),
    },
    {
      id: 'git-push',
      label: 'Git: Push',
      keywords: ['git', 'push', 'upload'],
      onSelect: () => execGitPush(),
    },
  ],

  onEnable: () => console.log('Git provider enabled'),
  onDisable: () => console.log('Git provider disabled'),
};

registry.registerProvider(gitProvider);
```

## Dynamic Command Loading

```typescript
const extensionProvider: CommandProvider = {
  id: 'extensions',
  name: 'Extensions',

  async getCommands() {
    const extensions = await fetchInstalledExtensions();
    return extensions.map((ext) => ({
      id: `ext-${ext.id}`,
      label: ext.name,
      onSelect: () => ext.activate(),
    }));
  },
};
```
