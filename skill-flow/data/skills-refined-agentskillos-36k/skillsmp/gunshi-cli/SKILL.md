---
name: gunshi-cli
description: Build TypeScript CLIs with gunshi. Use when creating command-line tools, parsing arguments, or implementing subcommands in TypeScript.
---

# Gunshi CLI

## Core API Pattern

```typescript
import { cli, define } from "gunshi";

const command = define({
  name: "greet",
  description: "A greeting command",
  args: {
    name: {
      type: "string",
      short: "n",
      description: "Name to greet",
      required: true,
    },
    times: { type: "number", short: "t", default: 1 },
  },
  run: (ctx) => {
    const { name, times } = ctx.values;
    // ctx.positionals for positional args
  },
});

await cli(process.argv.slice(2), command, {
  name: "my-app",
  version: "1.0.0",
});
```

## Argument Types & Properties

```typescript
args: {
  // String type
  input: {
    type: 'string',
    short: 'i',
    default: 'default.txt',
    required: true,
    description: 'Input file'
  },

  // Number type
  count: {
    type: 'number',
    short: 'n',
    default: 1,
    required: true
  },

  // Boolean type
  flag: {
    type: 'boolean',
    short: 'f',
    negatable: true  // Enables --no-flag
  },

  // Enum type (use 'enum' with choices)
  mode: {
    type: 'enum',
    choices: ['dev', 'prod'] as const
  },

  // Positional argument
  file: {
    type: 'positional',
    description: 'File to process'
  },

  // Custom type with parser
  config: {
    type: 'custom',
    parse: (val) => {
      const parsed = JSON.parse(val)
      if (!isValidConfig(parsed)) throw new Error('Invalid config')
      return parsed
    }
  },

  // Multiple values
  tags: {
    type: 'string',
    multiple: true  // Accepts multiple values
  },

  // Conflicting options
  format: {
    type: 'string',
    conflicts: ['raw', 'json']  // Mutually exclusive
  },

  // camelCase to kebab-case conversion
  strictMode: {
    type: 'boolean',
    toKebab: true  // CLI accepts --strict-mode
  }
}
```

**All ArgSchema Properties:**

- `type`: `'string' | 'number' | 'boolean' | 'enum' | 'positional' | 'custom'`
- `short`: Single-character alias (e.g., `'n'` for `-n`)
- `description`: Help text
- `default`: Default value
- `required`: Mark as required
- `multiple`: Accept multiple values
- `toKebab`: Convert camelCase to kebab-case in CLI
- `negatable`: Enable `--no-*` form for booleans
- `choices`: Allowed values for enum type
- `parse`: Custom parsing function for custom type
- `conflicts`: Mutually exclusive options (string or string[])

## Type Safety Patterns

**Basic inference (recommended):**

```typescript
const cmd = define({
  args: { name: { type: "string" } },
  run: (ctx) => {
    // ctx.values.name is automatically typed as string | undefined
  },
});
```

**With pre-defined args (use `as const`):**

```typescript
const args = {
  name: { type: "string" },
  count: { type: "number", default: 1 },
} as const;

const cmd = define({ args, run: (ctx) => {} });
```

**With plugin extensions (v0.27 currying pattern):**

```typescript
import { defineWithTypes } from "gunshi";

type MyExtensions = {
  logger: LoggerExtension;
};

// Use currying: defineWithTypes<T>()({ ... })
const cmd = defineWithTypes<{ extensions: MyExtensions }>()({
  name: "build",
  args: { target: { type: "string" } },
  run: (ctx) => {
    ctx.extensions.logger?.log(`Building ${ctx.values.target}`);
  },
});
```

**Combining multiple plugin types:**

```typescript
import type { I18nExtension } from "@gunshi/plugin-i18n";
import type { AuthExtension } from "./auth-plugin";
import { pluginId as i18nId } from "@gunshi/plugin-i18n";
import { pluginId as authId } from "./auth-plugin";

type CombinedExtensions = Record<typeof i18nId, I18nExtension> &
  Record<typeof authId, AuthExtension>;

const cmd = defineWithTypes<{ extensions: CombinedExtensions }>()({
  // ... command definition
});
```

## Context Object (`ctx`)

```typescript
interface CommandContext {
  // Parsed values
  values: ArgValues<Args>; // Typed argument values
  positionals: string[]; // Positional arguments
  explicit: Record<string, boolean>; // Which args user provided
  rest: string[]; // Args after '--'

  // Command metadata
  name?: string; // Current command name
  description?: string; // Command description
  args: Args; // Argument definitions

  // Environment
  env: {
    name?: string; // CLI name
    version?: string; // CLI version
    cwd?: string; // Working directory
  };

  // Utilities
  log(message?: string): void; // Output message
  extensions: Record<string, any>; // Plugin extensions (use optional chaining)

  // Call context
  callMode: "entry" | "subCommand";
  omitted: boolean; // Was command name omitted?
}
```

## Subcommands & Lazy Loading

```typescript
import { lazy } from "gunshi";

// Lazy load heavy command
const heavyCmd = lazy(
  async () => {
    const { processor } = await import("./heavy-module");
    return async (ctx) => processor(ctx.values);
  },
  {
    name: "process",
    description: "Process data",
    args: { input: { type: "string" } },
  },
);

// With plugin extensions
import { lazyWithTypes } from "gunshi";

const typedLazy = lazyWithTypes<{ extensions: MyExtensions }>()({
  loader: async () => import("./command"),
  name: "typed-command",
  args: {
    /* ... */
  },
});

// Main command with subcommands
const main = define({
  name: "cli",
  run: (ctx) => console.log("Main command"),
});

await cli(process.argv.slice(2), main, {
  name: "my-cli",
  subCommands: {
    heavy: heavyCmd,
    create: createCmd,
    list: listCmd,
  },
});
```

## CLI Configuration

```typescript
await cli(process.argv.slice(2), command, {
  name: "my-app",
  version: "1.0.0",
  description: "My CLI app",

  // Subcommands
  subCommands: { create: createCmd, list: listCmd },
  fallbackToEntry: true, // Handle unknown subcommands

  // Plugins
  plugins: [logger(), i18n()],

  // Custom rendering
  renderHeader: async (ctx) => `Custom header`,
  renderUsage: async (ctx) => `Custom usage`,
  renderValidationErrors: async (ctx, error) => `Error: ${error.message}`,

  // Hooks
  onBeforeCommand: async (ctx) => {
    /* setup */
  },
  onAfterCommand: async (ctx, result) => {
    /* cleanup */
  },
  onErrorCommand: async (ctx, error) => {
    /* handle error */
  },

  // Rendering options
  usageOptionType: true, // Show option types in help
  usageSilent: false, // Suppress output
});
```

## Plugin System Basics

```typescript
import { plugin } from "gunshi/plugin";

export default plugin({
  id: "company:logger",
  name: "Logger Plugin",
  dependencies: ["optional-plugin"],

  // Setup phase (add global options, decorators)
  setup: (ctx) => {
    ctx.addGlobalOption("verbose", {
      type: "boolean",
      description: "Enable verbose output",
    });

    // Wrap command execution
    ctx.decorateCommand((baseRunner) => async (ctx) => {
      console.log("Before command");
      const result = await baseRunner(ctx);
      console.log("After command");
      return result;
    });
  },

  // Extension phase (add ctx.extensions)
  extension: (ctx, cmd) => ({
    log: (msg) => console.log(msg),
    error: (msg) => console.error(msg),
  }),

  // Post-extension hook
  onExtension: (ctx, cmd) => {
    // Initialization after extension
  },
});
```

## Key Differences from Other Frameworks

1. **parseArgs-like API** - Unlike commander's chaining API
2. **Lazy loading built-in** - Better performance than cleye
3. **Negatable by default** - `negatable: true` auto-generates `--no-*`
4. **Type inference** - No manual type annotations needed (unlike cac)
5. **Universal runtime** - Node.js, Deno, Bun supported
6. **v0.27 type system** - GunshiParams for comprehensive type safety

## Gotchas

1. **Plugin extensions need `defineWithTypes<T>()()`** - Note the currying pattern in v0.27
2. **Use `as const` for external args** - Type inference fails without it
3. **Help/version built-in** - Don't manually implement `-h` or `-v`
4. **Optional chaining for extensions** - Plugins may not be installed: `ctx.extensions.logger?.log()`
5. **Positional vs named args** - Use `type: 'positional'` for position-based arguments
6. **Custom parsers throw errors** - Validation errors in `parse()` stop execution

## Real-world Projects

- pnpmc (PNPM Catalogs)
- sourcemap-publisher
- curxy (Ollama proxy)
- varlock (.env loader)
- ccusage (Claude Code usage analyzer)
