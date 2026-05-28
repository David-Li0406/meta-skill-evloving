---
name: monitor-experiment
description: Use this skill to monitor Beaker experiments until completion when the user asks to track or check an experiment's status.
---

# Monitor Beaker Experiment

## Finding the Experiment ID

If no experiment ID is provided, find the most recent experiment:

```bash
# List experiments in a workspace (e.g., ai2/open-instruct-dev)
beaker workspace experiments <workspace> 2>&1 | head -10
```

Common workspaces:
- `ai2/open-instruct-dev` - Development experiments
- `ai2/lm-eval` - Evaluation experiments
- `ai2/tulu-3-dev` - Tulu development

## Monitoring an Experiment

1. Get the experiment status:
```bash
beaker experiment get <experiment-id> --format json | jq '.[0] | {id, name, status: .jobs[0].status}'
```

2. Check the status fields:
   - `status.current`: "scheduled", "starting", "running", "succeeded", "failed", "canceled"
   - `status.exitCode`: Exit code (0 = success, non-zero = failure)
   - `status.started` / `status.exited`: Timestamps

3. If still running, wait 30 seconds and check again.

4. When complete:
   - If exitCode is 0: Report success.
   - If exitCode is non-zero: Fetch and display logs.

5. Continue monitoring until the experiment finishes or the user asks to stop.

## Useful Commands

```bash
# Check status (compact)
beaker experiment get <id> --format json | jq '.[0].jobs[0].status.current'

# Get logs on failure
beaker experiment logs <id>

# Get logs with tail (last N lines)
beaker experiment logs <id> 2>&1 | tail -100

# Stream logs in real-time for running experiments
beaker experiment logs --follow <id>

# Open in browser
echo "https://beaker.org/ex/<id>"
```