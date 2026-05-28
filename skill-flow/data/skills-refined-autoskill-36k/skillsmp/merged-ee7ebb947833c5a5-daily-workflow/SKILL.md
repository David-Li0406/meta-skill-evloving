---
name: daily-workflow
description: Use this skill for managing daily tasks across multiple projects, ensuring a clear flow of inputs, outputs, and logs.
---

# Daily Workflow Framework

> **Daily Workflow**: Collect, process, and log tasks to maintain a clear record of daily activities.

---

## Framework Overview

```
MAR (Understand Framework)
    ↓
  CLEAR (Task Definition)
    ↓
  ICE (Execution Tracking) ← Single Task Loop
    ↓
  Daily Workflow (Unified Workspace) ← Daily Management + Delivery ← This Skill
    ↓
  Scale (Growth)
```

**Core Principles**:
- ICE is a single-task loop (Intent → Condition → Eval).
- Daily Workflow is a cross-task workspace (in → out → log + artifacts).
- At the end of each day, clear in/out, log important items, and store artifacts.

---

## Structure

| File/Directory | Action | Lifecycle | Core Question |
|:---:|:---:|:--------:|----------|
| **in.md** | Collect | Daily | What did I receive today? |
| **out.md** | Distribute | Daily | What did I produce today? |
| **log.md** | Store | Permanent | What is worth keeping? |
| **artifacts/** | Deliver | Permanent | Completed products, documents, assets |

### Essence of Daily Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Daily Workflow Unified Workspace                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│     External World                                                          │
│         │                                                                   │
│         ▼                                                                   │
│    ┌─────────────────┐                                                     │
│    │     in.md       │  ← Collect: Ideas, Tasks, Clips                    │
│    │   (Inbox)       │     No judgment, no classification, just collect    │
│    └────────┬────────┘                                                     │
│             │                                                               │
│             ▼                                                               │
│    ┌─────────────────┐                                                     │
│    │   AI Processing  │  ← Execute each task using ICE framework          │
│    └────────┬────────┘                                                     │
│             │                                                               │
│             ▼                                                               │
│    ┌─────────────────┐                                                     │
│    │    out.md       │  ← Distribute: Processed results, ready to send    │
│    │   (Outbox)      │     Clear after sending to the right place         │
│    └────────┬────────┘                                                     │
│             │                                                               │
│     ┌───────┴───────┐                                                      │
│     ▼               ▼                                                       │
│  Distribute to Target  ┌─────────────────┐                                   │
│  (Email/Group/System)  │    log.md       │  ← Store: Append, permanent record │
│                       │   (Audit Trail)  │     Important items logged         │
│                       └─────────────────┘                                    │
│                                                                             │
│     ┌─────────────────┐                                                    │
│     │   artifacts/    │  ← Deliver: Permanent outputs                      │
│     │  (Deliverables) │     Completed products, documents, assets         │
│     └─────────────────┘                                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

| Scenario | Description |
|----------|-------------|
| 📥 **Collect Inputs** | Any ideas, tasks, or information go into in.md. |
| 📤 **Distribute Outputs** | Processed results are placed in out.md, awaiting dispatch. |
| 📋 **End-of-Day Cleanup** | Clear in/out at the end of each day, log important items. |
| 📦 **Permanent Delivery** | Store completed outputs in artifacts/. |
| 🔍 **Trace History** | Review past work records from log.md. |
| 🤖 **AI Collaboration** | in.md serves as the natural context for AI interactions. |

---

## in — Collect (Inbox)

### Definition

> The entry point for all inputs. No judgment, no classification, just collect.

### Typical Content

| Type | Example |
|------|---------|
| **Ideas** | Sudden thoughts or concepts |
| **Tasks** | Assignments from supervisors or personal tasks |
| **Clips** | Copied text, screenshots, links |
| **Messages** | Key points from emails or group messages |

### Usage Principles

```
✅ Everything goes into in.md — no need to classify
✅ Keep it low-barrier — even a single sentence is fine
✅ Process during daily cleanup — not immediately
```

---

## out — Distribute (Outbox)

### Definition

> The exit point for processed results. Awaiting distribution to final destinations.

### Typical Content

| Type | Example |
|------|---------|
| **Pending Emails** | Replies that are written but not sent |
| **Pending Submissions** | Documents completed but not uploaded |
| **Pending Notifications** | Information that needs to be communicated |
| **Pending Archives** | Content to be moved to formal directories |

### Usage Principles

```
✅ Place processed results here
✅ Delete after sending out
✅ Clear daily
```

---

## log — Store (Audit Trail)

### Definition

> Records worth keeping permanently. Append-only, never cleared.

### Typical Content

| Type | Example |
|------|---------|
| **Decisions** | Important decisions and their rationale |
| **Milestones** | Completion of project phases |
| **Financials** | Reimbursement, payment records |
| **Commitments** | Agreements made externally |

### Format Suggestion

```markdown
## 2026-01-22
- Confirmed contract with Mr. Zhang, scheduled signing next week
- Reimbursement of ¥328, reference #20260122-01

## 2026-01-21
- Completed project kickoff meeting with Client A
- New colleague Wang joined the team
```

---

## Daily Cleanup Rules

> **Perform daily cleanup at the end of each day.**

### Three Steps

| Step | Action | Check |
|:---:|------|------|
| **1** | Process in.md | Delete completed items, keep uncompleted ones |
| **2** | Clear out.md | Delete sent items, keep unsent ones |
| **3** | Archive to log.md | Append important items to the bottom of log.md |

### Daily Cleanup Checklist

```
□ No "tasks that could have been done today" in in.md
□ No "items that could have been sent today" in out.md
□ Important decisions/events have been appended to log.md
```

---

## Relationship with ICE

| Dimension | ICE | Daily Workflow |
|-----------|-----|----------------|
| **Scope** | Single Task | Cross Task |
| **Cycle** | Task Lifecycle | 24 Hours |
| **Structure** | Intent → Condition → Eval | in → out → log |
| **Output** | Task Loop | Daily Archive |

**Collaboration Model**:

```
in.md (Receive tasks)
    ↓
ICE (Execute single task)
    ↓
out.md (Task output)
    ↓
log.md (Archive record)
```

---

## AI Collaboration Scenarios

### Scenario 1: Let AI Help Process in.md

```
Please help me process the tasks in in.md:
1. Identify urgent tasks
2. Suggest processing order
3. Provide ICE structure for each task
```

### Scenario 2: Let AI Help Organize log.md

```
Please append the valuable content from today’s out.md to the bottom of log.md in date format.
```

### Scenario 3: Let AI Review log.md

```
Please find all records related to "Mr. Zhang's contract" from log.md over the past week.
```

---

## Common Questions

### Q: Will in.md pile up?

A: No. Process during daily cleanup. Delete completed items, keep uncompleted ones for tomorrow. If a task lingers for a week, it likely isn't important—delete it.

### Q: Will log.md become too long?

A: Yes, this is intentional. log.md is your work trajectory; the longer, the more valuable. Use search when needed.

### Q: I have multiple projects, how to use Daily Workflow?

A: Personal Daily Workflow is in the root directory `/DailyWorkflow/`, which is cross-project. Project-level can have `{Repo}/DailyWorkflow.md` (single file log).

---

## Templates

### in.md Template

```markdown
# in

> Collect everything, clear at the end of the day

---

## To-Do
- 

## Just Received
- 

## Ideas
- 
```

### out.md Template

```markdown
# out

> Processed results, clear after distribution

---

## Pending Sends
- [ ] 

## Pending Submissions
- [ ] 

## Pending Archives
- [ ] 
```

### log.md Template

```markdown
# log

> Append records, never clear

---

## 2026-01-22
- 

```

---

## Summary

| Remember | Description |
|----------|-------------|
| **Three Files** | in (Collect), out (Distribute), log (Store) |
| **Daily Cleanup** | Clear in/out daily, log important items |
| **Zero Friction** | Everything goes into in.md, no need to classify |
| **Cooperate with ICE** | ICE manages single tasks, Daily Workflow manages daily flow |

---

*Today's tasks, cleared today. Tomorrow's tasks, addressed tomorrow.*

---

*Version: v1.0 | Creation Date: 2026-01-22 | Maintainer: @taes*