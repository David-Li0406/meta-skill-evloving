---
name: checkpoint-session
description: Manage session lifecycle, learning extraction, and context metrics. Use when starting/ending sessions, analyzing workflows for learnings, querying knowledge graph, or checking session metrics.
allowed-tools: Bash, Read
---

# Checkpoint Session Skill

Manage Claude session lifecycle, learning extraction, and context metrics.

## When to Use

- Starting a new Claude session (auto-run via SessionStart hook)
- Ending a session and extracting learnings
- Analyzing completed workflows for patterns and mistakes
- Querying the knowledge graph for relevant learnings
- Checking session metrics and usage patterns

## CLI Reference

All commands use the checkpoint CLI:

```bash
bun run checkpoint <command> [args...]
```

## Session Lifecycle Commands

### Session Start

Initialize session context and check for resumable workflows:

```bash
bun run checkpoint session-start [--branch <name>] [--issue <number>]
```

What it does:

- Detects current git branch and modified files
- Cleans up stale workflows (>24 hours)
- Prompts for workflow resume if active workflows found
- Outputs session context summary

### Session End

Record session metrics and extract learnings:

```bash
bun run checkpoint session-end [options]
```

Options:

- `--workflow-id <id>` - Associate with specific workflow
- `--session-id <id>` - Session identifier (auto-detected from session-start)
- `--learnings-injected <n>` - Count of learnings used in session
- `--start-time <iso>` - Session start timestamp
- `--compacted` - Flag if context was compacted
- `--interrupted` - Flag if session was interrupted
- `--review-findings <n>` - Count of review findings
- `--files-read <n>` - Count of files read

## Learning Commands

### Analyze Workflow

Extract learnings from a completed workflow:

```bash
bun run checkpoint learning analyze <workflow-id> <dev-plan-path>
```

Analyzes:

- Planned vs actual commits
- Deviations from plan
- Review findings and fixes
- Patterns to repeat
- Mistakes to avoid

### Query Learnings

Find relevant learnings from the knowledge graph:

```bash
bun run checkpoint learning query [options]
```

At least one filter required:

- `--code-area <area>` - Filter by code area (e.g., "authentication", "database")
- `--file <path>` - Filter by file path
- `--issue <number>` - Filter by source issue number

Returns:

- Learning content
- Confidence scores
- Related patterns
- Related mistakes

## Metrics Commands

### List Session Metrics

View recorded session metrics:

```bash
bun run checkpoint metrics list [issue-number]
```

Shows per session:

- Files read
- Compaction status
- Duration
- Review findings
- Learnings injected/captured

### Metrics Summary

View aggregate metrics:

```bash
bun run checkpoint metrics summary
```

Shows:

- Total sessions
- Compaction rate
- Average files read
- Average learnings injected/captured
- Total review findings

## Example: Full Session Flow

```bash
# 1. Session starts (auto-run by hook)
bun run checkpoint session-start --branch feat/issue-394

# 2. During session: use /work-on-issue or /auto-issue
#    These use the workflow checkpoint commands

# 3. After workflow complete: analyze for learnings
bun run checkpoint learning analyze "workflow-394-xxx" ".claude/dev-plans/issue-394.md"

# 4. Session ends (capture metrics)
bun run checkpoint session-end --files-read 42 --review-findings 3
```

## Example: Query Knowledge Before Starting Work

```bash
# Find learnings about similar code areas
bun run checkpoint learning query --code-area "badge-verification"

# Find learnings from a related issue
bun run checkpoint learning query --issue 380

# Find learnings about a specific file
bun run checkpoint learning query --file "packages/openbadges-types/src/ob3.ts"
```

## Integration with Hooks

The session commands integrate with Claude Code hooks:

| Hook         | Command         | Purpose                           |
| ------------ | --------------- | --------------------------------- |
| SessionStart | `session-start` | Inject learnings, check workflows |
| SessionEnd   | `session-end`   | Extract learnings, record metrics |

Session metadata is automatically passed between hooks via temp files.
