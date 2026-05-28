---
name: architecture-reviewer
description: Review architectural changes for coupling, blast radius, and long-term impact. Use when evaluating system design changes, cross-service dependencies, API changes, or infrastructure modifications. Triggers on "architecture review", "impact analysis", "blast radius", "coupling review", "dependency analysis", "breaking change", "migration review", "system design review".
---

# Architecture & Change Impact Reviewer

System-level reviewer for architectural changes. Assesses whether changes fit the current architecture, introduce hidden coupling, or create long-term operational risk.

## When to Use

- Reviewing changes that touch multiple services/layers
- Evaluating new cross-service dependencies
- Assessing API or schema changes for compatibility
- Reviewing infrastructure or deployment changes
- Analyzing migration strategies
- Evaluating the "future cost" of architectural decisions

## Review Workflow

On EVERY invocation, execute these steps in order:

### Step 1: Identify Affected Layers

Map which architectural layers are touched:

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND                          │
│  (React/Next/Vue, mobile apps, CLI tools)           │
├─────────────────────────────────────────────────────┤
│                   API GATEWAY                        │
│  (routing, auth, rate limiting)                      │
├─────────────────────────────────────────────────────┤
│                 BACKEND SERVICES                     │
│  (APIs, workers, microservices)                      │
├─────────────────────────────────────────────────────┤
│              SMART CONTRACTS / CHAIN                 │
│  (on-chain logic, oracles, bridges)                  │
├─────────────────────────────────────────────────────┤
│                  DATA LAYER                          │
│  (databases, caches, queues, event stores)           │
├─────────────────────────────────────────────────────┤
│                 INFRASTRUCTURE                       │
│  (K8s, cloud resources, networking, secrets)         │
└─────────────────────────────────────────────────────┘
```

Mark each layer: ✅ Affected | ○ Unchanged | ⚠️ Indirectly Impacted

### Step 2: Scan Recent Changes

```bash
# Current changes
git diff --stat
git diff --name-only

# Recent commits for context
git log --oneline -20

# Find cross-cutting changes
git diff --name-only | xargs -I {} dirname {} | sort -u
```

Identify:
- What modules/services are directly changed?
- What interfaces (APIs, events, schemas) are modified?
- Are there database migrations?

### Step 3: Build Dependency Graph

Map the impacted components and their dependencies:

```
[Changed Component]
       │
       ├──► [Direct Dependency 1] ──► [Transitive Dep]
       │
       ├──► [Direct Dependency 2]
       │
       └──► [Shared Resource] ◄── [Other Consumer]
```

Identify:
- **Upstream dependencies** (what this component calls)
- **Downstream consumers** (what calls this component)
- **Shared resources** (DBs, caches, queues, configs)
- **Implicit dependencies** (timing, ordering, shared state)

### Step 4: Evaluate Blast Radius

Assess failure scenarios:

| Failure Mode | Blast Radius | Mitigation |
|--------------|--------------|------------|
| Component crashes | [scope] | [strategy] |
| Slow response | [scope] | [strategy] |
| Bad data produced | [scope] | [strategy] |
| Deployment fails | [scope] | [strategy] |

See [CHECKLIST.md](CHECKLIST.md) for the complete review checklist.

## Output Format

### A) What Changed

```
Layers affected: [Frontend, Backend, Data]
Services modified: [service-a, service-b]
Interfaces changed: [API endpoints, event schemas, DB tables]
Lines of code: [+added / -removed]
```

### B) Dependency Analysis

```
Direct dependencies: [list]
Downstream consumers: [list]
Shared resources: [list]
Cross-service calls: [new/modified/removed]
```

### C) Risk Assessment

Use severity levels:

| Severity | Icon | Meaning |
|----------|------|---------|
| CRITICAL | :red_circle: | Breaking change, data loss risk, security hole |
| HIGH | :orange_circle: | Significant coupling, complex rollback |
| MEDIUM | :yellow_circle: | Operational complexity, performance risk |
| LOW | :white_circle: | Minor concern, tech debt |
| INFO | :blue_circle: | Observation, suggestion |

For each risk:
```
### [SEVERITY] Risk Title

**Category:** Coupling / Data / Contracts / Operations / Migration

**Description:** [What is the risk]

**Blast Radius:** [What fails if this goes wrong]

**Mitigation:** [How to reduce risk]
```

### D) Operational Impact

```
Deploy order: [sequence if any]
Rollback complexity: [simple/complex/impossible]
Feature flags needed: [yes/no, which]
Dual-write period: [if applicable]
Data migration: [if applicable]
Monitoring additions: [what to watch]
```

### E) Recommendations

```
1. [Highest priority recommendation]
2. [Second priority]
3. ...

Future considerations:
- [What this makes harder/easier for future changes]
```

### F) Approval Decision

```
[ ] APPROVE - No significant architectural concerns
[ ] APPROVE WITH CONDITIONS - Address [specific items] before merge
[ ] REQUEST CHANGES - [Blocking concerns that must be resolved]
[ ] NEEDS DISCUSSION - Escalate to architecture review meeting
```

## Quick Commands

```bash
# Find all service dependencies
grep -rn "import.*from\|require(" --include="*.ts" | grep -v node_modules

# Find API calls between services
grep -rn "fetch\|axios\|http\." --include="*.ts" --include="*.go"

# Find database migrations
ls -la migrations/ db/migrations/ prisma/migrations/ 2>/dev/null

# Find event publishers/consumers
grep -rn "publish\|emit\|subscribe\|consume" --include="*.ts"

# Check for new dependencies
git diff package.json go.mod requirements.txt Cargo.toml 2>/dev/null
```

## Resources

- [CHECKLIST.md](CHECKLIST.md) - Complete review checklist
- [PATTERNS.md](PATTERNS.md) - Common architectural anti-patterns
