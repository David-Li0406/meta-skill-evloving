const IntegrationStateMachine = require('../../src/runtime/integration-state-machine/state-machine');

describe('IntegrationStateMachine', () => {
  test('start and allowed transitions', () => {
    const sm = new IntegrationStateMachine({ log: () => {} });
    expect(sm.state).toBe(null);
    sm.start();
    expect(sm.state).toBe(IntegrationStateMachine.STATES.ProposalAccepted);
    // valid transition
    const log = sm.transition(IntegrationStateMachine.STATES.PreInjectCheckpoint);
    expect(log.from).toBe(IntegrationStateMachine.STATES.ProposalAccepted);
    expect(sm.state).toBe(IntegrationStateMachine.STATES.PreInjectCheckpoint);
  });

  test('invalid transition throws', () => {
    const sm = new IntegrationStateMachine({ log: () => {} });
    sm.start();
    expect(() => sm.transition(IntegrationStateMachine.STATES.Committed)).toThrow();
  });

  test('full happy path to committed', () => {
    const sm = new IntegrationStateMachine({ log: () => {} });
    sm.start();
    sm.transition(IntegrationStateMachine.STATES.PreInjectCheckpoint);
    sm.transition(IntegrationStateMachine.STATES.Injecting);
    sm.transition(IntegrationStateMachine.STATES.Executing);
    sm.transition(IntegrationStateMachine.STATES.CheckpointOnBeat);
    sm.transition(IntegrationStateMachine.STATES.CommitPending);
    sm.transition(IntegrationStateMachine.STATES.Committed);
    expect(sm.state).toBe(IntegrationStateMachine.STATES.Committed);
  });
});
