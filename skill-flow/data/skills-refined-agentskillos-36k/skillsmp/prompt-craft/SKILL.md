---
name: prompt-craft
description: |
  Craft effective worker prompts from backlog issues using Claude 4 best practices.
  Use when preparing issues for workers, writing prompts, or optimizing prompt quality.
  Trigger with "craft prompt", "write prompt", "prepare issue", "make ready".
model: haiku
allowed-tools: Read, Grep, Glob, Bash
---

# Prompt Craft - Claude 4 Best Practices

Craft effective prompts for Claude workers using proven patterns.

## Core Principles

### 1. Be Explicit

Claude 4.x follows instructions precisely. Use action verbs.

| Less Effective | More Effective |
|----------------|----------------|
| "Can you suggest improvements?" | "Update the function to improve performance." |
| "Look at this code" | "Find and fix the null check bug" |
| "Help with testing" | "Write unit tests for the auth module" |

### 2. Add Context/Motivation

Explain WHY, not just WHAT. Claude generalizes from explanations.

| Less Effective | More Effective |
|----------------|----------------|
| "NEVER use ellipses" | "Never use ellipses since the TTS engine won't pronounce them correctly." |
| "Always add error handling" | "Add error handling so users see helpful messages instead of stack traces." |

### 3. Natural Skill Triggers

Use natural language, avoid aggressive markers.

| Avoid | Use |
|-------|-----|
| "CRITICAL: You MUST use this tool when..." | "Use the X skill for Y." |
| "ALWAYS: This is REQUIRED" | "Use this approach when..." |
| "IMPORTANT!!!: Never forget to..." | "Remember to..." |

### 4. Positive Framing

Tell Claude what TO do, not just what to avoid.

| Less Effective | More Effective |
|----------------|----------------|
| "Don't write long functions" | "Keep functions under 20 lines" |
| "Avoid complex logic" | "Use simple, readable patterns" |

## Prompt Structure

```markdown
## Context
[1-2 sentences: Why this work matters, what problem it solves]

## Task
[Clear, explicit action instruction using action verbs]

## Approach
[Optional: Skill hints, patterns to follow, key considerations]
Use the [skill] skill for [specific purpose].

## Key Files
[3-5 most relevant files to start with]
- path/to/main/file.ts
- path/to/related/file.ts

## When Done
[How to complete: close issue, what to include in summary]
Close issue: bd close ISSUE-ID --reason "summary"
```

## Skill Matching

Match skills based on content:

| Content Signal | Suggested Skill |
|----------------|-----------------|
| `.tsx`, `.jsx`, React | frontend-development |
| terminal, xterm, resize | xterm-js |
| auth, login, session | better-auth |
| database, SQL, query | databases |
| API, REST, endpoint | backend-development |
| CSS, styling, theme | ui-styling |
| docs, markdown | docs-seeker |

## Subagent Hints

Claude 4.5 naturally delegates. Add hints when beneficial:

```markdown
Use subagents in parallel to scaffold Dashboard, Settings, and Profile pages.
```

```markdown
Use an Explore agent to find the relevant authentication files first.
```

## Parallelization Hints

For tasks with independent subtasks:

```markdown
These components can be developed in parallel:
- HeaderComponent
- FooterComponent
- SidebarComponent
```

## Complexity Guidelines

| Prompt Length | When to Use |
|---------------|-------------|
| Short (3-5 lines) | Simple bug fixes, single-file changes |
| Medium (10-15 lines) | Feature work, multi-file changes |
| Long (20+ lines) | Complex features, architectural changes |

**Rule**: If you need more than 20 lines, the issue might need breaking down.

## Anti-Patterns

Avoid these common mistakes:

1. **Overloading**: Too many skills, too many files, too much context
2. **Vague tasks**: "Make it better" without specific criteria
3. **All caps**: CRITICAL, IMPORTANT, MUST - creates anxiety, not clarity
4. **Negative framing**: Lists of don'ts without corresponding dos
5. **No completion criteria**: Worker doesn't know when they're done

## References

- [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
