import { executeAppleScriptFile } from '../lib/applescript.js';
import { CompleteTodoSchema, CancelTodoSchema } from '../types/mcp.js';
import { AbstractToolHandler, ToolDefinition } from '../lib/abstract-tool-handler.js';
import { invalidateTodoCaches } from '../lib/cache.js';
import { z } from 'zod';

type CompleteTodoParams = z.infer<typeof CompleteTodoSchema>;
type CancelTodoParams = z.infer<typeof CancelTodoSchema>;
type StatusParams = CompleteTodoParams | CancelTodoParams;

/**
 * Handler for completing and canceling Things 3 todos
 */
class StatusToolHandler extends AbstractToolHandler<StatusParams> {
  protected definitions: ToolDefinition<StatusParams>[] = [
    {
      name: 'things_complete_todo',
      description: 'Mark a to-do as complete. Moves it to the Logbook.',
      schema: CompleteTodoSchema
    },
    {
      name: 'things_cancel_todo',
      description: 'Cancel a to-do. Removes it from active lists.',
      schema: CancelTodoSchema
    }
  ];

  async execute(toolName: string, params: StatusParams): Promise<string> {
    const { id } = params;
    let scriptName: string;
    let action: string;

    if (toolName === 'things_complete_todo') {
      scriptName = 'complete-todo';
      action = 'completed';
    } else if (toolName === 'things_cancel_todo') {
      scriptName = 'cancel-todo';
      action = 'canceled';
    } else {
      throw new Error(`Unknown tool: ${toolName}`);
    }

    const output = await executeAppleScriptFile(scriptName, [id]);

    // Check for error response
    if (output.startsWith('error:')) {
      const errorMsg = output.substring(6);
      throw new Error(`Failed to ${action.slice(0, -2)} todo: ${errorMsg}`);
    }

    // Parse success response: "completed|id|name" or "canceled|id|name"
    const parts = output.split('|');
    if (parts.length >= 3) {
      const [status, todoId, todoName] = parts;
      invalidateTodoCaches();
      return JSON.stringify({
        success: true,
        action: status,
        todo: {
          id: todoId,
          name: todoName
        }
      }, null, 2);
    }

    // Fallback for unexpected output format
    invalidateTodoCaches();
    return JSON.stringify({
      success: true,
      action,
      id
    }, null, 2);
  }
}

export const statusToolHandler = new StatusToolHandler();

export const statusTools = statusToolHandler.tools;
export const handleStatus = statusToolHandler.handle.bind(statusToolHandler);
