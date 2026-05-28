# Documentation Topics Reference

Quick reference mapping topics to documentation files. Use this to quickly find the right doc.

## Table of Contents

- [Core Concepts](#core-concepts)
- [Extending Claude Code](#extending-claude-code)
- [Configuration](#configuration)
- [Security](#security)
- [IDE Integrations](#ide-integrations)
- [CI/CD & Automation](#cicd--automation)
- [Cloud Providers](#cloud-providers)
- [Advanced Features](#advanced-features)
- [Help & Troubleshooting](#help--troubleshooting)
- [Keyword to Doc Mapping](#keyword-to-doc-mapping)

## Core Concepts

| Doc File | Topics Covered |
|----------|----------------|
| overview.md | What is Claude Code, key features, capabilities |
| quickstart.md | Installation, first run, basic usage |
| setup.md | Environment setup, API keys, configuration |
| interactive-mode.md | Interactive CLI usage, conversation flow |

## Extending Claude Code

| Doc File | Topics Covered |
|----------|----------------|
| hooks.md | Hook types (PreToolUse, PostToolUse, etc.), hook format, examples |
| hooks-guide.md | Step-by-step hook creation, common patterns, debugging |
| plugins.md | Plugin system, creating plugins, plugin structure |
| plugins-reference.md | Plugin manifest format, all plugin options |
| plugin-marketplaces.md | Installing from marketplaces, publishing plugins |
| skills.md | Agent Skills, SKILL.md format, allowed-tools |
| slash-commands.md | Custom slash commands, command files |
| sub-agents.md | Subagents, Task tool, agent types |
| mcp.md | MCP servers, configuration, available servers |

## Configuration

| Doc File | Topics Covered |
|----------|----------------|
| settings.md | All settings, settings.json, scopes (user/project) |
| cli-reference.md | CLI flags, environment variables, commands |
| memory.md | CLAUDE.md files, context injection, memory hierarchy |
| model-config.md | Model selection, opus/sonnet/haiku, model flags |
| iam.md | Permissions, tool access, allowlists, enterprise policies |
| terminal-config.md | Terminal integration, shell configuration |
| network-config.md | Proxy settings, network configuration |
| output-styles.md | Output formatting, verbose mode, streaming |
| statusline.md | Status bar configuration |

## Security

| Doc File | Topics Covered |
|----------|----------------|
| security.md | Security model, best practices, threat model |
| sandboxing.md | Bash sandboxing, filesystem isolation |
| data-usage.md | Data handling, privacy, what data is sent |
| legal-and-compliance.md | Compliance, legal considerations |

## IDE Integrations

| Doc File | Topics Covered |
|----------|----------------|
| vs-code.md | VS Code extension, keybindings, features |
| jetbrains.md | JetBrains plugin, IntelliJ, WebStorm |
| desktop.md | Desktop app, native features |

## CI/CD & Automation

| Doc File | Topics Covered |
|----------|----------------|
| headless.md | Non-interactive mode, automation, scripting |
| github-actions.md | GitHub Actions integration, workflows |
| gitlab-ci-cd.md | GitLab CI/CD integration |
| sdk.md | Claude Code SDK, programmatic usage |

## Cloud Providers

| Doc File | Topics Covered |
|----------|----------------|
| amazon-bedrock.md | AWS Bedrock setup, IAM, regions |
| google-vertex-ai.md | Google Cloud Vertex AI setup |
| microsoft-foundry.md | Azure AI Foundry setup |
| llm-gateway.md | LLM gateway configuration, proxies |

## Advanced Features

| Doc File | Topics Covered |
|----------|----------------|
| checkpointing.md | Conversation checkpoints, state management |
| analytics.md | Usage analytics, telemetry |
| monitoring-usage.md | Usage monitoring, cost tracking |
| devcontainer.md | Dev containers, remote development |
| third-party-integrations.md | External tool integrations |
| claude-code-on-the-web.md | Web-based Claude Code |

## Help & Troubleshooting

| Doc File | Topics Covered |
|----------|----------------|
| troubleshooting.md | Common issues, debugging, error messages |
| common-workflows.md | Best practices, workflow examples |
| costs.md | Pricing, token usage, cost optimization |

## Keyword to Doc Mapping

Use these keywords to find the right doc:

- **"hook", "PreToolUse", "PostToolUse"** → hooks.md, hooks-guide.md
- **"plugin", "marketplace"** → plugins.md, plugin-marketplaces.md
- **"skill", "SKILL.md"** → skills.md
- **"slash command", "/command"** → slash-commands.md
- **"MCP", "server", "tool"** → mcp.md
- **"agent", "subagent", "Task tool"** → sub-agents.md
- **"setting", "config", "settings.json"** → settings.md
- **"permission", "allow", "deny"** → iam.md
- **"sandbox", "isolation"** → sandboxing.md
- **"memory", "CLAUDE.md", "context"** → memory.md
- **"model", "opus", "sonnet", "haiku"** → model-config.md
- **"cost", "price", "token"** → costs.md
- **"VS Code", "extension"** → vs-code.md
- **"JetBrains", "IntelliJ"** → jetbrains.md
- **"GitHub Actions", "CI"** → github-actions.md
- **"GitLab", "CI/CD"** → gitlab-ci-cd.md
- **"headless", "non-interactive", "automation"** → headless.md
- **"Bedrock", "AWS"** → amazon-bedrock.md
- **"Vertex", "Google Cloud"** → google-vertex-ai.md
- **"Azure", "Foundry"** → microsoft-foundry.md
- **"error", "not working", "fix"** → troubleshooting.md
