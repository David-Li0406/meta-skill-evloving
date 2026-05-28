---
name: apify-lead-generation
description: Generates B2B/B2C leads by scraping Google Maps, websites, Instagram, TikTok, Facebook, LinkedIn, YouTube, and Google Search. Use when user asks to find leads, prospects, businesses, build lead lists, enrich contacts, or scrape profiles for sales outreach.
---

# Lead Generation

Scrape leads from multiple platforms using Apify Actors.

## Prerequisites

- `.env` file with `APIFY_TOKEN`
- Python 3.9+ and `uv`

## Workflow

Copy this checklist and track progress:

```
Task Progress:
- [ ] Step 1: Determine lead source (select Actor)
- [ ] Step 2: Read Actor schema from reference docs
- [ ] Step 3: Ask user preferences (format, filename)
- [ ] Step 4: Run the lead finder script
- [ ] Step 5: Summarize results
```

### Step 1: Determine Lead Source

Select the appropriate Actor based on user needs:

| User Need | Actor ID | Best For | Reference Doc |
|-----------|----------|----------|---------------|
| Local businesses | `compass/crawler-google-places` | Restaurants, gyms, shops | [Schema](reference/actors/compass-crawler-google-places.md) |
| Contact enrichment | `vdrmota/contact-info-scraper` | Emails, phones from URLs | [Schema](reference/actors/vdrmota-contact-info-scraper.md) |
| Instagram profiles | `apify/instagram-profile-scraper` | Influencer discovery | [Schema](reference/actors/apify-instagram-profile-scraper.md) |
| Instagram posts/comments | `apify/instagram-scraper` | Posts, comments, hashtags, places | [Schema](reference/actors/apify-instagram-scraper.md) |
| Instagram search | `apify/instagram-search-scraper` | Places, users, hashtags discovery | [Schema](reference/actors/apify-instagram-search-scraper.md) |
| TikTok videos/hashtags | `clockworks/tiktok-scraper` | Comprehensive TikTok data extraction | [Schema](reference/actors/clockworks-tiktok-scraper.md) |
| TikTok hashtags/profiles | `clockworks/free-tiktok-scraper` | Free TikTok data extractor | [Schema](reference/actors/clockworks-free-tiktok-scraper.md) |
| TikTok user search | `clockworks/tiktok-user-search-scraper` | Find users by keywords | [Schema](reference/actors/clockworks-tiktok-user-search-scraper.md) |
| TikTok profiles | `clockworks/tiktok-profile-scraper` | Creator outreach | [Schema](reference/actors/clockworks-tiktok-profile-scraper.md) |
| TikTok followers/following | `clockworks/tiktok-followers-scraper` | Audience analysis, segmentation | [Schema](reference/actors/clockworks-tiktok-followers-scraper.md) |
| Facebook pages | `apify/facebook-pages-scraper` | Business contacts | [Schema](reference/actors/apify-facebook-pages-scraper.md) |
| Facebook page contacts | `apify/facebook-page-contact-information` | Extract emails, phones, addresses | [Schema](reference/actors/apify-facebook-page-contact-information.md) |
| Facebook groups | `apify/facebook-groups-scraper` | Buying intent signals | [Schema](reference/actors/apify-facebook-groups-scraper.md) |
| Facebook events | `apify/facebook-events-scraper` | Event networking, partnerships | [Schema](reference/actors/apify-facebook-events-scraper.md) |
| Google Search | `apify/google-search-scraper` | Broad lead discovery | [Schema](reference/actors/apify-google-search-scraper.md) |
| YouTube channels | `streamers/youtube-scraper` | Creator partnerships | [Schema](reference/actors/streamers-youtube-scraper.md) |
| Google Maps emails | `poidata/google-maps-email-extractor` | Direct email extraction | [Schema](reference/actors/poidata-google-maps-email-extractor.md) |

### Step 2: Read Actor Schema

Read the corresponding reference doc from the table above to understand:
- Required and optional input parameters
- Output fields available
- Actor-specific requirements

### Step 3: Ask User Preferences

Before running, ask:
1. **Output format**:
   - **Quick answer** - Display top 5 results in chat (no file saved)
   - **CSV (all data)** - Full export with all fields
   - **CSV (basic fields)** - Export with essential fields only
   - **JSON (all data)** - Full export in JSON format
2. **Output filename** (if file output selected): Suggest descriptive name based on search

### Step 4: Run the Script

**Quick answer (display in chat, no file):**
```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT'
```

**CSV (all data):**
```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT' \
  --output OUTPUT_FILE.csv \
  --format csv
```

**CSV (basic fields):**
```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT' \
  --output OUTPUT_FILE.csv \
  --format csv \
  --fields basic
```

**JSON (all data):**
```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT' \
  --output OUTPUT_FILE.json \
  --format json
```

The script handles:
- Loading `APIFY_TOKEN` from `.env`
- Starting and polling the Actor run
- Downloading results in requested format (or displaying in chat)
- Reporting record count and file size

### Step 5: Summarize Results

After completion, report:
- Number of leads found
- File location
- Key fields available
- Suggested next steps (filtering, enrichment)

## Quick Examples

**Quick answer - display top 5 in chat:**
```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "compass/crawler-google-places" \
  --input '{"searchStringsArray": ["coffee shops"], "locationQuery": "Seattle, USA", "maxCrawledPlacesPerSearch": 50}'
```

**Google Maps - CSV with basic fields:**
```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "compass/crawler-google-places" \
  --input '{"searchStringsArray": ["coffee shops"], "locationQuery": "Seattle, USA", "maxCrawledPlacesPerSearch": 50}' \
  --output coffee-shops-seattle.csv \
  --format csv \
  --fields basic
```

**Contact enrichment - full JSON export:**
```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "vdrmota/contact-info-scraper" \
  --input '{"startUrls": [{"url": "https://example.com"}], "maxRequestsPerStartUrl": 20}' \
  --output contacts.json \
  --format json
```

See [reference/workflows.md](reference/workflows.md) for detailed step-by-step guides for each use case.

## Error Handling

| Error | Solution |
|-------|----------|
| `APIFY_TOKEN not found` | Ask user to create `.env` with `APIFY_TOKEN=your_token` |
| `Actor not found` | Check Actor ID spelling |
| `Run FAILED` | Ask user to check Apify console link in error output |
| `Timeout` | Reduce input size or increase `--timeout` |
