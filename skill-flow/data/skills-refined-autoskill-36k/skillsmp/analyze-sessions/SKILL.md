---
name: analyze-sessions
description: Analyze session logs to discover automation opportunities
allowed-tools: Read, Write, Glob, Grep, Bash
---

Analyze recorded session data to identify patterns and automation opportunities.

## Data Location

Session logs are stored in `.claude/logs/sessions.jsonl` in JSONL format (one JSON object per line).

Each entry contains:
```json
{
  "session_id": "...",
  "timestamp": "2026-01-23T12:00:00Z",
  "project": "project-name",
  "cwd": "/path/to/project",
  "transcript_path": "/path/to/transcript"
}
```

## Analysis Process

### 1. Read Session Logs

Read `.claude/logs/sessions.jsonl` and parse all entries.

If the file doesn't exist or is empty:
```
NO SESSION DATA
===============
No sessions have been logged yet.

Sessions are automatically logged when you use Claude Code.
Run a few sessions, then run /analyze-sessions again.
```

### 2. Calculate Statistics

```
SESSION ANALYSIS
================

Total sessions: {N}
Date range: {earliest} to {latest}
Projects: {list of unique projects}

Sessions per project:
- {project1}: {count}
- {project2}: {count}
```

### 3. Analyze Transcripts (If Available)

For each session with an accessible transcript_path:

1. Read the transcript file
2. Look for these patterns:

**Manual Interventions:**
- `AskUserQuestion` tool calls → Questions asked during sessions
- Text containing "manually", "by hand", "human must"
- Repeated similar questions across sessions

**Common Blockers:**
- Text containing "BLOCKED", "blocked", "waiting for"
- Error patterns that recur
- Missing credentials/env vars

**Tool Usage Patterns:**
- Count of each tool type used
- Sequences of tools that repeat

**Workflow Friction:**
- "cd" into directories (wrong directory issues)
- Repeated file lookups (missing context)
- Re-reading same files multiple times

### 4. Identify Automation Opportunities

Based on patterns found, identify:

**High Impact (Repeated across 3+ sessions):**
- Manual steps that could be automated with curl/Bash
- Questions that could be pre-answered in AGENTS.md
- Browser checks that could use Playwright

**Medium Impact (Repeated 2 times):**
- Verification steps that could be codified
- Setup steps that could be scripted

**Low Impact (Single occurrence but notable):**
- One-off manual interventions that might recur

### 5. Generate Report

Write analysis to `.claude/logs/ANALYSIS_REPORT.md`:

```markdown
# Session Analysis Report

Generated: {timestamp}
Sessions analyzed: {N}
Date range: {earliest} to {latest}

## Summary

- Total sessions: {N}
- Projects: {list}
- Common patterns identified: {count}

## Automation Opportunities

### High Priority

#### 1. {Pattern Name}
**Occurrences:** {N} sessions
**Pattern:** {description of what keeps happening}
**Suggested Automation:**
- {specific automation approach}
- {implementation hint}

#### 2. {Pattern Name}
...

### Medium Priority

#### 1. {Pattern Name}
...

### Low Priority

#### 1. {Pattern Name}
...

## Recommended Actions

1. **Create new skill:** {skill name} — {what it would automate}
2. **Add to AGENTS.md:** {guidance to add}
3. **Create hook:** {hook description}

## Raw Statistics

### Questions Asked (AskUserQuestion)
| Question Pattern | Count | Projects |
|-----------------|-------|----------|
| {pattern} | {N} | {list} |

### Tools Used
| Tool | Total Uses | Avg per Session |
|------|------------|-----------------|
| {tool} | {N} | {avg} |

### Blockers Encountered
| Blocker Type | Count | Resolution |
|--------------|-------|------------|
| {type} | {N} | {how resolved} |
```

### 6. Output Summary

After writing the report:

```
ANALYSIS COMPLETE
=================

Analyzed: {N} sessions
Report: .claude/logs/ANALYSIS_REPORT.md

Key Findings:
- {top finding 1}
- {top finding 2}
- {top finding 3}

Recommended next steps:
1. Review .claude/logs/ANALYSIS_REPORT.md for full details
2. Consider creating skills for high-priority patterns
3. Update AGENTS.md with guidance for common questions
```

## Limitations

- Transcript files may not be accessible (permissions, deleted)
- Analysis quality depends on session data available
- Some patterns require human judgment to identify
