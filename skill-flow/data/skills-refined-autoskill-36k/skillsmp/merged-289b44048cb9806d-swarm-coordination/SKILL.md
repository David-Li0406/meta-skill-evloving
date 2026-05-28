---
name: swarm-coordination
description: Use this skill for multi-agent coordination in OpenCode swarm workflows, especially when tasks benefit from parallelization or require managing multiple agents and task decomposition.
---

# Swarm Coordination

This skill provides guidance for effective multi-agent coordination in OpenCode swarm workflows.

## When to Use Swarm Coordination

**DO swarm when:**

- A task touches 3+ files.
- Natural parallel boundaries exist (frontend/backend/tests).
- Different specializations are needed.
- Time-to-completion matters.

**DON'T swarm when:**

- The task is 1-2 files.
- Heavy sequential dependencies exist.
- Coordination overhead exceeds the benefit.
- A tight feedback loop is needed.

**Heuristic:** If you can describe the task in one sentence without "and", don't swarm.

## MANDATORY: Swarm Mail

**ALL coordination MUST use `swarmmail_*` tools.** This is non-negotiable.

Swarm Mail is embedded (no external server needed) and provides:

- File reservations to prevent conflicts.
- Message passing between agents.
- Thread-based coordination tied to cells.

## Worker Survival Checklist (MANDATORY)

Every swarm worker MUST follow these steps. No exceptions.

```typescript
// 1. INITIALIZE - Register with Swarm Mail
swarmmail_init({
  project_path: "/abs/path/to/project",
  task_description: "bead-id: Task description"
});

// 2. QUERY LEARNINGS - Check what past agents learned
hivemind_find({
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
hivemind_store({
  information: "OAuth refresh tokens need 5min buffer...",
  metadata: "auth, oauth, tokens"
});

// 9. COMPLETE - Auto-releases, records outcome
swarm_complete({
  project_key: "/abs/path/to/project",
  agent_name: "WorkerName",
  bead_id: "bd-123.4",
  summary: "Auth service implemented with JWT",
  files_touched: ["src/auth/service.ts", "src/auth/schema.ts"]
});
```

## Task Clarity Check (BEFORE Decomposing)

**Before decomposing, ask: Is this task clear enough to parallelize?**

### Vague Task Signals (ASK QUESTIONS FIRST)

| Signal                   | Example                        | Problem                          |
| ------------------------ | ------------------------------ | -------------------------------- |
| No files mentioned       | "improve performance"          | Where? Which files?              |
| Vague verbs              | "fix", "update", "make better" | What specifically?               |
| Large undefined scope    | "refactor the codebase"        | Which parts? What pattern?       |
| Missing success criteria | "add auth"                     | OAuth? JWT? Session? What flows? |
| Ambiguous boundaries     | "handle errors"                | Which errors? Where? How?        |

### Clear Task Signals (PROCEED to Decompose)

| Signal             | Example                        | Why it's clear   |
| ------------------ | ------------------------------ | ---------------- |
| Specific files     | "update src/auth/\*.ts"        | Scope defined    |
| Concrete verbs     | "migrate from X to Y"          | Action defined   |
| Defined scope      | "the payment module"           | Boundaries clear |
| Measurable outcome | "tests pass", "no type errors" | Success criteria |

## Coordinator Workflow

### Phase 0: Socratic Planning (NEW - INTERACTIVE)

**Before decomposing, engage with the user to clarify the task.**

Swarm supports three interaction modes:

| Mode | Flag | Behavior |
|------|------|----------|
| **Full Socratic** | (default) | Ask questions, offer recommendations, collaborative planning |
| **Fast** | `--fast` | Skip questions, proceed with reasonable defaults |
| **Auto** | `--auto` | Minimal interaction, use heuristics for all decisions |
| **Confirm Only** | `--confirm-only` | Show plan, get yes/no, no discussion |

### Phase 1: Initialize Swarm Mail (FIRST)

```typescript
// ALWAYS initialize first - registers you as coordinator
await swarmmail_init({
  project_path: "$PWD",
  task_description: "Swarm: <task summary>",
});
```

### Phase 2: Knowledge Gathering (MANDATORY)

Before decomposing, query ALL knowledge sources:

```typescript
// 1. Past learnings from this project
hivemind_find({ query: "<task keywords>", limit: 5 });

// 2. How similar tasks were solved before
hivemind_find({ query: "<task description>", limit: 5, collection: "sessions" });

// 3. Design patterns and prior art
pdf_brain_search({ query: "<domain concepts>", limit: 5 });

// 4. Available skills to inject into workers
skills_list();
```

### Phase 3: Decomposition (DELEGATE TO SUBAGENT)

> **⚠️ CRITICAL: Context Preservation Pattern**
>
> **NEVER do planning inline in the coordinator thread.** Decomposition work consumes massive amounts of context and will exhaust your token budget on long swarms.
>
> **ALWAYS delegate planning to a `swarm-planner` subagent** and receive only the structured CellTree JSON result back.

### Phase 4: File Ownership (CRITICAL RULE)

**⚠️ COORDINATORS NEVER RESERVE FILES**

This is a hard rule. Here's why:

```typescript
// ❌ WRONG - Coordinator reserving files
swarmmail_reserve({
  paths: ["src/auth/**"],
  reason: "bd-123: Auth service implementation"
});

// ✅ CORRECT - Worker reserves their own files
const prompt = swarm_spawn_subtask({
  bead_id: "bd-123.4",
  files: ["src/auth/**"],  // Files listed here
});
```

### Phase 5: Spawn Workers

```typescript
for (const subtask of subtasks) {
  const prompt = await swarm_spawn_subtask({
    bead_id: subtask.id,
    epic_id: epic.id,
    subtask_title: subtask.title,
    subtask_description: subtask.description,
    files: subtask.files,
    shared_context: synthesizedContext,
  });

  Task({
    subagent_type: "swarm-worker",
    prompt: prompt.worker_prompt,
  });
}
```

### Phase 6: MANDATORY Review Loop (NON-NEGOTIABLE)

**⚠️ AFTER EVERY Worker Returns, You MUST Complete This Checklist:**

1. Check Swarm Mail (Worker may have sent messages).
2. Review the Work (Generate review prompt with diff).
3. Evaluate Against Criteria.
4. Send Feedback (Approve or Request Changes).
5. ONLY THEN Continue.

### Phase 7: Aggregate & Complete

- Verify all subtasks completed.
- Run final verification (typecheck, tests).
- Close epic with summary.
- Release any remaining reservations.
- Record outcomes for learning.

## Context Survival Patterns (CRITICAL)

Long-running swarms exhaust context windows. These patterns keep you alive.

### Pattern 1: Query Memory Before Starting

### Pattern 2: Checkpoint Before Risky Operations

### Pattern 3: Store Learnings Immediately

### Pattern 4: Progress Reports Trigger Auto-Checkpoints

### Pattern 5: Delegate Heavy Research to Subagents

### Pattern 6: Use Summaries Over Raw Data

## Communication Protocol

Workers communicate via Swarm Mail with epic ID as thread:

```typescript
// Progress update
swarmmail_send({
  to: ["coordinator"],
  subject: "Auth API complete",
  body: "Endpoints ready at /api/auth/*",
  thread_id: epic_id,
});

// Blocker
swarmmail_send({
  to: ["coordinator"],
  subject: "BLOCKED: Need DB schema",
  body: "Can't proceed without users table",
  thread_id: epic_id,
  importance: "urgent",
});
```

## Intervention Patterns

| Signal                  | Action                               |
| ----------------------- | ------------------------------------ |
| Worker blocked >5 min   | Check inbox, offer guidance          |
| File conflict           | Mediate, reassign files              |
| Worker asking questions | Answer directly                      |
| Scope creep             | Redirect, create new bead for extras |
| Repeated failures       | Take over or reassign                |

## Anti-Patterns

| Anti-Pattern                | Symptom                                    | Fix                                  |
| --------------------------- | ------------------------------------------ | ------------------------------------ |
| **Decomposing Vague Tasks** | Wrong subtasks, wasted agent cycles        | Ask clarifying questions FIRST       |
| **Mega-Coordinator**        | Coordinator editing files                  | Coordinator only orchestrates        |
| **Silent Swarm**            | No communication, late conflicts           | Require updates, check inbox         |
| **Over-Decomposed**         | 10 subtasks for 20 lines                   | 2-5 subtasks max                     |
| **Under-Specified**         | "Implement backend"                        | Clear goal, files, criteria          |
| **Inline Planning** ⚠️      | Context pollution, exhaustion on long runs | Delegate planning to subagent        |
| **Heavy File Reading**      | Coordinator reading 10+ files              | Subagent reads, returns summary only |
| **Deep Hivemind Drilling**  | Multiple hivemind_find calls inline        | Subagent searches, summarizes        |

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

## Full Swarm Flow

```typescript
// 1. Initialize Swarm Mail FIRST
swarmmail_init({ project_path: "$PWD", task_description: "..." });

// 2. Gather knowledge
hivemind_find({ query });
hivemind_find({ query, collection: "sessions" });
pdf_brain_search({ query });
skills_list();

// 3. Decompose
swarm_plan_prompt({ task });
swarm_validate_decomposition();
hive_create_epic();

// 4. Reserve files
swarmmail_reserve({ paths, reason, ttl_seconds });

// 5. Spawn workers (loop)
swarm_spawn_subtask();

// 6. Monitor
swarm_status();
swarmmail_inbox();
swarmmail_read_message({ message_id });

// 7. Complete
swarm_complete();
swarmmail_release();
hive_sync();
```

## ASCII Art, Whimsy & Diagrams (MANDATORY)

**We fucking LOVE visual flair.** Every swarm session should include:

### Session Summaries

When completing a swarm, output a beautiful summary with:

- ASCII art banner (figlet-style or custom)
- Box-drawing characters for structure
- Architecture diagrams showing what was built
- Stats (files modified, subtasks completed, etc.)
- A memorable quote or cow saying "ship it"

### During Coordination

- Use tables for status updates
- Draw dependency trees with box characters
- Show progress with visual indicators

### Examples

**Session Complete Banner:**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃         🐝 SWARM COMPLETE 🐝                 ┃
┃                                              ┃
┃   Epic: Add Authentication                   ┃
┃   Subtasks: 4/4 ✓                            ┃
┃   Files: 12 modified                         ┃
┃                                              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Architecture Diagram:**

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   INPUT     │────▶│  PROCESS    │────▶│   OUTPUT    │
└─────────────┘     └─────────────┘     └─────────────┘
```

**Dependency Tree:**

```
epic-123
├── epic-123.1 ✓ Auth service
├── epic-123.2 ✓ Database schema
├── epic-123.3 ◐ API routes (in progress)
└── epic-123.4 ○ Tests (pending)
```

**Ship It:**

```
    \   ^__^
     \  (oo)\_______
        (__)\       )\/\
            ||----w |
            ||     ||

    moo. ship it.
```

**This is not optional.** PRs get shared on Twitter. Session summaries get screenshot. Make them memorable. Make them beautiful. Make them fun.

Box-drawing characters: `─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ━ ┃ ┏ ┓ ┗ ┛`
Progress indicators: `✓ ✗ ◐ ○ ● ▶ ▷ ★ ☆ 🐝`