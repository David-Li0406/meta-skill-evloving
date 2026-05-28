# Triage Architecture

## The Correct Architecture

```
┌─────────────────────────────────────────────────────────────┐
│       PHASE 1a: PARALLEL ENRICHMENT (Stateless APIs)        │
│  • YouTube videos → parallel youtube-transcript calls       │
│  • Public articles → parallel Firecrawl scrape calls        │
│  • GitHub repos → parallel Firecrawl scrape calls           │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│       PHASE 1b: SEQUENTIAL ENRICHMENT (Browser Required)    │
│  • Twitter/X threads → Chrome DevTools (one at a time)      │
│  • Confluence pages → Chrome DevTools (one at a time)       │
│  • Any auth-required site → Chrome DevTools (sequential)    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              PHASE 2: PARALLEL ANALYSIS                     │
│  All enriched content → parallel subagents (batch of 3)     │
│  Each subagent has fresh context, analyzes one item         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              PHASE 3: SEQUENTIAL REVIEW                     │
│  Present proposals one at a time for user approval          │
└─────────────────────────────────────────────────────────────┘
```

## Detailed Architecture: Enrich → Analyze → Review

```
┌─────────────────────────────────────────────────────────────┐
│                    COORDINATOR (You)                         │
│  • Scans inbox, groups by SOURCE TYPE (not just item type)  │
│  • Groups items by enrichment capability:                   │
│    - Parallel-capable: YouTube, public articles, GitHub     │
│    - Sequential-only: Twitter/X, Confluence, auth sites     │
│  • Runs enrichment BEFORE spawning analysis subagents       │
│  • Spawns analysis subagents in parallel (batch of 3)       │
│  • Presents proposals ONE AT A TIME for review              │
└─────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ ENRICH PARALLEL │  │ ENRICH PARALLEL │  │ ENRICH SEQUENTIAL│
│ (YouTube MCP)   │  │ (Firecrawl)     │  │ (Chrome DevTools)│
│                 │  │                 │  │                  │
│ 3 videos at     │  │ 3 articles at   │  │ 1 Twitter thread │
│ once ✅         │  │ once ✅         │  │ at a time ⏳     │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Subagent   │      │  Subagent   │      │  Subagent   │
│  ANALYZE    │      │  ANALYZE    │      │  ANALYZE    │
│  (Item 1)   │      │  (Item 2)   │      │  (Item 3)   │
│             │      │             │      │             │
│ Has full    │      │ Has full    │      │ Has full    │
│ enriched    │      │ enriched    │      │ enriched    │
│ content ✅  │      │ content ✅  │      │ content ✅  │
└─────────────┘      └─────────────┘      └─────────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
                    ┌─────────────────┐
                    │  Review Queue   │
                    │  (Sequential)   │
                    └─────────────────┘
```

## Why This Architecture?

1. **Enrichment-aware batching** - Groups items by what CAN parallelize, not just item count
2. **Context isolation** - Each analysis subagent has fresh context, no rot
3. **Optimal parallelization** - YouTube/Firecrawl run parallel; Chrome DevTools sequential
4. **Full content for analysis** - Subagents receive enriched content, not just stubs
5. **Collaborative review** - User approves/edits proposals one at a time
6. **Native task tracking** - TodoWrite provides visibility (`Ctrl+T`) and persistence
7. **Resume capability** - TodoRead shows pending tasks on restart

## Philosophy: Solving Context Rot

This skill solves the **context rot problem**: when processing 20 inbox items sequentially, context fills up by item 5. By isolating each item's analysis in a subagent:

1. **Fresh context per item** - No pollution from previous items
2. **Parallel speed** - 3x faster than sequential
3. **Proposals not actions** - Subagents suggest, coordinator executes
4. **Collaborative review** - User stays in control
5. **Native task tracking** - TodoWrite provides visibility and persistence

The coordinator's context only holds:
- Vault metadata (areas, projects)
- Review queue (lightweight proposals)
- Task graph (managed by TodoWrite)

Heavy lifting happens in subagent contexts that are discarded after use.
