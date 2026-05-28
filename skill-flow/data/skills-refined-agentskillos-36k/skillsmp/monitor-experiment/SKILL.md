---
name: monitor-experiment
description: Monitor Beaker experiments until completion. Use when the user asks to monitor, check, or track a Beaker experiment.
allowed-tools: Bash(beaker:*)
---

# Monitor Beaker Experiment

## Finding the experiment ID

If no experiment ID is provided, find the most recent experiment:

```bash
# List experiments in a workspace (e.g., ai2/open-instruct-dev)
beaker workspace experiments ai2/open-instruct-dev 2>&1 | head -10
```

Common workspaces:
- `ai2/open-instruct-dev` - Development experiments
- `ai2/lm-eval` - Evaluation experiments
- `ai2/tulu-3-dev` - Tulu development

## Monitoring an experiment

1. Get the experiment status:
```bash
beaker experiment get <experiment-id> --format json | jq '.[0] | {id, name, status: .jobs[0].status}'
```

2. Check the status fields:
   - `status.current`: "scheduled", "starting", "running", "succeeded", "failed", "canceled"
   - `status.exitCode`: Exit code (0 = success, non-zero = failure)
   - `status.started` / `status.exited`: Timestamps

3. If still running, wait 30 seconds and check again

4. When complete:
   - If exitCode is 0: Report success
   - If exitCode is non-zero: Fetch and display logs

5. Continue monitoring until the experiment finishes or the user asks to stop

## Useful commands

```bash
# Check status (compact)
beaker experiment get <id> --format json | jq '.[0].jobs[0].status.current'

# Get logs on failure
beaker experiment logs <id>

# Get logs with tail (last N lines)
beaker experiment logs <id> 2>&1 | tail -100

# Open in browser
echo "https://beaker.org/ex/<id>"
```
