import { executeAppleScriptFile } from '../lib/applescript.js';
import { DeleteTodoSchema, DeleteProjectSchema } from '../types/mcp.js';
import { AbstractToolHandler, ToolDefinition } from '../lib/abstract-tool-handler.js';
import { invalidateTodoCaches, invalidateProjectCaches } from '../lib/cache.js';
import { z } from 'zod';

type DeleteTodoParams = z.infer<typeof DeleteTodoSchema>;
type DeleteProjectParams = z.infer<typeof DeleteProjectSchema>;
type DeleteParams = DeleteTodoParams | DeleteProjectParams;

/**
 * Handler for deleting Things 3 todos and projects
 * Requires explicit confirmation to prevent accidental deletion
 */
class DeleteToolHandler extends AbstractToolHandler<DeleteParams> {
  protected definitions: ToolDefinition<DeleteParams>[] = [
    {
      name: 'things_delete_todo',
      description: 'Delete a to-do (moves to Trash). Requires confirm: true to prevent accidents.',
      schema: DeleteTodoSchema
    },
    {
      name: 'things_delete_project',
      description: 'Delete a project and all its todos (moves to Trash). Requires confirm: true to prevent accidents.',
      schema: DeleteProjectSchema
    }
  ];

  async execute(toolName: string, params: DeleteParams): Promise<string> {
    const { id } = params;
    let scriptName: string;
    let itemType: string;

    if (toolName === 'things_delete_todo') {
      scriptName = 'delete-todo';
      itemType = 'todo';
    } else if (toolName === 'things_delete_project') {
      scriptName = 'delete-project';
      itemType = 'project';
    } else {
      throw new Error(`Unknown tool: ${toolName}`);
    }

    const output = await executeAppleScriptFile(scriptName, [id]);

    // Check for error response
    if (output.startsWith('error:')) {
      const errorMsg = output.substring(6);
      throw new Error(`Failed to delete ${itemType}: ${errorMsg}`);
    }

    // Parse success response: "deleted|id|name"
    const parts = output.split('|');
    if (parts.length >= 3) {
      const [, itemId, itemName] = parts;

      // Invalidate appropriate caches
      if (itemType === 'todo') {
        invalidateTodoCaches();
      } else {
        invalidateProjectCaches();
        invalidateTodoCaches(); // Projects contain todos
      }

      return JSON.stringify({
        success: true,
        action: 'deleted',
        [itemType]: {
          id: itemId,
          name: itemName
        }
      }, null, 2);
    }

    // Fallback for unexpected output format
    if (itemType === 'todo') {
      invalidateTodoCaches();
    } else {
      invalidateProjectCaches();
    }

    return JSON.stringify({
      success: true,
      action: 'deleted',
      id
    }, null, 2);
  }
}

export const deleteToolHandler = new DeleteToolHandler();

export const deleteTools = deleteToolHandler.tools;
export const handleDelete = deleteToolHandler.handle.bind(deleteToolHandler);
