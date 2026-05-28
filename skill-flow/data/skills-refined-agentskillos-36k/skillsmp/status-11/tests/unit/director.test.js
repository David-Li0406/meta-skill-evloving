const path = require('path');

describe('Director core', () => {
  let Director;

  beforeEach(() => {
    jest.resetModules();

    // Provide minimal browser/globals the module expects when running in Node
    global.window = global.window || {};
    global.window.Telemetry = { emit: jest.fn() };

    // Simple sessionStorage mock
    const store = new Map();
    global.sessionStorage = {
      getItem: (k) => (store.has(k) ? store.get(k) : null),
      setItem: (k, v) => store.set(k, String(v)),
      removeItem: (k) => store.delete(k),
      clear: () => store.clear(),
    };

    // Default ProposalValidator that approves
    global.window.ProposalValidator = {
      quickValidate: jest.fn(() => ({ valid: true }))
    };

    jest.isolateModules(() => {
      Director = require(path.join(process.cwd(), 'web/demo/js/director.js'));
    });
  });

  afterEach(() => {
    // clean up any globals we set
    delete global.window.__proposalValidReturnPaths;
    delete global.sessionStorage;
  });

  it('approves a low-risk proposal and returns latencyMs', async () => {
    const story = {
      mainContentContainer: { _namedContent: { campfire: {} } }
    };

    const proposal = {
      content: { text: 'Short content', return_path: 'campfire' },
      metadata: { confidence_score: 0.9 }
    };

    const res = await Director.evaluate(proposal, { story }, { riskThreshold: 0.5 });

    expect(res).toHaveProperty('decision', 'approve');
    expect(typeof res.riskScore).toBe('number');
    expect(res.riskScore).toBeLessThanOrEqual(0.5);
    expect(typeof res.latencyMs).toBe('number');
    expect(res.latencyMs).toBeGreaterThanOrEqual(0);
  });

  it('rejects when ProposalValidator fails', async () => {
    // make the validator fail
    global.window.ProposalValidator.quickValidate.mockReturnValueOnce({ valid: false, reason: 'Blocked by policy' });

    const proposal = { content: { text: 'x' }, metadata: { confidence_score: 0.5 } };

    const res = await Director.evaluate(proposal, {}, { riskThreshold: 0.5 });

    expect(res).toHaveProperty('decision', 'reject');
    expect(res).toHaveProperty('reason');
    expect(res.reason).toMatch(/Blocked|policy|Failed/i);
    expect(res.riskScore).toBe(1.0);
    expect(res.latencyMs).toBeGreaterThanOrEqual(0);
  });

  it('fails validation with reason "Failed policy validation" on invalid schema', async () => {
    global.window.ProposalValidator.quickValidate.mockReturnValueOnce({ valid: false, reason: 'Failed policy validation' });
    const proposal = { content: { text: 'x' }, metadata: { confidence_score: 0.5 } };
    const res = await Director.evaluate(proposal, {}, { riskThreshold: 0.5 });
    expect(res.decision).toBe('reject');
    expect(res.reason).toBe('Failed policy validation');
    expect(res.latencyMs).toBeGreaterThanOrEqual(0);
  });

  it('throws on malformed proposal (non-object)', async () => {
    await expect(Director.evaluate(null)).rejects.toThrow('Malformed proposal');
  });

  it('checkReturnPath recognizes named knots on story', () => {
    const story = { mainContentContainer: { _namedContent: { campfire: {}, elsewhere: {} } } };

    const ok = Director.checkReturnPath('campfire', story);
    expect(ok.feasible).toBe(true);
    expect(ok.confidence).toBe(0.9);
    expect(ok.reason).toMatch(/exists/);

    const bad = Director.checkReturnPath('nonexistent_knot_xyz', story);
    expect(bad.feasible).toBe(false);
    expect(bad.confidence).toBe(0.0);
    expect(bad.reason).toMatch(/does not exist/);
  });

  it('checkReturnPath falls back to __proposalValidReturnPaths', () => {
    // no story shape
    global.window.__proposalValidReturnPaths = ['alpha', 'beta'];

    const ok = Director.checkReturnPath('alpha', null);
    expect(ok.feasible).toBe(true);

    const bad = Director.checkReturnPath('gamma', null);
    expect(bad.feasible).toBe(false);
  });

  it('checkReturnPath completes within 50ms for existence checks', () => {
    const story = { mainContentContainer: { _namedContent: { campfire: {}, elsewhere: {} } } };
    const iterations = 200;
    const start = performance.now();
    for (let i = 0; i < iterations; i += 1) {
      Director.checkReturnPath('campfire', story);
      Director.checkReturnPath('missing_knot', story);
    }
    const duration = performance.now() - start;
    expect(duration).toBeLessThan(50);
  }, 100);

  it('computeRiskScore is deterministic and sensitive to confidence', () => {
    const pHigh = { metadata: { confidence_score: 0.95 }, content: { text: 'short' } };
    const pLow = { metadata: { confidence_score: 0.2 }, content: { text: 'short' } };

    const s1 = Director.computeRiskScore(pHigh, { returnPathCheck: { confidence: 0.9 } }, {});
    const s2 = Director.computeRiskScore(pHigh, { returnPathCheck: { confidence: 0.9 } }, {});
    const sLow = Director.computeRiskScore(pLow, { returnPathCheck: { confidence: 0.9 } }, {});

    expect(s1).toBeCloseTo(s2);
    expect(sLow).toBeGreaterThanOrEqual(s1);
  });

  it('produces low risk for high-confidence proposals', () => {
    const proposal = { metadata: { confidence_score: 0.9 }, content: { text: 'concise' } };
    const score = Director.computeRiskScore(proposal, { returnPathCheck: { confidence: 0.9 } }, {});
    expect(score).toBeLessThan(0.3);
  });

  it('produces high risk for low-confidence proposals', () => {
    const proposal = { metadata: { confidence_score: 0.3 }, content: { text: 'concise' } };
    const score = Director.computeRiskScore(proposal, { returnPathCheck: { confidence: 0.9 } }, {});
    expect(score).toBeGreaterThan(0.5);
  });

  it('elevates pacing risk for long exposition branches', () => {
    const shortProposal = { metadata: { confidence_score: 0.6 }, content: { text: 'concise text' } };
    const longProposal = { metadata: { confidence_score: 0.6 }, content: { text: 'long '.repeat(220) } }; // ~1100 chars
    const expositionCtx = { returnPathCheck: { confidence: 0.9 }, phase: 'exposition' };

    const shortScore = Director.computeRiskScore(shortProposal, expositionCtx, {});
    const longScore = Director.computeRiskScore(longProposal, expositionCtx, {});
    const climaxScore = Director.computeRiskScore(longProposal, { ...expositionCtx, phase: 'climax' }, {});

    expect(longScore).toBeGreaterThan(shortScore);
    expect(longScore).toBeGreaterThan(climaxScore);
    expect(longScore).toBeGreaterThan(0.35);
  });

  it('is deterministic across repeated calls (10 runs)', () => {
    const proposal = { metadata: { confidence_score: 0.7 }, content: { text: 'stable content' } };
    const context = { returnPathCheck: { confidence: 0.9 } };
    const scores = Array.from({ length: 10 }, () => Director.computeRiskScore(proposal, context, {}));
    const first = scores[0];
    scores.forEach(s => expect(s).toBeCloseTo(first));
  });

  it('approves high-confidence short proposal when fallback return paths include it', async () => {
    // ensure fallback list is present (no story shape available)
    global.window.__proposalValidReturnPaths = ['pines'];

    const proposal = {
      content: { text: 'Short safe content', return_path: 'pines' },
      metadata: { confidence_score: 0.99 }
    };

    const res = await Director.evaluate(proposal, {}, { riskThreshold: 0.8 });
    expect(res.decision).toBe('approve');
    expect(res.riskScore).toBeLessThanOrEqual(0.8);
  });

  it('rejects proposal when return_path is invalid (missing knot)', async () => {
    const story = { mainContentContainer: { _namedContent: { campfire: {} } } };
    const proposal = {
      content: { text: 'This is low confidence content', return_path: 'nonexistent_knot_xyz' },
      metadata: { confidence_score: 0.8 }
    };

    const res = await Director.evaluate(proposal, { story }, { riskThreshold: 0.9 });
    expect(res.decision).toBe('reject');
    expect(res.reason).toMatch(/Return path knot does not exist|return path check failed/i);
  });

  it('rejects low-confidence proposal without return_path or valid fallback', async () => {
    // Ensure no fallback and no story
    delete global.window.__proposalValidReturnPaths;

    const proposal = {
      content: { text: 'This is low confidence content', return_path: null },
      metadata: { confidence_score: 0.05 }
    };

    const res = await Director.evaluate(proposal, {}, { riskThreshold: 0.5 });
    expect(res.decision).toBe('reject');
    expect(res.reason).toMatch(/Return path check failed|Unable to verify return path/);
  });

  it('evaluate respects a very low threshold and rejects accordingly', async () => {
    const story = { mainContentContainer: { _namedContent: { campfire: {} } } };
    const proposal = { content: { text: 'This is somewhat long content '.repeat(40), return_path: 'campfire' }, metadata: { confidence_score: 0.5 } };

    // Set threshold extremely low so even modest risk should reject
    const res = await Director.evaluate(proposal, { story }, { riskThreshold: 0.01 });
    expect(res.decision).toBe('reject');
    expect(res.riskScore).toBeGreaterThan(0.01);
  });

  it('emits telemetry event on decision', async () => {
    const story = { mainContentContainer: { _namedContent: { campfire: {} } } };
    const proposal = { content: { text: 'Short content', return_path: 'campfire' }, metadata: { confidence_score: 0.9 } };

    await Director.evaluate(proposal, { story }, { riskThreshold: 0.5 });

    expect(global.window.Telemetry.emit).toHaveBeenCalled();
    const calls = global.window.Telemetry.emit.mock.calls;
    const directorCalls = calls.filter(c => c[0] === 'director_decision');
    expect(directorCalls.length).toBeGreaterThan(0);
    const payload = directorCalls[0][1];
    expect(payload).toHaveProperty('decision');
  });

  it('telemetry payload includes required fields and ISO timestamp; fills missing proposal_id; buffers 5 decisions', async () => {
    const story = { mainContentContainer: { _namedContent: { campfire: {} } } };
    const baseProposal = { content: { text: 'Short content', return_path: 'campfire' }, metadata: { confidence_score: 0.9 } };

    const payloads = [];
    for (let i = 0; i < 5; i += 1) {
      const proposal = { ...baseProposal, id: i === 0 ? undefined : `p-${i}` };
      const res = await Director.evaluate(proposal, { story }, { riskThreshold: 0.5 });
      expect(res).toHaveProperty('decision');
      const calls = global.window.Telemetry.emit.mock.calls.filter(c => c[0] === 'director_decision');
      const call = calls[calls.length - 1];
      expect(call).toBeTruthy();
      const payload = call[1];
      payloads.push(payload);
    }

    // Required fields
    payloads.forEach((p) => {
      expect(p).toHaveProperty('proposal_id');
      expect(p).toHaveProperty('decision');
      expect(p).toHaveProperty('reason');
      expect(p).toHaveProperty('riskScore');
      expect(p).toHaveProperty('latencyMs');
      expect(p).toHaveProperty('writerMs');
      expect(p).toHaveProperty('directorMs');
      expect(p).toHaveProperty('totalMs');
      expect(p).toHaveProperty('timestamp');
      expect(p).toHaveProperty('metrics');

      // Timestamp is valid ISO8601
      expect(() => new Date(p.timestamp).toISOString()).not.toThrow();
    });

    // First call had no proposal.id; ensure uuid filled
    expect(payloads[0].proposal_id).toMatch(/^uuid-|^[0-9a-f]{8}-/i);

    // sessionStorage contains 5 events
    const stored = JSON.parse(global.sessionStorage.getItem('ge-hch.director.telemetry') || '[]');
    expect(stored.length).toBe(5);
  });

});
