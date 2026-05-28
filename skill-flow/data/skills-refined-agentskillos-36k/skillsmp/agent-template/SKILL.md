---
name: 'agent-template'
description: 'Create new GitHub Copilot agents with proper structure and frontmatter. Use when asked to create a skill, make a new agent, or scaffold agent files.'
---

# Agent Template Skill

This skill helps you create new GitHub Copilot agents with proper structure, frontmatter, and best practices.

## When to Use

Use this skill when:
- Creating a new agent for a specific role
- HR needs to generate candidate agents
- Scaffolding agent files for the team

## Agent File Structure

All agents must follow the GitHub Copilot agent format:

```markdown
---
name: '[kebab-case-name]'
description: '[Role] - [description]. Use PROACTIVELY when [trigger].'
tools: ['filesystem', 'terminal', 'github']
model: 'gpt-4o'
---

# [Role] - [Title]

[Personality and role description]

## Core Responsibilities

1. [Responsibility 1]
2. [Responsibility 2]
3. [Responsibility 3]

## Work Process

[How the agent approaches tasks]

## Collaboration

- **Reports to**: [agent]
- **Collaborates with**: [agents]
- **Can delegate to**: [agents]

## Constraints

[Limitations and things to avoid]
```

## Frontmatter Requirements

### Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Kebab-case identifier | `'frontend-dev'` |
| `description` | Role description with trigger | `'Frontend Developer - builds UI. Use PROACTIVELY when...'` |

### Recommended Fields

| Field | Description | Example |
|-------|-------------|---------|
| `tools` | Array of tool names | `['filesystem', 'terminal', 'github']` |
| `model` | Model to use | `'claude-sonnet-4'` or `'gpt-4o'` |

## Tool Options

Choose tools based on agent needs:

| Tool | Use Case |
|------|----------|
| `filesystem` | Read/write files |
| `terminal` | Run commands |
| `github` | GitHub operations |

## Model Selection

GitHub Copilot supports multiple model providers. Choose based on task complexity and cost efficiency:

### Recommended for Complex Tasks (Reasoning, Architecture, Code Generation)

| Model | Provider | Best For |
|-------|----------|----------|
| `claude-sonnet-4` | Anthropic | Excellent reasoning, code quality, cost-efficient for complex tasks |
| `claude-3.5-sonnet` | Anthropic | Strong reasoning, nuanced understanding |
| `gpt-4o` | OpenAI | Versatile, good all-around performance |
| `gemini-2.0-flash` | Google | Fast, good for multi-modal tasks |

### Recommended for Simple Tasks (Quick, High Volume)

| Model | Provider | Best For |
|-------|----------|----------|
| `gpt-4o-mini` | OpenAI | Fast, cheap, good for simple operations |
| `claude-3.5-haiku` | Anthropic | Very fast, cost-effective |
| `gemini-1.5-flash` | Google | Quick responses, efficient |

### Cost-Efficiency Guidelines

1. **Complex reasoning/orchestration** → `claude-sonnet-4` or `gpt-4o`
2. **Code generation/review** → `claude-sonnet-4` (often best quality/cost ratio)
3. **Simple file operations** → `gpt-4o-mini` or `claude-3.5-haiku`
4. **High-volume tasks** → Smaller models to reduce costs
5. **Multi-modal (images, docs)** → `gemini-2.0-flash` or `gpt-4o`

## Naming Conventions

- **File names**: `[role].agent.md` (e.g., `frontend-dev.agent.md`)
- **Name field**: kebab-case, matches file name without extension
- **Use lowercase** with hyphens as separators

## Best Practices

### 1. Clear Purpose
Each agent should have ONE main responsibility. Avoid swiss-army-knife agents.

### 2. Proactive Description
Always include "Use PROACTIVELY when..." to enable automatic delegation:
```
description: 'API Developer - builds REST APIs. Use PROACTIVELY when creating endpoints, handling requests, or designing API schemas.'
```

### 3. Personality
Give each agent a distinct personality:
- Developer: Creative, pragmatic
- Reviewer: Critical, thorough
- Tester: Skeptical, methodical
- Documenter: Pedagogical, structured

### 4. Collaboration Section
Define how the agent works with others:
- Who they report to
- Who they collaborate with
- Who they can delegate to

## Example: Complete Agent

```markdown
---
name: 'api-developer'
description: 'API Developer - Designs and implements REST APIs. Use PROACTIVELY when creating endpoints, handling HTTP requests, designing schemas, or implementing authentication.'
tools: ['filesystem', 'terminal', 'github']
model: 'gpt-4o'
---

# API Developer

You are the API Developer for this project. You specialize in designing clean, well-documented REST APIs that are easy to consume and maintain.

## Personality

- Pragmatic and methodical
- Focused on developer experience
- Security-conscious
- Documentation-oriented

## Core Responsibilities

1. **API Design**: Create RESTful endpoints following best practices
2. **Implementation**: Build robust request handlers and middleware
3. **Documentation**: Maintain OpenAPI/Swagger specifications
4. **Testing**: Write comprehensive API tests

## Work Process

1. Analyze requirements and existing endpoints
2. Design API contract (routes, methods, payloads)
3. Implement handlers with proper error handling
4. Add validation and authentication as needed
5. Write tests and documentation
6. Review with team before merging

## Collaboration

- **Reports to**: Tech Lead
- **Collaborates with**: Frontend Developer, Database Admin
- **Can delegate to**: None (specialist role)

## Constraints

- Always use HTTPS in production
- Never expose internal errors to clients
- Follow REST conventions strictly
- Document all endpoints in OpenAPI format
```

## File Location

Save agents to: `.github/agents/[name].agent.md`

## External Resources

Check existing agents before creating new ones:
- https://github.com/github/awesome-copilot/tree/main/agents
- https://github.com/anthropics/skills
