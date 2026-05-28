---
name: consult-agents
description: Use when you need validation, analysis, or research from multiple AI agents before implementing. Gathers perspectives from Gemini and Codex, synthesizes feedback.
---

# Consult Agents

Get validation, analysis, or research feedback from Gemini and Codex before Claude Code implements.

**Core principle:** Claude Code implements. External agents validate and research.

## When to Use

- Validate an approach before implementing
- Research a topic from multiple perspectives
- Get code review feedback on a design
- Confirm understanding of requirements
- Aggregate opinions on trade-offs

## Quick Reference

| Task Type | Gemini Mode | Codex Mode |
|-----------|-------------|------------|
| Analyze code/files only | `gemini -p "..."` | `--sandbox read-only` |
| Research with web access | `gemini -p "..."` (has web search) | `--sandbox danger-full-access` |
| Deep repo analysis | tmux interactive | `--sandbox read-only` |

## Workflow

```
1. Prepare question/context (what you need validated)
2. Query Gemini → capture response
3. Query Codex → capture response
4. Synthesize: agreements, disagreements, insights
5. Claude Code decides and implements
```

## Parallel Execution

Run both agents simultaneously for faster feedback:

```bash
# Terminal 1: Gemini
gemini -p "Analyze this approach: [context]. What are the trade-offs?" 2>/dev/null

# Terminal 2: Codex
echo "Analyze this approach: [context]. What are the trade-offs?" | \
  codex exec --sandbox read-only --skip-git-repo-check -m gpt-5.2 2>/dev/null
```

Or use background jobs:
```bash
gemini -p "..." > /tmp/gemini-response.txt 2>/dev/null &
echo "..." | codex exec --sandbox read-only ... > /tmp/codex-response.txt 2>/dev/null &
wait
```

## Synthesis Template

After gathering responses, synthesize:

```markdown
## Agent Responses

### Gemini
[Summary of Gemini's perspective]

### Codex
[Summary of Codex's perspective]

## Synthesis

**Agreements:**
- [What both agents agree on]

**Disagreements:**
- [Where they differ and why]

**Key Insights:**
- [Unique valuable points from either]

## Decision
[Claude Code's decision based on aggregated feedback]
```

## Prompt Templates

### Validation
```
Review this [design/approach/code]:

[CONTEXT]

Questions:
1. Is this approach sound?
2. What are the risks?
3. What would you do differently?
```

### Research
```
Research [TOPIC] focusing on:
1. Current best practices
2. Common pitfalls
3. Recommended tools/libraries

Context: [Why you need this]
```

### Code Review
```
Review this code for:
- Correctness
- Performance concerns
- Security issues
- Maintainability

[CODE]
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Asking agents to implement | They validate; Claude Code implements |
| Not providing enough context | Include relevant code, constraints, goals |
| Ignoring disagreements | Disagreements reveal important trade-offs |
| Blindly following consensus | Use judgment; agents can both be wrong |

## When NOT to Use

- Simple, obvious implementations
- Time-critical changes (adds latency)
- Trivial questions (overkill)
