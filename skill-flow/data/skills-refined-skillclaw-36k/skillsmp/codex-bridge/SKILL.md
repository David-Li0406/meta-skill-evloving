---
name: codex-bridge
description: Call OpenAI Codex CLI for tasks. Use when user wants to ask Codex, get GPT's opinion, get a second opinion, compare with OpenAI, have Codex review something, or let Codex perform a task.
allowed-tools: Bash(node:*), Bash(codex:*), Read, Write
user-invocable: true
---

# Codex Bridge

Call OpenAI's Codex CLI to get responses, reviews, or perform tasks.

## When to Use This Skill

Activate when the user says things like:
- "Ask Codex...", "Have Codex...", "Let Codex..."
- "Get GPT's opinion on...", "What does OpenAI think..."
- "Get a second opinion on..."
- "Have Codex review..."
- "Let Codex fix/refactor/implement..."

## How to Call Codex

**Find the script path first:**
```bash
# Marketplace install (most users):
CODEX_BRIDGE="$HOME/.claude/plugins/cache/saurun-marketplace/saurun/*/skills/codex-bridge/codex-bridge.mjs"

# Resolve glob to actual path:
CODEX_BRIDGE=$(ls -1 $CODEX_BRIDGE 2>/dev/null | head -1)
```

**Basic command (read-only):**
```bash
node "$CODEX_BRIDGE" "<prompt>" --working-dir "<project-path>"
```

**With file modification capabilities:**
```bash
node "$CODEX_BRIDGE" "<prompt>" --full-auto --working-dir "<project-path>"
```

**CRITICAL:** Always pass `--working-dir` with the project directory so Codex can read files. Without it, Codex runs in its install location and can't access your project files.

## Decision Logic

### Use READ-ONLY mode (no flags) when:
- User wants an opinion, explanation, or review
- User wants to compare perspectives
- User is asking questions
- Task is about analysis, not modification

### Use `--full-auto` mode when:
- User explicitly asks Codex to fix, refactor, or implement something
- User wants Codex to make changes to files
- Words like "fix", "refactor", "implement", "update", "change" are used

## Handling File Reviews

When user wants Codex to review a file:

1. Read the file content first using the Read tool
2. Include the content in the prompt to Codex
3. Structure the prompt clearly

Example:
```bash
node "$CODEX_BRIDGE" "Review this planning document and provide feedback on feasibility, risks, and suggestions:

---
[FILE CONTENT HERE]
---" --working-dir "/path/to/project"
```

## Response Format

Always present Codex's response clearly:

**For opinions/reviews:**
> **Codex (OpenAI) says:**
> [response]

**For comparisons:**
Provide both my analysis and Codex's response, noting any differences.

**For file modifications:**
After Codex completes, show what changed using `git status` or `git diff`.

## Examples

**User:** "Have Codex review my planning doc at docs/plan.md"
**Action:**
1. Read docs/plan.md
2. Call codex-bridge with the content asking for review
3. Present feedback

**User:** "Get a second opinion from GPT on this architecture"
**Action:**
1. Call codex-bridge with the architecture question
2. Present both perspectives

**User:** "Let Codex fix the TypeScript errors"
**Action:**
1. Call codex-bridge with `--full-auto`
2. Show what files changed

## How It Works

The bridge handles CLI length limits intelligently:

1. **Input**: Short prompts (<7000 chars) pass directly as CLI args. Long prompts write to `.codex-bridge-prompt.txt`
2. **Output**: Response captured via `--output-last-message` temp file
3. **Cleanup**: Temp files automatically deleted after execution
4. **Timeout**: 20 minutes (1,200,000ms) default

This allows sending large file contents for review without hitting Windows' 8191 character CLI limit.

## Prerequisites

- Codex CLI installed: `npm install -g @openai/codex`
- Codex authenticated: `codex login`
