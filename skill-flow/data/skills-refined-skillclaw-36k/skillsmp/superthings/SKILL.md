---
name: superthings
description: Use when triaging Things inbox, creating tasks, or managing todos. Learns from corrections to improve title suggestions and project assignments over time.
---

# SuperThings - Intelligent Task Management

SuperThings learns from your corrections to get better at suggesting titles and projects for Things tasks.

## Learning System (Agent-Native)

The learning system is fully agent-native via MCP tools. Agents can read, write, and query learned patterns programmatically.

### MCP Tools for Learning

| Tool | Purpose |
|------|---------|
| `things_list_patterns` | List all learned patterns (title_transforms, project_hints, exact_overrides) |
| `things_suggest_for_task` | Get suggestion + confidence for a task title |
| `things_log_correction` | Log a single correction to teach the system |
| `things_update_pattern` | Adjust pattern confidence manually |
| `things_remove_pattern` | Remove a bad or outdated pattern |
| `things_learn_batch` | Process multiple triage decisions at once |

### Example Agent Workflow

An agent can now triage inbox programmatically:

1. `things_get_inbox` - Get inbox items
2. For each item: `things_suggest_for_task` - Get suggestions with confidence
3. If confidence < 3: Use AskUserQuestion with context
4. If confidence >= 3: Auto-apply with `[learned: Nx]` indicator
5. `things_learn_batch` - Update patterns from decisions
6. `things_update_todo` - Apply changes to Things

### Pattern Storage

Patterns stored in `~/claudesync/servers/super-things/data/patterns.json`:

```json
{
  "title_transforms": [
    {
      "match": "^Fix ",
      "transform": "Delegate to Brianna: {original}",
      "confidence": 12,
      "examples": ["Fix fireplace", "Fix garage door"],
      "last_used": "2026-01-15T10:00:00Z"
    }
  ],
  "project_hints": {
    "build": {"Deep Work": 15, "Computer": 2},
    "research": {"Computer": 23, "Deep Work": 1},
    "call": {"Call": 18}
  },
  "exact_overrides": {
    "Call mom": {"title": "Call: Mom", "project": "Call", "confidence": 8}
  },
  "stats": {
    "sessions_completed": 47,
    "items_processed": 892,
    "patterns_learned": 23,
    "accuracy_trend": [0.60, 0.72, 0.85]
  }
}
```

### History Logging

All corrections logged to `~/claudesync/servers/super-things/data/history.jsonl`:

```json
{"ts": "2026-01-20T10:00:00Z", "original": "Fix fireplace", "suggested_title": "Delegate to Brianna: Fix fireplace", "final_title": "Delegate to Brianna: Fix fireplace", "suggested_project": "Computer", "final_project": "Computer", "title_accepted": true, "project_accepted": true}
```

## Confidence Thresholds

| Confidence | Behavior |
|------------|----------|
| < 3 | Use AskUserQuestion with context (pattern, examples) |
| >= 3 | Auto-apply with `[learned: Nx]` indicator |
| >= 10 | Apply silently (trusted pattern) |

### AskUserQuestion for Low Confidence

When confidence is below 3, present options with full context:

```
question: "Title suggestion for 'Fix fireplace'?"
header: "2x"
options:
  - label: "Delegate to Brianna: Fix fireplace"
    description: "Pattern: ^Fix → Delegate | 2x confidence | Examples: Fix garage, Fix dishwasher"
  - label: "Fix fireplace"
    description: "Keep original unchanged"
```

## Using the Learning Tools

### Reading Patterns

```
things_list_patterns
→ Returns all title_transforms, project_hints, exact_overrides with counts
```

### Getting Suggestions

```
things_suggest_for_task({ title: "Fix dishwasher" })
→ {
    original: "Fix dishwasher",
    suggested_title: "Delegate to Brianna: Fix dishwasher",
    suggested_project: "Computer",
    confidence: 12,
    pattern_source: "title_transform",
    pattern_rule: "^Fix ",
    examples: ["Fix fireplace", "Fix garage door"]
  }
```

### Logging Corrections

Single correction:
```
things_log_correction({
  original_title: "Fix fireplace",
  suggested_title: "Delegate to Brianna: Fix fireplace",
  final_title: "Delegate to Brianna: Fix fireplace",
  title_accepted: true,
  project_accepted: true
})
```

Batch of corrections:
```
things_learn_batch({
  decisions: [
    { original_title: "Fix X", final_title: "Delegate: Fix X", title_accepted: true },
    { original_title: "Research Y", final_project: "Computer", project_accepted: true }
  ]
})
```

### Managing Patterns

Update confidence:
```
things_update_pattern({
  pattern_type: "title_transform",
  key: "^Fix ",
  confidence_delta: 1  // or set absolute with confidence: 10
})
```

Remove bad pattern:
```
things_remove_pattern({
  pattern_type: "title_transform",
  key: "^Fix "
})
```

## Projects Reference

| Project | ID |
|---------|-----|
| Computer | `LDhUsibk3dp2ZPioQySSiu` |
| Deep Work | `WamuBi2sFwbUwpXz9NZetP` |
| Call | `Er67bc9YAur6ZeKTCBLC4c` |
| Home | `NsSR9HR3pd2bVi2z4QHFfM` |
| Out and About | `5LwYiPJAkWGSCMHML8xaXb` |
| Kids/Activities | `7n14Jusf7nCrLADfAANabW` |
| Someday | `EZ5uJWRtcrvJ4U852NkNQ8` |

## External Tools

SuperThings uses external MCP tools for research and actions:

### Firecrawl - Quick Research / URL Scraping
**When to use**: URL tasks, single-page reads, video metadata
**MCP Function**: `mcp__firecrawl-mcp__firecrawl_scrape`
**Best for**: URLs in tasks, YouTube videos, GitHub repos, articles

### Tavily - Deep Research
**When to use**: "Research X" tasks, DD (Deep Dive), competitive analysis
**MCP Function**: `mcp__tavily__tavily_search`
**Best for**: Multi-source research, company analysis, current events

### BrowserBase - Browser Automation
**When to use**: Login-required sites, JavaScript-heavy pages, screenshots
**MCP Functions**: `mcp__browserbase__*`
**Best for**: Authenticated sites, form filling, dynamic pages

### Zapier Gmail - Email Operations
**When to use**: Email tasks, intro tasks, delegation
**MCP Functions**: `mcp__zapier__gmail_*`
**Best for**: Email tasks, intro emails, delegation

### Tool Selection

| Task Type | Tool |
|-----------|------|
| URL in task | Firecrawl |
| "Research X" | Tavily |
| Login-required site | BrowserBase |
| "Email X" | Zapier |

## Research Cache System

GTD research results cached to `~/claudesync/servers/super-things/data/research-cache.json`.

- Results persist for 7 days
- Use `/gtd resume` to continue a previous session
- Say "details N" to expand cached findings

## GTD Triage Commands

| Command | Action |
|---------|--------|
| `C` | Complete task |
| `C [note]` | Complete with note |
| `D [person]` | Delegate via email |
| `DD` | Deep Dive - more research |
| `DD [focus]` | Deep Dive with focus |

## Slash Commands

- `/thingsinbox` - Triage inbox with learning-based suggestions and AskUserQuestion for low confidence
- `/gtd` - Get Things Done workflow with research caching
