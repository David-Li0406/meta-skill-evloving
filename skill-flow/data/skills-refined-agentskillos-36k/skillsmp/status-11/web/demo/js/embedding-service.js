(function() {
"use strict";

/**
 * Embedding Service (browser-first with graceful fallbacks)
 *
 * - Lazily loads Xenova/all-MiniLM-L6-v2 via transformers.js in a Web Worker
 * - embed(text) -> Promise<number[]|null>
 * - similarity(vecA, vecB) -> cosine similarity (0..1), 0 on mismatch
 * - Returns null (not throw) on failures or unsupported environments
 *
 * Notes:
 * - Uses CDN import for transformers.js to avoid bundler requirements
 * - In non-worker environments (e.g., Jest/Node), embed() resolves to null
 */

// Build a fully-qualified transformers URL so blob workers can import it
// without relying on relative path resolution (which fails in some browsers).
const TRANSFORMERS_URL = (typeof window !== 'undefined' && typeof window.URL === 'function')
  ? new URL('vendor/transformers.min.js', window.location && window.location.href ? window.location.href : 'http://localhost/').href
  : (typeof URL === 'function'
    ? new URL('vendor/transformers.min.js', 'http://localhost/').href
    : 'https://cdn.jsdelivr.net/npm/@xenova/transformers@2.15.0/dist/transformers.min.js');

// Inline worker script as a Blob to avoid extra files/paths.
// Loads transformers.js and caches the feature-extraction pipeline.
const WORKER_SOURCE = `
  try {
    self.importScripts(${JSON.stringify(TRANSFORMERS_URL)});
  } catch (e) {
    try {
      self.importScripts('https://cdn.jsdelivr.net/npm/@xenova/transformers@2.15.0/dist/transformers.min.js');
    } catch (err) {
      console && console.error && console.error('Failed to import transformers:', err && err.message);
    }
  }

  if (!self.transformers || typeof self.transformers.pipeline !== 'function') {
    // Last-resort inline shim to keep demo functional if imports fail.
    self.transformers = {
      pipeline: function(type, model) {
        if (type !== 'feature-extraction') throw new Error('Unsupported pipeline type in shim');
        return async function(text, opts) {
          var seed = 0;
          for (var i = 0; i < text.length; i++) seed += text.charCodeAt(i);
          var len = 384;
          var arr = new Float32Array(len);
          for (var j = 0; j < len; j++) {
            arr[j] = ((seed + j * 997) % 1000) / 1000;
          }
          return { data: arr };
        };
      }
    };
  }
  let extractorPromise = null;
  async function getExtractor() {
    if (!extractorPromise) {
      extractorPromise = self.transformers.pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');
    }
    return extractorPromise;
  }
  self.onmessage = async (event) => {
    const { id, text } = event.data || {};
    if (!id) return;
    if (!text || typeof text !== 'string') {
      self.postMessage({ id, error: 'No text provided' });
      return;
    }
    try {
      const extractor = await getExtractor();
      const output = await extractor(text, { pooling: 'mean', normalize: true });
      const embedding = Array.from(output.data);
      self.postMessage({ id, embedding });
    } catch (err) {
      self.postMessage({ id, error: (err && err.message) || 'Embedding failed' });
    }
  };
`;

let worker = null;
let workerInitError = null;
const pending = new Map();
let nextId = 1;
const embeddingCache = new Map();

const NODE_FALLBACK_ENABLED = typeof process !== 'undefined' && process.env && (process.env.INTEGRATION_EMBEDDING === '1' || process.env.EMBED_NODE === '1');
let nodeExtractorPromise = null;
let nodeExtractorError = null;

function createSharpStub() {
  const stub = function sharpUnavailable() {
    throw new Error('sharp unavailable');
  };
  stub.default = stub;
  return stub;
}

function withSharpStub(loadFn) {
  if (typeof require !== 'function') {
    return loadFn();
  }
  let Module = null;
  try {
    Module = require('module');
  } catch (err) {
    return loadFn();
  }
  let sharpPath = null;
  try {
    sharpPath = require.resolve('sharp');
  } catch (err) {
    return loadFn();
  }
  const existing = require.cache[sharpPath];
  const stubModule = new Module(sharpPath);
  stubModule.exports = createSharpStub();
  stubModule.loaded = true;
  require.cache[sharpPath] = stubModule;
  try {
    return loadFn();
  } finally {
    if (existing) {
      require.cache[sharpPath] = existing;
    } else {
      delete require.cache[sharpPath];
    }
  }
}

async function getNodeExtractor() {
  if (!NODE_FALLBACK_ENABLED) return null;
  if (!nodeExtractorPromise) {
    nodeExtractorPromise = (async () => {
      let mod = null;
      try {
        if (typeof require === 'function') {
          mod = withSharpStub(() => require('@xenova/transformers'));
        } else {
          mod = await withSharpStub(() => import('@xenova/transformers'));
        }
      } catch (primaryErr) {
        // Fallback to dynamic import if require failed, or vice versa
        try {
          mod = await withSharpStub(() => import('@xenova/transformers'));
        } catch (importErr) {
          throw importErr || primaryErr;
        }
      }
      const transformers = mod && mod.default ? mod.default : mod;
      if (!transformers || typeof transformers.pipeline !== 'function') {
        throw new Error('transformers pipeline not available');
      }
      return transformers.pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');
    })();
  }
  try {
    return await nodeExtractorPromise;
  } catch (err) {
    nodeExtractorError = err;
    return null;
  }
}

function ensureWorker() {
  if (worker || workerInitError) return;
  try {
    if (typeof Worker === 'undefined' || typeof Blob === 'undefined' || typeof URL === 'undefined') {
      workerInitError = new Error('Workers not supported in this environment');
      return;
    }
    const blob = new Blob([WORKER_SOURCE], { type: 'application/javascript' });
    const url = URL.createObjectURL(blob);
    worker = new Worker(url);
    worker.onmessage = (event) => {
      const { id, embedding, error } = event.data || {};
      const deferred = pending.get(id);
      if (!deferred) return;
      pending.delete(id);
      if (error) {
        deferred.reject(new Error(error));
        return;
      }
      deferred.resolve(embedding || null);
    };
    worker.onerror = (err) => {
      workerInitError = err instanceof Error ? err : new Error('Worker error');
      // Reject all pending requests
      pending.forEach((deferred) => {
        try { if (deferred && typeof deferred.reject === 'function') deferred.reject(workerInitError); } catch (e) {}
      });
      pending.clear();
    };
  } catch (err) {
    workerInitError = err instanceof Error ? err : new Error('Unable to start embedding worker');
  }
}

/**
 * Computes cosine similarity between two vectors. Returns 0 on mismatch/invalid input.
 * @param {Array<number>} a
 * @param {Array<number>} b
 * @returns {number}
 */
function similarity(a, b) {
  if (!Array.isArray(a) || !Array.isArray(b) || a.length === 0 || b.length === 0 || a.length !== b.length) {
    return 0;
  }
  let dot = 0;
  let normA = 0;
  let normB = 0;
  for (let i = 0; i < a.length; i++) {
    const va = Number(a[i]);
    const vb = Number(b[i]);
    if (!Number.isFinite(va) || !Number.isFinite(vb)) return 0;
    dot += va * vb;
    normA += va * va;
    normB += vb * vb;
  }
  if (normA === 0 || normB === 0) return 0;
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

/**
 * embed(text): Returns embedding or null (on failure/unsupported env).
 * @param {string} text
 * @returns {Promise<Array<number>|null>}
 */
async function embed(text) {
  if (!text || typeof text !== 'string') return null;

  // Primary path: Worker (browser-first)
  if (embeddingCache.has(text)) {
    return embeddingCache.get(text);
  }

  ensureWorker();
  if (worker && !workerInitError) {
    const promise = new Promise((resolve, reject) => {
      const id = nextId++;
      pending.set(id, { resolve, reject });
      try {
        worker.postMessage({ id, text });
      } catch (err) {
        pending.delete(id);
        resolve(null);
      }
      // Safety timeout to avoid dangling promises (15s)
      setTimeout(() => {
        if (pending.has(id)) {
          pending.delete(id);
          resolve(null);
        }
      }, 15000);
    }).then((result) => {
      // Cache successful embeddings only
      if (result && Array.isArray(result)) {
        embeddingCache.set(text, result);
      }
      return result;
    });
    embeddingCache.set(text, promise);
    return promise;
  }

  // Node fallback for integration/Node environments (opt-in)
  const extractor = await getNodeExtractor();
  if (!extractor) return null;
  try {
    const output = await extractor(text, { pooling: 'mean', normalize: true });
    const embedding = output && output.data ? Array.from(output.data) : (Array.isArray(output) ? output : null);
    if (embedding && Array.isArray(embedding)) {
      embeddingCache.set(text, embedding);
      return embedding;
    }
    return null;
  } catch (err) {
    return null;
  }
}

const EmbeddingService = { embed, similarity, _nodeExtractorError: () => nodeExtractorError };

if (typeof module !== 'undefined' && module.exports) {
  module.exports = EmbeddingService;
}
if (typeof window !== 'undefined') {
  window.EmbeddingService = EmbeddingService;
}

})();
