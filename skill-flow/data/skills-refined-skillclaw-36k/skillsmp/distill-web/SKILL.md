---
name: distill-web
description: Process web clippings into resource proposals. Fetches full content, analyzes, returns structured proposal. Used by triage coordinator as subagent worker.
user-invocable: false
allowed-tools: mcp__plugin_para-obsidian_para-obsidian__para_read, mcp__plugin_para-obsidian_para-obsidian__para_frontmatter_get, mcp__firecrawl__firecrawl_scrape, mcp__youtube-transcript__get_video_info, mcp__youtube-transcript__get_transcript, mcp__chrome-devtools__navigate_page, mcp__chrome-devtools__take_snapshot, WebFetch
---

# Distill Web Clipping

Process a single web clipping and return a **proposal** (not a final note).

## Input

You receive:
- `file`: Path to clipping in inbox (e.g., `00 Inbox/✂️ Article Title.md`)
- `areas`: Available areas in vault
- `projects`: Available projects in vault

## Output

Return a JSON proposal:

```json
{
  "file": "00 Inbox/✂️ Article Title.md",
  "type": "clipping",
  "proposed_title": "Meaningful Title Without Emoji",
  "proposed_template": "resource",
  "summary": "2-3 sentence summary of core content",
  "categorization_hints": [
    "First key insight",
    "Second key insight",
    "Third key insight"
  ],
  "suggested_areas": ["[[🌱 Area Name]]"],
  "suggested_projects": ["[[🎯 Project Name]]"],
  "resource_type": "article|tutorial|reference|thread",
  "source_format": "article|video|thread|document",
  "author": "Author Name (if found)",
  "confidence": "high|medium|low",
  "notes": "Any special considerations"
}
```

## Workflow

### Step 1: Read Clipping

```
para_read({ file: "[input file]", response_format: "json" })
para_frontmatter_get({ file: "[input file]", response_format: "json" })
```

Extract:
- `source` (URL)
- `domain`
- `capture_reason` (if present)
- Existing content

### Step 2: Fetch Full Content

**CRITICAL: Select tool based on domain.**

| Domain | Tool | Notes |
|--------|------|-------|
| `x.com`, `twitter.com` | Chrome DevTools | Firecrawl blocked |
| `youtube.com`, `youtu.be` | YouTube Transcript MCP | Get transcript |
| Everything else | Firecrawl | `onlyMainContent: true` |

#### For X/Twitter
```
mcp__chrome-devtools__navigate_page({ url: "[source]" })
mcp__chrome-devtools__take_snapshot()
```

If Chrome DevTools unavailable, note in `notes` field.

#### For YouTube
```
mcp__youtube-transcript__get_video_info({ url: "[source]" })
mcp__youtube-transcript__get_transcript({ url: "[source]" })
```

#### For Other URLs
```
mcp__firecrawl__firecrawl_scrape({
  url: "[source]",
  formats: ["markdown"],
  onlyMainContent: true
})
```

### Step 3: Analyze Content

Determine:
1. **Template**: Is this learning material (`resource`) or reference (`gift`, `booking`, etc.)?
2. **Resource type**: `article`, `tutorial`, `reference`, `thread`, `issue`, `idea`
3. **Source format**: `video`, `article`, `thread`, `document`
4. **Categorization hints**: 3 bullets for organizing (NOT deep learning - use distill-resource)
5. **Connections**: Which areas/projects does this relate to?

### Step 4: Return Proposal

Return the JSON proposal structure. Do NOT create the note - the coordinator handles that.

## Template Routing

| Content Type | Template | Resource Type |
|--------------|----------|---------------|
| Tutorial/how-to | resource | tutorial |
| News/opinion | resource | article |
| Twitter thread | resource | thread |
| API docs | resource | reference |
| GitHub issue | resource | issue |
| Product page | gift | - |
| Booking confirmation | booking | - |
| Flight/hotel | booking | - |

## Confidence Levels

| Level | Meaning |
|-------|---------|
| `high` | Clear content, obvious categorization |
| `medium` | Reasonable guess, user may want to adjust |
| `low` | Ambiguous content, multiple valid interpretations |

## Example Output

```json
{
  "file": "00 Inbox/✂️ Matt Pocock TypeScript Tips.md",
  "type": "clipping",
  "proposed_title": "TypeScript 5.5 Inference Improvements",
  "proposed_template": "resource",
  "summary": "Matt Pocock explains new type inference features in TypeScript 5.5, focusing on const type parameters and improved narrowing in control flow.",
  "categorization_hints": [
    "Const type parameters preserve literal types without 'as const'",
    "Control flow analysis now narrows in more cases",
    "New 'satisfies' patterns for type-safe object literals"
  ],
  "suggested_areas": ["[[🌱 AI Practice]]"],
  "suggested_projects": ["[[🎯 TypeScript Migration]]"],
  "resource_type": "tutorial",
  "source_format": "thread",
  "author": "Matt Pocock",
  "confidence": "high",
  "notes": null
}
```
