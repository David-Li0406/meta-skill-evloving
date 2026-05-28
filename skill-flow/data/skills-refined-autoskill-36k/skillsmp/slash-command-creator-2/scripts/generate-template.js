#!/usr/bin/env node

/**
 * Generate command templates for specific patterns
 * Usage: node generate-template.js <pattern> [command-name]
 * Patterns: simple, args, bash, files
 */

const templates = {
  simple: (name) => `---
description: Brief description of what ${name} does
---

# ${name}

Write your command instructions here.
This is a simple command with no arguments.
`,

  args: (name) => `---
description: Process input with ${name} command
argument-hint: [input-text]
allowed-tools: Read, Write
---

# ${name}

Processing input: $ARGUMENTS

## Task

Execute the following task based on the provided input.
`,

  positional: (name) => `---
description: ${name} with specific parameters
argument-hint: [param1] [param2] [optional-param3]
allowed-tools: Read, Write
---

# ${name}

Parameters:
- First parameter: $1
- Second parameter: $2
- Third parameter: $3

## Task

Execute using the provided parameters.
`,

  bash: (name) => `---
description: ${name} with shell command execution
allowed-tools: Bash(git:*), Bash(npm:*)
---

# ${name}

## Context

- Current directory: !\`pwd\`
- Git status: !\`git status\`
- Git branch: !\`git branch --show-current\`

## Task

Execute the command based on the above context.
`,

  files: (name) => `---
description: ${name} that references project files
allowed-tools: Read, Write, Glob
---

# ${name}

## Analysis

Analyze the implementation in @src/components/
Check the configuration in @package.json

## Task

Process the referenced files and execute the task.
`,
};

function generateTemplate(pattern, commandName) {
  const template = templates[pattern];

  if (!template) {
    console.error(
      "❌ Unknown pattern. Available patterns:",
      Object.keys(templates).join(", "),
    );
    process.exit(1);
  }

  const output = template(commandName || "command");

  if (commandName) {
    const fileName = `${commandName}.md`;
    require("fs").writeFileSync(fileName, output);
    console.log(`✅ Generated ${fileName}`);
  } else {
    console.log(output);
  }
}

const pattern = process.argv[2];
const commandName = process.argv[3];

if (!pattern) {
  console.error("Usage: node generate-template.js <pattern> [command-name]");
  console.error("Patterns:", Object.keys(templates).join(", "));
  process.exit(1);
}

generateTemplate(pattern, commandName);
