---
name: ralph-json-generator
description: "Convert PRDs to prd.json format for autonomous execution workflows. Use when you have an existing PRD and need to convert it to executable JSON format. Works with any PRD markdown file. Triggers on: convert this prd to json, turn this into ralph format, create prd.json from this, make this executable."
model: claude-haiku-4-5-20251001
---

# Ralph JSON Generator (Haiku-Powered)

Converts existing PRDs (markdown or text) to executable `prd.json` format for autonomous agent workflows. Uses Claude Haiku for fast, cost-effective conversions.

---

## The Job

Take a PRD (markdown file or text) and convert it to `prd.json` in your project's `tasks/` directory.

---

## Output Format

```json
{
  "project": "[Project Name]",
  "branchName": "feature/[feature-name-kebab-case]",
  "description": "[Feature description from PRD title/intro]",
  "userStories": [
    {
      "id": "US-001",
      "title": "[Story title]",
      "description": "As a [user], I want [feature] so that [benefit]",
      "acceptanceCriteria": ["Criterion 1", "Criterion 2", "Typecheck passes"],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

---

## Story Size: The Number One Rule

**Each story must be completable in ONE focused work session (one context window).**

If a story is too big, the developer (or AI agent) runs out of focus before finishing and produces incomplete code.

### Right-sized stories:

- Add a database column and migration
- Add a UI component to an existing page
- Update a server action with new logic
- Add a filter dropdown to a list

### Too big (split these):

- "Build the entire dashboard" → Split into: schema, queries, UI components, filters
- "Add authentication" → Split into: schema, middleware, login UI, session handling
- "Refactor the API" → Split into one story per endpoint or pattern

**Rule of thumb:** If you cannot describe the change in 2-3 sentences, it is too big.

---

## Story Ordering: Dependencies First

Stories execute in priority order. Earlier stories must not depend on later ones.

**Correct order:**

1. Schema/database changes (migrations)
2. Server actions / backend logic
3. UI components that use the backend
4. Dashboard/summary views that aggregate data

**Wrong order:**

1. UI component (depends on schema that doesn't exist yet)
2. Schema change

---

## Acceptance Criteria: Must Be Verifiable

Each criterion must be something you can CHECK, not something vague.

### Good criteria (verifiable):

- "Add `status` column to tasks table with default 'pending'"
- "Filter dropdown has options: All, Active, Completed"
- "Clicking delete shows confirmation dialog"
- "Typecheck passes"
- "Tests pass"

### Bad criteria (vague):

- "Works correctly"
- "User can do X easily"
- "Good UX"
- "Handles edge cases"

### Always include as final criterion:

```
"Typecheck passes"
```

For stories with testable logic, also include:

```
"Tests pass"
```

### For stories that change UI, also include:

```
"Verify in browser using agent-browser skill"
```

Frontend stories are NOT complete until visually verified. Use agent-browser skill to navigate to the page, interact with the UI, and confirm changes work.

---

## Test Coverage Requirements

### Backend Features: PEST Tests (MANDATORY)

**ALL backend features MUST have PEST test coverage integrated into the story.**

For backend stories (models, controllers, services, APIs, database changes), include these acceptance criteria:

```
"Write PEST tests in app/Modules/{Module}/Tests/Feature/ or Tests/Unit/"
"Tests cover all new functionality and edge cases"
"Tests pass when run with 'cd site && composer test'"
```

**Backend stories are NOT complete without passing PEST tests.**

**Note**: Tests MUST be run via composer scripts:
- `cd site && composer test` - runs PEST tests via scripts/test.sh (auto-detects Sail)

### Frontend Features: Test Coverage Rules

**For UI stories, you MUST add:**

1. **Agent-Browser Verification (ALWAYS REQUIRED)** - Visual confirmation for ALL UI changes
2. **E2E Test Story (REQUIRED for complex frontend tasks)** - Automated tests for critical user flows

**When to add E2E tests:**
- Complex user interactions (multi-step workflows, forms with validation)
- Critical user paths (authentication, checkout, data submission)
- Features with significant business logic in the UI
- Components with conditional rendering or state management

**When E2E tests may not be needed:**
- Simple visual changes (styling updates, layout tweaks)
- Static content updates
- Minor UI adjustments
- Non-interactive components

---

## Additional Story Templates

### 1. E2E Test Story (For Complex Frontend Tasks)

For complex UI stories, add a corresponding e2e test story:

```json
{
  "id": "US-XXX-02",
  "title": "E2E Test: [Original Story Title]",
  "description": "Create an e2e test to verify [what the original story does].",
  "acceptanceCriteria": [
    "Create a Playwright e2e test in site/tests/e2e/",
    "Test navigates to the relevant page",
    "Test performs the user action (click, input, etc.)",
    "Test verifies the expected outcome",
    "Build assets before testing with 'cd site && bun run build'",
    "Test must pass when run with 'cd site && composer e2e'"
  ],
  "priority": [same as original + 0.1],
  "passes": false,
  "notes": ""
}
```

**Note**: E2E tests run via `cd site && composer e2e` which executes `bun run test:e2e`

**Debugging Note:** If e2e tests fail repeatedly, use the agent-browser skill for debugging:
- Start server: `~/.claude/skills/agent-browser/server.sh &`
- Use `getAISnapshot()` to inspect page structure
- Take debug screenshots to understand failures
- Check for timing issues or selector problems

### 2. Agent-Browser Verification Story (Required)

For each UI story, add a agent-browser verification story:

```json
{
  "id": "US-XXX-03",
  "title": "Agent-Browser Verification: [Original Story Title]",
  "description": "Verify [original story] using the agent-browser skill for visual confirmation.",
  "acceptanceCriteria": [
    "Check if agent-browser server is running (curl -s http://localhost:9222), start with '~/.claude/skills/agent-browser/server.sh &' if not",
    "Navigate to the relevant page",
    "Perform the user action and verify visually",
    "Take a screenshot as evidence (save to .claude/skills/agent-browser/tmp/)",
    "Verification must be documented in notes with screenshot path"
  ],
  "priority": [same as original + 0.2],
  "passes": false,
  "notes": ""
}
```

### Story Grouping Pattern

For each UI-related fix or feature, the story sequence should be:

1. **US-XXX-01**: The actual fix/feature implementation
2. **US-XXX-02**: E2E test for the fix/feature
3. **US-XXX-03**: Dev-browser visual verification

This ensures:
- Automated regression testing via e2e tests
- Visual confirmation via agent-browser
- Complete verification coverage

---

## Conversion Rules

1. **Each user story becomes one JSON entry**
2. **IDs**: Sequential (US-001, US-002, etc.)
3. **Priority**: Based on dependency order, then document order
4. **All stories**: `passes: false` and empty `notes`
5. **branchName**: Derive from feature name, kebab-case, prefixed with `feature/`
6. **Always add**: "Typecheck passes" to every story's acceptance criteria if not present

---

## Splitting Large PRDs

If a PRD has big features, split them into smaller stories:

**Original:**

> "Add user notification system"

**Split into:**

1. US-001: Add notifications table to database
2. US-002: Create notification service for sending notifications
3. US-003: Add notification bell icon to header
4. US-004: Create notification dropdown panel
5. US-005: Add mark-as-read functionality
6. US-006: Add notification preferences page

Each is one focused change that can be completed and verified independently.

---

## Example Conversion

**Input PRD:**

```markdown
# Task Status Feature

Add ability to mark tasks with different statuses.

## Requirements

- Toggle between pending/in-progress/done on task list
- Filter list by status
- Show status badge on each task
- Persist status in database
```

**Output prd.json:**

```json
{
  "project": "TaskApp",
  "branchName": "feature/task-status",
  "description": "Task Status Feature - Track task progress with status indicators",
  "userStories": [
    {
      "id": "US-001",
      "title": "Add status field to tasks table",
      "description": "As a developer, I need to store task status in the database.",
      "acceptanceCriteria": ["Add status column: 'pending' | 'in_progress' | 'done' (default 'pending')", "Generate and run migration successfully", "Typecheck passes"],
      "priority": 1,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-002",
      "title": "Display status badge on task cards",
      "description": "As a user, I want to see task status at a glance.",
      "acceptanceCriteria": ["Each task card shows colored status badge", "Badge colors: gray=pending, blue=in_progress, green=done", "Typecheck passes", "Verify in browser using agent-browser skill"],
      "priority": 2,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-003",
      "title": "Add status toggle to task list rows",
      "description": "As a user, I want to change task status directly from the list.",
      "acceptanceCriteria": ["Each row has status dropdown or toggle", "Changing status saves immediately", "UI updates without page refresh", "Typecheck passes", "Verify in browser using agent-browser skill"],
      "priority": 3,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-004",
      "title": "Filter tasks by status",
      "description": "As a user, I want to filter the list to see only certain statuses.",
      "acceptanceCriteria": ["Filter dropdown: All | Pending | In Progress | Done", "Filter persists in URL params", "Typecheck passes", "Verify in browser using agent-browser skill"],
      "priority": 4,
      "passes": false,
      "notes": ""
    }
  ]
}
```

**With E2E Test Story:**

```json
    {
      "id": "US-002-02",
      "title": "E2E Test: Display status badge on task cards",
      "description": "Create an e2e test to verify status badges display correctly on task cards.",
      "acceptanceCriteria": ["Create a Playwright e2e test in site/tests/e2e/", "Test navigates to task list page", "Test verifies badge elements exist with correct colors", "Build assets before testing with 'cd site && bun run build'", "Test must pass when run with 'cd site && composer e2e'"],
      "priority": 2.1,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-002-03",
      "title": "Agent-Browser Verification: Display status badge on task cards",
      "description": "Verify the status badge display using agent-browser skill for visual confirmation.",
      "acceptanceCriteria": ["Start agent-browser server with '~/.claude/skills/agent-browser/server.sh &'", "Navigate to task list page", "Verify badge colors visually (gray=pending, blue=in_progress, green=done)", "Take screenshot as evidence (save to .claude/skills/agent-browser/tmp/)", "Document verification in notes with screenshot path"],
      "priority": 2.2,
      "passes": false,
      "notes": ""
    },

---

## Archiving Previous Conversions

**Before writing a new prd.json, check if there's an existing one from a different feature:**

1. Read the current `tasks/prd.json` if it exists
2. Check if `branchName` differs from the new feature's branch name
3. If different and the file has substantial content:
   - Create archive folder: `tasks/archive/YYYY-MM-DD-feature-name/`
   - Copy current `prd.json` to archive
   - Note in output that previous version was archived

This preserves previous work while allowing new features to be converted.

---

## Usage Modes

### Mode 1: Convert from File

```
"Convert tasks/prd-authentication.md to prd.json"
```

### Mode 2: Convert from Text/Clipboard

```
"Convert this PRD to prd.json: [paste PRD content]"
```

### Mode 3: Convert with Splitting

```
"Convert tasks/prd-dashboard.md to prd.json and split large stories"
```

---

## Output Location

- **Primary output:** `tasks/prd.json`
- **Archives:** `tasks/archive/YYYY-MM-DD-feature-name/prd.json`

---

## Validation Checklist

Before saving prd.json, verify:

- [ ] **Previous run archived** (if prd.json exists with different branchName)
- [ ] Each story is completable in one session (small enough)
- [ ] Stories are ordered by dependency (schema → backend → UI)
- [ ] Every story has "Typecheck passes" as criterion
- [ ] UI stories have "Verify in browser using agent-browser skill" as criterion
- [ ] **UI stories have corresponding E2E test story (US-XXX-02)**
- [ ] **UI stories have corresponding Dev-Browser verification story (US-XXX-03)**
- [ ] Acceptance criteria are verifiable (not vague)
- [ ] No story depends on a later story
- [ ] Project name matches your project
- [ ] Branch name is kebab-case with appropriate prefix

---

## After Conversion

Once prd.json is created, you can:

1. **Review the JSON** - Check story order and sizes
2. **Execute stories** - Use with compound engineering or other workflows
3. **Track progress** - Update `passes: true` as stories complete
4. **Add notes** - Document learnings in the `notes` field

---

## Integration with Other Skills

### Works Great With:

**ralph-prd-generator:**

- Create PRD with ralph-prd-generator
- Convert to JSON with ralph-json-generator
- Complete workflow!

**Compound Engineering:**

- Convert PRD to JSON
- Execute with `/compound-engineering:work`
- Track completion

**Dev Browser:**

- JSON includes agent-browser verification for UI stories
- Ensures visual confirmation

---

## Model Usage Note

This skill uses **Claude Haiku (claude-haiku-4-5-20251001)** for cost-effective JSON conversion. Haiku excels at:

- ✅ Structured data transformation
- ✅ Fast processing
- ✅ Pattern recognition
- ✅ JSON generation

Perfect for converting PRDs to executable format economically.

---

## Example Workflow

```
# Step 1: Create PRD
"Create a PRD for user authentication"
→ Saved to tasks/prd-user-authentication.md

# Step 2: Convert to JSON
"Convert tasks/prd-user-authentication.md to prd.json"
→ Saved to tasks/prd.json

# Step 3: Execute
"Execute user story US-001 from prd.json"
→ Implements first story

# Step 4: Verify
"Mark US-001 as complete in prd.json"
→ Updates passes: true
```

---

## Tips for Best Results

### 1. Start with Good PRDs

Well-structured PRDs convert cleanly. Use ralph-prd-generator for consistent format.

### 2. Review Before Execution

Check the JSON before starting work - adjust story sizes if needed.

### 3. Archive Old Work

Keep previous prd.json files for reference - the skill handles this automatically.

### 4. Update as You Go

Mark stories as complete (`passes: true`) and add notes about learnings.

---

## Common Patterns

### Pattern 1: Full Workflow

```
1. Create PRD with ralph-prd-generator
2. Convert with ralph-json-generator
3. Execute systematically
```

### Pattern 2: Quick Conversion

```
"Convert this quick feature spec to prd.json: [paste text]"
```

### Pattern 3: Story Splitting

```
"This PRD has large stories - convert and split them appropriately"
```

---

## Cost Comparison

**Per conversion** (typical PRD with 5-10 stories):

| Model     | Cost   | Speed   |
| --------- | ------ | ------- |
| **Haiku** | ~$0.03 | Fast ⚡ |
| Sonnet    | ~$0.15 | Slower  |
| Opus      | ~$0.30 | Slowest |

Haiku is ideal for this structured transformation task!
