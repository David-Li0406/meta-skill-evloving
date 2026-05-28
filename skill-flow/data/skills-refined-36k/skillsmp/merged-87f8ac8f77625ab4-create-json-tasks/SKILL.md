---
name: create-json-tasks
description: Use this skill to convert PRDs into prd.json format for execution in various task automation tools, creating JSON task files with user stories, acceptance criteria, and dependencies.
---

# Create JSON Tasks from PRDs

This skill converts PRDs (markdown files or text) into a prd.json format suitable for execution in automation tools like rube-goldberg-tui, ralph-tui, and loopwright.

> **Note:** This skill is bundled with JSON tracker plugins for various tools. Future tracker plugins (Linear, GitHub Issues, etc.) will bundle their own task creation skills.

---

## The Job

1. **Extract Quality Gates** from the PRD's "Quality Gates" section.
2. Parse user stories from the PRD.
3. Append quality gates to each story's acceptance criteria.
4. Set up dependencies between stories.
5. Output ready for execution with the respective tool.

---

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

---

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
    }
  ]
}
```

---

## Story Size: The #1 Rule

**Each story must be completable in ONE iteration (~one agent context window).**

### Right-sized stories:
- Add a database column + migration.
- Add a UI component to an existing page.
- Update a server action with new logic.
- Add a filter dropdown to a list.

### Too big (split these):
- "Build the entire dashboard" → Split into: schema, queries, UI components, filters.
- "Add authentication" → Split into: schema, middleware, login UI, session handling.
- "Refactor the API" → Split into one story per endpoint or pattern.

**Rule of thumb:** If you can't describe the change in 2-3 sentences, it's too big.

---

## Dependencies with `dependsOn`

Use the `dependsOn` array to specify which stories must complete first:

```json
{
  "id": "US-002",
  "title": "Create API endpoints",
  "dependsOn": ["US-001"]
}
```

The tool will:
- Show US-002 as "blocked" until US-001 completes.
- Never select US-002 for execution while US-001 is open.

**Correct dependency order:**
1. Schema/database changes (no dependencies).
2. Backend logic (depends on schema).
3. UI components (depends on backend).
4. Integration/polish (depends on UI).

---

## Acceptance Criteria: Quality Gates + Story-Specific

Each story's acceptance criteria should include:
1. **Story-specific criteria** from the PRD.
2. **Quality gates** from the PRD's Quality Gates section (appended at the end).

### Good criteria (verifiable):
- "Add `status` column to tasks table with default 'open'."
- "Filter dropdown has options: All, Open, Closed."

### Bad criteria (vague):
- ❌ "Works correctly."
- ❌ "User can do X easily."

---

## Conversion Rules

1. **Extract Quality Gates** from PRD first.
2. **Each user story → one JSON entry.**
3. **IDs:** Sequential (US-001, US-002, etc.).
4. **Priority:** Based on dependency order (1 = highest).
5. **dependsOn:** Array of story IDs this story requires.
6. **All stories:** `passes: false` and empty `notes`.
7. **branchName:** Derive from feature name, kebab-case, prefixed with the tool name.
8. **Acceptance criteria:** Story criteria + quality gates appended.
9. **UI stories:** Also append UI-specific gates (browser verification).

---

## Output Location

Default: `./tasks/prd.json` (alongside the PRD markdown files).

Or specify a different path - the tool will use it with:
```bash
[tool] run --prd ./path/to/prd.json
```

---

## Checklist Before Saving

- [ ] Extracted Quality Gates from PRD (or asked user if missing).
- [ ] Each story completable in one iteration.
- [ ] Stories ordered by dependency (schema → backend → UI).
- [ ] `dependsOn` correctly set for each story.
- [ ] Quality gates appended to every story's acceptance criteria.
- [ ] UI stories have browser verification (if specified in Quality Gates).
- [ ] Acceptance criteria are verifiable (not vague).
- [ ] No circular dependencies.