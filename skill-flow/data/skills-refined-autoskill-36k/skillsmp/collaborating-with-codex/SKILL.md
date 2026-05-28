---
name: collaborating-with-codex
description: This skill should be used when working on architectural decisions, complex refactoring, system design, API redesign, or multi-component implementations. Also use when asked to "consult codex", "get a second opinion", "validate this plan", or "have codex review". Guides proactive collaboration with OpenAI Codex for brainstorming, plan validation, and code review.
---

# Codex Collaboration Guidelines

Use OpenAI Codex as a collaborative sub-agent for brainstorming, plan validation, and code review. Treat output as a second opinion—critically evaluate, don't blindly accept.

## Tools

- `codex` — Start new session (defaults to read-only sandbox)
- `codex-reply` — Continue session with prior context
- `codex-review` — Dedicated review mode with four presets:
  - `uncommitted` — Review staged/unstaged/untracked changes
  - `base` — PR-style review against a base branch
  - `commit` — Review a single commit
  - `custom` — Custom review with your own instructions

## When to Use

- Complex decisions where a second perspective adds value
- Architectural validation before implementation
- Plan validation before presenting to user
- Code review after significant changes

## When NOT to Use

- Simple, straightforward tasks
- Time-sensitive operations where latency matters
- Trivial changes that don't warrant discussion

## Guidelines

- **Form your own analysis first** to ensure independent perspectives—avoid anchoring bias
- Prompt specifically with context (like any sub-agent)
- Sessions run in read-only sandbox mode
- Use `codex-reply` for multi-turn discussions or reviews needing prior context
- Synthesize conclusions—don't just relay raw Codex output
- When developing plans (yourself or via Plan sub-agent), validate with Codex before presenting to user
