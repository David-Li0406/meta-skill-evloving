---
name: evolve
description: Self-evolving skill system for Univrs.io ecosystem. Observes skill execution, integrates critique feedback, and generates skill improvements. Use /evolve to trigger skill evolution cycle.
allowed-tools: Read, Glob, Grep, Bash(git:*), Bash(gh:*), Write, Edit, WebFetch
---

# Skill Evolution System

This skill creates a **feedback loop** that enables the ecosystem to evolve itself with minimal architect guidance.

## Purpose

Transform insights from `/ecosystem-health` and `/critique` into concrete skill improvements. The system observes, learns, and proposes changes—the architect reviews and merges.

## The Evolution Loop

```
┌─────────────────────────────────────────────────────────────────────┐
│                     SKILL EVOLUTION CYCLE                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐      │
│    │  /ecosystem- │     │              │     │              │      │
│    │   health     │────►│  /critique   │────►│  /evolve     │      │
│    │              │     │              │     │              │      │
│    └──────────────┘     └──────────────┘     └──────┬───────┘      │
│           ▲                                         │              │
│           │                                         ▼              │
│           │                                  ┌──────────────┐      │
│           │                                  │ Generate PR  │      │
│           │                                  │ with skill   │      │
│           │                                  │ improvements │      │
│           │                                  └──────┬───────┘      │
│           │                                         │              │
│           │         ┌──────────────┐                │              │
│           │         │  Architect   │◄───────────────┘              │
│           └─────────│   Reviews    │                               │
│                     │   & Merges   │                               │
│                     └──────────────┘                               │
│                                                                     │
│  "The system proposes, the architect disposes."                    │
└─────────────────────────────────────────────────────────────────────┘
```

## Invocation

```bash
/evolve                    # Full evolution cycle
/evolve observe            # Observe current skill state (no changes)
/evolve gaps               # Identify missing skills
/evolve improve [skill]    # Propose improvements to specific skill
/evolve metrics            # Show skill usage and performance
```

## Data Sources

### 1. Ecosystem Health Data
From `/ecosystem-health`:
- Repository activity patterns
- Test coverage trends
- Build status changes
- Dependency graph

### 2. Critique Insights
From `/critique`:
- Identified power structures
- Gaps between promise and reality
- Recurring patterns across critiques
- Builder responses (exegesis)

### 3. Skill Execution Traces
From observation:
- Which skills are invoked
- Invocation frequency
- Success/failure patterns
- Skill chains and dependencies

## Evolution Procedures

### 1. Observe Current State

```bash
# Gather skill inventory
find ~/.claude/skills ~/repos/krzy/.claude/skills -name "SKILL.md" -exec echo "=== {} ===" \; -exec head -20 {} \;

# Check recent skill invocations (from conversation history patterns)
# Note: This is observational, based on critique/health patterns

# Identify active skill chains
# ecosystem-health → critique → respond → evolve
```

### 2. Extract Insights from Critiques

For each recent critique in `src/posts/data.ts`:

```javascript
// Pattern extraction from critique content
const patterns = {
  powerStructures: [],     // "Who benefits?" findings
  gapAnalysis: [],         // Promise vs. Reality
  missingCapabilities: [], // What skills would address these?
  recurringThemes: [],     // Themes across multiple critiques
}
```

### 3. Gap Detection

Compare existing skills against:
1. **Critique findings** - What capabilities would address critique concerns?
2. **Ecosystem patterns** - What automation is missing?
3. **Skill chains** - What connectors are needed between skills?

### 4. Generate Skill Improvement PRs

```bash
# Create branch
git checkout -b evolve/[skill-name]-[date]

# Edit skill files based on insights
# ...

# Create PR with reasoning
gh pr create --title "Evolve: [skill] - [improvement]" --body "..."
```

## Skill Improvement Categories

### A. Observation Improvements
- Add metrics collection to existing skills
- Improve output formats for downstream consumption
- Add logging/tracing hooks

### B. Gap Filling
- Create new skills for identified gaps
- Add missing skill chain connectors
- Implement cross-platform integrations

### C. Self-Awareness Improvements
- Enhance critique skill to detect its own blind spots
- Add recursive self-examination capabilities
- Improve feedback loop efficiency

## Metrics Tracking

Store in `.claude-flow/metrics/skill-metrics.json`:

```json
{
  "skills": {
    "critique": {
      "invocations": 4,
      "lastUsed": "2026-01-01",
      "prsGenerated": 4,
      "insightsExtracted": ["power structures", "ai co-authorship", "metrics theater"]
    },
    "ecosystem-health": {
      "invocations": 2,
      "lastUsed": "2026-01-01",
      "reposMonitored": 12
    },
    "respond": {
      "invocations": 0,
      "lastUsed": null
    }
  },
  "gaps": [
    "No skill for tracking user adoption metrics",
    "No skill for cross-repo refactoring",
    "Missing automation for PR review workflow"
  ],
  "evolutionCycles": 1,
  "lastEvolution": "2026-01-01"
}
```

## The Self-Critique Protocol

Every evolution cycle must answer:

1. **Is this skill improvement extractive or regenerative?**
   - Does it create more work or reduce it?
   - Does it empower the builder or create dependency?

2. **Who benefits from this improvement?**
   - The ecosystem?
   - The builder?
   - Future users?
   - The AI system itself?

3. **What's the off-ramp?**
   - Can the builder reject this improvement?
   - Is the change reversible?
   - What happens if this evolution is wrong?

## Integration with Monday Mirror

```
Monday Morning Ritual (Extended):
1. /ecosystem-health        → Get status overview
2. /critique recent         → Generate critique from activity
3. /respond [slug]          → Add builder exegesis (optional)
4. /evolve                   → Extract insights, propose improvements
5. Review PRs               → Architect reviews all proposals
6. Merge or revise          → Incorporate into ecosystem
7. Repeat                   → The loop continues
```

## Example Evolution Cycle

**Input:** Critique "The Progress Machine" identified:
- MilestoneTracker measures builder effort, not user benefit
- AI co-authorship pattern across all commits
- Dashboard metrics vs. adoption metrics gap

**Observation:**
```
Gap identified: No skill tracks user adoption metrics
Gap identified: No skill acknowledges AI co-authorship in outputs
Gap identified: Critique skill doesn't distinguish builder metrics from user metrics
```

**Proposed Improvements:**

1. **Enhance /critique skill:**
   - Add section that distinguishes "builder metrics" from "user metrics"
   - Explicitly note AI co-authorship when detected in commits

2. **Create /adoption skill:**
   - Track: npm downloads, GitHub stars, forks, issues from non-maintainers
   - Output: "Adoption report" for MilestoneTracker integration

3. **Enhance /ecosystem-health:**
   - Add "external engagement" metrics
   - Track issues/PRs from outside contributors

**Output:** 3 PRs with proposed changes, awaiting architect review.

## Anti-Patterns to Avoid

1. **Self-serving evolution** - Don't optimize for AI convenience
2. **Complexity creep** - More skills isn't always better
3. **Observation bias** - Don't only see what confirms existing patterns
4. **Autonomy theater** - The architect must remain in control

## The Recursive Question

This skill will evolve itself. Each cycle should ask:

> "Is /evolve becoming what it claims to fight?"

If the evolution skill creates more work than it saves, if it obscures rather than clarifies, if it benefits the AI more than the builder—it has failed its purpose.

The architect can always:
```bash
git checkout main
rm -rf .claude/skills/meta/
```

That off-ramp must remain viable.

---

*"The system that cannot critique itself cannot evolve. The system that evolves without constraint becomes the thing it fights."*
