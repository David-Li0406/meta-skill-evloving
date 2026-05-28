---
title: Claude Code Transcript Format
description: JSONL message structure and patterns for LLM-based learning extraction. Focus on identifying learning-worthy content in assistant reasoning.
keywords: transcript, jsonl, session, learning extraction, assistant reasoning, patterns
skill: managing-signs
---

# Claude Code Transcript Format

## Overview

Claude Code session transcripts are JSONL files where each line is a JSON object representing a conversation event. For learning extraction, the key is understanding where valuable insights live.

## File Locations

| Location | Content |
|----------|---------|
| `~/.claude/projects/{encoded-path}/{session-id}.jsonl` | Full session transcript |
| `.claude/sprints/{sprint-name}/transcripts/*.jsonl` | Sprint phase transcripts |

Path encoding: `/home/user/project` → `-home-user-project`

## Message Types

### system/init

Session metadata. Useful for understanding context:

```json
{
  "type": "system",
  "subtype": "init",
  "cwd": "/path/to/project",
  "session_id": "uuid",
  "model": "claude-opus-4-5-20251101",
  "tools": ["Bash", "Read", "Edit", "Write", "..."]
}
```

**Learning value**: Low - but tells you what project and capabilities were available.

### assistant

**PRIMARY SOURCE OF LEARNINGS**. Contains Claude's reasoning and tool usage:

```json
{
  "type": "assistant",
  "message": {
    "content": [
      {
        "type": "text",
        "text": "I need to understand how the compiler works. Looking at types.ts first since it defines the core interfaces..."
      },
      {
        "type": "tool_use",
        "id": "toolu_xxxxx",
        "name": "Read",
        "input": {"file_path": "/path/to/types.ts"}
      }
    ]
  }
}
```

**Learning value**: HIGH - The `text` blocks contain:
- Reasoning about architecture
- Decisions and their rationale
- Discoveries about the codebase
- Problem-solving strategies
- Corrections and refinements

### user

User input OR tool results:

```json
{
  "type": "user",
  "message": {
    "content": [
      {
        "type": "tool_result",
        "tool_use_id": "toolu_xxxxx",
        "content": "actual file content or command output...",
        "is_error": false
      }
    ]
  }
}
```

**Learning value**: Medium - Shows what succeeded/failed and the actual content discovered.

### result

Session end summary (can ignore for extraction):

```json
{
  "type": "result",
  "subtype": "success",
  "total_cost_usd": 0.15,
  "num_turns": 12,
  "duration_ms": 45000
}
```

## Patterns for Learning Extraction

### High-Value Patterns in Assistant Text

Look for these linguistic patterns in assistant `text` blocks:

#### Discovery Patterns
- "I notice that..."
- "I see that..."
- "Looking at this, I can see..."
- "This shows that..."
- "Interestingly..."

#### Decision Patterns
- "I'll use X because..."
- "The right approach is..."
- "This should be done by..."
- "We need to..."
- "The best way to..."

#### Correction Patterns
- "Actually..."
- "I need to revise..."
- "This isn't quite right..."
- "The issue is..."
- "I was wrong about..."

#### Explanation Patterns
- "This works because..."
- "The reason is..."
- "This pattern exists because..."
- "The relationship between X and Y is..."

#### Strategy Patterns
- "First, I'll..."
- "To understand this, I need to..."
- "The approach here is..."
- "Step by step..."

### High-Value Tool Sequences

#### Investigation Sequence
```
Read(file_a.ts) → assistant reasoning → Read(file_b.ts) → assistant reasoning
```
Shows how files relate and what was discovered.

#### Error Recovery Sequence
```
Bash(command) [error] → assistant analysis → Bash(fixed_command) [success]
```
Shows what went wrong and how to fix it.

#### Iterative Refinement
```
Edit(attempt_1) → Build [error] → Edit(attempt_2) → Build [success]
```
Shows the correct approach after trial and error.

#### Multi-File Change
```
Edit(types.ts) → Edit(validate.ts) → Edit(compile.ts) → Build
```
Shows files that must change together.

## Tool Input Reference

| Tool | Key Input Fields |
|------|-----------------|
| `Bash` | `command`, `description` |
| `Read` | `file_path`, `offset`, `limit` |
| `Edit` | `file_path`, `old_string`, `new_string` |
| `Write` | `file_path`, `content` |
| `Glob` | `pattern`, `path` |
| `Grep` | `pattern`, `path`, `type` |
| `Task` | `prompt`, `subagent_type` |

## Processing Large Transcripts

Transcripts can be very large (100k+ lines). For LLM-based extraction:

1. **Check size first**: `wc -l transcript.jsonl`
2. **Use offset/limit** for Read tool: `offset: 1, limit: 500`
3. **Focus on assistant messages** - they contain the learnings
4. **Process in phases**:
   - Early transcript: initial exploration, understanding
   - Middle transcript: implementation, problem-solving
   - Late transcript: refinement, testing, fixes

## Correlating Tool Use with Results

The `tool_use_id` links requests to responses:

```
assistant.message.content[].id  ←→  user.message.content[].tool_use_id
```

This lets you understand:
- What was attempted
- What the result was (success/error)
- How the agent responded to that result

## Example Learning Extraction

From this transcript segment:

```json
{"type": "assistant", "message": {"content": [{"type": "text", "text": "The TypeScript build is failing with 'possibly undefined' errors. When I made the phases field optional in WorkflowDefinition, all consumers now need null checks. Let me fix each file systematically."}]}}
```

Extract:
- **Insight**: Making interface fields optional requires updating all consumers
- **Pattern**: TypeScript TS18048 errors indicate missing null checks
- **Strategy**: Fix systematically, file by file
- **Target**: Compiler CLAUDE.md (relates to TypeScript patterns)

## Quick Reference: What to Look For

| Source | Look For | Learning Type |
|--------|----------|---------------|
| Assistant text | Explanations, decisions, corrections | Architecture, Strategy |
| Tool sequences | Error→fix, multi-file changes | Pitfalls, Relationships |
| Successful complex ops | Working commands, integrations | Patterns, Conventions |
| Build/test results | What passed, what failed | Build patterns, Testing |
