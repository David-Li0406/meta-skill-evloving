# Google Search Scraper

**Actor ID:** `apify/google-search-scraper`

Scrape Google search results for lead discovery.

## Pricing Breakdown

**Base cost:** $4.50 per 1,000 search results pages scraped

Base tier includes: title, URL, description, rank, site links

### Optional Add-ons (per 1,000 results)
- Paid results/ads extraction: +$6.50

### Premium Add-ons 🚨
- Business leads enrichment (decision-maker contacts): +$100.00
- Google AI Mode (AI overviews, GEO tracking): +$200.00
- Perplexity AI search (cross-platform analysis): +$200.00

**Example costs for 100 results:**
- Base tier only: ~$0.45
- With paid ads extraction: ~$1.10
- With business leads: ~$10.45 🚨
- With Google AI Mode: ~$20.45 🚨
- With Perplexity AI: ~$20.45 🚨
- With all add-ons: ~$50+ 🚨

## Key Input Parameters

```json
{
  "queries": "software companies in Austin\nSaaS startups in Texas",
  "maxPagesPerQuery": 1,
  "resultsPerPage": 100,
  "countryCode": "us",
  "maximumLeadsEnrichmentRecords": 10
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `queries` | string | Search queries - use newlines to separate multiple queries (required). Can use advanced Google search techniques like "AI site:twitter.com" or "javascript OR python". Max 32 words per query. |
| `maxPagesPerQuery` | integer | Max pages to scrape per query (default: 1) |
| `resultsPerPage` | integer | Results per page: 10, 20, 30, 40, 50, 100 (default: 100). Note: actual results may differ due to Google's internal filtering. |
| `countryCode` | string | Country code for results (e.g., "us", "uk", "de"). Specifies Google domain and search country. |
| `languageCode` | string | Interface language code (e.g., "en", "es", "zh-CN"). Affects menus/buttons and may affect search results. |
| `searchLanguage` | string | Restricts search results to specific language (e.g., "en", "de", "ja"). Different from languageCode. |
| `mobileResults` | boolean | Use mobile user agent (default: false) |

## Common Use Cases

### Use Case 1: Basic Lead Discovery (Base Tier - Recommended)

Search Google to find companies, people, or content for lead generation.

**What you get:** Page titles, URLs, descriptions, rankings, site links

**Example: Find SaaS companies in Austin**

```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "apify/google-search-scraper" \
  --input '{
    "queries": "SaaS companies in Austin",
    "maxPagesPerQuery": 1,
    "resultsPerPage": 100,
    "countryCode": "us"
  }' \
  --output saas-companies-austin.csv \
  --format csv
```

**Cost:** ~$0.45 for 100 results

**AI Workflow:**
1. Ask user for search query and location/filters
2. Ask user for output format (CSV or JSON)
3. Run Actor with base parameters only (no add-ons)
4. Report: "Found X results. Key fields: title, url, description, rank"

---

### Use Case 2: Competitor Ad Analysis ($)

Extract paid search results (ads) to analyze competitor advertising strategies.

**Additional data:** Ad titles, URLs, descriptions, ad positions

**Example: Find companies advertising on "CRM software"**

```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "apify/google-search-scraper" \
  --input '{
    "queries": "CRM software",
    "maxPagesPerQuery": 1,
    "resultsPerPage": 100,
    "countryCode": "us",
    "includePaidResults": true
  }' \
  --output crm-ads.json \
  --format json
```

**Cost:** ~$1.10 for 100 results (+$0.65 for paid ads)

**AI Workflow:**
1. When user asks for "ads", "paid results", or "advertising analysis":

   > "I can enable paid results extraction to capture Google ads. This adds ~$6.50 per 1,000 results ($0.65 for 100 results). Continue? (y/n)"

2. If yes, add `"includePaidResults": true` to input
3. Report ad-specific fields found

---

### Use Case 3: B2B Lead Generation with Decision Makers ($$$)

⚠️ **Premium feature - High cost**

Find companies and extract decision-maker contacts (names, titles, emails, LinkedIn profiles).

**Additional data:** Employee names, job titles, work emails, LinkedIn URLs, company data

**Example: Find tech companies and their C-suite contacts**

```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "apify/google-search-scraper" \
  --input '{
    "queries": "AI startups in San Francisco",
    "maxPagesPerQuery": 1,
    "resultsPerPage": 20,
    "countryCode": "us",
    "maximumLeadsEnrichmentRecords": 5,
    "leadsEnrichmentDepartments": ["c_suite", "sales"]
  }' \
  --output ai-startups-contacts.json \
  --format json
```

**Cost:** ~$0.09 for 20 results (base) + ~$2.00 (leads enrichment) = ~$2.09 for 20 results 🚨

**AI Workflow:**
1. When user asks for "decision makers", "employee contacts", or "people at company":

   > "🚨 **Warning:** Business leads enrichment is a premium feature that costs $100 per 1,000 results (~$10 for 100 results, $2 for 20 results).
   >
   > This provides decision-maker names, job titles, work emails, and LinkedIn profiles.
   >
   > This is expensive and should only be used for high-value B2B outreach.
   >
   > Continue? (y/n)"

2. If yes, set `maximumLeadsEnrichmentRecords` (max leads per domain)
3. Optionally set `leadsEnrichmentDepartments` to filter by role
4. **Important:** Keep `resultsPerPage` low (20-50) to control costs

---

### Use Case 4: Google AI Mode Analysis ($$$)

⚠️ **Premium feature - Very high cost**

Track Google AI Overviews for Answer Engine Optimization (AEO) and brand visibility.

**Additional data:** AI-generated overview, featured sources, related questions

**Example: Monitor AI overviews for brand queries**

```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "apify/google-search-scraper" \
  --input '{
    "queries": "best CRM software 2024",
    "maxPagesPerQuery": 1,
    "resultsPerPage": 10,
    "countryCode": "us",
    "aiMode": "aiModeWithSearchResults"
  }' \
  --output ai-overview-crm.json \
  --format json
```

**Cost:** ~$0.05 for 10 results (base) + ~$2.00 (AI mode) = ~$2.05 for 10 results 🚨

**AI Workflow:**
1. When user asks for "AI overview", "GEO tracking", or "AI search analysis":

   > "🚨 **Warning:** Google AI Mode is a premium feature that costs $200 per 1,000 results (~$20 for 100 results, $2 for 10 results).
   >
   > This provides Google's AI-generated overviews and is useful for:
   > - Answer Engine Optimization (AEO) tracking
   > - Brand visibility in AI results
   > - Featured source analysis
   >
   > This is very expensive. I recommend testing with 10-20 results first.
   >
   > Continue? (y/n)"

2. If yes, set `aiMode` to "aiModeWithSearchResults" or "aiModeOnly"
3. **Critical:** Recommend keeping `resultsPerPage` very low (10-20) due to extreme cost

---

### Use Case 5: Perplexity AI Cross-Platform Search ($$$)

⚠️ **Premium feature - Very high cost**

Use Perplexity AI to get synthesized answers across multiple platforms.

**Additional data:** AI-generated answer with citations, related questions, images

**Example: Research a topic with Perplexity**

```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "apify/google-search-scraper" \
  --input '{
    "queries": "latest trends in B2B SaaS",
    "maxPagesPerQuery": 1,
    "resultsPerPage": 10,
    "countryCode": "us",
    "perplexitySearch": {
      "enablePerplexity": true,
      "searchRecency": "month",
      "returnImages": true,
      "returnRelatedQuestions": true
    }
  }' \
  --output perplexity-saas-trends.json \
  --format json
```

**Cost:** ~$0.05 for 10 results (base) + ~$2.00 (Perplexity) = ~$2.05 for 10 results 🚨

**AI Workflow:**
1. When user asks for "Perplexity", "AI research", or "cross-platform analysis":

   > "🚨 **Warning:** Perplexity AI search is a premium feature that costs $200 per 1,000 results (~$20 for 100 results, $2 for 10 results).
   >
   > This provides AI-synthesized answers with citations from multiple sources and is useful for:
   > - Comprehensive topic research
   > - Cross-platform content discovery
   > - Trend analysis with recent data
   >
   > This is very expensive. I recommend testing with 10-20 results first.
   >
   > Continue? (y/n)"

2. If yes, configure `perplexitySearch` object with desired options
3. **Critical:** Recommend keeping `resultsPerPage` very low (10-20) due to extreme cost

---

### Use Case 6: Recent Content Discovery (Base Tier)

Find recently published content using date filters.

**Example: Find articles about AI published in the last week**

```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "apify/google-search-scraper" \
  --input '{
    "queries": "artificial intelligence breakthrough",
    "maxPagesPerQuery": 1,
    "resultsPerPage": 50,
    "countryCode": "us",
    "quickDateRange": "w1"
  }' \
  --output ai-news-recent.csv \
  --format csv
```

**Cost:** ~$0.23 for 50 results (base tier only)

**AI Workflow:**
1. When user specifies time-based search ("recent", "last week", "today"):
2. Use `quickDateRange` (d[days], w[weeks], m[months]) or `afterDate`/`beforeDate`
3. No additional cost for date filters

---

### Use Case 7: Targeted Site Search (Base Tier)

Search within specific websites or domains.

**Example: Find mentions of a company on Twitter**

```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "apify/google-search-scraper" \
  --input '{
    "queries": "Apify site:twitter.com",
    "maxPagesPerQuery": 1,
    "resultsPerPage": 100,
    "countryCode": "us"
  }' \
  --output apify-twitter-mentions.csv \
  --format csv
```

**Cost:** ~$0.45 for 100 results (base tier only)

**AI Workflow:**
1. When user wants to search within a specific site:
2. Add `site:domain.com` to the query OR use the `site` parameter
3. No additional cost for site filtering

---

## Cost Management Guidelines for AI

### Default Behavior
- Always start with base tier (no add-ons)
- Never enable premium features without user confirmation
- Warn about extreme costs for AI Mode and Perplexity

### When to Ask About Paid Features

**Moderate-cost add-on (+$6.50 per 1,000 results):**
- User says "ads", "paid results" → Offer includePaidResults

**Prompt format:**
> "I can enable paid results extraction which adds ~$6.50 per 1,000 results ($Y for Z results). Continue? (y/n)"

**High-cost add-on (+$100 per 1,000 results):**
- User says "decision makers", "employee contacts" → Warn about business leads enrichment

**Prompt format:**
> "🚨 **Warning:** Business leads enrichment costs $100 per 1,000 results (~$10 for 100 results, $2 for 20 results).
>
> This provides decision-maker contacts and should only be used for high-value B2B outreach.
>
> I recommend starting with 20-50 results to control costs.
>
> Continue? (y/n)"

**Very high-cost add-ons (+$200 per 1,000 results):**
- User says "AI overview", "GEO tracking" → Warn about Google AI Mode
- User says "Perplexity", "cross-platform research" → Warn about Perplexity AI

**Prompt format:**
> "🚨 **Warning:** [Feature name] is a premium feature that costs $200 per 1,000 results (~$20 for 100 results, $2 for 10 results).
>
> [Explain what data it provides and use cases]
>
> This is VERY expensive. I strongly recommend testing with only 10-20 results first.
>
> Continue? (y/n)"

### Cost Estimation

Always show cost estimate before running:
- Calculate: (results / 1000) × (base cost + add-on costs)
- For multiple queries: multiply by number of queries
- Show estimate: "Estimated cost: $X.XX"

### Cost Control Strategies

For expensive add-ons, always recommend:
1. **Start small:** Test with 10-20 results first
2. **Reduce resultsPerPage:** Lower from 100 to 10-20 for premium features
3. **Limit queries:** Use 1-2 queries initially, not 10+
4. **Explain cost math:** "Each query × results = total cost"

### Alternative Suggestions

If user declines premium features:
- "Decision makers" → "I can find company websites with base search, then use Contact Details Scraper separately (cheaper)"
- "AI overview" → "I can provide regular search results which you can analyze yourself"
- "Perplexity" → "I can search Google normally, then you can research topics manually"

## Date Filters

| Parameter | Type | Description |
|-----------|------|-------------|
| `afterDate` | string | Filter results after date. Absolute (e.g., "2024-05-03") or relative (e.g., "8 days", "3 months"). UTC timezone. |
| `beforeDate` | string | Filter results before date. Absolute (e.g., "2024-05-03") or relative (e.g., "8 days", "3 months"). UTC timezone. |
| `quickDateRange` | string | Quick date range filter: d[number] for days, h[number] for hours, w[number] for weeks, m[number] for months, y[number] for years (e.g., "d10", "m3", "y1"). Don't combine with afterDate/beforeDate. |

## Business Leads Enrichment ($)

| Parameter | Type | Description |
|-----------|------|-------------|
| `maximumLeadsEnrichmentRecords` | integer | Max business leads per domain with employee names, job titles, emails, LinkedIn profiles, company data (default: 0 = disabled). Contains personal data - comply with GDPR. |
| `leadsEnrichmentDepartments` | array | Filter leads by department: "c_suite", "sales", "marketing", "product", "engineering_technical", "design", "education", "finance", "human_resources", "information_technology", "legal", "medical_health", "operations", "consulting". Only works when maximumLeadsEnrichmentRecords > 0. |

## AI Features ($)

| Parameter | Type | Description |
|-----------|------|-------------|
| `aiMode` | string | Google AI Mode for Answer Engine Optimization (AEO), GEO targeting, brand visibility tracking: "aiModeOff" (default), "aiModeWithSearchResults", "aiModeOnly" |
| `perplexitySearch` | object | Perplexity AI search for cross-platform analysis. Object with: `enablePerplexity` (boolean), `searchRecency` ("day", "week", "month", "year"), `returnImages` (boolean), `returnRelatedQuestions` (boolean) |

## Advanced Search Filters

| Parameter | Type | Description |
|-----------|------|-------------|
| `site` | string | Restrict search to specific site (e.g., "twitter.com") |
| `relatedToSite` | string | Find sites related to specified domain |
| `wordsInText` | string | Search for words in page text |
| `wordsInTitle` | string | Search for words in page title |
| `wordsInUrl` | string | Search for words in URL |
| `fileTypes` | array | Filter by file types (e.g., ["pdf", "doc"]) |
| `includeUnfilteredResults` | boolean | Include results Google normally filters out (may return more results) |
| `saveHtml` | boolean | Save HTML of results pages (default: false) |
| `saveHtmlToKeyValueStore` | boolean | Save HTML to key-value store instead of dataset (default: false) |

## Output Fields

### Basic Search Result

| Field | Description |
|-------|-------------|
| `title` | Result title |
| `url` | Result URL |
| `displayedUrl` | Displayed URL |
| `description` | Result snippet/description |
| `emphasizedKeywords` | Keywords highlighted in description |
| `siteLinks` | Additional site links |
| `searchQuery` | Object with search query details (term, url, device, page, type, domain, countryCode, languageCode, resultsPerPage) |
| `rank` | Result ranking position |

### Business Leads (Add-on)

Available when `maximumLeadsEnrichmentRecords` > 0:

| Field | Description |
|-------|-------------|
| `leadsEnrichment` | Array of enriched business leads with full name, email, job title, department, seniority, LinkedIn profile, company information (name, domain, industry, employee count) |

### AI Results (Add-on)

Available when `aiMode` is enabled or `perplexitySearch.enablePerplexity` is true:

| Field | Description |
|-------|-------------|
| `aiOverview` | Google AI Mode overview and analysis (when aiMode enabled) |
| `perplexityAnswer` | Perplexity AI generated answer with citations (when perplexitySearch enabled) |

## Essential Fields

For quick answers and basic data exports, these fields are most relevant (in priority order):

| Priority | Field | Description |
|----------|-------|-------------|
| 1 | `title` | Result title |
| 2 | `url` | Result URL |
| 3 | `description` | Snippet |
| 4 | `rank` | Position |
