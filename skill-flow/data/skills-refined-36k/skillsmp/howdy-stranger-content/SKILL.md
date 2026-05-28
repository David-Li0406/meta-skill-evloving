---
name: howdy-stranger-content
description: Manages content creation and data updates for Howdy, Stranger - independent economic commentary site. Use for creating posts, updating financial indicators, managing media, and maintaining JSON data files.
---

# Howdy, Stranger Content Management

Skill for managing all content updates and data maintenance on the static HTML site covering economic analysis, news, and lifestyle commentary.

## Overview

**Howdy, Stranger** is a static HTML/CSS/JS site with no backend database. All content is stored in JSON data files and markdown posts. This skill covers:
- Post creation and publishing
- Financial data indicator updates
- Media management
- News feed curation
- Site data maintenance

## Post Creation Workflow

Posts are stored as markdown files in `article/posts/` and referenced in `json/posts.json`.

### 1. Create Markdown Post File

Create a new file in `article/posts/` following the naming convention:
- Format: `YYYY-MM-DD-slug-title.md`
- Example: `2026-01-08-jancara-playlist.md`

Structure the markdown with optional YAML frontmatter:

```markdown
---
title: Optional Frontmatter Title
---

# Post Title

Content with optional lucide icons like `<i data-lucide="chart-line"></i>`.

## Structured Content

- Support for markdown headers, lists, tables
- Images: `![Alt text](path/to/image.webp)`
- Links: `[text](url)`

{{chart:Consumer Sentiment}}
```

### 2. Add Entry to posts.json

Add a new object to the array in `json/posts.json`:

```json
{
  "date": "2026-01-08T19:00:00Z",
  "file": "article/posts/2026-01-08-trade-deficit-debt-snapshot.md"
}
```

**Date format:** ISO 8601 with timezone (e.g., `2026-01-08T19:00:00Z` for UTC)

**Key rules:**
- Posts are displayed in reverse chronological order (newest first)
- Times are used to order posts from the same day (earlier times appear after later times in the list)
- Latest posts should be at the top of the array

### 3. Content Guidelines

**Avoid AI Red Flags** (from AGENTS.md):
- Avoid em dashes (—) and hyphens (-) in prose
  - Don't: "The tariff isn't the objective—it's the deterrent"
  - Do: "The tariff functions as a deterrent"
- Avoid the "It's not X, it's Y" inversion pattern

**Best Practices:**
- Include lucide icon in first heading or markdown: `<i data-lucide="book-open"></i>`
- First paragraph becomes the card snippet (max ~160 chars)
- First image becomes the card preview image
- Include financial data references when relevant (check `financials-data.json` for latest data)

### 4. Post Rendering

The `posts-loader.js` automatically:
- Extracts title from first h1/h2/h3 or strong tag
- Uses first image for card preview
- Truncates first paragraph for snippet
- Processes markdown via marked.js
- Wraps tables for mobile responsiveness
- Renders financial charts with `{{chart:Indicator Name}}`
- Wraps images with links to media.html

## Financial Data Management

All economic indicators are centralized in `json/financials-data.json`.

### Structure

```json
{
  "lastUpdated": "2026-01-08T20:30:00Z",
  "indices": [
    {
      "category": "Business Indicators",
      "agency": "FRED",
      "name": "10-yr Treasury Yield",
      "lastUpdated": "2025-12-10T14:00:00Z",
      "releaseDay": 0,
      "url": "https://fred.stlouisfed.org/series/DGS10",
      "march": "4.28",
      "april": "4.28",
      "may": "4.42",
      ...
      "explanation": "..."
    }
  ]
}
```

### Adding or Updating Indicators

**Monthly data fields:**
- Use lowercase month names: `january`, `february`, ..., `december`
- Store as strings with units (e.g., "4.28" for percentages, "$5,200" for prices)
- Can include "M" or "K" suffixes for large numbers (e.g., "4.00M" for millions)

**Required fields:**
- `name` - Display name for charts
- `category` - One of: Business Indicators, Consumer Indicators, Commodities, Housing Market, Trade & Tariffs, Employment Indicators, Prediction Markets
- `agency` - Data source (FRED, BLS, Census, Zillow, Kalshi, etc.)
- `explanation` - 2-3 sentence description for tooltips
- `lastUpdated` - ISO 8601 timestamp of last data refresh
- Monthly data fields with values

**Optional fields:**
- `releaseDay` - Typical release day of month (0 = varies)
- `url` - Link to source data
- `bps_probabilities` - For prediction markets (basis point odds)
- `game_title`, `game_time_iso` - For sports markets

### Calculating Month-over-Month Percentages

When publishing posts with financial data, calculate and verify MoM changes:

**Formula**: `((Current - Previous) / Previous) × 100`

**Verification steps:**
1. Identify current and previous month values from `financials-data.json`
2. Calculate the difference: Current - Previous
3. Divide by previous value: Difference / Previous
4. Multiply by 100 to get percentage
5. Round to one decimal place
6. Always double-check using a calculator before publishing

**Example:**
- November value: 79.2
- December value: 71.8
- Difference: 79.2 - 71.8 = 7.4
- Percentage: (7.4 / 79.2) × 100 = 9.34% → rounds to **9.3%**

**Critical:** Arithmetic errors in financial posts damage credibility. Verify all calculations before publishing.

### Chart Types

Charts are automatically selected based on indicator type:
- **Line charts** - Most economic indicators (default)
- **Bar charts** - Prediction markets (when `bps_probabilities` present)
- **Trade deficit charts** - When indicator has `imports` and `exports` fields

### Calculating Month-over-Month Percentages

When publishing posts with financial data, calculate and verify MoM changes:

**Formula**: `((Current - Previous) / Previous) × 100`

**Verification steps:**
1. Identify current and previous month values from `financials-data.json`
2. Calculate the difference: Current - Previous
3. Divide by previous value: Difference / Previous
4. Multiply by 100 to get percentage
5. Round to one decimal place
6. Always double-check using a calculator before publishing

**Example:**
- November value: 79.2
- December value: 71.8
- Difference: 79.2 - 71.8 = 7.4
- Percentage: (7.4 / 79.2) × 100 = 9.34% → rounds to **9.3%**

**Critical:** Arithmetic errors in financial posts damage credibility. Verify all calculations before publishing.

### Embedding Charts in Posts

Use the chart syntax in markdown:

```markdown
{{chart:Consumer Sentiment}}
```

The renderer will:
1. Parse the indicator name from financials-data.json
2. Extract monthly values
3. Create appropriate chart type
4. Render with responsive Chart.js

## Media Management

Media items are stored in `json/media.json` and displayed on `media.html`.

### Add Media Entry

```json
{
  "slug": "my-media-item",
  "title": "Media Title",
  "category": "music|film|book|podcast",
  "date": "2025-12-20",
  "link": "https://example.com",
  "image": "images/filename.webp"
}
```

**Slug format:** lowercase, hyphens, no spaces

**Image guidelines:**
- Use `.webp` format for modern browsers
- Store in `images/` directory
- Naming: `YYYY-MM-author-title.webp`

Posts can link to media items: `<a href="media.html#slug">link text</a>`

## Journal/Feed Management

Social media feeds and journal entries in `json/journal.json`:

```json
{
  "date": "2025-12-20",
  "content": "Tweet or status update",
  "source": "twitter|mastodon|custom",
  "link": "https://example.com/status"
}
```

## Common Workflow: Data Update Post

When publishing a data update (e.g., monthly economic indicators):

1. **Update `financials-data.json`:**
   - Find indicator by name
   - Update `lastUpdated` timestamp
   - Add new month value (use previous data as reference for format)
   - Update root-level `lastUpdated` timestamp

2. **Create post referencing the data:**
   - File: `article/posts/YYYY-MM-DD-indicator-update.md`
   - Include context and analysis
   - Embed chart with `{{chart:Indicator Name}}`
   - Link to `financials.html` if applicable

3. **Add to posts.json:**
   - Use correct ISO date/time
   - Place at top of array for latest posts

4. **Example:**
   ```markdown
   # Consumer Sentiment Surges in December
   
   <i data-lucide="chart-line"></i>
   
   Latest University of Michigan consumer sentiment data shows strong confidence recovery...
   
   {{chart:Consumer Sentiment}}
   
   The surge reflects...
   ```

## Technical Notes

### Posts Loader (`js/posts-loader.js`)

- Loads 8 posts initially (INITIAL_LOAD: 8)
- "Load More" button loads 10 at a time (BATCH_SIZE: 10)
- Uses `marked.js` for markdown parsing
- Chart.js for financial visualizations
- Lucide icons for illustrations
- Real-time "X minutes ago" timestamps

### Color Scheme

- Primary: `#2C5F5A` (teal)
- Accent: `#D4822A` (orange)
- Secondary: `#666` (gray)
- Support both light and dark modes via CSS variables

### CSS Classes for Content

- `.announcement-card` - Post card container
- `.card-expanded-content` - Full post content (hidden by default)
- `.card-title` - Post heading
- `.card-snippet` - Preview text
- `.chart-container` - Financial chart wrapper
- `.table-wrapper` - Responsive table wrapper

## File Locations

- **Posts:** `article/posts/*.md`
- **Posts index:** `json/posts.json`
- **Financial data:** `json/financials-data.json`
- **Media:** `json/media.json` + `images/`
- **Journal:** `json/journal.json`
- **Post loader:** `js/posts-loader.js`
- **HTML pages:** `index.html`, `financials.html`, `media.html`, etc.

## When to Use This Skill

- Creating new posts for Index, Media, Journal pages
- Updating monthly economic indicators
- Adding media posts
- Publishing news feed items
- Maintaining data freshness for the site
