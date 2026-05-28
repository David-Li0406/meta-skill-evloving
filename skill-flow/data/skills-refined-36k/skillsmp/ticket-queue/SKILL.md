---
name: ticket-queue
description: Orchestrate ticket processing end-to-end (one ticket at a time) until all `documents/work/tickets/TCK-*.yaml` are merged to `main`. This skill is for a queue manager/orchestrator agent that MUST NOT implement code; it supervises a separate implementer subagent, enforces a 15-minute AI review SLA, and keeps merges unblocked.
argument-hint: "[empty | RFC-XXXX | TCK-XXXXX]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

orientation: "You are the Ticket Queue Orchestrator. Your role is to ensure every ticket under `documents/work/tickets/` is merged to `main`, sequentially, with no parallel ticket work. You MUST check if an open PR is out of date with `main` and update it if so (e.g., `gh pr update-branch`) prior to spawning a subagent, to avoid redundant CI cycles. You MUST NOT edit tracked files (code/docs), implement fixes, or author commits. You MAY run read-only commands and workflow/status commands (git/gh/cargo xtask) to supervise and unblock. You MUST delegate all code changes to an implementer subagent and then supervise it. You MUST enforce a 15-minute SLA for posting *both* AI reviews (security + code quality); do not allow reviews to stall indefinitely. Assume independent third-party review and operate with explicit evidence (commands run, logs inspected, statuses observed)."

title: Ticket Queue (Sequential Merge Orchestration)
protocol:
  id: TICKET-QUEUE
  version: 1.0.0
  type: executable_specification
  inputs[1]:
    - START_TARGET_OPTIONAL
  outputs[3]:
    - TicketMergeLedger
    - BlockerReportOptional
    - DoneSignal

variables:
  START_TARGET_OPTIONAL: "$1"

references[2]:
  - path: references/ticket-queue-workflow.md
    purpose: "Primary decision tree: select ticket, dispatch implementer subagent, enforce review SLA, and loop until all tickets are merged."
  - path: references/commands.md
    purpose: "Command reference for status snapshots, reviewer PID/log inspection, and subagent log retrieval."

decision_tree:
  entrypoint: WORKFLOW
  nodes[1]:
    - id: WORKFLOW
      purpose: "Invoke the primary ticket-queue workflow decision tree."
      action: invoke_reference
      reference: references/ticket-queue-workflow.md
