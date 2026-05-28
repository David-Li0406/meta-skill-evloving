#!/usr/bin/env node

import { Command } from 'commander';
import { config as dotenvConfig } from 'dotenv';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import chalk from 'chalk';

import { initClient } from './api/client.js';
import {
  createTasksCommand,
  createTimeCommand,
  createWorkspacesCommand,
  createSpacesCommand,
  createMembersCommand,
  createConfigCommand,
  createListsCommand,
} from './commands/index.js';

// Get the directory of this file for loading .env
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load environment variables from .env file
dotenvConfig({ path: resolve(__dirname, '../.env') });

// Also try loading from current working directory
dotenvConfig();

const program = new Command();

program
  .name('clickup')
  .description('ClickUp CLI - Manage tasks and time entries')
  .version('1.0.0')
  .hook('preAction', () => {
    // Validate configuration before running commands
    const apiToken = process.env.CLICKUP_API_TOKEN;
    const workspaceId = process.env.CLICKUP_WORKSPACE_ID;

    // Skip validation for config command
    const args = process.argv.slice(2);
    if (args[0] === 'config') {
      return;
    }

    if (!apiToken) {
      console.error(chalk.red('Error: CLICKUP_API_TOKEN is not set.'));
      console.error('Set it in .env or as an environment variable.');
      console.error('Get your token from: ClickUp Settings → Apps → API Token');
      process.exit(1);
    }

    if (!workspaceId) {
      console.error(chalk.red('Error: CLICKUP_WORKSPACE_ID is not set.'));
      console.error('Set it in .env or as an environment variable.');
      console.error('Find your workspace ID in the ClickUp URL: app.clickup.com/WORKSPACE_ID/home');
      process.exit(1);
    }

    // Initialize the client
    initClient({
      apiToken,
      workspaceId,
      teamId: process.env.CLICKUP_TEAM_ID,
      userId: process.env.CLICKUP_USER_ID,
    });
  });

// Add subcommands
program.addCommand(createTasksCommand());
program.addCommand(createTimeCommand());
program.addCommand(createWorkspacesCommand());
program.addCommand(createSpacesCommand());
program.addCommand(createMembersCommand());
program.addCommand(createListsCommand());
program.addCommand(createConfigCommand());

// Parse arguments
program.parse();
