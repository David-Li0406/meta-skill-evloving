const EmbeddingService = require('../../web/demo/js/embedding-service.js');

describe('EmbeddingService.embed', () => {
  test('returns null when text is null/invalid', async () => {
    const result = await EmbeddingService.embed(null);
    expect(result).toBeNull();
  });

  test('resolves via mocked worker plumbing and caches results', async () => {
    // Mock a minimal Worker that immediately responds with a fixed embedding
    const fixedEmbedding = [0.1, 0.2, 0.3];
    const mockPostMessage = jest.fn();

    class MockWorker {
      constructor() {
        this.onmessage = null;
      }
      postMessage(msg) {
        mockPostMessage(msg);
        setTimeout(() => {
          if (this.onmessage) {
            this.onmessage({ data: { id: msg.id, embedding: fixedEmbedding } });
          }
        }, 0);
      }
    }

    // Install mocks
    const originalWorker = global.Worker;
    const originalBlob = global.Blob;
    const originalURL = global.URL;

    global.Worker = MockWorker;
    global.Blob = class Blob {
      constructor(parts) {
        this.parts = parts;
      }
    };
    global.URL = { createObjectURL: () => 'mock://worker' };

    // Re-require to ensure worker is (lazily) created with mocks
    jest.resetModules();
    const FreshService = require('../../web/demo/js/embedding-service.js');

    const result1 = await FreshService.embed('hello world');
    const result2 = await FreshService.embed('hello world');
    expect(mockPostMessage).toHaveBeenCalledTimes(1);
    expect(result1).toEqual(fixedEmbedding);
    expect(result2).toEqual(fixedEmbedding);

    // restore
    global.Worker = originalWorker;
    global.Blob = originalBlob;
    global.URL = originalURL;
  });
});
