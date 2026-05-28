---
name: prd-converter
description: "Convert PRDs to prd.json format for the SDK Bridge autonomous agent system. Use when you have an existing PRD and need to convert it to SDK Bridge's JSON format. Triggers on: convert this prd, turn this into sdk-bridge format, create prd.json from this, convert prd to json."
---

# SDK Bridge PRD Converter

Converts existing PRDs to the prd.json format that SDK Bridge uses for autonomous execution.

---

## The Job

Take a PRD (markdown file or text) and convert it to `prd.json` in your project directory.

---

## Output Format (Enhanced Schema)

```json
{
  "project": "[Project Name]",
  "branchName": "sdk-bridge/[feature-name-kebab-case]",
  "description": "[Feature description from PRD title/intro]",
  "userStories": [
    {
      "id": "US-001",
      "title": "[Story title]",
      "description": "As a [user], I want [feature] so that [benefit]",
      "acceptanceCriteria": [
        "Criterion 1",
        "Criterion 2 with verification",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": "",
      "depends_on": [],
      "related_to": [],
      "implementation_hint": "",
      "check_before_implementing": []
    }
  ]
}
```

### New Schema Fields (Phase 3 Enhancements)

- **depends_on** (array): IDs of stories that MUST complete before this one (e.g., `["US-001", "US-005"]`)
- **related_to** (array): IDs of stories that may contain related work to check (e.g., `["US-002"]`)
- **implementation_hint** (string): Guidance like "Check if US-005 already implemented this" or "Reuse existing badge component"
- **check_before_implementing** (array): Commands to run to verify existing implementation (e.g., `["grep cabin_class api.py"]`)

**When to use each:**
- `depends_on`: Hard dependency - this story CANNOT be done until dependency completes
- `related_to`: Soft dependency - check this story for similar code or patterns
- `implementation_hint`: Free-form text guidance for the agent
- `check_before_implementing`: Specific search commands to detect existing implementation

---

## Story Size: The Number One Rule

**Each story must be completable in ONE SDK Bridge iteration (one context window).**

SDK Bridge spawns a fresh Claude instance per iteration with no memory of previous work. If a story is too big, the LLM runs out of context before finishing and produces broken code.

### Right-sized stories (3-5 criteria):
**Data Layer:**
- Add new field to data model with validation
- Create migration for schema change
- Implement data access method for new query

**Logic Layer:**
- Add business rule validation
- Implement calculation or transformation logic
- Add error handling for specific failure case

**Presentation Layer:**
- Create reusable component with basic functionality
- Add interaction handler (click, submit, etc.)
- Implement visual state (loading, error, success)

### Too big (8+ criteria - must split):
**Pattern:** "Build entire [subsystem]"
- ❌ Single story: All layers combined
- ✅ Split into: Data → Logic → Presentation → Integration

**Pattern:** "Add complex [feature]"
- ❌ Single story: All configuration + functionality + edge cases
- ✅ Split into: Core behavior → Options → Error handling

**Pattern:** "Refactor [large module]"
- ❌ Single story: Entire module at once
- ✅ Split into: One story per file/function/component

**Rule of thumb:** If you cannot describe the change in 2-3 sentences, it is too big.

**Validation Rules:**
- ✅ **Ideal:** 3-5 acceptance criteria (including typecheck/browser verification)
- ⚠️ **Warning:** 6-7 criteria - consider splitting if possible
- ❌ **Too large:** 8+ criteria - MUST split into multiple stories
- **Time target:** Each story should complete in 10-20 minutes

**After converting, check for oversized stories:**
```bash
jq '.userStories[] | select((.acceptanceCriteria | length) > 7) | "\(.id): \(.title) - \(.acceptanceCriteria | length) criteria (TOO LARGE)"'
```

If you find stories with 8+ criteria, recommend splitting them in your output.

---

## Story Ordering: Dependencies First

Stories execute in priority order. Earlier stories must not depend on later ones.

**Correct order:**
1. Schema/database changes (migrations)
2. Server actions / backend logic
3. UI components that use the backend
4. Dashboard/summary views that aggregate data

**Wrong order:**
1. UI component (depends on schema that does not exist yet)
2. Schema change

---

## Acceptance Criteria: Must Be Verifiable

Each criterion must be something SDK Bridge can CHECK, not something vague.

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
"Verify in browser using dev-browser skill"
```

Frontend stories are NOT complete until visually verified. SDK Bridge will use the dev-browser skill to navigate to the page, interact with the UI, and confirm changes work.

---

## Conversion Rules

1. **Each user story becomes one JSON entry**
2. **IDs**: Sequential (US-001, US-002, etc.)
3. **Priority**: Based on dependency order, then document order
4. **All stories**: `passes: false` and empty `notes`
5. **branchName**: Derive from feature name, kebab-case, prefixed with `sdk-bridge/`
6. **Always add**: "Typecheck passes" to every story's acceptance criteria
7. **Infer dependencies**: Detect `depends_on`, `related_to`, and add hints (see below)

### Dependency Inference Rules

**Auto-detect `depends_on`:**
- Backend stories depend on schema/database stories
- UI stories depend on backend API/service stories
- Integration stories depend on component stories
- Look for explicit "Depends on: US-XXX" in PRD

**⚠️ Avoid False Dependencies:**
- NOT all stories need to depend on the previous story
- Stories can run in parallel if they work on different files/modules
- Only add `depends_on` for TRUE blocking dependencies
- **Test:** Can this story be implemented without the previous story being complete? If yes, don't add dependency

**True Dependencies (add `depends_on`):**
- Data model required before business logic using it
- API endpoint required before UI consuming it
- Authentication required before protected features
- Base component required before extensions/variants
- Configuration required before features using it

**False Dependencies (NO `depends_on`, use `related_to`):**
- Two UI components in different parts of the app
- Two API endpoints serving different purposes
- Two database tables with no foreign key relationship
- Parallel implementation tracks (e.g., UI theme + API layer)
- Sequential numbering doesn't imply dependency

**Auto-detect `related_to`:**
- Stories working on the same file/module
- Stories in the same feature area (e.g., all "priority" stories)
- Frontend and backend halves of the same feature
- Later stories in a sequence (US-007 related to US-005, US-006)

**Generate `implementation_hint`:**
- If `related_to` is not empty: "Check US-XXX for similar implementation patterns"
- If UI story follows data/API story: "US-XXX may have already implemented the data layer for this"
- If splitting a feature: "This is part of [feature area], coordinate with US-XXX for consistency"
- If extending existing work: "Builds on US-XXX, review that implementation before starting"

**Generate `check_before_implementing`:**
Extract key identifiers from acceptance criteria and create search commands:

**For data models:** `grep -rn "[ModelName]\|[field_name]" src/models/`
**For API/services:** `grep -rn "[endpoint_name]\|[function_name]" src/api/ src/services/`
**For UI components:** `grep -rn "[ComponentName]" src/components/ src/pages/`
**For configuration:** `grep -rn "[config_key]" config/ .env`

Use actual identifiers from the story (class names, function names, field names), not generic terms.

### Example: Dependency Detection

**Scenario:** Feature requiring data model, API endpoint, and UI

**PRD Stories:**
```markdown
### US-010: Add status field to data model
### US-011: Create filtering API endpoint
### US-012: Build filter UI component
```

**Dependency Analysis:**
- US-011 needs US-010 (can't filter by status field that doesn't exist) → `depends_on: ["US-010"]`
- US-012 needs US-011 (UI needs API to call) → `depends_on: ["US-011"]`
- US-012 related to US-010 (both involve "status" concept) → `related_to: ["US-010"]`

**Converted to JSON:**
```json
{
  "id": "US-012",
  "title": "Build filter UI component",
  "depends_on": ["US-011"],
  "related_to": ["US-010"],
  "implementation_hint": "US-010 added the status field to the data model. US-011 implemented the filtering endpoint. Review both for field names and API contract.",
  "check_before_implementing": [
    "grep -rn 'status' src/models/",
    "grep -rn 'filter.*status' src/api/"
  ]
}
```

---

## Splitting Large Features

Apply systematic decomposition when features have 8+ acceptance criteria:

**Pattern 1: Layer-Based Split**
```
Monolithic: "Add [feature] system"
↓
Decomposed:
1. "Implement [feature] data model"
2. "Create [feature] business logic"
3. "Build [feature] API endpoints"
4. "Design [feature] UI components"
5. "Add [feature] user workflows"
```

**Pattern 2: Capability-Based Split**
```
Monolithic: "Build advanced [feature]"
↓
Decomposed:
1. "Implement basic [feature] functionality"
2. "Add [feature] configuration options"
3. "Implement [feature] batch operations"
4. "Add [feature] export capability"
```

**Pattern 3: Journey-Based Split**
```
Monolithic: "Implement [workflow]"
↓
Decomposed:
1. "Implement [workflow] step 1: [action]"
2. "Implement [workflow] step 2: [action]"
3. "Implement [workflow] step 3: [action]"
4. "Add [workflow] error recovery"
```

Each story focuses on one responsibility and can be verified independently.

---

## Example

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
  "branchName": "sdk-bridge/task-status",
  "description": "Task Status Feature - Track task progress with status indicators",
  "userStories": [
    {
      "id": "US-001",
      "title": "Add status field to tasks table",
      "description": "As a developer, I need to store task status in the database.",
      "acceptanceCriteria": [
        "Add status column: 'pending' | 'in_progress' | 'done' (default 'pending')",
        "Generate and run migration successfully",
        "Typecheck passes"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-002",
      "title": "Display status badge on task cards",
      "description": "As a user, I want to see task status at a glance.",
      "acceptanceCriteria": [
        "Each task card shows colored status badge",
        "Badge colors: gray=pending, blue=in_progress, green=done",
        "Typecheck passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 2,
      "passes": false,
      "notes": "",
      "depends_on": ["US-001"],
      "related_to": [],
      "implementation_hint": "Reuse existing badge component if available, just add status color variants.",
      "check_before_implementing": [
        "grep -r 'Badge' components/",
        "grep status tasks/"
      ]
    },
    {
      "id": "US-003",
      "title": "Add status toggle to task list rows",
      "description": "As a user, I want to change task status directly from the list.",
      "acceptanceCriteria": [
        "Each row has status dropdown or toggle",
        "Changing status saves immediately",
        "UI updates without page refresh",
        "Typecheck passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 3,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-004",
      "title": "Filter tasks by status",
      "description": "As a user, I want to filter the list to see only certain statuses.",
      "acceptanceCriteria": [
        "Filter dropdown: All | Pending | In Progress | Done",
        "Filter persists in URL params",
        "Typecheck passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 4,
      "passes": false,
      "notes": ""
    }
  ]
}
```

---

## Archiving Previous Runs

**Before writing a new prd.json, check if there is an existing one from a different feature:**

1. Read the current `prd.json` if it exists
2. Check if `branchName` differs from the new feature's branch name
3. If different AND `progress.txt` has content beyond the header:
   - Create archive folder: `archive/YYYY-MM-DD-feature-name/`
   - Copy current `prd.json` and `progress.txt` to archive
   - Reset `progress.txt` with fresh header

**The sdk-bridge.sh script handles this automatically** when you run it, but if you are manually updating prd.json between runs, archive first.

---

## Checklist Before Saving

Before writing prd.json, verify:

- [ ] **Previous run archived** (if prd.json exists with different branchName, archive it first)
- [ ] Each story is completable in one iteration (small enough)
- [ ] Stories are ordered by dependency (schema to backend to UI)
- [ ] Every story has "Typecheck passes" as criterion
- [ ] UI stories have "Verify in browser using dev-browser skill" as criterion
- [ ] Acceptance criteria are verifiable (not vague)
- [ ] No story depends on a later story
