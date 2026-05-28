---
name: compound-docs
description: Use this skill to capture solved problems as categorized documentation with YAML frontmatter for fast lookup.
---

# Skill body

**Purpose:** Automatically document solved problems to build searchable institutional knowledge with category-based organization.

## Overview

This skill captures problem solutions immediately after confirmation, creating structured documentation that serves as a searchable knowledge base for future sessions.

**Organization:** Each problem is documented as a single markdown file in its symptom category directory (e.g., `docs/solutions/performance-issues/n-plus-one-briefs.md`). Files use YAML frontmatter for metadata and searchability.

---

<critical_sequence name="documentation-capture" enforce_order="strict">

## 7-Step Process

<step number="1" required="true">
### Step 1: Detect Confirmation

**Auto-invoke after phrases:**

- "that worked"
- "it's fixed"
- "working now"
- "problem solved"
- "that did it"

**OR manual:** `/doc-fix` command

**Document when:**
- Multiple investigation attempts needed
- Tricky debugging that took time
- Non-obvious solution
- Future sessions would benefit

**Skip documentation for:**
- Simple typos
- Obvious syntax errors
- Trivial fixes immediately corrected
</step>

<step number="2" required="true" depends_on="1">
### Step 2: Gather Context

Extract from conversation history:

**Required information:**

- **Module name**: Which module had the problem
- **Symptom**: Observable error/behavior (exact error messages)
- **Investigation attempts**: What didn't work and why
- **Root cause**: Technical explanation of the actual problem
- **Solution**: What fixed it (code/config changes)
- **Prevention**: How to avoid in the future

**Environment details:**

- Rails version
- Stage (0-6 or post-implementation)
- OS version
- File/line references

**BLOCKING REQUIREMENT:** If critical context is missing (module name, exact error, stage, or resolution steps), ask the user and WAIT for a response before proceeding to Step 3:

```
I need a few details to document this properly:

1. Which module had this issue? [ModuleName]
2. What was the exact error message or symptom?
3. What were the investigation attempts?
```
</step>

<step number="3" required="true" depends_on="2">
### Step 3: Check Existing Docs

```bash
# Search for similar issues
grep -r "exact error phrase" docs/
ls docs/[category]/
```

**If similar found:** Present options:
1. Create new doc with cross-reference (recommended)
2. Update existing doc (only if same root cause)
3. Other

**If not found:** Proceed to Step 4.
</step>

<step number="4" required="true" depends_on="3">
### Step 4: Generate Filename

Format: `[sanitized-symptom]-[module]-[YYYYMMDD].md`

**Rules:**
- Lowercase, hyphens for spaces
- Remove special characters
- Truncate < 80 chars

**Examples:**
- `missing-import-auth-module-20251110.md`
- `n-plus-one-user-queries-UserService-20251110.md`
</step>

<step number="5" required="true" depends_on="4">
### Step 5: Validate YAML Schema

Validate against `schema.yaml`.

**Required fields:**
- module, date, problem_type, component
- symptoms (array 1-5), root_cause
- resolution_type, severity

**BLOCK if validation fails** - show errors, request corrections.
</step>

<step number="6" required="true" depends_on="5">
### Step 6: Create Documentation

```bash
CATEGORY="[mapped from problem_type]"
mkdir -p docs/${CATEGORY}
echo "---" > docs/${CATEGORY}/[filename].md
# Add YAML frontmatter and content here
```
</step>

<step number="7" required="true" depends_on="6">
### Step 7: Confirm Documentation Creation

Notify the user that the documentation has been created successfully.
</step>

</critical_sequence>