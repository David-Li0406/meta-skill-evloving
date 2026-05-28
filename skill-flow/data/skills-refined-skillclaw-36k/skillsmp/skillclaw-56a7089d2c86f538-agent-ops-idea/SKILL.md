---
name: agent-ops-idea
description: Use this skill when you have a raw concept that needs fleshing out into a well-researched backlog issue.
---

# Agent Idea Workflow

## Purpose

Transform loosely structured ideas into well-researched IDEA issues in the backlog. This skill bridges the gap between "I have a vague idea" and "I have a trackable, researched issue ready for triage."

## When to Use

- User says "I have an idea for..." or invokes "/agent-idea"
- User describes a concept without clear requirements
- User wants to explore feasibility before committing to work
- Brainstorming sessions that should be captured

## MCP Integration (Optional Enhancement)

When MCP tools are available, use them to enhance research quality.

### Check MCP Availability

At skill start, check if MCP is configured:
1. Look for `.agent/mcp.yaml` or project's `mcp.yaml`
2. If present, MCP tools may be available for enhanced research

### Available MCP Tools

| Tool | Provider | Use Case |
|------|----------|----------|
| `brave_web_search` | brave-search | Search web for existing solutions, similar projects |
| `get_library_docs` | context7 | Get library documentation for relevant packages |
| `search_repositories` | github | Find similar open source implementations |
| `get_readme` | github | Fetch README from relevant repositories |

### Research Source Tags

When reporting research findings, tag sources with emojis:
- 🌐 = Web search (MCP: brave-search)
- 📚 = Library docs (MCP: context7)
- 🔍 = GitHub search (MCP: github)
- 💭 = Agent analysis (training data/reasoning)

### Graceful Fallback

If MCP tools fail or are unavailable:
1. **Log but don't block**: Note tool unavailability, continue with agent knowledge
2. **Tag appropriately**: Use 💭 tag for agent-sourced research
3. **Be transparent**: Mention in research notes that external tools were unavailable

Example fallback note:
```
⚠️ MCP tools unavailable — research based on agent knowledge.
For deeper research, enable MCP: `pip install agent-ops-cli[mcp]`
```

## Procedure

### Phase 1: Capture Raw Idea

1. **Accept idea text** from user (can be informal, incomplete, or vague)
2. **Echo back understanding**: "I understand you want to: {paraphrase}"
3. **Ask clarifying question** (optional, only if truly unclear):
   - "What problem does this idea aim to solve?"
4. **Document the idea** in the focus.md file.

### Phase 2: Research and Enrichment

1. **Utilize MCP tools** if available to gather relevant information.
2. **Compile findings** and tag sources appropriately.
3. **Draft a backlog issue** based on the enriched information.

### Phase 3: Finalization

1. **Review the drafted issue** with the user for feedback.
2. **Make necessary adjustments** based on user input.
3. **Create the final issue** in the issues/backlog.md file.
4. **Update the issue counter** in issues/.counter.