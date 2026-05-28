#!/usr/bin/env -S node --stack-size=8192

/**
 * Copyright (c) 2025 Elara AI Pty Ltd
 * Licensed under BSL 1.1. See LICENSE for details.
 */

/**
 * e3 CLI - East Execution Engine command-line interface
 *
 * All commands take a repository path as the first argument (`.` for current directory).
 */

import { createRequire } from 'node:module';
import { Command } from 'commander';

const require = createRequire(import.meta.url);
const packageJson = require('../../package.json') as { version: string };
import { repoCommand } from './commands/repo.js';
import { packageCommand } from './commands/package.js';
import { workspaceCommand } from './commands/workspace.js';
import { listCommand } from './commands/list.js';
import { treeCommand } from './commands/tree.js';
import { getCommand } from './commands/get.js';
import { setCommand } from './commands/set.js';
import { startCommand } from './commands/start.js';
import { runCommand } from './commands/run.js';
import { logsCommand } from './commands/logs.js';
import { convertCommand } from './commands/convert.js';
import { watchCommand } from './commands/watch.js';
import { createAuthCommand, createLoginCommand, createLogoutCommand } from './commands/auth.js';

const program = new Command();

program
  .name('e3')
  .description('East Execution Engine - Execute tasks across multiple runtimes')
  .version(packageJson.version);

// Repository commands
program
  .command('repo')
  .description('Repository operations')
  .addCommand(
    new Command('create')
      .description('Create a new repository')
      .argument('<repo>', 'Repository path or URL')
      .action(repoCommand.create)
  )
  .addCommand(
    new Command('remove')
      .description('Remove a repository')
      .argument('<repo>', 'Repository path or URL')
      .action(repoCommand.remove)
  )
  .addCommand(
    new Command('status')
      .description('Show repository status')
      .argument('<repo>', 'Repository path or URL')
      .action(repoCommand.status)
  )
  .addCommand(
    new Command('gc')
      .description('Remove unreferenced objects')
      .argument('<repo>', 'Repository path or URL')
      .option('--dry-run', 'Report what would be deleted without deleting')
      .option('--min-age <ms>', 'Minimum file age in ms before deletion', '60000')
      .action(repoCommand.gc)
  )
  .addCommand(
    new Command('list')
      .description('List repositories on a server')
      .argument('<server>', 'Server URL (e.g., http://localhost:3000)')
      .action(repoCommand.list)
  );

// Package commands
program
  .command('package')
  .description('Package operations')
  .addCommand(
    new Command('import')
      .description('Import package from .zip file')
      .argument('<repo>', 'Repository path')
      .argument('<zipPath>', 'Path to .zip file')
      .action(packageCommand.import)
  )
  .addCommand(
    new Command('export')
      .description('Export package to .zip file')
      .argument('<repo>', 'Repository path')
      .argument('<pkg>', 'Package name[@version]')
      .argument('<zipPath>', 'Output .zip path')
      .action(packageCommand.export)
  )
  .addCommand(
    new Command('list')
      .description('List installed packages')
      .argument('<repo>', 'Repository path')
      .action(packageCommand.list)
  )
  .addCommand(
    new Command('remove')
      .description('Remove a package')
      .argument('<repo>', 'Repository path')
      .argument('<pkg>', 'Package name[@version]')
      .action(packageCommand.remove)
  );

// Workspace commands
program
  .command('workspace')
  .description('Workspace operations')
  .addCommand(
    new Command('create')
      .description('Create an empty workspace')
      .argument('<repo>', 'Repository path')
      .argument('<name>', 'Workspace name')
      .action(workspaceCommand.create)
  )
  .addCommand(
    new Command('deploy')
      .description('Deploy a package to a workspace')
      .argument('<repo>', 'Repository path')
      .argument('<ws>', 'Workspace name')
      .argument('<pkg>', 'Package name[@version]')
      .action(workspaceCommand.deploy)
  )
  .addCommand(
    new Command('export')
      .description('Export workspace as a package')
      .argument('<repo>', 'Repository path')
      .argument('<ws>', 'Workspace name')
      .argument('<zipPath>', 'Output .zip path')
      .option('--name <name>', 'Package name (default: deployed package name)')
      .option('--version <version>', 'Package version (default: auto-generated)')
      .action(workspaceCommand.export)
  )
  .addCommand(
    new Command('list')
      .description('List workspaces')
      .argument('<repo>', 'Repository path')
      .action(workspaceCommand.list)
  )
  .addCommand(
    new Command('remove')
      .description('Remove a workspace')
      .argument('<repo>', 'Repository path')
      .argument('<ws>', 'Workspace name')
      .action(workspaceCommand.remove)
  )
  .addCommand(
    new Command('status')
      .description('Show detailed workspace status (tasks, datasets, locks)')
      .argument('<repo>', 'Repository path')
      .argument('<ws>', 'Workspace name')
      .action(workspaceCommand.status)
  );

// Dataset commands
program
  .command('list <repo> [path]')
  .description('List workspaces or tree contents at path (ws.path.to.tree)')
  .action(listCommand);

program
  .command('tree <repo> <path>')
  .description('Show full tree structure at path (ws or ws.subtree)')
  .option('--depth <n>', 'Maximum depth to display')
  .option('--types', 'Show dataset types')
  .action(treeCommand);

program
  .command('get <repo> <path>')
  .description('Get dataset value at path (ws.path.to.dataset)')
  .option('-f, --format <format>', 'Output format: east, json, beast2', 'east')
  .action(getCommand);

program
  .command('set <repo> <path> <file>')
  .description('Set dataset value from file (ws.path.to.dataset)')
  .option('--type <typespec>', 'Type specification in .east format (required for .json/.csv files)')
  .action(setCommand);

// Execution commands
program
  .command('run <repo> <task> [inputs...]')
  .description('Run task ad-hoc (task format: pkg/task or pkg@version/task)')
  .option('-o, --output <path>', 'Output file path')
  .option('--force', 'Force re-execution even if cached')
  .action(runCommand);

program
  .command('start <repo> <ws>')
  .description('Execute tasks in a workspace')
  .option('--filter <pattern>', 'Only run tasks matching pattern')
  .option('--concurrency <n>', 'Max concurrent tasks', '4')
  .option('--force', 'Force re-execution even if cached')
  .action(startCommand);

program
  .command('watch <repo> <workspace> <source>')
  .description('Watch a TypeScript file and auto-deploy on changes')
  .option('--start', 'Execute dataflow after each deploy')
  .option('--concurrency <n>', 'Max concurrent tasks when using --start', '4')
  .option('--abort-on-change', 'Abort running execution when file changes')
  .action(watchCommand);

program
  .command('logs <repo> <path>')
  .description('View task logs (path format: ws or ws.taskName)')
  .option('--follow', 'Follow log output')
  .action(logsCommand);

// Utility commands
program
  .command('convert [input]')
  .description('Convert between .east, .json, and .beast2 formats')
  .option('--from <format>', 'Input format: east, json, beast2 (default: auto-detect)')
  .option('--to <format>', 'Output format: east, json, beast2', 'east')
  .option('-o, --output <path>', 'Output file path (default: stdout)')
  .option('--type <typespec>', 'Type specification in .east format')
  .action(convertCommand);

// Authentication commands
program.addCommand(createLoginCommand());
program.addCommand(createLogoutCommand());
program.addCommand(createAuthCommand());

program.parse();
