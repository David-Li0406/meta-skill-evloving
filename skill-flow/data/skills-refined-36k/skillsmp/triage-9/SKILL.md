---
name: triage
description: Process inbox items using parallel subagents with sequential review. Uses native TodoWrite for task tracking with encoded dependencies. Single-session workflow.
user-invocable: true
disable-model-invocation: true
allowed-tools: Task, Read, TodoWrite, TodoRead, AskUserQuestion, mcp__plugin_para-obsidian_para-obsidian__para_read, mcp__plugin_para-obsidian_para-obsidian__para_list, mcp__plugin_para-obsidian_para-obsidian__para_create, mcp__plugin_para-obsidian_para-obsidian__para_delete, mcp__plugin_para-obsidian_para-obsidian__para_rename, mcp__plugin_para-obsidian_para-obsidian__para_frontmatter_get, mcp__plugin_para-obsidian_para-obsidian__para_list_areas, mcp__plugin_para-obsidian_para-obsidian__para_list_projects, mcp__youtube-transcript__get_transcript, mcp__youtube-transcript__get_video_info, mcp__firecrawl__firecrawl_scrape, mcp__firecrawl__firecrawl_search, mcp__chrome-devtools__navigate_page, mcp__chrome-devtools__take_snapshot, mcp__chrome-devtools__list_pages, mcp__chrome-devtools__select_page, mcp__chrome-devtools__new_page
---

# Triage Coordinator

Process inbox items - single file or bulk with **parallel subagents** and **sequential review**.

Uses **native TodoWrite** for task tracking with encoded dependencies `[DEPS:id1,id2]`.

## Scope

**Single-session workflow.** This skill runs in one Claude Code session.

### What Triage Does

- **Organize** inbox items into PARA destinations
- **Categorize** items with template, type, and connections
- **Summarize** content for quick reference (frontmatter only)
- Create notes with `distilled: false` (Layer 1 content)

### What Triage Does NOT Do

- **Progressive summarization** - Use `/para-obsidian:distill-resource` for Layers 2-4
- **Deep learning** - Triage creates quick captures, not studied notes
- **Insight extraction** - `categorization_hints` are for organization, not learning

---

## Architecture Overview

The triage workflow follows: **Enrich → Analyze → Review**

1. **Enrichment** - Fetch full content (parallel for YouTube/Firecrawl, sequential for Chrome DevTools)
2. **Analysis** - Spawn parallel subagents (batch of 3) with enriched content
3. **Review** - Present proposals one at a time for user approval

**See:** [architecture.md](references/architecture.md) for detailed diagrams.

---

## Input Routing

Check the `$ARGUMENTS`:

| Input | Action |
|-------|--------|
| Empty or `all` | Bulk processing (scan inbox, batch of 3) |
| `clippings` / `voice` / `attachments` | Filter by type, then bulk process |
| `"filename.md"` | Single file → direct to worker skill |

**Single file mode:** Skip batching, spawn one subagent, present proposal, done.

---

## Phase 0: Initialize Session

### 0.0 Check for Single File Mode

If `$ARGUMENTS` is a filename (contains `.md`):
1. Read frontmatter to determine type
2. Spawn single worker subagent
3. Present proposal
4. Execute action
5. Done (no batching needed)

### 0.1 Check for Resume

```
TodoRead()
```

Filter for tasks where `id.startsWith("triage:")`.

If existing triage tasks found:
```
Found existing triage session:
• 3 completed
• 2 pending
• 1 in progress

Resume from where you left off? (y/n)
```

**See:** [todowrite-patterns.md](references/todowrite-patterns.md) for dependency encoding.

### 0.2 Load Vault Context

```
para_list_areas({ response_format: "json" })
para_list_projects({ response_format: "json" })
```

Store for connection suggestions.

### 0.3 Scan Inbox

```
para_list({ path: "00 Inbox", response_format: "json" })
```

Categorize by **TWO dimensions**:

**1. Item Type (for analysis skill selection):**

| Type | Detection | Analysis Skill |
|------|-----------|----------------|
| `clipping` | `type === "clipping"` | distill-web |
| `transcription` | `type === "transcription"` | distill-voice |
| `attachment` | PDF/DOCX in Attachments | distill-attachment |

**2. Source Type (for enrichment):**

| Source | Enrichment Tool | Parallel? |
|--------|-----------------|-----------|
| YouTube | `youtube-transcript` MCP | ✅ Yes |
| Twitter/X | Chrome DevTools | ❌ No |
| Public article | Firecrawl | ✅ Yes |
| Voice memo | None (has content) | N/A |

**See:** [enrichment-strategies.md](references/enrichment-strategies.md) for full details.

### 0.4 Create Task Graph

Create all tasks upfront with dependencies:

```typescript
TodoWrite({
  todos: [
    // Batch 1 - parallel
    { id: "triage:batch-1:item-1", content: "[DEPS:none] Distill: ✂️ Article 1", status: "pending" },
    { id: "triage:batch-1:item-2", content: "[DEPS:none] Distill: ✂️ Article 2", status: "pending" },
    { id: "triage:batch-1:item-3", content: "[DEPS:none] Distill: 🎤 Voice memo", status: "pending" },

    // Batch 1 review - blocked until items done
    { id: "triage:batch-1:review", content: "[DEPS:triage:batch-1:item-1,...] Review batch 1", status: "pending" },

    // Cleanup
    { id: "triage:cleanup", content: "[DEPS:triage:batch-N:review] Cleanup session", status: "pending" }
  ]
})
```

**See:** [todowrite-patterns.md](references/todowrite-patterns.md) for full task graph example.

### 0.5 Present Summary

```
Found 6 items in inbox:

📋 By Type:
• 4 clippings (web articles, threads)
• 1 voice memo
• 1 attachment

Starting enrichment phase...
```

---

## Phase 1: Enrichment

**CRITICAL:** Enrichment happens BEFORE analysis. Subagents receive full content, not stubs.

### 1.1 Parallel Enrichment (YouTube, Firecrawl)

```typescript
// Run simultaneously
mcp__youtube-transcript__get_transcript({ url: "..." })
mcp__firecrawl__firecrawl_scrape({ url: "...", formats: ["markdown"] })
```

### 1.2 Sequential Enrichment (Chrome DevTools)

```typescript
// One at a time - Chrome DevTools is single browser instance
mcp__chrome-devtools__navigate_page({ url: "https://x.com/user/status/123" })
mcp__chrome-devtools__take_snapshot({})
// Complete before starting next
```

**See:** [enrichment-strategies.md](references/enrichment-strategies.md) for why Chrome DevTools cannot parallelize.

---

## Phase 2: Parallel Analysis

### 2.1 Find Unblocked Tasks

```
TodoRead() → find where:
  - status === "pending"
  - [DEPS:...] all completed (or DEPS:none)
```

### 2.2 Mark In Progress

```
TodoRead() → update status to "in_progress" → TodoWrite(all)
```

### 2.3 Spawn Subagents

For each batch of 3 items, spawn subagents **in parallel**:

```typescript
Task({
  subagent_type: "general-purpose",
  description: "Distill clipping: [title]",
  model: "haiku",
  prompt: `[Analysis prompt with enriched content]`
})
```

**CRITICAL**: Run 3 Task calls in a single message for parallel execution.

**See:** [subagent-prompts.md](references/subagent-prompts.md) for full prompt templates.

### 2.4 Collect Proposals & Mark Complete

1. Parse JSON proposal from each subagent
2. Store in review queue
3. Mark task completed in TodoWrite

---

## Phase 3: Sequential Review

Mark review task in progress, then present proposals ONE AT A TIME:

```
## Proposal 1 of 3

**📝 [Proposed Title]**
From: ✂️ [Original filename]

### Summary
[2-3 sentences]

### Key Insights
- [Insight 1]
- [Insight 2]

### Classification
| Template | resource |
| Type | article |

---

**Actions:** A (Accept) | E (Edit) | S (Skip) | D (Delete) | 3 (Deeper) | Q (Quit)
```

**See:** [output-templates.md](references/output-templates.md) for full format.

### Action Handling

| Action | Behavior |
|--------|----------|
| **A** | Create note, handle original |
| **E** | Ask what to change, re-present |
| **S** | Skip, move to next |
| **D** | Delete (with confirmation) |
| **3** | Spawn deep analysis subagent (model: sonnet) |
| **Q** | Exit (tasks persist in TodoWrite) |

### "3" (Deeper) Action

Spawn subagent with `model: "sonnet"` that returns 3 different categorization options.

**See:** [subagent-prompts.md](references/subagent-prompts.md#deep-analysis-prompt) for prompt.

---

## Phase 4: Execute Approved Actions

**IMPORTANT:** Always include `distilled: "false"` in args. Triage creates quick resource notes - use `/para-obsidian:distill-resource` for full progressive summarization.

### For Clippings
```
para_create({ template, title, dest: "03 Resources", args: {..., distilled: "false"} })
para_delete({ file: "00 Inbox/[original]", confirm: true })
```

### For Transcriptions
```
para_create({ template, title, dest: "03 Resources", args: {..., distilled: "false"} })
para_rename({ from: "00 Inbox/[original]", to: "04 Archives/Transcriptions/..." })
```

### For Attachments
```
para_create({ template: "resource", args: {..., distilled: "false"} })
// Attachment stays in place, linked via source field
```

---

## Phase 5: Cleanup

When all reviews complete:

```
TodoRead() → filter OUT all triage:* tasks → TodoWrite(remaining)
```

Report completion:
```
✅ Triage complete!

Processed 6 items:
• 4 accepted → created resource notes
• 1 skipped
• 1 deleted
```

---

## Quick Reference

### Batch Size
**3 items** per batch.

### Task ID Format
```
triage:batch-1:item-1   → Analysis task
triage:batch-1:review   → Review phase
triage:cleanup          → Final cleanup
```

### Dependency Encoding
```
[DEPS:none]           → Can start immediately
[DEPS:id1,id2]        → Blocked by id1 AND id2
```

### Models
- **Haiku** for initial analysis (fast, cheap)
- **Sonnet** for deep analysis (smarter)

---

## References

| File | Content |
|------|---------|
| [architecture.md](references/architecture.md) | Diagrams, phase overview, philosophy |
| [enrichment-strategies.md](references/enrichment-strategies.md) | Tool selection by source type |
| [subagent-prompts.md](references/subagent-prompts.md) | Analysis and deep analysis prompts |
| [output-templates.md](references/output-templates.md) | Proposal format, review UI |
| [todowrite-patterns.md](references/todowrite-patterns.md) | Dependency encoding, task graph |
