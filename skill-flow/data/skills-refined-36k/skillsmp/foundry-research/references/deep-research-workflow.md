# Deep Research Workflow

Multi-phase iterative research with automatic query decomposition and web source synthesis.

## Contents

- When to Use
- Architecture
- Execution Model
- MCP Operations (start, status, report, list, delete)
- Session States
- Polling Strategy
- User Gates
- Output Format
- Error Handling
- Integration with Session Management

## When to Use

- Complex questions requiring multiple sources
- Topics needing comprehensive coverage
- Research that benefits from iterative refinement
- Questions where surface-level answers are insufficient

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Deep Research                         │
├─────────────────────────────────────────────────────────┤
│  Query → Decompose → Search → Extract → Synthesize      │
│    │         │          │         │          │          │
│    └─────────┴──────────┴─────────┴──────────┘          │
│                    (iterates)                            │
└─────────────────────────────────────────────────────────┘
```

## Execution Model

Deep research runs **in the background** by default:

1. **Start** - Initiate research session, returns `research_id`
2. **Poll** - Check status periodically until complete
3. **Report** - Retrieve final synthesized report

This allows long-running research without blocking the conversation.

## MCP Operations

### Start Research

```bash
mcp__plugin_foundry_foundry-mcp__research action="deep-research" deep_research_action="start" query="Your research question" max_iterations=3 max_sub_queries=5 max_sources_per_query=5
```

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `query` | Yes | - | Main research question |
| `deep_research_action` | No | `start` | Sub-action: start, continue, resume |
| `max_iterations` | No | 3 | Maximum refinement iterations |
| `max_sub_queries` | No | 5 | Sub-queries generated per iteration |
| `max_sources_per_query` | No | 5 | Sources fetched per sub-query |
| `follow_links` | No | true | Extract and follow links from sources |
| `max_concurrent` | No | 3 | Parallel operations |
| `timeout_per_operation` | No | 120 | Seconds per web fetch |
| `task_timeout` | No | - | Overall task timeout (seconds) |

### Check Status

```bash
mcp__plugin_foundry_foundry-mcp__research action="deep-research-status" research_id="research-abc123"
```

Returns:
```json
{
  "research_id": "research-abc123",
  "status": "in_progress",
  "progress": {
    "iteration": 2,
    "max_iterations": 3,
    "queries_completed": 7,
    "sources_processed": 28
  },
  "started_at": "2025-01-02T10:00:00Z"
}
```

### Get Report

```bash
mcp__plugin_foundry_foundry-mcp__research action="deep-research-report" research_id="research-abc123"
```

Returns comprehensive report with:
- Executive summary
- Key findings
- Source citations
- Confidence assessments
- Follow-up questions

### List Sessions

```bash
mcp__plugin_foundry_foundry-mcp__research action="deep-research-list" limit=10 completed_only=false
```

### Delete Session

```bash
mcp__plugin_foundry_foundry-mcp__research action="deep-research-delete" research_id="research-abc123"
```

## Session States

```
started → in_progress → completed
              │              │
              └→ failed      └→ (report available)
```

| State | Description | Can Resume | Has Report |
|-------|-------------|------------|------------|
| `started` | Initialized, beginning decomposition | Yes | No |
| `in_progress` | Actively researching | Yes | Partial |
| `completed` | All iterations done | No | Yes |
| `failed` | Error during research | Yes | Partial |

## Polling Strategy

**Critical:** Claude cannot implement timed delays between tool calls. Follow these patience rules instead.

### Polling Rules

1. **Maximum checks:** 5 status checks per research session
2. **Progress tracking:** Track `sub_queries_completed` and `iteration` between checks
3. **Stall detection:** Research is stalled only if:
   - `elapsed_ms` > 300000 (5 minutes) AND
   - No change in `sub_queries_completed` or `iteration` since last check

### Polling Flow

```
1. Start research → notify user "This may take several minutes"
2. Check #1: Record initial progress (iteration, sub_queries_completed)
3. Check #2-4: Compare progress to previous check
   - If progress changed → continue checking
   - If no progress AND elapsed_ms > 300000 → stalled
4. Check #5 (final): If still in_progress, offer user options

On completed: fetch and present report
On failed: show error, offer retry
On stall detected: offer retry or background options
```

### What to Say Between Checks

Instead of silent rapid polling:
- After check #1: "Research is underway. Currently in {phase} phase..."
- After check #2-3: "Progress: {sub_queries_completed}/{sub_queries_total} queries completed..."
- After check #4: "Still working. Research has been running for {elapsed_ms/60000:.1f} minutes..."
- After check #5: Present user options if not complete

### Stall Recovery

When stall detected (>5 min with no progress), use AskUserQuestion:

```
"Research appears stalled ({elapsed} minutes, no progress). Options:"
- "Keep waiting (check 2 more times)"
- "Run in background (check later with foundry-research research-{id})"
- "Cancel and try different query"
```

### Anti-Patterns (DO NOT DO THIS)

**BAD - Rapid polling:**
```
[start deep-research]
[deep-research-status]  <-- VIOLATION: no user text
[deep-research-status]  <-- VIOLATION: consecutive calls
```

**GOOD - Paced polling:**
```
[start deep-research]
"Research started, typically takes 3-5 minutes..."
[deep-research-status]
"Progress: 3 of 5 sub-queries complete, 12 sources analyzed..."
[deep-research-status]
```

**BAD - Independent research while waiting:**
```
[start deep-research]
[WebSearch query="same topic"]  <-- VIOLATION: redundant research
[WebFetch url="..."]            <-- VIOLATION: deep research handles this
```

**GOOD - Wait for deep research:**
```
[start deep-research]
"Research started. The deep research workflow will gather and analyze sources..."
[deep-research-status]
```

## User Gates

| Checkpoint | Prompt |
|------------|--------|
| Start | "Starting deep research on '{query}'. This may take a few minutes." |
| Progress | "Research {progress}% complete. {n} sources analyzed so far." |
| Complete | Present report with source citations |
| Failed | "Research encountered an error: {error}. Retry?" |

## Output Format

```json
{
  "research_id": "research-abc123",
  "query": "Original research question",
  "status": "completed",
  "report": {
    "summary": "Executive summary of findings",
    "findings": [
      {
        "topic": "Sub-topic",
        "content": "Detailed findings",
        "confidence": "high|medium|low",
        "sources": ["url1", "url2"]
      }
    ],
    "sources": [
      {
        "url": "https://...",
        "title": "Source title",
        "relevance": 0.85
      }
    ],
    "follow_up_questions": [
      "Suggested follow-up question 1",
      "Suggested follow-up question 2"
    ]
  },
  "metadata": {
    "iterations": 3,
    "total_sources": 42,
    "duration_seconds": 180
  }
}
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `RESEARCH_NOT_FOUND` | Invalid research_id | List sessions, use valid ID |
| `RESEARCH_TIMEOUT` | Task exceeded timeout | Retry with higher `task_timeout` |
| `NO_SOURCES_FOUND` | Query too narrow/obscure | Broaden query terms |
| `RATE_LIMITED` | Too many concurrent requests | Wait and retry |

## Integration with Session Management

Deep research sessions are listed alongside threads in unified session management:

```
foundry-research sessions list
```

Shows both:
- Chat/thinkdeep/ideate threads (`thread-*`)
- Deep research sessions (`research-*`)

Sessions can be filtered:
- `type=threads` - Only conversation threads
- `type=research` - Only deep research sessions
- `type=all` - Both (default)
