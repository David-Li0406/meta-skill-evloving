---
name: cat:decompose-task
description: Use this skill when you need to split an oversized task into smaller, manageable subtasks with proper dependency management.
---

# Decompose Task

## Purpose

Break down a task that is too large for a single context window into smaller, manageable subtasks. This is essential for proactive context management, allowing work to continue efficiently when a task exceeds safe context bounds.

## When to Use

- Token report shows task approaching 40% threshold (80K tokens)
- Subagent has experienced compaction events
- PLAN.md analysis reveals task is larger than expected
- Partial collection indicates significant remaining work
- Pre-emptive decomposition during planning phase

## Workflow

### 1. Analyze Current Task Scope

```bash
TASK_DIR=".claude/cat/v${MAJOR}/v${MAJOR}.${MINOR}/${TASK_NAME}"

# Read current PLAN.md
cat "${TASK_DIR}/PLAN.md"

# Read STATE.md for progress
cat "${TASK_DIR}/STATE.md"

# If subagent exists, check its progress
if [ -d ".worktrees/${TASK}-sub-${UUID}" ]; then
  # Review commits made
  cd ".worktrees/${TASK}-sub-${UUID}"
  git log --oneline origin/HEAD..HEAD
fi
```

### 2. Identify Logical Split Points

Analyze PLAN.md for natural boundaries:

**Good split points:**
- Between independent features
- Between layers (model, service, controller)
- Between read and write operations
- Between setup and implementation
- Between implementation and testing

**Poor split points:**
- Middle of a refactoring
- Between tightly coupled components
- In the middle of a transaction boundary

### 3. Create New Task Directories

```bash
# Original task: 1.2/implement-parser
# New tasks: parser-lexer, parser-ast, parser-semantic (within same minor)

# Create directories for new tasks
mkdir -p ".claude/cat/v1/v1.2/parser-lexer"
mkdir -p ".claude/cat/v1/v1.2/parser-ast"
mkdir -p ".claude/cat/v1/v1.2/parser-semantic"
```

### 4. Create PLAN.md for Each New Task

Each new task gets its own focused PLAN.md:

```yaml
# 1.2a-parser-lexer/PLAN.md
---
task: 1.2a-parser-lexer
parent: 1.2-implement-parser
sequence: 1 of 3
---

# Implement Parser Lexer

## Objective
Implement the lexical analysis phase of the parser.

## Scope
- Token definitions
- Lexer implementation
- Lexer unit tests

## Dependencies
- None (first in sequence)

## Deliverables
- src/parser/Token.java
- src/parser/Lexer.java
- test/parser/LexerTest.java
```

### 5. Define Dependencies Between New Tasks

```yaml
# Dependency graph
dependencies:
  1.2a-parser-lexer: []  # No dependencies
  1.2b-parser-ast: [1.2a-parser-lexer]  # Depends on lexer
  1.2c-parser-semantic: [1.2b-parser-ast]  # Depends on AST
```