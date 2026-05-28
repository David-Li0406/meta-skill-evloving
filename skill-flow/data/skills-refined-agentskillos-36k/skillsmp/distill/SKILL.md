---
name: distill
description: Distill session episodes into persistent memory patterns
user_invocable: true
---

# /distill - Memory Distillation

Transforms episodic session logs into refined semantic memory patterns.

## Usage

```
/distill           # Distill episodes at current scope
/distill show      # Show current memory without distilling
/distill episodes  # Show pending episodes awaiting distillation
```

## How It Works

### Episode Collection

During agent work, learnings are logged to `.context/EPISODES.md`:

```markdown
## Session: 2026-01-10T14:30:00Z
- **Task**: Fix authentication bug
- **Outcome**: success
- **Learnings**:
  - JWT tokens need refresh handling in middleware
  - Error messages should include request ID
```

### Distillation Process

When `/distill` runs:

1. **Extract patterns** from each episode's learnings
2. **Classify** as pattern, pitfall, preference, or approach
3. **Match** against existing patterns in memory
4. **Reinforce** matching patterns (increases confidence)
5. **Add** new patterns with low initial confidence
6. **Decay** old patterns not recently reinforced
7. **Prune** patterns below confidence threshold

### Memory Output

Results are saved to `.context/MEMORY.md`:

```markdown
# Memory: [Scope]

## Patterns Observed
- JWT tokens need refresh handling
  Confidence: high | Last reinforced: 2026-01-10

## Pitfalls Discovered
- Avoid storing tokens in localStorage
  Confidence: medium | Last reinforced: 2026-01-08
```

## Implementation

When invoked, run:

```bash
python3 ~/.claude/plugins/agent-swarm/context/memory.py distill .
```

For showing memory:
```bash
python3 ~/.claude/plugins/agent-swarm/context/memory.py show .
```

For pending episodes:
```bash
python3 ~/.claude/plugins/agent-swarm/context/memory.py episodes .
```

## Logging Learnings

Agents can log learnings by including in their output:

```
LEARNING: [description of pattern, pitfall, or approach]
```

These are captured by post-task hooks and added to EPISODES.md.

## Confidence Mechanics

| Confidence | Meaning |
|------------|---------|
| 0.0 - 0.2 | Uncertain, may be pruned |
| 0.2 - 0.4 | Low, needs reinforcement |
| 0.4 - 0.7 | Medium, established pattern |
| 0.7 - 0.95 | High, well-validated |

- **Reinforcement**: Each observation increases confidence
- **Decay**: Patterns not seen in 30+ days lose confidence
- **Pruning**: Patterns below 0.2 are removed

## Automatic Distillation

Distillation triggers automatically when:
- Episode count exceeds threshold (default: 10)
- Session ends (if configured)
- Manually via `/distill` command
