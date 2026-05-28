// Load adapter with conservative rollback behavior when schema/checksum mismatches

const saveAdapter = require('./save-adapter');

module.exports = {
  loadSave(saveId, { expectedSchemaVersion = 1, onIncompatible = () => ({ action: 'rollback' }) } = {}) {
    try {
      const payload = saveAdapter.readSave(saveId);
      if (payload.schemaVersion !== expectedSchemaVersion) {
        return onIncompatible({ reason: 'schema_mismatch', save: payload });
      }
      return { action: 'resume', save: payload };
    } catch (err) {
      return onIncompatible({ reason: 'corrupt_save', error: err });
    }
  }
};
