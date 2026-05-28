---
name: codebase-research
description: Patterns and methods for researching a codebase to understand bug context. Use when investigating how code works, finding related files, or understanding code flow.
license: MIT
compatibility: VS Code Insiders with GitHub Copilot
metadata:
  author: accruent
  version: "2.0"
  based-on: HumanLayer research_codebase pattern
---

# Codebase Research

This skill provides research patterns for bug investigation, following the HumanLayer documentarian philosophy.

## Core Principles

### The Documentarian Philosophy

From HumanLayer's research_codebase pattern:

> **YOUR ONLY JOB IS TO DOCUMENT AND EXPLAIN THE CODEBASE AS IT EXISTS TODAY**
> - DO NOT suggest improvements or changes
> - DO NOT perform root cause analysis (that's a separate phase)
> - DO NOT critique the implementation
> - ONLY describe what exists, where it exists, how it works

### Research Best Practices

1. **Read files FULLY first** - Never use limit/offset for initial reads
2. **Use a single comprehensive subagent** - VS Code subagents run sequentially
3. **Wait for subagent to complete** - Synthesize only after it returns
4. **Verify every claim** - Include file:line references
5. **Stay factual** - No opinions, evaluations, or suggestions

## VS Code Copilot Tool Reference

| Tool Identifier | Purpose | Example Usage |
|-----------------|---------|---------------|
| `search/codebase` | Semantic search | Find conceptually related code |
| `search/fileSearch` | File name patterns | Find `*.test.ts` files |
| `search/textSearch` | Grep-style search | Find exact error messages |
| `search/usages` | Symbol usages | Trace function calls |
| `read/readFile` | Read file contents | Get full context |
| `web/githubRepo` | Git/GitHub info | Historical context |
| `runSubagent` | Spawn subagent | Comprehensive research |
| `edit/editFiles` | Create files | Save research documents |

## Subagent Research Pattern

Since VS Code subagents run sequentially (not in parallel), combine all research tasks into a single comprehensive subagent prompt:

```
Use a subagent to perform comprehensive codebase research for bug {TICKET-ID}.

## Research Tasks

### Task 1: Locate Relevant Code
Find all locations related to: {bug symptoms}
- Search for: {keywords, function names, error messages}
- Return: Table of file:line references

### Task 2: Analyze Code Flow
For relevant files, document:
- Entry points, data flow, dependencies, exit points
- Return: Flow diagram with file:line citations

### Task 3: Find Related Patterns
Search for:
- Similar code, related tests, documentation
- Return: Examples with file:line references

## Rules
- Document only, no evaluations
- Include file:line for every claim
```

## Research Document Structure

### hypothesis.md
Initial investigation hypotheses created before research:
- Symptom analysis
- Investigation areas with search targets
- Priority order

### codebase-research.md
Comprehensive research findings:
- Code locations table
- Execution flow diagram
- Dependencies and relationships
- Exact code snippets with citations

### verified-research.md
Verification of research accuracy:
- Claim verification tables
- Corrections made
- Confidence ratings

## Templates

See the templates folder for:
- [research-template.md](templates/research-template.md) - Main research document
- [hypothesis-template.md](templates/hypothesis-template.md) - Initial hypotheses

## Forbidden Patterns

Never use these phrases in research documents:
- "This could be improved by..."
- "A better approach would be..."
- "This is a code smell..."
- "Consider refactoring..."
- "The problem is..."
- "This should be..."

## References

- [HumanLayer research_codebase.md](https://github.com/humanlayer/humanlayer/blob/main/.claude/commands/research_codebase.md)
- [VS Code Custom Agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [VS Code Subagents](https://code.visualstudio.com/docs/copilot/chat/chat-sessions#_context-isolated-subagents)
