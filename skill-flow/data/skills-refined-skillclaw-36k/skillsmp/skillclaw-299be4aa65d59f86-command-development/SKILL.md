---
name: command-development
description: Use this skill when you need to create, add, or write a custom slash command for Claude, including defining command arguments, using frontmatter, and understanding command structure and best practices.
---

# Command Development for Claude Code

## Overview

Slash commands are frequently-used prompts defined as Markdown files that Claude executes during interactive sessions. Understanding command structure, frontmatter options, and dynamic features enables creating powerful, reusable workflows.

**Key concepts:**

- Markdown file format for commands
- YAML frontmatter for configuration
- Dynamic arguments and file references
- Bash execution for context
- Command organization and namespacing

## Command Basics

### What is a Slash Command?

A slash command is a Markdown file containing a prompt that Claude executes when invoked. Commands provide:

- **Reusability**: Define once, use repeatedly
- **Consistency**: Standardize common workflows
- **Sharing**: Distribute across team or projects
- **Efficiency**: Quick access to complex prompts

### Critical: Commands are Instructions FOR Claude

**Commands are written for agent consumption, not human consumption.**

When a user invokes `/command-name`, the command content becomes Claude's instructions. Write commands as directives TO Claude about what to do, not as messages TO the user.

**Correct approach (instructions for Claude):**

```markdown
Review this code for security vulnerabilities including:
- SQL injection
- XSS attacks
- Authentication issues

Provide specific line numbers and severity ratings.
```

**Incorrect approach (messages to user):**

```markdown
This command will review your code for security issues.
You'll receive a report with vulnerability details.
```

The first example tells Claude what to do. The second tells the user what will happen but doesn't instruct Claude. Always use the first approach.

### Command Locations

**Project commands** (shared with team):
- Location: `.claude/commands/`
- Scope: Available in specific project
- Label: Shown as "(project)" in `/help`
- Use for: Team workflows, project-specific tasks

**Personal commands** (available only to you):
- Location: `.claude/personal-commands/`
- Scope: Available in all projects
- Label: Shown as "(personal)" in `/help`
- Use for: Individual workflows and tasks