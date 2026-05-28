# Workflow: Migrate Existing Files

This workflow finds loose planning/architecture files in the repository and organizes them into the `.claude/` workspace.

---

## Step 1: Scan for Candidate Files

Search for files that might belong in `.claude/`:

```bash
# Plans and planning docs
find . -name "*plan*.md" -not -path "./.claude/*" -not -path "./node_modules/*"
find . -name "*roadmap*.md" -not -path "./.claude/*"
find . -name "*implementation*.md" -not -path "./.claude/*"

# Architecture docs
find . -name "*architecture*.md" -not -path "./.claude/*"
find . -name "*design*.md" -not -path "./.claude/*"
find . -name "*adr*.md" -not -path "./.claude/*"
find . -name "*decision*.md" -not -path "./.claude/*"

# Research and analysis
find . -name "*research*.md" -not -path "./.claude/*"
find . -name "*analysis*.md" -not -path "./.claude/*"
find . -name "*investigation*.md" -not -path "./.claude/*"
find . -name "*comparison*.md" -not -path "./.claude/*"

# Examples and patterns
find . -name "*example*.md" -not -path "./.claude/*" -not -path "./docs/*"
find . -name "*pattern*.md" -not -path "./.claude/*"
```

**Exclude from consideration:**
- Files in `docs/` (user-facing documentation)
- Files in `node_modules/`, `vendor/`, `.git/`
- README.md files
- CHANGELOG.md, CONTRIBUTING.md, LICENSE.md

---

## Step 2: Review Candidates

Present found files:

```
Found {n} potential files to migrate:

Plans (potential):
  1. [ ] ./specs/auth-implementation-plan.md
  2. [ ] ./notes/migration-roadmap.md

Architecture (potential):
  3. [ ] ./specs/api-design.md
  4. [ ] ./docs/decisions/use-postgres.md

Research (potential):
  5. [ ] ./notes/library-comparison.md

Analysis (potential):
  6. [ ] ./notes/performance-investigation.md

Examples (potential):
  (none found)

Options:
  a) Review each file and decide
  b) Migrate all to suggested categories
  c) Select specific files to migrate
  d) Cancel

Choose (a/b/c/d): _
```

---

## Step 3: Categorize Each File

For each file (if option 'a' selected):

```
File: ./specs/auth-implementation-plan.md
─────────────────────────────────────────

Preview (first 20 lines):
{file content preview}

Suggested category: plans
Reason: Contains "plan" in filename, content describes implementation steps

Options:
  1) Move to plans/ (suggested)
  2) Move to architecture/
  3) Move to examples/
  4) Move to research/
  5) Move to analysis/
  6) Skip (leave in place)
  7) Delete (file is obsolete)

Choose (1-7): _
```

---

## Step 4: Prepare Migration

For each file to migrate:

### 4a. Generate New Filename

```
Original: ./specs/auth-implementation-plan.md
New name: .claude/plans/2025-01-07-auth-implementation.md

(Date based on file modification date or today if creating new)
```

### 4b. Check/Add Frontmatter

**If file has YAML frontmatter:**
- Validate against category schema
- Update fields if needed
- Add missing required fields

**If file lacks frontmatter:**
- Generate frontmatter from file content
- Use filename for title
- Use file modification date for created/updated
- Set appropriate default status

### 4c. Check/Add Cross-References

**If file has Related section:**
- Validate codebase links exist
- Update paths for new location

**If file lacks Related section:**
```
File needs codebase links to migrate.

This file appears to relate to:
  - app/models/user.rb (mentioned in content)
  - app/controllers/sessions_controller.rb (mentioned in content)

Use these as codebase links? (y/n)
Or specify different files: _
```

---

## Step 5: Preview Changes

Show migration plan:

```
Migration Plan
═══════════════════════════════════════════════════

Files to migrate: 4

1. ./specs/auth-implementation-plan.md
   → .claude/plans/2025-01-07-auth-implementation.md
   Changes:
   - Add frontmatter (title, category, status, dates)
   - Add Related section with codebase links
   - Update relative paths in content

2. ./notes/library-comparison.md
   → .claude/research/2025-01-07-library-comparison.md
   Changes:
   - Update existing frontmatter (add missing fields)
   - Update Related section paths

3. ./specs/api-design.md
   → .claude/architecture/2025-01-07-api-design.md
   Changes:
   - Add frontmatter
   - Add Related section

4. ./notes/performance-investigation.md
   → .claude/analysis/2025-01-07-performance-investigation.md
   Changes:
   - Add frontmatter (type: performance)
   - Add Related section

───────────────────────────────────────────────────

Original files will be: [deleted / kept as backup]

Proceed with migration? (y/n)
```

---

## Step 6: Execute Migration

For each file:

1. **Create target directory** (if needed)
   ```bash
   mkdir -p .claude/{category}
   ```

2. **Read original file**

3. **Transform content:**
   - Add/update YAML frontmatter
   - Add/update Related section
   - Update any relative paths in content

4. **Write to new location**

5. **Handle original file:**
   - Option A: Delete original
   - Option B: Keep original (create copy)
   - Option C: Move (rename)

6. **Update any references** to old file path

---

## Step 7: Update INDEX Files

After all files migrated:

```bash
# Update each affected category's INDEX.md
```

Run [update-index.md](./update-index.md) for each category that received files.

---

## Step 8: Validation

Run validation on migrated files:

```
Validating migrated files...

✓ plans/2025-01-07-auth-implementation.md - Valid
✓ research/2025-01-07-library-comparison.md - Valid
✓ architecture/2025-01-07-api-design.md - Valid
✓ analysis/2025-01-07-performance-investigation.md - Valid

All migrated files are valid.
```

If validation fails, show issues and offer to fix.

---

## Step 9: Confirmation

```
Migration Complete
═══════════════════════════════════════════════════

Files migrated: 4
  - plans/: 1 file
  - architecture/: 1 file
  - research/: 1 file
  - analysis/: 1 file

INDEX files updated: 4

Original files: deleted

───────────────────────────────────────────────────

Note: If these files were referenced elsewhere in the codebase,
you may need to update those references.

Search for old references:
  grep -r "auth-implementation-plan" . --include="*.md"

───────────────────────────────────────────────────

What's next?
  1) Run validation to verify workspace
  2) Create new file
  3) Done
```

---

## Error Handling

### File already exists at target

```
Target file already exists:
  .claude/plans/2025-01-07-auth-implementation.md

Options:
  1) Overwrite existing file
  2) Use different name: 2025-01-07-auth-implementation-v2.md
  3) Skip this file
  4) Merge contents (manual review required)

Choose (1-4): _
```

### Cannot determine codebase links

```
Cannot find codebase links for: ./notes/random-notes.md

This file must link to at least one codebase file.

Options:
  1) Specify codebase files manually
  2) Skip this file (don't migrate)
  3) Create link to a general file (e.g., README.md)

Choose (1-3): _
```

### File has external dependencies

```
Warning: ./specs/api-design.md contains links to:
  - ../other-repo/shared-types.md (external)
  - https://external-docs.com/api (URL)

These links will need manual review after migration.

Continue? (y/n)
```
