# Slash Command Examples

Copy-paste ready examples for common slash command patterns.

## Example 1: Simple Prompt Command

The simplest form - just a prompt in a file.

```markdown
# .claude/commands/explain.md

Explain this code in simple terms:
- What does it do?
- How does it work?
- What are the key concepts?

Use analogies and avoid jargon.
```

**Usage:** `/explain`

**When to use:** Quick prompts you repeat often.

---

## Example 2: Command with All Arguments

Capture all user input with `$ARGUMENTS`.

```markdown
# .claude/commands/ask.md
---
argument-hint: <your question>
description: Ask a quick question about the codebase
---

Answer this question about the codebase: $ARGUMENTS

Be concise and direct. Reference specific files when relevant.
```

**Usage:** `/ask how does authentication work?`

**When to use:** Open-ended commands where user provides free-form input.

---

## Example 3: Positional Arguments

Access individual arguments with `$1`, `$2`, etc.

```markdown
# .claude/commands/create-component.md
---
argument-hint: [component-name] [type: page|layout|widget]
description: Create a new React component
---

Create a new React component:
- Name: $1
- Type: $2 (default: widget)

Follow our component conventions:
- Use TypeScript
- Include props interface
- Add JSDoc comments
- Create test file
```

**Usage:** `/create-component UserProfile page`

**When to use:** Structured commands with specific parameter roles.

---

## Example 4: Bash Execution with Git

Execute bash commands and use output as context.

```markdown
# .claude/commands/commit.md
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
argument-hint: [optional message]
description: Create a git commit with auto-generated message
---

## Current State

- Git status: !`git status --short`
- Staged diff: !`git diff --cached --stat`
- Recent commits: !`git log --oneline -5`
- Current branch: !`git branch --show-current`

## Task

Create a git commit for the staged changes.

If message provided: $ARGUMENTS
Otherwise: Generate message from changes.

Follow conventional commit format:
- feat: new feature
- fix: bug fix
- docs: documentation
- refactor: code refactoring
- test: tests
- chore: maintenance
```

**Usage:** `/commit` or `/commit feat: add user authentication`

**When to use:** Commands that need current system state.

---

## Example 5: File References

Include file contents with `@` prefix.

```markdown
# .claude/commands/migrate.md
---
argument-hint: <source-file>
description: Migrate a file to new patterns
allowed-tools: Read, Edit, Write
---

Migrate the following file to our new patterns:

@$1

Reference our migration guide:
@docs/migration-guide.md

Apply these transformations:
1. Update imports to new paths
2. Convert to TypeScript if JavaScript
3. Add proper typing
4. Update to new API patterns
```

**Usage:** `/migrate src/legacy/UserService.js`

**When to use:** Commands that operate on specific files.

---

## Example 6: Namespaced Commands (Subdirectory)

Organize related commands in subdirectories.

```markdown
# .claude/commands/db/migrate.md
---
allowed-tools: Bash(bun:*), Read, Write
description: Create database migration
---

## Current Schema

!`cat drizzle/schema.ts`

## Recent Migrations

!`ls -la drizzle/migrations/ | tail -5`

## Task

Create a new database migration for: $ARGUMENTS

Follow our migration conventions:
- Use Drizzle ORM
- Add both up and down migrations
- Include data migration if needed
```

```markdown
# .claude/commands/db/seed.md
---
allowed-tools: Bash(bun:*)
description: Seed database with test data
---

Seed the database with test data:
!`bun run db:seed`

Report what was seeded.
```

**Usage:** `/migrate add user avatar field` (shows as project:db)

**When to use:** Group related commands by domain.

---

## Example 7: Model Override

Force a specific model for the command.

```markdown
# .claude/commands/quick.md
---
model: claude-3-5-haiku-20241022
argument-hint: <question>
description: Quick answer using fast model
---

Answer quickly and concisely: $ARGUMENTS

- Be direct
- No code changes
- Maximum 2-3 sentences
```

```markdown
# .claude/commands/deep-think.md
---
model: claude-sonnet-4-20250514
argument-hint: <complex problem>
description: Deep analysis with extended thinking
---

Think deeply about this problem: $ARGUMENTS

Take your time. Consider:
- Multiple approaches
- Trade-offs
- Edge cases
- Long-term implications

Show your reasoning process.
```

**Usage:** `/quick what's the difference between map and flatMap?`

**When to use:** Optimize cost/speed or force deeper reasoning.

---

## Example 8: Tool Restrictions

Limit what tools the command can use.

```markdown
# .claude/commands/audit.md
---
allowed-tools: Read, Glob, Grep
description: Security audit (read-only)
---

Perform a security audit of the codebase.

Look for:
- Hardcoded secrets
- SQL injection vulnerabilities
- XSS vulnerabilities
- Insecure dependencies
- Missing input validation

DO NOT modify any files. Report findings only.
```

```markdown
# .claude/commands/dangerous-cleanup.md
---
allowed-tools: Bash(rm:*), Bash(find:*)
disable-model-invocation: true
description: Clean up temporary files (manual only)
---

Remove temporary and generated files:
- Build artifacts
- Cache directories
- Log files

Ask for confirmation before each deletion.
```

**Usage:** `/audit`

**When to use:** Enforce safety constraints or prevent accidental changes.

---

## Example 9: Multi-File Reference

Reference multiple files for comparison or context.

```markdown
# .claude/commands/compare-impl.md
---
argument-hint: <file1> <file2>
description: Compare two implementations
---

Compare these implementations:

## File 1
@$1

## File 2
@$2

Analyze:
- Approach differences
- Performance implications
- API compatibility
- Missing features in either
```

**Usage:** `/compare-impl src/auth/v1.ts src/auth/v2.ts`

---

## Example 10: Complex Workflow Command

Combine multiple features for complex workflows.

```markdown
# .claude/commands/release.md
---
allowed-tools: Bash(git:*), Bash(bun:*), Bash(npm:*), Read, Write, Edit
argument-hint: [major|minor|patch]
description: Prepare a new release
---

## Current State

- Current version: !`cat package.json | grep '"version"'`
- Git status: !`git status --short`
- Current branch: !`git branch --show-current`
- Unpushed commits: !`git log origin/main..HEAD --oneline`

## Changelog

@CHANGELOG.md

## Task

Prepare a $1 release (default: patch):

1. Ensure working directory is clean
2. Run tests: `bun test`
3. Update version in package.json
4. Update CHANGELOG.md with new version header
5. Create git commit: "chore: release vX.X.X"
6. Create git tag: "vX.X.X"

Do NOT push. Report what was done.
```

**Usage:** `/release minor`

---

## Example 11: Personal User Command

Commands in `~/.claude/commands/` work across all projects.

```markdown
# ~/.claude/commands/standup.md
---
description: Generate daily standup notes
---

Generate my daily standup notes.

Yesterday I worked on: !`git log --author="$(git config user.name)" --since="yesterday" --oneline`

Today I'll focus on: (analyze current branch and uncommitted work)

Blockers: (identify any failing tests or TODO comments)

Format as bullet points.
```

**Usage:** `/standup` (available in any project)

---

## Example 12: Disable Model Invocation

Prevent Claude from auto-triggering sensitive commands.

```markdown
# .claude/commands/deploy-prod.md
---
allowed-tools: Bash(*)
disable-model-invocation: true
argument-hint: [environment]
description: Deploy to production (manual only)
---

Deploy to: $1 (default: production)

This command is disabled for automatic invocation.
Only run when explicitly requested by user.

Steps:
1. Run tests
2. Build production bundle
3. Deploy via CI/CD
4. Verify deployment
5. Report status
```

**Usage:** `/deploy-prod` (Claude cannot trigger this via SlashCommand tool)

---

## Anti-Patterns

### Too Vague

```markdown
# Bad: No clear purpose
---
description: Do stuff
---

Help with the code.
```

**Fix:** Be specific about what the command does.

### Dangerous Without Guards

```markdown
# Bad: Unrestricted bash access
---
allowed-tools: Bash(*)
---

Run this command: $ARGUMENTS
```

**Fix:** Use specific bash patterns like `Bash(git:*)`.

### Missing Description

```markdown
# Bad: No frontmatter, can't be used by SlashCommand tool

Do a code review.
```

**Fix:** Always include description in frontmatter for discoverability.
