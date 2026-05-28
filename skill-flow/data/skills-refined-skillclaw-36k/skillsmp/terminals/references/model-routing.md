# Model Routing Guide

Route tasks to the most efficient model.

## Available Models

| Source | Model | Best For |
|--------|-------|----------|
| Claude Max | Opus | Brainstorming, complex implementation, architecture |
| Claude Max | Sonnet | General coding, reviews |
| Claude Max | Haiku | Quick exploration, simple tasks |
| Codex | codex | Code review, second opinion, bulk review |

## Claude Code Model Selection

```bash
# Spawn worker with specific model
claude --model haiku

# Or in agent frontmatter
model: haiku
```

## Routing Heuristics

| Task Type | Recommended Model |
|-----------|------------------|
| Brainstorming/ideation | Opus |
| Quick exploration | Haiku |
| Code implementation | Sonnet or Opus |
| Code review | Codex or Opus |
| Complex architecture | Opus |
| Quick fixes | Haiku |
| Documentation | Sonnet |
| Prompt writing | Haiku |
| Mechanical spawning | Haiku |
| Planning/decomposition | Sonnet |

## Worker Spawn Examples

```bash
# Haiku for exploration
curl -X POST http://localhost:8129/api/spawn \
  -d '{"command": "claude --model haiku"}'

# Sonnet for implementation
curl -X POST http://localhost:8129/api/spawn \
  -d '{"command": "claude --model sonnet"}'
```

## Plugin Agent Model Selection

Each plugin can specify model in agent frontmatter:

| Plugin | Agent | Model | Rationale |
|--------|-------|-------|-----------|
| prompt-writer | writer | Haiku | Fast, focused task |
| planner | planner | Sonnet | Needs reasoning |
| spawner | - | N/A | Mechanical, no agent |
| cleanup | cleanup | Haiku | Mechanical operations |
| conductor | orchestrator | Sonnet | Coordination decisions |
