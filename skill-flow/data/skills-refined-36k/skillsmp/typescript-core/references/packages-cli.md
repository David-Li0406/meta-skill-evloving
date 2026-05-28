# Packages – CLI Development

Building command-line tools is a common task, and we have a standard set of libraries for creating CLIs with great user experience. This section covers Oclif and companion packages for CLI development.

## Oclif – The CLI Framework

**Oclif** (Open CLI Framework) by Salesforce is our go-to framework for CLIs. It provides:

- A generator and dev toolkit to scaffold CLI projects (single or multi-command).
- Parsing of arguments and flags, automatic help generation, and command grouping.
- A plugin system for extending CLIs.

### Usage & Best Practices:

- We use TypeScript with Oclif. Oclif supports TS by default; just ensure to build/compile before publishing.
- Organize commands in the `src/commands` directory. Each file exports an Oclif command class.
- Use the command class `static` properties to define `description`, `flags`, `args` clearly (so help text is informative).
- Group commands by topic using folders (e.g., `commands/user/create.ts` and `commands/user/delete.ts` -> `cli user:create` in usage).
- Always implement the `catch` method or use Oclif’s global error handling to ensure no unhandled rejections (and to format errors nicely for users).
- Leverage Oclif's `Hook` system for things like initialization (e.g., loading config, checking for updates) or teardown.

**Example**: Creating a simple command in Oclif:

```ts
import { Command, Flags } from '@oclif/core';
export class HelloCommand extends Command {
  static description = 'Prints hello message';
  static flags = {
    name: Flags.string({ char: 'n', description: 'name to greet', required: true }),
  };

  async run() {
    const { flags } = await this.parse(HelloCommand);
    this.log(`Hello, ${flags.name}!`);
  }
}
```

This gives you `mycli hello -n Alice` -> prints "Hello, Alice!".

**Plugins**: Oclif supports installing commands as plugins (npm packages). We use this for shared functionality if needed. Also, Oclif has an official update mechanism (autoupdater) if distributing CLI via npm – consider enabling it so users can auto-update.

## Ink – React for CLI UIs

For CLIs that need interactive or complex output, **Ink** is invaluable. It lets us use React components to render to the terminal:

- We can manage state within the CLI UI using React hooks (e.g., update progress, respond to user input).
- Ink has many ready-made components:
  - `ink-text-input` for text inputs,
  - `ink-select-input` for interactive selection lists,
  - `ink-spinner` for spinners,
  - `ink-table` for nicely formatted tables,
  - etc.

### When to use Ink:

- If the CLI output is dynamic (like a live updating status, or a wizard with multiple steps).
- If we want to present data in a structured layout (Ink’s `<Box>` with flexbox styles can position elements, which is easier than manual cursor control).
- For rich text (colors, big ASCII art text via `ink-big-text`, gradients).

Ink works by rendering once you call `render()` with a React element. In Oclif, you might integrate by calling an Ink app in a command’s `run`.

**Example**: using Ink in an Oclif command:

```ts
import { Command } from '@oclif/core';
import { render, Text, Box } from 'ink';
import React, { useState, useEffect } from 'react';

const Counter = () => {
  const [count, setCount] = useState(0);
  useEffect(() => {
    const timer = setInterval(() => setCount(c => c+1), 100);
    return () => clearInterval(timer);
  }, []);
  return <Text color="green">Counter: {count}</Text>;
};

export default class Demo extends Command {
  async run() {
    render(<Counter />);
  }
}
```

### Integration with Oclif:

- If using Ink for the entire interface (like a full-screen app), make sure to call `this.exit(0)` or `process.exit` after Ink unmounts if needed (Ink will exit when component tree unmounts).
- For partial tasks (like rendering a spinner via Ink’s `<Text>Loading...</Text>`), sometimes using **Ora** might be simpler. Use the right tool for complexity: Ink for complex layout, Ora for one-liners.

## Inquirer – Interactive Prompts

**Inquirer** is a mature library for asking the user questions in the terminal (and receiving answers). We use it for:

- Yes/No confirmations (instead of requiring `--force` flags all the time).
- Selecting one option from a list (e.g., choose an environment to deploy to).
- Multi-select checkboxes.
- Inputting text (with validation function if needed).
- Password inputs (masked).

Even though Ink could also handle inputs, Inquirer is quick and has a higher-level API for common prompt patterns.

**Usage**:

```ts
import inquirer from 'inquirer';
const answer = await inquirer.prompt<{continue: boolean}>([
  {
    type: 'confirm',
    name: 'continue',
    message: 'Proceed with deletion?',
    default: false
  }
]);
if (!answer.continue) this.log('Operation cancelled by user');
```

- Always define `name` for each prompt question; use TypeScript generics or casting to get a typed result object.
- For lists, you can supply `choices` as an array of strings or `{ name, value }` objects where `name` is shown and `value` is returned.

**WARNING**: Inquirer and Ink can conflict if both listening to `stdin` at the same time. Typically, run Inquirer prompts outside of any Ink rendering or pause Ink, because both manage input. Usually, we don't use them simultaneously; design flow such that you either go with an Ink input component or an Inquirer prompt.

## Ora – Spinners

**Ora** provides a convenient CLI spinner:

- Simple API: `const spinner = ora('Loading data').start();` then later `spinner.succeed('Done');` or `spinner.fail('Failed');`.
- Start spinner before an async task, and ensure to `.stop()` or end it in a `.finally` or after the task.
- Use `spinner.succeed(...)` to output a green check and message, or `spinner.warn(...)` etc., depending on outcome.
- If logging while spinner is active, Ora will handle redrawing. But be careful mixing with other console output; sometimes stop spinner, print logs, then restart if needed.

In effect-based code, you can integrate by starting spinner, then performing an `Effect.runPromise` for the long task, then stopping spinner. Or wrap in an Effect that yields updates (but simpler to use imperative spinner in this case).

## cli-progress – Progress Bars

For tasks where we know the total work (like downloading X bytes, processing N items), **cli-progress** provides progress bars:
We prefer `cli-progress` when feedback needs to be more granular than a spinner. E.g., “Uploading 100 files – show progress 0 to 100”.

**Usage Example**:

```ts
import { SingleBar, Presets } from 'cli-progress';
const bar = new SingleBar({ clearOnComplete: true }, Presets.shades_classic);
bar.start(totalFiles, 0);
for(const file of files) {
  await uploadFile(file);
  bar.increment();
}
bar.stop();
```

This will display something like `[=====    ] 50% | 50/100 files`.

### Integration considerations:

- Ensure to stop the bar (`.stop()`) or complete it, otherwise the terminal may not reset correctly.
- Use `clearOnComplete` to remove the bar after finishing (if desired).
- For multi-progress (e.g., multiple concurrent tasks), `cli-progress` has a `MultiBar` class. We typically use single, but multi can be used for parallel downloads etc., if needed.
- Progress bars plus our logging: if using structured logging while a bar is active, it can mess up the console output. Usually, during a progress bar, avoid normal log outputs. Or write logs to a file instead. Once bar is done, you can print summary logs.
