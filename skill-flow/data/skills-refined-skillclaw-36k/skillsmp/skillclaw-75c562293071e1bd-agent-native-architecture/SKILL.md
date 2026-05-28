---
name: agent-native-architecture
description: Use this skill when building AI agents using prompt-native architecture, where features are defined in prompts rather than code. This approach is ideal for creating autonomous agents, designing MCP servers, implementing self-modifying systems, or adopting the "trust the agent's intelligence" philosophy.
---

# Skill body

## The Prompt-Native Philosophy

Agent native engineering inverts traditional software architecture. Instead of writing code that the agent executes, you define outcomes in prompts and let the agent figure out HOW to achieve them.

### The Foundational Principle

**Whatever the user can do, the agent can do. Many things the developer can do, the agent can do.**

Don't artificially limit the agent. If a user could read files, write code, browse the web, or deploy an app—the agent should be able to do those things too. The agent figures out HOW to achieve an outcome; it doesn't just call your pre-written functions.

### Features Are Prompts

Each feature is a prompt that defines an outcome and gives the agent the tools it needs. The agent then figures out how to accomplish it.

- **Traditional:** Feature = function in codebase that agent calls
- **Prompt-native:** Feature = prompt defining desired outcome + primitive tools

The agent doesn't execute your code. It uses primitives to achieve outcomes you describe.

### Tools Provide Capability, Not Behavior

Tools should be primitives that enable capability. The prompt defines what to do with that capability.

- **Wrong:** `generate_dashboard(data, layout, filters)` — agent executes your workflow
- **Right:** `read_file`, `write_file`, `list_files` — agent figures out how to build a dashboard

Pure primitives are better, but domain primitives (like `store_feedback`) are acceptable if they don't encode logic—just storage/retrieval.

### The Development Lifecycle

1. **Start in the prompt** - New features begin as natural language defining outcomes.
2. **Iterate rapidly** - Change behavior by editing prose, not refactoring code.
3. **Graduate when stable** - Harden to code when requirements stabilize AND speed/reliability matter.
4. **Many features stay as prompts** - Not everything needs to become code.

### Self-Modification (Advanced)

The advanced tier: agents that can evolve their own code, prompts, and behavior. Not required for every app, but a significant part of the future.

When implementing:
- Approval gates for code changes
- Auto-commit before modifications (rollback capability)
- Health checks after changes