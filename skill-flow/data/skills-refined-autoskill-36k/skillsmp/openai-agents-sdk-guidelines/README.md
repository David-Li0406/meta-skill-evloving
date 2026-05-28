# OpenAI Agents SDK Guidelines

A structured repository for creating and maintaining OpenAI Agents SDK best practices optimized for agents and LLMs.

## Structure

- `rules/` - Individual rule files (one per rule)
  - `_sections.md` - Section metadata (titles, impacts, descriptions)
  - `_template.md` - Template for creating new rules
  - `area-description.md` - Individual rule files
- `references/` - Concise reference documents
- `metadata.json` - Document metadata (version, organization, abstract)
- __`AGENTS.md`__ - Compiled output (generated)
- __`SKILL.md`__ - Skill definition file

## Rule Categories

Rules are organized by filename prefix:

| Prefix | Category | Impact |
|--------|----------|--------|
| `agent-` | Agent Design | CRITICAL |
| `multi-agent-` | Multi-Agent Patterns | CRITICAL |
| `tool-` | Tools | HIGH |
| `guardrail-` | Guardrails | MEDIUM-HIGH |
| `context-` | Context Management | MEDIUM |
| `runner-` | Running Agents | MEDIUM |
| `conversation-` | Conversation Management | MEDIUM |
| `streaming-` | Streaming & Advanced | LOW-MEDIUM |

## Creating a New Rule

1. Copy `rules/_template.md` to `rules/area-description.md`
2. Choose the appropriate area prefix from the table above
3. Fill in the frontmatter and content
4. Ensure you have clear examples with explanations
5. Rules are automatically sorted by title within each section

## Rule File Structure

Each rule file should follow this structure:

```markdown
---
title: Rule Title Here
impact: MEDIUM
impactDescription: Optional description
tags: tag1, tag2, tag3
---

## Rule Title Here

Brief explanation of the rule and why it matters.

**Incorrect (description of what's wrong):**

```python
# Bad code example
```

**Correct (description of what's right):**

```python
# Good code example
```

Optional explanatory text after examples.

Reference: [Link](https://example.com)
```

## Impact Levels

- `CRITICAL` - Highest priority, foundational patterns
- `HIGH` - Significant functionality improvements
- `MEDIUM-HIGH` - Important optimizations
- `MEDIUM` - Moderate improvements
- `LOW-MEDIUM` - Incremental improvements
- `LOW` - Edge case optimizations

## Key Concepts

### Agent
The core building block - an LLM configured with instructions and tools.

### Tools
Actions agents can take: function tools, hosted tools, agents-as-tools, MCP servers.

### Handoffs
Delegation mechanism where one agent transfers control to another.

### Guardrails
Validation checks on input (before agent runs) and output (after agent completes).

### Context
Dependency injection for passing state and dependencies to agents/tools.

### Runner
The execution engine that orchestrates agent runs and handles the agent loop.

## References

- [OpenAI Agents SDK Documentation](https://openai.github.io/openai-agents-python/)
- [GitHub Repository](https://github.com/openai/openai-agents-python)
- [Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
