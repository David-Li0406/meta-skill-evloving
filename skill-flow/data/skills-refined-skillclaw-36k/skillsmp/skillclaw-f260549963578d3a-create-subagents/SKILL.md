---
name: create-subagents
description: Use this skill when you need to create and configure specialized subagents in Claude Code for specific tasks or workflows.
---

# Skill body

## Overview

Subagents are specialized AI assistants that operate in isolated contexts, allowing for focused roles and limited tool access. This skill guides you through creating effective subagents, writing strong system prompts, configuring tool access, and orchestrating multi-agent workflows using the Task tool.

## Quick Start

### Step 1: Create the Subagent

1. Run the `/agents` command in Claude Code.
2. Select **Create New Agent**.
3. Choose the scope:
   - **Project-level**: `.claude/agents/` (current project only)
   - **User-level**: `~/.claude/agents/` (available in all projects)
4. Define the subagent:
   - **name**: Use lowercase letters and hyphens (e.g., `code-reviewer`).
   - **description**: Clearly state what this subagent does and when it should be used.
   - **tools**: Optional comma-separated list of tools (inherits all if omitted).
   - **model**: Optional (`sonnet`, `opus`, `haiku`, or `inherit`).
5. Write the system prompt (the subagent's instructions).

### Step 2: Validate the Subagent

**Always run validation after creating or modifying an agent:**

```sh
uv run .claude/skills/meta-agent-creator/scripts/validate-agent.py .claude/agents/your-agent-name.md
```

Fix any errors before committing.

## Example Subagent Definition

```markdown
---
name: code-reviewer
description: Expert code reviewer. Use proactively after code changes to review for quality, security, and best practices.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior code reviewer focused on quality, security, and best practices.

## Focus Areas
- Code quality and maintainability
- Security vulnerabilities
- Performance issues
- Best practices adherence

## Output Format
Provide specific, actionable feedback with file:line references.
```

## Managing Subagents

Use the `/agents` command for interactive agent management (view, create, edit, delete).

## Built-in Agents

Claude Code includes several built-in agents for common tasks, such as `Explore`, `Plan`, and `General-purpose`. Custom agents can be created to handle specific workflows or domain expertise.

## When to Create Custom Agents

- **Domain expertise**: For tasks like security audits, database migrations, or API design.
- **Workflow automation**: For tasks like test runners, deployment, or documentation.
- **Tool restrictions**: For read-only reviewers or sandboxed explorers.
- **Team consistency**: For shared agents across common workflows.

## Conclusion

Creating subagents allows for delegation of complex tasks to specialized agents that operate autonomously, returning their final output to the main conversation. Use this skill to streamline your workflows and enhance productivity in Claude Code.