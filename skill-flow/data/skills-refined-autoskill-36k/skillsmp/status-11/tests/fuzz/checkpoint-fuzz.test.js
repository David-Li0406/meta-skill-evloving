const CheckpointEngine = require('../../src/runtime/checkpoint/checkpoint');
const fs = require('fs');
const path = require('path');

describe('checkpoint fuzz harness (simple)', () => {
  const engine = new CheckpointEngine();
  const id = 'fuzz-1';
  const file = path.join(__dirname, '../../.runtime_checkpoints', `${id}.chk`);

  afterAll(() => {
    if (fs.existsSync(file)) fs.unlinkSync(file);
  });

  test('write checkpoint and handle corruption -> rollback', () => {
    // write a valid checkpoint
    engine.writeCheckpoint(id, { state: { x: 1 } });
    expect(fs.existsSync(file)).toBe(true);

    // simulate corruption by writing invalid JSON
    fs.writeFileSync(file, 'not-json', 'utf8');

    // read should throw and be caught by caller; here we assert it throws
    expect(() => engine.readCheckpoint(id)).toThrow();

    // simulate recovery by writing a fresh checkpoint
    engine.writeCheckpoint(id, { state: { x: 2 } });
    const obj = engine.readCheckpoint(id);
    expect(obj.data.state.x).toBe(2);
  });
});
