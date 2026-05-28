import { describe, it, expect } from '@jest/globals';
import { searchTools } from '../../../src/tools/search.js';

describe('Search tools', () => {
  describe('Tool definitions', () => {
    it('should export correct search tools', () => {
      expect(searchTools).toHaveLength(1);
      expect(searchTools[0].name).toBe('things_search');
    });

    it('should have proper description', () => {
      const searchTool = searchTools[0];
      expect(searchTool.description).toContain('Search');
      expect(searchTool.description).toContain('to-dos');
    });

    it('should have proper schema', () => {
      const searchTool = searchTools[0];
      expect(searchTool.inputSchema.type).toBe('object');
    });

    it('should have all expected properties', () => {
      const searchTool = searchTools[0];
      const props = searchTool.inputSchema.properties;

      expect(props.query).toBeDefined();
      expect(props.list).toBeDefined();
      expect(props.tag).toBeDefined();
      expect(props.has_url).toBeDefined();
      expect(props.max_results).toBeDefined();
    });

    it('should have no required fields', () => {
      const searchTool = searchTools[0];
      // All fields are optional in SearchTodosSchema
      expect(searchTool.inputSchema.required).toBeUndefined();
    });

    it('should have proper list enum values', () => {
      const searchTool = searchTools[0];
      const listProp = searchTool.inputSchema.properties.list;

      // Check enum values are present
      expect(listProp.enum || listProp.anyOf).toBeDefined();
    });
  });
});
