---
name: fanout
description: This skill should be used for multi-perspective analysis through parallel copilot sessions. Triggers include "analyze from multiple angles", "what are the gaps/patterns/friction", "explore before deciding", pre-refactor landscape mapping, or skill/architecture auditing. Each agent gets a DIFFERENT prompt, results aggregated.
---

# fanout

multi-perspective analysis through parallel copilot sessions. each agent gets a DIFFERENT prompt, results aggregated.

## philosophy

| principle | application |
|-----------|-------------|
| different perspectives | each agent analyzes from unique angle (not same prompt to many) |
| read-only by design | analysis and synthesis ONLY - never modify code or commit |
| parallel execution | spawn all sessions simultaneously, collect when ready |
| structured aggregation | combine diverse insights into actionable synthesis |
| output contracts | all agents return predictable JSON for reliable aggregation |

## when to use

| use | skip |
|-----|------|
| "analyze this from multiple angles" | single-perspective analysis (use pair consult) |
| "what are the gaps/patterns/friction points" | same question to multiple models (use pair group) |
| "explore before deciding" | ready to implement (use loop/auto) |
| pre-refactor landscape mapping | code changes needed (use pair delegate) |
| skill/architecture auditing | orchestrating skills (use skill-compose) |

## decision tree: fanout vs other skills

```
What kind of multi-agent work?
├── Same prompt to different models for consensus?
│   └── use pair --group (gemini + sonnet + codex same question)
├── Different prompts for diverse analysis?
│   └── use FANOUT (gap + pattern + friction + synergy)
├── Orchestrating multiple skills in sequence?
│   └── use skill-compose
├── Discovering and executing work items?
│   └── use auto (ideation → spawn)
├── Single consultation or delegation?
│   └── use pair (consult/delegate/review modes)
└── Long autonomous session with checkpoints?
    └── use loop
```

## decision tree: analysis type selection

```
What analysis perspectives needed?
├── Understanding existing patterns?
│   └── pattern-extraction template
├── Finding missing capabilities?
│   └── gap-analysis template
├── Identifying pain points?
│   └── friction-analysis template
├── Mapping connections between things?
│   └── synergy-mapping template
├── Auditing against platform capabilities?
│   └── platform-audit template
├── Meta-level reflection on approach?
│   └── meta-analysis template
└── Custom analysis?
    └── create ad-hoc prompt with output contract
```

## decision tree: session count

```
How many parallel sessions?
├── Deep dive on single topic?
│   └── 2-3 sessions (focused perspectives)
├── Broad landscape analysis?
│   └── 4-6 sessions (comprehensive coverage)
├── Resource constrained?
│   └── 2-3 sessions (prioritize highest value)
├── Exploratory/unknown scope?
│   └── 3-4 sessions (balanced coverage)
└── Follow-up to prior fanout?
    └── 1-2 sessions (fill specific gaps)
```

## workflow

### phase 1: scope and select

1. identify analysis target (codebase, skill, architecture, etc.)
2. select 3-6 analysis templates based on goal
3. customize templates if needed (target-specific context)

### phase 2: spawn parallel sessions with --await

```bash
# Generate parent ID for this fanout operation
FANOUT_ID="fanout-$(date +%Y%m%d-%H%M%S)-$(openssl rand -hex 4)"

# Build prompts with output contracts
for TEMPLATE in gap pattern friction synergy platform meta; do
  cat templates/${TEMPLATE}-analysis.md | \
    sed "s/\$TARGET/$TARGET/" > /tmp/${TEMPLATE}.md
done

# Spawn all sessions in parallel with --await --parent --timeout
# Each runs in background, awaits completion, writes result
for TEMPLATE in gap pattern friction synergy platform meta; do
  (
    RESULT=$(cat /tmp/${TEMPLATE}.md | \
      agents session start -a copilot -p $PROJECT \
        -g "${TEMPLATE}: $TARGET" \
        --parent "$FANOUT_ID" \
        --timeout 120 \
        --await \
        --json -q)
    echo "$RESULT" >> /tmp/results.jsonl
  ) &
done

# Wait for all background jobs
wait
```

**Key flags**:
- `--await` - blocks until session completes, returns output inline
- `--parent $FANOUT_ID` - links all sessions for hierarchy queries
- `--timeout 120` - auto-kill after 120s (prevents runaway sessions)

### phase 3: validate and filter results

```bash
# Filter successful results (--await returns combined session + await data)
jq -c 'select(.await.status == "completed")' /tmp/results.jsonl > /tmp/valid.jsonl

# Check for failures
FAILED=$(jq -c 'select(.await.status != "completed")' /tmp/results.jsonl | wc -l)
if [ "$FAILED" -gt 0 ]; then
  echo "Warning: $FAILED sessions failed or timed out"
fi

# Query all child sessions via parent hierarchy
agents session list --json -q | \
  jq -r --arg parent "$FANOUT_ID" '.[] | select(.parent_session_id == $parent)'
```

### phase 4: aggregate and synthesize

1. parse all output contracts from valid results
2. extract key findings from each perspective
3. identify patterns across analyses (repeated themes)
4. surface contradictions (where perspectives conflict)
5. synthesize actionable recommendations

## output contract (reused from pair)

all fanout agents MUST return this structure:

```json
{
  "mode": "fanout",
  "analysis_type": "gap | pattern | friction | synergy | platform | meta | custom",
  "status": "success | partial | blocked | failed",
  "summary": "50-200 words",
  "confidence": 8,
  "artifacts": [
    {
      "type": "analysis",
      "content": "structured findings"
    }
  ],
  "sources": {
    "files_read": ["path/to/file.ts:10-50"],
    "tools_used": ["layer", "outline", "grep"]
  },
  "assumptions": ["assumption that could affect correctness"],
  "next_steps": ["recommended follow-up"],
  "blockers": []
}
```

**CRITICAL constraint**: fanout analysis agents must NOT:
- modify files
- create commits
- write to disk (except output contract)
- execute side effects

## analysis templates

| template | purpose | when to use |
|----------|---------|-------------|
| gap-analysis | find missing capabilities | before adding features |
| pattern-extraction | identify existing patterns | before refactoring |
| friction-analysis | surface pain points | improving DX/UX |
| synergy-mapping | find connection opportunities | integration planning |
| platform-audit | check against capabilities | tool utilization review |
| meta-analysis | reflect on approach itself | continuous improvement |

see `templates/` directory for full prompt templates.

## aggregation patterns

### theme extraction

```
collect: all artifact.content from results
group by: repeated concepts/recommendations
output: ranked themes by frequency + confidence-weighted
```

### contradiction surfacing

```
for each pair of results:
  compare: recommendations in next_steps
  identify: conflicting advice
  note: confidence scores of each
output: conflicts with context for resolution
```

### confidence-weighted synthesis

```
for each recommendation across all results:
  weight = confidence * (1 if status=success else 0.5)
  accumulate weights per unique recommendation
output: recommendations sorted by accumulated weight
```

## concrete values

| metric | value | source | rationale |
|--------|-------|--------|-----------|
| default sessions | 4 | heuristic | balances coverage vs cognitive load; 4 perspectives sufficient for most analyses without overwhelming synthesis |
| max sessions | 6 | heuristic | diminishing returns beyond 6; Miller's 7±2 suggests humans struggle synthesizing >7 distinct inputs |
| session timeout | 120s | empirical | copilot + gemini-3-pro completes most prompts in 30-90s; 120s allows buffer without runaway |
| min confidence for inclusion | 5 | convention | midpoint on 1-10 scale; below 5 indicates agent uncertainty too high to trust findings |
| aggregation weight threshold | 0.5 | heuristic | partial/failed results weighted at 50% to include signal without overweighting uncertain data |

**sourcing legend**: `heuristic` = based on practical experience, not formal research; `empirical` = measured from actual tool usage; `convention` = widely adopted standard

## integration with agents CLI

```bash
# Start trace for fanout run
export AGENTS_TRACE_ID=$(agents report start "fanout: $TARGET" --agent claude --json -q | jq -r '.traceId')

# Report progress as sessions complete
agents report progress "3/6 analyses complete" --confidence 7

# Report completion with synthesis (gist captures multi-perspective analysis)
agents report complete "fanout synthesis ready: 6 perspectives, 12 recommendations" --confidence 9 --gist

# If blocked
agents report blocked "2 sessions timed out" --blocker-type error
```

## session spawning pattern

**IMPORTANT**: use `agents session start` NOT direct `copilot` calls.

```bash
# Correct: --await blocks until completion, returns output inline
RESULT=$(cat prompt.md | agents session start -a copilot -p $PROJECT \
  -g "analysis" \
  --parent "$FANOUT_ID" \
  --timeout 120 \
  --await \
  --json -q)

# Result contains both session info and await output:
# { "session_id": "...", "await": { "status": "completed", "output": "..." } }
STATUS=$(echo "$RESULT" | jq -r '.await.status')
OUTPUT=$(echo "$RESULT" | jq -r '.await.output')

# Wrong: no tracking, no parent correlation, loses result
copilot -p --model gemini-3-pro "prompt"
```

## error handling

| failure | detection | mitigation |
|---------|-----------|------------|
| session timeout | `await.status == "timeout"` or exit_code=143 | skip, note in synthesis |
| session failed | `await.status == "failed"` | check await.error, report |
| parse error | JSON extraction from await.output fails | include raw text, flag as unstructured |
| low confidence | confidence < 5 in output contract | weight down in aggregation |
| status: failed | explicit failure in contract | exclude from synthesis, report |
| partial results | status: partial in contract | include with caveat |

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| same prompt to all | defeats purpose, use pair group | different template per session |
| modifying code | violates read-only | use pair delegate for changes |
| skipping output contract | can't aggregate | always include contract in prompt |
| sequential spawning | slow, wastes parallelism | spawn all then collect |
| ignoring low-confidence | missing nuanced signals | include with weight, don't discard |
| too many sessions | resource waste | cap at 6, prioritize templates |
| no trace correlation | invisible in trails | always use agents report |

## composition with other skills

### fanout → pair

```
1. fanout: multi-perspective analysis
2. synthesize findings
3. pair consult: validate synthesis with human or senior model
4. pair delegate: implement selected recommendations
```

### ask-deep → fanout

```
1. ask-deep: clarify scope and priorities
2. fanout: deep analysis from multiple angles
3. synthesize: present findings
4. ask-deep review: validate findings with user
```

### fanout → loop

```
1. fanout: landscape analysis before work
2. synthesize: prioritized action items
3. loop: autonomous implementation with findings as context
```

## template summaries

| template | lines | key sections | when to use |
|----------|-------|--------------|-------------|
| gap-analysis | 66 | explore current state → identify expected capabilities → surface gaps → prioritize by impact | before adding features; comparing to mature projects |
| pattern-extraction | 68 | explore codebase → identify coding patterns → identify architectural patterns → document each | pre-refactor; understanding conventions |
| friction-analysis | 69 | explore workflow → identify friction categories (setup/build/test/debug/deploy/cognitive) → assess severity | improving DX; reducing development time |
| synergy-mapping | 68 | identify components → map current integrations → find missing connections → assess synergy value | integration planning; finding opportunities |
| platform-audit | 67 | inventory tools → audit utilization → identify underused capabilities → compare to best practices | tool review; capability discovery |
| meta-analysis | 70 | examine approach → identify assumptions → surface blind spots → recommend improvements | continuous improvement; retrospectives |

all templates include: `<role>`, `<context>`, `<task>`, `<constraints>` (READ-ONLY), and `<output_contract>` (JSON)

## reference summaries

| reference | lines | key content |
|-----------|-------|-------------|
| aggregation.md | 309 | theme extraction algorithms, contradiction surfacing logic, confidence-weighted synthesis, tie-breaking rules |
| failure-modes.md | 376 | timeout handling, parse errors, low confidence, partial results, session failures, recovery strategies |
| prompt-design.md | 229 | output contract structure, variable substitution, constraint patterns, effective role definitions |

## tool integration

| tool | command | purpose |
|------|---------|---------|
| agents | `agents session start --await --parent`, `agents report` | parallel session spawning, trace correlation |
| copilot | (via agents session) | analysis sessions |
| jq | `jq -c 'select(.await.status == "completed")'` | JSON parsing and filtering |
| layer | `layer . --format=json` | architecture analysis in prompts |
| outline | `outline --callers`, `outline --unused` | code structure analysis in prompts |
| trails | `agents report` (unified) | fanout history persistence |

### trails integration

fanout uses `agents report` which handles trails internally:

```bash
# Start fanout trace
export AGENTS_TRACE_ID=$(agents report start "fanout: $TARGET" --agent claude --json -q | jq -r '.traceId')

# Progress updates
agents report progress "4/6 analyses complete" --confidence 7

# Complete with synthesis (gist for permanent artifact)
agents report complete "fanout: $COUNT perspectives, $RECS recommendations" --confidence 9 --gist

# Query fanout history
trails trail replay --format json | jq '.[] | select(.task | contains("fanout"))'
```

**trails enables**:
- tracking analysis patterns over time
- measuring session success/timeout rates
- correlating fanout findings with implementation outcomes

### tooling requirements

| tool | required | purpose | fallback |
|------|----------|---------|----------|
| `agents` CLI | yes | session spawning with --await, trace correlation | none (core to fanout) |
| `jq` | yes | JSON parsing and filtering | none (install with `brew install jq`) |
| `openssl` | optional | random ID generation | use `date +%s` or `uuidgen` |
| `layer` | recommended | architecture analysis in prompts | `find . -name "package.json"` |
| `outline` | recommended | code structure analysis in prompts | `grep -rn "export"` |

## references

- [templates/gap-analysis.md](templates/gap-analysis.md) - capability gap detection
- [templates/pattern-extraction.md](templates/pattern-extraction.md) - existing pattern discovery
- [templates/friction-analysis.md](templates/friction-analysis.md) - pain point surfacing
- [templates/synergy-mapping.md](templates/synergy-mapping.md) - connection identification
- [templates/platform-audit.md](templates/platform-audit.md) - tool utilization review
- [templates/meta-analysis.md](templates/meta-analysis.md) - approach reflection
- [references/prompt-design.md](references/prompt-design.md) - effective prompt construction
- [references/aggregation.md](references/aggregation.md) - synthesis algorithms
- [references/failure-modes.md](references/failure-modes.md) - common issues and fixes
