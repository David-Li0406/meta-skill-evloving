---
name: normalize
description: Validate files against prompt reference guidelines
argument-hint: [--autofix] [paths...]
---

# Normalize

## Overview

Validate that prompt files and plugin READMEs conform to the exact structure defined in the template files. Ensures all prompt files exactly match the structure, section names, and content requirements defined in their respective templates.

Templates used for validation:

- `docs/templates/agent-template.md` for agents
- `plugins/agentic-sdlc/skills/create-skill/template.md` for skills
- `docs/templates/readme-template.md` for plugin READMEs

All templates use Mustache/Handlebars-style placeholders (`{{placeholder_name}}`) with HTML comment instructions. See `CLAUDE.md` section "Prompt Template Convention" for complete details.

## Arguments

### Definitions

- **`[--autofix]`** (optional): Automatically modify files to make them compliant with the templates. Without this flag, only reports issues.
- **`[paths...]`** (optional): One or more paths to files or directories to validate. If omitted, validates all prompt files and READMEs in the repository.

### Values

\$ARGUMENTS

## Core Principles

- Always read the template file to determine validation rules
- Never hardcode template requirements in this command - defer to templates
- Templates are the single source of truth for structure and content
- Section names must match exactly (case-sensitive)
- Required sections are listed in the template header comment
- Optional sections are marked with "(optional)" in the template
- Report all issues with clear, actionable feedback
- Only modify files when `--autofix` flag is provided
- Preserve existing content and style when autofixing

## Instructions

1. **Determine Files to Validate**

   If paths are provided via `$ARGUMENTS`:
   - For each file path: validate that file directly
   - For each directory path: find all `.md` files within

   If no paths provided, use a two-pass discovery approach for reliability:

   **Pass 1: Gather all markdown files using broad patterns**
   - `plugins/**/*.md` - All markdown files in plugins
   - `.claude/skills/**/SKILL.md` - Repository-level skills

   **Pass 2: Filter and classify discovered files**
   - Exclude non-prompt files: `CHANGELOG.md`, `CLAUDE.example.md`, and similar
   - Classify remaining files based on path patterns (see step 2)

   **Verification**: After discovery, report the total count of files found. If zero files are found when no arguments provided, warn that something may be wrong with the search.

2. **Classify Each File and Load Template**

   Determine the file type by checking if the file path contains these directory patterns:

   | Path Contains           | Type   | Template to Read                                       |
   | ----------------------- | ------ | ------------------------------------------------------ |
   | `/agents/` or `agents`  | Agent  | `docs/templates/agent-template.md`                     |
   | `/skills/` or `skills`  | Skill  | `plugins/agentic-sdlc/skills/create-skill/template.md` |
   | `/hooks/` or `hooks`    | Hook   | (no template - skip validation)                        |
   | Filename is `README.md` | README | `docs/templates/readme-template.md`                    |

   **Classification rules:**
   - Check path segments, not substrings (e.g., `/agents/` not just `agent`)
   - README.md files in plugin roots are validated; README.md in subdirectories are skipped
   - Files like CHANGELOG.md, CLAUDE.example.md are skipped (not prompts)
   - If a file cannot be classified, skip it and note in the report

3. **Parse Template Structure**

   Read the template file and extract:
   - **Header comment**: Contains REQUIRED SECTIONS, OPTIONAL SECTIONS, and SECTION ORDER
   - **Frontmatter fields**: Parse the `---` block to identify required fields
   - **Section names**: Extract all `## Section Name` headings
   - **Section order**: Note the order sections appear in the template
   - **Optional markers**: Sections with "(optional)" in their heading

4. **Validate Frontmatter**

   For prompt files (agents, skills):
   - Parse the YAML frontmatter from the file being validated
   - Compare against frontmatter fields defined in the template
   - Validate:
     - All required fields are present
     - `name` field uses kebab-case
     - `description` is a one-line description (under 100 characters recommended)
     - Field values match expected formats from template

   For README files:
   - READMEs do not have frontmatter - skip this step

5. **Validate Section Structure**

   Compare the file's sections against the template:
   - Extract all `##` level headings from the file
   - Compare against required sections from template header comment
   - Check for:
     - Missing required sections
     - Misspelled or incorrectly capitalized section names
     - Sections in wrong order (compared to template order)
     - Unexpected sections not in template

   For README files, also check:
   - Prompt sections (Commands, Agents, Skills, Hooks) are only present if plugin has those prompts
   - Optional sections are only present when applicable (per template instructions)

6. **Validate Section Content**

   Based on template HTML comments, validate content patterns:
   - Check character encoding (code files: ASCII only; markdown files: ASCII plus minimal functional emojis allowed)
   - Verify `{{placeholders}}` are replaced with actual values
   - Verify HTML comments from template are removed

7. **Apply Autofix (if `--autofix` flag is present)**

   When `--autofix` is specified:

   **Frontmatter fixes:**
   - Add missing frontmatter block if absent
   - Add missing required fields with sensible defaults derived from:
     - `name`: Derive from filename (convert to kebab-case)
     - `description`: Use first paragraph or heading as basis
     - Other fields: Use defaults from template examples

   **Structure fixes:**
   - Add missing required sections by copying placeholder from template
   - Insert sections in the correct order as defined in template
   - Mark added sections with `<!-- TODO: Fill in this section -->` comments
   - Rename incorrectly capitalized sections to match template exactly

   **Content fixes:**
   - Convert non-kebab-case names to kebab-case in frontmatter
   - Replace non-ASCII characters with ASCII equivalents
   - Preserve all existing content

   **Autofix principles:**
   - Always read both the file and the template before modifying
   - Preserve all existing content
   - Report each modification made

8. **Generate Report**

   For each file, report:
   - File path and detected type
   - Template being validated against
   - List of issues found (if any):
     - Missing frontmatter fields
     - Missing required sections
     - Section name mismatches
     - Sections in wrong order
     - Content format issues
   - Suggested fixes (validate-only mode) or modifications applied (autofix mode)

   Summary at end:
   - Total files checked
   - Files passing validation
   - Files with issues (by category)
   - Files modified (if autofix enabled)

## Output Guidance

### Validate-only mode (default)

```markdown
## Validation Results

### File Discovery

- Files found: 35
- Agents: 2
- Skills: 31
- READMEs: 2
- Skipped (non-prompt): 3 (CHANGELOG.md, CLAUDE.example.md, etc.)

### path/to/skill/SKILL.md (Skill)

Template: plugins/agentic-sdlc/skills/create-skill/template.md

**Frontmatter:**

- [PASS] All required fields present
- [PASS] name is kebab-case

**Structure:**

- [FAIL] Missing required section: "Output Guidance"
  Suggestion: Add section after "Instructions" section
- [FAIL] Section name mismatch: "## arguments" should be "## Arguments"

**Content:**

- [PASS] Instructions section uses numbered list
- [WARN] Description is 105 characters (recommended: under 100)

### plugins/my-plugin/README.md (README)

Template: docs/templates/readme-template.md

**Structure:**

- [PASS] All required sections present
- [WARN] "Agents" section present but plugin has no agents/ directory

## Summary

- Files checked: 32
- Passing: 29
- With issues: 3
```

### Autofix mode (`--autofix`)

```markdown
## Autofix Results

### File Discovery

- Files found: 35
- Agents: 2, Skills: 31, READMEs: 2
- Skipped: 3

### path/to/skill/SKILL.md (Skill)

Template: plugins/agentic-sdlc/skills/create-skill/template.md

- [FIXED] Added missing section: "Output Guidance"
- [FIXED] Renamed section: "## arguments" -> "## Arguments"
- [INFO] Preserved all existing content

## Summary

- Files checked: 35
- Files modified: 2
- Issues auto-fixed: 4
- Files now passing: 34
```

If all files pass validation:

```markdown
## Validation Results

### File Discovery

- Files found: 35
- Agents: 2, Skills: 31, READMEs: 2
- Skipped: 3

All 35 files pass validation - 100% compliant with templates.
```
