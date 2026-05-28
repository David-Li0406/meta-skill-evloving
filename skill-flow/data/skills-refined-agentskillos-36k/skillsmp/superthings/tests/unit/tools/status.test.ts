import { describe, it, expect } from '@jest/globals';
import { statusTools } from '../../../src/tools/status.js';

describe('Status tools', () => {
  describe('Tool definitions', () => {
    it('should export correct status tools', () => {
      expect(statusTools).toHaveLength(2);
      expect(statusTools[0].name).toBe('things_complete_todo');
      expect(statusTools[1].name).toBe('things_cancel_todo');
    });

    it('should have proper description for complete_todo', () => {
      const completeTool = statusTools[0];
      expect(completeTool.description).toContain('complete');
      expect(completeTool.description).toContain('Logbook');
    });

    it('should have proper description for cancel_todo', () => {
      const cancelTool = statusTools[1];
      expect(cancelTool.description).toContain('Cancel');
    });

    it('should have proper schema for complete_todo', () => {
      const completeTool = statusTools[0];
      expect(completeTool.inputSchema.type).toBe('object');
      expect(completeTool.inputSchema.properties.id).toBeDefined();
      expect(completeTool.inputSchema.required).toContain('id');
    });

    it('should have proper schema for cancel_todo', () => {
      const cancelTool = statusTools[1];
      expect(cancelTool.inputSchema.type).toBe('object');
      expect(cancelTool.inputSchema.properties.id).toBeDefined();
      expect(cancelTool.inputSchema.required).toContain('id');
    });

    it('should require only id field', () => {
      // Both tools should only have id as a property
      statusTools.forEach(tool => {
        const propNames = Object.keys(tool.inputSchema.properties);
        expect(propNames).toEqual(['id']);
      });
    });
  });
});
