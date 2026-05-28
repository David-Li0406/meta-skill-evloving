---
name: recovering-sessions
description: Use this skill when you need to recover from crashed, failed, or interrupted Claude Code sessions, ensuring that you can analyze logs, verify state, and generate resumption commands effectively.
---

# Session Recovery Skill

Recover from crashed, failed, or interrupted Claude Code sessions with automated analysis and resumption planning.

## Why This Skill

Claude Code sessions can crash during complex multi-agent operations. Recovery without this skill is:
- **Manual**: Requires parsing agent logs by hand
- **Error-prone**: Easy to miss completed or incomplete work
- **Time-consuming**: Ad-hoc investigation for each crash
- **Undocumented**: Knowledge lost between sessions

This skill provides **standardized recovery workflows** that:
- Discover and analyze agent conversation logs
- Verify on-disk state matches expected deliverables
- Generate recovery reports with clear status per task
- Create ready-to-execute Task() resumption commands
- Document prevention patterns to avoid future crashes

## When to Use

| Scenario | Action |
|----------|--------|
| Session crashed during parallel execution | Full recovery workflow |
| User reports interrupted work | Analyze recent agent logs |
| Need to determine completed vs incomplete | Status assessment |
| Generate resumption commands | Resumption plan |
| Session handoff to continue later | Handoff summary |
| Proactive health check | Scan for incomplete work |

## Quick Start

### Post-Crash Recovery

```
User: "Claude crashed while I had multiple agents running. Help me recover."

1. Identify project log directory
2. Discover recent agent logs (last 3 hours)
3. Analyze each log in parallel (haiku subagents)
4. Cross-reference with git status
5. Generate recovery report
6. Offer to commit completed work
7. Provide resumption commands for incomplete tasks
```

### Session Handoff

```
User: "I need to hand off this session to continue later."

1. Identify active/recent work
2. Capture current git state
3. Document in-progress tasks
4. Update progress tracking with session notes
5. Generate handoff summary with resumption instructions
```

### Proactive Health Check

```
User: "Check if any recent agent work was incomplete."
1. Review recent logs for any errors or interruptions
2. Cross-check with on-disk state
3. Generate a report of any incomplete tasks
```