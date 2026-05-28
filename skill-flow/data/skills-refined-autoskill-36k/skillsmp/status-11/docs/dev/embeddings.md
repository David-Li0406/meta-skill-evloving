Embedding Integration (runtime)

Overview
--------
The Director can optionally use local semantic embeddings to improve scoring for thematic consistency, lore adherence, and character voice. This feature is opt-in and disabled by default.

Enabling
--------
- Set `enableEmbeddings: true` in `.gengine/config.yaml` under `directorConfig`, or pass `{ enableEmbeddings: true }` via the `evaluate()` `config` argument.
- For Node integration tests you may set environment flags (used by embedding service): `EMBED_NODE=1` to enable Node fallback.

Telemetry
---------
When embeddings are enabled, Director emits embedding telemetry inside the `director_decision` event under `metrics.embedding` with fields:
- `used` (boolean) - whether embeddings were successfully computed
- `latencyMs` (number) - inference time in milliseconds
- `fallback` (boolean) - true when embeddings were not used and placeholders were applied
- `metrics` (optional object) - similarity metrics (0..1) for `thematic`, `lore`, and `voice` when available

Implementation notes
--------------------
- `evaluate()` computes embeddings asynchronously (using `web/demo/js/embedding-service.js` when available) and derives similarity metrics when story-level embeddings are provided on `storyContext` as `themeEmbedding`, `loreEmbedding`, `voiceEmbedding` arrays.
- `computeRiskScore()` remains synchronous and reads precomputed `config.embeddingMetrics` (if present) to convert similarities into placeholder risks. This keeps the core scoring deterministic and testable.

Follow-ups
----------
1) Precompute story-level embeddings at load-time and attach them to story context. (bead created)
2) Optionally emit a dedicated `embedding_inference` telemetry event in addition to including embedding metadata in director telemetry. (bead created)
