# faion-claude-code/references

## Overview

Technical reference files for Claude Code component creation. Each file provides detailed guidance for a specific component type including syntax, examples, naming conventions, and troubleshooting.

Total: ~2,185 lines of technical reference.

---

## Files

### skills.md (~346 lines)

Guide for creating and updating SKILL.md files.

**Contents:**
- Token economy rules (keep under 300 lines)
- SKILL.md frontmatter fields (name, description, allowed-tools, model, context, user-invocable)
- Built-in tools reference (Read, Write, Edit, Bash, Task, etc.)
- allowed-tools syntax with prefix matching (`Bash(git:*)`)
- Naming conventions (global `faion-{role}`, project `{project}-{name}`)
- SKILL.md body template
- Local/private skill setup (gitignore pattern)
- Troubleshooting common issues
- Automation scripts locations

---

### agents.md (~361 lines)

Guide for creating subagents with isolated context.

**Contents:**
- Agents vs Skills vs Commands comparison
- Agent file format and frontmatter (name, description, model, tools, skills, permissionMode)
- Available tools for agents
- Naming conventions (global `faion-{name}-agent`, project `{project}-{name}-agent`)
- Best practices and tool scoping by role
- Built-in agents (Explore, Plan, general-purpose)
- Prompt writing guidelines (role, input/output contract, workflow, rules)
- Parallel execution and pipeline patterns
- Creation process checklist
- Example agents (researcher, implementer)

---

### commands.md (~288 lines)

Guide for creating slash commands.

**Contents:**
- Commands vs Skills differences
- Command file format and frontmatter (description, argument-hint, allowed-tools, model)
- Argument syntax ($1, $2, $ARGUMENTS)
- Special syntax (! for Bash execution, @ for file references)
- Built-in tools (permission required vs not)
- Command locations (project, personal, namespaced)
- Naming conventions (global `{verb}`, project `{project}-{action}`)
- Examples (simple, with arguments, with context)
- Troubleshooting
- SlashCommand to Skill tool migration note (Jan 2026)

---

### hooks.md (~484 lines)

Guide for lifecycle automation scripts.

**Contents:**
- Hook events table (PreToolUse, PostToolUse, PermissionRequest, UserPromptSubmit, Stop, SubagentStop, Notification, SessionStart, SessionEnd, PreCompact)
- Configuration locations (settings.json, component frontmatter, plugins)
- Basic JSON structure
- Exit codes (0 = success, 2 = blocking error)
- Input schema (common fields, tool-specific: Bash, Write, Edit, MCP)
- Output schema (PreToolUse decision, Stop decision, UserPromptSubmit decision)
- Matcher patterns (exact, regex, pipe-separated, wildcard)
- Environment variables (CLAUDE_PROJECT_DIR, CLAUDE_CODE_REMOTE, etc.)
- Templates (Python, Bash, component-scoped YAML)
- Common patterns (auto-approve, block dangerous, auto-format, context injection, prevent exit, logging, file protection)
- Naming conventions (global `faion-{event}-{purpose}-hook`, project `{project}-{event}-{purpose}-hook`)
- Security best practices
- Debugging commands

---

### mcp.md (~706 lines)

Comprehensive MCP server reference.

**Contents:**
- Creating MCP servers in TypeScript (npm setup, McpServer class, tools, resources)
- Creating MCP servers in Python (FastMCP recommended, official SDK)
- MCP Server Catalog by category:
  - Marketing and Ads (Google Ads, Meta Ads, Mailgun, SendGrid)
  - Product Analytics (Mixpanel, Amplitude, PostHog, Stripe)
  - Project Management (Jira, Linear, ClickUp, Trello, Monday, Asana)
  - Development (GitHub, GitLab, PostgreSQL, Redis, Docker)
  - Design (Figma)
  - Knowledge and Docs (Airtable, Notion, Google Sheets, Confluence)
  - Social Media (Twitter/X, Instagram, LinkedIn, Telegram)
  - E-commerce (Stripe, Shopify)
  - AI and Generative (OpenAI/DALL-E, Replicate, ElevenLabs)
  - Infrastructure (Cloudflare, Hetzner, AWS, Vercel)
  - Browser and Automation (Puppeteer, Playwright)
  - Communication (Slack, Discord)
  - Memory (@anthropic/memory-mcp)
- Templates (API wrapper TypeScript, Database wrapper Python)
- Publishing to npm and PyPI
- Testing and debugging (MCP Inspector, FastMCP dev)
- Configuration via CLI and settings.json
- Troubleshooting table

---

## Usage

These references are loaded automatically by the skill based on request keywords. They can also be read directly when detailed information is needed for a specific component type.
