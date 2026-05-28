---
name: bead-review
description: QA/adversarial audit of bead decomposition for autonomous agent execution
---

# Bead Review Workflow

Review beads against the Technical Design Document using parallel sub-agents for comprehensive coverage. Identifies issues that could cause agent confusion, misimplementation, or wasted work.

## When to use

Use when you have:
- A polished Technical Design Document from Stage 2
- Beads output from Stage 3 (`/write-beads`)
- Need to QA audit the decomposition before implementation

## Architecture: Parallel Sub-Agents

BEADS.md files are typically thousands of lines. A single agent checking everything struggles to maintain accuracy. This review uses **5 parallel sub-agents** plus a **Review Synthesizer**.

### Required Sub-Agents (run in parallel)

#### 1. Coverage Checker
Validates TDD-to-bead mapping:
- Every TDD requirement maps to ≥1 bead
- No orphan beads (bead exists but doesn't trace back to TDD)
- All files mentioned in TDD appear in at least one bead
- Edge cases from TDD are represented

#### 2. Atomicity Checker
Validates bead sizing and responsibility:
- Each bead has one responsibility
- No "implement + refactor + test" bundles
- Beads sized for one focused session (~30 min)
- No bead hides multiple changes

#### 3. Dependency Validator
Validates dependency graph integrity:
- No circular dependencies
- No missing prerequisites
- P0/P1/P2 reflects actual critical path
- Dependency script is complete and uses `bd dep add`
- **DECISION beads have dependents gated via edges** (not `Blocked by:` text)
- Beads marked `Parallelism: decision-gated` depend on a DECISION bead

#### 4. Context Auditor
Validates bead self-sufficiency:
- No "see above" or implicit references
- No pronouns without antecedents
- **External APIs have contracts** (method/endpoint/params/response/errors) OR explicit UNVERIFIED with "How to verify:"
- Acceptance criteria are testable and unambiguous

#### 5. Metadata Checker
Validates required metadata fields:
- Every bead has `Parallelism:` in body (under `### Specification`)
  - Valid values: `parallelizable`, `requires-sequence`, `decision-gated`
- Every bead has `Confidence:` in body (under `### Specification`)
  - Valid values: `verified`, `assumed`, `unverified`
- Labels include project name and phase
- Priority assigned and reasonable
- Type is valid (task, feature, bug, decision)

### Review Synthesizer (runs after sub-agents)

The synthesizer merges findings from all sub-agents:

1. **Merge** - Collect all findings from sub-agents
2. **Deduplicate** - Coverage gap and missing dependency may be same root cause
3. **Consume ledger** - Read `BEADS_LEDGER.md` if exists
4. **Classify findings** - Each finding gets a classification:
   - `net-new` - First time seeing this issue
   - `known-open` - Issue was seen before and not yet fixed
   - `regression` - Previously fixed but reappeared
   - `waived` - Explicitly accepted (requires justification)
5. **Produce verdict** - `APPROVED` or findings with Required Fixes
6. **Update ledger** - Write findings to `BEADS_LEDGER.md`

## Iteration Policy Integration

Reference: `docs/guides/iteration-policy.md`

### Before Starting
```bash
# Check for existing ledger
if [ -f "docs/plans/<project>/BEADS_LEDGER.md" ]; then
  # Read and incorporate prior findings
  cat "docs/plans/<project>/BEADS_LEDGER.md"
fi
```

### Convergence Rules (Beads)

Stop iterating when ALL are true:
1. `BEADS.md` passes schema validation (including bd-format constraints)
2. **Two-pass stability:** 0 blockers in two consecutive full bead reviews
3. **No regressions:** `regression` count is 0

### Anti-Compounding Guardrail

A blocker MUST cite anchored evidence:
- Bead ID: `bead:CORE-02`
- Dependency edge: `edge:CORE-02->DECISION-01`
- Section heading: `section:Error Handling`
- File path: `file:services/web/src/x.ts`
- Missing field: `field:Parallelism in bead:CORE-02`

**If it cannot be anchored, it cannot be a blocker.**

## Output Format

### If APPROVED

```
APPROVED

Ledger pass: N (previous: N-1)
Blockers: 0
Regressions: 0
Convergence: achieved (two-pass stability)
```

### If Issues Found

```markdown
## 1. Summary of Findings

- Total beads: {n}
- Issues found: {n}
- Blockers: {n}
- Regressions: {n}
- Net-new: {n}
- Ready for implementation: yes/no

## 2. Detailed Issues & Fixes

### {IssueId}
- **Sub-agent:** {Coverage|Atomicity|Dependency|Context|Metadata}
- **Classification:** {net-new|known-open|regression|waived}
- **Severity:** {blocker|should-fix|minor}
- **Evidence:** {anchored description}
- **Fix:** {concrete change}

## 3. Spec Coverage Matrix

| Design Requirement | Covered By Beads | Status |
|---|---|---|
| ... | ... | ✓ / ✗ |

## 4. Revised Beads (if needed)

For any bead you changed, include the full revised bead definition in bd-compatible markdown (the entire `## ID: Title` section, including metadata and all subsections).
```

### IssueId Format

Use stable anchored identifiers:
```
bead-review::<type>::<anchor>
```

Examples:
- `bead-review::coverage::section:Rate Limiting`
- `bead-review::atomicity::bead:CORE-02`
- `bead-review::dependency::edge:DB-01->DECISION-01`
- `bead-review::context::api:stripe.charges.create`
- `bead-review::format::bead:CORE-05`

## Common Failure Modes

| Failure Mode | Prevention |
|--------------|------------|
| Running checks sequentially in one agent | Use parallel sub-agents |
| Sub-agents not given full BEADS.md | Each sub-agent reads full file |
| Not deduplicating overlapping findings | Synthesizer merges before output |
| Blockers without anchored evidence | Anti-compounding guardrail |
| Not consuming previous ledger | First action: read ledger |
| Revised beads not bd-compatible | Include full `## ID: Title` section |
