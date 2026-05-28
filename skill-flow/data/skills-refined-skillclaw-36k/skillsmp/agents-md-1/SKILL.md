---
name: agents-md
description: Guide for creating and editing CLAUDE.md or AGENTS.md files - AI agent instruction documents. Use when the user wants to create a new CLAUDE.md/AGENTS.md, edit existing agent documentation, set up AI instructions for a repository, or asks about best practices for agent docs structure.
---

# Agents MD

## Overview

This skill provides knowledge and templates for creating and editing CLAUDE.md and AGENTS.md files - structured documentation that guides AI coding agents working with a codebase.

## Output Format Selection

Let the user choose the output format:

| Format | Use Case |
|--------|----------|
| **CLAUDE.md** | Claude Code specific (supports `@` imports, hierarchical memory) |
| **AGENTS.md** | Cross-tool compatible (Codex, Cursor, Copilot, etc.) |

For format-specific features, see:
- `references/claude-md-features.md` - Claude Code specific features
- `references/agents-md-spec.md` - AGENTS.md specification

## Document Structure

Use this 8-section structure. See `assets/template.md` for the full template.

### 1. Project Name & Overview
Start with `# [Project Name]` followed by a brief description (1-3 sentences) explaining WHY this project exists, then list key features/capabilities as bullet points. No separate section heading needed.

### 2. Architecture Overview
Key architectural points as bullet list - important components, data flow, design decisions. Answer "WHAT are the key things to know?" Keep it concise (3-5 bullets). If `docs/ARCHITECTURE.md` or similar exists, link to it for details.

### 3. Directory Structure
Tree view of the repository layout with brief descriptions. Answer "WHERE is everything?"

### 4. Core Principles
Coding principles to follow. **Use these defaults as-is; append project-specific items rather than replacing:**

```markdown
## Core Principles
- Prefer existing patterns and terminology over general best practices
- Avoid adding new dependencies unless necessary; remove when possible
- Follow Conventional Commits for commit messages
```

### 5. Commands
Build, run, lint, and test commands. Example:

```markdown
## Commands
- `npm install` - Install dependencies
- `npm run dev` - Start development server
- `npm run build` - Production build
- `npm test` - Run all tests
- `npm run lint` - Run linter
```

### 6. Testing
Testing strategy and policies (not commands). **Use these defaults as-is; append project-specific items rather than replacing:**

```markdown
## Testing
- Prefer integration tests over unit tests
- Use in-source testing for unit tests covering edge cases
- Avoid mocks; use them only for external communication or resource fetching
```

### 7. Language Policy
Programming and natural language rules. **Use these defaults as-is; append project-specific items rather than replacing:**

```markdown
## Language Policy
- Follow the user's language for comments, commits, and tests
- Write the following files in English:
  - CLAUDE.md, AGENTS.md
  - Files under `.claude/`
  - Files under `.github/` (except comments)
```

### 8. Additional Resources
References to detailed documentation. Format:

```markdown
## Additional Resources
- `docs/ARCHITECTURE.md`: Detailed architecture decisions
- `docs/agents/[FILE].md`: [Description]
- `docs/adr/adr-001-[slug].md`: [ADR title]
```

## Best Practices

For detailed guidelines on writing effective agent documentation, see `references/best-practices.md`.

Key points:
- Keep under 300 lines (ideally under 100)
- Be specific, not generic
- Use Progressive Disclosure - link to detailed docs instead of including everything
- Let linters handle code style, not agent docs
