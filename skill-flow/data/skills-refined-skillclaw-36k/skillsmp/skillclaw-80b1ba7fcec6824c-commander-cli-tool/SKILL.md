---
name: commander-cli-tool
description: Use this skill when building command-line interfaces in Node.js with Commander.js, covering commands, options, arguments, and help text customization.
---

# Commander.js CLI Tool Skill

## Overview

This skill provides comprehensive guidance for building command-line interfaces (CLI) in Node.js using the Commander.js library. It includes common patterns for defining commands, options, arguments, and customizing the help system.

## Quick Start

### Installation

```bash
npm install commander
```

### Basic Program

```js
const { Command } = require('commander');
const program = new Command();

program
  .name('my-cli')
  .version('1.0.0')
  .description('CLI tool for managing tasks');

program
  .command('add <task>')
  .description('Add a new task')
  .action((task) => {
    console.log(`Added task: ${task}`);
  });

program
  .command('list')
  .description('List all tasks')
  .action(() => {
    console.log('Listing tasks...');
  });

program.parse();
```

## Command Patterns

| Pattern         | Syntax                | Description                     |
|------------------|----------------------|---------------------------------|
| Required arg     | `<name>`             | Must be provided                |
| Optional arg     | `[name]`             | Can be omitted                  |
| Variadic         | `<files...>`         | Multiple values                 |
| Option value     | `-o, --out <file>`   | Option with value               |
| Boolean flag     | `-v, --verbose`      | True when present               |
| Negatable        | `--no-cache`         | Sets cache=false                |

## Common Options

### Boolean Options

```js
program.option('-d, --debug', 'enable debug mode');
// Usage: my-cli --debug
```

### Value Options

```js
program.option('-p, --port <number>', 'server port');
// Usage: my-cli --port 8080
```

### Required Options

```js
program.requiredOption('-c, --config <path>', 'Config file');
// Usage: my-cli --config config.json
```

### Default Values

```js
program.option('-p, --port <number>', 'Port', '3000');
// Default: 3000 if not specified
```

## Subcommands

```js
const build = program.command('build');

build
  .command('dev')
  .description('Development build')
  .action(() => { /* ... */ });

build
  .command('prod')
  .description('Production build')
  .action(() => { /* ... */ });
```

## Tips

- Use `program.parse()` at the end, or `program.parseAsync()` for async operations.
- Access arguments via the action callback or `program.args`.
- Use `.alias('b')` for command shortcuts.
- Add examples with `.addHelpText('after', 'Examples:\n  $ mycli build src/')`.