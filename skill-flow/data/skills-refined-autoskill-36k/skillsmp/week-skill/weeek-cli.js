#!/usr/bin/env node
import fs from 'fs/promises';
import { resolve } from 'path';
import chalk from 'chalk';
import { Command } from 'commander';
import dotenv from 'dotenv';
import { WeeekClient } from './weeek-api.js';

dotenv.config();

const SPEC_PATH = resolve(process.cwd(), 'weeek_spec.json');
const program = new Command();
const client = new WeeekClient();

// --- Helpers ---

async function loadSpec() {
    try {
        const data = await fs.readFile(SPEC_PATH, 'utf8');
        return JSON.parse(data);
    } catch (err) {
        console.error(chalk.red(`Error: Could not read ${SPEC_PATH}`));
        process.exit(1);
    }
}

function getTags(spec) {
    const tags = spec.tags || [];
    const pathTags = new Set();
    if (spec.paths) {
        Object.values(spec.paths).forEach(pathItem => {
            Object.values(pathItem).forEach(operation => {
                if (operation && operation.tags) {
                    operation.tags.forEach(t => pathTags.add(t));
                }
            });
        });
    }
    return [...new Set([...tags.map(t => t.name || t), ...pathTags])].sort();
}

// --- CLI Config ---

program
    .name('weeek-cli')
    .description('CLI tool to explore and interact with WEEEK API')
    .version('3.3.0');

// --- Standard Commands ---

program
    .command('tags')
    .description('List all available tags from spec')
    .action(async () => {
        const spec = await loadSpec();
        const tags = getTags(spec);
        console.log(chalk.bold.blue('\nAvailable Tags:'));
        tags.forEach(t => console.log(`- ${t}`));
    });

program
    .command('endpoints')
    .description('List endpoints filtered by tag')
    .argument('<tag>', 'Tag to filter by')
    .action(async (tag) => {
        const spec = await loadSpec();
        const endpoints = [];
        for (const [path, pathItem] of Object.entries(spec.paths)) {
            for (const [method, operation] of Object.entries(pathItem)) {
                if (operation && operation.tags && operation.tags.includes(tag)) {
                    endpoints.push({ path, method, summary: operation.summary || 'No summary' });
                }
            }
        }
        if (endpoints.length === 0) {
            console.log(chalk.yellow(`No endpoints found for tag: ${tag}`));
            return;
        }
        console.log(chalk.bold.blue(`\nEndpoints for tag "${tag}":`));
        endpoints.forEach(e => {
            console.log(`${chalk.bold.green(e.method.toUpperCase().padEnd(7))} ${chalk.cyan(e.path.padEnd(35))} ${chalk.dim(e.summary)}`);
        });
    });

program
    .command('describe')
    .description('Get full description of an endpoint')
    .argument('<method>', 'HTTP method')
    .argument('<path>', 'Endpoint path')
    .action(async (method, path) => {
        const spec = await loadSpec();
        const normalizedPath = path.startsWith('/') ? path : `/${path}`;
        const pathItem = spec.paths[normalizedPath];
        if (!pathItem) {
            console.log(chalk.red(`Path not found: ${normalizedPath}`));
            return;
        }
        const operation = pathItem[method.toLowerCase()];
        if (!operation) {
            console.log(chalk.red(`Method ${method.toUpperCase()} not found for path: ${normalizedPath}`));
            return;
        }
        console.log('\n' + chalk.bold.bgWhite.black(` DETAILS: ${method.toUpperCase()} ${normalizedPath} `));
        console.log(chalk.bold.blue('\nSummary:   ') + (operation.summary || chalk.dim('N/A')));
        console.log(chalk.bold.blue('Description: ') + (operation.description || chalk.dim('N/A')));
    });

program
    .command('run')
    .description('Execute a raw API request')
    .argument('<method>', 'HTTP method')
    .argument('<path>', 'Endpoint path')
    .option('-d, --data <json>', 'JSON data for request body')
    .option('-p, --params <query>', 'Query parameters (e.g. "foo=bar")')
    .action(async (method, path, options) => {
        let params = null;
        if (options.params) {
            params = Object.fromEntries(new URLSearchParams(options.params));
        }
        let body = null;
        if (options.data) {
            try { body = JSON.parse(options.data); } catch { body = options.data; }
        }
        try {
            console.log(chalk.dim(`Executing ${method} ${path}...`));
            const result = await client.request(method, path, body, params);
            console.log(chalk.bold('\nResponse:'));
            console.log(typeof result === 'object' ? JSON.stringify(result, null, 2) : result);
        } catch (err) {
            console.error(chalk.red('\nRequest Failed:'), err.message);
        }
    });

// --- High-Level Usability Commands ---

program
    .command('board')
    .description('View board columns and tasks')
    .argument('<name>', 'Board name (partial match allowed)')
    .action(async (name) => {
        try {
            console.log(chalk.dim(`Fetching board "${name}"...`));
            const board = await client.getBoardWithContext(name);

            console.log(chalk.bold.green(`\nBoard: ${board.name} (ID: ${board.id})`));
            console.log(chalk.dim(`Project: ${board.projectName || 'N/A'}`));

            console.log(chalk.bold.blue(`\nColumns & Tasks:`));
            board.columns.forEach(col => {
                const colTasks = board.tasks.filter(t => t.boardColumnId === col.id);
                console.log(chalk.bold.magenta(`\n[${col.name.toUpperCase()}] (ID: ${col.id}) - ${colTasks.length} tasks`));
                if (colTasks.length === 0) {
                    console.log(chalk.dim('  (empty)'));
                } else {
                    colTasks.forEach(t => {
                        const priority = t.priority ? `[P${t.priority}]` : '';
                        console.log(`  • #${chalk.yellow(t.id)} ${t.title} ${chalk.red(priority)}`);
                    });
                }
            });
        } catch (err) {
            console.error(chalk.red('Error:'), err.message);
        }
    });

program
    .command('move')
    .description('Move a task to another column')
    .argument('<taskId>', 'Task ID')
    .argument('<columnName>', 'Target column name (partial match allowed)')
    .action(async (taskId, columnName) => {
        try {
            console.log(chalk.dim(`Moving task #${taskId} to "${columnName}"...`));
            await client.moveTaskToColumn(taskId, columnName);
            console.log(chalk.green(`\nSuccess! Task #${taskId} moved.`));
        } catch (err) {
            console.error(chalk.red('Error:'), err.message);
        }
    });

program
    .command('create')
    .description('Create a new task')
    .argument('<title>', 'Task title')
    .option('-b, --board <name>', 'Board name')
    .option('-c, --col <name>', 'Column name')
    .option('-u, --assignee <name>', 'Assignee name (fuzzy)')
    .option('-p, --prio <number>', 'Priority (0-3)', '0')
    .option('-d, --desc <text>', 'Description')
    .option('-s, --subtasks <titles>', 'Comma-separated subtask titles')
    .action(async (title, options) => {
        try {
            console.log(chalk.dim('Creating task...'));
            const subtasks = options.subtasks ? options.subtasks.split(',').map(s => s.trim()) : [];
            const task = await client.createTaskDetailed({
                title,
                boardName: options.board,
                columnName: options.col,
                assigneeName: options.assignee,
                priority: options.prio,
                description: options.desc,
                subtasks
            });

            console.log(chalk.green(`\nTask created successfully! ID: ${chalk.bold(task.id)}`));
            if (task.boardId) console.log(`Board ID: ${task.boardId} | Column ID: ${task.boardColumnId || 'None'}`);
        } catch (err) {
            console.error(chalk.red('Error:'), err.message);
        }
    });

program
    .command('show')
    .description('Show task details')
    .argument('<taskId>', 'Task ID')
    .action(async (taskId) => {
        try {
            console.log(chalk.dim(`Fetching task #${taskId}...`));
            const task = await client.getTask(taskId);

            if (!task) return console.error(chalk.red('Task not found.'));

            console.log(chalk.bold.blue(`\n[#${task.id}] ${task.title}`));
            if (task.priority !== null && task.priority !== undefined) {
                const priorities = ['Low', 'Medium', 'High', 'Hold'];
                console.log(chalk.yellow(`Priority: ${priorities[task.priority] || task.priority}`));
            }

            console.log(chalk.dim(`Status: ${task.isCompleted ? 'Completed' : 'Open'}`));

            if (task.assignees && task.assignees.length > 0) {
                console.log(`Assignees: ${task.assignees.join(', ')}`);
            }

            console.log(chalk.bold('\nDescription:'));
            console.log(WeeekClient.stripHtml(task.description) || chalk.dim('(No description)'));

            if (task.subTasks && task.subTasks.length > 0) {
                console.log(chalk.bold('\nSubtasks:'));
                task.subTasks.forEach(st => {
                    const stTitle = typeof st === 'object' ? st.title : `ID: ${st}`;
                    const stStatus = (typeof st === 'object' && st.isCompleted) ? '[x]' : '[ ]';
                    console.log(`  ${stStatus} ${stTitle}`);
                });
            }

        } catch (err) {
            console.error(chalk.red('Error:'), err.message);
        }
    });

program
    .command('users')
    .description('List workspace users')
    .action(async () => {
        try {
            const users = await client.getUsers();
            console.log(chalk.bold.blue('\nWorkspace Users:'));
            users.forEach(u => {
                console.log(`- ${chalk.bold(u.name)} (${chalk.cyan(u.email)}) [ID: ${u.id}]`);
            });
        } catch (err) {
            console.error(chalk.red('Error:'), err.message);
        }
    });

program
    .command('assign')
    .description('Assign a user to a task')
    .argument('<taskId>', 'Task ID')
    .argument('<userQuery>', 'User name or email (partial)')
    .action(async (taskId, userQuery) => {
        try {
            const user = await client.findUser(userQuery);
            if (!user) return console.error(chalk.red(`User matching "${userQuery}" not found.`));

            console.log(chalk.dim(`Assigning ${user.name} to task #${taskId}...`));
            await client.request('POST', `tm/tasks/${taskId}/assignees`, { userId: user.id });
            console.log(chalk.green(`Success! Assigned ${user.name}.`));

        } catch (err) {
            console.error(chalk.red('Error:'), err.message);
        }
    });

program
    .command('timer')
    .description('Manage task timer')
    .argument('<action>', 'start | stop')
    .argument('[taskId]', 'Task ID (required for start)')
    .action(async (action, taskId) => {
        try {
            if (action === 'start') {
                if (!taskId) return console.error(chalk.red('Task ID required to start timer.'));
                await client.startTimer(taskId);
                console.log(chalk.green(`Timer started for task #${taskId}.`));
            } else if (action === 'stop') {
                if (!taskId) return console.error(chalk.red('Task ID required to stop timer (API requirement).'));
                await client.stopTimer(taskId);
                console.log(chalk.green(`Timer stopped for task #${taskId}.`));
            } else {
                console.error(chalk.red('Invalid action. Use "start" or "stop".'));
            }
        } catch (err) {
            console.error(chalk.red('Error:'), err.message);
        }
    });

program
    .command('projects')
    .description('List all projects')
    .action(async () => {
        try {
            const projects = await client.getProjects();
            console.log(chalk.bold.blue('\nProjects:'));
            projects.forEach(p => {
                console.log(`- ${chalk.bold(p.name)} (ID: ${p.id})`);
            });
        } catch (err) {
            console.error(chalk.red('Error:'), err.message);
        }
    });

program
    .command('boards')
    .description('List boards (optionally filtered by project ID)')
    .argument('[projectId]', 'Project ID')
    .action(async (projectId) => {
        try {
            console.log(chalk.dim(projectId ? `Fetching boards for project ${projectId}...` : 'Fetching all boards...'));
            const boards = await client.getBoards(projectId);
            console.log(chalk.bold.blue('\nBoards:'));
            boards.forEach(b => {
                const projectInfo = b.projectName ? ` [Project: ${b.projectName}]` : '';
                console.log(`- ${chalk.bold(b.name)} (ID: ${b.id})${projectInfo}`);
            });
        } catch (err) {
            console.error(chalk.red('Error:'), err.message);
        }
    });

program
    .command('help')
    .description('Show SKILL.md documentation')
    .action(async () => {
        const help = await client.getHelp();
        console.log(help);
    });

program.parse();
