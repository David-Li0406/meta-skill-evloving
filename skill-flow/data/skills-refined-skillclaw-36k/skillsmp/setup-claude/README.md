# Setup Claude Skill

A production-ready, CLI-first repository setup system that configures the **complete Claude Code ecosystem**: skills, commands, subagents, hooks, rules, MCPs, and plugins.

## Core Philosophy

1. **CLI-First**: Always prefer CLI tools over MCP (more token-efficient)
2. **Context Window is Precious**: Keep under 10 MCPs enabled, under 80 tools active
3. **Modular Configuration**: Rules in ~/.claude/rules/, not one mega CLAUDE.md
4. **Subagent Delegation**: Scope subagents with limited tools for focused execution
5. **Progressive Automation**: Hooks for formatting, linting, reminders

## Usage

### Initialize a New Repository

```bash
claude
> /setup-claude init
```

This runs a 13-phase setup process:
1. Environment & Global Tools Check
2. Project Scaffolding
3. Tech Stack Interview
4. CLI Discovery & Authentication
5. MCP Configuration (Context Window Aware)
6. Plugin Setup
7. Skills Installation
8. Subagent Configuration
9. Rules Configuration
10. Hooks Configuration
11. CLAUDE.md Generation
12. Ralph TUI Setup
13. Verification & Summary

### Audit an Existing Repository

```bash
cd existing-project
claude
> /setup-claude audit
```

This runs an 8-phase audit process:
1. Environment Analysis
2. CLI Audit
3. Context Window Analysis
4. Gap Analysis
5. Recommendations Report
6. Interactive Fixes
7. Context Window Optimization
8. Summary & Verification

## What Gets Configured

### Project-Level (`.claude/`)
```
.claude/
├── skills/           # Project-specific skills
├── commands/         # Project-specific commands
├── agents/           # Subagent definitions
├── rules/            # Modular best practice rules
└── settings.json     # Project hooks & permissions
```

### Files Created
- `CLAUDE.md` - Project context file with 10 required sections
- `.mcp.json` - MCP configuration (context-window aware)
- `.ralph-tui/` - Ralph TUI configuration and templates

### Global Tools Verified
- Claude Code (latest version)
- Agent Browser CLI
- Ralph TUI
- GitHub CLI (gh)
- Tech-stack specific CLIs (Vercel, Supabase, Stripe, etc.)

## Key Features

### CLI-First Philosophy
For each external service, the skill:
1. Detects the service from config files/dependencies
2. Looks up the official CLI
3. Checks if installed and authenticated
4. Only falls back to MCP when no CLI exists

### Context Window Management
- Tracks enabled MCPs and tool count
- Warns when exceeding recommended limits (10 MCPs, 80 tools)
- Offers optimization suggestions in audit mode

### Comprehensive CLAUDE.md
Generated with all 10 required sections:
1. Project Description
2. Development Workflow
3. Things NOT to Do
4. Common Code Practices
5. Commands (dev, test, build, lint)
6. Available Skills (with triggers)
7. MCP Servers (enabled + when to use)
8. Documentation Methods
9. Subagents (when to delegate)
10. General Guidelines

### Modular Rules
Instead of one mega CLAUDE.md, rules are split into:
- `security.md` - No hardcoded secrets, validate inputs
- `coding-style.md` - File organization, naming conventions
- `testing.md` - TDD workflow, coverage requirements
- `git-workflow.md` - Commit format, PR process

### Subagent Templates
Pre-configured subagents for common workflows:
- `planner.md` - Feature implementation planning
- `code-reviewer.md` - Quality/security review
- `tdd-guide.md` - Test-driven development
- `refactor-cleaner.md` - Dead code removal

## Skill Structure

```
setup-claude/
├── README.md                    # This file
├── SKILL.md                     # Entry point
├── workflows/
│   ├── init-new-repo.md         # 13-phase init workflow
│   └── audit-existing-repo.md   # 8-phase audit workflow
├── components/
│   ├── cli-discovery.md         # CLI research workflow
│   ├── mcp-management.md        # MCP setup + context management
│   ├── plugin-setup.md          # Essential plugins
│   ├── subagent-setup.md        # Subagent configuration
│   ├── rules-configuration.md   # Modular rules setup
│   ├── documentation-setup.md   # Context7 + web research
│   ├── hooks-configuration.md   # Sophisticated hook patterns
│   ├── tools-installation.md    # CLI-first tool setup
│   ├── skills-discovery.md      # User-invokable skills
│   ├── claudemd-writing.md      # All 10 required sections
│   └── folder-structure.md      # Project scaffolding
├── reference/
│   ├── tech-stack-clis.md       # CLI tools by tech stack
│   ├── mcp-servers.md           # MCP server configurations
│   ├── essential-plugins.md     # Plugin recommendations
│   ├── subagent-templates.md    # Common subagent patterns
│   ├── hook-patterns.md         # Enhanced hook patterns
│   ├── mandatory-skills.md      # Required skills
│   └── tech-stack-skills.md     # Tech-specific skills
└── templates/
    ├── ralph-tui/
    │   ├── config.toml          # Ralph TUI config
    │   └── prompt.hbs           # Prompt template
    ├── subagents/
    │   ├── planner.md
    │   ├── code-reviewer.md
    │   ├── tdd-guide.md
    │   └── refactor-cleaner.md
    ├── rules/
    │   ├── security.md
    │   ├── coding-style.md
    │   ├── testing.md
    │   └── git-workflow.md
    └── claude-md/
        └── complete-template.md
```

## Sources

This skill incorporates best practices from:
- Anthropic Claude Code Best Practices Guide
- Claude Skills Authoring Best Practices
- @affaanmustafa's "Shorthand Guide to Everything Claude Code" (10 months daily use)

## Related Skills

- `/prd` - Create product requirements documents
- `/agent-browser` - Browser automation and E2E testing
