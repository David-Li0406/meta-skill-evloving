import { z } from 'zod';
import { AbstractToolHandler, ToolDefinition } from '../lib/abstract-tool-handler.js';
import { BulkUpdateSchema } from '../types/mcp.js';
import { executeAppleScriptFile } from '../lib/applescript.js';
import { invalidateTodoCaches } from '../lib/cache.js';

type BulkUpdateParams = z.infer<typeof BulkUpdateSchema>;

export const bulkTools = [
  {
    name: 'things_bulk_update',
    description: 'Update multiple to-dos at once. Useful for batch operations like moving multiple tasks to a project, adding tags to several items, or rescheduling a group of todos.',
    inputSchema: {
      type: 'object' as const,
      properties: {
        ids: {
          type: 'array',
          items: { type: 'string' },
          description: 'Array of to-do IDs to update (max 100)',
        },
        updates: {
          type: 'object',
          description: 'Fields to update on all specified todos',
          properties: {
            when: {
              type: 'string',
              description: 'Schedule todos: today/tomorrow/evening/anytime/someday or YYYY-MM-DD',
            },
            deadline: {
              type: 'string',
              description: 'Set deadline date (YYYY-MM-DD)',
            },
            tags_add: {
              type: 'array',
              items: { type: 'string' },
              description: 'Tags to add to all todos',
            },
            tags_remove: {
              type: 'array',
              items: { type: 'string' },
              description: 'Tags to remove from all todos',
            },
            list_id: {
              type: 'string',
              description: 'Move all todos to this project/area ID',
            },
            list: {
              type: 'string',
              description: 'Move all todos to this list by name',
            },
          },
        },
      },
      required: ['ids', 'updates'],
    },
  },
];

class BulkToolHandler extends AbstractToolHandler<BulkUpdateParams> {
  protected definitions: ToolDefinition<BulkUpdateParams>[] = [
    {
      name: 'things_bulk_update',
      description: 'Update multiple to-dos at once',
      schema: BulkUpdateSchema,
    },
  ];

  async execute(toolName: string, params: BulkUpdateParams): Promise<string> {
    if (toolName !== 'things_bulk_update') {
      throw new Error(`Unknown tool: ${toolName}`);
    }

    const { ids, updates } = params;

    // Build AppleScript arguments
    const args = [
      ids.join(','),
      updates.when || '',
      updates.deadline || '',
      updates.tags_add?.join(',') || '',
      updates.tags_remove?.join(',') || '',
      updates.list_id || '',
      updates.list || '',
    ];

    const result = await executeAppleScriptFile('bulk-update', args);

    // Parse result: success|count or success|count|failed:id1,id2
    const parts = result.split('|');
    const successCount = parseInt(parts[1], 10) || 0;

    const response: {
      success: boolean;
      updated: number;
      total: number;
      failed?: string[];
      failedCount?: number;
    } = {
      success: true,
      updated: successCount,
      total: ids.length,
    };

    // Check for failures
    if (parts.length > 2 && parts[2].startsWith('failed:')) {
      const failedIds = parts[2].replace('failed:', '').split(',');
      response.failed = failedIds;
      response.failedCount = failedIds.length;
      response.success = failedIds.length === 0;
    }

    // Invalidate cache since we modified todos
    invalidateTodoCaches();

    return JSON.stringify(response, null, 2);
  }
}

export const bulkToolHandler = new BulkToolHandler();
