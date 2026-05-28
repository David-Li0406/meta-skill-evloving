# EXECUTE Phase

**Purpose:** DO the work - spawn agents based on assigned capabilities for each ISC row.

**ISC Mutation:** STATUS changes (PENDING → ACTIVE → DONE/ADJUSTED/BLOCKED)

**Gate Question:** All rows addressed? Capabilities executed properly?

## What Happens

1. **Execute by capability phase** - Research first, then thinking, then execution
2. **Update status in real-time** - Mark ACTIVE when starting, DONE when complete
3. **Spawn agents based on assigned capabilities** - Use Task tool with appropriate subagent_type
4. **Handle blockers** - Mark BLOCKED with reason if stuck
5. **Run parallel rows simultaneously** - Rows marked × execute concurrently

## Capability-Based Execution Flow

Execute ISC rows in phases based on their assigned capabilities:

```
PHASE A: RESEARCH (first - parallel)
├─ 🔬 research.web_search → WebSearch tool
└─ 🔬 research.explore → Task(subagent_type: Explore)

PHASE B: THINKING (synthesis - sequential)
├─ 💡 thinking.deep thinking → Deep reasoning
├─ 💡 thinking.tree_of_thought → Branching exploration
└─ 🔍 analysis.science → Hypothesis-driven exploration

PHASE C: EXECUTION (implementation - parallel where marked)
├─ 🤖 execution.general → Task(subagent_type: general-purpose, model: haiku)
├─ 🤖 execution.explore → Task(subagent_type: Explore)
├─ 🤖 execution.plan → Task(subagent_type: Plan)
└─ 🔄 execution.ralph_loop → RalphLoopExecutor (iterative until success)

PHASE D: VERIFICATION (validation - last)
├─ ✅ verification.browser → Skill(Browser)
└─ ✅ verification.skeptical_verifier → Task with skeptical verification prompt
```

## Spawning Agents by Capability

### Research

```typescript
// For rows with research.* capability
// Use WebSearch for web research
WebSearch({ query: "best practices for [topic]" })

// Use Explore for codebase research
Task({
  description: "Explore: [ISC row description]",
  prompt: "[Row description] - find relevant code patterns",
  subagent_type: "Explore",
  model: "sonnet"
})
```

### Execution Agents

```typescript
// For rows with execution.* capability
Task({
  description: "Execute: [ISC row description]",
  prompt: "[Row description] - implement this requirement",
  subagent_type: "general-purpose",
  model: "sonnet"
})
```

### Ralph Loop Execution (🔄)

For ISC rows assigned `execution.ralph_loop` - persistent iteration until success:

```bash
# Start a Ralph loop for an ISC row
bun run ~/.claude/skills/THEALGORITHM/Tools/RalphLoopExecutor.ts \
  --prompt "Fix the auth bug until all tests pass" \
  --completion-promise "All tests pass" \
  --max-iterations 15 \
  --isc-row 3
```

**How Ralph Loop works:**
1. Creates state file with prompt and completion criteria
2. Claude works on the task, tries to exit
3. Stop hook intercepts exit and feeds SAME prompt back
4. Claude sees previous work in files/git history
5. Loop continues until:
   - Completion promise detected in `<promise>PROMISE_TEXT</promise>` tags
   - Max iterations reached

**When to use Ralph Loop:**
- Tasks requiring iteration until tests pass
- Bug fixes that need multiple attempts
- Refactoring that benefits from progressive improvement
- Any task with clear, verifiable success criteria

**ISC Status for Ralph rows:**
- `⏳ PENDING` - Not started
- `🔄 LOOPING` - Ralph loop active (custom status)
- `✅ DONE` - Completion promise detected
- `🚫 BLOCKED` - Max iterations exhausted without success

**Monitoring Ralph loops:**
```bash
# Check status
bun run ~/.claude/skills/THEALGORITHM/Tools/RalphLoopExecutor.ts --status

# Cancel loop
bun run ~/.claude/skills/THEALGORITHM/Tools/RalphLoopExecutor.ts --cancel
```

**Keywords that trigger Ralph Loop assignment:**
- "iterate until", "keep trying", "until tests pass"
- "until it works", "persistent", "retry until"
- "loop until", "ralph", "keep iterating"

## Parallel Execution

Rows marked with × (parallel) can be executed simultaneously:

```typescript
// Multiple agents in single response = parallel execution
Task({ description: "Row 1", subagent_type: "general-purpose", run_in_background: true })
Task({ description: "Row 2", subagent_type: "general-purpose", run_in_background: true })
Task({ description: "Row 3", subagent_type: "general-purpose", run_in_background: true })
```

**Max concurrent by effort level:**
| Effort | Max Parallel |
|--------|--------------|
| QUICK | 1 |
| STANDARD | 3 |
| THOROUGH | 5 |
| DETERMINED | 10 |

**Parallelization rules:**
- Research tasks = usually parallelizable
- Independent implementation tasks = parallelizable
- Sequential dependencies = NOT parallelizable
- Rows with × suffix on capability = parallelizable

## Status Updates

```bash
# Mark row as active (starting work)
bun run ISCManager.ts update --row 1 --status ACTIVE

# Mark row as done
bun run ISCManager.ts update --row 1 --status DONE

# Mark row as blocked
bun run ISCManager.ts update --row 1 --status BLOCKED --reason "Missing API key"

# Mark row as adjusted (scope changed)
bun run ISCManager.ts update --row 1 --status ADJUSTED --reason "Used REST instead of GraphQL"
```

## Example Execution

**ISC before EXECUTE:**
```markdown
| # | What Ideal Looks Like | Capability | Status |
|---|----------------------|------------|--------|
| 1 | Research good patterns | 🔬 web_search× | ⏳ PENDING |
| 2 | Explore codebase patterns | 🔬 explore× | ⏳ PENDING |
| 3 | Synthesize findings | 💡 deep thinking | ⏳ PENDING |
| 4 | Implement component | 🤖 general× | ⏳ PENDING |
| 5 | Implement styling | 🤖 general× | ⏳ PENDING |
| 6 | Browser verify | ✅ browser | ⏳ PENDING |
```

**Execution flow:**

**Phase A: Research (parallel)**
```typescript
// Both run in background simultaneously
WebSearch({ query: "component design patterns" })
Task({ description: "Explore patterns", subagent_type: "Explore", run_in_background: true })
```
→ Wait for both to complete → Mark rows 1, 2 DONE

**Phase B: Thinking**
→ Synthesize research findings into design approach
→ Mark row 3 DONE

**Phase C: Execution (parallel where marked)**
```typescript
// Parallel implementation
Task({ description: "Implement component", subagent_type: "general-purpose", run_in_background: true })
Task({ description: "Implement styling", subagent_type: "general-purpose", run_in_background: true })
```
→ Wait for both → Mark rows 4, 5 DONE

**Phase D: Verification**
```typescript
Skill({ skill: "Browser", args: "Verify component renders correctly" })
```
→ Mark row 6 DONE

**ISC after EXECUTE:**
```markdown
| # | What Ideal Looks Like | Capability | Status |
|---|----------------------|------------|--------|
| 1 | Research good patterns | 🔬 web_search× | ✅ DONE |
| 2 | Explore codebase patterns | 🔬 explore× | ✅ DONE |
| 3 | Synthesize findings | 💡 deep thinking | ✅ DONE |
| 4 | Implement component | 🤖 general× | ✅ DONE |
| 5 | Implement styling | 🤖 general× | ✅ DONE |
| 6 | Browser verify | ✅ browser | ✅ DONE |
```

## Commands

```bash
# Update phase
bun run ISCManager.ts phase -p EXECUTE

# Start a row
bun run ISCManager.ts update --row 1 --status ACTIVE

# Complete a row
bun run ISCManager.ts update --row 1 --status DONE

# Check progress
bun run ISCManager.ts summary

# View current ISC
bun run ISCManager.ts show
```

## Exit Criteria

- All rows have been attempted
- Capabilities executed in correct phase order
- Each row is DONE, ADJUSTED, or BLOCKED
- No row left in PENDING or ACTIVE state
- Ready for VERIFY phase
