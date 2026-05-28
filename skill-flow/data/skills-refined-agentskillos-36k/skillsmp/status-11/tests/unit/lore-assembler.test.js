const path = require('path');

describe('lore-assembler', () => {
  let LoreAssembler;

  beforeEach(() => {
    jest.resetModules();
    LoreAssembler = require(path.join(process.cwd(), 'web/demo/js/lore-assembler.js'));
    LoreAssembler.clearHistory();
  });

  describe('extractVariables', () => {
    it('extracts variables from story variablesState', () => {
      const mockStory = {
        variablesState: {
          campfire_log: true,
          courage: 2,
          caution: 1,
          met_stranger: false,
          found_artifact: true,
          wolves_spotted: true,
          pocket_compass: false
        }
      };

      const result = LoreAssembler.extractVariables(mockStory);

      expect(result.campfire_log).toBe(true);
      expect(result.courage).toBe(2);
      expect(result.caution).toBe(1);
      expect(result.met_stranger).toBe(false);
      expect(result.found_artifact).toBe(true);
      expect(result.wolves_spotted).toBe(true);
      expect(result.pocket_compass).toBe(false);
    });

    it('returns empty object for null story', () => {
      const result = LoreAssembler.extractVariables(null);
      expect(result).toEqual({});
    });

    it('handles missing variables gracefully', () => {
      const mockStory = {
        variablesState: {
          courage: 1
        }
      };

      const result = LoreAssembler.extractVariables(mockStory);
      expect(result.courage).toBe(1);
      expect(result.campfire_log).toBeUndefined();
    });
  });

  describe('recordChoice and getChoiceHistory', () => {
    it('records choices in history', () => {
      LoreAssembler.recordChoice('First choice');
      LoreAssembler.recordChoice('Second choice');

      const history = LoreAssembler.getChoiceHistory();
      expect(history).toHaveLength(2);
      expect(history[0].text).toBe('First choice');
      expect(history[1].text).toBe('Second choice');
    });

    it('limits history to MAX_CHOICE_HISTORY', () => {
      for (let i = 0; i < 10; i++) {
        LoreAssembler.recordChoice(`Choice ${i}`);
      }

      const history = LoreAssembler.getChoiceHistory();
      expect(history).toHaveLength(LoreAssembler.MAX_CHOICE_HISTORY);
      expect(history[0].text).toBe('Choice 5'); // Oldest should be removed
    });

    it('clearHistory clears all history', () => {
      LoreAssembler.recordChoice('Test choice');
      LoreAssembler.clearHistory();

      const history = LoreAssembler.getChoiceHistory();
      expect(history).toHaveLength(0);
    });
  });

  describe('determineContextType', () => {
    it('identifies dialogue scenes', () => {
      expect(LoreAssembler.determineContextType('stranger_dialogue', {})).toBe('dialogue');
      expect(LoreAssembler.determineContextType('escorted_return', {})).toBe('dialogue');
    });

    it('identifies tension scenes', () => {
      expect(LoreAssembler.determineContextType('tense_return', {})).toBe('tension');
      expect(LoreAssembler.determineContextType('any_scene', { wolves_spotted: true })).toBe('tension');
    });

    it('identifies discovery scenes', () => {
      expect(LoreAssembler.determineContextType('watchtower', {})).toBe('discovery');
      expect(LoreAssembler.determineContextType('artifact_mystery', {})).toBe('discovery');
    });

    it('defaults to exploration', () => {
      expect(LoreAssembler.determineContextType('pines', {})).toBe('exploration');
      expect(LoreAssembler.determineContextType('unknown_scene', {})).toBe('exploration');
    });
  });

  describe('getValidReturnPaths', () => {
    it('returns valid return paths excluding current knot', () => {
      const paths = LoreAssembler.getValidReturnPaths('pines');

      expect(paths).toContain('return_with_supplies');
      expect(paths).toContain('campfire');
      expect(paths).not.toContain('pines'); // Excludes current
      expect(paths).not.toContain('rescue_end'); // Excludes endings
    });

    it('excludes ending paths', () => {
      const paths = LoreAssembler.getValidReturnPaths('start');

      expect(paths).not.toContain('rescue_end');
      expect(paths).not.toContain('waiting_end');
      expect(paths).not.toContain('quiet_end');
    });
  });

  describe('assembleLORE', () => {
    it('assembles complete LORE context', () => {
      const mockStory = {
        variablesState: {
          campfire_log: true,
          courage: 3,
          caution: 1,
          met_stranger: true,
          found_artifact: false,
          wolves_spotted: false,
          pocket_compass: true
        },
        state: {
          currentPathString: 'pines.something'
        }
      };

      LoreAssembler.recordChoice('Head toward the pines');

      const lore = LoreAssembler.assembleLORE(mockStory);

      expect(lore.player_state.courage).toBe(3);
      expect(lore.player_state.caution).toBe(1);
      expect(lore.player_state.inventory).toContain('flint and tinder');
      expect(lore.player_state.inventory).toContain('pocket compass');
      expect(lore.game_state.current_scene).toBe('pines');
      expect(lore.game_state.met_stranger).toBe(true);
      expect(lore.narrative_context.recent_choices).toContain('Head toward the pines');
      expect(lore.context_hash).toBeDefined();
      expect(lore.capture_timestamp).toBeDefined();
    });
  });
});
