const path = require('path');

describe('proposal-validator', () => {
  let ProposalValidator;

  beforeEach(() => {
    jest.resetModules();
    ProposalValidator = require(path.join(process.cwd(), 'web/demo/js/proposal-validator.js'));
  });

  describe('checkProfanity', () => {
    it('detects profanity in text', () => {
      const result = ProposalValidator.checkProfanity('This is some damn text');
      expect(result.hasProfanity).toBe(true);
      expect(result.matches).toContain('damn');
    });

    it('returns clean for normal text', () => {
      const result = ProposalValidator.checkProfanity('This is a clean sentence');
      expect(result.hasProfanity).toBe(false);
      expect(result.matches).toHaveLength(0);
    });

    it('handles case-insensitive matching', () => {
      const result = ProposalValidator.checkProfanity('DAMN and Damn');
      expect(result.hasProfanity).toBe(true);
    });

    it('handles null/undefined input', () => {
      expect(ProposalValidator.checkProfanity(null).hasProfanity).toBe(false);
      expect(ProposalValidator.checkProfanity(undefined).hasProfanity).toBe(false);
    });

    it('matches whole words only', () => {
      const result = ProposalValidator.checkProfanity('classic class assignment');
      // Should not match "ass" within "class" or "assignment"
      expect(result.hasProfanity).toBe(false);
    });
  });

  describe('validateSchema', () => {
    it('validates correct proposal structure', () => {
      const validProposal = {
        choice_text: 'Explore the mysterious cave',
        content: {
          text: 'You venture into the darkness...',
          return_path: 'campfire'
        },
        metadata: {
          confidence_score: 0.85,
          thematic_fit: 0.9
        }
      };

      const result = ProposalValidator.validateSchema(validProposal);
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    it('fails for missing required fields', () => {
      const invalidProposal = {
        choice_text: 'Test'
      };

      const result = ProposalValidator.validateSchema(invalidProposal);
      expect(result.valid).toBe(false);
      expect(result.errors.length).toBeGreaterThan(0);
    });

    it('fails for wrong types', () => {
      const invalidProposal = {
        choice_text: 123, // should be string
        content: {
          text: 'Valid text',
          return_path: 'campfire'
        }
      };

      const result = ProposalValidator.validateSchema(invalidProposal);
      expect(result.valid).toBe(false);
      expect(result.errors).toContain('Field choice_text must be string, got number');
    });

    it('warns for out-of-range confidence scores', () => {
      const proposal = {
        choice_text: 'Test',
        content: {
          text: 'Test content',
          return_path: 'campfire'
        },
        metadata: {
          confidence_score: 1.5 // Out of range
        }
      };

      const result = ProposalValidator.validateSchema(proposal);
      expect(result.warnings.length).toBeGreaterThan(0);
    });
  });

  describe('validateReturnPath', () => {
    it('passes for valid return paths', () => {
      const proposal = {
        content: {
          return_path: 'campfire'
        }
      };
      const validPaths = ['campfire', 'pines', 'return_with_supplies'];

      const result = ProposalValidator.validateReturnPath(proposal, validPaths);
      expect(result.valid).toBe(true);
    });

    it('warns for unrecognized return paths', () => {
      const proposal = {
        content: {
          return_path: 'unknown_knot'
        }
      };
      const validPaths = ['campfire', 'pines'];

      const result = ProposalValidator.validateReturnPath(proposal, validPaths);
      expect(result.warnings.length).toBeGreaterThan(0);
    });

    it('fails for ending paths', () => {
      const proposal = {
        content: {
          return_path: 'rescue_end'
        }
      };

      const result = ProposalValidator.validateReturnPath(proposal, []);
      expect(result.valid).toBe(false);
    });
  });

  describe('quickValidate', () => {
    it('returns valid for good proposals', () => {
      const proposal = {
        choice_text: 'Test choice',
        content: {
          text: 'Test content text that is long enough',
          return_path: 'campfire'
        }
      };

      const result = ProposalValidator.quickValidate(proposal);
      expect(result.valid).toBe(true);
    });

    it('sanitizes profanity in choice text', () => {
      const proposal = {
        choice_text: 'A damn good choice',
        content: {
          text: 'Clean content',
          return_path: 'campfire'
        }
      };

      const result = ProposalValidator.quickValidate(proposal);
      expect(result.valid).toBe(true);
      expect(result.sanitizedProposal.choice_text).toContain('[expletive]');
    });

    it('sanitizes profanity in content', () => {
      const proposal = {
        choice_text: 'Clean choice',
        content: {
          text: 'Content with damn word',
          return_path: 'campfire'
        }
      };

      const result = ProposalValidator.quickValidate(proposal);
      expect(result.valid).toBe(true);
      expect(result.sanitizedProposal.content.text).toContain('[expletive]');
    });

    it('fails on explicit content', () => {
      const proposal = {
        choice_text: 'Look closer',
        content: {
          text: 'The chamber was a torture chamber filled with gore.',
          return_path: 'campfire'
        }
      };

      const result = ProposalValidator.quickValidate(proposal);
      expect(result.valid).toBe(false);
      expect(result.reason).toContain('Explicit content');
    });

    it('fails on ending return path', () => {
      const proposal = {
        choice_text: 'End it',
        content: {
          text: 'The story ends here.',
          return_path: 'rescue_end'
        }
      };

      const result = ProposalValidator.quickValidate(proposal, { validReturnPaths: [] });
      expect(result.valid).toBe(false);
    });
  });

  describe('validateProposal (full)', () => {
    it('performs complete validation', () => {
      const validProposal = {
        choice_text: 'Enter the cave',
        content: {
          branch_type: 'narrative_delta',
          text: 'You step into the darkness, feeling the cool air wash over you. The cave walls glisten with moisture.',
          return_path: 'campfire'
        },
        metadata: {
          confidence_score: 0.85,
          thematic_fit: 0.9
        }
      };

      const result = ProposalValidator.validateProposal(validProposal, {
        validReturnPaths: ['campfire', 'pines']
      });

      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
      expect(result.report).toBeTruthy();
    });

    it('reports sanitization transforms', () => {
      const proposal = {
        choice_text: 'A damn good choice',
        content: {
          branch_type: 'narrative_delta',
          text: 'Line 1\n\n\nLine 2 with <b>markup</b>.',
          return_path: 'campfire'
        },
        metadata: {
          confidence_score: 0.7
        }
      };

      const result = ProposalValidator.validateProposal(proposal, {
        validReturnPaths: ['campfire']
      });

      expect(result.valid).toBe(true);
      expect(result.report.status).toBe('rejected_with_sanitization');
      expect(result.report.rules.some(rule => rule.result === 'sanitized')).toBe(true);
      expect(result.sanitizedProposal.content.text).not.toContain('<b>');
      expect(result.sanitizedProposal.choice_text).toContain('[expletive]');
    });
  });
});
