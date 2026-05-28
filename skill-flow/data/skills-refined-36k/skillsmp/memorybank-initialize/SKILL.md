---
name: memorybank-initialize
description: Bootstrap a new project's Memory Bank by creating the six core files with templates and gathering initial project information from the user.
---

# Memory Bank: Initialize

Bootstrap a new project with complete Memory Bank structure.

**Helper Scripts Available:**
- `scripts/validate_memorybank.py` - Validates structure

## What It Does

Creates Memory Bank structure in `memory-bank/` directory:

```
project-root/
└── memory-bank/
    ├── projectbrief.md         # Foundation (goals, scope)
    ├── productContext.md       # User experience & vision
    ├── techContext.md          # Technologies & setup
    ├── systemPatterns.md       # Architecture & patterns
    ├── activeContext.md        # Current work focus
    └── progress.md             # Status & learnings
```

## Workflow

1. **Check if exists:** Validate memory-bank doesn't already exist
2. **Create directory:** Make `memory-bank/` folder
3. **Create 6 files:** Use templates for each file
4. **Gather info:** Prompt user for initial project details
5. **Validate:** Run `validate_memorybank.py`

## File Templates

### projectbrief.md
```markdown
# Project Brief

## Project Name
[Name]

## Core Purpose
[What problem does this solve?]

## Key Objectives
- Objective 1
- Objective 2

## Scope
[What's included and what's not]

## Success Criteria
[How do we know we succeeded?]
```

### productContext.md
```markdown
# Product Context

## User Problems
[What problems are users facing?]

## Solution Approach
[How does this project solve those problems?]

## User Experience Goals
- Goal 1
- Goal 2

## Key Features
- Feature 1
- Feature 2
```

### techContext.md
```markdown
# Technical Context

## Technology Stack
- **Framework:** [e.g., Next.js 14]
- **Language:** [e.g., TypeScript]
- **Database:** [e.g., PostgreSQL]

## Development Setup
[How to get started developing]

## Key Dependencies
- Dependency 1
- Dependency 2

## Constraints
[Technical limitations or requirements]
```

### systemPatterns.md
```markdown
# System Patterns

## Architecture Overview
[High-level system design]

## Key Technical Decisions
- Decision 1: [Rationale]
- Decision 2: [Rationale]

## Design Patterns
[Patterns used in the codebase]

## Component Relationships
[How major components interact]
```

### activeContext.md
```markdown
# Active Context

## Current Focus
[What you're working on right now]

## Recent Changes
[What changed recently]

## Next Steps
- Step 1
- Step 2

## Blockers
[Any issues preventing progress]

## Learnings
[Recent insights or patterns discovered]
```

### progress.md
```markdown
# Progress

## What's Working
- Working item 1
- Working item 2

## What's Left to Build
- [ ] Feature 1
- [ ] Feature 2

## Current Status
[Overall project status]

## Known Issues
- Issue 1
- Issue 2
```

## Tool Usage

```bash
# After creating files, validate
python scripts/validate_memorybank.py /path/to/project
```

See `scripts/README.md` for complete documentation.
