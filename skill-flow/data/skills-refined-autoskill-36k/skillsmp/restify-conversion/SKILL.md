---
name: restify-conversion
description: Orchestrate the conversion of Node.js Restify API services to Rust Dropshot API traits. Use this skill when migrating Node.js services to Rust. This orchestrator spawns separate sub-agents for each phase to manage context.
allowed-tools: Bash(git add:*), Bash(git commit:*), Bash(make:*), Bash(git branch:*), Bash(git status:*), Bash(mkdir:*), Read, Glob, Grep, Write, Edit
---

<!--
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Copyright 2026 Edgecast Cloud LLC.
-->

# Restify to Dropshot Conversion Orchestrator

This skill orchestrates the multi-phase conversion of Node.js Restify APIs to Rust Dropshot traits by spawning separate sub-agents for each phase.

## Why Separate Sub-agents?

Each phase can be context-intensive (reading many source files, generating code). Running all phases in a single context risks running out of context mid-conversion. By spawning separate sub-agents:

1. Each phase gets fresh context
2. Checkpoints allow resumption if interrupted
3. Summaries pass essential information between phases
4. User can review between phases if desired

## Pre-flight Checks (CRITICAL)

Before starting any conversion, verify:

1. **Not on main/master branch:**
   ```bash
   git branch --show-current
   ```
   If on `main` or `master`, ask user to create/switch to a feature branch first.

2. **Working directory is clean:**
   ```bash
   git status --porcelain
   ```
   If there are uncommitted changes, ask user to commit or stash them first.

**Do not proceed until both checks pass.**

## Plan File Location

Plan files are stored in the project directory (NOT under `.claude/`) so they:
- Don't trigger excessive permission prompts
- Can be committed with the work
- Are visible in PRs

Location: `conversion-plans/<service>/plan.md`

## Autonomous Execution (IMPORTANT)

**Execute all phases automatically without pausing for user input** unless:
1. A pre-flight check fails (wrong branch, dirty working directory)
2. A phase encounters an error that cannot be resolved
3. A build or test failure occurs that requires user decision

Do NOT pause between phases to ask "should I continue?" or wait for confirmation. The entire conversion (phases 1-5) should run to completion automatically. If you find yourself about to ask the user whether to proceed to the next phase, just proceed instead.

## Orchestration Flow

When asked to convert a Restify service, execute this flow:

### Step 0: Pre-flight Checks

Before spawning any sub-agent:

```bash
# Check branch
git branch --show-current
# Must NOT be main or master

# Check for uncommitted changes
git status --porcelain
# Must be empty
```

If either check fails, inform the user and stop.

### Step 1: Spawn Phase 1 (Analyze)

```
Use the Task tool with subagent_type="general-purpose" to run Phase 1:

Prompt: "Execute the restify conversion Phase 1: Analyze.
Source path: <user-provided-path>
Read .claude/skills/restify-conversion/phase1-analyze.md for instructions.
Output a summary to conversion-plans/<service>/plan.md"
```

Wait for completion. Read the generated plan.md to get:
- Service name
- Version
- Endpoint count
- Route conflicts and resolutions
- File structure plan

**After Phase 1 completes:**
```bash
make check
git add conversion-plans/<service>/plan.md
git commit -m "Add <service> conversion plan (Phase 1)"
```

### Step 2: Spawn Phase 2 (Generate API)

```
Use the Task tool with subagent_type="general-purpose" to run Phase 2:

Prompt: "Execute the restify conversion Phase 2: Generate API Trait.
Service name: <service>
Read the plan at conversion-plans/<service>/plan.md
Read .claude/skills/restify-conversion/phase2-api.md for instructions.
Read .claude/skills/restify-conversion/reference.md for mapping rules.
Update plan.md with Phase 2 results."
```

Wait for completion. Verify:
- `make format package-build PACKAGE=<service>-api` succeeds
- OpenAPI spec exists at `openapi-specs/generated/<service>-api.json`

**After Phase 2 completes:**
```bash
make check
git add apis/<service>-api/ openapi-specs/generated/<service>-api.json conversion-plans/<service>/plan.md Cargo.toml Cargo.lock openapi-manager/
git commit -m "Add <service> API trait (Phase 2)"
```

### Step 3: Spawn Phase 3 (Generate Client)

```
Use the Task tool with subagent_type="general-purpose" to run Phase 3:

Prompt: "Execute the restify conversion Phase 3: Generate Client.
Service name: <service>
Read the plan at conversion-plans/<service>/plan.md
Read .claude/skills/restify-conversion/phase3-client.md for instructions.
Update plan.md with Phase 3 results."
```

Wait for completion. Verify:
- `make format package-build PACKAGE=<service>-client` succeeds

**After Phase 3 completes:**
```bash
make check
git add clients/internal/<service>-client/ conversion-plans/<service>/plan.md Cargo.toml Cargo.lock
git commit -m "Add <service> client library (Phase 3)"
```

### Step 4: Spawn Phase 4 (Generate CLI)

```
Use the Task tool with subagent_type="general-purpose" to run Phase 4:

Prompt: "Execute the restify conversion Phase 4: Generate CLI.
Service name: <service>
Read the plan at conversion-plans/<service>/plan.md
Read .claude/skills/restify-conversion/phase4-cli.md for instructions.
Update plan.md with Phase 4 results."
```

Wait for completion. Verify:
- `make format package-build PACKAGE=<service>-cli` succeeds
- `make format build` succeeds

**After Phase 4 completes:**
```bash
make check
git add cli/<service>-cli/ conversion-plans/<service>/plan.md Cargo.toml Cargo.lock
git commit -m "Add <service> CLI (Phase 4)"
```

### Step 5: Spawn Phase 5 (Validate)

```
Use the Task tool with subagent_type="general-purpose" to run Phase 5:

Prompt: "Execute the restify conversion Phase 5: Validate.
Service name: <service>
Source path: <original-source-path>
Read the plan at conversion-plans/<service>/plan.md
Read .claude/skills/restify-conversion/phase5-validate.md for instructions.
Create a validation report at conversion-plans/<service>/validation.md"
```

**After Phase 5 completes:**
```bash
make check
git add conversion-plans/<service>/
git commit -m "Add <service> validation report (Phase 5 - conversion complete)"
```

## Checkpoint Files

All state is persisted in `conversion-plans/<service>/`:

- `plan.md` - Conversion plan and phase completion status
- `validation.md` - Phase 5 validation report

This allows:
- Resuming from any phase if interrupted
- User review between phases
- Audit trail of the conversion
- Commits track progress through the conversion

## Error Handling

If any phase fails:
1. The sub-agent should document the error in plan.md
2. The orchestrator reports the failure to the user
3. User can fix issues and resume from the failed phase

## Usage

When the user asks to convert a service:

```
Convert the Restify API at /path/to/sdc-vmapi to Dropshot
```

1. **Run pre-flight checks** (branch not main/master, working directory clean)
2. Confirm the source path exists
3. Derive service name from the path (e.g., "vmapi" from "sdc-vmapi")
4. Create `conversion-plans/<service>/` directory
5. Execute phases 1-5 in sequence, spawning sub-agents
6. After each phase: run `make check`, commit the work
7. Report final status and any validation findings

## Commit Messages

Each phase produces a commit:
- Phase 1: `Add <service> conversion plan (Phase 1)`
- Phase 2: `Add <service> API trait (Phase 2)`
- Phase 3: `Add <service> client library (Phase 3)`
- Phase 4: `Add <service> CLI (Phase 4)`
- Phase 5: `Add <service> validation report (Phase 5 - conversion complete)`

This creates an atomic, reviewable history of the conversion process.
