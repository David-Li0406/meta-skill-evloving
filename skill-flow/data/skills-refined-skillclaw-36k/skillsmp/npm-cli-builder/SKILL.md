---
name: npm-cli-builder
description: Skill for building npm CLI tools. Use when creating command-line tools with Node.js, npm packaging, argument parsing with commander or yargs, and npm publish workflows.
---

# NPM CLI Builder Skill

This skill provides guidance for building npm CLI tools with proper structure, argument parsing, and npm publishing.

## CLI Project Structure

```
<cli-name>/
├── package.json
├── bin/
│   └── <cli-name>.js       # Entry point with shebang
├── src/
│   ├── index.js            # Main exports
│   ├── commands/           # Command implementations
│   │   ├── install.js
│   │   ├── list.js
│   │   └── validate.js
│   ├── lib/                # Core logic
│   │   ├── registry.js
│   │   ├── installer.js
│   │   └── validator.js
│   └── utils/              # Utilities
│       ├── logger.js
│       └── config.js
├── README.md
└── LICENSE
```

## Package.json Configuration

```json
{
  "name": "<cli-name>",
  "version": "1.0.0",
  "description": "CLI tool description",
  "type": "module",
  "bin": {
    "<cli-name>": "./bin/<cli-name>.js"
  },
  "main": "./src/index.js",
  "engines": {
    "node": ">=18.0.0"
  },
  "files": [
    "bin",
    "src"
  ],
  "scripts": {
    "start": "node bin/<cli-name>.js",
    "lint": "eslint .",
    "test": "node --test"
  },
  "keywords": ["cli", "tool"],
  "license": "MIT",
  "dependencies": {
    "commander": "^12.0.0",
    "chalk": "^5.3.0",
    "ora": "^8.0.0"
  }
}
```

## CLI Entry Point Template

`bin/<cli-name>.js`:
```javascript
#!/usr/bin/env node

import { program } from 'commander';
import { installCommand } from '../src/commands/install.js';
import { listCommand } from '../src/commands/list.js';
import { validateCommand } from '../src/commands/validate.js';

program
  .name('<cli-name>')
  .description('CLI tool description')
  .version('1.0.0');

program
  .command('install')
  .description('Install skills from a repository')
  .argument('<repo>', 'GitHub repository (owner/repo)')
  .option('-s, --skill <name>', 'Install specific skill')
  .option('-a, --all', 'Install all skills')
  .action(installCommand);

program
  .command('list')
  .description('List installed skills')
  .option('-j, --json', 'Output as JSON')
  .action(listCommand);

program
  .command('validate')
  .description('Validate installed skills')
  .argument('[skill]', 'Specific skill to validate')
  .action(validateCommand);

program.parse();
```

## Command Pattern

`src/commands/install.js`:
```javascript
import { Installer } from '../lib/installer.js';
import { Registry } from '../lib/registry.js';
import ora from 'ora';
import chalk from 'chalk';

export async function installCommand(repo, options) {
  const spinner = ora('Installing skills...').start();
  
  try {
    const installer = new Installer();
    const registry = new Registry();
    
    if (options.all) {
      const skills = await installer.installAll(repo);
      for (const skill of skills) {
        await registry.add(skill);
      }
      spinner.succeed(`Installed ${skills.length} skills`);
    } else if (options.skill) {
      const skill = await installer.install(repo, options.skill);
      await registry.add(skill);
      spinner.succeed(`Installed ${skill.name}`);
    } else {
      spinner.fail('Specify --all or --skill <name>');
      process.exit(1);
    }
  } catch (error) {
    spinner.fail(chalk.red(error.message));
    process.exit(1);
  }
}
```

## Best Practices

1. **Use ESM modules** - Modern Node.js with `"type": "module"`
2. **Proper error handling** - Catch errors, display helpful messages
3. **Progress indicators** - Use ora for spinners
4. **Colored output** - Use chalk for styling
5. **Exit codes** - Return proper exit codes (0 success, 1+ failure)
6. **Help text** - Comprehensive --help output
7. **Validation** - Validate inputs before processing

## Publishing Checklist

1. Update version in package.json
2. Run tests: `npm test`
3. Login: `npm login`
4. Publish: `npm publish`
5. Test global install: `npm install -g <cli-name>`
