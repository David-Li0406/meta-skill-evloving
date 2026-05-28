import { Command } from 'commander';
import ora from 'ora';
import { getClient } from '../api/client.js';
import {
  formatTask,
  formatTasksTable,
  formatComments,
  success,
  error,
  info,
  parseDuration,
} from '../utils/index.js';
import { parseDate } from '../utils/dates.js';
import type { Task } from '../types/clickup.js';

export function createTasksCommand(): Command {
  const tasks = new Command('tasks').description('Manage ClickUp tasks');

  // Search tasks
  tasks
    .command('search [query]')
    .description('Search for tasks')
    .option('-s, --status <status>', 'Filter by status')
    .option('-a, --assignee <assignee>', 'Filter by assignee (use "me" for yourself)')
    .option('-l, --list <list>', 'Filter by list name')
    .option('--space <space>', 'Filter by space ID')
    .option('--include-subtasks', 'Include subtasks in results')
    .option('--include-closed', 'Include closed tasks')
    .option('-t, --table', 'Output as table')
    .option('--json', 'Output as JSON')
    .option('-p, --page <number>', 'Page number', '0')
    .action(async (query: string | undefined, options) => {
      const spinner = ora('Searching tasks...').start();

      try {
        const client = getClient();
        const config = (client as unknown as { config: { workspaceId: string; userId?: string } }).config;

        // Resolve assignee
        let assigneeIds: string[] | undefined;
        if (options.assignee) {
          if (options.assignee.toLowerCase() === 'me' && config.userId) {
            assigneeIds = [config.userId];
          } else {
            const member = await client.findMember(options.assignee);
            if (member) {
              assigneeIds = [member.user.id.toString()];
            }
          }
        }

        // Resolve list
        let listIds: string[] | undefined;
        if (options.list) {
          const list = await client.findListByName(options.list);
          if (list) {
            listIds = [list.id];
          } else {
            spinner.fail(`List "${options.list}" not found`);
            return;
          }
        }

        const tasks = await client.searchTasks(config.workspaceId, query || '', {
          statuses: options.status ? [options.status] : undefined,
          assignees: assigneeIds,
          listIds,
          spaceIds: options.space ? [options.space] : undefined,
          includeSubtasks: options.includeSubtasks,
          includeClosed: options.includeClosed,
          page: parseInt(options.page, 10),
        });

        spinner.stop();

        if (tasks.length === 0) {
          info('No tasks found matching your criteria.');
          return;
        }

        if (options.json) {
          console.log(JSON.stringify(tasks, null, 2));
        } else if (options.table) {
          console.log(formatTasksTable(tasks));
        } else {
          console.log(`Found ${tasks.length} task(s):\n`);
          for (const task of tasks) {
            console.log(formatTask(task));
            console.log('');
          }
        }
      } catch (err) {
        spinner.fail('Failed to search tasks');
        error(err instanceof Error ? err.message : String(err));
      }
    });

  // Get task details
  tasks
    .command('get <taskId>')
    .description('Get task details by ID or custom ID (e.g., TCG-1234)')
    .option('-c, --comments', 'Include comments')
    .option('-s, --subtasks', 'Include subtasks')
    .option('-f, --full', 'Include everything (comments, subtasks, attachments)')
    .option('-v, --verbose', 'Show full description')
    .option('--json', 'Output as JSON')
    .action(async (taskId: string, options) => {
      const spinner = ora('Fetching task...').start();

      try {
        const client = getClient();

        // Resolve task ID (handles custom IDs like TCG-1234)
        const resolvedId = await client.resolveTaskId(taskId);
        const task = await client.getTask(
          resolvedId,
          options.subtasks || options.full
        );

        let comments: Awaited<ReturnType<typeof client.getTaskComments>> | undefined;
        if (options.comments || options.full) {
          comments = await client.getTaskComments(resolvedId);
        }

        spinner.stop();

        if (options.json) {
          console.log(JSON.stringify({ task, comments }, null, 2));
        } else {
          console.log(formatTask(task, { verbose: options.verbose || options.full }));

          if (task.subtasks && task.subtasks.length > 0) {
            console.log('\n' + '─'.repeat(50));
            console.log(`Subtasks (${task.subtasks.length}):`);
            for (const subtask of task.subtasks) {
              const id = subtask.custom_id || subtask.id;
              const status = subtask.status.status;
              console.log(`  • ${id}: ${subtask.name} [${status}]`);
            }
          }

          if (comments && comments.length > 0) {
            console.log('\n' + '─'.repeat(50));
            console.log(`Comments (${comments.length}):\n`);
            console.log(formatComments(comments));
          }
        }
      } catch (err) {
        spinner.fail('Failed to fetch task');
        error(err instanceof Error ? err.message : String(err));
      }
    });

  // Create task
  tasks
    .command('create <name>')
    .description('Create a new task')
    .requiredOption('-l, --list <list>', 'List name or ID (required)')
    .option('-d, --description <desc>', 'Task description')
    .option('-s, --status <status>', 'Task status')
    .option('-p, --priority <priority>', 'Priority: urgent, high, normal, low')
    .option('-a, --assignee <assignee>', 'Assignee (use "me" for yourself)')
    .option('--due <date>', 'Due date (YYYY-MM-DD)')
    .option('--start <date>', 'Start date (YYYY-MM-DD)')
    .option('--estimate <duration>', 'Time estimate (e.g., "4h", "2h 30m")')
    .option('--parent <taskId>', 'Parent task ID for subtasks')
    .option('--json', 'Output as JSON')
    .action(async (name: string, options) => {
      const spinner = ora('Creating task...').start();

      try {
        const client = getClient();
        const config = (client as unknown as { config: { workspaceId: string; userId?: string } }).config;

        // Resolve list
        let listId = options.list;
        if (!/^\d+$/.test(listId)) {
          const list = await client.findListByName(options.list);
          if (!list) {
            spinner.fail(`List "${options.list}" not found`);
            return;
          }
          listId = list.id;
        }

        // Resolve assignee
        let assigneeIds: number[] | undefined;
        if (options.assignee) {
          if (options.assignee.toLowerCase() === 'me' && config.userId) {
            assigneeIds = [parseInt(config.userId, 10)];
          } else {
            const member = await client.findMember(options.assignee);
            if (member) {
              assigneeIds = [member.user.id];
            }
          }
        }

        // Map priority string to number
        const priorityMap: Record<string, number> = {
          urgent: 1,
          high: 2,
          normal: 3,
          low: 4,
        };

        const task = await client.createTask(listId, {
          name,
          description: options.description,
          status: options.status,
          priority: options.priority ? priorityMap[options.priority.toLowerCase()] : undefined,
          assignees: assigneeIds,
          due_date: options.due ? parseDate(options.due).getTime() : undefined,
          start_date: options.start ? parseDate(options.start).getTime() : undefined,
          time_estimate: options.estimate ? parseDuration(options.estimate) : undefined,
          parent: options.parent,
        });

        spinner.stop();

        if (options.json) {
          console.log(JSON.stringify(task, null, 2));
        } else {
          success(`Task created: ${task.custom_id || task.id}`);
          console.log(formatTask(task));
        }
      } catch (err) {
        spinner.fail('Failed to create task');
        error(err instanceof Error ? err.message : String(err));
      }
    });

  // Update task
  tasks
    .command('update <taskId>')
    .description('Update a task')
    .option('-n, --name <name>', 'New task name')
    .option('-d, --description <desc>', 'New description')
    .option('-s, --status <status>', 'New status')
    .option('-p, --priority <priority>', 'Priority: urgent, high, normal, low, or "null" to clear')
    .option('--due <date>', 'Due date (YYYY-MM-DD or "null" to clear)')
    .option('--start <date>', 'Start date (YYYY-MM-DD or "null" to clear)')
    .option('--estimate <duration>', 'Time estimate (e.g., "4h" or "null" to clear)')
    .option('--json', 'Output as JSON')
    .action(async (taskId: string, options) => {
      const spinner = ora('Updating task...').start();

      try {
        const client = getClient();

        // Resolve task ID
        const resolvedId = await client.resolveTaskId(taskId);

        // Map priority string to number
        const priorityMap: Record<string, number> = {
          urgent: 1,
          high: 2,
          normal: 3,
          low: 4,
        };

        // Build update payload
        const updateData: Parameters<typeof client.updateTask>[1] = {};

        if (options.name) updateData.name = options.name;
        if (options.description) updateData.description = options.description;
        if (options.status) updateData.status = options.status;

        if (options.priority) {
          updateData.priority =
            options.priority.toLowerCase() === 'null'
              ? null
              : priorityMap[options.priority.toLowerCase()];
        }

        if (options.due) {
          updateData.due_date =
            options.due.toLowerCase() === 'null'
              ? null
              : parseDate(options.due).getTime();
        }

        if (options.start) {
          updateData.start_date =
            options.start.toLowerCase() === 'null'
              ? null
              : parseDate(options.start).getTime();
        }

        if (options.estimate) {
          updateData.time_estimate =
            options.estimate.toLowerCase() === 'null'
              ? null
              : parseDuration(options.estimate);
        }

        const task = await client.updateTask(resolvedId, updateData);

        spinner.stop();

        if (options.json) {
          console.log(JSON.stringify(task, null, 2));
        } else {
          success(`Task updated: ${task.custom_id || task.id}`);
          console.log(formatTask(task));
        }
      } catch (err) {
        spinner.fail('Failed to update task');
        error(err instanceof Error ? err.message : String(err));
      }
    });

  // Delete task
  tasks
    .command('delete <taskId>')
    .description('Delete a task')
    .option('-f, --force', 'Skip confirmation')
    .action(async (taskId: string, options) => {
      try {
        const client = getClient();

        // Resolve task ID
        const resolvedId = await client.resolveTaskId(taskId);

        if (!options.force) {
          // Get task info for confirmation
          const task = await client.getTask(resolvedId);
          console.log(`About to delete: ${task.custom_id || task.id} - ${task.name}`);
          console.log('Use --force to skip this confirmation.');
          return;
        }

        const spinner = ora('Deleting task...').start();
        await client.deleteTask(resolvedId);
        spinner.stop();

        success(`Task ${taskId} deleted`);
      } catch (err) {
        error(err instanceof Error ? err.message : String(err));
      }
    });

  return tasks;
}
