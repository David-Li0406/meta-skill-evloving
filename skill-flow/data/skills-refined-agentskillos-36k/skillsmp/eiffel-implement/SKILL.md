---
name: eiffel-implement
description: Phase 4 of Eiffel Spec Kit. Writes feature bodies while keeping contracts FROZEN. Detects unauthorized contract changes. Use with /eiffel.implement command.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task
---

# /eiffel.implement - Phase 4: Implementation

**Purpose:** Write feature bodies that satisfy contracts. Contracts are FROZEN - no modifications allowed.

## Usage

```
/eiffel.implement <project-path>
```

## Project Scoping

```
<project-path>/
├── .eiffel-workflow/
│   ├── tasks.md (from Phase 3)
│   └── evidence/
│       ├── phase4-contracts-before.txt
│       ├── phase4-contracts-after.txt
│       └── phase4-compile.txt
├── src/*.e (implementation goes here)
```

## Prerequisites

- Phase 3 complete: `<project-path>/.eiffel-workflow/tasks.md` approved

## Critical Rule: CONTRACTS ARE FROZEN

**DO NOT modify require/ensure/invariant clauses.**

If implementation seems impossible without changing contracts:
1. STOP
2. Document why
3. Return to Phase 1 (/eiffel.contracts)
4. Re-run Phase 2 review after changes

## Workflow

### Step 1: Snapshot Contracts

```bash
grep -n "require\|ensure\|invariant" <project-path>/src/*.e > <project-path>/.eiffel-workflow/evidence/phase4-contracts-before.txt
```

### Step 2: Implement Tasks

For each task in tasks.md:
1. Read the feature contracts
2. Read the approach from approach.md
3. Write feature body between `do` and `ensure`
4. Compile after each feature

### Step 3: Compile After Each Task

**CRITICAL: You MUST cd to the project directory before compiling.** The EIFGENs folder is created in the current working directory, not where the ECF file is located. Compiling from the wrong directory pollutes other folders with build artifacts.

```bash
cd <project-path> && /d/prod/ec.sh -batch -config <project>.ecf -target <project>_tests -c_compile
```

**ZERO WARNINGS POLICY:** If the compiler reports obsolete call warnings or any other warnings, FIX THEM IMMEDIATELY. Do not note them and move on. Do not defer them. Fix them right now before proceeding. Common fixes:
- Obsolete `as_string_8`: Use explicit `{STRING_32} "literal"` manifest type or `.to_string_8`
- Obsolete feature calls: Replace with the suggested alternative in the warning message

### Step 4: Detect Contract Changes

```bash
grep -n "require\|ensure\|invariant" <project-path>/src/*.e > <project-path>/.eiffel-workflow/evidence/phase4-contracts-after.txt
diff <project-path>/.eiffel-workflow/evidence/phase4-contracts-before.txt <project-path>/.eiffel-workflow/evidence/phase4-contracts-after.txt
```

**If contracts changed:** STOP and notify human.

### Step 5: Save Evidence

Save to `<project-path>/.eiffel-workflow/evidence/phase4-compile.txt`:
```
# Phase 4 Implementation Evidence
# Project: <project-path>
# Date: [timestamp]

[Paste compilation output]

Contract changes detected: [yes/no]
# Status: PASS / FAIL
```

## Context Management (RLM Pattern)

This skill focuses ONLY on: `<project-path>`

**DO NOT:**
- Read files outside this project directory
- Load entire ecosystem or multiple libraries into context
- Keep large file contents in working memory

**DO:**
- Use Task tool with Explore agent for ecosystem questions
- Ask targeted questions when implementation needs external API details
- Release context after getting answers

**Example - Ecosystem Query:**
```
Need to call simple_json from your implementation? Don't read all its files.
Instead: Task(subagent_type=Explore) → "How do I serialize an object to JSON string with simple_json?"
```

The sub-agent searches, summarizes, and returns ONLY what you need. Your context stays focused on this project.

## Completion

```
Phase 4 COMPLETE: Implementation done.
Project: <project-path>

- All features implemented
- Contracts unchanged
- Compilation: PASS

Next: Run /eiffel.verify <project-path> to generate and run tests.
```
