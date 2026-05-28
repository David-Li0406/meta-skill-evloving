---
name: commander-cli-tool-building
description: Use this skill when building command-line interfaces in Node.js with Commander.js, covering commands, options, arguments, and help text customization.
---

# Commander.js CLI Tool Building

## Overview

This skill provides comprehensive guidance for building command-line interfaces (CLI) in Node.js using Commander.js. It includes patterns for defining commands, options, arguments, and customizing the help system.

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
  .command('build <input>')
  .description('Build the project')
  .option('-o, --output <file>', 'Output file', 'output.json')
  .option('-w, --watch', 'Watch mode')
  .option('-v, --verbose', 'Verbose output')
  .action((input, options) => {
    console.log(`Building ${input} to ${options.output}`);
    if (options.watch) startWatcher();
  });

program.parse();
```

## Command Patterns

| Pattern          | Syntax                     | Description                     |
|------------------|----------------------------|---------------------------------|
| Required arg     | `<name>`                   | Must be provided                |
| Optional arg     | `[name]`                   | Can be omitted                  |
| Variadic         | `<files...>`               | Multiple values                 |
| Option value     | `-o, --out <file>`         | Option with value               |
| Boolean flag     | `-v, --verbose`            | True when present               |
| Negatable        | `--no-cache`               | Sets cache=false                |

## Common Patterns

### Options

- **Boolean Options**: 
  ```js
  program.option('-d, --debug', 'enable debug mode');
  ```

- **Value Options**: 
  ```js
  program.option('-p, --port <number>', 'server port', 3000);
  ```

- **Required Options**: 
  ```js
  program.requiredOption('-c, --config <path>', 'Config file');
  ```

- **Choices**: 
  ```js
  program.option('-e, --env <env>', 'Environment').choices(['dev', 'prod']);
  ```

### Commands and Subcommands

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

## Help System Customization

### Custom Help Text

```js
program.addHelpText('after', `
Example call:
  $ my-cli --help`);
```

### Show Help After Error

```js
program.showHelpAfterError();
```

## Error Handling

```js
program.exitOverride(); // Throw instead of process.exit
```

## Advanced Features

### Parsing Configuration

```js
program.enablePositionalOptions();
program.passThroughOptions();
program.allowUnknownOption();
program.allowExcessArguments();
```

### TypeScript Support

```js
import { Command } from '@commander-js/extra-typings';
const program = new Command();
```

## Resources

For comprehensive API documentation including all options, commands, arguments, help system customization, and advanced features, refer to the detailed API reference.