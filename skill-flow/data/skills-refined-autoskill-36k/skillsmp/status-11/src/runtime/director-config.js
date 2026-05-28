// Director tuning configuration
// Load defaults but allow local overrides from .gengine/config.yaml and environment variables.
// The .gengine/config.yaml may contain a top-level `directorConfig` / `DIRECTOR_CONFIG`
// mapping or individual keys like `weights` / `pacingTargets`.

const fs = (() => {
  try { return require('fs'); } catch (e) { return null; }
})();
const path = (() => {
  try { return require('path'); } catch (e) { return null; }
})();

let yaml = null;
try { yaml = require('js-yaml'); } catch (e) { yaml = null; }

function deepMerge(target, src) {
  if (!src) return target;
  Object.keys(src).forEach(k => {
    const sv = src[k];
    if (sv && typeof sv === 'object' && !Array.isArray(sv) && typeof target[k] === 'object') {
      target[k] = deepMerge(Object.assign({}, target[k]), sv);
    } else {
      target[k] = sv;
    }
  });
  return target;
}

function loadLocalConfig() {
  try {
    if (!fs || !path) return {};
    const cfgPath = path.join(process.cwd(), '.gengine', 'config.yaml');
    if (!fs.existsSync(cfgPath)) return {};

    const raw = fs.readFileSync(cfgPath, 'utf8');
    let parsed = {};
    if (yaml) {
      parsed = yaml.load(raw) || {};
    } else {
      // Minimal fallback parser: KEY: value lines
      raw.split(/\r?\n/).forEach(line => {
        const t = line.trim();
        if (!t || t.startsWith('#')) return;
        const m = t.match(/^([A-Za-z0-9_\-\.]+)\s*:\s*(.*)$/);
        if (m) parsed[m[1]] = m[2];
      });
    }
    return parsed;
  } catch (e) {
    return {};
  }
}

const defaults = {
  weights: {
    proposal_confidence: 0.7,
    narrative_pacing: 0.15,
    return_path_confidence: 0.1,
    player_preference: 0.05,
    thematic_consistency: 0,
    lore_adherence: 0,
    character_voice: 0
  },

  pacingTargets: {
    exposition: 300,
    rising_action: 400,
    climax: 700,
    falling_action: 350,
    resolution: 300
  },

  pacingToleranceFactor: 0.6,

  placeholderDefault: 0.3,

  // Enable embedding-based scoring in the runtime. Disabled by default.
  // Can be toggled via local .gengine/config.yaml or environment overrides
  // (see loadLocalConfig/ENV parsing in this file). When enabled the Director
  // will attempt to compute semantic embeddings for proposals and use
  // similarity-derived metrics for thematic/lore/voice scoring.
  enableEmbeddings: false,

  // Global default decision threshold used by the Director when not overridden per-call
  // Value is in 0.0..1.0 where lower is stricter (default 0.4)
  riskThreshold: 0.4
};

// Attempt to load local overrides
const local = loadLocalConfig();
let merged = Object.assign({}, defaults);

// Support several possible shapes in the YAML: a top-level directorConfig, or
// top-level keys (weights, pacingTargets, etc.).
if (local) {
  const c = local.directorConfig || local.DIRECTOR_CONFIG || local.DirectorConfig || null;
  if (c && typeof c === 'object') {
    merged = deepMerge(merged, c);
  } else {
    // Merge any matching top-level keys
    ['weights', 'pacingTargets', 'pacingToleranceFactor', 'placeholderDefault'].forEach(k => {
      if (Object.prototype.hasOwnProperty.call(local, k)) {
        merged = deepMerge(merged, { [k]: local[k] });
      }
      const upk = String(k).toUpperCase();
      if (Object.prototype.hasOwnProperty.call(local, upk)) {
        merged = deepMerge(merged, { [k]: local[upk] });
      }
    });
  }
}

// Environment variables may also override individual values (optional).
// For example: process.env.DIRECTOR_WEIGHTS__PROPOSAL_CONFIDENCE=0.5
if (typeof process !== 'undefined' && process.env) {
  Object.keys(process.env).forEach(envK => {
    // pattern: DIRECTOR_WEIGHTS__proposal_confidence or DIRECTOR_PACINGTARGETS__exposition
    const m = envK.match(/^DIRECTOR_([A-Z0-9_]+)__([A-Z0-9_]+)$/);
    if (m) {
      const section = m[1].toLowerCase();
      const key = m[2].toLowerCase();
      try {
        const val = Number(process.env[envK]);
        if (!Number.isNaN(val)) merged[section] = merged[section] || {}, merged[section][key] = val;
        else merged[section] = merged[section] || {}, merged[section][key] = process.env[envK];
      } catch (e) {}
    }
  });
}

module.exports = merged;
