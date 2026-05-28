---
name: skill-compose
description: This skill should be used when orchestrating multiple skills together for complex workflows. Triggers include "chain these skills", "use X then Y skill", "multi-skill workflow", "which skills", "suggest skills", or when a task requires capabilities from several skills. Handles skill selection (plan mode) and execution with data flow and aggregated validation.
---

# skill-compose

unified skill orchestration: plan optimal chains AND execute them. replaces both skill-chain (decision) and skill-compose (execution).

## philosophy

> "the whole is greater than the sum of its skills"

| principle | application |
|-----------|-------------|
| composition over complexity | chain simple skills, don't create mega-skills |
| decisive by default | propose ONE chain with confidence, not a menu |
| explicit handoffs | clear data flow between skills |
| aggregated validation | validate the chain, not just individual skills |
| fail-fast | stop chain on skill failure |

## modes

| mode | trigger | behavior |
|------|---------|----------|
| **plan** | "which skills", "suggest skills" | propose optimal chain, don't execute |
| **execute** | "chain these skills", "use X then Y" | run the full chain with handoffs |
| **auto** | task description | plan + execute if confidence >= 7 |

## when to use

| use | skip |
|-----|------|
| task needs multiple skill capabilities | single skill sufficient |
| "which skills should I use" | skill already invoked |
| "do X then Y" requests | skills are independent |
| complex multi-step workflows | simple sequential tasks |
| unclear optimal approach | creating new skill instead |

## decision tree: mode selection

```
What mode?
├── User asks "which skills" or "suggest skills"?
│   └── mode: plan (propose only)
├── User says "chain", "use X then Y", "run workflow"?
│   └── mode: execute
├── Task description with implied skills?
│   └── mode: auto
│       ├── confidence >= 7 → plan + execute
│       └── confidence < 7 → plan + ask
└── Default
    └── mode: auto
```

## decision tree: chain selection (plan mode)

```
What chain fits best?
├── User explicitly named skills?
│   └── Use those skills, add only required pre/post steps
├── Has a Linear issue or PR URL?
│   ├── Linear issue → issue-context → loop
│   └── PR URL → pr-audit
├── Needs clarification before execution?
│   └── ask-deep → [execution skill]
├── Needs autonomous implementation?
│   └── loop (+ pr-audit if merge-bound)
├── Needs external AI validation?
│   └── pair (mode based on intent)
├── Multi-hour work with guardrails?
│   └── loop → context checkpoint → slack
└── Unsure / multiple candidates?
    └── pair quick to resolve
```

## decision tree: chain length

```
How deep should the chain be?
├── Single clear skill? → use it only
├── Two-step (prep → execute)? → add one prep
├── Three-step (prep → execute → validate)? → add validator
├── Chain > 3 skills?
│   ├── Does it require orchestration? → proceed with care
│   └── No → simplify, remove weakest link
└── Confidence < 7?
    └── ask 1 question or invoke pair quick
```

## decision tree: composition pattern

```
What's the relationship between skills?
├── Sequential (output feeds input)
│   └── Chain: skill-A → skill-B → skill-C
├── Parallel (independent analysis)
│   └── Fan-out: input → [A, B, C] → aggregate
├── Validation wrapper
│   └── Sandwich: validate → work → validate
└── Iterative refinement
    └── Loop: work → check → work → check
```

## routing table (quick reference)

| signal | chain |
|--------|-------|
| Linear issue | `issue-context → loop` |
| "improve skill X" | `skill-improve → pair` |
| "create skill" | `ask-deep → skill-create` |
| PR URL | `pr-audit` |
| "quick" / "fast" | `pair quick` |
| "thorough" / "deep" | `pair thorough` |
| "pair with codex" | `pair` (implement mode) |
| new feature, unclear reqs | `ask-deep → loop` |
| scaffold UI | `emil-kowalski` (use /scaffold-dashboard prompt for dashboards) |
| notification needed | `[work] → slack` or `imessage` |
| multi-hour autonomy | `loop → context checkpoint → slack` |
| multi-perspective analysis | `fanout` (gap + pattern + friction in parallel) |

## skill inventory

```
skills (20):
├── orchestration/  loop, pair, fanout, auto
├── context/        context (journal, checkpoint, handoff modes)
├── meta/           skill-create, skill-improve, skill-audit, skill-compose, metaprompt-factory
├── review/         pr-audit, project-review
├── analysis/       friction-analysis
├── clarify/        ask-deep
├── enrich/         issue-context
├── testing/        test-pilot
├── persona/        emil-kowalski
├── connections/    slack, imessage
└── docs/           agent-docs-audit
```

## workflow

### plan mode

```bash
# 1. gather context
# - user prompt/intent
# - session history
# - working directory
# - recent tool outputs

# 2. match against routing table (exact signals first)

# 3. score candidates if no exact match
# - trigger match (0-10)
# - context fit (0-10)
# - composition potential

# 4. output plan
```

**high confidence (>=7):**

```markdown
**chain:** skill-a → skill-b → skill-c
**why:** [1-2 sentences citing context signals]
**confidence:** X/10
```

**low confidence (<7):**

```markdown
**chain:** skill-a → skill-b
**why:** [reasoning]
**confidence:** X/10
**uncertainty:** [what's unclear]
```

### execute mode

```bash
# 1. identify required capabilities
Task: "improve a skill and notify me when done"

Required capabilities:
├── skill improvement → skill-improve
├── validation → pair thorough
└── notification → slack

# 2. determine sequence
dependency analysis:
- skill-improve needs skill to exist ✓
- pair thorough needs improved skill → after skill-improve
- notification needs result → after validation

sequence: skill-improve → pair thorough → slack

# 3. define handoffs
| from | to | data passed |
|------|-----|-------------|
| skill-improve | pair thorough | improved SKILL.md content |
| pair thorough | slack | validation result JSON |

# 4. execute chain
# step 1: improve
# [run skill-improve workflow]

# step 2: validate
# [run pair thorough]

# step 3: notify
echo "Skill improved. Validation: $VALIDATION" | slack dm send --user luke

# 5. aggregate validation
```

### auto mode

```bash
# 1. run plan mode
# 2. if confidence >= 7, execute immediately
# 3. if confidence < 7, present plan and ask
```

## composition patterns

### sequential chain

```
skill-A → skill-B → skill-C

example: skill-create → skill-improve → pair thorough
         (create)     (improve)       (validate)
```

### validation sandwich

```
pair quick → skill-A → pair quick
(pre-check)    (work)    (post-check)

example: pair quick → loop → pair quick
         (approach ok?)  (implement) (result ok?)
```

### parallel fan-out

```
         ┌→ skill-A
input →──┼→ skill-B
         └→ skill-C
              ↓
          aggregate

example: issue arrives
         ├→ issue-context (enrich)
         ├→ pair quick (approach)
         └→ test-pilot (test plan)
              ↓
          combined context for loop
```

**For multi-perspective analysis**, see the `fanout` skill which runs different analysis prompts (gap, pattern, friction, synergy) in parallel and aggregates findings.

## common compositions

| workflow | chain |
|----------|-------|
| skill creation pipeline | skill-create → skill-improve → pair thorough |
| autonomous work with notification | loop → pr-audit → slack |
| research and synthesis | ask-deep → metaprompt-factory → pair quick |
| issue to implementation | issue-context → loop → pr-audit → slack |
| context-aware handoff | context handoff → pair → context delivery |

## execution modes

### synchronous (default)

```
skill-A (3min) → skill-B (2min) → skill-C (1min) = 6min total
```

### parallel where possible

```
         ┌→ skill-A (3min) ─┐
input →──┤                  ├→ aggregate (1min) = 4min total
         └→ skill-B (2min) ─┘
```

### background with callback

```
loop (background) → on_complete: slack notify
```

## concrete values

| metric | value | source |
|--------|-------|--------|
| confidence thresholds | >=7 proceed, 5-6 ask, <5 pair quick | routing calibration |
| pair quick depth | 1-2 min | pair skill |
| pair thorough depth | 10-30 min | pair skill |
| loop depth | 30 min - hours | loop skill |
| skill-improve depth | 20-60 min | skill-improve |
| max chain length | 3-4 skills | cognitive load |

## confidence calibration

| score | meaning | action |
|-------|---------|--------|
| 9-10 | exact signal match | plan + execute immediately |
| 7-8 | strong fit, minor ambiguity | plan + execute, note assumptions |
| 5-6 | multiple valid paths | plan + ask 1 clarifying question |
| <5 | insufficient context | plan + invoke pair quick |

## error handling

### fail-fast (default)

```
skill-A → skill-B (fails) → STOP
                          ↓
                    notify failure
```

### retry with backoff

```
skill-A → skill-B (fails) → retry (1s) → retry (2s) → fail
```

### fallback chain

```
skill-A → skill-B (fails) → skill-B-fallback → skill-C
```

## slack notifications

**skill-compose notifies #agents** at chain lifecycle points:

```bash
# 1. START: when chain begins
slack agent post --agent claude --channel agents \
  --text "compose: starting $CHAIN_NAME ($SKILL_COUNT skills)" -w saya

# 2. COMPLETE: when chain finishes
slack agent post --agent claude --channel agents \
  --text "compose: done $CHAIN_NAME - $STATUS ($DURATION)" -w saya

# 3. ERROR: on chain failure
slack agent post --agent claude --channel agents \
  --text "compose: failed $CHAIN_NAME at $FAILED_SKILL ($ERROR)" -w saya
```

## gap detection

if the task repeatedly hits a missing capability, route to `skill-create`:

- memory/persistence layer → `context` skill
- verification skill → `test-pilot`
- skill health telemetry → `skill-telemetry`

## tool integration

| tool | command | purpose |
|------|---------|---------|
| slack | `slack agent post --agent claude` | chain lifecycle notifications |
| trails | `trails trail record` | chain history, trace correlation |
| agents | `agents session start` | spawn sub-agents for skills |
| pair | via skill invocation | validation, implementation delegation |

### trails integration

persist chain execution for debugging and optimization:

```bash
# record chain start
TRACE=$(trails trail record --agent claude --new-trace --action started \
  --task "skill-compose: $CHAIN_NAME" --json -q | jq -r '.trace_id')

# record chain completion
trails trail record --agent claude --trace-id $TRACE --action completed \
  --task "chain done: $SKILL_COUNT skills, $DURATION" --confidence $CONFIDENCE --json -q
```

**trails enables**:
- tracking chain success rates
- identifying slow skill combinations
- correlating failures across chains

## references

- [references/composition-examples.md](references/composition-examples.md) - detailed examples
- [references/handoff-patterns.md](references/handoff-patterns.md) - data flow patterns
- [references/skill-inventory.md](references/skill-inventory.md) - complete catalog (merged from skill-chain)
- [references/chain-examples.md](references/chain-examples.md) - annotated patterns (merged from skill-chain)

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| mega-skill | one skill tries to do everything | compose simpler skills |
| multiple options | analysis paralysis | propose ONE chain with confidence |
| no confidence | hides uncertainty | always include X/10 |
| implicit handoffs | unclear data flow | document handoff explicitly |
| no aggregated validation | individual passes, chain fails | validate the whole chain |
| ignore failures | chain continues after error | fail-fast by default |
| sequential when parallel possible | slower than needed | identify independent skills |
| deep chain for simple task | unnecessary overhead | strip to single skill |
| proceeding when uncertain | wrong chain | ask 1 question or pair quick |
