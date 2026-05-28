import chalk from 'chalk';
import Table from 'cli-table3';
import type { Task, TimeEntry, WeeklyReport, Comment } from '../types/clickup.js';

/**
 * Format milliseconds to human-readable duration
 */
export function formatDuration(ms: number | string | null | undefined): string {
  if (!ms) return '-';

  const totalMs = typeof ms === 'string' ? parseInt(ms, 10) : ms;
  if (isNaN(totalMs) || totalMs <= 0) return '-';

  const hours = Math.floor(totalMs / 3600000);
  const minutes = Math.floor((totalMs % 3600000) / 60000);

  if (hours > 0 && minutes > 0) {
    return `${hours}h ${minutes}m`;
  } else if (hours > 0) {
    return `${hours}h`;
  } else {
    return `${minutes}m`;
  }
}

/**
 * Parse duration string to milliseconds
 * Supports: "2h", "30m", "2h 30m", "2.5h", "150" (minutes)
 */
export function parseDuration(input: string): number {
  // If just a number, treat as minutes
  if (/^\d+$/.test(input)) {
    return parseInt(input, 10) * 60000;
  }

  let totalMs = 0;

  // Match hours
  const hoursMatch = input.match(/(\d+(?:\.\d+)?)\s*h/i);
  if (hoursMatch) {
    totalMs += parseFloat(hoursMatch[1]) * 3600000;
  }

  // Match minutes
  const minutesMatch = input.match(/(\d+)\s*m/i);
  if (minutesMatch) {
    totalMs += parseInt(minutesMatch[1], 10) * 60000;
  }

  return totalMs;
}

/**
 * Format a timestamp to date string
 */
export function formatDate(timestamp: string | number | undefined): string {
  if (!timestamp) return '-';

  const ts = typeof timestamp === 'string' ? parseInt(timestamp, 10) : timestamp;
  if (isNaN(ts)) return '-';

  return new Date(ts).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

/**
 * Format a timestamp to time string
 */
export function formatTime(timestamp: string | number | undefined): string {
  if (!timestamp) return '-';

  const ts = typeof timestamp === 'string' ? parseInt(timestamp, 10) : timestamp;
  if (isNaN(ts)) return '-';

  return new Date(ts).toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  });
}

/**
 * Format a timestamp to datetime string
 */
export function formatDateTime(timestamp: string | number | undefined): string {
  if (!timestamp) return '-';

  const ts = typeof timestamp === 'string' ? parseInt(timestamp, 10) : timestamp;
  if (isNaN(ts)) return '-';

  return new Date(ts).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  });
}

/**
 * Format priority with color
 */
export function formatPriority(priority: { priority: string } | null | undefined): string {
  if (!priority) return chalk.gray('none');

  switch (priority.priority.toLowerCase()) {
    case 'urgent':
      return chalk.red.bold('URGENT');
    case 'high':
      return chalk.red('high');
    case 'normal':
      return chalk.yellow('normal');
    case 'low':
      return chalk.blue('low');
    default:
      return priority.priority;
  }
}

/**
 * Format status with color
 */
export function formatStatus(status: { status: string; color?: string }): string {
  const statusName = status.status;

  // Common status mappings
  switch (statusName.toLowerCase()) {
    case 'complete':
    case 'done':
    case 'closed':
      return chalk.green(statusName);
    case 'in progress':
    case 'developing':
    case 'in review':
      return chalk.yellow(statusName);
    case 'to do':
    case 'open':
    case 'to refine':
      return chalk.gray(statusName);
    case 'blocked':
      return chalk.red(statusName);
    default:
      return statusName;
  }
}

/**
 * Format a task for display
 */
export function formatTask(task: Task, options: { verbose?: boolean } = {}): string {
  const lines: string[] = [];

  // Header line
  const id = task.custom_id || task.id;
  lines.push(chalk.bold.cyan(id) + ' | ' + chalk.bold(task.name));

  // Status and priority
  const statusStr = formatStatus(task.status);
  const priorityStr = formatPriority(task.priority);
  lines.push(`Status: ${statusStr} | Priority: ${priorityStr}`);

  // Assignees
  if (task.assignees.length > 0) {
    const assigneeNames = task.assignees.map((a) => a.username).join(', ');
    lines.push(`Assignee: ${assigneeNames}`);
  }

  // Time tracking
  const tracked = formatDuration(task.time_spent);
  const estimated = formatDuration(task.time_estimate);
  if (tracked !== '-' || estimated !== '-') {
    lines.push(`Time: ${tracked} tracked / ${estimated} estimated`);
  }

  // Due date
  if (task.due_date) {
    lines.push(`Due: ${formatDate(task.due_date)}`);
  }

  // Description (verbose mode)
  if (options.verbose && task.text_content) {
    lines.push('');
    lines.push(chalk.dim('Description:'));
    lines.push(task.text_content.substring(0, 500));
    if (task.text_content.length > 500) {
      lines.push(chalk.dim('... (truncated)'));
    }
  }

  // URL
  lines.push(chalk.dim(task.url));

  return lines.join('\n');
}

/**
 * Format tasks as a table
 */
export function formatTasksTable(tasks: Task[]): string {
  const table = new Table({
    head: [
      chalk.bold('ID'),
      chalk.bold('Name'),
      chalk.bold('Status'),
      chalk.bold('Priority'),
      chalk.bold('Assignee'),
      chalk.bold('Due'),
    ],
    colWidths: [12, 40, 15, 10, 15, 12],
    wordWrap: true,
  });

  for (const task of tasks) {
    table.push([
      task.custom_id || task.id.substring(0, 10),
      task.name.substring(0, 38),
      task.status.status,
      task.priority?.priority || '-',
      task.assignees[0]?.username || '-',
      task.due_date ? formatDate(task.due_date) : '-',
    ]);
  }

  return table.toString();
}

/**
 * Format a time entry for display
 */
export function formatTimeEntry(entry: TimeEntry): string {
  const lines: string[] = [];

  const taskInfo = entry.task
    ? `${entry.task.custom_id || entry.task.id} - ${entry.task.name}`
    : 'No task';

  lines.push(chalk.bold.cyan(entry.id) + ' | ' + taskInfo);

  const startTs = parseInt(entry.start, 10);
  const date = formatDate(startTs);
  const startTime = formatTime(startTs);
  const endTime = entry.end ? formatTime(entry.end) : 'running';
  const duration = formatDuration(entry.duration_ms || entry.duration);

  lines.push(`${date} | ${startTime} - ${endTime} | ${chalk.green(duration)}`);

  if (entry.description) {
    lines.push(chalk.dim(entry.description));
  }

  return lines.join('\n');
}

/**
 * Format time entries as a table
 */
export function formatTimeEntriesTable(entries: TimeEntry[]): string {
  const table = new Table({
    head: [
      chalk.bold('ID'),
      chalk.bold('Task'),
      chalk.bold('Date'),
      chalk.bold('Start'),
      chalk.bold('End'),
      chalk.bold('Duration'),
      chalk.bold('Description'),
    ],
    colWidths: [22, 25, 12, 10, 10, 10, 25],
    wordWrap: true,
  });

  for (const entry of entries) {
    const startTs = parseInt(entry.start, 10);
    table.push([
      entry.id.substring(0, 20),
      entry.task?.name?.substring(0, 23) || '-',
      formatDate(startTs),
      formatTime(startTs),
      entry.end ? formatTime(entry.end) : '-',
      formatDuration(entry.duration_ms || entry.duration),
      entry.description?.substring(0, 23) || '-',
    ]);
  }

  return table.toString();
}

/**
 * Format weekly time report
 */
export function formatWeeklyReport(report: WeeklyReport): string {
  const lines: string[] = [];

  lines.push(chalk.bold.underline(`Weekly Time Report: ${report.weekStart} - ${report.weekEnd}`));
  lines.push('');

  // Daily breakdown
  lines.push(chalk.bold('Daily Breakdown:'));
  const dailyTable = new Table({
    head: [
      chalk.bold('Day'),
      chalk.bold('Date'),
      chalk.bold('Hours'),
      chalk.bold('Entries'),
    ],
    colWidths: [12, 14, 10, 8],
  });

  for (const day of report.dailyBreakdown) {
    dailyTable.push([
      day.dayOfWeek,
      day.date,
      day.totalHours.toFixed(2),
      day.entries.length.toString(),
    ]);
  }

  lines.push(dailyTable.toString());
  lines.push('');

  // Task breakdown
  if (report.taskBreakdown.length > 0) {
    lines.push(chalk.bold('By Task:'));
    const taskTable = new Table({
      head: [chalk.bold('Task'), chalk.bold('Hours')],
      colWidths: [50, 10],
    });

    for (const task of report.taskBreakdown) {
      taskTable.push([
        `${task.taskId} - ${task.taskName.substring(0, 40)}`,
        task.totalHours.toFixed(2),
      ]);
    }

    lines.push(taskTable.toString());
    lines.push('');
  }

  // Total
  lines.push(chalk.bold.green(`Total: ${report.totalHours.toFixed(2)} hours`));

  return lines.join('\n');
}

/**
 * Format comments
 */
export function formatComments(comments: Comment[]): string {
  const lines: string[] = [];

  for (const comment of comments) {
    lines.push(
      chalk.bold(comment.user.username) +
        ' - ' +
        chalk.dim(formatDateTime(comment.date))
    );
    lines.push(comment.comment_text);
    lines.push('');
  }

  return lines.join('\n');
}

/**
 * Success message
 */
export function success(message: string): void {
  console.log(chalk.green('✓') + ' ' + message);
}

/**
 * Error message
 */
export function error(message: string): void {
  console.error(chalk.red('✗') + ' ' + message);
}

/**
 * Warning message
 */
export function warn(message: string): void {
  console.warn(chalk.yellow('⚠') + ' ' + message);
}

/**
 * Info message
 */
export function info(message: string): void {
  console.log(chalk.blue('ℹ') + ' ' + message);
}
