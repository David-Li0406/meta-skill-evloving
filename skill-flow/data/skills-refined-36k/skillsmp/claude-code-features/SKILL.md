---
description: Guide for distinguishing Claude Code features (Commands, Skills, Agents, Hooks, Rules) and selection criteria. Use when decomposing context files, deciding where to add new features, or customizing Claude Code.
---

# Claude Code Features Guide

Guide for choosing between 5 major Claude Code features.

## Feature Overview

| Feature | Trigger | Essence | Best For |
|---------|---------|---------|----------|
| **Commands** | Manual (`/command`) | Inject saved prompts instantly | Repeatable **standard workflows** by user execute |
| **Skills** | Auto (Claude decides) | Knowledge loaded on demand | **On-demand knowledge** (tool usage, guidelines) |
| **Agents** | Manual/delegation | Specialists with independent context | **Bulk data processing** & parallel tasks |
| **Hooks** | Event-driven | Shell scripts auto-executed around tools | **Deterministic automation** |
| **Rules** | Conditional/always | Modularized rules | **Path-conditional constraints** |

## Decision Flowchart

```
1. "Should it auto-execute on events like file edits?"
   → Yes: Hooks (implement as shell commands)

2. "Needs independent context for bulk data processing?"
   → Yes: Agents (don't pollute main conversation)

3. "Knowledge not always needed, but should surface when relevant?"
   → Yes: Skills (tool usage guides, domain expertise, patterns)

4. "Standard procedure user explicitly executes?"
   → Yes: Commands (instant /command execution)

5. "Constraints for specific paths or entire project?"
   → Yes: Rules (conditional with paths:)

6. Cannot classify
   → Keep in CLAUDE.md
```

## Feature Details

- @${CLAUDE_PLUGIN_ROOT}/skills/claude-code-features/commands.md
- @${CLAUDE_PLUGIN_ROOT}/skills/claude-code-features/skills.md
- @${CLAUDE_PLUGIN_ROOT}/skills/claude-code-features/agents.md
- @${CLAUDE_PLUGIN_ROOT}/skills/claude-code-features/hooks.md
- @${CLAUDE_PLUGIN_ROOT}/skills/claude-code-features/rules.md

## References

@${CLAUDE_PLUGIN_ROOT}/skills/claude-code-features/references.md
