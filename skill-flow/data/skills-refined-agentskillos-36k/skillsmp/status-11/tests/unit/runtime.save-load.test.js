const saveAdapter = require('../../src/runtime/save-adapter');
const loadAdapter = require('../../src/runtime/load-adapter');
const fs = require('fs');
const path = require('path');

describe('save/load adapters', () => {
  const saveId = 'test-save-1';
  afterAll(() => {
    const file = path.join(__dirname, '../../.saves', `${saveId}.save`);
    if (fs.existsSync(file)) fs.unlinkSync(file);
  });

  test('write and read save payload correctly', () => {
    const file = saveAdapter.writeSave(saveId, { gameState: { pos: 1 }, branchHistory: [{ id: 'b1' }], lastCheckpointId: 'c1', schemaVersion: 1 });
    expect(fs.existsSync(file)).toBe(true);
    const payload = saveAdapter.readSave(saveId);
    expect(payload.branchHistory[0].id).toBe('b1');
  });

  test('load adapter detects schema mismatch and calls onIncompatible', () => {
    saveAdapter.writeSave(saveId, { gameState: { pos: 2 }, schemaVersion: 99 });
    const res = loadAdapter.loadSave(saveId, { expectedSchemaVersion: 1, onIncompatible: (info) => ({ action: 'rollback', info }) });
    expect(res.action).toBe('rollback');
    expect(res.info.reason).toBe('schema_mismatch' || res.info.save);
  });
});
