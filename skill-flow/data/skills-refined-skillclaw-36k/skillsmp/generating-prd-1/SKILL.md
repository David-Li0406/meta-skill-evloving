---
name: generating-prd
description: Generates prd.json task tracking file from PRD.md requirements document. Use when initializing Ralph loop or when the user asks to convert PRD to JSON format for autonomous execution.
---

# PRD to JSON Conversion

Parses `docs/PRD.md` and generates `ralph/state/prd.json` for Ralph loop task tracking.

## Purpose

The Ralph loop requires a structured JSON file to track task completion. This
skill extracts implementation stories from PRD.md and creates the required
prd.json format.

## Workflow

1. **Read `docs/PRD.md`** to extract functional requirements
2. **Identify atomic stories** - tasks that fit in single context window
3. **Generate `ralph/state/prd.json`** with proper schema
4. **Validate JSON** format before saving

## PRD.json Schema

See `ralph/templates/prd.json.template` for the complete schema and structure.

Required fields:
- `project`: The current project name
- `desciption`: A concise project description
- `source`: 'docs/PRD.md'
- `generated`: "YYYY-MM-DD HH:MM:SS"
- `stories`: Array of story objects (see below)

## Story Extraction Rules

**Atomic Stories**: Each story must complete within single context window

- Single feature addition (100-300 lines)
- Single bug fix
- Single refactoring task
- Single test suite addition

**From PRD.md Extract**:

- Functional requirements → stories
- API endpoints → implementation stories
- CLI commands → feature stories
- Evaluation metrics → metric implementation stories

**Story Attributes**:

- `id`: Unique identifier (STORY-XXX format)
- `title`: Brief 3-7 word description
- `description`: What to implement (1-2 sentences)
- `acceptance`: Testable completion criteria
- `files`: Expected files to modify/create
- `passes`: Boolean (false initially)
- `completed_at`: Timestamp when marked passing

## Validation Rules

Before saving prd.json:

- [ ] All required fields present for each story
- [ ] IDs are unique
- [ ] All stories have `passes: false` initially
- [ ] Acceptance criteria are specific and testable
- [ ] File paths match project structure

## Example Story Conversion

**From PRD.md**:
```markdown
## Functional Requirements
### CLI
- Command Line Interface:
  - Environment setup commands: make setup_dev
```

**To prd.json story**:
```json
{
  "id": "STORY-001",
  "title": "Add make setup_dev command",
  "description": "Create Makefile recipe for development environment setup",
  "acceptance": [
    "Makefile contains setup_dev recipe",
    "Recipe installs all dev dependencies",
    "Recipe passes validation checks"
  ],
  "files": ["Makefile"],
  "passes": false,
  "completed_at": null
}
```

Use `ralph/templates/prd.json.template` as the base structure and populate the stories array.

## Usage

To generate prd.json:

```bash
# Run this skill to parse PRD.md
# Output will be saved to ralph/state/prd.json
```

Ralph loop will then use this file to track task completion.
