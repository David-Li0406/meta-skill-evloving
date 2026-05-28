---
name: publish-to-discord
description: Use this skill to publish news digests and breaking alerts to Discord via the Discord MCP server, ensuring messages comply with Discord's character limits.
---

# Skill body

## When to Use

- Publishing regular news digests
- Alerting about breaking news
- Sharing formatted news summaries

## Prerequisites

- `DISCORD_MCP_URL` environment variable set (or use default)
- Target channel exists (default: `ai-news`)
- Content formatted for Discord (markdown)

## Input Schema

```json
{
  "content": "string - Formatted content to publish",
  "content_type": "string - 'digest' or 'breaking_alert'",
  "article": {
    "title": "string - Article title (for breaking alerts)",
    "url": "string - Article URL",
    "source": "string - News source",
    "category": "string - Article category",
    "ai_summary": "string - AI-generated summary"
  },
  "channel_name": "string - Target channel (default: ai-news)"
}
```

## Actions

### Step 1: Validate Configuration

1. Check that Discord MCP is accessible. If not:
   - Log warning
   - Return `published=false`
   - Skip remaining steps

### Step 2: Route by Content Type

**For digest:**
1. Split message if > 1900 characters (Discord limit is 2000)
2. Post each chunk as a separate message
3. Return message ID of the first chunk

**For breaking_alert:**
1. Build Discord embed with the article details
2. Post the embed to the specified channel
3. Return the message ID of the posted embed

## Output Schema

```json
{
  "message_id": "string - Discord message ID if successful",
  "published": "boolean - Whether publish succeeded"
}
```