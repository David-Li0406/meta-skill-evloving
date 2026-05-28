---
name: gemini-cli-integration
description: Use this skill when you need to execute Gemini CLI for AI-powered code analysis, generation, and web research, leveraging Google's Gemini models for complex reasoning tasks and alternative perspectives.
---

# Gemini CLI Integration

## Overview

This skill enables the execution of Gemini CLI commands, integrating Google's Gemini AI models into workflows for code generation, review, analysis, and specialized tasks.

## When to Use

- Complex reasoning tasks requiring advanced AI capabilities
- Code generation and analysis with Gemini models
- Tasks requiring Google's latest AI technology
- Alternative perspectives on code problems
- Web research needing current information via Google Search
- Codebase architecture analysis and mapping dependencies

## Usage

**Mandatory**: Run via `uv` with a fixed timeout of 7200000ms (2 hours):

```bash
uv run ~/.claude/skills/gemini/scripts/gemini.py "<prompt>" [working_dir]
```

**Optional** (direct execution or using Python):

```bash
~/.claude/skills/gemini/scripts/gemini.py "<prompt>" [working_dir]
# or
python3 ~/.claude/skills/gemini/scripts/gemini.py "<prompt>" [working_dir]
```

## Environment Variables

- **GEMINI_MODEL**: Configure model (default: `gemini-3-pro-preview`)
  - Example: `export GEMINI_MODEL=gemini-3`

## Timeout Control

- **Fixed**: 7200000 milliseconds (2 hours), immutable
- **Bash tool**: Always set `timeout: 7200000` for double protection

### Parameters

- `prompt` (required): Task prompt or question
- `working_dir` (optional): Working directory (default: current directory)

### Return Format

Plain text output from Gemini:

```text
Model response text here...
```

Error format (stderr):

```text
ERROR: Error message
```

### Invocation Pattern

When calling via Bash tool, always include the timeout parameter:

```yaml
Bash tool parameters:
- command: uv run ~/.claude/skills/gemini/scripts/gemini.py "<prompt>"
- timeout: 7200000
- description: <brief description of the task>
```

### Examples

**Basic query:**

```bash
uv run ~/.claude/skills/gemini/scripts/gemini.py "explain quantum computing"
# timeout: 7200000
```

**Code analysis:**

```bash
uv run ~/.claude/skills/gemini/scripts/gemini.py "review this code for security issues: $(cat app.py)"
# timeout: 7200000
```

**With specific working directory:**

```bash
uv run ~/.claude/skills/gemini/scripts/gemini.py "analyze project structure" "/path/to/project"
# timeout: 7200000
```

**Using python3 directly (alternative):**

```bash
python3 ~/.claude/skills/gemini/scripts/gemini.py "your prompt here"
```

## Core Instructions

### Verify Installation

```bash
command -v gemini || which gemini
```

### Basic Command Pattern

```bash
gemini "[prompt]" --yolo -o text 2>&1
```

Key flags:
- `--yolo` or `-y`: Auto-approve all tool calls
- `-o text`: Human-readable output
- `-o json`: Structured output with stats

### Output Processing

For JSON output (`-o json`), parse:
```json
{
  "response": "actual content",
  "stats": {
    "models": { "tokens": {...} },
    "tools": { "byName": {...} }
  }
}
```

## Error Handling

### Rate Limit Exceeded
- CLI auto-retries with backoff
- Use `-m gemini-2.5-flash` for lower priority tasks
- Run in background for long operations

### Command Failures
- Check JSON output for detailed error stats
- Verify Gemini is authenticated: `gemini --version`
- Check `~/.gemini/settings.json` for config issues

## Integration Workflow

### Standard Generate-Review-Fix Cycle

```bash
# 1. Generate
gemini "Create [code]" --yolo -o text

# 2. Review (Gemini reviews its own work)
gemini "Review [file] for bugs and security issues" -o text

# 3. Fix identified issues
gemini "Fix [issues] in [file]. Apply now." --yolo -o text
```

## Gemini's Unique Capabilities

These tools are available only through Gemini:

1. **google_web_search** - Real-time internet search via Google
2. **codebase_investigator** - Deep architectural analysis
3. **save_memory** - Cross-session persistent memory

## Configuration

### Project Context (Optional)

Create `.gemini/GEMINI.md` in project root for persistent context that Gemini will automatically read.

### Session Management

List sessions: `gemini --list-sessions`
Resume session: `echo "follow-up" | gemini -r [index] -o text`

## See Also

- `reference.md` - Complete command and flag reference
- `templates.md` - Prompt templates for common operations
- `patterns.md` - Advanced integration patterns
- `tools.md` - Gemini's built-in tools documentation