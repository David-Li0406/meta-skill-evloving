# Track Agent Workflow

## Purpose

Maintain a history of spawned subagents in `agent-history.json` for resume capability and audit trail.

## Agent Lifecycle States

```
spawned → completed
    ↓
interrupted → resumed → completed
    ↓                      ↓
  failed              failed
```

## State Definitions

| Status | Description |
|--------|-------------|
| `spawned` | Agent started, execution in progress |
| `completed` | Agent finished successfully |
| `interrupted` | Agent stopped mid-execution (Ctrl+C, crash, etc.) |
| `resumed` | Previously interrupted agent was continued |
| `failed` | Agent encountered unrecoverable error |
| `timeout` | Agent exceeded time limit |

## Tracking Operations

### On Spawn

```typescript
interface TrackSpawnInput {
  agent_id: string;         // From Task tool result
  plan_number: string;      // e.g., "02"
  task_group: string;       // e.g., "API Endpoints"
  state_path: string;       // Path to .long-run/
}

function trackSpawn(input: TrackSpawnInput): void {
  const history_path = `${input.state_path}/agent-history.json`;

  // Read current history
  const history = JSON.parse(read_file(history_path));

  // Create new entry
  const entry = {
    agent_id: input.agent_id,
    task_description: `Execute plan ${input.plan_number}: ${input.task_group}`,
    plan: input.plan_number,
    timestamp: new Date().toISOString(),
    status: "spawned",
    completion_timestamp: null
  };

  // Add entry
  history.agents.push(entry);

  // Enforce max_agents limit
  if (history.agents.length > history.max_agents) {
    // Remove oldest completed entries first
    const completed = history.agents.filter(e =>
      e.status === 'completed' || e.status === 'failed'
    );
    if (completed.length > 0) {
      const oldest = completed[0];
      history.agents = history.agents.filter(e => e !== oldest);
    }
  }

  // Write atomically
  write_atomic(history_path, JSON.stringify(history, null, 2));

  // Write transient current-agent-id.txt
  write_file(`${input.state_path}/current-agent-id.txt`, input.agent_id);
}
```

### On Completion

```typescript
interface TrackCompleteInput {
  agent_id: string;
  state_path: string;
  status: 'completed' | 'failed' | 'timeout';
}

function trackComplete(input: TrackCompleteInput): void {
  const history_path = `${input.state_path}/agent-history.json`;

  // Read current history
  const history = JSON.parse(read_file(history_path));

  // Find and update entry
  const entry = history.agents.find(e => e.agent_id === input.agent_id);
  if (entry) {
    entry.status = input.status;
    entry.completion_timestamp = new Date().toISOString();
  }

  // Write atomically
  write_atomic(history_path, JSON.stringify(history, null, 2));

  // Clear current-agent-id.txt
  delete_file(`${input.state_path}/current-agent-id.txt`);
}
```

### On Interrupt

```typescript
function trackInterrupt(agent_id: string, state_path: string): void {
  const history_path = `${state_path}/agent-history.json`;

  const history = JSON.parse(read_file(history_path));

  const entry = history.agents.find(e => e.agent_id === agent_id);
  if (entry) {
    entry.status = "interrupted";
    entry.completion_timestamp = new Date().toISOString();
  }

  write_atomic(history_path, JSON.stringify(history, null, 2));

  // Keep current-agent-id.txt for resume detection
}
```

### On Resume

```typescript
function trackResume(old_agent_id: string, new_agent_id: string, state_path: string): void {
  const history_path = `${state_path}/agent-history.json`;

  const history = JSON.parse(read_file(history_path));

  // Mark old as resumed
  const old_entry = history.agents.find(e => e.agent_id === old_agent_id);
  if (old_entry) {
    old_entry.status = "resumed";
    old_entry.resumed_by = new_agent_id;
  }

  // Add new entry
  history.agents.push({
    agent_id: new_agent_id,
    task_description: old_entry?.task_description || "Resumed execution",
    plan: old_entry?.plan,
    timestamp: new Date().toISOString(),
    status: "spawned",
    completion_timestamp: null,
    resumes: old_agent_id
  });

  write_atomic(history_path, JSON.stringify(history, null, 2));
  write_file(`${state_path}/current-agent-id.txt`, new_agent_id);
}
```

## Query Operations

### Find Active Agent

```typescript
function findActiveAgent(state_path: string): AgentEntry | null {
  // Quick path: check transient file
  const current_id_path = `${state_path}/current-agent-id.txt`;
  if (file_exists(current_id_path)) {
    const agent_id = read_file(current_id_path).trim();

    const history = JSON.parse(read_file(`${state_path}/agent-history.json`));
    return history.agents.find(e => e.agent_id === agent_id) || null;
  }

  return null;
}
```

### Find Interrupted Agent

```typescript
function findInterruptedAgent(state_path: string): AgentEntry | null {
  const history = JSON.parse(read_file(`${state_path}/agent-history.json`));

  // Find most recent interrupted (not resumed) agent
  const interrupted = history.agents
    .filter(e => e.status === 'interrupted' || e.status === 'spawned')
    .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

  return interrupted[0] || null;
}
```

### Get Plan History

```typescript
function getPlanHistory(state_path: string, plan_number: string): AgentEntry[] {
  const history = JSON.parse(read_file(`${state_path}/agent-history.json`));

  return history.agents
    .filter(e => e.plan === plan_number)
    .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
}
```

## agent-history.json Schema

```json
{
  "version": "1.0",
  "agents": [
    {
      "agent_id": "a5023ff",
      "task_description": "Execute plan 02: API Endpoints",
      "plan": "02",
      "timestamp": "2026-01-15T14:22:10Z",
      "status": "completed",
      "completion_timestamp": "2026-01-15T14:45:32Z"
    },
    {
      "agent_id": "b7134aa",
      "task_description": "Execute plan 03: Frontend",
      "plan": "03",
      "timestamp": "2026-01-15T14:46:00Z",
      "status": "interrupted",
      "completion_timestamp": "2026-01-15T15:10:00Z"
    },
    {
      "agent_id": "c9245bb",
      "task_description": "Execute plan 03: Frontend",
      "plan": "03",
      "timestamp": "2026-01-15T15:15:00Z",
      "status": "spawned",
      "completion_timestamp": null,
      "resumes": "b7134aa"
    }
  ]
}
```

## Max Agents Enforcement

When `agents.length > 50`:

1. Find oldest agent entry with status `completed` or `failed`
2. Remove it from array
3. If no completed/failed entries, remove oldest `interrupted` that has been `resumed`
4. Never remove `spawned` entries (active agents)

## Error Handling

| Error | Action |
|-------|--------|
| agent-history.json missing | Create from template |
| Parse error | Attempt recovery from SUMMARY.md files |
| Write failure | Retry atomic write 3 times |
| Duplicate agent_id | Use timestamp to disambiguate |
