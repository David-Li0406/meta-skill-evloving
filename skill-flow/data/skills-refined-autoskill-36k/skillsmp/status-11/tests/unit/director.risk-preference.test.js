jest.mock('../../web/demo/js/player-preference', () => {
  return {
    getPreference: jest.fn(() => 0.5),
  };
});

const PlayerPreference = require('../../web/demo/js/player-preference');

// Expose mock to Director via global before requiring Director
beforeAll(() => {
  global.PlayerPreference = PlayerPreference;
});

afterAll(() => {
  delete global.PlayerPreference;
});

const Director = require('../../web/demo/js/director');

const proposal = {
  content: {
    text: 'Some branch text',
    branch_type: 'dialogue',
  },
  metadata: { confidence_score: 0.8 },
};

describe('Director computeRiskScore with player preference', () => {
  beforeEach(() => {
    PlayerPreference.getPreference.mockReset();
  });

  test('uses PlayerPreference.getPreference when available', () => {
    PlayerPreference.getPreference.mockReturnValue(0.9);
    const score = Director.computeRiskScore(proposal, {}, {});
    expect(score).toBeLessThan(0.27);
    expect(PlayerPreference.getPreference).toHaveBeenCalledWith('dialogue');
  });


  test('falls back to 0.5 when preference is NaN', () => {
    PlayerPreference.getPreference.mockReturnValue(NaN);
    const score = Director.computeRiskScore(proposal, {}, {});
    expect(PlayerPreference.getPreference).toHaveBeenCalled();
    expect(score).toBeGreaterThan(0.25); // higher risk because pref risk = 0.5 -> risk 0.5
  });

  test('accepts config override getPreference', () => {
    const cfg = {
      getPreference: () => 1.0,
      weights: { player_preference: 0.2 },
    };
    const score = Director.computeRiskScore(proposal, {}, cfg);
    expect(score).toBeLessThan(0.25);
  });
});
