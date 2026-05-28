import { executeAppleScriptFile } from '../lib/applescript.js';
import { GetStatsSchema } from '../types/mcp.js';
import { AbstractToolHandler, ToolDefinition } from '../lib/abstract-tool-handler.js';
import { z } from 'zod';

type StatsParams = z.infer<typeof GetStatsSchema>;

interface TaskStats {
  inbox: number;
  today: number;
  upcoming: number;
  anytime: number;
  someday: number;
  logbook: number;
  projects: number;
  areas: number;
  totalActive: number;
}

/**
 * Handler for getting Things 3 task statistics
 */
class StatsToolHandler extends AbstractToolHandler<StatsParams> {
  protected definitions: ToolDefinition<StatsParams>[] = [
    {
      name: 'things_get_stats',
      description: 'Get task statistics including counts for inbox, today, upcoming, anytime, someday, completed tasks, projects, and areas.',
      schema: GetStatsSchema
    }
  ];

  async execute(toolName: string, _params: StatsParams): Promise<string> {
    if (toolName !== 'things_get_stats') {
      throw new Error(`Unknown tool: ${toolName}`);
    }

    const output = await executeAppleScriptFile('get-stats', []);

    // Check for error response
    if (output.startsWith('error:')) {
      const errorMsg = output.substring(6);
      throw new Error(`Failed to get stats: ${errorMsg}`);
    }

    // Parse output: inbox|today|upcoming|anytime|someday|logbook|projects|areas
    const parts = output.split('|');
    if (parts.length >= 8) {
      const stats: TaskStats = {
        inbox: parseInt(parts[0], 10) || 0,
        today: parseInt(parts[1], 10) || 0,
        upcoming: parseInt(parts[2], 10) || 0,
        anytime: parseInt(parts[3], 10) || 0,
        someday: parseInt(parts[4], 10) || 0,
        logbook: parseInt(parts[5], 10) || 0,
        projects: parseInt(parts[6], 10) || 0,
        areas: parseInt(parts[7], 10) || 0,
        totalActive: 0
      };

      // Calculate total active tasks (excluding logbook/completed)
      stats.totalActive = stats.inbox + stats.today + stats.upcoming + stats.anytime + stats.someday;

      return JSON.stringify({
        stats,
        summary: {
          activeTasksNeedingAttention: stats.inbox + stats.today,
          deferredTasks: stats.upcoming + stats.anytime + stats.someday,
          completedTasks: stats.logbook
        }
      }, null, 2);
    }

    throw new Error('Unexpected output format from get-stats script');
  }
}

export const statsToolHandler = new StatsToolHandler();

export const statsTools = statsToolHandler.tools;
export const handleStats = statsToolHandler.handle.bind(statsToolHandler);
