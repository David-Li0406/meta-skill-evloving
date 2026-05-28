---
name: plan-forge-cli
description: Run plan-forge CLI directly to generate development plans. Use when user asks to run plan-forge, generate a plan via CLI, or needs to use plan-forge commands directly (not via MCP). Covers new plans, resume, feedback, and provider configuration.
---

# Plan-Forge CLI

Run plan-forge directly via command line to generate iterative development plans.

## Quick Start

```bash
# Set API key
export ANTHROPIC_API_KEY="your-key"

# Generate a plan
plan-forge run --task "Add user authentication"

# Or with cargo (from repo)
cargo run -- run --task "Add user authentication"
```

## Core Commands

### New Plan from Task String

```bash
plan-forge run --task "your task description"
```

### New Plan from File

```bash
# Task from markdown file
plan-forge run --path requirements.md

# File + additional context
plan-forge run --path requirements.md --task "Focus on security"
```

### Resume Existing Plan

```bash
# Resume from plan directory
plan-forge run --path plans/active/my-task-slug/

# Resume with feedback
plan-forge run --path plans/active/my-task-slug/ --task "Use JWT instead of sessions"

# Resume by session ID
plan-forge run --session-id my-task-slug --feedback "Add rate limiting"
```

## CLI Options

| Option | Short | Description |
|--------|-------|-------------|
| `--task` | `-t` | Task description (or feedback when resuming) |
| `--path` | `-p` | Path to task file or existing plan directory |
| `--working-dir` | `-w` | Working directory for planning |
| `--output` | `-o` | Output directory (default: `./plans/active`) |
| `--verbose` | `-v` | Enable debug logging |
| `--threshold` | | Review pass threshold 0.0-1.0 (default: 0.8) |
| `--max-iterations` | | Max iterations before stopping (default: 10) |
| `--max-total-tokens` | | Token budget limit (-1 for unlimited) |

## Output Paths

| Path | Purpose |
|------|---------|
| `.plan-forge/<slug>/` | Session state (orchestrator memory) |
| `plans/active/<slug>/` | Output files (plan markdown) |

## Provider Configuration

### Anthropic (Default)

```bash
export ANTHROPIC_API_KEY="your-key"
plan-forge run --task "your task"
```

### OpenAI

```bash
export OPENAI_API_KEY="your-key"
plan-forge run --task "your task" \
  --planner-provider openai \
  --reviewer-provider openai
```

### LiteLLM Proxy

```bash
export LITELLM_HOST=http://localhost:4000
export LITELLM_API_KEY=sk-xxx
export PLAN_FORGE_PLANNER_PROVIDER=litellm
export PLAN_FORGE_PLANNER_MODEL=claude-opus-4.5
export PLAN_FORGE_REVIEWER_PROVIDER=litellm
export PLAN_FORGE_REVIEWER_MODEL=claude-opus-4.5
plan-forge run --task "your task" --max-total-tokens -1
```

### Microsoft Foundry

```bash
export MICROSOFT_FOUNDRY_RESOURCE=foundry-myresource
export MICROSOFT_FOUNDRY_API_KEY=your-key
export PLAN_FORGE_ORCHESTRATOR_PROVIDER=microsoft_foundry
export PLAN_FORGE_ORCHESTRATOR_MODEL=claude-opus-4-5
export PLAN_FORGE_PLANNER_PROVIDER=microsoft_foundry
export PLAN_FORGE_PLANNER_MODEL=claude-opus-4-5
export PLAN_FORGE_REVIEWER_PROVIDER=microsoft_foundry
export PLAN_FORGE_REVIEWER_MODEL=claude-opus-4-5
plan-forge run --task "your task"
```

## Workflow Examples

### Example 1: Generate and Iterate

```bash
# Initial plan
plan-forge run --task "Add REST API for user management" --verbose

# Check output
cat plans/active/add-rest-api-for-user-management/add-rest-api-for-user-management-plan.md

# Resume with feedback
plan-forge run --path plans/active/add-rest-api-for-user-management/ \
  --task "Use FastAPI instead of Flask"
```

### Example 2: Plan from Requirements File

```bash
# Create requirements file
cat > requirements.md << 'EOF'
Task: Implement OAuth2 Authentication

Objective: Add OAuth2 login with Google and GitHub providers.

Success Criteria:
- Users can log in via Google OAuth
- Users can log in via GitHub OAuth
- Session tokens stored in Redis

Context:
- Follow pattern in src/auth/session.rs
- Add tests to tests/auth/oauth_test.rs
EOF

# Generate plan
plan-forge run --path requirements.md
```

### Example 3: Verbose Debug Mode

```bash
# See iteration details
plan-forge run --task "Refactor database layer" --verbose

# With token limit
plan-forge run --task "Complex refactor" --max-total-tokens 100000 --verbose
```

## Exit Conditions

Plan-forge stops when:
- Plan passes review (score >= 0.80)
- Max iterations reached (default: 10)
- Human input required (ambiguity or security concern flagged)
- Token budget exhausted

## Tips

1. **Use verbose mode** (`-v`) to see iteration progress and review scores
2. **Set working directory** (`-w`) when planning for a different project
3. **Use file input** (`--path`) for complex tasks requiring detailed context
4. **Resume with feedback** to refine plans without starting over
5. **Check .plan-forge/** for session state if you need to debug
