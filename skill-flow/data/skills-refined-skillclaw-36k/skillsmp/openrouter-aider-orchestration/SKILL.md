---
name: openrouter-aider-orchestration
description: |
  Build multi-model AI orchestrators using OpenRouter with Aider. Use when: (1) "No endpoints
  found" or "Missing API Key" errors with OpenRouter models, (2) "Argument list too long"
  when passing large files to Aider, (3) JSON parsing fails due to line-wrapped output from
  Aider, (4) building cost-effective agent systems with model routing, (5) git merge fails
  with "untracked working tree files would be overwritten" for .aider.* files. Covers model
  naming conventions, litellm prefix requirements, --read flag for large files, JSON cleaning
  for programmatic output extraction, and worktree merge handling.
author: Claude Code
version: 1.1.0
date: 2026-01-22
---

# OpenRouter + Aider Multi-Model Orchestration

## Problem

Building AI orchestrators that use multiple models via OpenRouter with Aider involves several
non-obvious integration challenges: model naming, API key routing, handling large inputs, and
parsing structured output.

## Context / Trigger Conditions

- Error: "No endpoints found for anthropic/claude-3-opus" - deprecated model name
- Error: "Missing Anthropic API Key" - missing openrouter/ prefix
- Error: "Argument list too long" - file content too large for command line
- Error: "Invalid control character" in JSON - Aider wraps lines at ~80 chars
- Error: "untracked working tree files would be overwritten" for .aider.* - merge conflict
- Building multi-agent systems with cost-aware model routing

## Solution

### 1. Model Naming Convention

OpenRouter requires the `openrouter/` prefix when using litellm (which Aider uses internally):

```python
# WRONG - causes "Missing API Key" error
model = "anthropic/claude-3.5-sonnet"

# CORRECT - routes through OpenRouter
model = "openrouter/anthropic/claude-3.5-sonnet"
```

Current Claude model names (as of 2026):
```python
CLAUDE_OPUS = "openrouter/anthropic/claude-opus-4"      # Was claude-3-opus
CLAUDE_SONNET = "openrouter/anthropic/claude-sonnet-4"  # Was claude-3.5-sonnet
CLAUDE_HAIKU = "openrouter/anthropic/claude-3.5-haiku"  # Still valid
```

Cost-effective alternatives:
```python
DEEPSEEK_V3 = "openrouter/deepseek/deepseek-chat"           # ~$0.0003/1K tokens
GEMINI_PRO = "openrouter/google/gemini-2.0-flash-001"       # ~$0.0001/1K tokens
QWEN_CODER = "openrouter/qwen/qwen-2.5-coder-32b-instruct"  # ~$0.0002/1K tokens
```

### 2. Large File Handling

When input files exceed command-line limits (~128KB on Linux), use `--read`:

```python
# WRONG - causes "Argument list too long" for large files
subprocess.run([
    "aider", "--model", model,
    "--message", f"Analyze this PRD:\n\n{large_prd_content}"
])

# CORRECT - use --read flag to load file
subprocess.run([
    "aider", "--model", model,
    "--read", prd_file_path,
    "--message", "Analyze the PRD file and extract tasks as JSON"
])
```

### 3. JSON Output Cleaning

Aider wraps long lines at ~80 characters, breaking JSON strings:

```python
def clean_aider_json(output: str) -> dict:
    """Extract and clean JSON from Aider output."""
    # Find JSON block
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', output)
    if not json_match:
        # Try finding raw JSON
        json_match = re.search(r'\[\s*\{[\s\S]*\}\s*\]', output)

    if not json_match:
        raise ValueError("No JSON found in output")

    json_str = json_match.group(1) if '```' in output else json_match.group(0)

    # CRITICAL: Fix line-wrapped strings
    # Aider wraps at ~80 chars, inserting newlines in string values
    json_str = re.sub(r'\n\s+', ' ', json_str)  # Collapse wrapped lines
    json_str = re.sub(r'"\s*\n\s*"', '""', json_str)  # Fix split strings

    return json.loads(json_str)
```

### 4. Complete Orchestration Pattern

```python
import subprocess
import os

def run_agent(issue_id: str, model: str, project_root: str):
    """Run Aider agent on an issue."""
    env = os.environ.copy()
    env["OPENROUTER_API_KEY"] = os.getenv("OPENROUTER_API_KEY")

    cmd = [
        "aider",
        "--model", model,  # Must include openrouter/ prefix
        "--openai-api-key", env["OPENROUTER_API_KEY"],
        "--openai-api-base", "https://openrouter.ai/api/v1",
        "--message", f"Work on issue {issue_id}",
        "--no-gitignore",
        "--auto-commits",
        "--yes-always",
        "--no-analytics",
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=project_root,
        env=env
    )

    return result.stdout
```

## Verification

1. Model works: Agent produces output without API errors
2. Large files work: PRDs >100KB process successfully
3. JSON parsing works: Structured output extracts correctly

## Example

```bash
# Cost-effective agent run
aider \
  --model openrouter/deepseek/deepseek-chat \
  --openai-api-key "$OPENROUTER_API_KEY" \
  --openai-api-base "https://openrouter.ai/api/v1" \
  --read large_spec.md \
  --message "Extract tasks from the spec as JSON" \
  --yes-always
```

### 5. Auto-Merge with Worktrees

When using git worktrees with auto-merge, Aider creates history files that block merges:

```
error: The following untracked working tree files would be overwritten by merge:
    .aider.chat.history.md
    .aider.input.history
```

**Solution**: Clean up Aider files before merging:

```python
def merge_branch(branch_name: str, project_root: str):
    """Merge a branch, handling Aider artifacts."""
    # Remove Aider history files that block merge
    for aider_file in [".aider.chat.history.md", ".aider.input.history"]:
        path = os.path.join(project_root, aider_file)
        if os.path.exists(path):
            os.remove(path)

    # Now merge
    subprocess.run(["git", "merge", branch_name], cwd=project_root, check=True)
```

Or add to `.gitignore`:
```
.aider.*
```

## Notes

- DeepSeek V3 offers ~50x cost savings vs Claude Opus with good code quality
- Always verify model names at https://openrouter.ai/models - they change
- The `openrouter/` prefix is required for litellm routing, not just the API
- Aider's `--no-show-model-warnings` suppresses deprecation notices
- For programmatic use, consider `--no-git` to avoid commit overhead
- **Worktree merges**: Aider creates `.aider.*` files that block git merge - clean before merging

## References

- [OpenRouter Model Naming](https://openrouter.ai/docs/api/reference/overview)
- [OpenRouter Models List](https://openrouter.ai/models)
- [Aider --read Flag Usage](https://aider.chat/docs/usage/conventions.html)
- [Aider Large File Tips](https://aider.chat/docs/usage/tips.html)
- [LiteLLM OpenRouter Provider](https://docs.litellm.ai/docs/providers/openrouter)
