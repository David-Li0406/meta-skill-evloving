import { Command } from 'commander';
import ora from 'ora';
import chalk from 'chalk';
import Table from 'cli-table3';
import { getClient } from '../api/client.js';
import { error, info } from '../utils/index.js';

export function createWorkspacesCommand(): Command {
  const workspaces = new Command('workspaces').description('Manage workspaces');

  workspaces
    .command('list')
    .description('List all accessible workspaces')
    .option('--json', 'Output as JSON')
    .action(async (options) => {
      const spinner = ora('Fetching workspaces...').start();

      try {
        const client = getClient();
        const workspacesList = await client.getWorkspaces();

        spinner.stop();

        if (options.json) {
          console.log(JSON.stringify(workspacesList, null, 2));
        } else {
          console.log('Workspaces:\n');
          for (const ws of workspacesList) {
            console.log(`  ${chalk.bold(ws.name)}`);
            console.log(`    ID: ${ws.id}`);
            console.log(`    Members: ${ws.members.length}`);
            console.log('');
          }
        }
      } catch (err) {
        spinner.fail('Failed to fetch workspaces');
        error(err instanceof Error ? err.message : String(err));
      }
    });

  return workspaces;
}

export function createSpacesCommand(): Command {
  const spaces = new Command('spaces').description('Manage spaces');

  spaces
    .command('list')
    .description('List all spaces in the workspace')
    .option('--json', 'Output as JSON')
    .action(async (options) => {
      const spinner = ora('Fetching spaces...').start();

      try {
        const client = getClient();
        const config = (client as unknown as { config: { workspaceId: string } }).config;
        const spacesList = await client.getSpaces(config.workspaceId);

        spinner.stop();

        if (options.json) {
          console.log(JSON.stringify(spacesList, null, 2));
        } else {
          console.log('Spaces:\n');
          for (const space of spacesList) {
            console.log(`  ${chalk.bold(space.name)}`);
            console.log(`    ID: ${space.id}`);
            console.log(`    Private: ${space.private ? 'Yes' : 'No'}`);
            console.log('');
          }
        }
      } catch (err) {
        spinner.fail('Failed to fetch spaces');
        error(err instanceof Error ? err.message : String(err));
      }
    });

  return spaces;
}

export function createMembersCommand(): Command {
  const members = new Command('members').description('Manage workspace members');

  members
    .command('list')
    .description('List all members in the workspace')
    .option('-t, --table', 'Output as table')
    .option('--json', 'Output as JSON')
    .action(async (options) => {
      const spinner = ora('Fetching members...').start();

      try {
        const client = getClient();
        const membersList = await client.getWorkspaceMembers();

        spinner.stop();

        if (options.json) {
          console.log(JSON.stringify(membersList, null, 2));
        } else if (options.table) {
          const table = new Table({
            head: [
              chalk.bold('ID'),
              chalk.bold('Username'),
              chalk.bold('Email'),
            ],
            colWidths: [12, 25, 35],
          });

          for (const member of membersList) {
            table.push([
              member.user.id.toString(),
              member.user.username,
              member.user.email,
            ]);
          }

          console.log(table.toString());
        } else {
          console.log('Members:\n');
          for (const member of membersList) {
            console.log(`  ${chalk.bold(member.user.username)}`);
            console.log(`    ID: ${member.user.id}`);
            console.log(`    Email: ${member.user.email}`);
            console.log('');
          }
        }
      } catch (err) {
        spinner.fail('Failed to fetch members');
        error(err instanceof Error ? err.message : String(err));
      }
    });

  members
    .command('find <nameOrEmail>')
    .description('Find a member by name or email')
    .option('--json', 'Output as JSON')
    .action(async (nameOrEmail: string, options) => {
      const spinner = ora('Searching...').start();

      try {
        const client = getClient();
        const member = await client.findMember(nameOrEmail);

        spinner.stop();

        if (!member) {
          info(`No member found matching "${nameOrEmail}"`);
          return;
        }

        if (options.json) {
          console.log(JSON.stringify(member, null, 2));
        } else {
          console.log(`Found member:\n`);
          console.log(`  ${chalk.bold(member.user.username)}`);
          console.log(`    ID: ${member.user.id}`);
          console.log(`    Email: ${member.user.email}`);
        }
      } catch (err) {
        spinner.fail('Failed to find member');
        error(err instanceof Error ? err.message : String(err));
      }
    });

  return members;
}

export function createConfigCommand(): Command {
  const config = new Command('config').description('Show configuration');

  config
    .command('show')
    .description('Show current configuration')
    .action(() => {
      const apiToken = process.env.CLICKUP_API_TOKEN;
      const workspaceId = process.env.CLICKUP_WORKSPACE_ID;
      const teamId = process.env.CLICKUP_TEAM_ID;
      const userId = process.env.CLICKUP_USER_ID;

      console.log('Current Configuration:\n');
      console.log(`  API Token: ${apiToken ? chalk.green('Set') + ` (${apiToken.substring(0, 8)}...)` : chalk.red('Not set')}`);
      console.log(`  Workspace ID: ${workspaceId || chalk.red('Not set')}`);
      console.log(`  Team ID: ${teamId || chalk.dim('Not set (using workspace ID)')}`);
      console.log(`  User ID: ${userId || chalk.dim('Not set')}`);
      console.log('');
      console.log(chalk.dim('Set these in .env or as environment variables.'));
    });

  return config;
}

export function createListsCommand(): Command {
  const lists = new Command('lists').description('Manage lists');

  lists
    .command('find <name>')
    .description('Find a list by name')
    .option('--json', 'Output as JSON')
    .action(async (name: string, options) => {
      const spinner = ora('Searching for list...').start();

      try {
        const client = getClient();
        const list = await client.findListByName(name);

        spinner.stop();

        if (!list) {
          info(`No list found matching "${name}"`);
          return;
        }

        if (options.json) {
          console.log(JSON.stringify(list, null, 2));
        } else {
          console.log(`Found list:\n`);
          console.log(`  ${chalk.bold(list.name)}`);
          console.log(`    ID: ${list.id}`);
          if (list.folder) {
            console.log(`    Folder: ${list.folder.name}`);
          }
        }
      } catch (err) {
        spinner.fail('Failed to find list');
        error(err instanceof Error ? err.message : String(err));
      }
    });

  return lists;
}
