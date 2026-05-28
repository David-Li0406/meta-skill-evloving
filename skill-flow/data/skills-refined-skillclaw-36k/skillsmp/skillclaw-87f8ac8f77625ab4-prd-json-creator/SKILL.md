---
name: prd-json-creator
description: Use this skill to convert PRDs into a standardized prd.json format for various execution environments, including rube-goldberg-tui, ralph-tui, and loopwright.
---

# PRD JSON Creator

This skill converts Product Requirement Documents (PRDs) into a prd.json format suitable for execution in different environments. It extracts user stories, acceptance criteria, and dependencies, ensuring the output is ready for the specified tool.

## The Job

Take a PRD (markdown file or text) and create a prd.json file:
1. **Extract Quality Gates** from the PRD's "Quality Gates" section.
2. Parse user stories from the PRD.
3. Append quality gates to each story's acceptance criteria.
4. Set up dependencies between stories.
5. Output ready for the specified execution command.

## Step 1: Extract Quality Gates

Look for the "Quality Gates" section in the PRD:

```markdown
## Quality Gates

These commands must pass for every user story:
- `pnpm typecheck` - Type checking
- `pnpm lint` - Linting

For UI stories, also include:
- Verify in browser using dev-browser skill
```

Extract:
- **Universal gates:** Commands that apply to ALL stories (e.g., `pnpm typecheck`).
- **UI gates:** Commands that apply only to UI stories (e.g., browser verification).

**If no Quality Gates section exists:** Ask the user what commands should pass, or use a sensible default like `npm run typecheck`.

## Output Format

The JSON file must be a flat object at the root level:

```json
{
  "name": "[Project name from PRD or directory]",
  "branchName": "[tool]/[feature-name-kebab-case]",
  "description": "[Feature description from PRD]",
  "userStories": [
    {
      "id": "US-001",
      "title": "[Story title]",
      "description": "As a [user], I want [feature] so that [benefit]",
      "acceptanceCriteria": [
        "Criterion 1 from PRD",
        "Criterion 2 from PRD",
        "pnpm typecheck passes",
        "pnpm lint passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": "",
      "dependsOn": []
    },
    {
      "id": "US-002",
      "title": "[UI Story that depends on US-001]",
      "description": "...",
      "acceptanceCriteria": [
        "...",
        "pnpm typecheck passes",
        "pnpm lint passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 2,
      "passes": false,
      "notes": "",
      "dependsOn": ["US-001"]
    }
  ]
}
```