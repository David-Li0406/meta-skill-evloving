-- NTM State Store: Bead History Schema
-- Version: 003
-- Description: Creates table for tracking bead state transitions

-- Bead history: tracks all state transitions for beads/assignments
CREATE TABLE IF NOT EXISTS bead_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT REFERENCES sessions(id) ON DELETE CASCADE,
    bead_id TEXT NOT NULL,
    bead_title TEXT,
    from_status TEXT,  -- NULL for initial assignment
    to_status TEXT NOT NULL,
    agent_id TEXT REFERENCES agents(id) ON DELETE SET NULL,
    agent_type TEXT,  -- cc, cod, gmi
    agent_name TEXT,  -- Agent Mail name
    pane INTEGER,
    trigger TEXT,  -- What caused the transition (e.g., "user_assign", "agent_complete", "crash", "retry")
    reason TEXT,  -- Additional context (e.g., failure reason)
    prompt_sent TEXT,  -- Prompt at time of assignment (for assigned transitions)
    retry_count INTEGER DEFAULT 0,
    transition_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_bead_history_session_id ON bead_history(session_id);
CREATE INDEX IF NOT EXISTS idx_bead_history_bead_id ON bead_history(bead_id);
CREATE INDEX IF NOT EXISTS idx_bead_history_agent_id ON bead_history(agent_id);
CREATE INDEX IF NOT EXISTS idx_bead_history_to_status ON bead_history(to_status);
CREATE INDEX IF NOT EXISTS idx_bead_history_transition_at ON bead_history(transition_at);

-- Composite index for querying bead timeline
CREATE INDEX IF NOT EXISTS idx_bead_history_bead_timeline
    ON bead_history(bead_id, transition_at);

-- Composite index for session + status queries
CREATE INDEX IF NOT EXISTS idx_bead_history_session_status
    ON bead_history(session_id, to_status);
