import { jsonBuilder } from '../lib/json-builder.js';
import { UpdateTodoJSONSchema, UpdateProjectJSONSchema, AddItemsToProjectSchema } from '../types/mcp.js';
import { AbstractToolHandler, ToolDefinition } from '../lib/abstract-tool-handler.js';
import { invalidateTodoCaches, invalidateProjectCaches } from '../lib/cache.js';
import { z } from 'zod';

type UpdateTodoParams = z.infer<typeof UpdateTodoJSONSchema>;
type UpdateProjectParams = z.infer<typeof UpdateProjectJSONSchema>;
type AddItemsParams = z.infer<typeof AddItemsToProjectSchema>;
type UpdateJSONParams = UpdateTodoParams | UpdateProjectParams | AddItemsParams;

/**
 * Unified handler for updating Things 3 items using JSON API
 * Supports updating todos, projects, and adding items to projects
 */
class UpdateJSONToolHandler extends AbstractToolHandler<UpdateJSONParams> {
  protected definitions: ToolDefinition<UpdateJSONParams>[] = [
    {
      name: 'things_update_todo',
      description: 'Update an existing to-do in Things using JSON API for full feature support',
      schema: UpdateTodoJSONSchema
    },
    {
      name: 'things_update_project',
      description: 'Update an existing project in Things using JSON API for full feature support',
      schema: UpdateProjectJSONSchema
    },
    {
      name: 'things_add_items_to_project',
      description: 'Add todos and headings to an existing project. Items are added as a flat array where headings act as visual separators for the todos that follow them.',
      schema: AddItemsToProjectSchema
    }
  ];

  async execute(toolName: string, params: UpdateJSONParams): Promise<string> {
    let result: string;

    if (toolName === 'things_update_todo') {
      const todoParams = params as z.infer<typeof UpdateTodoJSONSchema>;
      result = await jsonBuilder.updateTodo(todoParams);
      invalidateTodoCaches();
    } else if (toolName === 'things_update_project') {
      const projectParams = params as z.infer<typeof UpdateProjectJSONSchema>;
      result = await jsonBuilder.updateProject(projectParams);
      invalidateProjectCaches();
    } else if (toolName === 'things_add_items_to_project') {
      const addItemsParams = params as z.infer<typeof AddItemsToProjectSchema>;
      result = await jsonBuilder.addItemsToProject(addItemsParams);
      invalidateTodoCaches(); // Adding items to project affects todo lists
    } else {
      throw new Error(`Unknown tool: ${toolName}`);
    }

    return result;
  }
}

export const updateJSONToolHandler = new UpdateJSONToolHandler();

export const updateJSONTools = updateJSONToolHandler.tools;
export const handleUpdateJSON = updateJSONToolHandler.handle.bind(updateJSONToolHandler);