const EmbeddingService = require('../../web/demo/js/embedding-service.js');

describe('EmbeddingService.similarity', () => {
  test('happy vs joyful > 0.7', () => {
    // Craft vectors with high cosine similarity (~0.96)
    const happy = [0.9, 0.3, 0.1, 0.0];
    const joyful = [0.88, 0.32, 0.05, 0.02];
    const sim = EmbeddingService.similarity(happy, joyful);
    expect(sim).toBeGreaterThan(0.7);
  });

  test('happy vs database < 0.4', () => {
    // Craft vectors with low cosine similarity (~0.23)
    const happy = [0.9, 0.3, 0.1, 0.0];
    const database = [-0.2, 0.05, 0.4, -0.1];
    const sim = EmbeddingService.similarity(happy, database);
    expect(sim).toBeLessThan(0.4);
  });

  test('handles invalid vectors by returning 0', () => {
    expect(EmbeddingService.similarity([], [1])).toBe(0);
    expect(EmbeddingService.similarity([1, 2], [1])).toBe(0);
    expect(EmbeddingService.similarity(['a'], [1])).toBe(0);
  });
});
