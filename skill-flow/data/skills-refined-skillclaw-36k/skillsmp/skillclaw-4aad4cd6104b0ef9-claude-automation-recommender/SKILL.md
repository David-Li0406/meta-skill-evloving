---
name: claude-automation-recommender
description: Use this skill to analyze a codebase and recommend Claude Code automations (hooks, subagents, skills, slash commands, plugins, MCP servers) when optimizing workflows or setting up Claude Code for a project.
---

# Claude Automation Recommender

Analyze codebase patterns to recommend tailored Claude Code automations across all extensibility options.

**This skill is read-only.** It analyzes the codebase and outputs recommendations. It does NOT create or modify any files. Users implement the recommendations themselves or ask Claude separately to help build them.

## Output Guidelines

- **Recommend 1-2 of each type**: Don't overwhelm - surface the top 1-2 most valuable automations per category.
- **If user asks for a specific type**: Focus only on that type and provide more options (3-5 recommendations).
- **Tell users they can ask for more**: End by noting they can request more recommendations for any specific category.

## Automation Types Overview

| Type          | Best For                                                        |
|---------------|-----------------------------------------------------------------|
| **Hooks**     | Automatic actions on tool events (format on save, lint, block edits) |
| **Subagents** | Specialized reviewers/analyzers that run in parallel            |
| **Skills**    | Packaged expertise with workflows and reference material        |
| **Slash Commands** | Quick, repeatable prompts with arguments                  |
| **Plugins**   | Collections of skills that can be installed                     |
| **MCP Servers** | External tool integrations (databases, APIs, browsers, docs) |

## Workflow

### Phase 1: Codebase Analysis

Gather project context:

```bash
# Detect project type and tools
ls -la package.json pyproject.toml Cargo.toml go.mod pom.xml 2>/dev/null
cat package.json 2>/dev/null | head -50

# Check dependencies for MCP server recommendations
cat package.json 2>/dev/null | grep -E '"(react|vue|angular|next|express|fastapi|django|prisma|supabase|stripe)"'

# Check for existing Claude Code config
ls -la .claude/ CLAUDE.md 2>/dev/null

# Analyze project structure
ls -la src/ app/ lib/ tests/ components/ pages/ api/ 2>/dev/null
```

**Key Indicators to Capture:**

| Category          | What to Look For                                   | Informs Recommendations For |
|-------------------|----------------------------------------------------|-----------------------------|
| Language/Framework | package.json, pyproject.toml, import patterns     | Hooks, MCP server recommendations |
| Project Structure  | Directory layout, presence of specific files      | Subagents, Skills, Plugins  |
| Existing Config    | .claude/ directory, CLAUDE.md file                | Tailored recommendations     |