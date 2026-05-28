// Simple async HookManager for runtime integration points
// - Promise-based handlers
// - Handlers are non-blocking: failures are caught and do not stop other handlers
// - Supports parallel or sequential emission

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

  // Emit handlers in parallel. Returns an array of {status, value|reason} entries.
  async emitParallel(hookName, payload = {}) {
    const handlers = this._handlers.get(hookName) || [];
    const promises = handlers.map(async (h) => {
      try {
        const v = await h(payload);
        return { status: 'fulfilled', value: v };
      } catch (err) {
        // Keep error information but don't throw
        return { status: 'rejected', reason: err };
      }
    });
    return Promise.all(promises);
  }

  // Emit handlers sequentially. Short-circuits on thrown error only if stopOnError=true
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

module.exports = HookManager;
