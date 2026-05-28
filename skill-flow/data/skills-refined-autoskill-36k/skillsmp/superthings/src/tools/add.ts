import { jsonBuilder } from '../lib/json-builder.js';
import { AddTodoSchema, AddProjectSchema } from '../types/mcp.js';
import { AbstractToolHandler, ToolDefinition } from '../lib/abstract-tool-handler.js';
import { invalidateTodoCaches, invalidateProjectCaches } from '../lib/cache.js';
import { z } from 'zod';

type AddParams = z.infer<typeof AddTodoSchema> | z.infer<typeof AddProjectSchema>;

/**
 * Unified handler for creating Things 3 items using JSON API
 * Supports to-dos, projects, headings, and hierarchical structures
 */
class AddToolHandler extends AbstractToolHandler<AddParams> {
  protected definitions: ToolDefinition<AddParams>[] = [
    {
      name: 'things_add_todo',
      description: 'Add a new to-do to Things with full support for checklists to break down complex tasks into manageable steps. Use checklist when task has multiple components that don\'t warrant a separate project.',
      schema: AddTodoSchema
    },
    {
      name: 'things_add_project',
      description: 'Creates a project in Things with support for sections (headings) and todos. Perfect for complex projects with multiple phases, days, or categories. Headings act as visual dividers - todos that follow a heading in the items array will appear grouped under it.',
      schema: AddProjectSchema
    }
  ];

  async execute(toolName: string, params: AddParams): Promise<string> {
    let result: string;

    if (toolName === 'things_add_todo') {
      const todoParams = params as z.infer<typeof AddTodoSchema>;
      result = await jsonBuilder.createTodo(todoParams);
      invalidateTodoCaches();
    } else if (toolName === 'things_add_project') {
      const projectParams = params as z.infer<typeof AddProjectSchema>;
      result = await jsonBuilder.createProject(projectParams);
      invalidateProjectCaches();
    } else {
      throw new Error(`Unknown tool: ${toolName}`);
    }

    return result;
  }
}

export const addToolHandler = new AddToolHandler();

export const addTools = addToolHandler.tools;
export const handleAdd = addToolHandler.handle.bind(addToolHandler);