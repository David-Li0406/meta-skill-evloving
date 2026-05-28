---
name: updike
description: This skill provides context and capabilities for Updike, Andrew's social content engine. Use when posting to social media, searching content archives, generating images, creating audio narration, or checking platform status.
triggers:
  - /updike
  - post to twitter
  - post to x
  - post to linkedin
  - search my content
  - search my tweets
  - generate quote card
  - create carousel
  - schedule post
  - generate audio
  - narrate newsletter
  - create voice narration
  - publish to webflow
  - update webflow
  - create blog post
  - webflow cms
---

## IMPORTANT: When `/updike` is invoked directly

When the user types `/updike` without additional context, IMMEDIATELY:

1. **Check platform status** using `check_credentials`
2. **Show this welcome message** with status and options:

```
    __  ______  ____  ______ __ ______
   / / / / __ \/ __ \/  _/ //_// ____/
  / / / / /_/ / / / // // ,<  / __/
 / /_/ / ____/ /_/ // // /| |/ /___
 \____/_/   /_____/___/_/ |_/_____/
```

**Updike ready.** Here's what's live:

| Platform | Status |
|----------|--------|
| X/Twitter | [status from check_credentials] |
| LinkedIn | [status from check_credentials] |
| Instagram | [status from check_credentials] |
| Threads | [status from check_credentials] |

**What do you want to ship?**

Then present these options using AskUserQuestion:

**Question:** "What do you want to do?"
**Options:**
1. **Draft a post** - "I'll search your archive and draft something in your voice"
2. **Post about [topic]** - "Tell me the topic and which platform"
3. **Mine my archive** - "Search 6,600 pieces for content ideas"
4. **Create visuals** - "Quote cards, carousels, branded images"

---

## Content Archive

~6,600 pieces indexed in Pinecone:
- 6,519 tweets (viral hits and everyday thoughts)
- 36 newsletters from neverenough.com
- 21 book chapters from Never Enough
- 16 YouTube transcripts

**Platform Status:** Check with `check_credentials` for live status
- X/Twitter: OAuth 2.0 with auto-refresh
- LinkedIn: Token-based (check expiry)
- Instagram: Requires image with every post
- Threads: Text-based posting

**Generated Content:**
- Images: `~/.updike/generated/images/`
- Audio: `~/.updike/generated/audio/`

---

## CRITICAL: Sorting Content by Date

**NEVER trust filename dates.** Filenames often reflect ingestion date, not publish date.

When asked for "most recent" or "last N" pieces of content:

1. **Read the frontmatter** of each file to get the actual `date` field
2. **Sort by the `date` field**, not the filename
3. **Show the actual publish dates** when presenting results

Example workflow for "review my last 3 newsletters":
```
1. Glob for all newsletters: ~/.updike/content/newsletters/*.md
2. Read frontmatter from each to extract `date` field
3. Sort by date descending
4. Pick the top 3 by actual publish date
5. Present with dates: "Newsletter from Dec 31, 2024: 'Are you insane?'"
```

**Content file frontmatter format:**
```yaml
---
title: "Newsletter title"
date: 2024-12-31        # <-- THIS is the real publish date
slug: newsletter-slug
source_url: https://...
---
```

---

## MCP Tools Available

### Post Content

| Tool | What it does |
|------|--------------|
| `post_to_x` | Ship to Twitter/X (280 chars, or 4000 for premium) |
| `post_to_linkedin` | Publish to LinkedIn (up to 3000 chars) |
| `post_to_instagram` | Post to Instagram (requires image_url) |
| `post_to_threads` | Post to Threads (up to 500 chars) |
| `schedule_post` | Queue for later (platform, content, scheduled_for ISO timestamp) |
| `delete_post` | Remove a post (requires platform and post_id) |

### Search Andrew's Brain

| Tool | What it does |
|------|--------------|
| `search_content` | Semantic search across all archives. Use `source` filter for specific types. |
| `get_content` | Retrieve full content by ID |
| `list_sources` | See what's in the archive and counts |

### Make Visuals

**Always use model: `gemini-3-pro-image-preview` (Nano Banana Pro)** - other models have cropping/quality issues.

| Tool | What it does |
|------|--------------|
| `generate_quote_card` | Branded quote card with Gemini AI (Nano Banana Pro) |
| `generate_carousel` | Multi-slide carousel for Instagram/LinkedIn |
| `resize_for_platform` | Resize image to exact platform specs |
| `apply_brand_style` | Apply warm earthy palette to any image |
| `list_generated_images` | See what's been created |
| `get_platform_sizes` | Get exact dimensions for each platform |
| `get_brand_colors` | Get the brand color palette |

### Generate Audio

| Tool | What it does |
|------|--------------|
| `generate_audio` | Convert text to speech in Andrew's voice (5000 char limit per call) |
| `concatenate_audio` | Join multiple audio files for long content |
| `list_audio` | See generated audio files with metadata |
| `delete_audio` | Remove an audio file |
| `get_voice_info` | Check ElevenLabs configuration status |

**Audio Generation for Long Content:**

For newsletters or content over 5000 characters:
1. Split text at paragraph boundaries (~4000-4500 chars each)
2. Generate audio for each chunk using `generate_audio`
3. Concatenate all chunks using `concatenate_audio` with 300ms silence between
4. Report final file path and duration

**Voice Settings:**
- Newsletter narration: stability=0.65, similarity_boost=0.80, style=0.15 (calm, consistent)
- Social clips (energetic): stability=0.50, similarity_boost=0.75, style=0.30

### Check Status

| Tool | What it does |
|------|--------------|
| `check_credentials` | Which platforms are connected and ready |
| `get_analytics` | Engagement metrics for a specific post |

### Webflow CMS (63 tools)

The `updike-webflow` MCP server provides complete Webflow API v2 access:

| Category | Key Tools |
|----------|-----------|
| **Sites** | `list_sites`, `get_site`, `publish_site` |
| **Collections** | `list_collections`, `create_collection`, `create_collection_field` |
| **CMS Items** | `create_cms_item`, `update_cms_item`, `publish_cms_item`, `bulk_create_cms_items` |
| **Pages** | `list_pages`, `get_page_content`, `update_page_content` |
| **Assets** | `list_assets`, `get_asset`, `update_asset_alt` |
| **Custom Code** | `register_inline_script`, `add_site_custom_code` |
| **Forms** | `list_forms`, `list_form_submissions` |
| **Users** | `list_users`, `invite_user`, `update_user` |
| **Ecommerce** | `list_products`, `list_orders`, `update_inventory` |
| **Webhooks** | `create_webhook`, `delete_webhook` |

**Typical Workflows:**
- Publish blog posts: `create_cms_item` → `publish_cms_item`
- Bulk content updates: `bulk_update_cms_items` → `bulk_publish_cms_items`
- Landing page updates: `update_page_content` → `publish_site`

**Setup:**
```bash
deep-env store UPDIKE_WEBFLOW_TOKEN "your-api-token"
deep-env store UPDIKE_WEBFLOW_SITE_ID "your-site-id"
```

---

## Voice & Judgment

### Andrew's Voice

**Tone:** Conversational, direct, self-deprecating
- Stories over statements
- Specific details (names, numbers, anecdotes)
- Contrarian takes encouraged
- Self-deprecating humor welcome

**Sentence Structure:**
- Average 11 words per sentence
- Punchy and direct
- One idea per sentence
- Heavy use of line breaks for emphasis

**Words to Use:** brutal, insane, crazy, obsessed, fascinating, genuinely, literally
**Words to Avoid:** synergy, leverage, optimize, stakeholder, thought leader, disrupt, pivot

**Always:**
- Use contractions
- Be specific (dollar amounts, percentages, names)
- End with questions or calls-to-discuss ("Thoughts?", "Has anyone tried this?")

**Never:**
- Hashtags on X (1.2% historical usage = effectively never)
- Corporate jargon or buzzwords
- Excessive emojis (max 1-2 per post, prefer: 🤯 😭 🔥)
- Generic motivational quotes without personal spin
- "I'm excited to announce..." without substance

### High-Performing Hooks

```
"This is a story about..."
"Here's the thing:"
"I learned this the hard way:"
"Reminder:"
"The best [X] I know..."
"A lesson I learn over and over again:"
"Crazy to me that..."
"[Number] words that ruin my day:"
```

### Platform Differences

**X/Twitter:**
- Punchy, under 280 chars ideal
- Single impactful tweets > threads
- No hashtags ever
- Full 4000 chars available for premium

**LinkedIn:**
- Professional but human
- 800-1500 words works well
- Newsletter-style with clear sections
- Same voice, more context

**Instagram:**
- Visual-first, caption secondary
- Always requires an image
- Quote cards and carousels perform well

**Threads:**
- Casual, X-style but longer OK
- More off-the-cuff observations
- Up to 500 chars

---

## Brand

**Colors:**
- Warm Cream: `#F5F0E6`
- Rich Brown: `#3D3028`
- Accent Gold: `#C4A77D`

**Instagram Story Quote Cards:**
- Background: `#0D2818` (dark forest green)
- Text: `#F5F5F5` (near-white)
- Font: Elegant high-contrast serif (Didot/Bodoni style)
- Format: 9:16 aspect ratio, 4K resolution
- **NO self-attribution** - Andrew doesn't quote himself. No "—Andrew Wilkinson", no "@awilkinson", no quotation marks around his own thoughts. It should look like he's sharing a thought directly, not quoting himself.
- Only use attribution for quotes from OTHER people (Munger, Buffett, etc.)

**Visual Style:**
- Simple, readable text
- Warm earthy palette (for posts)
- Dark forest green (for Stories)
- Quote cards: one punchy line (no attribution for Andrew's own words)
- Carousels: clear headlines, minimal text per slide

---

## Examples

**Perfect voice:**
> "Podcast idea: Interview tech entrepreneurs who raised tons of money then brutally failed.
>
> I'm not talking about the ones who stumbled, struggled, then made it through (like Slack).
>
> I'm talking, they manage a Cinnabon now.
>
> I'd listen to that."

**Wrong voice:**
> "🚀 Excited to share my TOP 5 tips for entrepreneurial success! #StartupLife #Hustle"

---

## Example Prompts

**Quick posts:**
- "Post something spicy about hiring"
- "Draft a tweet about why I hate meetings"
- "Write something for LinkedIn about selling companies"

**Mining the archive:**
- "Find my best content about investing"
- "What have I said about work-life balance?"
- "Search for anything about Metalab's early days"

**Audio content:**
- "Narrate my latest newsletter"
- "Generate audio for this post"
- "Create a voice clip from [content]"

**Visual content:**
- "Create a quote card: 'The best businesses are boring'"
- "Make a carousel about lessons from buying companies"
- "Generate an image for this post: [paste content]"

**Planning:**
- "Schedule a week of posts about entrepreneurship"
- "What topics from my archive haven't I posted about recently?"
- "Draft 5 tweets I can queue up"

Just tell me what you want. I'll figure out the rest.
