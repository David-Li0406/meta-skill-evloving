---
name: design-orchestrate
description: Run multi-agent pipeline for complete spec-to-PRP workflow. USE WHEN orchestrate, full pipeline, multi-agent, complete workflow.
context: fork
---

# Design Orchestrate

Runs the multi-agent orchestration pipeline for complete spec-to-PRP workflow. Runs in isolated context as it spawns multiple sub-agents and generates extensive intermediate artifacts.

## Why Forked Context

- Spawns multiple sub-agents (spec-analyst, validator, prp-generator, reviewer)
- Generates intermediate files (analysis.json, validation.json)
- Multi-phase execution with detailed logging
- Returns clean summary to main context

## Usage

```
/design-orchestrate specs/feature-spec.md --domain api
/design-orchestrate specs/migration-spec.md --phase analysis
/design-orchestrate specs/api-spec.md --domain integration --output ./output
```

## Phases

| Phase | Agents | Output |
|-------|--------|--------|
| `analysis` | spec-analyst, validator (parallel) | analysis.json, validation.json |
| `generate` | prp-generator | prp-{name}.md |
| `review` | reviewer | review.json |
| `retrospective` | retrospective | retrospective-{name}.md |
| `full` | All phases (default) | All artifacts |

## Architecture

```
                     User Request
                          │
                          ▼
            ┌─────────────────────────┐
            │      Orchestrator       │
            │  (design-orchestrate)   │
            └─────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
   ┌───────────┐   ┌───────────┐   ┌───────────┐
   │spec-analyst│   │ validator │   │CONVENTIONS│
   │           │   │           │   │  check    │
   └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
         │               │               │
         └───────────────┼───────────────┘
                         ▼
               ┌─────────────────┐
               │  prp-generator  │
               └────────┬────────┘
                        ▼
               ┌─────────────────┐
               │    reviewer     │
               └────────┬────────┘
                        │
               ┌────────┴────────┐
               ▼                 ▼
          APPROVED          NEEDS WORK
```

## Execution

**Phase 1: Analysis (Parallel)**
```bash
# Run in parallel
./agents/spec-analyst.sh "{spec}" --domain "{domain}" &
./agents/validator.sh "{spec}" --domain "{domain}" &
wait
```

Output: `analysis.json`, `validation.json`

**Phase 2: Generation**
```bash
./agents/prp-generator.sh "{spec}" \
  --analysis analysis.json \
  --validation validation.json \
  --template "{template}"
```

Output: `prp-{name}.md`

**Phase 3: Review**
```bash
./agents/reviewer.sh "prp-{name}.md"
```

Output: `review.json` with APPROVED or NEEDS_WORK status

**Phase 4: Retrospective (Post-Implementation)**
```bash
./agents/retrospective.sh "prp-{name}.md" --outcome "{summary}"
```

Output: `retrospective-{name}.md`, `invariant-proposals.json`

## Output Format

```
╔═══════════════════════════════════════════════════════════════╗
║      MULTI-AGENT DESIGN OPS ORCHESTRATOR                      ║
╚═══════════════════════════════════════════════════════════════╝

Phase: full
Domain: api
Output: ./output

━━━ Phase 1: Analysis ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[10:23:45] Starting parallel analysis...
[10:23:47] ✓ spec-analyst completed
[10:23:48] ✓ validator completed

Analysis results: Completeness=85%, Thinking=Think
Validation results: Confidence=78%, Violations=0

━━━ Phase 2: Generation ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[10:23:50] ✓ prp-generator completed

━━━ Phase 3: Review ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[10:23:52] ✓ reviewer completed

╔═══════════════════════════════════════════════════════════════╗
║                      ORCHESTRATION COMPLETE                   ║
╚═══════════════════════════════════════════════════════════════╝

Generated Files:
  - analysis.json
  - validation.json
  - prp-feature.md
  - review.json

Status: PRP APPROVED - Ready for implementation
```

## Return to Main Context

After completion, returns concise summary:
```
Orchestration Complete
======================
Spec: specs/feature-spec.md
Domain: api
Phase: full

Results:
- Analysis: Completeness 85%, Thinking level: Think
- Validation: Confidence 78%, 0 violations
- PRP: Generated (Quality 82/100)
- Review: APPROVED

Output: ./output/prp-feature.md

Next: Fill placeholders and begin implementation
```

## Related Commands

- `/design validate` — Run validation phase only
- `/design prp` — Generate PRP (uses shared context for conversational input)
- `/design review` — Run review phase only

---

*Forked skill — multi-agent pipeline isolated from main context*
