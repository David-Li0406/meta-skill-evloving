# Ralph JSON Converter - Installation & Usage Guide

## What This Skill Does

Converts PRD markdown files into executable `prd.json` format for systematic implementation. Features:

- ✅ Converts any PRD markdown to structured JSON
- ✅ Ensures stories are properly sized (one session each)
- ✅ Orders stories by dependencies
- ✅ Adds verification criteria automatically
- ✅ Archives previous conversions
- ✅ Uses Claude Haiku for cost-effective conversion

---

## Installation (Project-Local)

This skill works alongside `ralph-prd-generator` in your project.

### Step 1: Create Skills Directory

```bash
# Navigate to your project root
cd ~/Work/htdocs/Enskiedutech

# Create the skill directory
mkdir -p .claude/skills/ralph-json-converter
```

### Step 2: Copy the Skill File

```bash
# Copy SKILL.md to your project
# (Download from outputs and place here)
cp /path/to/ralph-json-converter/SKILL.md .claude/skills/ralph-json-converter/
```

### Step 3: Verify Installation

```bash
ls -la .claude/skills/ralph-json-converter/SKILL.md
```

### Step 4: Ensure Tasks Directory Exists

```bash
# Create if not already present
mkdir -p tasks
mkdir -p tasks/archive
```

Your project structure:

```
your-project/
├── .claude/
│   └── skills/
│       ├── ralph-prd-generator/
│       │   └── SKILL.md
│       └── ralph-json-converter/
│           └── SKILL.md
├── tasks/
│   ├── prd-*.md              # PRD markdown files
│   ├── prd.json              # Current executable JSON
│   └── archive/              # Previous conversions
│       └── 2026-01-10-feature-name/
│           └── prd.json
├── public/
└── package.json
```

---

## How to Use

### Method 1: Convert Existing PRD File

```bash
# Convert a specific PRD file
"Convert tasks/prd-authentication.md to prd.json"
```

**What happens:**

1. Claude reads the PRD markdown
2. Extracts user stories and requirements
3. Ensures stories are properly sized
4. Orders by dependencies
5. Adds verification criteria
6. Saves to `tasks/prd.json`

### Method 2: Convert from Text

```bash
# Paste PRD content directly
"Convert this PRD to prd.json: [paste PRD text]"
```

### Method 3: Convert with Story Splitting

```bash
# Automatically split large stories
"Convert tasks/prd-dashboard.md to prd.json and split any large stories"
```

---

## Complete Workflow Example

### Scenario: Building User Authentication

**Step 1: Create the PRD**

```
You: "Create a PRD for user authentication with email and password"

Claude (using ralph-prd-generator):
[Asks clarifying questions]
[Generates comprehensive PRD]
✓ Saved to tasks/prd-user-authentication.md
```

**Step 2: Convert to JSON**

```
You: "Convert tasks/prd-user-authentication.md to prd.json"

Claude (using ralph-json-converter):
[Reads PRD markdown]
[Validates story sizes]
[Orders by dependencies]
[Generates JSON]
✓ Saved to tasks/prd.json

Summary:
- 6 user stories created
- Ordered: Schema → Backend → UI
- All stories include typecheck verification
- UI stories include browser verification
```

**Step 3: Review the JSON**

```
You: "Show me the contents of tasks/prd.json"

Claude: [Displays the JSON structure]
```

**Step 4: Execute Stories**

```
You: "Implement user story US-001 from prd.json"

Claude: [Implements the first story systematically]
```

**Step 5: Track Progress**

```
You: "Mark US-001 as complete in prd.json"

Claude: [Updates "passes": true, adds notes]
```

---

## Understanding the JSON Format

### JSON Structure

```json
{
  "project": "MyApp",
  "branchName": "feature/user-authentication",
  "description": "User authentication with email/password login",
  "userStories": [
    {
      "id": "US-001",
      "title": "Add users table to database",
      "description": "As a developer, I need to store user credentials securely.",
      "acceptanceCriteria": ["Create users table with email, password_hash columns", "Add unique constraint on email", "Generate and run migration", "Typecheck passes"],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

### Field Descriptions

| Field                | Purpose                     | Example                   |
| -------------------- | --------------------------- | ------------------------- |
| `project`            | Your project name           | "TaskApp"                 |
| `branchName`         | Git branch for this feature | "feature/auth-system"     |
| `description`        | Brief feature summary       | "User authentication..."  |
| `id`                 | Story identifier            | "US-001"                  |
| `title`              | Short story name            | "Add users table"         |
| `description`        | Full user story             | "As a [user]..."          |
| `acceptanceCriteria` | Verifiable checklist        | ["Criterion 1", ...]      |
| `priority`           | Execution order             | 1, 2, 3...                |
| `passes`             | Completion status           | false → true when done    |
| `notes`              | Implementation notes        | "Used bcrypt for hashing" |

---

## Story Sizing Rules

### ✅ Right-Sized Stories

Each story should be completable in **one focused work session** (~1-2 hours).

**Examples:**

- "Add status column to tasks table"
- "Create login form component"
- "Add password reset endpoint"
- "Display user avatar in header"

### ❌ Too Large - Need Splitting

**Example:** "Build user authentication system"

**Split into:**

1. US-001: Add users table to database
2. US-002: Create password hashing utility
3. US-003: Implement login endpoint
4. US-004: Create login form UI
5. US-005: Add session management
6. US-006: Implement logout functionality

---

## Dependency Ordering

Stories execute in `priority` order. **Dependencies must come first.**

### Correct Order Example

```json
{
  "userStories": [
    {
      "id": "US-001",
      "title": "Add notifications table",
      "priority": 1 // ← Database schema first
    },
    {
      "id": "US-002",
      "title": "Create notification service",
      "priority": 2 // ← Backend logic second
    },
    {
      "id": "US-003",
      "title": "Add notification bell icon",
      "priority": 3 // ← UI last
    }
  ]
}
```

### ❌ Wrong Order

```json
{
  "userStories": [
    {
      "id": "US-001",
      "title": "Add notification bell icon",
      "priority": 1 // ← Can't work without backend!
    },
    {
      "id": "US-002",
      "title": "Add notifications table",
      "priority": 2 // ← Should be first
    }
  ]
}
```

---

## Verification Criteria

### Always Included

Every story automatically gets:

```json
"acceptanceCriteria": [
  "... your specific criteria ...",
  "Typecheck passes"  // ← Always added
]
```

### For UI Stories

Stories that modify the interface get:

```json
"acceptanceCriteria": [
  "... your specific criteria ...",
  "Typecheck passes",
  "Verify in browser using dev-browser skill"  // ← For visual confirmation
]
```

### For Logic Stories

Stories with testable logic get:

```json
"acceptanceCriteria": [
  "... your specific criteria ...",
  "Tests pass",
  "Typecheck passes"
]
```

---

## Archiving Previous Work

When converting a new feature, the skill automatically archives previous work:

### Automatic Archiving

```bash
# You have: tasks/prd.json (feature A)
# You run: "Convert prd-feature-b.md to prd.json"

# Skill automatically:
1. Detects different branchName
2. Creates: tasks/archive/2026-01-10-feature-a/
3. Moves old prd.json to archive
4. Creates new prd.json for feature B
```

### Manual Archive Check

```bash
"Show me archived prd.json files"
```

---

## Tracking Progress

### Marking Stories Complete

After implementing a story:

```bash
"Mark US-001 as complete in prd.json"
```

**Updates:**

```json
{
  "id": "US-001",
  "passes": true, // ← Changed from false
  "notes": "Used Laravel validation rules for email" // ← Added
}
```

### Checking Progress

```bash
"How many stories are complete in prd.json?"

"Show me incomplete stories"
```

---

## Usage Patterns

### Pattern 1: Standard Workflow

```bash
# 1. Create PRD
"Create a PRD for dark mode support"

# 2. Convert to JSON
"Convert tasks/prd-dark-mode-support.md to prd.json"

# 3. Implement story by story
"Implement US-001 from prd.json"
"Implement US-002 from prd.json"
...

# 4. Mark complete
"Mark US-001 as complete"
```

### Pattern 2: Quick Feature

```bash
# Convert feature description directly to JSON
"Convert this feature to prd.json: Add sorting to the tasks list (name, date, priority)"
```

### Pattern 3: Story Review

```bash
# Convert and review before implementation
"Convert tasks/prd-api-refactor.md to prd.json"
"Review the story sizes in prd.json - are any too large?"
"Split US-003 into smaller stories"
```

---

## Integration Examples

### With Compound Engineering

```bash
# 1. Convert PRD to JSON
"Convert tasks/prd-notifications.md to prd.json"

# 2. Execute with compound engineering
"/compound-engineering:work tasks/prd.json"
```

### With Dev Browser

```bash
# UI stories automatically include browser verification
# After implementing UI story:
"Use dev-browser to verify US-003 (notification bell icon)"
```

### With Both Skills

```bash
# Complete workflow
"Create a PRD for payment integration"           # ralph-prd-generator
"Convert tasks/prd-payment-integration.md to prd.json"  # ralph-json-converter
"Implement US-001 from prd.json"                 # You or compound engineering
```

---

## Common Issues & Solutions

### Issue: Stories Too Large

**Problem:** JSON has stories that are too big

**Solution:**

```bash
"Review prd.json and split any stories that are too large"
```

### Issue: Wrong Dependency Order

**Problem:** UI story comes before backend

**Solution:**

```bash
"Reorder stories in prd.json to put dependencies first"
```

### Issue: Missing Verification

**Problem:** UI story missing browser verification

**Solution:**
The skill automatically adds it, but if missing:

```bash
"Add browser verification to all UI stories in prd.json"
```

### Issue: Previous Work Not Archived

**Problem:** Old prd.json still present

**Solution:**

```bash
"Archive the current prd.json before converting the new PRD"
```

---

## Advanced Usage

### Custom Story Ordering

```bash
"Convert tasks/prd-dashboard.md to prd.json but prioritize backend stories first"
```

### Story Filtering

```bash
"Create prd.json with only the backend stories from tasks/prd-full-feature.md"
```

### Batch Processing

```bash
"Convert all PRD files in tasks/ to individual prd-*.json files"
```

---

## Best Practices

### 1. One Feature at a Time

Keep one active `prd.json` at a time. Archive when switching features.

### 2. Review Before Implementing

```bash
"Show me prd.json and verify story sizes and order"
```

### 3. Update as You Go

Mark stories complete and add notes immediately after implementation.

### 4. Use Verification

Always run browser verification for UI stories.

### 5. Keep PRD Source

Don't delete the original PRD markdown - keep it for reference.

---

## File Organization

### Recommended Structure

```
tasks/
├── prd-feature-a.md          # Source PRD (keep)
├── prd-feature-b.md          # Source PRD (keep)
├── prd.json                  # Active JSON (current feature)
└── archive/
    ├── 2026-01-09-feature-a/
    │   └── prd.json
    └── 2026-01-08-dashboard/
        └── prd.json
```

---

## Cost Savings with Haiku

**Per conversion** (typical PRD → JSON):

| Model     | Input  | Output | Total      |
| --------- | ------ | ------ | ---------- |
| **Haiku** | $0.002 | $0.025 | **~$0.03** |
| Sonnet    | $0.010 | $0.135 | ~$0.15     |
| Opus      | $0.050 | $0.225 | ~$0.30     |

**Annual savings** (100 conversions): $27 with Haiku vs $270 with Opus!

---

## Tips for Success

### 1. Start with Good PRDs

Use ralph-prd-generator for consistent PRD format that converts cleanly.

### 2. Review Story Sizes

Before implementing, check if stories are right-sized.

### 3. Follow Dependencies

Always implement in priority order - don't skip ahead.

### 4. Track Progress

Keep prd.json updated with completion status and notes.

### 5. Archive Regularly

Don't lose previous work - let the skill archive automatically.

---

## Example Session

```bash
You: "Create a PRD for adding comments to tasks"
Claude: [Creates tasks/prd-task-comments.md]

You: "Convert tasks/prd-task-comments.md to prd.json"
Claude: ✓ Archived previous prd.json to tasks/archive/2026-01-10-notifications/
        ✓ Created new prd.json with 5 user stories
        ✓ Stories ordered: Schema → Backend → UI

You: "Show me US-001"
Claude: [Shows first story details]

You: "Implement US-001"
Claude: [Implements database schema]

You: "Mark US-001 complete with note: Used foreign key constraints"
Claude: ✓ Updated prd.json - US-001 marked complete

You: "How many stories remain?"
Claude: 4 stories remaining (US-002 through US-005)
```

---

## Summary

**Installation:**

1. Create `.claude/skills/ralph-json-converter/`
2. Copy SKILL.md
3. Ensure `tasks/` directory exists

**Usage:**

```bash
# Convert PRD to JSON
"Convert tasks/prd-[feature].md to prd.json"

# Or from text
"Convert this PRD to prd.json: [paste]"
```

**Output:**

- Executable JSON at `tasks/prd.json`
- Previous versions archived
- Ready for systematic implementation

**Benefits:**

- ✅ Cost-effective with Haiku
- ✅ Proper story sizing
- ✅ Dependency ordering
- ✅ Automatic verification criteria
- ✅ Progress tracking built-in

Ready to convert your first PRD! 🚀
