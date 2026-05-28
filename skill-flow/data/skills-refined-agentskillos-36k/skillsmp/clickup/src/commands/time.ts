import { Command } from 'commander';
import ora from 'ora';
import { getClient } from '../api/client.js';
import {
  formatTimeEntry,
  formatTimeEntriesTable,
  formatWeeklyReport,
  formatDuration,
  parseDuration,
  success,
  error,
  info,
} from '../utils/index.js';
import {
  parseDate,
  parseDateTimeToMs,
  getStartOfDay,
  getEndOfDay,
  getWeekRange,
  getWeekStart,
  getWeekDays,
  formatDateYMD,
  formatDateReadable,
  getDayOfWeek,
  isSameDay,
} from '../utils/dates.js';
import type { TimeEntry, WeeklyReport, WeeklyReportEntry } from '../types/clickup.js';

export function createTimeCommand(): Command {
  const time = new Command('time').description('Manage time entries');

  // List time entries
  time
    .command('list')
    .description('List time entries')
    .option('-d, --date <date>', 'Show entries for specific date (default: today)')
    .option('--start <date>', 'Start date for range')
    .option('--end <date>', 'End date for range')
    .option('--task <taskId>', 'Filter by task ID')
    .option('-t, --table', 'Output as table')
    .option('--json', 'Output as JSON')
    .action(async (options) => {
      const spinner = ora('Fetching time entries...').start();

      try {
        const client = getClient();
        const config = (client as unknown as { config: { workspaceId: string; teamId?: string } }).config;
        const teamId = config.teamId || config.workspaceId;

        // Determine date range
        let startDate: number;
        let endDate: number;

        if (options.start && options.end) {
          startDate = getStartOfDay(options.start);
          endDate = getEndOfDay(options.end);
        } else if (options.date) {
          startDate = getStartOfDay(options.date);
          endDate = getEndOfDay(options.date);
        } else {
          // Default to today
          startDate = getStartOfDay(new Date());
          endDate = getEndOfDay(new Date());
        }

        let entries = await client.getTimeEntries(teamId, {
          startDate,
          endDate,
        });

        // Filter by task if specified
        if (options.task) {
          const resolvedTaskId = await client.resolveTaskId(options.task);
          entries = entries.filter((e) => e.task?.id === resolvedTaskId);
        }

        spinner.stop();

        if (entries.length === 0) {
          info('No time entries found for the specified period.');
          return;
        }

        if (options.json) {
          console.log(JSON.stringify(entries, null, 2));
        } else if (options.table) {
          console.log(formatTimeEntriesTable(entries));
        } else {
          // Calculate total
          let totalMs = 0;
          for (const entry of entries) {
            const durationMs = parseInt(entry.duration_ms || entry.duration || '0', 10);
            totalMs += durationMs;
          }

          console.log(`Time entries (${entries.length}):\n`);
          for (const entry of entries) {
            console.log(formatTimeEntry(entry));
            console.log('');
          }
          console.log(`Total: ${formatDuration(totalMs)}`);
        }
      } catch (err) {
        spinner.fail('Failed to fetch time entries');
        error(err instanceof Error ? err.message : String(err));
      }
    });

  // Weekly report
  time
    .command('report')
    .description('Show weekly time report')
    .option('-w, --week <date>', 'Week containing this date (default: current week)')
    .option('--detailed', 'Show detailed breakdown')
    .option('--json', 'Output as JSON')
    .action(async (options) => {
      const spinner = ora('Generating weekly report...').start();

      try {
        const client = getClient();
        const config = (client as unknown as { config: { workspaceId: string; teamId?: string } }).config;
        const teamId = config.teamId || config.workspaceId;

        // Get week range
        const weekDate = options.week ? parseDate(options.week) : new Date();
        const { start, end } = getWeekRange(weekDate);

        const entries = await client.getTimeEntries(teamId, {
          startDate: start,
          endDate: end,
        });

        // Build report
        const weekStart = getWeekStart(weekDate);
        const weekDays = getWeekDays(weekStart);

        const dailyBreakdown: WeeklyReportEntry[] = weekDays.map((day) => ({
          date: formatDateYMD(day),
          dayOfWeek: getDayOfWeek(day),
          totalHours: 0,
          entries: [],
        }));

        const taskTotals = new Map<string, { taskId: string; taskName: string; totalMs: number }>();
        let totalMs = 0;

        for (const entry of entries) {
          const entryDate = new Date(parseInt(entry.start, 10));
          const durationMs = parseInt(entry.duration_ms || entry.duration || '0', 10);

          // Add to daily breakdown
          const dayIndex = weekDays.findIndex((day) => isSameDay(day, entryDate));
          if (dayIndex >= 0) {
            dailyBreakdown[dayIndex].totalHours += durationMs / 3600000;
            dailyBreakdown[dayIndex].entries.push({
              id: entry.id,
              taskId: entry.task?.custom_id || entry.task?.id,
              taskName: entry.task?.name,
              date: formatDateYMD(entryDate),
              startTime: new Date(parseInt(entry.start, 10)).toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit',
              }),
              endTime: entry.end
                ? new Date(parseInt(entry.end, 10)).toLocaleTimeString('en-US', {
                    hour: '2-digit',
                    minute: '2-digit',
                  })
                : undefined,
              duration: formatDuration(durationMs),
              description: entry.description,
            });
          }

          // Add to task totals
          if (entry.task) {
            const taskKey = entry.task.id;
            const existing = taskTotals.get(taskKey);
            if (existing) {
              existing.totalMs += durationMs;
            } else {
              taskTotals.set(taskKey, {
                taskId: entry.task.custom_id || entry.task.id,
                taskName: entry.task.name,
                totalMs: durationMs,
              });
            }
          }

          totalMs += durationMs;
        }

        const report: WeeklyReport = {
          weekStart: formatDateReadable(weekStart),
          weekEnd: formatDateReadable(weekDays[6]),
          totalHours: totalMs / 3600000,
          dailyBreakdown,
          taskBreakdown: Array.from(taskTotals.values()).map((t) => ({
            taskId: t.taskId,
            taskName: t.taskName,
            totalHours: t.totalMs / 3600000,
          })),
        };

        spinner.stop();

        if (options.json) {
          console.log(JSON.stringify(report, null, 2));
        } else {
          console.log(formatWeeklyReport(report));
        }
      } catch (err) {
        spinner.fail('Failed to generate report');
        error(err instanceof Error ? err.message : String(err));
      }
    });

  // Add time entry
  time
    .command('add <taskId>')
    .description('Add a time entry to a task')
    .option('-d, --duration <duration>', 'Duration (e.g., "2h 30m")')
    .option('--start <datetime>', 'Start time (YYYY-MM-DD HH:MM)')
    .option('--end <datetime>', 'End time (YYYY-MM-DD HH:MM)')
    .option('--date <date>', 'Date for the entry (default: today)')
    .option('--description <desc>', 'Description')
    .option('--billable', 'Mark as billable')
    .option('--json', 'Output as JSON')
    .action(async (taskId: string, options) => {
      const spinner = ora('Creating time entry...').start();

      try {
        const client = getClient();
        const config = (client as unknown as { config: { workspaceId: string; teamId?: string; userId?: string } }).config;
        const teamId = config.teamId || config.workspaceId;

        // Resolve task ID
        const resolvedTaskId = await client.resolveTaskId(taskId);

        // Calculate start and end times
        let startMs: number;
        let endMs: number | undefined;
        let durationMs: number | undefined;

        if (options.start && options.end) {
          // Explicit start and end
          startMs = parseDateTimeToMs(options.start);
          endMs = parseDateTimeToMs(options.end);
          durationMs = endMs - startMs;
        } else if (options.start && options.duration) {
          // Start + duration
          startMs = parseDateTimeToMs(options.start);
          durationMs = parseDuration(options.duration);
          endMs = startMs + durationMs;
        } else if (options.duration) {
          // Just duration - use date or today
          const date = options.date ? parseDate(options.date) : new Date();
          // Default to 9 AM on the specified date
          date.setHours(9, 0, 0, 0);
          startMs = date.getTime();
          durationMs = parseDuration(options.duration);
          endMs = startMs + durationMs;
        } else {
          spinner.fail('Please provide --duration or both --start and --end');
          return;
        }

        const entry = await client.createTimeEntry(teamId, {
          tid: resolvedTaskId,
          start: startMs,
          end: endMs,
          duration: durationMs,
          description: options.description,
          billable: options.billable,
          assignee: config.userId ? parseInt(config.userId, 10) : undefined,
        });

        spinner.stop();

        if (options.json) {
          console.log(JSON.stringify(entry, null, 2));
        } else {
          success(`Time entry created: ${formatDuration(durationMs)}`);
          console.log(formatTimeEntry(entry));
        }
      } catch (err) {
        spinner.fail('Failed to create time entry');
        error(err instanceof Error ? err.message : String(err));
      }
    });

  // Update time entry
  time
    .command('update <entryId>')
    .description('Update a time entry')
    .option('-d, --duration <duration>', 'New duration (e.g., "2h 30m")')
    .option('--start <datetime>', 'New start time (YYYY-MM-DD HH:MM)')
    .option('--end <datetime>', 'New end time (YYYY-MM-DD HH:MM)')
    .option('--description <desc>', 'New description')
    .option('--billable', 'Mark as billable')
    .option('--not-billable', 'Mark as not billable')
    .option('--json', 'Output as JSON')
    .action(async (entryId: string, options) => {
      const spinner = ora('Updating time entry...').start();

      try {
        const client = getClient();
        const config = (client as unknown as { config: { workspaceId: string; teamId?: string } }).config;
        const teamId = config.teamId || config.workspaceId;

        const updateData: Parameters<typeof client.updateTimeEntry>[2] = {};

        if (options.start) {
          updateData.start = parseDateTimeToMs(options.start);
        }
        if (options.end) {
          updateData.end = parseDateTimeToMs(options.end);
        }
        if (options.duration) {
          updateData.duration = parseDuration(options.duration);
        }
        if (options.description) {
          updateData.description = options.description;
        }
        if (options.billable) {
          updateData.billable = true;
        }
        if (options.notBillable) {
          updateData.billable = false;
        }

        const entry = await client.updateTimeEntry(teamId, entryId, updateData);

        spinner.stop();

        if (options.json) {
          console.log(JSON.stringify(entry, null, 2));
        } else {
          success('Time entry updated');
          console.log(formatTimeEntry(entry));
        }
      } catch (err) {
        spinner.fail('Failed to update time entry');
        error(err instanceof Error ? err.message : String(err));
      }
    });

  // Move time entry (shorthand for changing date)
  time
    .command('move <entryId>')
    .description('Move a time entry to a different date')
    .requiredOption('--to <date>', 'Target date (YYYY-MM-DD)')
    .option('--json', 'Output as JSON')
    .action(async (entryId: string, options) => {
      const spinner = ora('Moving time entry...').start();

      try {
        const client = getClient();
        const config = (client as unknown as { config: { workspaceId: string; teamId?: string } }).config;
        const teamId = config.teamId || config.workspaceId;

        // Get current entry to preserve time of day
        const currentEntry = await client.getTimeEntry(teamId, entryId);
        const currentStart = new Date(parseInt(currentEntry.start, 10));

        // Parse target date and preserve time of day
        const targetDate = parseDate(options.to);
        targetDate.setHours(
          currentStart.getHours(),
          currentStart.getMinutes(),
          currentStart.getSeconds(),
          0
        );

        const newStartMs = targetDate.getTime();
        const durationMs = currentEntry.duration_ms
          ? parseInt(currentEntry.duration_ms, 10)
          : 0;
        const newEndMs = newStartMs + durationMs;

        const entry = await client.updateTimeEntry(teamId, entryId, {
          start: newStartMs,
          end: newEndMs,
        });

        spinner.stop();

        if (options.json) {
          console.log(JSON.stringify(entry, null, 2));
        } else {
          success(`Time entry moved to ${formatDateReadable(targetDate)}`);
          console.log(formatTimeEntry(entry));
        }
      } catch (err) {
        spinner.fail('Failed to move time entry');
        error(err instanceof Error ? err.message : String(err));
      }
    });

  // Delete time entry
  time
    .command('delete <entryId>')
    .description('Delete a time entry')
    .option('-f, --force', 'Skip confirmation')
    .action(async (entryId: string, options) => {
      try {
        const client = getClient();
        const config = (client as unknown as { config: { workspaceId: string; teamId?: string } }).config;
        const teamId = config.teamId || config.workspaceId;

        if (!options.force) {
          // Get entry info for confirmation
          const entry = await client.getTimeEntry(teamId, entryId);
          const duration = formatDuration(entry.duration_ms);
          const taskName = entry.task?.name || 'No task';
          console.log(`About to delete: ${duration} on "${taskName}"`);
          console.log('Use --force to skip this confirmation.');
          return;
        }

        const spinner = ora('Deleting time entry...').start();
        await client.deleteTimeEntry(teamId, entryId);
        spinner.stop();

        success(`Time entry ${entryId} deleted`);
      } catch (err) {
        error(err instanceof Error ? err.message : String(err));
      }
    });

  // Start timer
  time
    .command('start <taskId>')
    .description('Start a timer on a task')
    .option('--description <desc>', 'Description for the time entry')
    .action(async (taskId: string, options) => {
      const spinner = ora('Starting timer...').start();

      try {
        const client = getClient();
        const config = (client as unknown as { config: { workspaceId: string; teamId?: string } }).config;
        const teamId = config.teamId || config.workspaceId;

        // Resolve task ID
        const resolvedTaskId = await client.resolveTaskId(taskId);

        const entry = await client.startTimer(teamId, resolvedTaskId, options.description);

        spinner.stop();
        success(`Timer started on ${entry.task?.name || taskId}`);
      } catch (err) {
        spinner.fail('Failed to start timer');
        error(err instanceof Error ? err.message : String(err));
      }
    });

  // Stop timer
  time
    .command('stop')
    .description('Stop the current timer')
    .action(async () => {
      const spinner = ora('Stopping timer...').start();

      try {
        const client = getClient();
        const config = (client as unknown as { config: { workspaceId: string; teamId?: string } }).config;
        const teamId = config.teamId || config.workspaceId;

        const entry = await client.stopTimer(teamId);

        spinner.stop();
        const duration = formatDuration(entry.duration_ms);
        success(`Timer stopped: ${duration}`);
        console.log(formatTimeEntry(entry));
      } catch (err) {
        spinner.fail('Failed to stop timer');
        error(err instanceof Error ? err.message : String(err));
      }
    });

  // Current timer status
  time
    .command('current')
    .description('Show current running timer')
    .option('--json', 'Output as JSON')
    .action(async (options) => {
      const spinner = ora('Checking timer...').start();

      try {
        const client = getClient();
        const config = (client as unknown as { config: { workspaceId: string; teamId?: string } }).config;
        const teamId = config.teamId || config.workspaceId;

        const entry = await client.getCurrentTimer(teamId);

        spinner.stop();

        if (!entry) {
          info('No timer currently running.');
          return;
        }

        if (options.json) {
          console.log(JSON.stringify(entry, null, 2));
        } else {
          console.log('Current timer:');
          console.log(formatTimeEntry(entry));
        }
      } catch (err) {
        spinner.fail('Failed to check timer');
        error(err instanceof Error ? err.message : String(err));
      }
    });

  return time;
}
