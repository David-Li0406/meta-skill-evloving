---
name: generating-prd-from-userstory
description: Transforms UserStory.md into PRD.md by extracting features and converting user stories into functional requirements.
---

# PRD Generation from User Story

Converts `docs/UserStory.md` into `docs/PRD.md` with structured functional requirements.

## Purpose

Bridges the gap between user-focused stories and implementation-ready requirements by converting narrative descriptions into technical requirements.

## Workflow

1. **Read UserStory.md**
   - Validate file exists at `docs/UserStory.md`
   - Parse all sections: Problem, Users, Value, Stories, Criteria, Constraints

2. **Extract and convert**
   - User stories → Functional requirements (WHAT the system must do)
   - Success criteria + Constraints → Non-functional requirements (HOW it performs)
   - Group by functional area (CLI, API, Storage, etc.)

3. **Generate PRD.md**
   - Project Overview: Combine problem statement + value proposition
   - User Stories Reference: Link to UserStory.md
   - Functional Requirements: Organized by feature area
   - Non-Functional Requirements: Performance, usability, platform
   - Out of Scope: Copy from UserStory.md

4. **Save and next steps**
   - Check for existing PRD.md (backup as `PRD.md.bak` if overwriting)
   - Write to `docs/PRD.md`
   - Suggest: `make ralph_init` to generate prd.json

## Conversion Examples

**User Story → Functional Requirement**:
- "As a developer, I want to add tasks from CLI" → "CLI command: `task add "description"`"

**Success Criteria → Non-Functional**:
- "Operations in < 5 seconds" → "Performance: All CLI operations complete in < 5 seconds"

**Constraints → Non-Functional**:
- "Must work on Linux, macOS, Windows" → "Platform Support: Cross-platform compatibility"

## Template

See `ralph/templates/prd.md.template` for structure and placeholders.

## Usage

```bash
make ralph_prd
```

## Next Steps

```bash
make ralph_init    # Generate prd.json from PRD.md
make ralph_run     # Start Ralph loop
```
