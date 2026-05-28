import { describe, it, expect } from '@jest/globals';
import { learningTools } from '../../../src/tools/learning.js';

describe('Learning tools', () => {
  describe('Tool definitions', () => {
    it('should export all learning tools', () => {
      expect(learningTools).toHaveLength(6);
      const toolNames = learningTools.map(t => t.name);
      expect(toolNames).toContain('things_list_patterns');
      expect(toolNames).toContain('things_suggest_for_task');
      expect(toolNames).toContain('things_log_correction');
      expect(toolNames).toContain('things_update_pattern');
      expect(toolNames).toContain('things_remove_pattern');
      expect(toolNames).toContain('things_learn_batch');
    });
  });

  describe('things_list_patterns', () => {
    const tool = learningTools.find(t => t.name === 'things_list_patterns')!;

    it('should have proper description', () => {
      expect(tool.description).toContain('patterns');
    });

    it('should have no required parameters', () => {
      expect(tool.inputSchema.required).toBeUndefined();
    });
  });

  describe('things_suggest_for_task', () => {
    const tool = learningTools.find(t => t.name === 'things_suggest_for_task')!;

    it('should have proper description', () => {
      expect(tool.description).toContain('suggestion');
      expect(tool.description).toContain('confidence');
    });

    it('should require title parameter', () => {
      expect(tool.inputSchema.required).toContain('title');
    });

    it('should have title property with correct type', () => {
      expect(tool.inputSchema.properties.title).toBeDefined();
      expect(tool.inputSchema.properties.title.type).toBe('string');
    });
  });

  describe('things_log_correction', () => {
    const tool = learningTools.find(t => t.name === 'things_log_correction')!;

    it('should have proper description', () => {
      expect(tool.description).toContain('correction');
    });

    it('should require original_title and final_title', () => {
      expect(tool.inputSchema.required).toContain('original_title');
      expect(tool.inputSchema.required).toContain('final_title');
    });

    it('should have optional title_accepted and project_accepted', () => {
      expect(tool.inputSchema.properties.title_accepted).toBeDefined();
      expect(tool.inputSchema.properties.project_accepted).toBeDefined();
      // Optional means not in required array
      expect(tool.inputSchema.required).not.toContain('title_accepted');
      expect(tool.inputSchema.required).not.toContain('project_accepted');
    });
  });

  describe('things_update_pattern', () => {
    const tool = learningTools.find(t => t.name === 'things_update_pattern')!;

    it('should have proper description', () => {
      expect(tool.description).toContain('confidence');
    });

    it('should require pattern_type and key', () => {
      expect(tool.inputSchema.required).toContain('pattern_type');
      expect(tool.inputSchema.required).toContain('key');
    });

    it('should have pattern_type with enum values', () => {
      expect(tool.inputSchema.properties.pattern_type).toBeDefined();
      expect(tool.inputSchema.properties.pattern_type.enum).toContain('title_transform');
      expect(tool.inputSchema.properties.pattern_type.enum).toContain('project_hint');
      expect(tool.inputSchema.properties.pattern_type.enum).toContain('exact_override');
    });
  });

  describe('things_remove_pattern', () => {
    const tool = learningTools.find(t => t.name === 'things_remove_pattern')!;

    it('should have proper description', () => {
      expect(tool.description.toLowerCase()).toContain('remove');
      expect(tool.description.toLowerCase()).toContain('pattern');
    });

    it('should require pattern_type and key', () => {
      expect(tool.inputSchema.required).toContain('pattern_type');
      expect(tool.inputSchema.required).toContain('key');
    });
  });

  describe('things_learn_batch', () => {
    const tool = learningTools.find(t => t.name === 'things_learn_batch')!;

    it('should have proper description', () => {
      expect(tool.description).toContain('batch');
      expect(tool.description).toContain('decisions');
    });

    it('should require decisions parameter', () => {
      expect(tool.inputSchema.required).toContain('decisions');
    });

    it('should have decisions as array type', () => {
      expect(tool.inputSchema.properties.decisions).toBeDefined();
      expect(tool.inputSchema.properties.decisions.type).toBe('array');
    });
  });
});
