const HookManager = require('../../src/runtime/hook-manager');
const createTelemetrySubscriber = require('../../src/runtime/subscribers/telemetry');
const createPersistenceSubscriber = require('../../src/runtime/subscribers/persistence');
const fs = require('fs');
const path = require('path');

describe('runtime subscribers integration', () => {
  test('telemetry and persistence subscribers register and respond non-blocking', async () => {
    const hm = new HookManager();
    const telemetry = createTelemetrySubscriber({ log: () => {} });
    const persistence = createPersistenceSubscriber();

    hm.on('pre_inject', telemetry.pre_inject);
    hm.on('post_inject', telemetry.post_inject);
    hm.on('state_change', persistence.on_state_change);

    const res = await hm.emitParallel('pre_inject', { foo: 1 });
    expect(res.some(r => r.status === 'fulfilled')).toBe(true);

    // ensure log file exists and contains at least one line after audit
    const logDir = path.join(__dirname, '../../.runtime_logs');
    const logFile = path.join(logDir, 'integration.log');
    // emit a state change
    await hm.emitParallel('state_change', { state: 'test' });
    expect(fs.existsSync(logFile)).toBe(true);
    const txt = fs.readFileSync(logFile, 'utf8');
    expect(txt.length).toBeGreaterThan(0);
  });
});
