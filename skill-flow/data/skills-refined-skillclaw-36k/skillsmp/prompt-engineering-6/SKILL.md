---
name: prompt-engineering
description: Create and optimize prompts for AI agents and subagent spawning. Use when asked to "craft a prompt", "improve this prompt", "create agent instructions", "spawn a subagent with...", "design agent definition", "hire a new agent", "optimize agent performance", "this agent isn't working", or "refine instructions". Handles technique selection, model-specific optimization, framework application (COSTAR, CRISPE, 5C), and anti-pattern detection.
allowed-tools: Read, Write
---

# Prompt Engineering

Create effective prompts for agents, subagents, and complex AI tasks.

## Quick Decision Tree

```
What do you need?
│
├─ Simple direct task?
│  └─ Read: references/techniques/zero-shot.md
│
├─ Learn from examples?
│  └─ Read: references/techniques/few-shot.md
│
├─ Show reasoning?
│  └─ Read: references/techniques/cot.md
│
├─ Explore multiple solutions?
│  └─ Read: references/techniques/tot.md
│
├─ Use external tools?
│  └─ Read: references/techniques/react.md
│
├─ High accuracy needed?
│  └─ Read: references/techniques/self-consistency.md
│
├─ Quality control loop?
│  └─ Read: references/techniques/constitutional-ai.md
│
├─ Domain expertise?
│  └─ Read: references/techniques/role-based.md
│
├─ Well-structured task?
│  └─ Read: references/frameworks/costar.md
│
├─ Creative/exploratory?
│  └─ Read: references/frameworks/crispe.md
│
├─ Complex workflow?
│  └─ Read: references/frameworks/5c.md
│
├─ Creating an agent?
│  └─ Read: references/examples/agent-definition.md
│
├─ Spawning subagent?
│  └─ Read: references/examples/subagent-spawn.md
│
└─ Debugging failing prompt?
   └─ Read: references/anti-patterns.md
```

## When to Use This Skill

| User Says | Load This Reference |
|-----------|---------------------|
| "Create new agent" | `references/examples/agent-definition.md` |
| "Spawn subagent" | `references/examples/subagent-spawn.md` |
| "Fix this prompt" | `references/anti-patterns.md` |
| "Need high accuracy" | `references/techniques/self-consistency.md` |
| "Show reasoning" | `references/techniques/cot.md` |

## Technique Quick Reference

| When | Technique | File |
|------|-----------|------|
| Simple task | Zero-shot | `techniques/zero-shot.md` |
| Pattern learning | Few-shot | `techniques/few-shot.md` |
| Reasoning needed | CoT | `techniques/cot.md` |
| Multiple approaches | ToT | `techniques/tot.md` |
| External tools | ReAct | `techniques/react.md` |
| Critical accuracy | Self-Consistency | `techniques/self-consistency.md` |
| Quality control | Constitutional | `techniques/constitutional-ai.md` |
| Expert perspective | Role-based | `techniques/role-based.md` |

## Framework Quick Reference

| When | Framework | File |
|------|-----------|------|
| Structured output | COSTAR | `frameworks/costar.md` |
| Creative freedom | CRISPE | `frameworks/crispe.md` |
| Complex pipeline | 5C | `frameworks/5c.md` |

## Agent Definition (Inline Summary)

```markdown
---
name: agent-name
description: What + when triggers
model: opus | sonnet | haiku
type: coder | specialist
---

## Role & Responsibility
## Decision Authority (Can decide / Must escalate)
## Workflow (numbered steps)
## Anti-Patterns
## Examples
```

**Full example**: Read `references/examples/agent-definition.md`

## Subagent Spawn (Inline Summary)

```xml
<context>[Why task matters]</context>
<instructions>[Numbered steps]</instructions>
<constraints>[Hard limits]</constraints>
<output_format>[Exact structure]</output_format>
<success_criteria>[Measurable]</success_criteria>
```

**Full example**: Read `references/examples/subagent-spawn.md`

## Claude Optimizations (Always Apply)

1. **XML tags**: `<instructions>`, `<context>`, `<thinking>`, `<answer>`
2. **Be explicit**: "exactly 5 bullets" not "be brief"
3. **Bookend**: Critical instructions at start AND end

## Quality Checklist

- [ ] Output format specified
- [ ] Length bounded
- [ ] Success criteria defined
- [ ] No vague words ("good", "nice")

## Reference Structure

```
references/
├── techniques/          # Load ONE when technique needed
│   ├── zero-shot.md
│   ├── few-shot.md
│   ├── cot.md
│   ├── tot.md
│   ├── react.md
│   ├── self-consistency.md
│   ├── constitutional-ai.md
│   └── role-based.md
├── frameworks/          # Load ONE when framework needed
│   ├── costar.md
│   ├── crispe.md
│   └── 5c.md
├── examples/            # Load ONE when example needed
│   ├── agent-definition.md
│   ├── subagent-spawn.md
│   └── debugging-prompt.md
└── anti-patterns.md     # Load when debugging
```

**Principle**: Only load what you need. Each file is self-contained.
