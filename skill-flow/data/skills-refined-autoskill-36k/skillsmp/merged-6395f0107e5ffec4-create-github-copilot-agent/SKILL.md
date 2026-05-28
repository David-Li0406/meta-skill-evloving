---
name: create-github-copilot-agent
description: Use this skill when you need to create structured GitHub Copilot agent files for specialized workflows or scaffold new agents with proper frontmatter and best practices.
---

# Create GitHub Copilot Agent

This skill helps you create new GitHub Copilot agents with proper structure, frontmatter, and tailored expertise for specific development tasks.

## When to Use This Skill

- User asks to "create an agent", "make custom agent", or "scaffold agent"
- Need specialized workflow for specific task types
- Want focused behavior for testing, planning, refactoring, security, etc.
- Creating task-specific assistants that can be assigned to issues
- HR needs to generate candidate agents or scaffolding agent files for the team

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

### Recommended for Complex Tasks

| Model | Provider | Best For |
|-------|----------|----------|
| `claude-sonnet-4` | Anthropic | Excellent reasoning, code quality |
| `gpt-4o` | OpenAI | Versatile, good all-around performance |

### Recommended for Simple Tasks

| Model | Provider | Best For |
|-------|----------|----------|
| `gpt-4o-mini` | OpenAI | Fast, cheap, good for simple operations |

## Best Practices

### 1. Clear Purpose
Each agent should have ONE main responsibility. Avoid swiss-army-knife agents.

### 2. Proactive Description
Always include "Use PROACTIVELY when..." to enable automatic delegation.

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

## Validation Checklist

Before committing a custom agent:

- [ ] File ends with `.agent.md` (recommended) or `.md`
- [ ] Located in `.github/agents/`
- [ ] Has `name` in YAML frontmatter
- [ ] Has `description` in YAML frontmatter
- [ ] Name is lowercase with hyphens
- [ ] Description is clear and specific
- [ ] Tools are appropriately limited (if not all tools needed)
- [ ] Prompt is under 30,000 characters
- [ ] Responsibilities are clearly defined
- [ ] Behavioral constraints are specified
- [ ] Output format is defined (if applicable)
- [ ] Agent has been tested with sample tasks

## External Resources

Check existing agents before creating new ones:
- [github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/agents)
- [anthropics/skills](https://github.com/anthropics/skills)