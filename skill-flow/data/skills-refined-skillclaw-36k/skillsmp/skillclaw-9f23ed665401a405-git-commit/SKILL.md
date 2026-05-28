---
name: git-commit
description: Use this skill when you need to write clear, descriptive commit messages that effectively communicate the changes made in your code.
---

# Git Commit Message Skill

**Purpose**: Provide guidance for writing clear, descriptive commit messages that explain WHAT the code does and WHY.

## Core Principles

### 1. Describe WHAT the Code Does, Not the Process

```
# WRONG - Describes the process
Squashed commits
Combined multiple commits
Merged feature branch

# CORRECT - Describes what the code does
Add user authentication with JWT tokens
Fix memory leak in connection pool
Refactor parser to use visitor pattern
```

### 2. Use Imperative Mood (Command Form)

```
# WRONG
Added authentication
Authentication was added

# CORRECT
Add user authentication
Fix authentication timeout bug
```

### 3. Subject Line Formula

```
<Verb> <what> [<where/context>]

Examples:
Add   rate limiting      to API endpoints
Fix   memory leak        in connection pool
Refactor  parser         to use visitor pattern
```

**Rules**:
- Max 72 characters (50 ideal)
- Imperative mood (Add, Fix, Update, Remove, Refactor)
- No period at end
- Capitalize first word

### 4. Describe Changes Conceptually

The commit diff already shows which files were changed. Describe WHAT changed conceptually, not WHERE.

```
# WRONG - Subject line lists files
Update Parser.java and Lexer.java for comment handling

# WRONG - Body has "Files updated" section
config: update display standards

Files updated:
- commands/status.md
- skills/collect-results/SKILL.md
- concepts/display-standards.md

# CORRECT - Describes what changed
Fix comment handling in member declarations

# CORRECT - Body describes changes, not files
config: update display standards

Standardize fork display format and checkpoint messaging.
```

## Structure for Complex Changes

```
Subject line: Brief summary (50-72 chars, imperative mood)

Body paragraph: Explain the overall change and why it's needed.

Changes:
- First major change
- Second major change
- Third major change
```

## Task ID Footer (MANDATORY for CAT tasks)

**Every commit for a CAT task MUST include the Task ID in the last line.** A task may span multiple commits (across sessions or addressing distinct aspects). Each commit MUST include the same Task ID:

```
feature: add yield statement parsing support

Add YIELD_STATEMENT node type and parseYieldStatement() method
for JDK 14+ switch expressions.

- Added YIELD_STATEMENT to NodeType enum
- Created parseYieldStatement(
```