---
name: codex-oracle
description: Delegate complex reasoning, planning, or deep analysis tasks to OpenAI's GPT-5.2-Codex model. Use when tasks require extended thinking, multi-step planning, or when you need a second opinion on complex problems.
---

# Codex Oracle

## Core Purpose

Offload specific types of work to OpenAI's GPT-5.2-Codex - their most advanced agentic coding model - when deep reasoning and extended thinking would produce better results. This skill turns Codex into a specialized consultant that Claude orchestrates.

## When to Use This Skill

**Ideal use cases:**

- Complex multi-step planning that benefits from extended reasoning
- Architecture decisions with many interacting constraints
- Debugging complex issues where root cause is unclear
- Algorithm design and optimization
- Code review for subtle bugs or security issues
- Large refactors and code migrations
- Generating comprehensive test cases
- Evaluating tradeoffs across many dimensions
- Second opinion on your approach before implementation

**Do NOT use for:**

- Simple questions with obvious answers
- Tasks that require real-time file system access
- Anything Claude can handle well directly
- Quick lookups or straightforward code changes

## How to Use

### Step 1: Prepare the Prompt

Write a clear, self-contained prompt for Codex. Include:

- Full context (Codex has no memory of our conversation)
- Specific code snippets or file contents if relevant
- Clear success criteria
- Any constraints or preferences

### Step 2: Execute the Call

Run the script via Bash:

```bash
~/.claude/skills/codex-oracle/scripts/call-openai.sh "YOUR_PROMPT_HERE" [model] [reasoning_effort]
```

**Parameters:**

- `prompt` (required): The task for Codex
- `model` (optional): Default is `gpt-5.2-codex`. Alternatives: `gpt-5.2`, `o3`, `gpt-4o`
- `reasoning_effort` (optional): `high` (default). Options: `xhigh`, `high`, `medium`, `low`, `none`

### Step 3: Interpret and Apply Results

- Review Codex's response critically
- Verify any code suggestions work in our actual codebase
- Adapt recommendations to match existing patterns
- Don't blindly copy-paste - synthesize with your context

## Prompt Engineering for Codex

### Good Prompt Structure

```
## Task
[Clear statement of what you need]

## Context
[Relevant background, constraints, existing code]

## Requirements
- [Specific requirement 1]
- [Specific requirement 2]

## Output Format
[What you want back - code, analysis, plan, etc.]
```

### Example Prompts

**Architecture Planning:**

```
## Task
Design a caching layer for our API that handles 10k requests/second.

## Context
- Node.js/Express backend
- PostgreSQL database
- Currently experiencing 500ms average response times
- Most queries are read-heavy (90% reads, 10% writes)

## Requirements
- Sub-50ms cache hits
- Cache invalidation on writes
- Graceful degradation if cache fails

## Output Format
Provide architecture diagram (ASCII), key code snippets, and implementation steps.
```

**Debug Analysis:**

```
## Task
Identify why this function intermittently returns incorrect results.

## Context
[Paste the function code]

This function is called in a multi-threaded context. The bug occurs ~5% of the time.

## Requirements
- Identify the root cause
- Propose a fix with minimal code changes
- Explain why the fix works

## Output Format
Root cause analysis, then the fix with inline comments explaining the changes.
```

## Model Selection Guide

| Model           | Best For                                                       | Speed | Cost |
| --------------- | -------------------------------------------------------------- | ----- | ---- |
| `gpt-5.2-codex` | Complex coding, refactors, migrations, agentic tasks (DEFAULT) | Slow  | High |
| `gpt-5.2`       | General deep reasoning                                         | Slow  | High |
| `o3`            | Deep reasoning, complex planning                               | Slow  | High |
| `gpt-4o`        | Quick tasks, simple code gen                                   | Fast  | Low  |

## Reasoning Effort Levels

For GPT-5.2 and o-series models, `reasoning_effort` controls how much "thinking" the model does:

- `xhigh`: Maximum reasoning depth. Use for critical decisions, complex architecture. (GPT-5.2 only)
- `high`: Deep reasoning. Default for most complex tasks.
- `medium`: Balanced. Good for moderate complexity.
- `low`: Quick answers. Use when speed matters more than depth.
- `none`: No extended reasoning. Fast responses.

## Integration with Claude Workflow

### As Part of Brainstorming

1. Claude does initial problem exploration
2. Codex generates additional architectural options
3. Claude synthesizes and presents unified recommendation

### As a Debugging Partner

1. Claude reproduces and isolates the bug
2. Codex analyzes root cause with fresh perspective
3. Claude implements and verifies the fix

### As Code Reviewer

1. Claude identifies areas of concern
2. Codex does deep review of specific complex sections
3. Claude consolidates findings and proposes changes

## Error Handling

**"OPENAI_API_KEY not set"**: Add to `~/.secrets/api-keys.sh`:

```bash
export OPENAI_API_KEY='your-key-here'
```

Then restart terminal or run `source ~/.zshrc`.

**API errors**: Check model name is valid, prompt isn't too long, API key has sufficient credits.

**Empty response**: May indicate rate limiting or model overload. Wait and retry.

## Example Session

```
User: I'm stuck on optimizing this database query. Can you get Codex's input?

Claude: I'll prepare a prompt for Codex with the query details and our performance requirements.

[Claude runs:]
~/.claude/skills/codex-oracle/scripts/call-openai.sh "
## Task
Optimize this PostgreSQL query for sub-100ms execution on 10M row table.

## Current Query
SELECT u.*, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id
ORDER BY order_count DESC
LIMIT 100;

## Context
- users table: 10M rows, indexed on id, email, created_at
- orders table: 50M rows, indexed on id, user_id, created_at
- Current execution: 2.3 seconds
- PostgreSQL 15

## Requirements
- Must maintain same result set
- Prefer query changes over schema changes
- If indexes needed, specify exact definition
"

[GPT-5.2-Codex responds with detailed optimization plan]

Claude: Codex suggests three optimizations:
1. Add a partial index on orders for recent users
2. Rewrite as a CTE to leverage index-only scans
3. Consider a materialized view for this specific dashboard query

Let me verify these work with our actual schema...
```

## Security Notes

- Never include secrets or credentials in prompts to Codex
- The API key is stored in your environment, not in this skill
- Responses from Codex should be reviewed before applying to production code
