---
name: interactive-workspace-discovery
description: Use this skill when you want to explore the tools, workflows, agents, and hooks available in your workspace.
---

# Skill body

## /help - Workspace Discovery

Guide users through the capabilities of this workspace setup.

## Usage

```
/help                    # Interactive guided discovery
/help workflows          # Workflow orchestration skills
/help agents             # Specialist agents catalog
/help tools              # CLI tools (tldr, prove, recall)
/help hooks              # Active hooks and what they do
/help advanced           # MCP, frontmatter, customization
/help <name>             # Deep dive on specific skill/agent
```

## Behavior Based on Arguments

### No Arguments: Interactive Discovery

Use AskUserQuestion to guide the user:

```
question: "What are you trying to do?"
header: "Goal"
options:
  - label: "Explore/understand a codebase"
    description: "Find patterns, architecture, conventions"
  - label: "Fix a bug"
    description: "Investigate, diagnose, implement fix"
  - label: "Build a feature"
    description: "Plan, implement, test new functionality"
  - label: "Prove something mathematically"
    description: "Formal verification with Lean 4"
```

Based on response, show relevant tools:

| Goal | Show |
|------|------|
| Explore codebase | scout agent, tldr CLI, /explore workflow |
| Fix a bug | /fix workflow, sleuth agent, debug-agent |
| Build feature | /build workflow, architect agent, kraken agent |
| Prove math | /prove skill, lean4 skill, Godel-Prover |
| Research docs | oracle agent, nia-docs, perplexity |
| Configure workspace | hooks, rules, settings, frontmatter |

### /help workflows

Display workflow meta-skills:

```markdown
## Workflow Skills

Orchestrate multi-agent pipelines for complex tasks.

| Workflow | Purpose | Agents Used |
|----------|---------|-------------|
| /fix | Bug investigation → diagnosis → implementation | sleuth → kraken → arbiter |
| /build | Feature planning → implementation → testing | architect → kraken → arbiter |
| /debug | Deep investigation of issues | debug-agent, sleuth |
| /tdd | Test-driven development cycle | arbiter → kraken → arbiter |
| /refactor | Code transformation with safety | phoenix → kraken → judge |
| /review | Code review and feedback | critic, judge |
| /security | Vulnerability analysis | aegis |
| /explore | Codebase discovery |
```