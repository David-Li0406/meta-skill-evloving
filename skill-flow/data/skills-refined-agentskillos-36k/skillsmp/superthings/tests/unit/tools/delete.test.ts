import { describe, it, expect } from '@jest/globals';
import { deleteTools } from '../../../src/tools/delete.js';

describe('Delete tools', () => {
  describe('Tool definitions', () => {
    it('should export correct delete tools', () => {
      expect(deleteTools).toHaveLength(2);
      expect(deleteTools[0].name).toBe('things_delete_todo');
      expect(deleteTools[1].name).toBe('things_delete_project');
    });

    it('should have proper description for delete_todo', () => {
      const deleteTodoTool = deleteTools[0];
      expect(deleteTodoTool.description).toContain('Delete');
      expect(deleteTodoTool.description).toContain('Trash');
      expect(deleteTodoTool.description).toContain('confirm');
    });

    it('should have proper description for delete_project', () => {
      const deleteProjectTool = deleteTools[1];
      expect(deleteProjectTool.description).toContain('Delete');
      expect(deleteProjectTool.description).toContain('project');
      expect(deleteProjectTool.description).toContain('confirm');
    });

    it('should have proper schema for delete_todo', () => {
      const deleteTodoTool = deleteTools[0];
      expect(deleteTodoTool.inputSchema.type).toBe('object');
      expect(deleteTodoTool.inputSchema.properties.id).toBeDefined();
      expect(deleteTodoTool.inputSchema.properties.confirm).toBeDefined();
      expect(deleteTodoTool.inputSchema.required).toContain('id');
      expect(deleteTodoTool.inputSchema.required).toContain('confirm');
    });

    it('should have proper schema for delete_project', () => {
      const deleteProjectTool = deleteTools[1];
      expect(deleteProjectTool.inputSchema.type).toBe('object');
      expect(deleteProjectTool.inputSchema.properties.id).toBeDefined();
      expect(deleteProjectTool.inputSchema.properties.confirm).toBeDefined();
      expect(deleteProjectTool.inputSchema.required).toContain('id');
      expect(deleteProjectTool.inputSchema.required).toContain('confirm');
    });

    it('should require both id and confirm fields', () => {
      deleteTools.forEach(tool => {
        const propNames = Object.keys(tool.inputSchema.properties);
        expect(propNames).toHaveLength(2);
        expect(propNames).toContain('id');
        expect(propNames).toContain('confirm');
      });
    });
  });
});
