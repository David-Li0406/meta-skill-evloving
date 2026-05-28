# Decision Guide: Commands vs Skills vs Subagents

When to use each Claude Code extension mechanism.

## Overview

| Feature | Invocation | Context | Best For |
|---------|------------|---------|----------|
| **Slash Commands** | User-invoked (`/command`) | Shared with main conversation | Repeatable tasks, quick shortcuts |
| **Skills** | Model-invoked (auto-detected) | Can include scripts/assets | Domain expertise, complex workflows |
| **Subagents** | Delegated by Claude | Own context window | Parallel work, specialized roles |

## Slash Commands

### What They Are

Markdown files containing prompts that execute when you type `/command-name`. They're essentially saved prompts with optional tool permissions and context injection.

### When to Use

✅ **Use slash commands for:**
- Quick, repeatable tasks you trigger manually
- Git workflows (commit, push, PR creation)
- Code review shortcuts
- Team-shared workflows (checked into git)
- Simple automations you want explicit control over

❌ **Don't use slash commands for:**
- Complex workflows needing scripts or templates
- Tasks Claude should auto-detect and handle
- Operations requiring isolated context

### Examples

```
# Good slash command use cases
/commit          - Quick git commit
/fix-issue 123   - Fix specific GitHub issue
/review          - Run code review
/deploy staging  - Deploy to environment
```

### Key Characteristics

- **Location:** `.claude/commands/` (project) or `~/.claude/commands/` (personal)
- **Trigger:** Manual (type `/command`)
- **Context:** Shares main conversation context
- **Complexity:** Simple to moderate

## Skills

### What They Are

Directories with `SKILL.md` plus optional scripts, references, and assets. Claude automatically loads relevant skills based on your request.

### When to Use

✅ **Use skills for:**
- Domain expertise Claude should apply automatically
- Workflows requiring scripts or templates
- Complex multi-file operations
- Company-specific knowledge and processes
- Tasks where Claude should "just know" what to do

❌ **Don't use skills for:**
- Simple shortcuts you want manual control over
- One-off tasks
- Quick git operations

### Examples

```
# Good skill use cases
- Document generation (docx, xlsx, pptx, pdf)
- Database schema knowledge
- Company coding standards
- API integration patterns
- Brand guidelines for content
```

### Key Characteristics

- **Location:** `.claude/skills/` (project) or `~/.claude/skills/` (personal)
- **Trigger:** Automatic (Claude decides based on description)
- **Context:** Loaded on-demand, can include rich resources
- **Complexity:** Moderate to high

### Structure

```
skill-name/
├── SKILL.md           # Main instructions
├── scripts/           # Executable code
├── references/        # Documentation
└── assets/            # Templates, images
```

## Subagents

### What They Are

Specialized AI instances that Claude delegates tasks to. Each subagent has its own context window and can work in parallel.

### When to Use

✅ **Use subagents for:**
- Parallel execution of multiple tasks
- Specialized roles (security auditor, test writer, etc.)
- Tasks needing isolated context (won't pollute main chat)
- Complex multi-step operations with different expertise needs

❌ **Don't use subagents for:**
- Simple sequential tasks
- Quick operations
- Tasks where main Claude context is needed

### Examples

```
# Good subagent use cases
- Launch 5 parallel search agents
- Security auditor reviewing code
- Test generator writing unit tests
- Documentation writer updating docs
- Parallel code reviewers for different aspects
```

### Key Characteristics

- **Location:** `.claude/agents/` (project) or `~/.claude/agents/` (personal)
- **Trigger:** Delegated by main Claude or explicitly called
- **Context:** Separate context window per agent
- **Complexity:** High (parallel coordination)

## Decision Framework

### Start Here

```
Do you want manual control over when this runs?
├── YES → Slash Command
└── NO → Continue...

Does it need scripts, templates, or rich resources?
├── YES → Skill
└── NO → Continue...

Does it need isolated context or parallel execution?
├── YES → Subagent
└── NO → Continue...

Is it domain expertise Claude should auto-apply?
├── YES → Skill
└── NO → Slash Command
```

### Quick Reference

| Scenario | Best Choice |
|----------|-------------|
| "Run this when I type /deploy" | Slash Command |
| "Claude should know our coding standards" | Skill |
| "Run 5 searches in parallel" | Subagent |
| "Quick git commit shortcut" | Slash Command |
| "Generate Excel with our schema" | Skill |
| "Security review as a specialist" | Subagent |
| "Team PR workflow in git" | Slash Command |
| "Auto-detect when I need help with PDFs" | Skill |
| "Multiple reviewers for different aspects" | Subagent |

## Combining Approaches

These mechanisms work together:

### Commands + Subagents

Slash command that orchestrates subagents:
```markdown
---
description: Find duplicate issues using parallel search
allowed-tools: Bash(gh:*), Task
---

Launch 5 parallel agents to search for duplicates...
```

### Commands + Skills

Command that leverages skill knowledge:
```markdown
---
description: Generate report using company template
---

Generate a quarterly report. Use the reporting skill for format.
```

### Subagents with Skills

Subagent definition that references skills:
```markdown
---
name: security-reviewer
description: Security specialist for code review
tools: Read, Grep, Glob
---

Use the security skill guidelines when reviewing...
```

## Migration Patterns

### Command → Skill

When a command grows too complex:

**Before (command):**
```markdown
# .claude/commands/review.md
Review this code for security and performance issues...
```

**After (skill):**
```
.claude/skills/code-review/
├── SKILL.md
├── scripts/run-linters.sh
└── references/
    ├── security-checklist.md
    └── performance-patterns.md
```

### When to Migrate

Consider migrating command → skill when:
- You're adding script files
- You need reference documentation
- Claude should auto-detect when to use it
- Multiple related commands could consolidate

## Summary

| | Slash Commands | Skills | Subagents |
|---|---|---|---|
| **Control** | You decide when | Claude decides when | Claude delegates |
| **Complexity** | Low-Medium | Medium-High | High |
| **Context** | Shared | On-demand | Isolated |
| **Parallelism** | No | No | Yes |
| **Resources** | Prompt only | Scripts, assets, refs | Own prompt |
| **Best for** | Shortcuts | Expertise | Specialists |
