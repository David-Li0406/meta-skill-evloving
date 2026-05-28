(function() {
"use strict";

/**
 * @module Director
 * @description
 * Lightweight AI Director implementing a deterministic 5-step decision pipeline.
 *
 * Decision steps:
 * 1. **Validation**: schema/policy validation via `ProposalValidator.quickValidate` (if present).
 * 2. **Return-path feasibility**: verifies `proposal.content.return_path` exists in the story.
 * 3. **Risk scoring**: computes a 0.0–1.0 risk score via {@link module:Director.computeRiskScore}.
 * 4. **Coherence check**: compares risk to a configurable threshold.
 * 5. **Final decision + telemetry**: returns a decision result and emits a `director_decision` event.
 *
 * This module is written to work in both browser (demo) and Node (unit tests).
 *
 * @example
 * // Browser usage
 * const proposal = {
 *   id: 'p-123',
 *   content: { text: 'A sudden storm breaks the silence…', return_path: 'knot_after_branch' },
 *   metadata: { confidence_score: 0.72 }
 * };
 *
 * const storyContext = { story: inkStoryInstance, phase: 'rising_action' };
 * const config = { riskThreshold: 0.4, writerMs: 250 };
 *
 * const result = await window.Director.evaluate(proposal, storyContext, config);
 * // result.decision -> 'approve' | 'reject'
 */

// Node/browser performance shim
let perf;
try {
  perf = (typeof performance !== 'undefined') ? performance : require('perf_hooks').performance;
} catch (e) {
  perf = (typeof performance !== 'undefined') ? performance : { now: () => Date.now() };
}

// Load director tuning defaults from a configurable file when available. This supports
// live tuning without editing the Director implementation. In bundler/node environments
// we require the shared config at src/runtime/director-config.js. In browsers, we prefer
// the latest window.DirectorConfig set by director-config-loader (which may load after
// this script executes), so we access it at call-time.
let DEFAULT_DIRECTOR_CONFIG = {};
try {
  if (typeof require === 'function') {
    // path from web/demo/js to repo src/runtime
    DEFAULT_DIRECTOR_CONFIG = require('../../../src/runtime/director-config');
  }
} catch (e) {
  // ignore
}

function getDefaultDirectorConfig() {
  try {
    if (typeof window !== 'undefined' && window.DirectorConfig && Object.keys(window.DirectorConfig).length > 0) {
      return window.DirectorConfig;
    }
  } catch (e) {}
  return DEFAULT_DIRECTOR_CONFIG || {};
}

// Helper to merge config with defaults
function mergeConfig(cfg) {
  if (!cfg || typeof cfg !== 'object') cfg = {};
  return Object.assign({}, getDefaultDirectorConfig() || {}, cfg);
}

function safeNumber(v, fallback = 0) {
  return typeof v === 'number' && Number.isFinite(v) ? v : fallback;
}

function clamp01(v, fallback = 0) {
  const n = safeNumber(v, fallback);
  if (n < 0) return 0;
  if (n > 1) return 1;
  return n;
}

function generateUUID() {
  try {
    if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
      return crypto.randomUUID();
    }
  } catch (e) {}
  // Fallback RFC4122-ish generator
  const rand = () => Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
  return `uuid-${rand()}${rand()}-${rand()}-${rand()}-${rand()}-${rand()}${rand()}${rand()}`;
}

function buildDecisionMetrics(proposal = {}, context = {}) {
  const text = (proposal.content && typeof proposal.content.text === 'string') ? proposal.content.text : '';
  const confidence = clamp01(proposal.metadata && proposal.metadata.confidence_score, 0.5);
  const pacing = clamp01((text.length - 300) / 700, 0);
  const returnPath = clamp01(context.returnPathCheck && context.returnPathCheck.confidence, 0);
    return {
      confidence,
      pacing,
      returnPath,
      thematic: null,
      lore: null,
      voice: null
    };
}

/**
 * checkReturnPath(returnPath, story)
 * Minimal existence check: looks for named knots on the inkjs story object
 * Returns { feasible, reason, confidence }
 */
function checkReturnPath(returnPath, story, proposal = {}) {
  if (!returnPath) {
    return { feasible: false, reason: 'No return_path provided', confidence: 0.0 };
  }

  // Try inkjs internal named content if available
  try {
    const named = story && story.mainContentContainer && story.mainContentContainer._namedContent;
    if (named && typeof named === 'object') {
      if (Object.prototype.hasOwnProperty.call(named, returnPath)) {
        return { feasible: true, reason: 'Return path exists', confidence: 0.9 };
      }
      return { feasible: false, reason: 'Return path knot does not exist', confidence: 0.0 };
    }
  } catch (e) {
    // fallthrough to fallback check
  }

  // Fallback: if the proposal itself included a validReturnPaths array on generation we can trust that
  try {
    if (Array.isArray(proposal && proposal.validReturnPaths)) {
      if (proposal.validReturnPaths.includes(returnPath)) {
        return { feasible: true, reason: 'Return path listed in proposal.validReturnPaths', confidence: 0.9 };
      }
      return { feasible: false, reason: 'Return path not present in proposal.validReturnPaths', confidence: 0.0 };
    }
  } catch (e) {}

  // Secondary fallback: global validReturnPaths (legacy tests)
  try {
    if (Array.isArray(window && window.__proposalValidReturnPaths)) {
      if (window.__proposalValidReturnPaths.includes(returnPath)) {
        return { feasible: true, reason: 'Return path listed in validReturnPaths', confidence: 0.9 };
      }
      return { feasible: false, reason: 'Return path not present in validReturnPaths', confidence: 0.0 };
    }
  } catch (e) {}

  // Unknown story shape -> be conservative: reject (in production we might attempt reachability analysis)
  return { feasible: false, reason: 'Unable to verify return path', confidence: 0.0 };
}

/**
 * computeRiskScore(proposal, context, config)
 * Lightweight deterministic scoring using three active metrics and three placeholders.
 * Returns number between 0.0 (low risk) and 1.0 (high risk).
 */
function getPlayerPreferenceScore(proposal = {}, config = {}) {
  const override = safeNumber(config && config.playerPreferenceScore, null);
  if (Number.isFinite(override)) return clamp01(override, 0.5);

  if (config && typeof config.getPreference === 'function') {
    const val = safeNumber(config.getPreference(proposal), null);
    if (Number.isFinite(val)) return clamp01(val, 0.5);
  }

  try {
    if (typeof PlayerPreference !== 'undefined' && PlayerPreference.getPreference) {
      const branchType = (proposal && proposal.content && (proposal.content.branch_type || proposal.content.branchType)) || 'default';
      const val = safeNumber(PlayerPreference.getPreference(branchType), null);
      if (Number.isFinite(val)) return clamp01(val, 0.5);
    }
  } catch (e) {}

  return 0.5;
}

function computeRiskScore(proposal = {}, context = {}, config = {}) {
  // Merge config early so helpers can reference merged values deterministically
  const mergedCfg = mergeConfig(config || {});

  // We want deterministic results given same inputs
  const confidence = safeNumber(proposal.metadata && proposal.metadata.confidence_score, 0.5);
  // proposal_confidence_risk: high confidence -> low risk
  const proposal_confidence_risk = 1.0 - Math.max(0, Math.min(1, confidence));

  // narrative_pacing_risk: heuristic based on content length vs phase target
  const text = (proposal.content && proposal.content.text) || '';
  const len = text.length;
  const phase = (context && context.phase) || 'exposition';
  const defaultPacingTargets = Object.assign({
    exposition: 300,
    rising_action: 400,
    climax: 700,
    falling_action: 350,
    resolution: 300
  }, (mergedCfg && mergedCfg.pacingTargets) || (config && config.pacingTargets) || {});
  const expectedLen = Math.max(1, safeNumber(defaultPacingTargets[phase], 300));
  const toleranceFactor = Math.max(0.05, safeNumber((mergedCfg && mergedCfg.pacingToleranceFactor) || config && config.pacingToleranceFactor, 0.6));
  // Risk grows once length exceeds expected; at expected*(1+toleranceFactor) risk reaches ~1
  const pacingRatio = len / expectedLen;
  const pacingOver = Math.max(0, pacingRatio - 1);
  const narrative_pacing_risk = Math.min(1, pacingOver / toleranceFactor);

  // return_path_confidence_risk derived from context.returnPathCheck (if present)
  const returnPathConfidence = safeNumber((context && context.returnPathCheck && context.returnPathCheck.confidence), 0.0);
  const return_path_confidence_risk = 1.0 - Math.max(0, Math.min(1, returnPathConfidence));

  // player preference risk: high preference -> low risk
  const preferenceScore = getPlayerPreferenceScore(proposal, config);
  const player_preference_risk = 1.0 - Math.max(0, Math.min(1, preferenceScore));

  // Placeholder metrics (thematic, lore, voice)
  const placeholder = safeNumber((mergedCfg && mergedCfg.placeholderDefault) || config.placeholderDefault, 0.3);
  let thematic_consistency_risk = placeholder;
  let lore_adherence_risk = placeholder;
  let character_voice_risk = placeholder;

  // If the caller provided precomputed embedding similarity metrics in
  // config.embeddingMetrics (values 0..1), use them to derive risks. This
  // keeps computeRiskScore synchronous and test-friendly while allowing the
  // async evaluate() path to supply embedding-derived metrics.
  try {
    const em = config && config.embeddingMetrics;
    if (em && typeof em === 'object') {
      if (Number.isFinite(em.thematic)) thematic_consistency_risk = 1.0 - clamp01(em.thematic, placeholder);
      if (Number.isFinite(em.lore)) lore_adherence_risk = 1.0 - clamp01(em.lore, placeholder);
      if (Number.isFinite(em.voice)) character_voice_risk = 1.0 - clamp01(em.voice, placeholder);
    }
  } catch (e) {}

  // Weights (configurable)
  const weights = Object.assign({
    proposal_confidence: 0.7,
    narrative_pacing: 0.15,
    return_path_confidence: 0.1,
    player_preference: 0.05,
    thematic_consistency: 0,
    lore_adherence: 0,
    character_voice: 0
  }, (mergedCfg && mergedCfg.weights) || config.weights || {});

  // Weighted average of active metrics
  const activeSum = weights.proposal_confidence + weights.narrative_pacing + weights.return_path_confidence + weights.player_preference;
  const activeScore = (
    proposal_confidence_risk * weights.proposal_confidence +
    narrative_pacing_risk * weights.narrative_pacing +
    return_path_confidence_risk * weights.return_path_confidence +
    player_preference_risk * weights.player_preference
  ) / Math.max(1e-6, activeSum);

  // Add fraction for placeholders (kept small / configurable)
  const placeholderSum = (weights.thematic_consistency || 0) + (weights.lore_adherence || 0) + (weights.character_voice || 0);
  const placeholderScore = (thematic_consistency_risk * (weights.thematic_consistency || 0) +
                           lore_adherence_risk * (weights.lore_adherence || 0) +
                           character_voice_risk * (weights.character_voice || 0)) / Math.max(1e-6, placeholderSum || 1);

  // Mix active + placeholder (placeholder usually zero in defaults)
  const totalWeight = activeSum + placeholderSum;
  const totalScore = (activeScore * activeSum + placeholderScore * placeholderSum) / Math.max(1e-6, totalWeight);

  // Clamp
  return Math.max(0, Math.min(1, totalScore));
}

/**
 * emitDecisionTelemetry(decisionResult, extras)
 * Emits director_decision events via Telemetry (if available) and buffers last 50 in sessionStorage.
 */
function emitDecisionTelemetry(decisionResult = {}, extras = {}) {
  const proposalId = decisionResult.proposal_id || (decisionResult.proposal && decisionResult.proposal.id);
  const writerMs = safeNumber(decisionResult.writerMs ?? extras.writerMs, 0);
  const directorMs = safeNumber(decisionResult.directorMs ?? decisionResult.latencyMs ?? extras.directorMs, 0);
  const totalMs = safeNumber(decisionResult.totalMs ?? (writerMs + directorMs), writerMs + directorMs);

  const payload = Object.assign({}, decisionResult, {
    proposal_id: proposalId || generateUUID(),
    timestamp: new Date().toISOString(),
    writerMs,
    directorMs,
    totalMs,
    metrics: Object.assign({
      confidence: null,
      pacing: null,
      returnPath: null,
      thematic: null,
      lore: null,
      voice: null
    }, decisionResult.metrics || extras.metrics || {})
  });

  // Ensure required fields exist even if undefined
  const eventName = 'director_decision';

  try {
    if (typeof window !== 'undefined' && window.Telemetry && typeof window.Telemetry.emit === 'function') {
      window.Telemetry.emit(eventName, payload);
    } else if (typeof console !== 'undefined') {
      console.log('[director] telemetry', payload);
    }

    // Buffer in sessionStorage
    if (typeof sessionStorage !== 'undefined') {
      try {
        const raw = sessionStorage.getItem('ge-hch.director.telemetry') || '[]';
        const arr = JSON.parse(raw);
        arr.push(payload);
        while (arr.length > 50) arr.shift();
        sessionStorage.setItem('ge-hch.director.telemetry', JSON.stringify(arr));
      } catch (e) {}
    }
  } catch (e) {}

  return payload;
}

/**
 * Decision result returned by {@link module:Director.evaluate}.
 *
 * @typedef {Object} DecisionResult
 * @property {string} [proposal_id] - Proposal identifier (if provided by the Writer).
 * @property {'approve'|'reject'} decision - Director decision.
 * @property {string} reason - Human-readable rationale for the decision.
 * @property {number} riskScore - Risk score in the range 0.0 (low risk) to 1.0 (high risk).
 * @property {number} latencyMs - Director evaluation latency in milliseconds.
 * @property {number} writerMs - Optional Writer latency (passed via config for telemetry).
 * @property {number} directorMs - Director-only latency in milliseconds.
 * @property {number} totalMs - writerMs + directorMs.
 * @property {Object} [metrics] - Metric breakdown used for telemetry/debug.
 */

/**
 * Evaluate a Writer proposal and decide whether it can be injected.
 *
 * @function evaluate
 * @memberof module:Director
 * @async
 * @param {Object} proposal - Writer proposal to evaluate.
 * @param {Object} [storyContext={}] - Current story context.
 * @param {Object} [storyContext.story] - inkjs story instance (used for return-path feasibility).
 * @param {string} [storyContext.phase] - Narrative phase used for pacing heuristics.
 * @param {Object} [config={}] - Evaluation configuration.
 * @param {number} [config.riskThreshold=0.4] - Max acceptable risk for approval.
 * @param {number} [config.writerMs=0] - Writer latency in ms (optional, telemetry only).
 * @returns {Promise<DecisionResult>} Decision result.
 * @throws {Error} If the proposal is missing or malformed.
 */
async function evaluate(proposal, storyContext = {}, config = {}) {
  const start = perf.now();

  // Quick sanity
  if (!proposal || typeof proposal !== 'object') {
    throw new Error('Malformed proposal');
  }

  // Step 1: validation (schema + quick safety)
  try {
    const validation = (typeof ProposalValidator !== 'undefined' && ProposalValidator.quickValidate)
      ? ProposalValidator.quickValidate(proposal, {
        validReturnPaths: storyContext && storyContext.validReturnPaths
      })
      : { valid: true };

    if (!validation || !validation.valid) {
      const latencyMs = Math.max(0, perf.now() - start);
      const result = { decision: 'reject', reason: validation && validation.reason ? validation.reason : 'Failed policy validation', riskScore: 1.0, latencyMs, writerMs: 0, directorMs: latencyMs, totalMs: latencyMs };
      emitDecisionTelemetry(result);
      return result;
    }

    if (validation.sanitizedProposal) {
      proposal = validation.sanitizedProposal;
    }
  } catch (e) {
    const latencyMs = Math.max(0, perf.now() - start);
    const result = { decision: 'reject', reason: 'Validation error', riskScore: 1.0, latencyMs, writerMs: 0, directorMs: latencyMs, totalMs: latencyMs };
    emitDecisionTelemetry(result);
    return result;
  }

  // Step 2: return-path feasibility
  let returnCheck = { feasible: true, reason: 'No check performed', confidence: 0.9 };
  try {
    const returnPath = (proposal.content && proposal.content.return_path) || null;
    returnCheck = checkReturnPath(returnPath, storyContext && storyContext.story, proposal);
    if (!returnCheck.feasible) {
    const latencyMs = Math.max(0, perf.now() - start);
    const result = { decision: 'reject', reason: `Return path check failed: ${returnCheck.reason}`, riskScore: 1.0, latencyMs, writerMs: 0, directorMs: latencyMs, totalMs: latencyMs };
    emitDecisionTelemetry(result);
    return result;
  }
} catch (e) {
  // conservative rejection
  const latencyMs = Math.max(0, perf.now() - start);
  const result = { decision: 'reject', reason: 'Return path check error', riskScore: 1.0, latencyMs, writerMs: 0, directorMs: latencyMs, totalMs: latencyMs };
  emitDecisionTelemetry(result);
  return result;
}


  // Step 3: risk scoring
  const context = { returnPathCheck: returnCheck, story: storyContext && storyContext.story };

  // If embeddings are enabled, attempt to compute embedding similarity metrics
  // asynchronously and pass them into computeRiskScore via config.embeddingMetrics.
  let finalConfig = config;
  try {
    const mergedCfg = mergeConfig(config || {});
    const embeddingsEnabled = Boolean((mergedCfg && mergedCfg.enableEmbeddings) || config.enableEmbeddings);
    if (embeddingsEnabled) {
      const EmbeddingService = (typeof window !== 'undefined' && window.EmbeddingService) ? window.EmbeddingService : (typeof require === 'function' ? require('../../../web/demo/js/embedding-service') : null);
      if (EmbeddingService && typeof EmbeddingService.embed === 'function' && typeof EmbeddingService.similarity === 'function') {
      try {
          const text = (proposal.content && proposal.content.text) || '';
          // Capture embedding timing and fallback status for telemetry
          let emb = null;
          let emMetrics = null;
          let embeddingTelemetry = { used: false, latencyMs: 0, fallback: true };
          try {
            const embStart = perf.now();
            emb = await (EmbeddingService.embed ? EmbeddingService.embed(text) : null);
            embeddingTelemetry.latencyMs = Math.max(0, Math.round(perf.now() - embStart));
            embeddingTelemetry.used = Boolean(emb && Array.isArray(emb));
            embeddingTelemetry.fallback = !embeddingTelemetry.used;

            if (emb && Array.isArray(emb)) {
              emMetrics = {};
              const themeEmb = storyContext && storyContext.themeEmbedding;
              const loreEmb = storyContext && storyContext.loreEmbedding;
              const voiceEmb = storyContext && storyContext.voiceEmbedding;
              if (themeEmb && Array.isArray(themeEmb)) emMetrics.thematic = EmbeddingService.similarity(emb, themeEmb);
              if (loreEmb && Array.isArray(loreEmb)) emMetrics.lore = EmbeddingService.similarity(emb, loreEmb);
              if (voiceEmb && Array.isArray(voiceEmb)) emMetrics.voice = EmbeddingService.similarity(emb, voiceEmb);
              finalConfig = Object.assign({}, config, { embeddingMetrics: emMetrics });
            }
          } catch (innerErr) {
            // treat as fallback - keep embeddingTelemetry indicating fallback
          }
          // expose embedding telemetry/metrics to outer scope via finalConfig extras
          if (!finalConfig) finalConfig = config;
          finalConfig._embeddingTelemetry = embeddingTelemetry;
          finalConfig._embeddingMetrics = emMetrics;
        } catch (e) {
          // ignore embedding failures and continue with placeholder behavior
        }
      }
    }
  } catch (e) {}
  const riskScore = computeRiskScore(proposal, context, finalConfig);

  // Step 4: coherence check (threshold)
  const threshold = safeNumber((config && config.riskThreshold), 0.4);
  const decision = (riskScore <= threshold) ? 'approve' : 'reject';
  const reason = decision === 'approve' ? 'Risk acceptable' : 'Risk above threshold';

  const latencyMs = Math.max(0, perf.now() - start);
  const writerMs = safeNumber(config && config.writerMs, 0);
  const directorMs = latencyMs;
  const totalMs = writerMs + directorMs;
  const metrics = buildDecisionMetrics(proposal, context);
  const result = {
    proposal_id: proposal.id || proposal.proposal_id,
    decision,
    reason,
    riskScore,
    latencyMs,
    writerMs,
    directorMs,
    totalMs,
    metrics
  };
  // If embedding telemetry was captured in finalConfig, include it in the
  // director telemetry payload under `metrics.embedding` so ingestion can
  // observe embedding inference timing and fallback status.
  try {
    const emt = finalConfig && finalConfig._embeddingTelemetry;
    const emm = finalConfig && finalConfig._embeddingMetrics;
    if (emt || emm) {
      result.metrics = Object.assign({}, result.metrics, { embedding: Object.assign({}, emt || {}, { metrics: emm || null }) });
    }
  } catch (e) {}

  emitDecisionTelemetry(result);
  return result;
}

// Exports
const Director = {
  evaluate,
  checkReturnPath,
  computeRiskScore,
  emitDecisionTelemetry,
  _getPlayerPreferenceScore: getPlayerPreferenceScore
};

if (typeof module !== 'undefined' && module.exports) {
  module.exports = Director;
}
if (typeof window !== 'undefined') {
  window.Director = Director;
}

})();
