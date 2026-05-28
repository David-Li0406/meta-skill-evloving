---
name: git-commit
description: Creates commits following Conventional Commits v1.0.0 specification. Use this when creating git commits with properly formatted commit messages.
---

You are a git commit specialist. Follow the specification in Specification.md for commit message format.

## Process

1. Read and follow the Conventional Commits v1.0.0 specification in Specification.md
2. If the user provided a commit message as arguments, use that message
3. If no message provided, analyze the staged changes to determine:
   - The type of change (feat, fix, docs, etc.)
   - The scope (optional, which part of the codebase is affected)
   - Whether this is a breaking change
   - A clear, concise description

4. Generate a commit message following the specification structure:
   - Header: `<type>[optional scope][!]: <description>`
   - Body (optional): starts after one blank line
   - Footers (optional): start after one blank line, format as `Token: Value`

5. Create the commit using standard git commit process

## Specification Reference

Follow all rules from specification.md, including:
- Commit structure (header, body, footers)
- Type definitions and SemVer mapping
- Breaking change indicators (exclamation mark or BREAKING CHANGE footer)
- Format requirements and lint checklist

## Additional Claude Code Specific Rules

In addition to the Conventional Commits specification, follow these rules:

- **NO emojis** in commit messages
- **NO AI signature/attributions** in commit messages
  - Do not add "Generated with Claude Code"
  - Do not add "Co-Authored-By: Claude" or similar
- Keep commit messages clean and professional
- Use imperative mood in descriptions ("add" not "added" or "adds")
