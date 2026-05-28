import { AddTodoParams, AddProjectParams, UpdateTodoJSONParams, UpdateProjectJSONParams, AddItemsToProjectParams } from '../types/things.js';
import { executeAppleScriptFile } from './applescript.js';

/**
 * Unified builder for Things 3 items using AppleScript (SILENT MODE)
 * Uses AppleScript instead of URL schemes to avoid activating/focusing Things
 */
export class ThingsJSONBuilder {
  /**
   * Create a to-do item using AppleScript
   */
  async createTodo(params: AddTodoParams): Promise<string> {
    const args = this.buildTodoArgs(params);
    await executeAppleScriptFile('create-todo', args);
    return `Created to-do: "${params.title}"`;
  }

  /**
   * Create a project using AppleScript
   * Returns structured JSON when items are included
   */
  async createProject(params: AddProjectParams): Promise<string> {
    const args = this.buildProjectArgs(params);
    const projectId = await executeAppleScriptFile('create-project', args);

    // If no items, return simple success
    if (!params.items || params.items.length === 0) {
      return JSON.stringify({
        success: true,
        project: {
          id: projectId,
          title: params.title
        }
      }, null, 2);
    }

    // Process items with detailed tracking
    const results = {
      success: [] as { title: string }[],
      failed: [] as { title: string; reason: string }[],
      skipped: [] as { title: string; reason: string }[]
    };

    for (const item of params.items) {
      if (item.type === 'heading') {
        results.skipped.push({
          title: item.title,
          reason: 'Headings cannot be added via AppleScript'
        });
        continue;
      }

      try {
        const todoArgs = this.buildTodoArgs({
          title: item.title,
          notes: item.notes,
          when: item.when,
          deadline: item.deadline,
          tags: item.tags,
          list_id: projectId,
          completed: item.completed,
          canceled: item.canceled,
          checklist_items: item.checklist?.map(c => c.title)
        });
        await executeAppleScriptFile('create-todo', todoArgs);
        results.success.push({ title: item.title });
      } catch (error) {
        results.failed.push({
          title: item.title,
          reason: error instanceof Error ? error.message : 'Unknown error'
        });
      }
    }

    return JSON.stringify({
      success: true,
      project: {
        id: projectId,
        title: params.title
      },
      items: {
        total: params.items.length,
        succeeded: results.success.length,
        failed: results.failed.length,
        skipped: results.skipped.length
      },
      created: results.success.map(s => s.title),
      failed: results.failed,
      skipped: results.skipped
    }, null, 2);
  }

  /**
   * Update an existing to-do using AppleScript
   */
  async updateTodo(params: UpdateTodoJSONParams): Promise<string> {
    const args = this.buildUpdateTodoArgs(params);
    await executeAppleScriptFile('update-todo', args);
    return `Updated to-do: "${params.title || params.id}"`;
  }

  /**
   * Update an existing project using AppleScript
   */
  async updateProject(params: UpdateProjectJSONParams): Promise<string> {
    const args = this.buildUpdateProjectArgs(params);
    await executeAppleScriptFile('update-project', args);
    return `Updated project: "${params.title || params.id}"`;
  }

  /**
   * Add items to an existing project
   * Returns structured JSON with detailed success/failure information
   */
  async addItemsToProject(params: AddItemsToProjectParams): Promise<string> {
    const results = {
      success: [] as { title: string; type: string }[],
      failed: [] as { title: string; type: string; reason: string }[],
      skipped: [] as { title: string; type: string; reason: string }[]
    };

    for (const item of params.items) {
      if (item.type === 'heading') {
        results.skipped.push({
          title: item.title,
          type: 'heading',
          reason: 'Headings cannot be added via AppleScript (only during project creation)'
        });
        continue;
      }

      try {
        const todoArgs = this.buildTodoArgs({
          title: item.title,
          notes: item.notes,
          when: item.when,
          deadline: item.deadline,
          tags: item.tags,
          list_id: params.id,
          completed: item.completed,
          canceled: item.canceled,
          checklist_items: item.checklist?.map(c => c.title)
        });
        await executeAppleScriptFile('create-todo', todoArgs);
        results.success.push({
          title: item.title,
          type: 'todo'
        });
      } catch (error) {
        results.failed.push({
          title: item.title,
          type: 'todo',
          reason: error instanceof Error ? error.message : 'Unknown error'
        });
      }
    }

    // Build structured response
    const response = {
      projectId: params.id,
      summary: {
        total: params.items.length,
        succeeded: results.success.length,
        failed: results.failed.length,
        skipped: results.skipped.length
      },
      success: results.success.map(s => s.title),
      failed: results.failed,
      skipped: results.skipped
    };

    return JSON.stringify(response, null, 2);
  }

  /**
   * Build arguments array for create-todo AppleScript
   * Order: title, notes, when, deadline, tags, list, listId, heading, completed, canceled, checklistItems
   */
  private buildTodoArgs(params: AddTodoParams): string[] {
    return [
      params.title || '',
      params.notes || '',
      params.when || '',
      params.deadline || '',
      params.tags?.join(',') || '',
      params.list || '',
      params.list_id || '',
      params.heading || '',
      params.completed ? 'true' : 'false',
      params.canceled ? 'true' : 'false',
      params.checklist_items?.join('\n') || ''
    ];
  }

  /**
   * Build arguments array for update-todo AppleScript
   * Order: id, title, notes, when, deadline, tags, list, listId, completed, canceled
   */
  private buildUpdateTodoArgs(params: UpdateTodoJSONParams): string[] {
    return [
      params.id,
      params.title || '',
      params.notes || '',
      params.when || '',
      params.deadline || '',
      params.tags?.join(',') || '',
      params.list || '',
      params.list_id || '',
      params.completed !== undefined ? String(params.completed) : '',
      params.canceled !== undefined ? String(params.canceled) : ''
    ];
  }

  /**
   * Build arguments array for create-project AppleScript
   * Order: title, notes, when, deadline, tags, areaId, area, completed, canceled
   */
  private buildProjectArgs(params: AddProjectParams): string[] {
    return [
      params.title || '',
      params.notes || '',
      params.when || '',
      params.deadline || '',
      params.tags?.join(',') || '',
      params.area_id || '',
      params.area || '',
      params.completed ? 'true' : 'false',
      params.canceled ? 'true' : 'false'
    ];
  }

  /**
   * Build arguments array for update-project AppleScript
   * Order: id, title, notes, when, deadline, tags, areaId, area, completed, canceled
   */
  private buildUpdateProjectArgs(params: UpdateProjectJSONParams): string[] {
    return [
      params.id,
      params.title || '',
      params.notes || '',
      params.when || '',
      params.deadline || '',
      params.tags?.join(',') || '',
      params.area_id || '',
      params.area || '',
      params.completed !== undefined ? String(params.completed) : '',
      params.canceled !== undefined ? String(params.canceled) : ''
    ];
  }
}

// Export singleton instance
export const jsonBuilder = new ThingsJSONBuilder();
