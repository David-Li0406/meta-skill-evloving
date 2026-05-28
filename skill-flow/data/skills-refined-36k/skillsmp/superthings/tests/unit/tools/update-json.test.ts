import { describe, it, expect } from '@jest/globals';
import { updateJSONTools } from '../../../src/tools/update-json.js';

describe('Update JSON tools', () => {
  describe('Tool definitions', () => {
    it('should export correct update tools', () => {
      expect(updateJSONTools).toHaveLength(3);
      expect(updateJSONTools[0].name).toBe('things_update_todo');
      expect(updateJSONTools[1].name).toBe('things_update_project');
      expect(updateJSONTools[2].name).toBe('things_add_items_to_project');
    });

    it('should have proper schemas for update_todo', () => {
      const todoTool = updateJSONTools[0];
      expect(todoTool.description).toContain('Update');
      expect(todoTool.description).toContain('to-do');
      expect(todoTool.inputSchema.type).toBe('object');
      expect(todoTool.inputSchema.properties.title).toBeDefined();
      expect(todoTool.inputSchema.properties.id).toBeDefined();
      expect(todoTool.inputSchema.required).toContain('title');
      expect(todoTool.inputSchema.required).toContain('id');
    });

    it('should have proper schemas for update_project', () => {
      const projectTool = updateJSONTools[1];
      expect(projectTool.description).toContain('Update');
      expect(projectTool.description).toContain('project');
      expect(projectTool.inputSchema.type).toBe('object');
      expect(projectTool.inputSchema.properties.title).toBeDefined();
      expect(projectTool.inputSchema.properties.id).toBeDefined();
      expect(projectTool.inputSchema.required).toContain('title');
      expect(projectTool.inputSchema.required).toContain('id');
    });

    it('should have proper schemas for add_items_to_project', () => {
      const addItemsTool = updateJSONTools[2];
      expect(addItemsTool.description).toContain('Add');
      expect(addItemsTool.description).toContain('project');
      expect(addItemsTool.inputSchema.type).toBe('object');
      expect(addItemsTool.inputSchema.properties.id).toBeDefined();
      expect(addItemsTool.inputSchema.properties.items).toBeDefined();
      expect(addItemsTool.inputSchema.required).toContain('id');
      expect(addItemsTool.inputSchema.required).toContain('items');
    });

    it('should have all expected properties for update_todo', () => {
      const todoTool = updateJSONTools[0];
      const props = todoTool.inputSchema.properties;

      expect(props.id).toBeDefined();
      expect(props.title).toBeDefined();
      expect(props.notes).toBeDefined();
      expect(props.when).toBeDefined();
      expect(props.deadline).toBeDefined();
      expect(props.tags).toBeDefined();
      expect(props.checklist_items).toBeDefined();
      expect(props.list_id).toBeDefined();
      expect(props.list).toBeDefined();
      expect(props.heading).toBeDefined();
      expect(props.completed).toBeDefined();
      expect(props.canceled).toBeDefined();
    });

    it('should have all expected properties for update_project', () => {
      const projectTool = updateJSONTools[1];
      const props = projectTool.inputSchema.properties;

      expect(props.id).toBeDefined();
      expect(props.title).toBeDefined();
      expect(props.notes).toBeDefined();
      expect(props.when).toBeDefined();
      expect(props.deadline).toBeDefined();
      expect(props.tags).toBeDefined();
      expect(props.area_id).toBeDefined();
      expect(props.area).toBeDefined();
      expect(props.items).toBeDefined();
      expect(props.completed).toBeDefined();
      expect(props.canceled).toBeDefined();
    });

    it('should have all expected properties for add_items_to_project', () => {
      const addItemsTool = updateJSONTools[2];
      const props = addItemsTool.inputSchema.properties;

      expect(props.id).toBeDefined();
      expect(props.items).toBeDefined();
    });
  });
});
