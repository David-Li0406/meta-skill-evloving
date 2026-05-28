const HookManager = require('../../src/runtime/hook-manager');

describe('HookManager', () => {
  test('emitParallel runs handlers and catches errors', async () => {
    const hm = new HookManager();
    hm.on('pre_inject', async (p) => { return 'ok'; });
    hm.on('pre_inject', async (p) => { throw new Error('fail'); });
    const res = await hm.emitParallel('pre_inject', { foo: 1 });
    expect(res.length).toBe(2);
    expect(res.filter(r => r.status === 'fulfilled').length).toBe(1);
    expect(res.filter(r => r.status === 'rejected').length).toBe(1);
  });

  test('emitSequential preserves order', async () => {
    const hm = new HookManager();
    const called = [];
    hm.on('a', async () => { called.push(1); });
    hm.on('a', async () => { called.push(2); });
    await hm.emitSequential('a', {});
    expect(called).toEqual([1,2]);
  });
});
