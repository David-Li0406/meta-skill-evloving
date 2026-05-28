---
name: Sync Specs from Session
description: This skill should be used when the user asks to "sync specs", "update specs from work", "record what we did", "add to speclan", "document implemented features", or wants to capture session work as SPECLAN specifications. Analyzes conversation context to identify implemented features and syncs with speclan directory.
version: 0.1.0
---

# Sync Specs from Session

Analyze the current session context to identify implemented features, compare with existing SPECLAN specifications, and create or update specs based on user confirmation.

## When to Use

- After completing implementation work and wanting to document it
- When user asks to sync or update specs based on recent work
- To capture newly implemented functionality in SPECLAN format

## Workflow Overview

```
1. Analyze Session → 2. Scan Speclan → 3. Compare & Diff → 4. Ask User → 5. Apply Changes
```

## Step 1: Analyze Session Context

Review the conversation history to identify:

### 1.1 Code Changes Made

Look for patterns indicating implementation:
- Files created or modified (Write/Edit tool usage)
- Functions, classes, or components added
- API endpoints implemented
- Database schema changes
- Configuration updates

### 1.2 Extract Feature Information

For each identified change, extract:

```yaml
feature_candidate:
  title: "<descriptive name>"
  description: "<what it does and why>"
  code_paths: ["<files involved>"]
  type: "new" | "enhancement" | "bugfix"
  scope: "feature" | "requirement" | "both"
```

### 1.3 Categorize Changes

Group related changes into logical features:
- Multiple file changes for one feature = single feature
- Independent changes = separate features
- Small fixes to existing features = requirement updates

## Step 2: Scan Speclan Directory

### 2.1 Detect Speclan Location

```bash
# Check common locations
if [ -d "speclan" ]; then
  SPECLAN_DIR="speclan"
elif [ -d "specs/speclan" ]; then
  SPECLAN_DIR="specs/speclan"
else
  # No speclan directory - all features are new
  SPECLAN_DIR=""
fi
```

### 2.2 Index Existing Specs

If speclan directory exists, build an index:

```bash
# List all features
find "$SPECLAN_DIR/features" -name "F-*.md" -type f 2>/dev/null

# Extract titles and paths
for f in $(find "$SPECLAN_DIR/features" -name "F-*.md" -type f); do
  id=$(grep "^id:" "$f" | head -1 | cut -d: -f2 | tr -d ' ')
  title=$(grep "^title:" "$f" | head -1 | cut -d: -f2-)
  echo "$id|$title|$f"
done
```

### 2.3 Build Existing Spec Map

Create a mapping of:
- Feature ID → Title → File path
- Feature ID → Code paths mentioned (from `## Scope` or similar sections)
- Feature ID → Status (for edit rules)

## Step 3: Compare and Generate Diff

### 3.1 Match Session Work to Existing Specs

For each feature candidate from session:

1. **Title similarity check**: Compare with existing feature titles
2. **Code path overlap**: Check if code_paths match existing features
3. **Description similarity**: Semantic comparison of purpose

### 3.2 Classify Each Change

| Session Feature | Existing Spec | Classification |
|-----------------|---------------|----------------|
| New code paths | No match | **CREATE** new feature |
| Same code paths | Match found, status editable | **UPDATE** existing feature |
| Same code paths | Match found, status locked | **CHANGE_REQUEST** needed |
| Enhancement | Partial match | **ADD_REQUIREMENT** to feature |

### 3.3 Prepare Change Summary

Build a structured summary:

```yaml
changes:
  create:
    - title: "User Authentication"
      description: "JWT-based auth with refresh tokens"
      code_paths: ["src/auth/", "src/middleware/auth.ts"]

  update:
    - id: "F-1142"
      title: "Pet Management"
      changes: "Added bulk import functionality"
      code_paths: ["src/pets/import.ts"]

  change_requests:
    - parent_id: "F-1089"
      title: "Add Export Feature"
      reason: "Feature is in-development status"

  requirements:
    - feature_id: "F-1142"
      title: "Validate CSV format on import"
      code_paths: ["src/pets/validators/csv.ts"]
```

## Step 4: Ask User for Confirmation

Present the identified changes to the user using AskUserQuestion or direct prompting.

### 4.1 Summary Format

```markdown
## Identified Changes from Session

Based on our session, I identified the following potential spec updates:

### New Features to Create
1. **User Authentication** - JWT-based auth with refresh tokens

### Existing Features to Update
1. **F-1142 Pet Management** - Add bulk import functionality
   - Current status: draft (editable)

### Change Requests Needed
1. **F-1089 Data Export** - Feature is locked (in-development)
   - Proposed: Add CSV export option

### New Requirements
1. For **F-1142**: Validate CSV format on import
```

Note: Code paths are used internally to match session work to existing specs, but are NOT included in the specs themselves.

### 4.2 Ask for User Selection

Use AskUserQuestion to let user choose:

```yaml
questions:
  - question: "Which changes would you like to apply to specs?"
    header: "Apply"
    multiSelect: true
    options:
      - label: "Create: User Authentication"
        description: "New feature for JWT auth implementation"
      - label: "Update: F-1142 Pet Management"
        description: "Add bulk import to existing feature"
      - label: "CR for F-1089: Data Export"
        description: "Create change request for locked feature"
      - label: "Requirement for F-1142"
        description: "Add CSV validation requirement"
```

### 4.3 Handle User Response

- **Selected items**: Proceed to create/update
- **"Other" response**: User may provide custom instructions
- **No selection**: Skip spec updates

## Step 5: Apply Changes

### 5.1 Generate IDs

For new entities, generate collision-free IDs:

```bash
# Use the ID generator skill/script
FEATURE_ID=$(./skills/speclan-id-generator/scripts/generate-id.sh feature "$SPECLAN_DIR")
REQ_ID=$(./skills/speclan-id-generator/scripts/generate-id.sh requirement "$SPECLAN_DIR")
```

### 5.2 Create New Features

For each new feature:

1. **Create directory structure:**
   ```bash
   mkdir -p "$SPECLAN_DIR/features/F-####-slug"
   mkdir -p "$SPECLAN_DIR/features/F-####-slug/requirements"
   ```

2. **Write feature file** with YAML frontmatter:
   ```yaml
   ---
   id: F-####
   type: feature
   title: <Title>
   status: under-test
   owner: <from session or "Developer">
   created: "<ISO-8601>"
   updated: "<ISO-8601>"
   goals: []
   ---

   # <Title>

   ## Overview
   <Description from session analysis - focus on WHAT and WHY, not HOW>

   ## Scope
   <Bullet points of functionality - user-facing capabilities, not code details>
   ```

**IMPORTANT:** Specs must be implementation-agnostic. Do NOT include:
- Code paths or file names
- Implementation details or technical approach
- Code fragments or snippets
- Internal architecture details

Focus on WHAT the feature does for users, not HOW it's implemented.

### 5.3 Update Existing Features

For features with editable status (draft, review, approved):

1. **Read current file**
2. **Update relevant sections:**
   - Add new scope items
   - Update description if needed
   - Add implementation notes
3. **Update `updated` timestamp**
4. **Write file back**

### 5.4 Create Change Requests

For locked entities (features or requirements in-development, under-test, released):

1. **Generate CR ID:**
   ```bash
   CR_ID=$(./skills/speclan-id-generator/scripts/generate-id.sh change-request "$SPECLAN_DIR")
   ```

2. **Create CR file:**
   ```yaml
   ---
   id: CR-####
   type: changeRequest
   title: <Change title>
   status: pending
   owner: Developer
   created: "<ISO-8601>"
   updated: "<ISO-8601>"
   parentId: <F-#### or R-####>
   parentType: <feature or requirement>
   changeType: enhancement
   description: <Brief description>
   changes: |
     <Detailed change narrative from session>
   ---
   ```

3. **Place in correct location (adjacent to target entity):**
   ```
   # For features:
   speclan/features/F-####-slug/change-requests/CR-####-slug.md

   # For requirements:
   speclan/features/.../requirements/R-####-slug/change-requests/CR-####-slug.md
   ```

### 5.5 Create New Requirements

For requirements under existing features:

1. **Generate requirement ID**
2. **Create requirement directory structure:**
   ```bash
   mkdir -p "speclan/features/F-####-parent/requirements/R-####-slug"
   ```
3. **Write requirement file:**
   ```
   speclan/features/F-####-parent/requirements/R-####-slug/R-####-slug.md
   ```
4. **Update parent feature's `updated` timestamp**

## Step 6: Report Results

After applying changes, report:

```markdown
## Spec Sync Complete

### Created
- F-#### User Authentication (speclan/features/F-####-user-authentication/)
- R-#### CSV Validation (speclan/features/F-1142-pet-management/requirements/R-####-csv-validation/)

### Updated
- F-1142 Pet Management - added bulk import scope

### Change Requests Created
- CR-#### for F-1089 Data Export (speclan/features/F-1089-.../change-requests/)
- CR-#### for R-#### (speclan/.../requirements/R-####-.../change-requests/)

### Next Steps
- Review created specs for accuracy
- Assign goals to new features
- Process pending change requests
```

## Edge Cases

### No Speclan Directory

If speclan/ doesn't exist:
1. Ask user if they want to initialize it
2. If yes, create basic structure:
   ```bash
   mkdir -p speclan/goals speclan/features speclan/templates
   ```
3. Proceed with creating new features

### No Identifiable Features

If session has no clear feature work:
- Report: "No significant feature implementations detected in this session"
- Offer to manually describe what to document

### Ambiguous Matches

When a session feature could match multiple existing specs:
- Present options to user
- Let them choose the correct match or create new

## Integration with Other Skills

### SPECLAN Format
Reference for proper file structure and frontmatter fields.

### SPECLAN ID Generator
Use for collision-free ID generation.

### Spec Converter
If user also has speckit, consider syncing there too.
