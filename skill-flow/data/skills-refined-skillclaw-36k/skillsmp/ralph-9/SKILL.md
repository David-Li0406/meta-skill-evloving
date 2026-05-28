---
name: ralph
description: Convert PRD documents to AG4ONE Ralph loop format and manage autonomous cycles
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
---

# AG4ONE Ralph Skill

## Overview

This skill converts PRD documents to AG4ONE Ralph loop format and manages autonomous development cycles.

## Usage

### Convert PRD to Ralph Format
```
Load ag4one Ralph skill and convert [prd-file].json to ralph format
```

### Start Ralph Loop
```
Load ag4one Ralph skill and start autonomous development
```

## What it does

1. **PRD Conversion** - Transforms markdown PRDs to Ralph-compatible JSON
2. **Loop Management** - Manages Ralph iteration cycles
3. **Progress Tracking** - Monitors development progress
4. **Quality Assurance** - Ensures all stories pass verification
5. **Archive Management** - Handles run history and archiving

## Ralph Loop Features

### Autonomous Execution
- **Fresh context** each iteration (new AI instance)
- **Single story focus** per iteration
- **Quality checks** before committing
- **Progress persistence** via git and logs

### Multi-Platform Support
- **Opencode CLI** (primary)
- **Claude Code** (secondary)
- **Gemini CLI** (basic support)

### Intelligent Management
- **Branch management** - Automatic creation and switching
- **Archive system** - Previous runs preserved
- **Progress logs** - Detailed tracking and learnings
- **Pattern consolidation** - Discovered patterns saved

## Loop Process

1. **Read PRD** - Get highest priority incomplete story
2. **Implement** - Build the feature following AG4ONE patterns
3. **Verify** - Run quality checks and testing
4. **Commit** - Save changes with structured messages
5. **Update PRD** - Mark story as completed
6. **Learn** - Record patterns and learnings
7. **Repeat** - Continue until all stories complete

## Quality Gates

- **Typecheck** - All code must typecheck
- **Linting** - Code style compliance
- **Tests** - Unit/integration tests pass
- **Browser Verification** - UI changes tested in browser
- **CI/CD** - Pipeline remains green

## Progress Tracking

### Progress Log Format
```
## [Date] - [Story ID]
Platform: opencode|claude|gemini
- Implementation details
- Files changed
- Learnings for future iterations
```

### Pattern Consolidation
Key learnings moved to `## Codebase Patterns` section for reuse across iterations.

## Completion

Ralph signals completion when:
- All stories marked `passes: true`
- Quality checks pass
- Ready for production review

Completes with: `<promise>COMPLETE</promise>`

---

**AG4ONE Ralph Skill** - Autonomous development loop management.