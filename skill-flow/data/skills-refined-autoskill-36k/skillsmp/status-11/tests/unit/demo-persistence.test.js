const HookManager = require('../../src/runtime/hook-manager');
const createDemoPersistence = require('../../src/runtime/subscribers/demo-persistence');
const fs = require('fs');
const path = require('path');

describe('demo persistence subscriber', () => {
  test('writes a .save file on post_checkpoint', async () => {
    const hm = new HookManager();
    const demo = createDemoPersistence({ logger: { info: () => {}, warn: () => {} } });
    // register
    hm.on('post_checkpoint', demo.post_checkpoint);

    const payload = { payload: { story: '{"fake":"state"}' } };
    await hm.emitParallel('post_checkpoint', payload);

    // look for files in src/.saves
    const saveDir = path.join(__dirname, '../../src/.saves');
    const files = fs.existsSync(saveDir) ? fs.readdirSync(saveDir) : [];
    expect(files.some(f => f.endsWith('.save'))).toBe(true);
  });

  test('writes rollback debug on on_rollback', async () => {
    const hm = new HookManager();
    const demo = createDemoPersistence({ logger: { info: () => {}, warn: () => {} } });
    hm.on('on_rollback', demo.on_rollback);

    await hm.emitParallel('on_rollback', { error: new Error('boom') });
    const saveDir = path.join(__dirname, '../../src/.saves');
    const files = fs.existsSync(saveDir) ? fs.readdirSync(saveDir) : [];
    expect(files.some(f => f.endsWith('.save'))).toBe(true);
  });
});
