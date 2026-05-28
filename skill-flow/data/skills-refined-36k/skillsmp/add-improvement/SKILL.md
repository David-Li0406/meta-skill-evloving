---
name: add-improvement
description: Add a new improvement to the improvements tracking document
argument-hint: [--explore] <context>
---

# Add Improvement

## Overview

Add a new improvement entry to the improvements tracking document. This skill creates a structured improvement record with a unique ID, progress tracking checkbox, and detailed description section.

## Arguments

### Definitions

- **`[--explore]`** (optional): When set, analyze the codebase to add additional technical information to the improvement request. Defaults to `false`.
- **`<context>`** (required): Description of the improvement request. Can include problem description, affected areas, or desired outcome.

### Values

\$ARGUMENTS

## Configuration

The improvements document path is configured via `improvementsPath` in settings or defaults to `agentic/improvements.md`.

To override in `.claude/configs/agentic-sdlc.json`:

```json
{
  "improvementsPath": "custom/path/improvements.md"
}
```

## Core Principles

- Create the improvements document if it doesn't exist
- Generate unique improvement IDs using sequential numbering
- Keep improvement details concise (max 100 lines per entry)
- Preserve existing improvements when adding new ones
- Use consistent formatting matching existing entries
- Use existing ID prefixes when the improvement type is clear (SEC, DEBT, TEST, DOC)
- Improvement entries should be self-contained and actionable

## Instructions

1. **Determine File Path**
   - Check for `agentic-sdlc.improvementsPath` in settings
   - Default to `agentic/improvements.md` if not configured

2. **Check Document Existence**
   - If the document does not exist, create it with the template structure (see Templates section)
   - If it exists, read the current content

3. **Generate Improvement ID**
   - Scan existing entries to find the highest ID number
   - Generate next sequential ID in format `IMP-XXX` (e.g., `IMP-007`)
   - Use prefix based on context if clearly identifiable:
     - `SEC-XXX` for security-related improvements
     - `DEBT-XXX` for technical debt
     - `TEST-XXX` for testing improvements
     - `DOC-XXX` for documentation improvements
     - `IMP-XXX` for general improvements (default)

4. **Codebase Analysis** (if `--explore` is set)
   - Analyze the codebase to identify:
     - Relevant files and components affected
     - Existing patterns or implementations related to the improvement
     - Dependencies or impacts on other parts of the system
   - Include this technical context in the improvement details

5. **Create Improvement Entry**
   - Add checkbox entry to Progress Tracking section: `- [ ] ID: Short title`
   - Add detailed section to Improvements List with:
     - Status: Pending
     - Problem: Clear description of the issue or opportunity
     - Files to Investigate: Relevant file paths (if known or discovered via codebase exploration)
     - Expected Behavior / Goal: What the improvement should achieve
     - Acceptance Criteria: Measurable criteria for completion

6. **Write Updated Document**
   - Preserve all existing content
   - Insert new checkbox in Progress Tracking section (at the end of the list)
   - Append new details section to Improvements List

7. **Report Result**
   - Output confirmation with the new improvement ID
   - Show the improvement title and file path

## Output Guidance

Return a JSON object summarizing the action taken:

```json
{
  "success": true,
  "improvement_id": "{{improvement_id}}",
  "title": "{{title}}",
  "document_path": "{{document_path}}",
  "explored_codebase": "{{explored}}",
  "files_identified": ["{{files_array}}"]
}
```

<!--
Placeholders:
- {{improvement_id}}: Generated ID (e.g., IMP-007, SEC-003)
- {{title}}: Short descriptive title of the improvement
- {{document_path}}: Path to the improvements document
- {{explored}}: Boolean indicating if codebase exploration was performed
- {{files_array}}: Array of file paths identified during exploration (empty if not explored)
-->

## Templates

### New Document Template

When creating a new improvements document, use this structure:

```markdown
# Improvements

This file tracks improvement opportunities identified during code analysis. Each improvement has a checklist entry for progress tracking and a detailed section explaining the issue.

## How to Use This File

1. **Adding Improvements**: Add a checkbox to the Progress Tracking section (`- [ ] IMP-XXX: Short title`) and a corresponding details section with problem description, files to investigate, and acceptance criteria.
2. **Working on Improvements**: Mark the item as in-progress by keeping `[ ]` and update the Status in the details section to "In Progress".
3. **Completing Improvements**: Change `[ ]` to `[x]` and update the Status to "Completed".
4. **Implementation**: Use `/sdlc-plan` to create an implementation plan, then implement the changes.

## Progress Tracking

<!-- Add new items here -->

## Improvements List

List the details of every improvement request, 100 lines maximum per item.
```

### Improvement Entry Template

```markdown
---

### ID: Short descriptive title

**Status**: Pending

**Problem**: Clear description of the issue or opportunity.

**Files to Investigate**:

- `path/to/file.ts` - Brief note about relevance

**Expected Behavior / Goal**: What the improvement should achieve.

**Acceptance Criteria**:

- [ ] First measurable criterion
- [ ] Second measurable criterion
```

<!--
Template placeholders:
- ID: The generated improvement ID (e.g., IMP-007)
- Short descriptive title: Brief title describing the improvement
- Problem description: What issue needs to be addressed
- Files to Investigate: Relevant files (discovered via exploration or provided in context)
- Expected Behavior / Goal: Desired outcome
- Acceptance Criteria: Measurable completion criteria
-->
