---
name: eiffel-verify
description: Phase 5 of Eiffel Spec Kit. Generates test suite derived from contracts and runs tests. Includes AI chain coverage gap analysis. Use with /eiffel.verify command.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task
---

# /eiffel.verify - Phase 5: Test Generation and Verification

**Purpose:** Flesh out skeletal tests, generate contract-derived tests, verify all tests pass.

## Usage

```
/eiffel.verify <project-path>
```

## Project Scoping

```
<project-path>/
├── .eiffel-workflow/
│   ├── prompts/
│   │   └── phase5-coverage-review.md
│   └── evidence/
│       ├── phase5-tests.txt
│       └── phase5-coverage.txt
├── test/*.e (tests fleshed out here)
```

## Prerequisites

- Phase 4 complete: implementation compiles

## Workflow

### Step 1: Flesh Out Skeletal Tests

Complete tests created in Phase 1.

### Step 2: Generate Contract-Derived Tests

For each postcondition, ensure a test verifies it.

### Step 3: Generate Coverage Review Prompt

Create `<project-path>/.eiffel-workflow/prompts/phase5-coverage-review.md`:

```markdown
# Test Coverage Review

## Contracts
[PASTE src/*.e]

## Tests
[PASTE test/*.e]

## Check For:
- Postconditions without corresponding tests
- Edge cases not tested
- Precondition boundary tests missing
```

### Step 4: Compile and Run Tests (MANDATORY GATE)

**CRITICAL: You MUST cd to the project directory before compiling.** The EIFGENs folder is created in the current working directory, not where the ECF file is located. Compiling from the wrong directory pollutes other folders with build artifacts.

```bash
cd <project-path> && /d/prod/ec.sh -batch -config <project>.ecf -target <project>_tests -c_compile
./EIFGENs/<project>_tests/W_code/<project>.exe
```

**ZERO WARNINGS POLICY:** If the compiler reports obsolete call warnings or any other warnings, FIX THEM IMMEDIATELY. Do not note them and move on. Do not defer them. Fix them right now before proceeding.

**ALL TESTS MUST PASS.**

### Step 5: Save Evidence

Save to `<project-path>/.eiffel-workflow/evidence/phase5-tests.txt`:
```
# Phase 5 Test Evidence
# Project: <project-path>
# Date: [timestamp]

[Paste test output]

Tests run: [count]
Tests passed: [count]
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
- Ask targeted questions when tests need to understand external library behavior
- Release context after getting answers

**Example - Ecosystem Query:**
```
Need to understand how simple_testing assertions work? Don't read all its files.
Instead: Task(subagent_type=Explore) → "What assertions does EQA_TEST_SET provide?"
```

The sub-agent searches, summarizes, and returns ONLY what you need. Your context stays focused on this project.

## Completion

```
Phase 5 COMPLETE: Verification passed.
Project: <project-path>

Tests: [N] passed

Next: Run /eiffel.harden <project-path> for adversarial testing.
```
