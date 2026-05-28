# Parallel Investigation Strategies

Use Claude Code's built-in subagents to efficiently explore codebases without bloating main context.

## When to Use Parallel Exploration

| Scenario | Agents | Thoroughness |
|----------|--------|--------------|
| Single feature area | 1 | medium |
| Cross-cutting concerns | 2-3 | medium each |
| Full architecture review | 2-3 | very thorough |
| Quick file discovery | 1 | quick |

## Parallel Exploration Pattern

Launch multiple Explore agents in a single message for independent investigations:

```
Agent 1: Use the Explore agent (medium thoroughness) to find:
- All files in the authentication module
- Existing auth patterns and middleware
- Related test files

Agent 2: Use the Explore agent (medium thoroughness) to find:
- Database models and schemas
- Migration patterns
- ORM usage examples

Agent 3: Use the Explore agent (quick thoroughness) to find:
- Configuration files
- Environment variable usage
- Deployment scripts
```

## Investigation Focus Areas

| Focus | What to Look For |
|-------|------------------|
| **Patterns** | Existing implementations of similar features |
| **Structure** | Directory organization, naming conventions |
| **Dependencies** | Import chains, shared utilities |
| **Testing** | Test patterns, fixtures, mocks |
| **Config** | Environment handling, feature flags |

## Benefits of Parallel Investigation

1. **Context isolation** - Each agent uses separate context
2. **Speed** - Small model size (haiku) processes quickly
3. **Thoroughness** - Multiple perspectives on codebase
4. **Main context preserved** - Results summarized, not raw file contents

## Anti-Patterns

- **Too many agents** - Maximum 3 per round
- **Overlapping scope** - Each agent should have distinct focus
- **Sequential when parallel possible** - Launch independent searches together
- **Exploring known code** - Use direct Read for files you've already identified
