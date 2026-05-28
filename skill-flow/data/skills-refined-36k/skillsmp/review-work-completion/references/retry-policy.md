# Retry Policy

## When to Retry

Retry on: missing CLI tool, runtime error, or malformed output format.

1. Retry up to 3 times
2. Log: `[RETRY] {agent} attempt {n}/3`
3. After 3 failures: mark agent unavailable, continue with others
4. If ALL agents fail: report failure

Consolidation uses partial results from available agents.

## Format Compliance

If an agent's output doesn't match the required format:

1. Send one retry: "Your output format is incorrect. Reformat using exactly: `[{AGENT_NAME}] {emoji} {description} | File: {path or N/A} | Task: {id or general}` — one issue per line."
2. If still non-compliant after retry, parse what you can and note `(format warning)` next to that agent's findings in consolidation.
