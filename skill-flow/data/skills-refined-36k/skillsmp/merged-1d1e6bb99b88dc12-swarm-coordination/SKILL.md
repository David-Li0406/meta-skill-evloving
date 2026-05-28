---
name: swarm-coordination
description: Use this skill for multi-agent coordination in OpenCode swarm workflows, especially when tasks benefit from parallelization or require managing task decomposition.
---

# Swarm Coordination

This skill provides guidance for effective multi-agent coordination in OpenCode swarm workflows.

## When to Use Swarm Coordination

Use swarm coordination when:

- A task has multiple independent subtasks that can run in parallel.
- The task requires different specializations (e.g., frontend + backend + tests).
- Work can be divided by file/module boundaries.
- Time-to-completion matters and parallelization helps.

Avoid swarming for:

- Tasks involving 1-2 files.
- Heavy sequential dependencies.
- Situations where coordination overhead exceeds the benefit.

## MANDATORY: Swarm Mail

**ALL coordination MUST use `swarmmail_*` tools.** This is non-negotiable.

Swarm Mail is embedded (no external server needed) and provides:

- File reservations to prevent conflicts.
- Message passing between agents.
- Thread-based coordination tied to cells.

## Worker Survival Checklist (MANDATORY)

Every swarm worker MUST follow these steps:

```typescript
// 1. INITIALIZE - Register with Swarm Mail
swarmmail_init({
  project_path: "/abs/path/to/project",
  task_description: "bead-id: Task description"
});

// 2. QUERY LEARNINGS - Check what past agents learned
semantic_memory_find({
  query: "task keywords domain",
  limit: 5
});

// 3. LOAD SKILLS - Get domain expertise
skills_list();
skills_use({ name: "relevant-skill" });

// 4. RESERVE FILES - Claim exclusive ownership
swarmmail_reserve({
  paths: ["src/assigned/**"],
  reason: "bead-id: What I'm working on",
  ttl_seconds: 3600
});

// 5. DO WORK
// ... implement changes ...

// 6. REPORT PROGRESS - Every 30min or at milestones
swarm_progress({
  project_key: "/abs/path/to/project",
  agent_name: "WorkerName",
  bead_id: "bd-123.4",
  status: "in_progress",
  message: "Auth service 80% complete, testing remaining",
  progress_percent: 80
});

// 7. CHECKPOINT - Before risky operations
swarm_checkpoint({
  bead_id: "bd-123.4",
  checkpoint_name: "pre-refactor",
  reason: "About to refactor auth flow"
});

// 8. STORE LEARNINGS - Capture what you discovered
semantic_memory_store({
  information: "OAuth refresh tokens need 5min buffer...",
  metadata: "auth, oauth, tokens"
});

// 9. COMPLETE - Auto-releases, runs UBS, records outcome
swarm_complete({
  project_key: "/abs/path/to/project",
  agent_name: "WorkerName",
  bead_id: "bd-123.4",
  summary: "Auth service implemented with JWT",
  files_touched: ["src/auth/service.ts", "src/auth/schema.ts"]
});
```

## Task Decomposition Strategy

### 1. Analyze the Task

Before decomposing, understand:

- What are the distinct units of work?
- Which parts can run in parallel vs sequentially?
- What are the file/module boundaries?
- Are there shared resources that need coordination?

### 2. Choose a Decomposition Strategy

**Parallel Strategy** - For independent subtasks:

```text
Parent Task: "Add user authentication"
├── Subtask 1: "Create auth API endpoints" (backend)
├── Subtask 2: "Build login/signup forms" (frontend)
├── Subtask 3: "Write auth integration tests" (testing)
└── Subtask 4: "Add auth documentation" (docs)
```

**Sequential Strategy** - When order matters:

```text
Parent Task: "Migrate database schema"
├── Step 1: "Create migration files"
├── Step 2: "Update model definitions"
├── Step 3: "Run migrations"
└── Step 4: "Verify data integrity"
```

**Hybrid Strategy** - Mixed dependencies:

```text
Parent Task: "Add feature X"
├── Phase 1 (parallel):
│   ├── Subtask A: "Design API"
│   └── Subtask B: "Design UI mockups"
├── Phase 2 (sequential, after Phase 1):
│   └── Subtask C: "Implement based on designs"
└── Phase 3 (parallel):
    ├── Subtask D: "Write tests"
    └── Subtask E: "Update docs"
```

## File Reservation Protocol

When multiple agents work on the same codebase:

1. **Initialize Swarm Mail first** - Use `swarmmail_init` before any work.
2. **Reserve files before editing** - Use `swarmmail_reserve` to claim files.
3. **Respect reservations** - Don't edit files reserved by other agents.
4. **Release when done** - Use `swarmmail_release` or let `swarm_complete` handle it.
5. **Coordinate on shared files** - If you must edit a reserved file, send a message to the owning agent.

## Communication Patterns

### Broadcasting Updates

```typescript
swarmmail_send({
  to: ["*"],
  subject: "API Complete",
  body: "Completed API endpoints, ready for frontend integration",
  thread_id: epic_id,
});
```

### Direct Coordination

```typescript
swarmmail_send({
  to: ["frontend-agent"],
  subject: "Auth API Spec",
  body: "Auth API is at /api/auth/*, here's the spec...",
  thread_id: epic_id,
});
```

### Checking for Messages

```typescript
// Check inbox (max 5, no bodies for context safety)
const inbox = await swarmmail_inbox();

// Read specific message body
const message = await swarmmail_read_message({ message_id: N });
```

### Reporting Blockers

```typescript
swarmmail_send({
  to: ["coordinator"],
  subject: "BLOCKED: Need DB schema",
  body: "Can't proceed without users table",
  thread_id: epic_id,
  importance: "urgent",
});
```

## Best Practices

1. **Initialize Swarm Mail first** - Always call `swarmmail_init` before any work.
2. **Small, focused subtasks** - Each subtask should be completable in one agent session.
3. **Clear boundaries** - Define exactly what files/modules each subtask touches.
4. **Explicit handoffs** - When one task enables another, communicate clearly.
5. **Graceful failures** - If a subtask fails, don't block the whole swarm.
6. **Progress updates** - Use beads to track subtask status.
7. **Load relevant skills** - Workers should call `skills_use()` based on their task type.

## Swarm Mail Quick Reference

| Tool                     | Purpose                             |
| ------------------------ | ----------------------------------- |
| `swarmmail_init`         | Initialize session (REQUIRED FIRST) |
| `swarmmail_send`         | Send message to agents              |
| `swarmmail_inbox`        | Check inbox (max 5, no bodies)      |
| `swarmmail_read_message` | Read specific message body          |
| `swarmmail_reserve`      | Reserve files for exclusive editing |
| `swarmmail_release`      | Release file reservations           |
| `swarmmail_ack`          | Acknowledge message                 |
| `swarmmail_health`       | Check database health               |

## Conclusion

This skill provides a comprehensive framework for coordinating multiple agents in OpenCode swarm workflows, ensuring efficient task management and communication. Follow the guidelines to maximize productivity and minimize conflicts in collaborative environments.