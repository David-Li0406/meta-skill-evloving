---
name: [process-name]
description: [Action] [Context] using a step-by-step workflow. Use when [User Trigger].
license: Apache-2.0
metadata:
  author: [Author]
  version: "1.0"
---

# Workflow: [Process Name]

This skill guides you through the process of [Process Name]. Follow these steps exactly.

## When to use this skill

Use this skill when you need to [Goal of the process]. This ensures consistency and proper verification.

## Prerequisites

Before starting, ensure:

- [ ] You are connected to [Environment].
- [ ] Tool [X] is installed.

## Steps

1.  **Initiate**:
    - Run `[Command]` to start.
    - _Verification_: Check that output contains "Started".

2.  **Execute**:
    - Run `[Command]` to perform the main task.
    - _Verification_: Verify file [X] exists.

3.  **Finalize**:
    - Run `[Command]` to cleanup.
    - _Verification_: Ensure exit code is 0.

## Rollback / Failure Handling

If any step fails:

1.  Run `[Rollback Command]`.
2.  Report the error to the user.

## Progressive Disclosure

For complex workflows, store detailed troubleshooting guides in `references/TROUBLESHOOTING.md`.
