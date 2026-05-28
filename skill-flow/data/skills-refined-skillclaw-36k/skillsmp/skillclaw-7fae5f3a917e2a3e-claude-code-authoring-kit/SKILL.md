---
name: claude-code-authoring-kit
description: Use this skill when creating Claude Code extensions or configuring Claude Code features, including Skills, sub-agents, plugins, and more.
---

# Claude Code Authoring Kit

Comprehensive reference for Claude Code Skills, sub-agents, plugins, slash commands, hooks, memory, settings, sandboxing, headless mode, and advanced agent patterns.

## Documentation Index

### Core Features:

- **Skills**: Agent Skills creation and management
- **Sub-agents**: Development and delegation of specialized assistants
- **Plugins**: Architecture and distribution of plugins
- **Slash Commands**: Creation and orchestration of custom commands

### Configuration:

- **Settings**: Configuration hierarchy and management
- **Memory**: Context and knowledge persistence
- **Hooks**: Event-driven automation
- **Access Control**: Security and permissions management

### Advanced Features:

- **Sandboxing**: Security isolation for safe execution
- **Headless Mode**: Programmatic and CI/CD usage
- **Devcontainers**: Containerized environments for development
- **CLI Reference**: Command-line interface usage
- **Status Line**: Custom status display
- **Agent Patterns**: Engineering best practices for advanced agent design

## Quick Reference

- **Skills Location**: Model-invoked extensions can be found in `~/.claude/skills/` (personal) or `.claude/skills/` (project).
- **Progressive Disclosure**: Features are revealed progressively based on user interaction, with a maximum of 500 lines for Skills.
- **Trigger Conditions**: Keywords and phases for loading features include "skill", "agent", "plugin", "slash command", "hook", "sandbox", "headless", "memory", "settings", and more.