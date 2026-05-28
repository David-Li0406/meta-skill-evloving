const path = require('path');

describe('prompt-engine', () => {
  let PromptEngine;

  beforeEach(() => {
    jest.resetModules();
    PromptEngine = require(path.join(process.cwd(), 'web/demo/js/prompt-engine.js'));
  });

  describe('formatTraits', () => {
    it('returns bold for high courage', () => {
      const traits = PromptEngine.formatTraits(5, 1);
      expect(traits.courage_trait).toBe('bold and adventurous');
    });

    it('returns cautious for high caution', () => {
      const traits = PromptEngine.formatTraits(1, 5);
      expect(traits.courage_trait).toBe('careful and methodical');
    });

    it('returns balanced for equal values', () => {
      const traits = PromptEngine.formatTraits(2, 2);
      expect(traits.courage_trait).toBe('balanced');
    });
  });

  describe('formatInventory', () => {
    it('formats items as comma-separated list', () => {
      const result = PromptEngine.formatInventory(['sword', 'shield', 'potion']);
      expect(result).toBe('sword, shield, potion');
    });

    it('returns "nothing notable" for empty inventory', () => {
      expect(PromptEngine.formatInventory([])).toBe('nothing notable');
      expect(PromptEngine.formatInventory(null)).toBe('nothing notable');
    });
  });

  describe('formatRecentContext', () => {
    it('formats single choice', () => {
      const result = PromptEngine.formatRecentContext(['Go north']);
      expect(result).toBe('The wanderer chose to: "Go north"');
    });

    it('formats multiple choices', () => {
      const result = PromptEngine.formatRecentContext(['Choice 1', 'Choice 2', 'Choice 3']);
      expect(result).toContain('Recent actions');
      expect(result).toContain('"Choice 1"');
    });

    it('handles empty choices', () => {
      const result = PromptEngine.formatRecentContext([]);
      expect(result).toContain('just arrived');
    });
  });

  describe('getSceneName', () => {
    it('returns human-readable names for known scenes', () => {
      expect(PromptEngine.getSceneName('pines')).toBe('deep in the pine forest');
      expect(PromptEngine.getSceneName('campfire')).toBe('by the campfire');
      expect(PromptEngine.getSceneName('watchtower')).toBe('at the old watchtower');
    });

    it('formats unknown scenes', () => {
      expect(PromptEngine.getSceneName('mystery_cave')).toBe('at mystery cave');
    });
  });

  describe('selectTemplateType', () => {
    it('selects dialogue for dialogue context', () => {
      const lore = { game_state: { context_type: 'dialogue' } };
      expect(PromptEngine.selectTemplateType(lore)).toBe('dialogue');
    });

    it('selects dialogue for tension context', () => {
      const lore = { game_state: { context_type: 'tension' } };
      expect(PromptEngine.selectTemplateType(lore)).toBe('dialogue');
    });

    it('selects exploration for discovery context', () => {
      const lore = { game_state: { context_type: 'discovery' } };
      expect(PromptEngine.selectTemplateType(lore)).toBe('exploration');
    });

    it('defaults to exploration', () => {
      const lore = { game_state: { context_type: 'exploration' } };
      expect(PromptEngine.selectTemplateType(lore)).toBe('exploration');
    });
  });

  describe('buildPrompt', () => {
    const mockLore = {
      player_state: {
        courage: 2,
        caution: 1,
        inventory: ['compass', 'torch']
      },
      game_state: {
        current_scene: 'pines',
        context_type: 'exploration',
        wolves_spotted: false,
        met_stranger: true
      },
      narrative_context: {
        recent_choices: ['Head toward the pines'],
        tone: 'mysterious'
      }
    };

    it('builds dialogue prompt', () => {
      const { systemPrompt, userPrompt } = PromptEngine.buildPrompt(
        mockLore,
        'dialogue',
        ['campfire', 'return_with_supplies']
      );

      expect(systemPrompt).toContain('creative narrative writer');
      expect(userPrompt).toContain('compass, torch');
      expect(userPrompt).toContain('campfire, return_with_supplies');
    });

    it('builds exploration prompt', () => {
      const { systemPrompt, userPrompt } = PromptEngine.buildPrompt(
        mockLore,
        'exploration',
        ['campfire', 'pines']
      );

      expect(systemPrompt).toContain('Output Format');
      expect(userPrompt).toContain('Player Context');
      expect(userPrompt).toContain('pine forest');
    });

    it('includes additional context for wolves_spotted', () => {
      const wolvesLore = {
        ...mockLore,
        game_state: { ...mockLore.game_state, wolves_spotted: true }
      };

      const { userPrompt } = PromptEngine.buildPrompt(
        wolvesLore,
        'dialogue',
        ['campfire']
      );

      expect(userPrompt).toContain('Wolves');
    });
  });

  describe('buildAutoPrompt', () => {
    it('auto-selects template type based on context', () => {
      const dialogueLore = {
        player_state: { courage: 1, caution: 1, inventory: [] },
        game_state: { current_scene: 'stranger_dialogue', context_type: 'dialogue' },
        narrative_context: { recent_choices: [], tone: 'mysterious' }
      };

      const result = PromptEngine.buildAutoPrompt(dialogueLore, ['campfire']);

      expect(result.templateType).toBe('dialogue');
      expect(result.systemPrompt).toBeDefined();
      expect(result.userPrompt).toBeDefined();
    });
  });
});
