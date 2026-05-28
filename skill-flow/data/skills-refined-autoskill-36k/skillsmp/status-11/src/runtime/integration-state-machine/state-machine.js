// Minimal deterministic 12-state integration state machine

const STATES = Object.freeze({
  ProposalAccepted: 'ProposalAccepted',
  PreInjectCheckpoint: 'PreInjectCheckpoint',
  Injecting: 'Injecting',
  Executing: 'Executing',
  CheckpointOnBeat: 'CheckpointOnBeat',
  CommitPending: 'CommitPending',
  Committed: 'Committed',
  RollbackPending: 'RollbackPending',
  RollingBack: 'RollingBack',
  RolledBack: 'RolledBack',
  TerminalSuccess: 'TerminalSuccess',
  TerminalFailure: 'TerminalFailure'
});

class IntegrationStateMachine {
  constructor(logger = console) {
    this.state = null;
    this.logger = logger;
  }

  _logTransition(from, to, meta) {
    const entry = { ts: new Date().toISOString(), from, to, meta };
    if (this.logger && typeof this.logger.log === 'function') this.logger.log('[state]', JSON.stringify(entry));
    return entry;
  }

  // Initialize the machine into the first state
  start() {
    if (this.state !== null) throw new Error('State machine already started');
    this.state = STATES.ProposalAccepted;
    this._logTransition(null, this.state);
    return this.state;
  }

  transition(next, meta = {}) {
    const from = this.state;
    // Define allowed transitions
    const allowed = new Map([
      [STATES.ProposalAccepted, [STATES.PreInjectCheckpoint, STATES.TerminalFailure]],
      [STATES.PreInjectCheckpoint, [STATES.Injecting, STATES.RollbackPending]],
      [STATES.Injecting, [STATES.Executing, STATES.RollbackPending]],
      [STATES.Executing, [STATES.CheckpointOnBeat, STATES.RollbackPending, STATES.TerminalFailure]],
      [STATES.CheckpointOnBeat, [STATES.CommitPending, STATES.RollbackPending]],
      [STATES.CommitPending, [STATES.Committed, STATES.RollbackPending]],
      [STATES.Committed, [STATES.TerminalSuccess, STATES.RollbackPending]],
      [STATES.RollbackPending, [STATES.RollingBack]],
      [STATES.RollingBack, [STATES.RolledBack]],
      [STATES.RolledBack, [STATES.TerminalFailure, STATES.TerminalSuccess]],
      [STATES.TerminalSuccess, []],
      [STATES.TerminalFailure, []]
    ]);

    const allowedNext = allowed.get(from) || [];
    if (!allowedNext.includes(next)) throw new Error(`Invalid transition from ${from} to ${next}`);

    this.state = next;
    const log = this._logTransition(from, next, meta);
    return log;
  }

  serialize() {
    return { state: this.state };
  }

  static STATES = STATES;
}

module.exports = IntegrationStateMachine;
