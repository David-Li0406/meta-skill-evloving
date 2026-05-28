---
name: session-analysis-and-improvement
description: Use this skill to analyze Claude Code sessions, identify strengths and weaknesses, and suggest high-confidence improvements to skills and configurations.
---

# Session Analysis and Improvement

Analyze Claude Code sessions to learn what went well and what could be improved, then suggest high-confidence fixes to skills and configurations.

## Input

- **Session ID**: Provided as an argument (e.g., `/session-analysis abc-123-def`).
- **Session File**: Located at `~/.claude/projects/*/<SESSION_ID>.jsonl`.
- **Debug Log**: Optional, located at `~/.claude/debug/<SESSION_ID>.txt`.

## Session Log Format

The session logs are in JSONL format with records like:
```json
{"type": "user", "message": {"role": "user", "content": "..."}}
{"type": "assistant", "message": {"role": "assistant", "content": [{"type": "tool_use", "name": "...", "input": {...}}]}}
```

## Analysis Steps

### 1. Read the Session File

```bash
# Find the session file
find ~/.claude/projects -name "<SESSION_ID>.jsonl" 2>/dev/null

# Read the session log
cat <SESSION_FILE>

# Read the debug log if available
cat ~/.claude/debug/<SESSION_ID>.txt 2>/dev/null
```

### 2. Analyze and Suggest Improvements

#### Permissions (settings.json)
- Look for `Permission suggestions for` in the debug log.
- Identify commands that required manual approval.
- Suggest `permissions.allow` rules.

#### Memory / Rules (CLAUDE.md, .claude/rules/)
- Find repeated explanations from the user.
- Identify `AskUserQuestion` tool calls with similar questions.
- Suggest content for CLAUDE.md or path-specific rules.

#### Skills (.claude/skills/<name>/SKILL.md)
- Identify repeated multi-step workflows.
- Find manual instructions given multiple times.
- Suggest skill definitions with frontmatter.

#### Agents (.claude/agents/<name>.md)
- Find repeated `Task` tool delegations with the same patterns.
- Identify common subagent_type + description combinations.
- Suggest custom agent definitions.

#### Hooks (settings.json)
- Find repeated pre/post processing steps.
- Identify manual formatting or validation tasks.
- Suggest hook configurations.

### 3. Create a Report

Save the report to `~/.claude/retrospectives/<SESSION_ID>.md`:

```markdown
# Session Analysis: <SESSION_ID>

**Date**: YYYY-MM-DD
**Project**: /path/to/project

## Session Summary
[What was accomplished]

## What Went Well
- [Successes]

## Suggested Improvements

### 1. Permissions
```json
{"permissions": {"allow": ["Bash(command:*)"]}}
```
**Reason**: [Why this helps]

### 2. Memory / Rules
```markdown
# Content to add
```
**Reason**: [Why this helps]

### 3. Skills
```yaml
---
name: skill-name
description: ...
---
```
**Reason**: [Why this helps]

### 4. Agents
```yaml
---
name: agent-name
tools: Read, Grep
---
```
**Reason**: [Why this helps]

### 5. Hooks
```json
{"hooks": {...}}
```
**Reason**: [Why this helps]

## Action Items
- [ ] Specific action 1
- [ ] Specific action 2
```

## Key Principles

- **Counterfactual-driven**: Every fix must pass the 3/3 counterfactual test.
- **Evidence-based**: Quote or cite specific session content.
- **Iteration-focused**: Primary signal = things that required retry/correction.
- **Skill-focused**: Goal is improving skills, not critiquing user or session.
- **Log-driven**: Write findings to log as you go, refresh before synthesis.

## Error Handling

| Error | Response |
|-------|----------|
| Session file not found | Ask user to provide path directly. |
| Malformed JSONL (parse error) | Skip malformed lines, note in report. |
| Skill file not found | Note as "skill definition unavailable" in comparison. |
| jq not available | Use grep/sed fallback patterns to extract JSON fields. |
| Empty session | Report "Session contains no analyzable content". |

## Final Recommendations

For each high-confidence issue, format as follows:

```markdown
## Issue: {short title}

**Confidence**: HIGH
**Counterfactual score**: 3/3

### Evidence
{Quote or describe specific session content}

### What Happened
{Brief description of the problem}

### Root Cause
{Why the current skill didn't prevent this - be specific about what's missing}

### Suggested Fix
**File**: {skill file path}
**Section**: {phase/section name}
**Line**: ~{approximate line number}

**Current behavior**:
{What the skill does now}

**Proposed behavior**:
{What the skill should do instead}
```

---

This skill is designed to provide a comprehensive analysis of Claude Code sessions, focusing on identifying areas for improvement and suggesting actionable changes to enhance performance and effectiveness.