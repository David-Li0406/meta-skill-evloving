const PlayerPreference = require('../../web/demo/js/player-preference');

function clearStorage() {
  if (typeof localStorage !== 'undefined') {
    localStorage.clear();
  }
}

function corruptStorage() {
  if (typeof localStorage !== 'undefined') {
    localStorage.setItem('ge-hch.ai-preferences', '{ not valid json');
  }
}

describe('PlayerPreference', () => {
  beforeEach(() => {
    clearStorage();
  });

  test('cold start returns default 0.5', () => {
    expect(PlayerPreference.getPreference('dialogue')).toBe(0.5);
  });

  test('3 accepts + 1 reject yields > 0.6 for dialogue', () => {
    PlayerPreference.recordOutcome('dialogue', true);
    PlayerPreference.recordOutcome('dialogue', true);
    PlayerPreference.recordOutcome('dialogue', true);
    const score = PlayerPreference.recordOutcome('dialogue', false);
    expect(score).toBeGreaterThan(0.6); // 0.75 expected
    expect(PlayerPreference.getPreference('dialogue')).toBeGreaterThan(0.6);
  });

  test('records outcomes and updates preference', () => {
    const p1 = PlayerPreference.recordOutcome('lore', true);
    const p2 = PlayerPreference.recordOutcome('lore', false);
    expect(p1).toBeCloseTo(1.0);
    expect(p2).toBeCloseTo(0.5);
    expect(PlayerPreference.getPreference('lore')).toBeCloseTo(0.5);
  });

  test('persists across calls via localStorage', () => {
    PlayerPreference.recordOutcome('puzzle', true);
    // Re-require to simulate reload
    jest.resetModules();
    const Reloaded = require('../../web/demo/js/player-preference');
    expect(Reloaded.getPreference('puzzle')).toBeCloseTo(1.0);
  });

  test('clamps to 0-1 and handles bad inputs', () => {
    expect(PlayerPreference.getPreference('')).toBe(0.5);
    expect(PlayerPreference.recordOutcome('', true)).toBe(0.5);
    corruptStorage();
    expect(PlayerPreference.getPreference('combat')).toBe(0.5);
  });

  test('handles 100+ events quickly', () => {
    const start = performance.now();
    for (let i = 0; i < 100; i++) {
      PlayerPreference.recordOutcome('exploration', i % 2 === 0);
    }
    const elapsed = performance.now() - start;
    expect(PlayerPreference.getPreference('exploration')).toBeGreaterThanOrEqual(0);
    expect(elapsed).toBeLessThan(20);
  });
});
