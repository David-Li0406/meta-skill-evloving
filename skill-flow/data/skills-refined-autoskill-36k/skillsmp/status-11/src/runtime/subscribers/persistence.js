const fs = require('fs');
const path = require('path');

// Simple append-only persistence subscriber for integration audit logs.
// For demo/testing: writes JSONL lines to .runtime_logs/integration.log

const LOG_DIR = path.join(__dirname, '../../../.runtime_logs');
const LOG_FILE = path.join(LOG_DIR, 'integration.log');

function ensureLogDir() {
  if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });
}

module.exports = function createPersistenceSubscriber() {
  ensureLogDir();
  return {
    name: 'runtime-persistence-subscriber',
    async on_state_change(payload) {
      try {
        const entry = { ts: new Date().toISOString(), type: 'state_change', payload };
        fs.appendFileSync(LOG_FILE, JSON.stringify(entry) + '\n', 'utf8');
      } catch (err) {
        // ignore write errors for demo
      }
    },
    async audit(payload) {
      try {
        const entry = { ts: new Date().toISOString(), type: 'audit', payload };
        fs.appendFileSync(LOG_FILE, JSON.stringify(entry) + '\n', 'utf8');
      } catch (err) {}
    }
  };
};
