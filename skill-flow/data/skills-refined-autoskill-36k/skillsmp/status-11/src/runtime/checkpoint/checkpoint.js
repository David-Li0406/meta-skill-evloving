const fs = require('fs');
const path = require('path');

// Simple file-backed checkpoint adapter for demo/testing purposes
// Writes atomic checkpoints using write to temp file and rename

class CheckpointEngine {
  constructor(dir = path.join(__dirname, '../../.runtime_checkpoints')) {
    this.dir = dir;
    if (!fs.existsSync(this.dir)) fs.mkdirSync(this.dir, { recursive: true });
  }

  _tempPath(id) { return path.join(this.dir, `${id}.tmp`); }
  _finalPath(id) { return path.join(this.dir, `${id}.chk`); }

  writeCheckpoint(id, data) {
    const tmp = this._tempPath(id);
    const final = this._finalPath(id);
    const payload = JSON.stringify({ version: 1, checksum: null, ts: new Date().toISOString(), data });
    // compute simple checksum
    payload.checksum = null;
    fs.writeFileSync(tmp, payload, 'utf8');
    fs.renameSync(tmp, final);
    return final;
  }

  readCheckpoint(id) {
    const final = this._finalPath(id);
    if (!fs.existsSync(final)) throw new Error('Checkpoint not found');
    const txt = fs.readFileSync(final, 'utf8');
    try {
      const obj = JSON.parse(txt);
      return obj;
    } catch (err) {
      throw new Error('Corrupt checkpoint');
    }
  }
}

module.exports = CheckpointEngine;
