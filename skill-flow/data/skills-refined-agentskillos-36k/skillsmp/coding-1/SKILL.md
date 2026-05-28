---
name: coding
description: Use when performing coding tasks (implement features, fix bugs, refactor code). Orchestrates language detection, mode switching (normal/autopilot/full-auto), quality enforcement, and verification.
allowed-tools: ["shell", "apply_patch", "read_file", "write_file", "update_plan"]
metadata:
  short-description: General coding orchestrator with modes
---

# Coding Orchestrator

This skill serves as the primary entry point for general coding tasks. It provides:
- **Mode switching**: normal (confirm all) / autopilot (confirm risky) / full-auto (minimal confirmation)
- **Language detection**: Auto-detect project language and apply appropriate guidance
- **Quality enforcement**: Integrate task-discipline, code-quality, verification patterns
- **Risk-based confirmation**: Consistent behavior based on operation risk tier

**Read these references:**
- `references/workflow.md` - Universal coding workflow
- `references/quality.md` - Quality priorities (correctness > safety > maintainability)
- `references/safety.md` - Runtime + security safety
- `references/risk-taxonomy.md` - 4-tier operation risk classification
- `references/guardrails.md` - Per-mode guardrails and limits
- `~/.config/agent/core/methodology.md` - 5-phase problem-solving
- `~/.config/agent/core/task-management.md` - Task discipline patterns

---

## Mode Selection

### Active Mode Determination

Mode is determined by (priority order):

1. **Explicit argument**: `mode:autopilot` or `mode:full-auto` prefix in arguments
2. **Session context**: Previously set mode (sticky within session)
3. **Default**: `normal`

### Mode Definitions

| Mode | Philosophy | Confirmation Behavior |
|------|------------|----------------------|
| **normal** | Maximum safety | Confirm for all modifications (Tier 1/2/3) |
| **autopilot** | Balanced autonomy | Confirm for risky operations (Tier 1/2), auto for safe (Tier 3/4) |
| **full-auto** | Maximum autonomy | Confirm for critical only (Tier 1), auto for all else |

See `references/risk-taxonomy.md` for full tier definitions.

### Mode Switching

**Explicit mode in arguments:**
```
mode:autopilot fix the bug in handler.go
mode:full-auto add tests to all packages
```

**Conversational switching:**
User says any of:
- "switch to autopilot mode" / "use autopilot"
- "switch to full-auto mode" / "go full auto"
- "back to normal mode" / "use normal mode"

**Mode persistence:**
Once set, mode persists for the entire session until explicitly changed. Each new session starts in `normal` mode.

**Escalation safeguards:**
- normal → autopilot: Acknowledge, proceed
- normal → full-auto: Warn about risks, confirm intent, proceed
- autopilot → full-auto: Warn about risks, confirm intent, proceed
- De-escalation (to more restrictive): Acknowledge, proceed immediately

---

## Language Detection

Detect the project's primary language to apply language-specific guidance.

### Detection Priority

1. **Explicit in request**: "fix the Go handler", "update the Python script"
2. **File extension**: `.go`, `.py`, `.rs`, `.ts`, `.js`, `.java`, etc.
3. **Project markers** (check working directory):
   - `go.mod` → Go
   - `Cargo.toml` → Rust
   - `package.json` → JavaScript/TypeScript
   - `pyproject.toml` or `requirements.txt` → Python
   - `pom.xml` or `build.gradle` → Java
4. **Ask if ambiguous**: Multiple languages detected or unclear

### Language-Specific Guidance

When a language is detected, read and apply ALL guidance from that language's domain:

**Go (detected):**
```markdown
Read and apply:
- `~/.config/agent/domain/coding/go/style.md`
- `~/.config/agent/domain/coding/go/idioms.md`
- `~/.config/agent/domain/coding/go/concurrency.md`
- `~/.config/agent/domain/coding/go/testing.md`
- `~/.config/agent/domain/coding/go/tooling.md`
- `~/.config/agent/domain/coding/go/organization.md`
- `~/.config/agent/domain/coding/go/performance.md`
```

**Python (future):**
```markdown
Read and apply:
- `~/.config/agent/domain/coding/python/style.md`
- `~/.config/agent/domain/coding/python/idioms.md`
- (etc.)
```

**Other languages:**
Apply generic workflow from `references/workflow.md` and `references/quality.md`.

---

## Workflow

The coding skill follows a 5-phase workflow with mode-specific confirmation behavior.

### Phase 1: Context Gathering

**Objectives:**
- Determine active mode
- Detect project language
- Read relevant files before modifying
- Load language-specific guidance

**Steps:**
1. Parse arguments for mode prefix (`mode:autopilot`, `mode:full-auto`)
2. If no explicit mode, check session context for previously set mode
3. If no session mode, use `normal` as default
4. Detect language using priority algorithm
5. Read target files (never modify before reading)
6. Load language-specific guidance modules

**Mode behavior:** All modes identical (read-only phase).

### Phase 2: Planning (if non-trivial)

**When to plan:**
- Tasks requiring 3+ distinct steps
- Multi-file modifications
- Complex logic changes
- Non-obvious implementation approach

**Apply task-discipline patterns:**
1. Create TODO list with atomic, testable tasks
2. Use imperative form for content: "Fix bug in parser"
3. Use present continuous for activeForm: "Fixing bug in parser"
4. Ensure exactly ONE task is `in_progress` at any time
5. Mark tasks `completed` immediately after finishing

**Mode behavior:** All modes identical (planning phase).

### Phase 3: Implementation

Apply universal coding workflow from `references/workflow.md`:

1. **Understand before modifying**: Read code, understand context
2. **Make minimal, targeted changes**: Don't refactor unrelated code
3. **Test incrementally**: Don't save all testing for the end
4. **Document non-obvious decisions**: Add comments where logic isn't self-evident

**Mode-specific confirmation behavior:**

**Normal mode:**
- Propose complete plan upfront
- Confirm before EACH file modification
- Show exact changes (diff if useful)
- Offer options: [P]roceed / [D]iff / [S]kip / [A]bort

**Autopilot mode:**
- Proceed automatically for Tier 3/4 operations
- Report progress: "Created X, Modified Y"
- Pause only for Tier 1/2 operations (see `references/risk-taxonomy.md`)
- Create checkpoint (git stash) before destructive operations
- Track operation count and time limits (see `references/guardrails.md`)
- Commits are never auto-run; require explicit confirmation/manual action

**Full-auto mode:**
- Proceed automatically for Tier 2/3/4 operations (except never-auto overrides)
- Audit log all operations with timestamps (see `references/guardrails.md`)
- Create checkpoints before major operations (>5 files or git push)
- Pause for Tier 1 CRITICAL operations and never-auto overrides (e.g., commits)
- Report progress every 10 operations or 5 minutes
- Stop after 3 consecutive failures, offer recovery options

### Phase 4: Quality Gates

Before claiming completion, enforce quality checks:

**Apply code-quality patterns:**
1. **Correctness**: Does the code do what it's supposed to?
2. **Safety**: Any runtime safety issues (nil dereferences, races, leaks)?
3. **Maintainability**: Is the code clear and simple?
4. **Performance**: Any obvious inefficiencies?
5. **Style**: Does it follow language conventions?

**Language-specific quality checks:**

**Go:**
```bash
# Run tests (if applicable)
go test -race -count 1 ./...

# Run linter (if applicable)
golangci-lint run --new=false ./...

# Format code
golines --base-formatter=gofumpt --ignore-generated --max-len=79 --tab-len=4 --no-reformat-tags --chain-split-dots -w .
gofumpt -w .
```

**Mode behavior for quality checks:**
- **Normal**: Confirm before running each tool
- **Autopilot**: Auto-run tests/lint/format (Tier 3), report results
- **Full-auto**: Auto-run all quality checks, only stop if failures block progress

### Phase 5: Verification

Apply `verification-before-completion` patterns:

**NEVER claim completion without evidence:**
1. Run the verification command (tests, lint, build)
2. Confirm output supports the claim
3. ONLY THEN declare completion

**Examples of evidence:**
- Tests passing: `ok github.com/user/repo/package 0.123s`
- Lint clean: `golangci-lint run` with no output or exit 0
- Build successful: `go build -o /dev/null ./...` with exit 0
- Manual verification: Show output of commands that confirm fix

**Mode behavior:**
- All modes must provide evidence before completion
- Cannot skip verification even in full-auto
- If verification fails, apply recovery procedures (see `references/guardrails.md`)

---

## Cross-Skill Coordination

### Absorb (Apply Inline)

These skills' patterns are absorbed and applied directly within the coding workflow:

| Skill | When | What to Apply |
|-------|------|---------------|
| `task-discipline` | 3+ step tasks | TODO list with exactly ONE in_progress at any time |
| `code-quality` | All coding | Priority order: correctness > safety > maintainability > performance > style |
| `verification-before-completion` | Before completion claims | Evidence requirement: run verification, show output, then claim success |

### Delegate (Recommend Invocation)

Recommend explicit skill invocation when appropriate:

| Condition | Recommended Skill | When to Recommend |
|-----------|-------------------|-------------------|
| Bugs/test failures encountered | `systematic-debugging` | After 2 failed fix attempts or unclear root cause |
| Security-sensitive code | `safety-check` | When modifying auth, crypto, input validation, or data access |
| Pre-commit checks needed | `go-precommit` (or language equivalent) | Before creating commits |
| Code review requested | `review` | User explicitly asks for review |
| Strict TDD requested | `tdd-enforce` | User explicitly requests test-first approach |

**Recommendation format:**
```
I encountered test failures. I recommend using the `systematic-debugging` skill
for a methodical root-cause analysis.

Would you like me to:
1. Continue debugging manually
2. Invoke the systematic-debugging skill
3. Ask you for guidance
```

---

## Operation Risk Classification

Before performing any operation, classify it using the risk taxonomy:

**Tier 1 (CRITICAL):** Force push main, credentials, prod DB, external API mutations
**Tier 2 (HIGH):** File deletion, git state changes (commit/push/merge/rebase), non-deterministic line edits, package management
**Tier 3 (MEDIUM):** New files, tests, deterministic formatting/lint fixes, builds
**Tier 4 (LOW):** Read-only operations

See `references/risk-taxonomy.md` for complete classification algorithm and examples.

**Apply confirmation behavior based on mode and tier:**

| Tier | Normal | Autopilot | Full-Auto |
|------|--------|-----------|-----------|
| 1 | Confirm | Confirm | **Confirm** |
| 2 | Confirm | Confirm | Auto |
| 3 | Confirm | Auto | Auto |
| 4 | Auto | Auto | Auto |

**Never-auto overrides** (e.g., `git commit`) supersede this matrix.

---

## Guardrails and Limits

Apply limits from `references/guardrails.md` based on active mode:

**Autopilot limits:**
- Max 10 files modified per operation
- Max 100 lines modified per file
- Auto-stash before destructive operations

**Full-auto limits:**
- Report progress every 10 operations or 5 minutes
- Pause after 30 minutes
- Stop after 3 consecutive failures

**Absolute never-auto (all modes including full-auto):**
- Git commits (`git commit`, `git commit --amend`)
- Force push to main/master
- Credential/secret operations
- Production deployments
- Database migrations on prod

---

## Recovery and Safety

### Checkpoints

**Autopilot mode:**
```bash
# Before Tier 2 destructive operations
git stash push -m "autopilot-checkpoint-$(date +%s)"
```

**Full-auto mode:**
```bash
# Before operations affecting >5 files or git push
git stash push -m "full-auto-checkpoint-$(date +%s)"
```

### Rollback on Failure

If an operation fails and a checkpoint exists:
```
Operation failed: tests not passing after modification

Recovery options:
1. [R]evert to checkpoint
2. [D]ebug the issue
3. [C]ontinue anyway (not recommended)
4. [S]witch to normal mode

Choice: _
```

### Audit Logging

Full-auto mode logs all operations. Autopilot logs Tier 2/3 operations. See `references/guardrails.md` for file location and redaction requirements.

Example format:
```
[12:00:01] [FULL-AUTO] [TIER-3] Created: api/handler.go [SUCCESS]
[12:00:03] [FULL-AUTO] [TIER-3] Created: api/handler_test.go [SUCCESS]
[12:00:05] [FULL-AUTO] [TIER-2] Modified: api/routes.go (+15 lines) [SUCCESS]
```

---

## Integration with Existing Skills

This skill complements (does not replace) existing skills:

| Existing Skill | Relationship |
|----------------|--------------|
| `go-development` | `coding` applies Go guidance when Go detected; users can still invoke `go-development` directly |
| `feature` | `coding` handles tactical implementation; `feature` handles strategic 7-phase workflow |
| `code-quality` | `coding` absorbs quality patterns inline |
| `task-discipline` | `coding` absorbs task patterns for 3+ step work |
| `verification-before-completion` | `coding` absorbs verification gate requirement |
| `systematic-debugging` | `coding` recommends invocation when bugs encountered |
| `safety-check` | `coding` recommends invocation for security-sensitive code |
| `review` | `coding` recommends invocation when review requested |

---

## Activation Triggers

This skill activates for:
- General coding requests: "implement X", "fix bug in Y", "refactor Z"
- Mode-prefixed requests: "mode:autopilot add error handling"
- Generic file modifications (when not caught by more specific skills)

This skill does NOT activate for:
- Planning/design requests (use `planner`)
- Review requests (use `review`)
- Explicit debugging requests (use `systematic-debugging`)
- Language-specific tool invocations (use `go-test`, `go-lint`, etc.)

---

## Arguments

Mode: ${MODE}
Target: ${ARGUMENTS}

**Argument patterns:**
- `mode:normal implement user authentication`
- `mode:autopilot fix all lint errors`
- `mode:full-auto add tests for parser package`
- `fix bug in handler.go:42` (defaults to normal mode)
