-- NTM State Store: Metrics Schema
-- Version: 002
-- Description: Creates tables for success metrics tracking

-- Metrics counters: tracks counts for various metric types
CREATE TABLE IF NOT EXISTS metric_counters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT REFERENCES sessions(id) ON DELETE CASCADE,
    metric_name TEXT NOT NULL,
    tool TEXT,
    operation TEXT,
    count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_metric_counters_session_id ON metric_counters(session_id);
CREATE INDEX IF NOT EXISTS idx_metric_counters_metric_name ON metric_counters(metric_name);
CREATE INDEX IF NOT EXISTS idx_metric_counters_tool ON metric_counters(tool);
CREATE UNIQUE INDEX IF NOT EXISTS idx_metric_counters_unique
    ON metric_counters(session_id, metric_name, COALESCE(tool, ''), COALESCE(operation, ''));

-- Latency samples: stores latency measurements
CREATE TABLE IF NOT EXISTS metric_latencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT REFERENCES sessions(id) ON DELETE CASCADE,
    operation TEXT NOT NULL,
    duration_ms REAL NOT NULL,
    recorded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_metric_latencies_session_id ON metric_latencies(session_id);
CREATE INDEX IF NOT EXISTS idx_metric_latencies_operation ON metric_latencies(operation);
CREATE INDEX IF NOT EXISTS idx_metric_latencies_recorded_at ON metric_latencies(recorded_at);

-- Blocked commands: tracks commands that were blocked
CREATE TABLE IF NOT EXISTS blocked_commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT REFERENCES sessions(id) ON DELETE CASCADE,
    agent_id TEXT REFERENCES agents(id) ON DELETE SET NULL,
    command TEXT NOT NULL,
    reason TEXT NOT NULL,
    blocked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_blocked_commands_session_id ON blocked_commands(session_id);
CREATE INDEX IF NOT EXISTS idx_blocked_commands_agent_id ON blocked_commands(agent_id);
CREATE INDEX IF NOT EXISTS idx_blocked_commands_blocked_at ON blocked_commands(blocked_at);

-- File conflicts: tracks file reservation conflicts
CREATE TABLE IF NOT EXISTS file_conflicts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT REFERENCES sessions(id) ON DELETE CASCADE,
    requesting_agent_id TEXT REFERENCES agents(id) ON DELETE SET NULL,
    holding_agent_id TEXT REFERENCES agents(id) ON DELETE SET NULL,
    path_pattern TEXT NOT NULL,
    conflict_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_file_conflicts_session_id ON file_conflicts(session_id);
CREATE INDEX IF NOT EXISTS idx_file_conflicts_conflict_at ON file_conflicts(conflict_at);

-- Metric snapshots: stores periodic snapshots for comparison
CREATE TABLE IF NOT EXISTS metric_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT REFERENCES sessions(id) ON DELETE CASCADE,
    snapshot_name TEXT NOT NULL,
    snapshot_data TEXT NOT NULL,  -- JSON blob of all metrics
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_metric_snapshots_session_id ON metric_snapshots(session_id);
CREATE INDEX IF NOT EXISTS idx_metric_snapshots_snapshot_name ON metric_snapshots(snapshot_name);
CREATE INDEX IF NOT EXISTS idx_metric_snapshots_created_at ON metric_snapshots(created_at);
