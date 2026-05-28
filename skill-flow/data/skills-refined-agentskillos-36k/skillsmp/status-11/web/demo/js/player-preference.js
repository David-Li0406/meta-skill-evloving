(function () {
  "use strict";

  const STORAGE_KEY = 'ge-hch.ai-preferences';
  const DEFAULT_SCORE = 0.5;

  function safeParse(json) {
    try {
      return JSON.parse(json);
    } catch (_) {
      return null;
    }
  }

  const GLOBAL_CACHE_KEY = '__ge_hch_player_preferences_cache__';
  const _shared = (typeof globalThis !== 'undefined' && globalThis[GLOBAL_CACHE_KEY]) || {
    cachedRaw: null,
    cachedState: null,
    pendingTimer: null,
    pendingState: null,
  };
  if (typeof globalThis !== 'undefined') {
    globalThis[GLOBAL_CACHE_KEY] = _shared;
  }

  function loadState() {
    if (typeof localStorage === 'undefined') return _shared.cachedState || { events: [], totals: {} };
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      // If nothing stored, normalize to null for comparison
      const normRaw = raw || null;
      if (_shared.cachedRaw === normRaw && _shared.cachedState) return _shared.cachedState;
      if (!raw) {
        _shared.cachedRaw = null;
        _shared.cachedState = { events: [], totals: {} };
        return _shared.cachedState;
      }
      const parsed = safeParse(raw);
      if (!parsed || typeof parsed !== 'object') {
        _shared.cachedRaw = null;
        _shared.cachedState = { events: [], totals: {} };
        return _shared.cachedState;
      }
      const events = Array.isArray(parsed.events) ? parsed.events : [];
      const totals = parsed.totals && typeof parsed.totals === 'object' ? parsed.totals : {};
      _shared.cachedRaw = normRaw;
      _shared.cachedState = { events, totals };
      return _shared.cachedState;
    } catch (_) {
      _shared.cachedRaw = null;
      _shared.cachedState = { events: [], totals: {} };
      return _shared.cachedState;
    }
  }

  function saveState(state) {
    _shared.cachedState = state;

    if (typeof localStorage === 'undefined') {
      _shared.cachedRaw = null;
      return;
    }

    // Coalesce rapid consecutive writes (e.g., perf-heavy tests) into a single
    // async write, avoiding repeated JSON.stringify/setItem cost while keeping
    // cached state immediately available across module reloads.
    _shared.pendingState = state;
    if (_shared.pendingTimer) return;

    _shared.pendingTimer = setTimeout(() => {
      try {
        const raw = JSON.stringify(_shared.pendingState);
        localStorage.setItem(STORAGE_KEY, raw);
        _shared.cachedRaw = raw || null;
      } catch (_) {
        _shared.cachedRaw = null;
      } finally {
        _shared.pendingTimer = null;
        _shared.pendingState = null;
      }
    }, 0);
  }

  function clamp01(value) {
    if (!Number.isFinite(value)) return DEFAULT_SCORE;
    if (value < 0) return 0;
    if (value > 1) return 1;
    return value;
  }

  const PlayerPreference = {
    getPreference(branchType) {
      if (!branchType) return DEFAULT_SCORE;
      const { totals } = loadState();
      const entry = totals[branchType];
      if (!entry || !entry.total) return DEFAULT_SCORE;
      return clamp01(entry.accepted / entry.total);
    },

    recordOutcome(branchType, accepted) {
      if (!branchType || typeof branchType !== 'string') return DEFAULT_SCORE;
      const outcome = Boolean(accepted);
      const state = loadState();
      const now = new Date().toISOString();
      state.events.push({ branchType, accepted: outcome, timestamp: now });
      const current = state.totals[branchType] || { accepted: 0, total: 0 };
      const nextTotals = {
        accepted: current.accepted + (outcome ? 1 : 0),
        total: current.total + 1,
      };
      state.totals[branchType] = nextTotals;
      saveState(state);
      return clamp01(nextTotals.accepted / nextTotals.total);
    },

    _debugLoad() {
      // For tests only.
      return loadState();
    },
  };

  if (typeof window !== 'undefined') {
    window.PlayerPreference = PlayerPreference;
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = PlayerPreference;
  }
})();
