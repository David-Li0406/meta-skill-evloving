import { describe, it, expect } from '@jest/globals';
import { statsTools } from '../../../src/tools/stats.js';

describe('Stats tools', () => {
  describe('Tool definitions', () => {
    it('should export correct stats tools', () => {
      expect(statsTools).toHaveLength(1);
      expect(statsTools[0].name).toBe('things_get_stats');
    });

    it('should have proper description', () => {
      const statsTool = statsTools[0];
      expect(statsTool.description).toContain('statistics');
      expect(statsTool.description).toContain('inbox');
      expect(statsTool.description).toContain('today');
    });

    it('should have proper schema', () => {
      const statsTool = statsTools[0];
      expect(statsTool.inputSchema.type).toBe('object');
    });

    it('should have no required parameters', () => {
      const statsTool = statsTools[0];
      // Empty schema - no parameters needed
      expect(statsTool.inputSchema.required).toBeUndefined();
    });

    it('should have empty properties (no params needed)', () => {
      const statsTool = statsTools[0];
      const propNames = Object.keys(statsTool.inputSchema.properties);
      expect(propNames).toHaveLength(0);
    });
  });
});
