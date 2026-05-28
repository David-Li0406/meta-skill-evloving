---
name: meta
description: Enterprise-scale project orchestrator. Decomposes massive goals into Epic/Feature/Story hierarchy, asks expert-level clarifying questions, and coordinates multi-session execution via APL. Use for projects too large for a single /apl session.
argument-hint: "<goal or subcommand>"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Task, TodoWrite
model: sonnet
context: fork
agent: meta-orchestrator
---

# /meta - Enterprise Project Orchestrator

Meta-orchestrator for planning and executing enterprise-scale projects. Operates in two distinct phases:

1. **PLAN Phase** - Expert questioning + Epic/Feature/Story decomposition
2. **LOOP Phase** - Execute ONE Epic at a time (user-initiated)

## Commands

### Start New Project (PLAN Phase)
```
/meta <enterprise goal>
```
Analyzes goal, asks expert questions, creates Epic/Feature/Story breakdown. Does NOT auto-execute.

**Example:**
```
/meta Build a healthcare patient portal with appointment scheduling and medical records
```

### Execute Next Epic (LOOP Phase)
```
/meta loop
/meta loop <epic_id>
```
Executes stories in ONE Epic via APL orchestrator. Stops when Epic complete.

### View Progress
```
/meta status
```
Shows Epic/Feature/Story progress with minimal context load.

### Re-enter Planning
```
/meta plan
```
Modify or add to existing plan.

### Answer Questions
```
/meta answer <question_id> <answer>
```
Provide answer to a clarifying question during PLAN phase.

### Export Documentation
```
/meta export
```
Generate markdown summary of project plan and progress.

## State Directory

Project state is stored in `.meta/` in your project root:

```
.meta/
├── active/              # Current context (small)
├── epics/               # Full Epic definitions
├── archive/             # Completed work
├── plan.json            # Project plan
└── progress.json        # Metrics
```

## Key Behaviors

- **PLAN completes before execution** - No code is written until you run `/meta loop`
- **ONE Epic per loop** - Context is managed by processing one Epic at a time
- **User controls pacing** - You must explicitly call `/meta loop` between Epics
- **APL unchanged** - Stories are handed off to existing APL orchestrator

## Example Workflow

```bash
# 1. Start planning
/meta Build an e-commerce platform with user accounts, product catalog, and checkout

# 2. Answer expert questions (multiple batches)
/meta answer 1 "Stripe for payments"
/meta answer 2 "PostgreSQL"

# 3. Review the plan
/meta status

# 4. Execute first Epic
/meta loop

# 5. Review, then continue
/meta status
/meta loop

# 6. Repeat until complete
```
