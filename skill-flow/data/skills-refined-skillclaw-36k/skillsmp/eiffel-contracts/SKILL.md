---
name: eiffel-contracts
description: Phase 1 of Eiffel Spec Kit. Generates class skeletons with require/ensure/invariant contracts plus skeletal test classes. Contracts ARE tests brought into the class. Use with /eiffel.contracts command.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task
---

# /eiffel.contracts - Phase 1: Contracts + Skeletal Tests

**Purpose:** Generate class skeletons with contracts before any implementation. Contracts ARE tests - brought in from external test classes to live where they have semantic meaning.

## Usage

```
/eiffel.contracts <project-path>
```

**Example:**
```
/eiffel.contracts d:\prod\simple_cache
```

If no path provided, ask user: "Which project? Provide the full path (e.g., d:\prod\simple_cache)"

## Project Scoping

All files are created inside the PROJECT directory:
```
<project-path>/
├── .eiffel-workflow/
│   ├── intent-v2.md (from Phase 0)
│   └── evidence/
│       └── phase1-compile.txt
├── src/
│   └── *.e (contract skeletons)
├── test/
│   └── *.e (skeletal tests)
└── <project>.ecf
```

## Prerequisites

- Phase 0 complete: `<project-path>/.eiffel-workflow/intent-v2.md` exists and approved

Verify:
```bash
test -f <project-path>/.eiffel-workflow/intent-v2.md && echo "Phase 0 complete" || echo "ERROR: Run /eiffel.intent first"
```

## Workflow

### Step 1: Read Intent

Read `<project-path>/.eiffel-workflow/intent-v2.md` to understand requirements.

### Step 2: Query Ecosystem (via Sub-Agent if needed)

If the library depends on other simple_* libraries, use Task tool:
```
"What classes does simple_mml provide? Show me MML_SET and MML_MAP signatures."
```

### Step 3: Generate Class Skeletons with Contracts

Create source files in `<project-path>/src/` with:
- Full contract specifications (require/ensure/invariant)
- Feature signatures with `do end` stubs (no implementation)
- **MML model queries for all collection attributes** (MANDATORY)

**ECF must include simple_mml:**
```xml
<library name="simple_mml" location="$SIMPLE_EIFFEL\simple_mml\simple_mml.ecf"/>
```

**MML Model Query Checklist (MANDATORY for collections):**
| Attribute Type | Model Query Type | Example |
|----------------|------------------|---------|
| HASH_TABLE [V, K] | MML_MAP [K, V] | `headers_model: MML_MAP [STRING, STRING]` |
| ARRAYED_LIST [T] | MML_SEQUENCE [T] | `items_model: MML_SEQUENCE [ITEM]` |
| Set-like collection | MML_SET [T] | `keys_model: MML_SET [KEY]` |

**Contract Completeness Checklist:**
Every postcondition must answer:
1. **What changed?** (direct effect)
2. **How did it change?** (relationship to `old` state)
3. **What did NOT change?** (frame conditions via MML `|=|`)

```eiffel
class SIMPLE_CACHE [K, V]

inherit
    ANY
        redefine
            default_create
        end

create
    make, default_create

feature {NONE} -- Initialization

    make (a_capacity: INTEGER)
            -- Create cache with `a_capacity` slots.
        require
            positive_capacity: a_capacity > 0
        do
            capacity := a_capacity
            create internal_table.make (a_capacity)
        ensure
            capacity_set: capacity = a_capacity
            is_empty: count = 0
        end

feature -- Model Queries (for MML postconditions)

    keys_model: MML_SET [K]
            -- Model of all keys in cache.
        do
            create Result.make_empty
            across internal_table as ic loop
                Result := Result & @ic.key
            end
        end

feature -- Commands

    put (a_key: K; a_value: V)
            -- Store `a_value` under `a_key`.
        require
            key_valid: a_key /= Void
        do
            -- Implementation in Phase 4
        ensure
            has_key: keys_model.has (a_key)
            value_stored: item (a_key) = a_value
            count_bounded: count <= capacity
            others_unchanged: keys_model.removed (a_key) |=| old keys_model.removed (a_key)
        end

invariant
    count_non_negative: count >= 0
    count_bounded: count <= capacity

end
```

### Step 4: Generate Skeletal Test Classes

Create test files in `<project-path>/test/`:

```eiffel
class TEST_SIMPLE_CACHE

inherit
    EQA_TEST_SET

feature -- Tests

    test_make_creates_empty_cache
            -- Test that make creates an empty cache.
        local
            l_cache: SIMPLE_CACHE [STRING, INTEGER]
        do
            create l_cache.make (10)
            assert ("is empty", l_cache.count = 0)
            assert ("capacity set", l_cache.capacity = 10)
        end

    test_put_stores_value
            -- Test that put stores retrievable value.
        local
            l_cache: SIMPLE_CACHE [STRING, INTEGER]
        do
            create l_cache.make (10)
            l_cache.put ("key", 42)
            -- Postconditions verify correctness; this confirms observable behavior
            assert ("value retrieved", l_cache.item ("key") = 42)
        end

    test_put_on_full_cache
            -- Skeletal: will be fleshed out in Phase 5.
        do
            -- TODO: Phase 5
        end

end
```

### Step 5: Create/Update ECF

Ensure `<project-path>/<project>.ecf` exists with proper targets.

### Step 5b: ECF Dependency Audit (simple_* First - MANDATORY)

**RULE:** Validate ECF against simple_* first policy from intent-v2.md.

**Scan ECF for violations:**
```bash
grep -E '\$ISE_LIBRARY|\$GOBO|gobo' <project-path>/<project>.ecf
```

**Allowed ISE libraries (no simple_* equivalent):**
- `$ISE_LIBRARY/library/base/base.ecf` - fundamental types
- `$ISE_LIBRARY/library/time/time.ecf` - DATE, TIME, DATE_TIME
- `$ISE_LIBRARY/library/testing/testing.ecf` - EQA_TEST_SET

**BLOCKED (simple_* exists):**
| ISE/Gobo Path | Use Instead |
|---------------|-------------|
| `$ISE_LIBRARY/library/process` | simple_process |
| `$ISE_LIBRARY/contrib/.../json` | simple_json |
| `$ISE_LIBRARY/library/net` | simple_http |
| `$ISE_LIBRARY/library/xml` | simple_xml |
| `$GOBO/library/regexp` | simple_regex |
| `$GOBO/library/string` | simple_encoding |

**If violation found:**
1. Check if simple_* equivalent exists:
   ```
   Task(subagent_type=Explore) → "Does a simple_* library exist for [capability]?"
   ```
2. If exists → Replace with simple_* in ECF
3. If not exists → Document gap and get user approval to use ISE/Gobo temporarily

**ECF Template (correct pattern):**
```xml
<capability>
    <concurrency support="scoop"/>
    <void_safety support="all"/>
</capability>
<!-- ISE allowed -->
<library name="base" location="$ISE_LIBRARY/library/base/base.ecf"/>
<library name="testing" location="$ISE_LIBRARY/library/testing/testing.ecf"/>
<!-- simple_* preferred -->
<library name="simple_json" location="$SIMPLE_EIFFEL/simple_json/simple_json.ecf"/>
<library name="simple_http" location="$SIMPLE_EIFFEL/simple_http/simple_http.ecf"/>
<library name="simple_mml" location="$SIMPLE_EIFFEL/simple_mml/simple_mml.ecf"/>
```

**Evidence:** Add to phase1-compile.txt:
```
ECF Dependency Audit:
- ISE allowed: base, time, testing
- simple_* used: [list]
- Violations: [none or list with justification]
- Gaps identified: [none or list for future simple_*]
```

### Step 6: Compile (MANDATORY GATE)

**CRITICAL: You MUST cd to the project directory before compiling.** The EIFGENs folder is created in the current working directory, not where the ECF file is located. Compiling from the wrong directory pollutes other folders with build artifacts.

```bash
cd <project-path> && /d/prod/ec.sh -batch -config <project>.ecf -target <project>_tests -c_compile
```

**MUST see "System Recompiled."** If compilation fails, fix contracts before proceeding.

**ZERO WARNINGS POLICY:** If the compiler reports obsolete call warnings or any other warnings, FIX THEM IMMEDIATELY. Do not note them and move on. Do not defer them. Fix them right now before proceeding. Common fixes:
- Obsolete `as_string_8`: Use explicit `{STRING_32} "literal"` manifest type or `.to_string_8`
- Obsolete feature calls: Replace with the suggested alternative in the warning message

### Step 6b: SCOOP Consumer Test (MANDATORY GATE)

**Why:** Libraries may compile standalone but break when consumed by SCOOP-enabled projects. This catches VUAR(2) type conformance errors early.

Create a minimal SCOOP consumer test file `<project-path>/test/test_scoop_consumer.e`:

```eiffel
note
    description: "SCOOP consumer compatibility test"

class TEST_SCOOP_CONSUMER

feature -- Test

    test_scoop_compatibility
            -- Verify library types work in SCOOP context.
        local
            -- Declare locals using library's main types
            l_instance: <MAIN_CLASS>
        do
            create l_instance.make
            -- Minimal usage to trigger type checking
        end

end
```

**Compile with explicit SCOOP:**
```bash
cd <project-path> && /d/prod/ec.sh -batch -config <project>.ecf -target <project>_tests -c_compile
```

The ECF already has `<concurrency support="scoop"/>`, so this verifies SCOOP compatibility.

**If VUAR(2) errors occur:** The library's generic constraints need `separate` keyword. See simple_mml v1.0.1 for the pattern: `[G -> detachable separate ANY]`

### Step 7: Save Evidence

Save to `<project-path>/.eiffel-workflow/evidence/phase1-compile.txt`:
```
# Phase 1 Compilation Evidence
# Project: <project-path>
# Date: [timestamp]
# Command: /d/prod/ec.sh -batch -config <project>.ecf -target <project>_tests -c_compile

[Paste actual compilation output here]

# Status: PASS / FAIL
```

## Completion

When compilation succeeds:
```
Phase 1 COMPLETE: Contracts and skeletal tests created.
Project: <project-path>

Files created:
  - src/*.e (contract skeletons)
  - test/*.e (skeletal tests)
  - Compilation: PASS

Next: Run /eiffel.review <project-path> to submit contracts for adversarial AI review.
```

## Context Management (RLM Pattern)

This skill focuses ONLY on: `<project-path>`

**DO NOT:**
- Read files outside this project directory
- Load entire ecosystem or multiple libraries into context
- Keep large file contents in working memory

**DO:**
- Use Task tool with Explore agent for ecosystem questions
- Ask targeted questions: "What are MML_SET's key features?" not "Show me all simple_mml"
- Release context after getting answers

**Example - Ecosystem Query:**
```
Need simple_mml API? Don't read all its files.
Instead: Task(subagent_type=Explore) → "Show MML_SET and MML_MAP creation and query signatures"
```

The sub-agent searches, summarizes, and returns ONLY what you need. Your context stays focused on this project.

## Anti-Drift

- Contracts are written BEFORE implementation
- Compilation gate ensures contracts are syntactically valid
- Skeletal tests document what will be tested (can't claim "I forgot")
- **MML is mandatory for collections** - decided in Phase 0, enforced here
- **SCOOP consumer test catches integration issues early** - no "works for me" drift
- **simple_* first policy enforced** - ECF audit blocks ISE/Gobo where simple_* exists
- **Gaps documented** - ISE/Gobo usage requires justification and creates future simple_* recommendations
- **Skill Version Lock:** If you discover skill improvements during workflow, queue them in `<project-path>/.eiffel-workflow/skill-improvements.md` - do NOT modify skills mid-workflow
