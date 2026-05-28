---
name: git-commit
description: Create git commits with conventional commit messages
---

## Commit Messages

When creating git commit messages, follow these guidelines:

Write a git commit message in the Conventional Commits 1.0.0 format.
Use exactly this structure:
<type>[optional scope]: <description> on the first line, then an optional body, then optional footer lines.

Rules to follow:

    <type> must be one of: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert.

    The description must be a short, imperative summary of the change (max ~70 characters).

    If the change is breaking, either:

        append ! right after the type or optional scope (e.g. feat!: ... or feat(api)!: ...), or

        add a footer line starting with BREAKING CHANGE: followed by the explanation.

    The body (if present) must start after one blank line and can give more detail in full sentences or bullet points.

    Footers (if present) must start after a blank line following the body and can include items like BREAKING CHANGE: ... or issue references such as Refs: #123.

    Do not include any text outside the commit message itself (no commentary, no code fences, no prefixes like "Here is your commit message").

Make sure to include your commit messages body as well for readers help understand why these changes were made, or what these changes bring.

Here is the exact process to follow:

### Process

1. **Think about what changed:**
    - Review the conversation history and understand what was accomplished
    - Run `git status` to see current changes
    - Run `git diff` to understand the modifications
    - Consider whether changes should be one commit or multiple logical commits

2. **Plan your commit(s):**
    - Identify which files belong together
    - Draft clear, descriptive commit messages
    - Use imperative mood in commit messages
    - Focus on why the changes were made, not just what

3. **Execute:**
    - Use `git add` with specific files (never use `-A` or `.`)
    - Create commits with your planned messages
    - Show the result with `git log --oneline -n [number]`

### Important

- **NEVER add co-author information**
- Commits should be authored solely by the user
- Do not include any "Generated with ..." messages
- Do not add "Co-Authored-By" lines
- Write commit messages as if the user wrote them
- Always ask for confirmation before committing
- Always show the diff to the user before committing or amending commits

### Remember

- You have the full context of what was done in this session
- Group related changes together
- Keep commits focused and atomic when possible
- The user trusts your judgment - they asked you to commit
