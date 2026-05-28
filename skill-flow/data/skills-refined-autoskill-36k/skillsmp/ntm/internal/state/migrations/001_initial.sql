-- NTM State Store: Initial Schema
-- Version: 001
-- Description: Creates all tables for NTM orchestration state

-- Sessions table: tracks NTM orchestration sessions
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    project_path TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'active',  -- active, paused, terminated
    config_snapshot TEXT,  -- JSON of config at spawn time
    coordinator_agent TEXT -- Agent Mail name of coordinator
);

CREATE INDEX IF NOT EXISTS idx_sessions_name ON sessions(name);
CREATE INDEX IF NOT EXISTS idx_sessions_status ON sessions(status);
CREATE INDEX IF NOT EXISTS idx_sessions_project_path ON sessions(project_path);

-- Agents table: tracks AI agents within sessions
CREATE TABLE IF NOT EXISTS agents (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    name TEXT NOT NULL,  -- Agent Mail name (e.g., "GreenLake")
    type TEXT NOT NULL,  -- cc, cod, gmi
    model TEXT,
    tmux_pane_id TEXT,
    last_seen TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'idle',  -- idle, working, error, crashed
    current_task_id TEXT,
    performance_data TEXT,  -- JSON of performance stats
    UNIQUE(session_id, name)
);

CREATE INDEX IF NOT EXISTS idx_agents_session_id ON agents(session_id);
CREATE INDEX IF NOT EXISTS idx_agents_type ON agents(type);
CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);
CREATE INDEX IF NOT EXISTS idx_agents_name ON agents(name);

-- Tasks table: tracks units of work assigned to agents
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    agent_id TEXT REFERENCES agents(id) ON DELETE SET NULL,
    bead_id TEXT,
    correlation_id TEXT,
    context_pack_id TEXT,
    status TEXT NOT NULL DEFAULT 'pending',  -- pending, assigned, working, completed, failed
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    assigned_at TIMESTAMP,
    completed_at TIMESTAMP,
    result TEXT  -- success, failure, partial
);

CREATE INDEX IF NOT EXISTS idx_tasks_session_id ON tasks(session_id);
CREATE INDEX IF NOT EXISTS idx_tasks_agent_id ON tasks(agent_id);
CREATE INDEX IF NOT EXISTS idx_tasks_bead_id ON tasks(bead_id);
CREATE INDEX IF NOT EXISTS idx_tasks_correlation_id ON tasks(correlation_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);

-- Reservations table: tracks file reservations (advisory locks)
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    agent_id TEXT NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    path_pattern TEXT NOT NULL,
    exclusive INTEGER NOT NULL DEFAULT 1,  -- 0 = shared, 1 = exclusive
    correlation_id TEXT,
    reason TEXT,
    expires_at TIMESTAMP NOT NULL,
    released_at TIMESTAMP,
    force_released_by TEXT
);

CREATE INDEX IF NOT EXISTS idx_reservations_session_id ON reservations(session_id);
CREATE INDEX IF NOT EXISTS idx_reservations_agent_id ON reservations(agent_id);
CREATE INDEX IF NOT EXISTS idx_reservations_path_pattern ON reservations(path_pattern);
CREATE INDEX IF NOT EXISTS idx_reservations_expires_at ON reservations(expires_at);

-- Approvals table: tracks pending approval requests for sensitive actions
CREATE TABLE IF NOT EXISTS approvals (
    id TEXT PRIMARY KEY,
    action TEXT NOT NULL,
    resource TEXT NOT NULL,
    reason TEXT,
    requested_by TEXT NOT NULL,
    correlation_id TEXT,
    requires_slb INTEGER NOT NULL DEFAULT 0,  -- 0 = no, 1 = yes ("Stop, Look, Broadcast")
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',  -- pending, approved, denied, expired
    approved_by TEXT,
    approved_at TIMESTAMP,
    denied_reason TEXT
);

CREATE INDEX IF NOT EXISTS idx_approvals_status ON approvals(status);
CREATE INDEX IF NOT EXISTS idx_approvals_requested_by ON approvals(requested_by);
CREATE INDEX IF NOT EXISTS idx_approvals_expires_at ON approvals(expires_at);
CREATE INDEX IF NOT EXISTS idx_approvals_correlation_id ON approvals(correlation_id);

-- Context packs table: tracks pre-built context prompts for tasks
CREATE TABLE IF NOT EXISTS context_packs (
    id TEXT PRIMARY KEY,
    bead_id TEXT NOT NULL,
    agent_type TEXT NOT NULL,  -- cc, cod, gmi
    repo_rev TEXT NOT NULL,
    correlation_id TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    token_count INTEGER,
    rendered_prompt TEXT
);

CREATE INDEX IF NOT EXISTS idx_context_packs_bead_id ON context_packs(bead_id);
CREATE INDEX IF NOT EXISTS idx_context_packs_agent_type ON context_packs(agent_type);
CREATE INDEX IF NOT EXISTS idx_context_packs_correlation_id ON context_packs(correlation_id);

-- Tool health table: tracks health status of ecosystem tools
CREATE TABLE IF NOT EXISTS tool_health (
    tool TEXT PRIMARY KEY,
    version TEXT,
    capabilities TEXT,  -- JSON array
    last_ok TIMESTAMP,
    last_error TEXT
);

-- Event log table: stores all events for replay/debugging
CREATE TABLE IF NOT EXISTS event_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT REFERENCES sessions(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL,
    event_data TEXT NOT NULL,  -- JSON payload
    correlation_id TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_event_log_session_id ON event_log(session_id);
CREATE INDEX IF NOT EXISTS idx_event_log_event_type ON event_log(event_type);
CREATE INDEX IF NOT EXISTS idx_event_log_correlation_id ON event_log(correlation_id);
CREATE INDEX IF NOT EXISTS idx_event_log_created_at ON event_log(created_at);
