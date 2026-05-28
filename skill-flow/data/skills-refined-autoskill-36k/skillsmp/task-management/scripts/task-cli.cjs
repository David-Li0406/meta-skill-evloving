#!/usr/bin/env node
/**
 * Task Management CLI
 * Project-level task tracking with YAML storage
 */

const { program } = require('commander');
const { addTask, listTasks, getTask, updateTask, completeTask, deleteTask, workOnTask, blockTask } = require('./lib/task-ops.cjs');
const { generateView } = require('./lib/view-generator.cjs');
const fs = require('fs');

program
  .name('task')
  .description('Project-level task management')
  .version('1.0.0');

// Add task
program
  .command('add <title>')
  .description('Add a new task')
  .option('-d, --description <text>', 'Task description')
  .option('-p, --priority <level>', 'Priority: low, medium, high, critical')
  .option('-e, --effort <size>', 'Effort: S, M, L, XL')
  .option('-t, --tags <tags>', 'Comma-separated tags')
  .option('-a, --assignee <name>', 'Assignee name')
  .option('--due <date>', 'Due date (YYYY-MM-DD)')
  .action((title, options) => {
    const task = addTask(title, {
      description: options.description,
      priority: options.priority,
      effort: options.effort,
      tags: options.tags,
      assignee: options.assignee,
      due_date: options.due
    });
    console.log(`✅ Created task ${task.id}: ${task.title}`);
  });

// List tasks
program
  .command('list')
  .alias('ls')
  .description('List tasks')
  .option('-s, --status <status>', 'Filter by status')
  .option('-t, --tag <tag>', 'Filter by tag')
  .option('-a, --assignee <name>', 'Filter by assignee')
  .option('-p, --priority <level>', 'Filter by priority')
  .option('--json', 'Output as JSON')
  .action((options) => {
    const tasks = listTasks({
      status: options.status,
      tag: options.tag,
      assignee: options.assignee,
      priority: options.priority
    });

    if (options.json) {
      console.log(JSON.stringify(tasks, null, 2));
      return;
    }

    if (tasks.length === 0) {
      console.log('No tasks found.');
      return;
    }

    console.log('\n  ID      Status        Title');
    console.log('  ------  -----------   --------------------------------');
    tasks.forEach(t => {
      const status = t.status.padEnd(12);
      console.log(`  ${t.id}   ${status}  ${t.title}`);
    });
    console.log(`\n  Total: ${tasks.length} task(s)\n`);
  });

// Get task details
program
  .command('get <id>')
  .description('Get task details')
  .option('--json', 'Output as JSON')
  .action((id, options) => {
    const task = getTask(id);
    if (!task) {
      console.error(`Task ${id} not found.`);
      process.exit(1);
    }

    if (options.json) {
      console.log(JSON.stringify(task, null, 2));
      return;
    }

    console.log(`\n  ${task.id}: ${task.title}`);
    console.log(`  Status: ${task.status}`);
    if (task.priority) console.log(`  Priority: ${task.priority}`);
    if (task.effort) console.log(`  Effort: ${task.effort}`);
    if (task.tags) console.log(`  Tags: ${task.tags.join(', ')}`);
    if (task.description) console.log(`\n  ${task.description}`);
    if (task.context) console.log(`\n  Context: ${JSON.stringify(task.context)}`);
    console.log('');
  });

// Update task
program
  .command('update <id>')
  .description('Update a task')
  .option('--title <title>', 'New title')
  .option('-d, --description <text>', 'New description')
  .option('-s, --status <status>', 'New status')
  .option('-p, --priority <level>', 'New priority')
  .option('-e, --effort <size>', 'New effort')
  .option('-t, --tags <tags>', 'New tags')
  .option('-a, --assignee <name>', 'New assignee')
  .option('--due <date>', 'New due date')
  .option('-n, --notes <notes>', 'Progress notes')
  .action((id, options) => {
    const task = updateTask(id, {
      title: options.title,
      description: options.description,
      status: options.status,
      priority: options.priority,
      effort: options.effort,
      tags: options.tags,
      assignee: options.assignee,
      due_date: options.due,
      notes: options.notes
    });

    if (!task) {
      console.error(`Task ${id} not found.`);
      process.exit(1);
    }
    console.log(`✅ Updated task ${task.id}`);
  });

// Complete task
program
  .command('complete <id>')
  .alias('done')
  .description('Mark task as complete (auto-archives)')
  .option('-n, --notes <notes>', 'Completion notes')
  .action((id, options) => {
    const task = completeTask(id, options.notes);
    if (!task) {
      console.error(`Task ${id} not found.`);
      process.exit(1);
    }
    console.log(`✅ Completed and archived task ${task.id}: ${task.title}`);
  });

// Delete task
program
  .command('delete <id>')
  .alias('rm')
  .description('Delete a task')
  .action((id) => {
    const success = deleteTask(id);
    if (!success) {
      console.error(`Task ${id} not found.`);
      process.exit(1);
    }
    console.log(`🗑️  Deleted task ${id}`);
  });

// Work on task
program
  .command('work <id>')
  .description('Start working on a task (sets to in_progress)')
  .action((id) => {
    const task = workOnTask(id);
    if (!task) {
      console.error(`Task ${id} not found.`);
      process.exit(1);
    }
    console.log(`🔄 Working on ${task.id}: ${task.title}`);
    if (task.description) console.log(`\n  ${task.description}`);
    if (task.context) {
      console.log('\n  Context:');
      if (task.context.plan) console.log(`    Plan: ${task.context.plan}`);
      if (task.context.branch) console.log(`    Branch: ${task.context.branch}`);
      if (task.context.files) console.log(`    Files: ${task.context.files.join(', ')}`);
    }
    console.log('');
  });

// Block task
program
  .command('block <id>')
  .description('Mark task as blocked')
  .option('--by <blockerId>', 'Blocking task ID')
  .action((id, options) => {
    if (!options.by) {
      console.error('Please specify --by <blockerId>');
      process.exit(1);
    }
    const task = blockTask(id, options.by);
    if (!task) {
      console.error('Task(s) not found.');
      process.exit(1);
    }
    console.log(`🚫 Task ${id} is now blocked by ${options.by}`);
  });

// Generate markdown view
program
  .command('view')
  .description('Generate markdown view of all tasks')
  .action(() => {
    const markdown = generateView();
    console.log(markdown);
  });

// Export to file
program
  .command('export [file]')
  .description('Export tasks to markdown file')
  .action((file) => {
    const markdown = generateView();
    const outFile = file || 'tasks-view.md';
    fs.writeFileSync(outFile, markdown, 'utf8');
    console.log(`📄 Exported to ${outFile}`);
  });

program.parse();
