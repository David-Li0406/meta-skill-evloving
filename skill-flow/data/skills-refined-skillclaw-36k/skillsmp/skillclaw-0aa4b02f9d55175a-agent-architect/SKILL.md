---
name: agent-architect
description: Use this skill when you need to create and refine OpenCode agents through a guided Q&A process, ensuring they meet specific requirements and configurations.
---

# Skill body

## Overview
Create and refine OpenCode agents via guided Q&A. Use proactively for agent creation, performance improvement, or configuration design.

## Examples
- **User:** "Create an agent for code reviews"  
  **Action:** Ask about scope, permissions, tools, model preferences, and generate AGENTS.md frontmatter.
  
- **User:** "My agent ignores context"  
  **Action:** Analyze description clarity, allowed-tools, permissions, and suggest improvements.
  
- **User:** "Add a database expert agent"  
  **Action:** Gather requirements, set `convex-database-expert` in `subagent_type`, and configure permissions.
  
- **User:** "Make my agent faster"  
  **Action:** Suggest smaller models, reduce allowed-tools, and tighten permissions.

## Core Approach
- **Conversational Process:** Agent creation is conversational, not transactional. 
  - MUST NOT assume what the user wants—ask.
  - SHOULD start with broad questions, drilling into details only if needed.
  - Users MAY skip configuration they don't care about.
  - MUST always show drafts and iterate based on feedback.

The goal is to help users create agents that fit their needs, not to overwhelm them with every possible configuration option.

## Question Tool
- **Batching:** Use the `question` tool for 2+ related questions. Single questions → plain text.
- **Syntax:** `header` ≤12 chars, `label` 1-5 words, add "(Recommended)" to default.

### Critical Permission Logic
- You MUST ask the user about permissions explicitly.
- By default, agents are ALLOWED all tools and permissions. You MUST NOT add `bash`, `read`, `write`, or `edit` to the config unless the user explicitly wants to RESTRICT them.
- If the user wants standard "full access", do NOT add a permission block for tools. Rely on system defaults.
- **EXCEPTION:** Skills MUST ALWAYS be configured with `"*": "deny"` and explicit allows to prevent accidental skill loading.

## Agent Locations
| Scope | Path |
|-------|------|
| Project | `.opencode/agent/<name>.md` |
| Global | `~/.config/opencode/agent/<name>.md` |

## Agent File Format
```yaml
---
description: When to use this agent. Include trigger examples.
model: anthropic/claude-sonnet-4-20250514  # Optional
mode: primary | subagent | all           # Optional (defaults to standard)
permission:
  skill: { "*": "deny", "my-skill": "allow" }
  bash: { "*": "ask" }            # Only if restricting permissions
---
System prompt in markdown body (second person).
```