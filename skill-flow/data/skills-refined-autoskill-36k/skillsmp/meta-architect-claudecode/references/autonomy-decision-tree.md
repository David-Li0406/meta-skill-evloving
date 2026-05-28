# Autonomy Decision Tree

## Table of Contents

- [The 5-Step Autonomy Policy](#the-5-step-autonomy-policy)
- [Autonomy Design Checklist](#autonomy-design-checklist)

Skills should be **autonomous by default** — they should complete without questions in 80-95% of expected cases.

## The 5-Step Autonomy Policy

### Step 0: Check Tool Load (Pre-Execution)

Before any autonomous action, verify MCP configuration is appropriate for the task scope.

**Action:**
- Check `.mcp.json` for project-scope MCP configuration
- Verify only task-relevant MCPs are configured
- Comment out or move unused MCPs to local scope

**Scope Decision:**
- **Plugin authoring tasks** → Project scope: file-search, simplewebfetch only
- **Research/verification tasks** → Project scope: browser, deepwiki, simplewebfetch
- **Validation/review tasks** → Project scope: file-search, LSP (if needed)
- **Cross-project utilities** → User scope: ONLY for truly universal tools

**Configuration edits** (requires Claude Code restart):
```json
// .mcp.json - Authoring phase
{
  "mcpServers": {
    "file-search": { "command": "..." },
    "simplewebfetch": { "command": "..." }
    // "browser": { ... } // Comment out for authoring
    // "deepwiki": { ... } // Comment out for authoring
  }
}
```

**Why this matters:**
- Prevents tool definitions from exceeding 10% context threshold
- Avoids automatic Tool Search activation (adds overhead)
- Reduces context rot during long sessions
- Improves reliability of autonomous workflows

**For detailed MCP scope management**: See [common.md](common.md#context-window-management)

### Step 1: Classify (No Questions)

Before taking any action, classify the task to understand the budget and approach.

**Task Type Classification:**
- **Analysis**: Read-only exploration, pattern recognition, documentation synthesis
- **Modification**: Code changes, refactoring, feature implementation
- **Risky Execution**: Deployments, migrations, destructive operations

**Criticality Assessment:**
- **High**: Data loss, security impact, production changes, costly operations
- **Medium**: Breaking changes to non-critical systems, moderate time cost
- **Low**: Reversible changes, local development, fast operations

**Variability Assessment:**
- **Low**: Same steps every time (deployment, test execution)
- **Medium**: Some variation but predictable patterns (code review, refactoring)
- **High**: Highly contextual (creative work, architecture decisions)

**Define Budget:**
- Target: 1-2 top-level prompts maximum
- Max: 3 subagents per task, 2 correction cycles per file
- Immediate stop if criteria met mid-execution

### Step 2: Explore First

Before asking questions, use safe, low-cost discovery actions.

**Safe Exploration Actions:**
- `Read` — Read files to understand structure
- `Grep` — Search for patterns across codebase
- `Glob` — Find files by pattern
- Structure inspection — Analyze imports, dependencies, file organization

**Resolve Ambiguity:**
- Use discovery instead of questions
- Infer from existing code patterns
- Check for similar implementations in the codebase

### Step 3: Can Proceed Deterministically?

Ask: Do I have enough information to complete the task without questions?

**If YES:** Execute the complete workflow with explicit success criteria:
- Define what "done" looks like
- Execute all steps
- Verify against success criteria
- Report completion

**If NO:** Continue to Step 4

### Step 4: Question Burst (Rare, Contractual)

Questions are authorized ONLY when ALL THREE conditions are true:

**Condition 1: Information NOT Inferrable**
- The information cannot be discovered through read/grep/inspection
- The information is not in documentation or code patterns
- The information is genuinely missing from the context

**Condition 2: High Impact if Wrong Choice**
- Wrong choice would cause significant rework
- Wrong choice would introduce security issues
- Wrong choice would break core functionality
- Wrong choice would be costly (time, money, data)

**Condition 3: Small Set Unlocks Everything**
- 3-7 questions maximum
- Answers enable deterministic completion
- No follow-up questions expected after burst

**Example Valid Question Burst:**
```
I need to know the deployment configuration:

1. What is the target environment? (staging/production)
2. Should database migrations run automatically? (yes/no)
3. Should the deployment trigger a health check? (yes/no)

These 3 answers will enable me to complete the deployment workflow.
```

**Example Invalid Question Burst:**
```
Which files should I refactor?  (Violates Condition 1 — can be discovered via grep)
What color should the button be?  (Violates Condition 2 — low impact)
Should I add a space here? And here? And here?  (Violates Condition 3 — not a small set)
```

### Step 5: Escalate

When autonomy is not appropriate, recommend escalation:

**Recommend Command When:**
- User control is required (deployments, releases, migrations)
- Tool constraints are strict (read-only review, audit)
- Operation is costly/long (full repo audit, large data processing)
- Stable entrypoint needed ("run tests", "build")

**Recommend Fork/Subagent When:**
- Noise isolation is needed (exploration, log triage, extensive grep)
- Parallel execution is beneficial (independent tasks)
- Separate context window is required (state isolation)
- Long-running operations (background processing)

## Autonomy Design Checklist

**Before Building:**
- [ ] What ambiguity can be resolved through exploration (read/grep)?
- [ ] What truly requires user input (cannot be inferred)?
- [ ] What are the explicit success/stop criteria?
- [ ] Which fork pattern matches the use case?

**Question Burst Test:**
- [ ] Information NOT inferrable from repo/tools?
- [ ] High impact if wrong choice?
- [ ] Small set (3-7 max) unlocks everything?

**If any "no":** Encode decision tree instead of asking

**Escalation Criteria:**
- [ ] Explicit control needed → Recommend command
- [ ] Noise/isolation needed → Recommend fork/subagent
