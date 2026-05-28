// Demo persistence subscriber
// Listens to post_checkpoint and on_rollback hooks and writes debug save artifacts
// into src/.saves/ using the project's save-adapter. Intended for local dev/CI only.

const saveAdapter = require('../save-adapter');
const path = require('path');

function makeId() {
  return `demo-save-${Date.now().toString(36)}-${Math.random().toString(16).slice(2,8)}`;
}

module.exports = function createDemoPersistenceSubscriber(opts = {}) {
  const logger = opts.logger || console;

  return {
    name: 'demo-persistence-subscriber',

    // post_checkpoint receives { payload, story }
    async post_checkpoint(ctx = {}) {
      try {
        const payload = ctx.payload || {};
        const saveId = makeId();
        // Save minimal wrapper compatible with save-adapter
        const gameState = payload.story || null;
        const branchHistory = payload.loreHistory || [];
        const lastCheckpointId = null;
        const file = saveAdapter.writeSave(saveId, { gameState, branchHistory, lastCheckpointId });
        logger.info('[demo-persistence] wrote save', file);
      } catch (err) {
        // Don't let persistence errors break runtime
        try { logger.warn('[demo-persistence] write failed', err); } catch (e) {}
      }
    },

    // on_rollback receives { error }
    async on_rollback(ctx = {}) {
      try {
        const err = ctx.error;
        const saveId = makeId();
        // Write a small audit file to .saves to help debugging
        const debug = {
          ts: new Date().toISOString(),
          type: 'rollback',
          error: (err && err.message) ? err.message : String(err)
        };
        // Reuse save-adapter to write a small file (store under saveId so it's easy to find)
        saveAdapter.writeSave(saveId, { gameState: { rollbackDebug: debug }, branchHistory: [], lastCheckpointId: null });
        logger.info('[demo-persistence] rollback debug written', saveId);
      } catch (err) {
        try { logger.warn('[demo-persistence] on_rollback failed', err); } catch (e) {}
      }
    }
  };
};
