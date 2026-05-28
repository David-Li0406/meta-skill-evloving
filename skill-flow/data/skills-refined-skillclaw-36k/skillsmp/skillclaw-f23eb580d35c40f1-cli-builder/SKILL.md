---
name: cli-builder
description: Use this skill when creating TypeScript command-line tools with Bun, including argument parsing, subcommand patterns, and output formatting.
---

# CLI Builder

Build TypeScript command-line tools with Bun.

## When to Build a CLI

CLIs are ideal for:
- Developer tools and automation
- Project-specific commands
- Scripts that need arguments/flags
- Tools that compose with shell pipelines

## Quick Start

### Minimal CLI

```typescript
#!/usr/bin/env bun
// scripts/my-tool.ts

const args = process.argv.slice(2);
const command = args[0];

if (!command || command === "help") {
  console.log(`
Usage: my-tool <command>

Commands:
  hello    Say hello
  help     Show this message
`);
  process.exit(0);
}

if (command === "hello") {
  console.log("Hello, world!");
}
```

Run with: `bun scripts/my-tool.ts hello`

### With Argument Parsing

Use `parseArgs` from Node's `util` module (works in Bun):

```typescript
#!/usr/bin/env bun
import { parseArgs } from "util";

const { values, positionals } = parseArgs({
  args: process.argv.slice(2),
  options: {
    name: { type: "string", short: "n" },
    verbose: { type: "boolean", short: "v", default: false },
    help: { type: "boolean", short: "h", default: false },
  },
  allowPositionals: true,
});

if (values.help) {
  console.log(`
Usage: greet [options] <message>

Options:
  -n, --name <name>   Name to greet
  -v, --verbose       Verbose output
  -h, --help          Show help
`);
  process.exit(0);
}

const message = positionals[0] || "Hello";
const name = values.name || "World";

console.log(`${message}, ${name}!`);
if (values.verbose) {
  console.log(`  (greeted at ${new Date().toISOString()})`);
}
```

## Subcommand Pattern

For CLIs with multiple commands, use a command registry:

```typescript
#!/usr/bin/env bun
import { parseArgs } from "util";

type Command = {
  description: string;
  run: (args: string[]) => Promise<void>;
};

const commands: Record<string, Command> = {
  init: {
    description: "Initialize a new project",
    run: async (args) => {
      const { values } = parseArgs({
        args,
        options: {
          template: { type: "string", short: "t", default: "default" },
        },
      });
      console.log(`Initializing with template: ${values.template}`);
    },
  },

  build: {
    description: "Build the project",
    run: async (args) => {
      console.log("Building the project...");
    },
  },
};

// Example of executing a command
const commandToRun = args[0];
if (commands[commandToRun]) {
  await commands[commandToRun].run(args.slice(1));
} else {
  console.log(`Unknown command: ${commandToRun}`);
}
```