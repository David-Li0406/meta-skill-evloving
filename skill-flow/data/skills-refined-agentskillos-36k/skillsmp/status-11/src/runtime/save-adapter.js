// Simple save adapter for carrying branch metadata and resume payload

const fs = require('fs');
const path = require('path');

const SAVE_DIR = path.join(__dirname, '../.saves');
if (!fs.existsSync(SAVE_DIR)) fs.mkdirSync(SAVE_DIR, { recursive: true });

function computeChecksum(str) {
  // Simple checksum for demo purposes
  let h = 0;
  for (let i = 0; i < str.length; i++) h = ((h << 5) - h) + str.charCodeAt(i), h |= 0;
  return h.toString(16);
}

module.exports = {
  writeSave(saveId, { gameState, branchHistory = [], lastCheckpointId = null, schemaVersion = 1 } = {}) {
    const payload = { schemaVersion, ts: new Date().toISOString(), branchHistory, lastCheckpointId, gameState };
    const txt = JSON.stringify(payload);
    const checksum = computeChecksum(txt);
    const final = { checksum, payload };
    const file = path.join(SAVE_DIR, `${saveId}.save`);
    fs.writeFileSync(file, JSON.stringify(final), 'utf8');
    return file;
  },
  readSave(saveId) {
    const file = path.join(SAVE_DIR, `${saveId}.save`);
    if (!fs.existsSync(file)) throw new Error('Save not found');
    const txt = fs.readFileSync(file, 'utf8');
    try {
      const obj = JSON.parse(txt);
      const calculated = computeChecksum(JSON.stringify(obj.payload));
      if (calculated !== obj.checksum) throw new Error('Checksum mismatch');
      return obj.payload;
    } catch (err) {
      throw new Error('Corrupt save');
    }
  }
};
