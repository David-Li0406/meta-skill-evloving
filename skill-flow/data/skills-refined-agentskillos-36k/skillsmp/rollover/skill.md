---
name: rollover
description: Start fresh session when context is high, preserving continuity via episodic-memory
---

You've decided to rollover to a fresh session. This preserves your full session
in episodic-memory while starting clean.

## Step 1: Generate Handoff Summary

Write a BRIEF handoff summary (aim for ~500 words max). Focus on state, not history:

```
### Current Task
[Issue/goal and current status in 1-2 sentences]

### Key Decisions
- [Decision]: [rationale] (1 line each, max 5)

### Modified Files
- [file]: [what changed] (1 line each)

### Immediate Next Steps
1. [Next action to take]
2. [Following action]

### Critical Context
[Anything the next session MUST know - blockers, gotchas, important findings]
```

## Step 2: Execute Rollover

Save your summary and run the rollover command:

```bash
cat > /tmp/rollover-summary.txt << 'EOF'
[paste your summary here]
EOF

./work --rollover --summary-file /tmp/rollover-summary.txt
```

This will:
1. Sync current session to episodic-memory (full content preserved)
2. Record session end in database with lineage
3. Generate continuation prompt for new session
4. Output the command to start the new session

## Step 3: Start New Session

Run the command output by the rollover (usually):
```bash
claude --prompt-file /tmp/work-continuation-{worker_id}.md
```

## Step 4: In the New Session

Your summary will be injected automatically. For details NOT in the summary,
use episodic-memory to search the full parent session:

```
mcp__episodic-memory__search with query: "specific thing you need"
```

The parent session is fully indexed - nothing is lost, just a search away.
