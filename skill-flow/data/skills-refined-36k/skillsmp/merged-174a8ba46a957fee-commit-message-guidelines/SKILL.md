---
name: commit-message-guidelines
description: Use this skill when creating commits or writing PR descriptions to ensure clarity and consistency in commit messages.
---

# Commit Message Guidelines

## Purpose
Provide guidance for writing clear, descriptive commit messages that explain WHAT the code does and WHY.

## Core Principles

### 1. Describe WHAT the Code Does, Not the Process
- **WRONG**: Squashed commits, Combined multiple commits, Merged feature branch
- **CORRECT**: Add user authentication with JWT tokens, Fix memory leak in connection pool, Refactor parser to use visitor pattern

### 2. Use Imperative Mood (Command Form)
- **WRONG**: Added authentication, Authentication was added
- **CORRECT**: Add user authentication, Fix authentication timeout bug

### 3. Subject Line Formula
```
<Verb> <what> [<where/context>]
```
**Examples**:
- Add rate limiting to API endpoints
- Fix memory leak in connection pool
- Refactor parser to use visitor pattern

**Rules**:
- Max 72 characters (50 ideal)
- Imperative mood (Add, Fix, Update, Remove, Refactor)
- No period at end
- Capitalize first word

### 4. Describe Changes Conceptually
The commit diff already shows which files were changed. Describe WHAT changed conceptually, not WHERE.
- **WRONG**: Update Parser.java and Lexer.java for comment handling
- **CORRECT**: Fix comment handling in member declarations

## Structure for Complex Changes
```
Subject line: Brief summary (50-72 chars, imperative mood)

Body paragraph: Explain the overall change and why it's needed.

Changes:
- First major change
- Second major change
- Third major change

Task ID: v{major}.{minor}-{task-name}
```

## Commit Types (MANDATORY)
When working in a CAT-managed project, use ONLY these types:
| Type       | When to Use                                      | Example                               |
|------------|--------------------------------------------------|---------------------------------------|
| `feature`  | New functionality, endpoint, component           | `feature: add user registration`      |
| `bugfix`   | Bug fix, error correction                         | `bugfix: correct email validation`    |
| `test`     | Test-only changes                                 | `test: add failing test for hashing`  |
| `refactor` | Code cleanup, no behavior change                  | `refactor: extract validation helper`  |
| `performance` | Performance improvement                        | `performance: add database index`     |
| `docs`     | User-facing docs (README, API docs)              | `docs: add API documentation`         |
| `style`    | Formatting, linting fixes                          | `style: format auth module`           |
| `config`   | Config, tooling, deps, Claude-facing docs        | `config: add bcrypt dependency`       |
| `planning` | Planning system updates                           | `planning: add task 5 summary`       |

**Format**: `{type}: {description}`

### Commit Type Separation (MANDATORY)
Keep one commit type per commit. Each commit should have ONE type.
- **WRONG**: bugfix: fix parser bug and update documentation
- **CORRECT**: 
  - bugfix: fix parser bug for comments in member declarations
  - config: correct method names in requirements-api.md

## Good Verbs for Description
| Verb      | Use For                                   |
|-----------|-------------------------------------------|
| **add**   | New feature, file, function               |
| **fix**   | Bug fix or correction                     |
| **update**| Modify existing feature (non-breaking)    |
| **remove**| Delete feature, file, or code             |
| **refactor**| Restructure without changing behavior   |
| **improve**| Enhance existing feature                  |

## Anti-Patterns to Avoid
- Meaningless: WIP, Fix stuff, Updates
- Overly Generic: Update code, Fix bugs, Refactor
- Just the Process: Squashed commits, Merged feature branch
- Too Technical: Change variable name from x to userCount
- Listing Modified Files: Update Parser.java, Lexer.java, and TokenType.java

## Checklist Before Committing
- [ ] Subject line is imperative mood ("Add", not "Added")
- [ ] Subject line is specific (not "Update files")
- [ ] Subject line is under 72 characters
- [ ] Body explains WHAT and WHY, not HOW
- [ ] No file names listed (the diff already shows which files changed)
- [ ] For squashed commits: synthesized meaningful summary
- [ ] Message would make sense in git history 6 months from now

## Quick Test
Ask yourself: "If I read this in git log in 6 months, would I understand what this commit does and why?" If no, revise the message.