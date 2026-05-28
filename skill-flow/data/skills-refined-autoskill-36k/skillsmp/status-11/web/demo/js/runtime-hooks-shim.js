// Lightweight browser HookManager shim for demo runtime
// Prefers the project's HookManager module when available (bundled builds); falls back to an inline implementation for plain browser loads.
(function() {
  // Try to use the repository HookManager if running in a bundler/node-like environment
  try {
    // relative path from web/demo/js to src/runtime/hook-manager
    const HM = require('../../src/runtime/hook-manager');
    const HMConstructor = (HM && typeof HM === 'function') ? HM : (HM && HM.default) ? HM.default : null;
    if (HMConstructor) {
      if (typeof window !== 'undefined') {
        if (!window.RuntimeHooks) window.RuntimeHooks = new HMConstructor();

        // Attempt to wire demo-only persistence subscriber when running in a bundler/node environment
        // This will write debug save artifacts to src/.saves for developer inspection. It is skipped in
        // plain browser loads where Node APIs are not available.
        try {
          // relative path from web/demo/js to project src
          const createDemoPersistence = require('../../src/runtime/subscribers/demo-persistence');
          if (typeof createDemoPersistence === 'function') {
            try {
              const demoPersistence = createDemoPersistence({ logger: console });
              if (demoPersistence && window.RuntimeHooks && typeof window.RuntimeHooks.on === 'function') {
                if (demoPersistence.post_checkpoint) window.RuntimeHooks.on('post_checkpoint', demoPersistence.post_checkpoint.bind(demoPersistence));
                if (demoPersistence.on_rollback) window.RuntimeHooks.on('on_rollback', demoPersistence.on_rollback.bind(demoPersistence));
                console.info('[demo] demo-persistence subscriber registered');
              }
            } catch (e) {
              // swallow registration errors
              console.warn('[demo] failed to register demo-persistence subscriber', e);
            }
          }
        } catch (e) {
          // not available in this environment (likely plain browser load); ignore
        }
      }
      if (typeof module !== 'undefined' && module.exports) module.exports = window.RuntimeHooks;
      return;
    }
  } catch (e) {
    // not available in this environment; fall through to inline shim
  }

  // Inline fallback HookManager implementation
  class HookManager {
    constructor() {
      this._handlers = new Map();
    }
    on(hookName, handler) {
      if (!this._handlers.has(hookName)) this._handlers.set(hookName, []);
      this._handlers.get(hookName).push(handler);
      return () => this.off(hookName, handler);
    }
    off(hookName, handler) {
      const list = this._handlers.get(hookName) || [];
      const i = list.indexOf(handler);
      if (i >= 0) list.splice(i, 1);
      if (list.length === 0) this._handlers.delete(hookName);
    }
    async emitParallel(hookName, payload = {}) {
      const handlers = this._handlers.get(hookName) || [];
      const promises = handlers.map(async (h) => {
        try {
          const v = await h(payload);
          return { status: 'fulfilled', value: v };
        } catch (err) {
          return { status: 'rejected', reason: err };
        }
      });
      return Promise.all(promises);
    }
    async emitSequential(hookName, payload = {}, { stopOnError = false } = {}) {
      const handlers = this._handlers.get(hookName) || [];
      const results = [];
      for (const h of handlers) {
        try {
          const v = await h(payload);
          results.push({ status: 'fulfilled', value: v });
        } catch (err) {
          results.push({ status: 'rejected', reason: err });
          if (stopOnError) throw err;
        }
      }
      return results;
    }
  }

  if (typeof window !== 'undefined') {
    if (!window.RuntimeHooks) {
      window.RuntimeHooks = new HookManager();
      console.debug('[demo] RuntimeHooks shim initialized (fallback)');
    } else {
      console.debug('[demo] RuntimeHooks already present; shim skipped');
    }
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = window.RuntimeHooks;
  }
})();
