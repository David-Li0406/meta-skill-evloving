---
name: bootstrap
description: Generate feature plan with codebase-aware context
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

# Bootstrap

Generate a feature plan with codebase-aware context. This skill scans your codebase, understands existing patterns, and creates a targeted feature specification and execution plan.

## When to Use

- Starting a new feature in an existing codebase
- You have a clear idea of what to build
- You want to skip the full product/technical spec workflow
- You ran `/adopt` from the orchestrator and saved context

## Instructions

### Step 1: Gather Initial Description

**Check for existing context first:**
```bash
cat .claude/bootstrap-context.md 2>/dev/null
```

**If bootstrap-context.md exists:**
- Read the content
- Show a summary: "I found saved context from your previous session:"
- Ask: "Should I use this context, or would you like to provide something different?"

**If no saved context, or user wants something different:**

Ask the user:
```
What would you like to build?

Provide a brief description (1-2 sentences for simple features) or a detailed
description if you have specific requirements.
```

Store the response as `USER_DESCRIPTION`.

### Step 2: Orient to Project Root

Find the project root:

1. Check if current directory is a git repository:
   ```bash
   git rev-parse --show-toplevel 2>/dev/null
   ```

2. If not a git repo, search up for AGENTS.md:
   ```bash
   # Start from current directory and search upward
   dir="$(pwd)"
   while [[ "$dir" != "/" ]]; do
     if [[ -f "$dir/AGENTS.md" ]]; then
       echo "$dir"
       break
     fi
     dir="$(dirname "$dir")"
   done
   ```

3. If neither found, use current directory as PROJECT_ROOT

Store result as `PROJECT_ROOT`. Report to user:
```
Project root: {PROJECT_ROOT}
```

### Step 3: Run /setup Automatically

Ensure the toolkit is installed in the project:

1. Determine toolkit location:
   - Check if we're running from the toolkit (GENERATOR_PROMPT.md exists in cwd)
   - If not, resolve from `.claude/toolkit-version.json` or common paths

2. Run `/setup PROJECT_ROOT` (idempotent — safe to run multiple times)
   - If toolkit already installed and current, setup will report "Already up to date"
   - If toolkit needs updating, setup will perform incremental sync
   - If toolkit not installed, setup will perform full installation

3. Continue after setup completes (no user interaction needed for idempotent runs)

### Step 4: Codebase Scan

Scan the codebase to understand its structure and patterns, **guided by USER_DESCRIPTION**.

**4.1 Directory Structure**

List top-level directories and key locations:
```bash
ls -la PROJECT_ROOT
ls PROJECT_ROOT/src PROJECT_ROOT/lib PROJECT_ROOT/app 2>/dev/null
```

Note the primary source directory structure.

**4.2 Technology Detection**

Check for project configuration files:
```bash
ls PROJECT_ROOT/package.json PROJECT_ROOT/requirements.txt PROJECT_ROOT/go.mod \
   PROJECT_ROOT/Cargo.toml PROJECT_ROOT/pyproject.toml PROJECT_ROOT/composer.json \
   PROJECT_ROOT/Gemfile PROJECT_ROOT/pom.xml PROJECT_ROOT/build.gradle 2>/dev/null
```

If found, read the main config file to extract:
- Language/runtime version
- Key dependencies
- Framework being used
- Build/test commands

**4.3 Pattern Discovery (Informed by USER_DESCRIPTION)**

Search for code related to what the user wants to build:

```bash
# Search for keywords from USER_DESCRIPTION
grep -r "{keywords}" PROJECT_ROOT/src --include="*.{ext}" -l | head -10
```

For each relevant file found:
- Read the file to understand patterns
- Note naming conventions
- Note file organization patterns
- Note testing approach (if test files found)

Look for patterns that should be followed:
- Component structure (if UI)
- API route patterns (if backend)
- Database access patterns
- Error handling patterns
- Logging patterns

**4.4 Read Context Documents**

Read available context files:

```bash
# Required
cat PROJECT_ROOT/AGENTS.md

# Optional (if exist)
cat PROJECT_ROOT/LEARNINGS.md 2>/dev/null
cat PROJECT_ROOT/TECHNICAL_SPEC.md 2>/dev/null
cat PROJECT_ROOT/PRODUCT_SPEC.md 2>/dev/null
```

**4.5 Compile Codebase Context**

Summarize findings as `CODEBASE_CONTEXT`:
```
CODEBASE CONTEXT
================
Language/Framework: {detected}
Primary source: {src directory}

Patterns to follow:
- {pattern 1 with file reference}
- {pattern 2 with file reference}

Related existing code:
- {file}: {what it does, relevance to feature}

Testing approach: {how tests are structured}
```

### Step 5: Check for Unfinished Execution Plans

Look for existing execution plans that might be incomplete:

```bash
# Find all execution plans
find PROJECT_ROOT -name "EXECUTION_PLAN.md" -type f
```

For each found plan:

1. Check if `.claude/phase-state.json` exists for completion status
2. If no state file, parse the plan for completion:
   - Count `- [x]` (completed) vs `- [ ]` (incomplete) criteria
   - A plan is incomplete if any criteria are unchecked

**If unfinished plans exist:**

Report to user:
```
UNFINISHED EXECUTION PLANS DETECTED
===================================
- EXECUTION_PLAN.md: Phase 2 of 4 (5/12 tasks complete)
- features/analytics/EXECUTION_PLAN.md: Phase 1 of 2 (3/8 tasks complete)
```

Ask with AskUserQuestion:
```
Question: "There are unfinished execution plans. How should I proceed?"
Options:
- "Continue anyway" — Create new feature plan alongside existing work
- "Add TODO reminder" — Add reminder to TODOS.md and continue
- "Cancel" — Stop bootstrap to focus on existing work
```

If "Add TODO reminder":
```bash
# Append to TODOS.md
echo "- [ ] [backlog] Complete unfinished execution plans before starting new work" >> PROJECT_ROOT/TODOS.md
```

If "Cancel": Stop and report existing plans that need attention.

### Step 6: Ask Clarifying Questions

Based on the codebase scan and USER_DESCRIPTION, identify gaps:

**What's clear** (from USER_DESCRIPTION and scan):
- Core functionality / what it does
- How it relates to existing code

**What might be missing:**
- Scope boundaries (what's NOT included)
- Edge cases / error handling approach
- Integration points with existing code
- Acceptance criteria for "done"

**If important gaps exist**, ask targeted questions. Keep it minimal — only ask what's necessary to create an actionable plan.

Example questions (informed by scan):
- "I see you have {existing pattern}. Should the new feature follow the same approach?"
- "Should this integrate with {related existing code}?"
- "What's the testing expectation — unit tests, integration tests, both?"

**Do NOT ask about:**
- Things clearly implied by USER_DESCRIPTION
- Implementation details you can decide based on codebase patterns
- Nice-to-haves that can be added later

If USER_DESCRIPTION is comprehensive and codebase patterns are clear, acknowledge and proceed without questions.

### Step 7: Derive and Confirm Feature Name

Derive a kebab-case name from USER_DESCRIPTION:

1. Extract key nouns/concepts from description
2. Create a short, descriptive name (2-4 words)
3. Convert to kebab-case (lowercase, hyphens)

Examples:
- "Add dark mode toggle" → `dark-mode`
- "User authentication with OAuth" → `oauth-auth`
- "Analytics dashboard for admin" → `admin-analytics`

Ask user to confirm:
```
Feature name: {derived-name}

Press enter to confirm, or type a different name:
```

Validate the name:
- Lowercase only
- Hyphens and underscores allowed
- No spaces or special characters
- No leading/trailing hyphens

Store as `FEATURE_NAME`.

### Step 8: Create Feature Directory and Documents

Create the feature directory structure:

```bash
mkdir -p PROJECT_ROOT/features/FEATURE_NAME
```

**Create FEATURE_SPEC.md:**

```markdown
# Feature: {FEATURE_NAME}

## Problem

{Extracted from USER_DESCRIPTION — what problem does this solve?}

## Solution

{Derived from USER_DESCRIPTION + codebase patterns — high-level approach}

## Codebase Context

### Patterns to Follow
{From CODEBASE_CONTEXT — specific patterns this feature should match}

### Related Code
{Files that will be modified or serve as templates}

### Integration Points
{How this connects to existing functionality}

## Scope

### In Scope
- {Core functionality items}

### Out of Scope
- {Explicitly excluded items}
- {Future enhancements that are NOT part of this work}

## Acceptance Criteria

### Functional
- [ ] {User-facing criterion}
- [ ] {User-facing criterion}

### Technical
- [ ] {Code quality criterion}
- [ ] Tests pass
- [ ] No new linting errors
```

**Create EXECUTION_PLAN.md:**

```markdown
# Execution Plan: {FEATURE_NAME}

## Overview

{2-3 sentence summary of what this accomplishes}

## Codebase Context

### Relevant Existing Code
{From scan — files that will be modified or referenced}

### Patterns to Follow
{Specific patterns from CODEBASE_CONTEXT with file references}

### Integration Points
{Where this feature connects to existing code}

## Phase 1: {Phase Name}

### Setup
- [ ] {Any prerequisite setup}

### Step 1.1: {Logical grouping}

#### Task 1.1.A: {Specific task}

{Brief description of what this task accomplishes}

**Files to modify:**
- `{file path}` — {what changes}

**Acceptance Criteria:**
- [ ] (CODE) {Testable code criterion}
- [ ] (TEST) {Test requirement}

#### Task 1.1.B: {Next task}
...

## Phase 2: {If needed}
...

## Out of Scope

- {Things explicitly not included — prevents scope creep}
```

**Guidelines for plan generation:**
- Use 1-3 phases for simple features, more for complex ones
- Each task should be completable in one focused session
- Reference specific files from codebase scan
- Acceptance criteria must be testable/verifiable
- Include codebase context so agents understand the existing patterns

### Step 9: Update CLAUDE.md

If CLAUDE.md exists but doesn't reference AGENTS.md, add the reference:

```bash
grep -q "AGENTS.md" PROJECT_ROOT/CLAUDE.md 2>/dev/null
```

If not found or CLAUDE.md doesn't exist, create/update:
```markdown
@AGENTS.md
```

### Step 10: Clean Up and Report

**If bootstrap-context.md was used**, offer to delete it:
```
The bootstrap context file is no longer needed. Delete it?
1. Yes (recommended)
2. No, keep it for reference
```

**Report success:**

```
FEATURE PLAN CREATED
====================
Feature: {FEATURE_NAME}
Location: PROJECT_ROOT/features/FEATURE_NAME/

Files created:
- FEATURE_SPEC.md — Feature requirements and scope
- EXECUTION_PLAN.md — {N} phases, {M} tasks

Codebase scan findings:
- Language: {detected}
- Related code: {count} files identified
- Patterns: {key patterns to follow}

Next steps:
1. Review the feature spec:
   cat PROJECT_ROOT/features/FEATURE_NAME/FEATURE_SPEC.md

2. Review the execution plan:
   cat PROJECT_ROOT/features/FEATURE_NAME/EXECUTION_PLAN.md

3. Start execution:
   cd PROJECT_ROOT/features/FEATURE_NAME
   /fresh-start
   /phase-start 1
```

## Example

**Input:** "Add a dark mode toggle to the settings page. It should persist the preference to localStorage and apply a dark class to the body element."

**Codebase scan finds:**
- React app in `src/`
- Settings page at `src/pages/Settings.tsx`
- Existing toggle component at `src/components/Toggle.tsx`
- CSS modules pattern used throughout

**Output:** A feature directory at `features/dark-mode/` with:

**FEATURE_SPEC.md** containing:
- Problem: Users want to reduce eye strain with dark mode
- Solution: Add toggle using existing Toggle component
- Patterns to follow: CSS modules, localStorage for persistence
- Related code: Settings.tsx, Toggle.tsx, existing CSS variables

**EXECUTION_PLAN.md** with phases:
1. Add dark mode CSS variables and styles
2. Add toggle to settings page with localStorage persistence
3. Apply dark mode class to body based on preference
4. Add tests for persistence and toggle behavior

Each task references the specific files to modify and patterns to follow.
