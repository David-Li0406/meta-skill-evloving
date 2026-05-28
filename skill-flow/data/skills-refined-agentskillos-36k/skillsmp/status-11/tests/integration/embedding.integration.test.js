/** @jest-environment ./tests/helpers/node-no-webstorage-environment.js */

// Optional integration test. Requires network + model download. Skip in CI by default.
// Set EMBED_NODE=1 to force Node fallback (no Worker) or INTEGRATION_EMBEDDING=1 for browser path.
const EmbeddingService = require('../../web/demo/js/embedding-service.js');

const shouldRun = process.env.INTEGRATION_EMBEDDING === '1' || process.env.EMBED_NODE === '1';
const describeFn = shouldRun ? describe : describe.skip;

function requireFlag() {
  if (!shouldRun) {
    throw new Error('Set EMBED_NODE=1 (Node fallback) or INTEGRATION_EMBEDDING=1 to run this integration test');
  }
}

// Note: This uses the real embedding service. It will download the model via CDN
// and may take several seconds on first run. Intended for manual verification.
describeFn('EmbeddingService integration (real model)', () => {
  jest.setTimeout(30000); // allow model download

  test('happy vs joyful similarity is reasonably high', async () => {
    requireFlag();
    const { spawnSync } = require('child_process');
    const path = require('path');
    const script = `
      (async () => {
        const svc = require(${JSON.stringify(path.resolve(__dirname, '../../web/demo/js/embedding-service.js'))});
        const a = await svc.embed('I feel very happy and joyful today.');
        const b = await svc.embed('What a joyful, delightful feeling of happiness!');
        if (!a || !b) {
          console.error('embed returned null', { aLen: a && a.length, bLen: b && b.length, err: svc._nodeExtractorError && svc._nodeExtractorError() });
          process.exit(2);
        }
        const sim = svc.similarity(a, b);
        console.log('similarity', sim);
        if (Number(sim) > 0.5) process.exit(0);
        process.exit(3);
      })().catch((err) => {
        console.error(err);
        process.exit(1);
      });
    `;
    const result = spawnSync(process.execPath, ['-e', script], {
      env: { ...process.env, EMBED_NODE: '1', NODE_OPTIONS: '' },
      encoding: 'utf8',
    });
    if (result.status !== 0) {
      const err = EmbeddingService._nodeExtractorError && EmbeddingService._nodeExtractorError();
      const msg = `Child embedding run failed (status ${result.status}). stdout: ${result.stdout}\nstderr: ${result.stderr}\nflags: EMBED_NODE=${process.env.EMBED_NODE}, INTEGRATION_EMBEDDING=${process.env.INTEGRATION_EMBEDDING}${err ? `; extractor error: ${err.message || err}` : ''}`;
      throw new Error(msg);
    }
  });
});
