---
name: eiffel-harden
description: Phase 6 of Eiffel Spec Kit. Generates adversarial tests, stress tests, and edge case tests. AI chain suggests attack vectors. Use with /eiffel.harden command.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task
---

# /eiffel.harden - Phase 6: Adversarial Testing

**Purpose:** Break the implementation with adversarial inputs, stress tests, and edge cases.

## Usage

```
/eiffel.harden <project-path>
```

## Project Scoping

```
<project-path>/
├── .eiffel-workflow/
│   ├── prompts/
│   │   └── phase6-adversarial-review.md
│   └── evidence/
│       └── phase6-tests.txt
├── test/*.e (adversarial tests added here)
```

## Prerequisites

- Phase 5 complete: all tests pass

## Workflow

### Step 0: MML Contract Hardening

Before adversarial tests, strengthen contracts with Mathematical Model Library (MML).

**Add simple_mml dependency to ECF:**
```xml
<library name="simple_mml" location="$SIMPLE_EIFFEL\simple_mml\simple_mml.ecf"/>
```

**Add MML model queries for collections:**
```eiffel
feature -- Model Queries

    items_model: MML_MAP [K, V]
            -- Mathematical model of stored items.
        do
            create Result.make_empty
            across internal_table as ic loop
                Result := Result.extended (@ic.key, @ic.item)
            end
        end
```

**Strengthen postconditions with frame conditions:**
```eiffel
ensure
    -- What changed
    key_added: items_model.has (a_key)
    value_set: items_model [a_key] = a_value

    -- What did NOT change (frame condition)
    others_unchanged: items_model.removed (a_key) |=| old items_model.removed (a_key)
```

**MML Checklist:**
- [ ] Collection attributes have model queries (MML_SET, MML_MAP, MML_SEQUENCE)
- [ ] Postconditions use `|=|` for equality comparisons
- [ ] Frame conditions specify what did NOT change
- [ ] Old expressions capture pre-state: `old items_model`

### Step 1: Generate Adversarial Prompt

Create `<project-path>/.eiffel-workflow/prompts/phase6-adversarial-review.md`:

```markdown
# Adversarial Test Suggestions

## Contracts
[PASTE src/*.e]

## Current Tests
[PASTE test/*.e]

## Suggest Tests For:
1. Boundary values (0, 1, MAX_INT, empty strings)
2. Capacity limits (full, zero capacity)
3. SCOOP concurrent access
4. State transitions in unexpected order
5. Resource exhaustion
```

### Step 2: Human Submits to AI (Optional)

User may submit prompt to external AI for adversarial suggestions.

### Step 3: Generate Adversarial Tests

Add tests like:
- `test_with_zero_capacity`
- `test_same_key_repeatedly`
- `test_stress_many_operations`
- `test_concurrent_access_scoop`

### Step 4: Compile and Run All Tests

**CRITICAL: You MUST cd to the project directory before compiling.** The EIFGENs folder is created in the current working directory, not where the ECF file is located. Compiling from the wrong directory pollutes other folders with build artifacts.

```bash
cd <project-path> && /d/prod/ec.sh -batch -config <project>.ecf -target <project>_tests -c_compile
./EIFGENs/<project>_tests/W_code/<project>.exe
```

**ZERO WARNINGS POLICY:** If the compiler reports obsolete call warnings or any other warnings, FIX THEM IMMEDIATELY. Do not note them and move on. Do not defer them. Fix them right now before proceeding.

**ALL TESTS MUST PASS.**

### Step 4b: SCOOP Consumer Integration Gate (MANDATORY)

**Why:** This catches integration issues that don't appear in standalone compilation. A library with `concurrency=scoop` may compile fine but cause VUAR(2) errors in consumer libraries.

**Create mock consumer project** (temporary, can delete after test):

```bash
mkdir -p <project-path>/test_consumer
```

Create `<project-path>/test_consumer/consumer_test.ecf`:
```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<system name="consumer_test" uuid="[generate-new-uuid]">
    <target name="consumer_test">
        <root class="CONSUMER_TEST" feature="make"/>
        <capability>
            <concurrency support="scoop"/>
            <void_safety support="all"/>
        </capability>
        <library name="base" location="$ISE_LIBRARY\library\base\base.ecf"/>
        <library name="<project>" location="..\<project>.ecf"/>
        <cluster name="src" location="."/>
    </target>
</system>
```

Create `<project-path>/test_consumer/consumer_test.e`:
```eiffel
class CONSUMER_TEST
create make
feature
    make
        local
            l_obj: <MAIN_LIBRARY_CLASS>
        do
            create l_obj.make
            -- Use library types in SCOOP context
        end
end
```

**Compile consumer:**
```bash
cd <project-path>/test_consumer && /d/prod/ec.sh -batch -config consumer_test.ecf -target consumer_test -c_compile
```

**If VUAR(2) errors:** Fix generic constraints in the library (add `separate` keyword).

**Cleanup:**
```bash
rm -rf <project-path>/test_consumer
```

### Step 5: Save Evidence

Save to `<project-path>/.eiffel-workflow/evidence/phase6-tests.txt`:
```
# Phase 6 Hardening Evidence
# Project: <project-path>
# Date: [timestamp]

## MML Hardening
MML dependency added: [yes/no]
Model queries added: [count]
Frame conditions added: [count]

## SCOOP Consumer Integration
Consumer test created: [yes/no]
Consumer compilation: [PASS/FAIL]
VUAR(2) errors fixed: [count or N/A]

## Adversarial Testing
Adversarial tests added: [count]
Stress tests added: [count]

[Paste test output]

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
- Ask targeted questions when adversarial tests need to understand attack vectors from similar libraries
- Release context after getting answers

**Example - Ecosystem Query:**
```
Need ideas for stress testing patterns? Don't read all test files in ecosystem.
Instead: Task(subagent_type=Explore) → "What adversarial test patterns exist in simple_container tests?"
```

The sub-agent searches, summarizes, and returns ONLY what you need. Your context stays focused on this project.

## Completion

```
Phase 6 COMPLETE: Hardening passed.
Project: <project-path>

All tests: PASS

Next: Run /eiffel.ship <project-path> for final checklist.
```
