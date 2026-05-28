# Advanced Lead Generation Workflows

Multi-step workflows that combine multiple Actors for complex lead generation tasks.

---

## Workflow 1: B2B Lead List Building

Build a comprehensive B2B lead list combining multiple sources.

### Checklist

```
Task Progress:
- [ ] Clarify target industry and location
- [ ] Step 1: Run Google Maps Scraper for businesses
- [ ] Step 2: Run Contact Details Scraper on websites found
- [ ] Combine and deduplicate results
- [ ] Export final lead list
```

### Example Interaction

**User:** "Build a lead list for SaaS companies in Austin"

**Response:**
1. Start with Google Search or Maps to find companies
2. Extract websites from results
3. Run Contact Details Scraper on each website
4. Merge results into single lead list with:
   - Company name
   - Website
   - Email addresses
   - Phone numbers
   - Social profiles

---

## Workflow 2: YouTube Creator Lead Generation

Find YouTube creators making content about a specific topic.

### Checklist

```
Task Progress:
- [ ] Get topic/keyword from user
- [ ] Ask how many videos to search (default: 50)
- [ ] Run YouTube Scraper to find videos
- [ ] Extract unique channel names from results
- [ ] Run YouTube Scraper again for channel details
- [ ] Report creator stats and contact info
```

### Example Interaction

**User:** "Give me leads for YouTube creators about Claude Code"

**Response:**
1. Ask: "How many videos should I search? (default: 50)"
2. Step 1 - Find videos about the topic:

```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "streamers/youtube-scraper" \
  --input '{"searchKeywords": ["Claude Code"], "maxResults": 50}' \
  --output claude-code-videos.json \
  --format json
```

3. Extract unique channel names/URLs from results
4. Step 2 - Get detailed channel information:

```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "streamers/youtube-scraper" \
  --input '{"startUrls": [{"url": "https://www.youtube.com/@channel1"}, {"url": "https://www.youtube.com/@channel2"}], "maxResults": 1}' \
  --output youtube-creators.csv \
  --format csv
```

5. Report: "Found 35 unique creators making Claude Code content. Top channels by subscribers: Channel A (50K), Channel B (25K), Channel C (12K). Key fields: channelName, subscriberCount, description, email (if available)."

### Tips
- Use specific keywords to find niche creators
- Filter results by subscriber count for influencer tiers
- Look for email in channel description for outreach
- Consider engagement rate (views/subscribers) not just subscriber count
