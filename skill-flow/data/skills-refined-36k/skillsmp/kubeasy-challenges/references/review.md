# Review a Challenge

Evaluate Kubeasy challenges for pedagogical quality, validation coherence, and bypass resistance.

## Sub-Agent Pattern

**Critical**: Challenge review MUST be performed by a sub-agent with fresh context.

### Why Sub-Agent?

1. **No prior knowledge**: The reviewer must discover the solution like a real user
2. **Unbiased evaluation**: Can't be influenced by knowing how the challenge was built
3. **Realistic simulation**: Fresh context forces genuine investigation

### Invoking the Sub-Agent

Use Claude's Task tool to spawn a sub-agent with the instructions from [agents/reviewer.md](../agents/reviewer.md).

```
Task: Review Kubeasy challenge "<slug>"

Agent instructions: Load and follow agents/reviewer.md

Input:
  slug: <slug>

Output:
  /tmp/challenge-review-<slug>.json
```

The agent will:
1. Read challenge.yaml (description only, not manifests)
2. Start and investigate the challenge
3. Attempt to solve (max 5 attempts)
4. Score and document findings

## What the Agent Does

See [agents/reviewer.md](../agents/reviewer.md) for full details. Summary:

1. **Phase 1**: Read challenge.yaml (description only)
2. **Phase 2**: Start the challenge
3. **Phase 3**: Investigate with kubectl
4. **Phase 4**: Attempt resolution (max 5 tries)
5. **Phase 5**: Evaluate and score
6. **Phase 6**: Write JSON report

## Score Interpretation

| Score | Rating | Action |
|-------|--------|--------|
| 18-20 | Excellent | Ready to publish |
| 14-17 | Good | Minor tweaks needed |
| 10-13 | Needs work | Revise before publishing |
| <10 | Major issues | Significant redesign required |

## Batch Review

To review all challenges:

```python
import os
import json

challenges_dir = "/Users/paul/Workspace/kubeasy/challenges"
slugs = [d for d in os.listdir(challenges_dir) 
         if os.path.isdir(os.path.join(challenges_dir, d)) 
         and not d.startswith('.')]

for slug in slugs:
    # Spawn sub-agent for each (with fresh context)
    pass

# Aggregate results
results = []
for slug in slugs:
    report_path = f"/tmp/challenge-review-{slug}.json"
    if os.path.exists(report_path):
        with open(report_path) as f:
            results.append(json.load(f))

# Sort by score
results.sort(key=lambda x: x.get('score', 0))
```

## Red Flags

Issues requiring immediate attention:

| Flag | Meaning | Action |
|------|---------|--------|
| `bypassed: true` | Challenge was trivially bypassed | Add Kyverno policies |
| `coherent: false` | Validation doesn't match goal | Fix objectives |
| `attempts: 5` + `passed: false` | May be unsolvable | Review difficulty/docs |
| `score < 10` | Major quality issues | Redesign challenge |
