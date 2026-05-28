const path = require('path');

describe('Director telemetry emitter', () => {
  let Director;
  let store;

  beforeEach(() => {
    jest.resetModules();
    store = {};

    global.sessionStorage = {
      getItem: (key) => Object.prototype.hasOwnProperty.call(store, key) ? store[key] : null,
      setItem: (key, value) => { store[key] = String(value); },
      removeItem: (key) => { delete store[key]; }
    };

    global.window = global.window || {};
    global.window.Telemetry = { emit: jest.fn() };
    global.window.ProposalValidator = {
      quickValidate: jest.fn(() => ({ valid: true }))
    };

    jest.isolateModules(() => {
      Director = require(path.join(process.cwd(), 'web/demo/js/director.js'));
    });
  });

  afterEach(() => {
    delete global.window;
    delete global.sessionStorage;
  });

  it('emits director_decision with required fields and valid timestamp', () => {
    const payload = {
      proposal_id: 'p-123',
      decision: 'approve',
      reason: 'Risk acceptable',
      riskScore: 0.2,
      latencyMs: 12,
      writerMs: 5,
      directorMs: 7,
      totalMs: 12,
      metrics: { confidence: 0.9, pacing: 0.1, returnPath: 0.8 }
    };

    Director.emitDecisionTelemetry(payload);

    expect(global.window.Telemetry.emit).toHaveBeenCalledWith(
      'director_decision',
      expect.objectContaining({
        proposal_id: 'p-123',
        decision: 'approve',
        reason: 'Risk acceptable',
        riskScore: 0.2,
        latencyMs: 12,
        writerMs: 5,
        directorMs: 7,
        totalMs: 12
      })
    );

    const emitted = global.window.Telemetry.emit.mock.calls[0][1];
    expect(emitted.metrics).toMatchObject({
      confidence: 0.9,
      pacing: 0.1,
      returnPath: 0.8
    });
    expect(emitted).toHaveProperty('timestamp');
    expect(Number.isNaN(Date.parse(emitted.timestamp))).toBe(false);
    expect(typeof emitted.writerMs).toBe('number');
    expect(typeof emitted.directorMs).toBe('number');
    expect(typeof emitted.totalMs).toBe('number');

    const buffered = JSON.parse(sessionStorage.getItem('ge-hch.director.telemetry'));
    expect(buffered).toHaveLength(1);
    expect(buffered[0].proposal_id).toBe('p-123');
  });

  it('generates a UUID when proposal_id is missing', () => {
    Director.emitDecisionTelemetry({
      decision: 'reject',
      reason: 'Missing proposal id',
      riskScore: 1.0,
      latencyMs: 3,
      writerMs: 0,
      directorMs: 3,
      totalMs: 3,
      metrics: { confidence: 0.1, pacing: 0.2, returnPath: 0.3 }
    });

    const emitted = global.window.Telemetry.emit.mock.calls[0][1];
    expect(emitted.proposal_id).toBeTruthy();
    // Should generate a uuid (either native crypto or fallback prefix)
    expect(typeof emitted.proposal_id).toBe('string');
    expect(typeof emitted.writerMs).toBe('number');
    expect(typeof emitted.directorMs).toBe('number');
    expect(typeof emitted.totalMs).toBe('number');
  });

  it('caps the sessionStorage buffer at 50 events', () => {
    for (let i = 0; i < 55; i += 1) {
      Director.emitDecisionTelemetry({
        proposal_id: `p-${i + 1}`,
        decision: 'approve',
        reason: 'ok',
        riskScore: 0.1,
        latencyMs: 1,
        writerMs: 0,
        directorMs: 1,
        totalMs: 1,
        metrics: { confidence: 0.5, pacing: 0.1, returnPath: 0.9 }
      });
    }

    const buffered = JSON.parse(sessionStorage.getItem('ge-hch.director.telemetry'));
    expect(buffered).toHaveLength(50);
    expect(buffered[0].proposal_id).toBe('p-6');
    expect(buffered[49].proposal_id).toBe('p-55');
    buffered.forEach((entry) => {
      expect(typeof entry.writerMs).toBe('number');
      expect(typeof entry.directorMs).toBe('number');
      expect(typeof entry.totalMs).toBe('number');
    });
  });

  it('evaluate emits telemetry and buffers entries after multiple choices', async () => {
    const story = { mainContentContainer: { _namedContent: { campfire: {} } } };
    const proposals = Array.from({ length: 5 }).map((_, i) => ({
      id: `p-eval-${i + 1}`,
      content: { text: 'Short content', return_path: 'campfire' },
      metadata: { confidence_score: 0.95 }
    }));

    for (const proposal of proposals) {
      await Director.evaluate(proposal, { story }, { riskThreshold: 0.9, writerMs: 4 });
    }

    const buffered = JSON.parse(sessionStorage.getItem('ge-hch.director.telemetry'));
    expect(buffered).toHaveLength(5);
    buffered.forEach((entry) => {
      expect(entry).toHaveProperty('proposal_id');
      expect(entry).toHaveProperty('decision');
      expect(entry.metrics).toBeDefined();
      expect(typeof entry.writerMs).toBe('number');
      expect(typeof entry.directorMs).toBe('number');
      expect(typeof entry.totalMs).toBe('number');
      expect(entry.totalMs).toBe(entry.writerMs + entry.directorMs);
    });
  });
});
