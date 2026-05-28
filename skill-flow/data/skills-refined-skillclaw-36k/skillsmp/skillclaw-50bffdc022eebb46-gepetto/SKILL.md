---
name: gepetto
description: Use this skill when planning features that require thorough pre-implementation analysis through detailed, sectionized implementation plans.
---

# Gepetto

Orchestrates a multi-step planning process: Research → Interview → Spec Synthesis → Plan → External Review → Sections.

## CRITICAL: First Actions

**BEFORE anything else**, do these in order:

### 1. Print Intro

Print intro banner immediately:
```
═══════════════════════════════════════════════════════════════
GEPETTO: AI-Assisted Implementation Planning
═══════════════════════════════════════════════════════════════
Research → Interview → Spec Synthesis → Plan → External Review → Sections

Note: GEPETTO will write many .md files to the planning directory you pass it.
```

### 2. Validate Spec File Input

**Check if user provided @file at invocation AND it's a spec file (ends with `.md`).**

If NO @file was provided OR the path doesn't end with `.md`, output this and STOP:
```
═══════════════════════════════════════════════════════════════
GEPETTO: Spec File Required
═══════════════════════════════════════════════════════════════

This skill requires a markdown spec file path (must end with .md).
The planning directory is inferred from the spec file's parent directory.

To start a NEW plan:
  1. Create a markdown spec file describing what you want to build.
  2. It can be as detailed or as vague as you like.
  3. Place it in a directory where gepetto can save planning files.
  4. Run: /gepetto @path/to/your-spec.md

To RESUME an existing plan:
  1. Run: /gepetto @path/to/your-spec.md

Example: /gepetto @planning/my-feature-spec.md
═══════════════════════════════════════════════════════════════
```
**Do not continue. Wait for user to re-invoke with a .md file path.**

### 3. Setup Planning Session

Determine session state by checking existing files:

1. Set `planning_dir` = parent directory of the spec file.
2. Set `initial_file` = the spec file path.
3. Scan for existing planning files:
   - `claude-research.md`
   - `claude-interview.md`
   - `claude-spec.md`
   - `claude-plan.md`
   - `claude-integration-notes.md`
   - `claude-ralph-loop-prompt.md`
   - `claude-ralphy-prd.md`
   - `reviews/` directory
   - `sections/` directory

4. Determine mode and resume point:

| Files Found | Mode | Resume From |
|-------------|------|-------------|
| None | new | Step 4 |
| research only | resume | Step 6 (interview) |
| research + interview | resume | Step 7 (spec synthesis) |
| research + interview + spec | resume | Step 8 (plan) |
| research + interview + spec + plan | resume | Step 9 (external review) |
| all files present | resume | Step 10 (sections) |