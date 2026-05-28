---
name: research
description: 'Deep codebase exploration. Triggers: research, explore, investigate, understand, deep dive, current state.'
---

# Research Skill

Orchestrate Explore agents to systematically investigate a codebase.

## How It Works

Research doesn't explore directly - it **dispatches Explore agents** that follow the 6-tier discovery hierarchy. This keeps context clean and uses the specialized exploration capabilities.

```
/research <topic>
    │
    ├── Task(Explore) → Prior art check (.agents/, MCP)
    ├── Task(Explore) → Code-map discovery
    ├── Task(Explore) → Semantic search (MCP)
    ├── Task(Explore) → Targeted code exploration
    │
    └── Synthesize findings → .agents/research/
```

## Quick Start

```bash
/research authentication flows in services/auth
```

## Workflow

### 1. Setup

```bash
mkdir -p .agents/{research,synthesis}/
```

### 2. Mine Prior Knowledge (MANDATORY)

**Before dispatching Explore agents, query the knowledge flywheel:**

```bash
# Query CASS-indexed sessions for prior solutions
ao forge search "$TOPIC" --cass --limit 10

# Inject relevant learnings with decay applied
ao inject "$TOPIC" --apply-decay --format markdown --max-tokens 500
```

**If ao CLI unavailable, fall back to file search:**
```bash
grep -r "$TOPIC" .agents/learnings/ .agents/patterns/ .agents/research/ 2>/dev/null | head -20
```

**Output:** Display prior knowledge summary before proceeding. If high-relevance prior art exists, ask user whether to reference existing or start fresh.

### 3. Prior Art Check (Explore Agent)

Launch an Explore agent to check existing knowledge:

```
Task(
  subagent_type="Explore",
  prompt="Search for prior research on '$TOPIC':
    1. Check .agents/research/ for existing docs
    2. Check .agents/learnings/ and .agents/patterns/
    3. Use mcp__smart-connections-work__lookup for semantic matches
    4. Use mcp__ai-platform__memory_recall for stored insights

    Report: What prior work exists? Can we reference instead of duplicate?",
  description="Prior art check"
)
```

If prior art exists: **reference it**, don't duplicate.

### 4. Context Discovery (Explore Agents)

Launch Explore agents for each tier as needed:

**Tier 1-2: Structured Knowledge**
```
Task(
  subagent_type="Explore",
  prompt="For topic '$TOPIC':
    1. Check docs/code-map/ for architecture docs
    2. Run semantic search via MCP tools
    3. Return: key files, entry points, patterns found",
  description="Code-map + semantic search"
)
```

**Tier 3-4: Code Exploration**
```
Task(
  subagent_type="Explore",
  prompt="For topic '$TOPIC' in path '$SCOPE':
    1. Find relevant files (Glob with specific patterns)
    2. Search for keywords (Grep with scope)
    3. Read key files and trace relationships
    4. Return: findings with file:line citations",
  description="Targeted code exploration"
)
```

### 5. Synthesize Findings

After Explore agents return, synthesize into a research document:

**Write to:** `.agents/research/YYYY-MM-DD-{topic}.md`

**Required sections:**
- Executive Summary (2-3 sentences)
- Current State (key files table)
- Findings (with `file:line` evidence)
- Constraints & Risks
- Recommendation
- Next Steps

### 6. Create Synthesis Artifact

**MANDATORY:** Research is chaos. Synthesis is the ratchet.

```
/research (chaos) → SYNTHESIS (ratchet) → /plan or /product
```

**Write to:** `.agents/synthesis/YYYY-MM-DD-{topic}.md`

Consolidate findings into a single canonical reference (~10-20K chars).

### 7. Lock the Ratchet

**Index and record for the flywheel:**

```bash
# Index research output so future sessions can find it
ao forge index .agents/research/YYYY-MM-DD-$TOPIC.md
ao forge index .agents/synthesis/YYYY-MM-DD-$TOPIC.md

# Record provenance in the ratchet chain
ao ratchet record research \
  --input "$TOPIC" \
  --output ".agents/research/YYYY-MM-DD-$TOPIC.md" \
  --output ".agents/synthesis/YYYY-MM-DD-$TOPIC.md"
```

**The ratchet is now locked.** This research is discoverable by future `/research` calls via `ao forge search`.

## 6-Tier Discovery Hierarchy

Explore agents follow this priority order:

| Tier | Source | When to Use |
|------|--------|-------------|
| 1 | Code-map (`docs/code-map/`) | Always first - fastest, most authoritative |
| 2 | Semantic search (MCP) | Conceptual matches, stored insights |
| 3 | Scoped grep/glob | Specific keywords, file patterns |
| 4 | Source code reading | Direct evidence from files |
| 5 | Knowledge artifacts (`.agents/`) | Historical context |
| 6 | External (web) | Last resort only |

## Key Rules

| Rule | Why |
|------|-----|
| Use Explore agents | Keeps main context clean |
| Check prior art first | Prevents re-solving |
| Scope all searches | Context efficiency |
| Always cite `file:line` | Verifiable claims |
| Synthesize before planning | Single source of truth |

## Explore Agent Configuration

When launching Explore agents, specify thoroughness:

| Level | Use For |
|-------|---------|
| `"quick"` | Simple lookups, single-file questions |
| `"medium"` | Feature exploration, moderate scope |
| `"very thorough"` | Architecture research, cross-cutting concerns |

Example:
```
Task(
  subagent_type="Explore",
  prompt="Very thorough exploration of authentication system...",
  description="Auth system deep dive"
)
```

## ao CLI Integration

When ao CLI is available, use it for knowledge operations:

```bash
# Search existing knowledge before exploring
ao forge search "<topic>" --limit 10

# Index research output for future retrieval
ao forge index .agents/research/<topic>.md

# Record research completion for provenance
ao ratchet record research --input "<topic>" --output ".agents/research/<topic>.md"
```

## References

- `references/context-discovery.md` - 6-tier hierarchy details
- `references/document-template.md` - Output format

## Next

```
/research → SYNTHESIS → /plan or /product
```

After research, create synthesis doc, then run `/plan` or `/product`.
