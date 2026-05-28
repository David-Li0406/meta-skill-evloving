---
name: ralph
description: Converts PRD markdown files to Ralph-compatible prd.json format for autonomous execution. Use when asked to convert a PRD, create prd.json, or prepare stories for Ralph.
---

# Ralph Skill

Converts Product Requirements Documents (PRD) from markdown format to the JSON structure required by the Ralph autonomous execution loop.

## Workflow

1. **Read PRD**: Parse the markdown PRD file
2. **Extract Stories**: Pull out all user stories with acceptance criteria
3. **Generate JSON**: Create prd.json with proper structure
4. **Validate**: Ensure all required fields are present

## prd.json Structure

```json
{
  "name": "Feature Name",
  "branchName": "feature/feature-name",
  "description": "Brief description of the feature",
  "userStories": [
    {
      "id": "US-001",
      "title": "Story Title",
      "description": "As a [user] I want [capability] So that [benefit]",
      "acceptanceCriteria": [
        "Criterion 1",
        "Criterion 2"
      ],
      "technicalNotes": "Implementation hints",
      "dependencies": ["US-000"],
      "priority": 1,
      "passes": false
    }
  ]
}
```

## Field Descriptions

| Field | Required | Description |
|-------|----------|-------------|
| name | Yes | Feature name from PRD title |
| branchName | Yes | Git branch name (kebab-case with feature/ prefix) |
| description | Yes | Overview from PRD |
| userStories | Yes | Array of story objects |
| id | Yes | Story ID (US-XXX format) |
| title | Yes | Short story title |
| description | Yes | Full user story text |
| acceptanceCriteria | Yes | Array of criteria strings (without checkboxes) |
| technicalNotes | No | Implementation hints |
| dependencies | No | Array of story IDs this depends on |
| priority | Yes | 1 = highest, larger = lower priority |
| passes | Yes | Always starts as false |

## Conversion Rules

1. **Extract story ID and title** from `### [US-XXX] Title` headers
2. **Parse user story format**: "As a... I want... So that..."
3. **Extract acceptance criteria**: Remove `- [ ]` checkbox prefixes
4. **Identify dependencies**: Look for "Dependency:" in technical notes
5. **Assign priority**: Based on phase/order in PRD (Phase 1 = priority 1-10, Phase 2 = 11-20, etc.)
6. **Set passes: false** for all stories initially

## Usage

```
Load the ralph skill and convert tasks/prd-[feature-name].md to prd.json
```

## Output

Creates `prd.json` in the project root, ready for Ralph execution via:

```bash
./scripts/ralph/ralph.sh
```
