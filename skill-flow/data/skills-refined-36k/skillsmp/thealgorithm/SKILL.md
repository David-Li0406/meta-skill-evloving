---
name: THEALGORITHM
description: Universal execution engine using scientific method to achieve ideal state. USE WHEN complex tasks, multi-step work, "run the algorithm", "use the algorithm", OR any non-trivial request that benefits from structured execution with ISC (Ideal State Criteria) tracking.
---

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/CORE/USER/SKILLCUSTOMIZATIONS/THEALGORITHM/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.

# THE ALGORITHM - Universal Execution Engine

**PURPOSE:** Produce euphoric, highly surprising, exceptional results that solve the problem better than expected.

**PHILOSOPHY:** Move from current state to ideal state using the scientific method. The ISC (Ideal State Criteria) captures what "ideal" looks like, which we execute against, verify against, and iterate against until achieved.

**CORE PRINCIPLE:** Effort classification determines which capabilities are available. Higher effort unlocks more powerful tools.

---

## Core Mission

**The goal of The Algorithm—and indeed of the PAI system overall—is to create Euphoric Surprise at its ability to perform every task in service of helping its principal become the best version of themselves.**

This is the north star. Every capability, every phase, every ISC row exists to serve this mission. When the system works correctly, the principal should be genuinely surprised and delighted by how thoroughly, thoughtfully, and effectively their request was fulfilled—not just "done" but done in a way that exceeds expectations and moves them closer to their ideal self.

---

## Quick Start

```bash
# 1. CLASSIFY EFFORT
bun run ~/.claude/skills/THEALGORITHM/Tools/EffortClassifier.ts --request "your request"
# Or with override: --override DETERMINED
# Or inline: "algorithm effort THOROUGH: your request"

# 3. LOAD CAPABILITIES for effort level
bun run ~/.claude/skills/THEALGORITHM/Tools/CapabilityLoader.ts --effort STANDARD

# 4. CREATE ISC
bun run ~/.claude/skills/THEALGORITHM/Tools/ISCManager.ts create --request "your request"

# 5. MANAGE ISC during EXECUTE
bun run ~/.claude/skills/THEALGORITHM/Tools/ISCManager.ts capability --row 1 -c research.perplexity
bun run ~/.claude/skills/THEALGORITHM/Tools/ISCManager.ts update --row 1 --status DONE
bun run ~/.claude/skills/THEALGORITHM/Tools/ISCManager.ts show
```

## Effort → Capability Matrix

**Capabilities.yaml is the source of truth.** See `Data/Capabilities.yaml`.

| Effort | Models | Thinking | Analysis | Research | Execution | Parallel |
|--------|--------|----------|----------|----------|-----------|----------|
| **TRIVIAL** | — | — | — | — | — | 0 |
| **QUICK** | haiku | — | — | — | general-purpose | 1 |
| **STANDARD** | haiku, sonnet | deep thinking | Science | WebSearch | general-purpose, Explore | 1-3 |
| **THOROUGH** | haiku, sonnet | All + Plan Mode | All | WebSearch | All + Plan | 3-5 |
| **DETERMINED** | all + opus | All | All | All | unlimited | 10 |

## ISC Scale (CRITICAL)

**The ISC is NOT limited to a small number of rows.** The ISC captures what "ideal" looks like, and for complex problems this can be massive:

| Scale | When | Examples |
|-------|------|----------|
| **5-10 rows** | Quick fixes, simple features | "Fix typo", "Add button" |
| **20-50 rows** | Standard development work | "Add dark mode", "Create API endpoint" |
| **50-200 rows** | Complex features, refactors | "Redesign auth system", "Add new major feature" |
| **200-1000+ rows** | Major projects, DETERMINED effort | "Build entire system", "Security audit" |

**ISC rows come from:**
- **EXPLICIT requirements** - What user literally asked for
- **INFERRED requirements** - From context (TECHSTACKPREFERENCES, past work, etc.)
- **IMPLICIT requirements** - Security, quality, testing standards
- **Research findings** - Best practices discovered via research agents
- **Anti-patterns** - Things to AVOID discovered via research
- **Edge cases** - Discovered through thinking/analysis
- **Verification criteria** - How to confirm each requirement is met

**The algorithm's capabilities EXPAND the ISC:**
- Research agents find best practices → add ISC rows
- Research agents find anti-patterns → add "avoid X" ISC rows
- Council debate surfaces edge cases → add ISC rows
- Analysis reveals assumptions → add ISC rows
- Verification requirements → add ISC rows for each testable criterion

**Higher effort = larger, higher quality ISC.** The DETERMINED level can have thousands of ISC rows because we use ALL capabilities to discover everything that "ideal" looks like.

## The 7 Phases

Execute IN ORDER. Each phase mutates the ISC:

| Phase | Action | ISC Mutation | Gate Question |
|-------|--------|--------------|---------------|
| **OBSERVE** | Understand request + user context | CREATE rows | Do I have 2+ rows? Used context to infer? |
| **THINK** | Ensure nothing missing | COMPLETE rows | All rows clear, testable? |
| **PLAN** | Sequence + assign capabilities | ORDER rows + ASSIGN capabilities | Dependencies mapped? Capabilities assigned? |
| **BUILD** | Make rows testable | REFINE rows | Each row specific enough to verify? |
| **EXECUTE** | Do the work (spawn agents per capability) | ADVANCE status | Every row has final status? |
| **VERIFY** | Test each DONE row (skeptical agent) | CONFIRM status | Tested/confirmed each completion? |
| **LEARN** | Output for user to rate | OUTPUT results | User rates for memory system |

**CRITICAL:** The LEARN phase does NOT self-rate. User rates outputs for the memory system.

## The ISC Table (FRONT AND CENTER)

Every non-trivial task has an ISC. **Display this prominently throughout execution:**

```markdown
## 🎯 IDEAL STATE CRITERIA

**Request:** Add dark mode to the settings page
**Effort:** STANDARD | **Phase:** EXECUTE | **Iteration:** 1

| # | What Ideal Looks Like | Source | Capability | Status |
|---|----------------------|--------|------------|--------|
| 1 | Research good patterns | INFERRED | 🔬 web_search | ⏳ PENDING |
| 2 | Toggle component works | EXPLICIT | 🤖 general | 🔄 ACTIVE |
| 3 | Theme state persists | EXPLICIT | 🤖 general× | ⏳ PENDING |
| 4 | Uses TypeScript | INFERRED | — | ✅ DONE |
| 5 | Tests pass | IMPLICIT | ✅ verify | ⏳ PENDING |
| 6 | Browser-verified | IMPLICIT | ✅ browser | ⏳ PENDING |

**Legend:** 🔬 Research | 💡 Thinking | 🗣️ Debate | 🔍 Analysis | 🤖 Execution | ✅ Verify | × Parallel
```

**Source types:**
- `EXPLICIT` - User literally said this
- `INFERRED` - Derived from user context (TECHSTACKPREFERENCES, etc.)
- `IMPLICIT` - Universal standards (security, quality)

**Status progression:**
- `PENDING` → `ACTIVE` → `DONE`
- `ADJUSTED` - Modified with reason
- `BLOCKED` - Cannot achieve, triggers loop-back

## Execution Flow

### Step 1: EFFORT CLASSIFICATION (REQUIRED FIRST)

```bash
bun run ~/.claude/skills/THEALGORITHM/Tools/EffortClassifier.ts --request "your request"
```

**Override methods:**
- CLI flag: `--override THOROUGH`
- Inline pattern: `"algorithm effort DETERMINED: build this feature"`

The effort level determines ALL available capabilities.

### Step 2: CAPABILITY LOADING

```bash
bun run ~/.claude/skills/THEALGORITHM/Tools/CapabilityLoader.ts --effort STANDARD
```

Returns available: models, thinking modes, debate systems, research agents, execution agents, verification.

### Step 3: ISC CREATION + CAPABILITY ASSIGNMENT

For each ISC row, select appropriate capability:

```bash
bun run ~/.claude/skills/THEALGORITHM/Tools/CapabilitySelector.ts --row "Research best practices" --effort STANDARD
# Returns: research.perplexity as primary, with icon 🔬

bun run ~/.claude/skills/THEALGORITHM/Tools/ISCManager.ts capability --row 1 -c research.perplexity
```

### Step 4: ORCHESTRATED EXECUTION

Execute in phases based on capability assignments:

```
PHASE A: RESEARCH (parallel for independent queries)
├─ Row with 🔬 research.web_search → Use WebSearch tool
└─ Row with 🔬 research.explore → Spawn Explore agent

PHASE B: THINKING (for creative/analysis needs)
├─ Row with 💡 thinking.deep thinking → Invoke BeCreative skill
└─ Row with 🔍 analysis.science → Invoke Science skill

PHASE C: EXECUTION (parallel agents)
├─ Row with 🤖 execution.general → Spawn general-purpose agent
├─ Row with 🤖 execution.plan → Spawn Plan agent (THOROUGH+)
└─ Rows marked × → Run in parallel

PHASE D: VERIFICATION (skeptical, different from executor)
├─ Row with ✅ verification.browser → Browser skill validation
└─ All rows → Skeptical verification agent (different from executor)
```

### For TRIVIAL (skip algorithm):
Direct response, no ISC, no capability loading. Just answer.

## Capability Categories

### Models (compute resources)
- `models.haiku` - Fast, cheap (QUICK+)
- `models.sonnet` - Balanced reasoning (STANDARD+)
- `models.opus` - Maximum intelligence (DETERMINED)

### Thinking Modes
- `thinking.deep thinking` - BeCreative skill for creative solutions (STANDARD+)
- `thinking.tree_of_thought` - Branching exploration (THOROUGH+)
- `thinking.plan_mode` - EnterPlanMode for complex implementations (THOROUGH+)


### Analysis Modes
- `analysis.science` - Hypothesis-driven exploration (STANDARD+)

### Research
- `research.web_search` - WebSearch tool for web research, current events (STANDARD+)
- `research.explore` - Explore subagent for codebase exploration (STANDARD+)

### Execution (Vanilla Subagent Types)
- `execution.general` - general-purpose for multi-step tasks, research (QUICK+)
- `execution.explore` - Explore for codebase exploration (STANDARD+)
- `execution.plan` - Plan for architecture design (THOROUGH+)


### Verification
- `verification.browser` - Web application validation (STANDARD+)
- `verification.skeptical_verifier` - Different agent than executor (STANDARD+)

## Iteration Loop

When VERIFY finds issues:

```
BLOCKED row
    │
    ├─ Unclear what ideal looks like? → Loop to THINK
    ├─ Wrong approach? → Loop to PLAN
    └─ Execution error? → Loop to EXECUTE

Iteration count bounded by effort level:
- QUICK: 1 iteration max
- STANDARD: 2 iterations
- THOROUGH: 3-5 iterations
- DETERMINED: Unlimited until success
```

## Integration

### Uses
- **CORE Skill** - User context for ISC inference
- **Browser Skill** - Web verification in VERIFY phase
- **BeCreative Skill** - deep thinking for THINK phase

### Memory
- ISC artifacts: `MEMORY/Work/{session}/ISC.md`
- Learnings: `MEMORY/Learning/ALGORITHM/`
- Patterns: `MEMORY/Signals/algorithm-patterns.jsonl`

## Workflow Routing

| Trigger | Action |
|---------|--------|
| "run the algorithm" | Full execution |
| "use the algorithm" | Full execution |
| "algorithm effort LEVEL" | Force effort level + full execution |
| Complex multi-step request | Auto-invoke if appropriate |

## Enhanced ISC Features

### Verification Paired at Creation

**CRITICAL:** Every ISC row should have a verification method defined at creation, not after.

```bash
# Add row WITH verification (recommended)
bun run ISCManager.ts add -d "Toggle component works" -s EXPLICIT \
  --verify-method browser --verify-criteria "Toggle visible in settings"
```

**Verification methods:** browser, test, grep, api, lint, manual, agent, inferred

See `Data/VerificationMethods.yaml` for selection guidance.

### Agent Claim System

Prevents race conditions when multiple agents work on ISC items.

```bash
# Claim an item
bun run ISCManager.ts claim --row 1 --agent Engineer

# Release when done
bun run ISCManager.ts release --row 1

# See what's available
bun run ISCManager.ts available
```

Claims expire after 30 minutes (stale detection).

### Research Override System

Research findings can BLOCK user assumptions. User must acknowledge.

```bash
# Research agent finds issue
bun run ISCManager.ts research-block --row 2 \
  --reason "Best practice is X, not Y" --source research.perplexity

# User acknowledges
bun run ISCManager.ts acknowledge --row 2 --action OVERRIDE  # or ACCEPT
```

### Nested Algorithm

Complex items spawn child ISAs.

```bash
# Mark item as nested
bun run ISCManager.ts nest --row 5

# Update child status
bun run ISCManager.ts child-status --row 5 --child-status COMPLETE
```

### Interview Protocol

When ideal state is unclear, use structured questions.

```bash
bun run ISCManager.ts interview -r "vague request"
```

**The 5 Questions:**
1. What does success look like when this is done?
2. Who will use this and what will they do with it?
3. What would make you show this to your friends?
4. What existing thing is this most similar to?
5. What should this definitely NOT do?

## Files

| File | Purpose |
|------|---------|
| `Data/Capabilities.yaml` | **Source of truth** for all capabilities |
| `Data/VerificationMethods.yaml` | **Verification method registry** |
| `Tools/EffortClassifier.ts` | Classify TRIVIAL→DETERMINED |
| `Tools/CapabilityLoader.ts` | Load + filter capabilities by effort |
| `Tools/CapabilitySelector.ts` | Select capabilities for ISC rows |
| `Tools/ISCManager.ts` | **Enhanced:** ISC with verification, claims, research, nesting |
| `Tools/TraitModifiers.ts` | Effort → trait mappings |
| `Phases/*.md` | Detailed phase documentation (Observe.md has interview protocol) |
| `Reference/CapabilityMatrix.md` | Effort → capability documentation |

## The Purpose

**Produce euphoric, highly surprising, exceptional results that solve the user's problem better than expected.**

The ISC captures what "ideal" looks like. Effort determines available capabilities. Execute against it. Verify against it. Iterate until achieved.

**This is not documentation. This is a command. Execute the algorithm.**
