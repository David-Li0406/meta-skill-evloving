---
name: conversation-reader
description: "Extract and read Claude conversation JSONL files with composable filters (discovery: rubber-duck). Evaluate at rubber-duck or at any point in the sesssion when task requires reading conversation history, verifying tool outputs, or auditing session behavior. Use instead of raw Read/grep on ~/.claude/projects/*.jsonl files."
---

# Conversation Reader

Extract conversation content with composable filters. Use for self-reflection, verification, and audit.

## Quick Start

```bash
# Script path (plugin or fallback)
SCRIPT="$([ -f "${CLAUDE_PLUGIN_ROOT}/lib/extract_conversation.py" ] && echo "${CLAUDE_PLUGIN_ROOT}/lib/extract_conversation.py" || echo ~/.claude/lib/extract_conversation.py)"

# Conversation only (user + assistant text)
uv run python "$SCRIPT" "<conversation.jsonl>" --user --assistant

# Tool calls and results
uv run python "$SCRIPT" "<conversation.jsonl>" --tools

# Everything, last 50 items
uv run python "$SCRIPT" "<conversation.jsonl>" --user --assistant --tools --last 50

# JSONL format (backwards compat)
uv run python "$SCRIPT" "<conversation.jsonl>" --tools --json
```

## Flags

| Flag | Description |
|------|-------------|
| `--user` | Include user messages |
| `--assistant` | Include assistant messages |
| `--tools` | Include tool calls/results |
| `--last N` | Limit to last N items |
| `--output FILE` | Custom output path (default: `/tmp/{conversation_uid}.txt`) |
| `--json` | Output JSONL instead of XML (backwards compat) |

At least one of `--user`, `--assistant`, `--tools` required.

## Output Formats

### Default: Semantic XML

Optimized for AI consumption. Each entry has semantic tag with index:

```xml
<user_1>
Fix the bug in config.py
</user_1>

<bash_2>
git status
→ On branch main
    modified: config.py
</bash_2>

<assistant_3>
I'll update the config file now.
</assistant_3>

<edit_4>
config.py
  'timeout=30' → 'timeout=60'
</edit_4>

<thinking_5>
Reviewing the change... confidence is high
</thinking_5>
```

### --json: JSONL Format

One JSON object per line (backwards compatible):

```json
{"role": "user", "text": "Fix the bug", "_id": "abc123"}
{"role": "assistant", "tool_name": "Bash", "tool_input": {...}}
```

## Chunking

- **Auto-chunks:** Splits into ~20K token files when content is large
- **IMPORTANT: Read each chunk in its entirety** - the whole purpose of chunking is to create context-sized pieces. Don't try to grep or extract from chunks; load each one fully.

## Truncation

| Tool | Behavior |
|------|----------|
| Bash, Glob, Task | Always full (high-value) |
| Read, Grep | Truncate >1000 chars |
| Edit, Write | Summarize (file + confirmation) |

## When to Use

| Scenario | Flags |
|----------|-------|
| "What did we discuss?" | `--user --assistant` |
| "What did Claude do?" | `--tools` |
| "Verify tool output" | `--tools --last 20` |
| "Full audit" | `--user --assistant --tools` |
| "Need raw JSON" | Add `--json` |
