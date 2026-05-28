import { describe, it, expect } from '@jest/globals';
import { bulkTools } from '../../../src/tools/bulk.js';

describe('Bulk tools', () => {
  describe('Tool definitions', () => {
    it('should export correct bulk tools', () => {
      expect(bulkTools).toHaveLength(1);
      expect(bulkTools[0].name).toBe('things_bulk_update');
    });

    it('should have proper description', () => {
      const bulkTool = bulkTools[0];
      expect(bulkTool.description).toContain('Update multiple');
      expect(bulkTool.description).toContain('batch');
    });

    it('should have proper schema', () => {
      const bulkTool = bulkTools[0];
      expect(bulkTool.inputSchema.type).toBe('object');
      expect(bulkTool.inputSchema.required).toContain('ids');
      expect(bulkTool.inputSchema.required).toContain('updates');
    });

    it('should have ids as array property', () => {
      const bulkTool = bulkTools[0];
      const props = bulkTool.inputSchema.properties;
      expect(props.ids.type).toBe('array');
      expect(props.ids.items.type).toBe('string');
    });

    it('should have updates as object property', () => {
      const bulkTool = bulkTools[0];
      const props = bulkTool.inputSchema.properties;
      expect(props.updates.type).toBe('object');
      expect(props.updates.properties).toBeDefined();
    });

    it('should have update fields for scheduling', () => {
      const bulkTool = bulkTools[0];
      const updateProps = bulkTool.inputSchema.properties.updates.properties;
      expect(updateProps.when).toBeDefined();
      expect(updateProps.deadline).toBeDefined();
    });

    it('should have update fields for tags', () => {
      const bulkTool = bulkTools[0];
      const updateProps = bulkTool.inputSchema.properties.updates.properties;
      expect(updateProps.tags_add).toBeDefined();
      expect(updateProps.tags_remove).toBeDefined();
      expect(updateProps.tags_add.type).toBe('array');
      expect(updateProps.tags_remove.type).toBe('array');
    });

    it('should have update fields for list assignment', () => {
      const bulkTool = bulkTools[0];
      const updateProps = bulkTool.inputSchema.properties.updates.properties;
      expect(updateProps.list_id).toBeDefined();
      expect(updateProps.list).toBeDefined();
    });
  });
});
