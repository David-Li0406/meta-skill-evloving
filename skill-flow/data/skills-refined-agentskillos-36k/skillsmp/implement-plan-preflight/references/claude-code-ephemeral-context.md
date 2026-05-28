# Claude Code Ephemeral Context

This document explains the ephemeral nature of Claude Code's Plan Mode artifacts and why the `/itp:go` workflow exists to capture decisions before they're lost.

## Plan File Location & Naming

Claude Code stores plan files in a global directory with randomly-generated names:

| Component     | Behavior                                                               | Source                                                                                                   |
| ------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Directory** | `~/.claude/plans/`                                                     | [GitHub Issue #12707](https://github.com/anthropics/claude-code/issues/12707)                            |
| **Filename**  | Random adjective-noun pattern (e.g., `abstract-fluttering-unicorn.md`) | [Reddit Discussion](https://www.reddit.com/r/ClaudeCode/comments/1p6vzg8/the_new_plan_mode_is_not_good/) |

> **Quote from Issue #12707**: "The new plan mode... can ONLY use plan files in ~/.claude/plans... Read ../../../.claude/plans/abstract-fluttering-unicorn.md"

### Why Random Names?

When asked why it chose `glittery_bouncing_feather.md`, Claude responded: "it just used a random name." This is not a bug—it's the default behavior. The names are not derived from your task description.

## The Overwrite Problem

Plan files are **overwritten** when:

- You enter Plan Mode for a new task
- A new planning session begins
- Context is compacted and Claude regenerates the plan

This means any decisions made during planning (via `AskUserQuestion` flows) are lost unless explicitly captured in version-controlled artifacts.

## AskUserQuestion Tool

The `AskUserQuestion` tool is the mechanism Claude uses to clarify requirements during planning. It's **not officially documented** but widely discussed:

| Aspect            | Details                                                                                                | Source                                                                        |
| ----------------- | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| **Tool Name**     | `AskUserQuestion`                                                                                      | [GitHub Issue #10346](https://github.com/anthropics/claude-code/issues/10346) |
| **Added in**      | Version 2.0.21                                                                                         | Changelog                                                                     |
| **Documentation** | Missing from official docs                                                                             | [Issue #10346](https://github.com/anthropics/claude-code/issues/10346)        |
| **Tutorial**      | [egghead.io](https://egghead.io/create-interactive-ai-tools-with-claude-codes-ask-user-question~b47wn) | Community                                                                     |

### Why This Matters for ADRs

Decisions made via `AskUserQuestion` flows include:

- Architectural choices (which library, which pattern)
- Trade-off resolutions (performance vs simplicity)
- Scope clarifications (what's in/out of scope)

These decisions **live only in the conversation context**. When context compacts at ~95% capacity, they're summarized away. The `/itp:go` workflow captures these decisions in ADRs before they're lost.

## References

- [GitHub Issue #12707](https://github.com/anthropics/claude-code/issues/12707) - Plan files outside ~/.claude/plans
- [GitHub Issue #10685](https://github.com/anthropics/claude-code/issues/10685) - Plan agent AskUserQuestion behavior
- [GitHub Issue #10346](https://github.com/anthropics/claude-code/issues/10346) - Missing AskUserQuestion documentation
- [Reddit Discussion](https://www.reddit.com/r/ClaudeCode/comments/1p6vzg8/the_new_plan_mode_is_not_good/) - Random naming behavior
- [egghead.io Tutorial](https://egghead.io/create-interactive-ai-tools-with-claude-codes-ask-user-question~b47wn) - AskUserQuestion guide
- [Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) - Official guidance
