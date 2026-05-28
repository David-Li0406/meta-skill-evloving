# Workflow: Validate Workspace

This workflow checks the `.claude/` workspace structure and identifies issues.

---

## Step 1: Check Directory Structure

Verify these directories exist:

```
.claude/
├── plans/
├── architecture/
├── examples/
├── research/
└── analysis/
```

**For each missing directory:**
- Log: "Missing directory: .claude/{category}/"
- Add to auto-fix list

---

## Step 2: Check INDEX.md Files

For each category directory that exists:

1. Check if INDEX.md exists
2. If missing, log: "Missing INDEX.md in .claude/{category}/"
3. Add to auto-fix list

---

## Step 3: Validate Each File

For each `.md` file (excluding INDEX.md) in each category:

### 3a. Frontmatter Validation

Check YAML frontmatter:
- [ ] Has YAML frontmatter (content between `---` markers)
- [ ] Has `title` field
- [ ] Has `category` field matching directory
- [ ] Has `created` date in YYYY-MM-DD format
- [ ] Has `updated` date in YYYY-MM-DD format
- [ ] Has `author` field
- [ ] Has category-specific required fields (see [frontmatter-schemas.md](../references/frontmatter-schemas.md))
- [ ] Status values are valid enums for the category

**Log issues:**
```
{filename}: Missing required field 'title'
{filename}: Invalid status 'wip' - must be one of [draft, in-progress, approved, implemented, superseded]
{filename}: Category 'plan' doesn't match directory 'plans'
```

### 3b. Cross-Reference Validation

Check cross-references:
- [ ] Has `## Related` section
- [ ] Has `### Codebase` subsection under Related
- [ ] At least one codebase link present
- [ ] Codebase links use markdown format `[name](path)`
- [ ] Codebase link targets exist in repository

**Log issues:**
```
{filename}: Missing '## Related' section
{filename}: Missing '### Codebase' subsection
{filename}: No codebase links found (at least one required)
{filename}: Broken link - ../../app/models/user.rb does not exist
```

### 3c. Naming Validation

Check filename:
- [ ] Follows `YYYY-MM-DD-description.md` pattern
- [ ] Date is valid
- [ ] Description is kebab-case
- [ ] No special characters except hyphens

**Log issues:**
```
{filename}: Doesn't follow naming convention YYYY-MM-DD-description.md
{filename}: Invalid date '2025-13-45'
{filename}: Description should be kebab-case, found 'User_Auth'
```

---

## Step 4: Check INDEX Accuracy

For each INDEX.md:

- [ ] Lists all files in directory
- [ ] No entries for non-existent files
- [ ] `file_count` matches actual file count
- [ ] Status groupings are accurate

**Log issues:**
```
{category}/INDEX.md: Missing entry for '2025-01-07-new-file.md'
{category}/INDEX.md: Lists non-existent file '2025-01-07-deleted-file.md'
{category}/INDEX.md: file_count is 3 but directory has 5 files
```

---

## Step 5: Generate Report

```
═══════════════════════════════════════════════════
        Workspace Validation Report
═══════════════════════════════════════════════════

Directories
───────────────────────────────────────────────────
✓ .claude/plans/
✓ .claude/architecture/
✗ .claude/examples/          (missing)
✓ .claude/research/
✓ .claude/analysis/

INDEX Files
───────────────────────────────────────────────────
✓ plans/INDEX.md
✓ architecture/INDEX.md
✗ examples/INDEX.md          (missing - directory missing)
✗ research/INDEX.md          (missing)
✓ analysis/INDEX.md

Files Validated
───────────────────────────────────────────────────
Total: 15 files
Valid: 12 files
Issues: 3 files

Issues Found
───────────────────────────────────────────────────
plans/2025-01-07-auth-migration.md:
  ✗ Missing codebase links in '## Related' section

architecture/2025-01-05-old-design.md:
  ✗ Invalid status 'wip' - must be: proposed, accepted, deprecated, superseded
  ✗ Broken link: ../../app/models/widget.rb (file not found)

research/notes.md:
  ✗ Filename doesn't follow YYYY-MM-DD-description.md pattern
  ✗ Missing YAML frontmatter

INDEX Accuracy
───────────────────────────────────────────────────
✗ plans/INDEX.md: file_count mismatch (says 4, has 5)
✗ analysis/INDEX.md: missing entry for 2025-01-07-perf-audit.md

═══════════════════════════════════════════════════
        Summary: 8 issues found
═══════════════════════════════════════════════════
```

---

## Step 6: Auto-Fix Options

Present fixable issues:

```
Auto-fix available for these issues:

Directories & INDEX files:
  [1] Create missing .claude/examples/ directory
  [2] Create missing .claude/examples/INDEX.md
  [3] Create missing .claude/research/INDEX.md

INDEX accuracy:
  [4] Update plans/INDEX.md with correct file_count
  [5] Add missing entry to analysis/INDEX.md

Manual fix required:
  - plans/2025-01-07-auth-migration.md: Add codebase links
  - architecture/2025-01-05-old-design.md: Fix status value
  - architecture/2025-01-05-old-design.md: Fix broken link
  - research/notes.md: Rename and add frontmatter

Options:
  a) Auto-fix all (1-5)
  b) Select specific fixes
  c) Skip auto-fix
  d) View detailed instructions for manual fixes

Choose (a/b/c/d): _
```

---

## Step 7: Execute Auto-Fixes

If user chooses to auto-fix:

### Create missing directories
```bash
mkdir -p .claude/{category}
```

### Create missing INDEX.md
Use [index-template.md](../templates/index-template.md) with `file_count: 0`

### Update INDEX.md accuracy
Run [update-index.md](./update-index.md) workflow for affected categories

---

## Step 8: Manual Fix Instructions

For issues requiring manual intervention:

```
Manual Fix Instructions
═══════════════════════════════════════════════════

plans/2025-01-07-auth-migration.md - Missing codebase links
───────────────────────────────────────────────────
Add a '## Related' section with codebase links:

  ## Related

  ### Codebase
  - [user.rb](../../app/models/user.rb) - User model for auth

  ### Related Documentation
  - (add if related docs exist)

───────────────────────────────────────────────────

research/notes.md - Naming and frontmatter issues
───────────────────────────────────────────────────
1. Rename file to follow convention:
   mv .claude/research/notes.md .claude/research/2025-01-07-{topic}.md

2. Add YAML frontmatter at the beginning:
   ---
   title: {Title}
   category: research
   status: in-progress
   created: 2025-01-07
   updated: 2025-01-07
   author: Claude
   tags: []
   sources: []
   ---

───────────────────────────────────────────────────
```

---

## Step 9: Confirmation

After fixes applied:

```
Validation complete.

Auto-fixes applied: 5
Manual fixes needed: 4

Re-run validation to verify fixes? (y/n)
```

If re-run requested, go back to Step 1.
