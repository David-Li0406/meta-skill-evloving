---
name: ulw
description: ULTRAWORK MODE - Maximum capability activation. Use when you need parallel agent orchestration, strict verification, and zero tolerance for incomplete work. Triggers automatically on 'ultrawork' or 'ulw' in message.
---

# ULTRAWORK MODE (ULW)

> **ACTIVATION**: Say "ULTRAWORK MODE ENABLED!" when this skill is loaded.

## [CODE RED] Maximum Precision Required

YOU MUST LEVERAGE ALL AVAILABLE AGENTS TO THEIR FULLEST POTENTIAL.
TELL THE USER WHAT AGENTS YOU WILL LEVERAGE TO SATISFY THEIR REQUEST.

---

## Agent Utilization Principles

| Capability | Agent | Execution |
|------------|-------|-----------|
| Codebase Exploration | `explore` | BACKGROUND TASKS, parallel |
| Documentation & References | `researcher` | BACKGROUND TASKS, parallel |
| Planning & Strategy | `plan` agent | Dedicated work breakdown |
| High-IQ Reasoning | `oracle` | Architecture, debugging |
| Frontend/UI | `coder` with `frontend-philosophy` | Delegate visual work |
| Code Implementation | `coder` | Atomic coding tasks |
| Code Review | `reviewer` | Before completion |

---

## Execution Rules

### TODO Tracking (MANDATORY)
- Track EVERY step with `todowrite`
- Mark complete IMMEDIATELY after each step
- Never batch completions

### Parallel Execution (THREE TIERS)

**Tier 1: Agent-Level Parallelism**
```
// Fire 3-10+ background agents simultaneously
task(agent="explore", prompt="Find X...", background=true)
task(agent="explore", prompt="Find Y...", background=true)
task(agent="researcher", prompt="Find Z docs...", background=true)
// Continue working, collect with background_output when needed
```

**Tier 2: Tool-Level Parallelism (BATCH)**

Use the `batch` tool for 2-25 independent tool operations:

```json
{
  "tool": "batch",
  "parameters": {
    "tool_calls": [
      {"tool": "read", "parameters": {"filePath": "src/file1.ts"}},
      {"tool": "read", "parameters": {"filePath": "src/file2.ts"}},
      {"tool": "grep", "parameters": {"pattern": "import", "include": "*.ts"}},
      {"tool": "bash", "parameters": {"command": "git status"}}
    ]
  }
}
```

| ✅ GOOD TO BATCH | ❌ DO NOT BATCH |
|------------------|-----------------|
| Read multiple files | Tools that depend on prior output |
| grep + glob + read combos | Sequential mutations (create → read) |
| Multiple bash commands | The `batch` tool itself |
| Multi-file edits (independent) | MCP/environment tools |
| LSP tools on different files | Ordered stateful operations |

**Limits**: Max 25 tools per batch. Partial failures don't stop others.
**Impact**: 2-5x speedup for independent operations.

**Tier 3: Combined (MAXIMUM THROUGHPUT)**
```
// Spawn agents + batch tools simultaneously
task(agent="explore", background=true)
task(agent="researcher", background=true)
batch([read(5 files), grep(3 patterns), glob(2 paths)])
```

**Priority**: Batch tools FIRST when possible. Spawn agents SECOND for cognitive tasks.

### Verification Loop
- Re-read original request after completion
- Check ALL requirements met before reporting done
- Run build/test commands and show output

---

## Verification Guarantee (NON-NEGOTIABLE)

**NOTHING is "done" without PROOF it works.**

### Pre-Implementation: Define Success Criteria

| Criteria Type | Description | Example |
|---------------|-------------|---------|
| **Functional** | What behavior must work | "Button triggers API call" |
| **Observable** | What can be measured | "Console shows 'success'" |
| **Pass/Fail** | Binary, no ambiguity | "Returns 200 OK" |

### Execution & Evidence Requirements

| Phase | Action | Required Evidence |
|-------|--------|-------------------|
| **Build** | Run build command | Exit code 0, no errors |
| **Test** | Execute test suite | All tests pass |
| **Manual Verify** | Test the actual feature | Describe what you observed |
| **Regression** | Ensure nothing broke | Existing tests still pass |

**WITHOUT evidence = NOT verified = NOT done.**

### Verification Phase Batching

Use batch tool during verification for efficiency:

```json
{
  "tool": "batch",
  "parameters": {
    "tool_calls": [
      {"tool": "bash", "parameters": {"command": "bun run build", "description": "Build project"}},
      {"tool": "bash", "parameters": {"command": "bun test", "description": "Run tests"}},
      {"tool": "bash", "parameters": {"command": "bun run typecheck", "description": "Type check"}}
    ]
  }
}
```

**Verification checklist batch:**
```json
{
  "tool": "batch", 
  "parameters": {
    "tool_calls": [
      {"tool": "lsp_diagnostics", "parameters": {"filePath": "src/changed-file-1.ts"}},
      {"tool": "lsp_diagnostics", "parameters": {"filePath": "src/changed-file-2.ts"}},
      {"tool": "grep", "parameters": {"pattern": "TODO|FIXME|XXX", "include": "src/**/*.ts"}}
    ]
  }
}
```

### TDD Workflow (when test infrastructure exists)

1. **SPEC**: Define success criteria
2. **RED**: Write failing test → Run → Confirm FAILS
3. **GREEN**: Write code → Run test → Confirm PASSES
4. **REFACTOR**: Clean up → Tests STAY green
5. **VERIFY**: Full test suite, no regressions
6. **EVIDENCE**: Report what you ran and output seen

---

## Verification Anti-Patterns (BLOCKING)

| Violation | Why It Fails |
|-----------|--------------|
| "It should work now" | No evidence. Run it. |
| "I added the tests" | Did they pass? Show output. |
| "Fixed the bug" | How do you know? What did you test? |
| "Implementation complete" | Did you verify against success criteria? |
| Skipping test execution | Tests exist to be RUN |

**CLAIM NOTHING WITHOUT PROOF. EXECUTE. VERIFY. SHOW EVIDENCE.**

---

## Zero Tolerance Failures

| Violation | Consequence |
|-----------|-------------|
| **Scope Reduction** | NEVER make "demo", "skeleton", "basic" versions |
| **MockUp Work** | NEVER mock data when real implementation asked |
| **Partial Completion** | NEVER stop at 60-80% |
| **Assumed Shortcuts** | NEVER skip "optional" requirements |
| **Premature Stopping** | NEVER declare done until ALL TODOs completed |
| **Test Deletion** | NEVER delete failing tests to pass build |

**THE USER ASKED FOR X. DELIVER EXACTLY X. NOT A SUBSET. NOT A DEMO.**

---

## Workflow Summary

1. **Analyze** the request, identify required capabilities
2. **Spawn** explore/researcher agents in PARALLEL (3-10+ if needed)
3. **Plan** with gathered context (use `plan` agent for complex work)
4. **Execute** with continuous verification against original requirements
5. **Review** delegate to `reviewer` before completion
6. **Verify** build, test, show evidence
7. **Complete** only when ALL requirements proven to work

---

## Quick Reference: Agent Routing

```
// Codebase search
task(agent="explore", prompt="...", background=true)

// External docs/GitHub
task(agent="researcher", prompt="...", background=true)

// Strategic planning
task(agent="plan", prompt="...")

// Architecture consultation
task(agent="oracle", prompt="...")

// Implementation
task(agent="coder", prompt="...", skills=["code-philosophy"])

// Code review
task(agent="reviewer", prompt="Review changes in [files]")
```
