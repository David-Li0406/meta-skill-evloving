---
name: gunshi-cli
description: Use this skill when building command-line interfaces (CLIs) in JavaScript/TypeScript with the Gunshi library.
---

# Gunshi CLI

Gunshi is a modern JavaScript command-line library designed for creating CLIs, parsing arguments, and implementing subcommands.

## Core API Pattern

```typescript
import { cli, define } from "gunshi";

const command = define({
  name: "<command_name>",
  description: "<command_description>",
  args: {
    <arg_name>: {
      type: "<arg_type>",
      short: "<short_option>",
      description: "<arg_description>",
      required: true,
    },
    <optional_arg_name>: { type: "<optional_arg_type>", default: <default_value> },
  },
  run: (ctx) => {
    const { <arg_name> } = ctx.values;
    // ctx.positionals for positional args
  },
});

await cli(process.argv.slice(2), command, {
  name: "<cli_name>",
  version: "<cli_version>",
});
```

## Argument Types & Properties

```typescript
args: {
  // String type
  input: {
    type: 'string',
    short: 'i',
    default: '<default_value>',
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
    choices: ['<choice1>', '<choice2>'] as const
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
      const parsed = JSON.parse(val);
      if (!isValidConfig(parsed)) throw new Error('Invalid config');
      return parsed;
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

## Context Object (`ctx`)

```typescript
interface CommandContext {
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

const heavyCmd = lazy(
  async () => {
    const { processor } = await import("./heavy-module");
    return async (ctx) => processor(ctx.values);
  },
  {
    name: "<subcommand_name>",
    description: "<subcommand_description>",
    args: { input: { type: "string" } },
  },
);
```

## CLI Configuration

```typescript
await cli(process.argv.slice(2), command, {
  name: "<cli_name>",
  version: "<cli_version>",
  description: "<cli_description>",
  subCommands: { <subcommand_name>: heavyCmd },
  fallbackToEntry: true, // Handle unknown subcommands
});
```

## Plugin System Basics

```typescript
import { plugin } from "gunshi/plugin";

export default plugin({
  id: "<plugin_id>",
  name: "<plugin_name>",
  dependencies: ["<optional_plugin>"],

  setup: (ctx) => {
    ctx.addGlobalOption("<option_name>", {
      type: "boolean",
      description: "<option_description>",
    });
  },

  extension: (ctx, cmd) => ({
    log: (msg) => console.log(msg),
    error: (msg) => console.error(msg),
  }),
});
```

## Key Differences from Other Frameworks

1. **parseArgs-like API** - Unlike commander's chaining API.
2. **Lazy loading built-in** - Better performance than other libraries.
3. **Negatable by default** - `negatable: true` auto-generates `--no-*`.
4. **Type inference** - No manual type annotations needed.
5. **Universal runtime** - Node.js, Deno, Bun supported.

## Gotchas

1. **Plugin extensions need `defineWithTypes<T>()()`** - Note the currying pattern.
2. **Use `as const` for external args** - Type inference fails without it.
3. **Help/version built-in** - Don't manually implement `-h` or `-v`.
4. **Optional chaining for extensions** - Plugins may not be installed.
5. **Positional vs named args** - Use `type: 'positional'` for position-based arguments.

## Real-world Projects

- pnpmc (PNPM Catalogs)
- sourcemap-publisher
- curxy (Ollama proxy)
- varlock (.env loader)
- ccusage (Claude Code usage analyzer)