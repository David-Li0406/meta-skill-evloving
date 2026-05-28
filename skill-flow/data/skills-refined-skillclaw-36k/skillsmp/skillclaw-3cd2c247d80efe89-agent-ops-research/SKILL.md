---
name: agent-ops-research
description: Use this skill when you need to conduct structured research on technologies, patterns, libraries, or any topic requiring investigation, with the option to create actionable items from findings.
---

# Research Skill

## Purpose

Conduct structured research on topics, technologies, libraries, patterns, or any subject requiring investigation. Produces documented findings with optional issue creation for actionable items.

## When to Use

- Evaluating a new technology or library
- Investigating best practices for a pattern
- Researching solutions to a problem
- Comparing alternatives (frameworks, tools, approaches)
- Understanding external APIs or services
- Preparing for a design decision

## Research Modes

### Quick Research (default)
Fast investigation using available tools and knowledge.

```
/agent-research "FastAPI vs Flask for REST APIs"
→ Quick comparison based on docs and knowledge
```

### Deep Research
Thorough investigation with documentation lookup, code analysis, and structured output.

```
/agent-research deep "Implementing OAuth2 in Python"
→ Detailed findings with examples and recommendations
```

### Comparative Research
Side-by-side evaluation of alternatives.

```
/agent-research compare "pytest vs unittest vs nose2"
→ Feature matrix, pros/cons, recommendation
```

## Research Procedure

### 1. Scope Definition

Before researching, clarify:
- **Topic**: What exactly are we researching?
- **Context**: Why do we need this information?
- **Constraints**: Time budget, depth required, specific questions?
- **Output**: What format is most useful?

If scope is unclear, invoke `agent-ops-interview` for one question at a time.

### 2. Information Gathering

**Sources (in priority order):**

1. **Workspace Context**
   - Existing code patterns
   - Project documentation
   - Constitution constraints
   - Previous research (`.agent/docs/`)

2. **Built-in Knowledge**
   - Language/framework documentation
   - Common patterns and best practices
   - Known tradeoffs and gotchas

3. **External Tools (if available)**
   - Web search via MCP tools
   - Documentation lookup
   - API exploration

4. **Code Analysis**
   - Read relevant source code
   - Analyze existing implementations
   - Check test patterns

### 3. Synthesis

Organize findings into:
- **Summary**: Key takeaways from the research.
- **Recommendations**: Actionable items based on findings.
- **Documentation**: Create or update relevant documents as needed.