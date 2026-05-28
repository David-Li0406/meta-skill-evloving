---
name: codebase-analysis
description: Invoke IMMEDIATELY via python script when user requests codebase analysis, architecture review, security assessment, or quality evaluation. Do NOT explore first - the script orchestrates exploration.
---

# Codebase Analysis

When this skill activates, IMMEDIATELY invoke the script. The script IS the workflow.

## Invocation

```bash
python3 scripts/analyze.py \
  --step-number 1 \
  --total-steps 6 \
  --thoughts "Starting analysis. User request: <describe what user asked to analyze>"
```

| Argument        | Required | Description                               |
| --------------- | -------- | ----------------------------------------- |
| `--step-number` | Yes      | Current step (starts at 1)                |
| `--total-steps` | Yes      | Minimum 6; adjust as script instructs     |
| `--thoughts`    | Yes      | Accumulated state from all previous steps |

Do NOT explore or analyze first. Run the script and follow its output.