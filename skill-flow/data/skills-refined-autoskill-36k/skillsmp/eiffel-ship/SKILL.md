---
name: eiffel-ship
description: Phase 7 of Eiffel Spec Kit. Final checklist - naming review, documentation, GitHub prep, ecosystem integration check. BLOCKS until human approves. Use with /eiffel.ship command.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task
---

# /eiffel.ship - Phase 7: Ship Checklist

**Purpose:** Final verification before release. Documentation, naming, ecosystem integration.

## Usage

```
/eiffel.ship <project-path>
```

## Project Scoping

```
<project-path>/
├── .eiffel-workflow/
│   ├── prompts/
│   │   └── phase7-checklist-review.md
│   └── evidence/
│       └── phase7-ship.txt
├── README.md
├── CHANGELOG.md
├── docs/
```

## Prerequisites

- Phase 6 complete: hardening passed

## Workflow

### Step 1: Naming Review

Check all public names against Eiffel conventions:
- Class names: UPPER_SNAKE_CASE
- Feature names: lower_snake_case
- Locals: l_prefix
- Arguments: a_prefix
- No abbreviations

### Step 2: Documentation Check

- [ ] README.md exists
- [ ] CHANGELOG.md exists
- [ ] All public features have header comments

### Step 3: Ecosystem Integration

- [ ] ECF references correct simple_* dependencies
- [ ] No ISE stdlib where simple_* exists
- [ ] SCOOP compatible
- [ ] Void safety enabled

### Step 4: Generate Checklist Review Prompt

Create `<project-path>/.eiffel-workflow/prompts/phase7-checklist-review.md`:

```markdown
# Ship Checklist Verification

## README Claims
[PASTE README.md]

## Actual Code
[PASTE summary of src/*.e features]

## Tests
[summary of test coverage]

## Verify:
- README claims match actual functionality
- No missing documentation
- Naming conventions followed
```

### Step 5: Final Compilation and Test

**CRITICAL: You MUST cd to the project directory before compiling.** The EIFGENs folder is created in the current working directory, not where the ECF file is located. Compiling from the wrong directory pollutes other folders with build artifacts.

```bash
cd <project-path> && /d/prod/ec.sh -batch -config <project>.ecf -target <project>_tests -c_compile
./EIFGENs/<project>_tests/W_code/<project>.exe
```

**ZERO WARNINGS POLICY:** The final release MUST have zero warnings. If the compiler reports obsolete call warnings or any other warnings, FIX THEM IMMEDIATELY before shipping.

### Step 6: Human Approval

**"Ship checklist complete. Ready to release?"**

**DO NOT mark complete until user explicitly approves.**

### Step 7: Save Evidence

Save to `<project-path>/.eiffel-workflow/evidence/phase7-ship.txt`:
```
# Phase 7 Ship Evidence
# Project: <project-path>
# Date: [timestamp]

Naming review: PASS/FAIL
Documentation: PASS/FAIL
Ecosystem: PASS/FAIL
Tests: PASS/FAIL

Human approved: [yes/no]

# Status: READY_TO_SHIP / NEEDS_WORK
```

## Context Management (RLM Pattern)

This skill focuses ONLY on: `<project-path>`

**DO NOT:**
- Read files outside this project directory
- Load entire ecosystem or multiple libraries into context
- Keep large file contents in working memory

**DO:**
- Use Task tool with Explore agent for ecosystem questions
- Ask targeted questions about ecosystem conventions for README/CHANGELOG
- Release context after getting answers

**Example - Ecosystem Query:**
```
Need to check ecosystem README conventions? Don't read all README files.
Instead: Task(subagent_type=Explore) → "What's the standard README structure for simple_* libraries?"
```

The sub-agent searches, summarizes, and returns ONLY what you need. Your context stays focused on this project.

## Completion

```
Phase 7 COMPLETE: Ready to ship.
Project: <project-path>

All phases complete:
✓ Phase 0: Intent
✓ Phase 1: Contracts
✓ Phase 2: Review
✓ Phase 3: Tasks
✓ Phase 4: Implement
✓ Phase 5: Verify
✓ Phase 6: Harden
✓ Phase 7: Ship

Library is ready for release.
```
