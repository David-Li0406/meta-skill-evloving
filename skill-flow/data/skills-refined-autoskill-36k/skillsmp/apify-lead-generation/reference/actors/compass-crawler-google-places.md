# Google Maps Scraper

**Actor ID:** `compass/crawler-google-places`

Scrape local businesses from Google Maps with contact details, ratings, and reviews.

**Pricing:** Event-based pricing starting at $4 per 1,000 places (FREE tier). Additional features and add-ons have separate pricing. See [detailed pricing](https://help.apify.com/en/articles/10774732-google-maps-scraper-is-going-to-pay-per-event-pricing).

## Pricing Breakdown

**Base cost:** $4 per 1,000 places

Free tier includes: business name, address, phone, website, category, rating, coordinates

### Optional Add-ons (per 1,000 places)
- Filters (categoryFilterWords, placeMinimumStars, etc.): +$1.00
- Place details (opening hours, popular times, review distribution): +$2.00
- Company contacts (emails, social profiles from websites): +$2.00
- Reviews: +$0.50 per 1,000 reviews
- Images: +$0.50 per 1,000 images

### Premium Add-ons 🚨
- Business leads enrichment (decision-maker contacts): +$100.00
- Social media profile enrichment (follower counts, verification): +$100.00

**Example costs for 100 places:**
- Free tier only: ~$0.40
- With place details + contacts: ~$0.80
- With business leads: ~$10.40 🚨

## Basic Search Parameters

```json
{
  "searchStringsArray": ["restaurant"],
  "locationQuery": "New York, USA",
  "maxCrawledPlacesPerSearch": 50,
  "language": "en"
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `searchStringsArray` | array | Search terms (e.g., "restaurant", "gym") |
| `locationQuery` | string | Location using free text (city + country recommended) |
| `maxCrawledPlacesPerSearch` | integer | Max results per search term (leave empty for all) |
| `language` | string | Results language (default: "en") - supports 100+ languages |
| `allPlacesNoSearchAction` | string | Scrape all visible places on map: "all_places_no_search_ocr" or "all_places_no_search_mouse" |

## Common Use Cases

### Use Case 1: Basic Lead Discovery (FREE - Recommended)

Find local businesses with essential contact information.

**What you get:** Business name, address, phone, website, category, rating

**Example: Find coffee shops in Seattle**

```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "compass/crawler-google-places" \
  --input '{"searchStringsArray": ["coffee shops"], "locationQuery": "Seattle, USA", "maxCrawledPlacesPerSearch": 100, "language": "en"}' \
  --output coffee-shops-seattle.csv \
  --format csv
```

**Cost:** ~$0.40 for 100 results

**AI Workflow:**
1. Ask user for business type and location
2. Ask user for output format (CSV or JSON)
3. Run Actor with free tier parameters only
4. Report: "Found X businesses. Key fields: title, address, phone, website, rating"

---

### Use Case 2: Enriched Leads with Contact Details ($)

Add email addresses and social media profiles scraped from business websites.

**Additional data:** Emails, Facebook, Instagram, LinkedIn, Twitter, YouTube URLs

**Example: Coffee shops with contact enrichment**

```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "compass/crawler-google-places" \
  --input '{
    "searchStringsArray": ["coffee shops"],
    "locationQuery": "Seattle, USA",
    "maxCrawledPlacesPerSearch": 100,
    "language": "en",
    "scrapeContacts": true
  }' \
  --output coffee-shops-enriched.csv \
  --format csv
```

**Cost:** ~$0.60 for 100 results (+$0.20 for contact scraping)

**AI Workflow:**
1. When user asks for "emails" or "contact info", ask for confirmation:

   > "I can enable contact enrichment to extract emails and social profiles from business websites. This adds ~$2 per 1,000 places ($0.20 for 100 places). Continue? (y/n)"

2. If yes, add `"scrapeContacts": true` to input
3. Report contact fields found: emails, social profiles

---

### Use Case 3: Deep Place Analysis ($)

Get detailed information including opening hours, popular times, and review distribution.

**Additional data:** Opening hours, popular times, review breakdown by star rating, questions & answers

**Example: Coffee shops with place details**

```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "compass/crawler-google-places" \
  --input '{
    "searchStringsArray": ["coffee shops"],
    "locationQuery": "Seattle, USA",
    "maxCrawledPlacesPerSearch": 100,
    "language": "en",
    "scrapePlaceDetailPage": true
  }' \
  --output coffee-shops-details.csv \
  --format csv
```

**Cost:** ~$0.60 for 100 results (+$0.20 for place details)

**AI Workflow:**
1. When user asks for "opening hours", "popular times", or "detailed info":

   > "I can scrape the detailed place pages for opening hours, popular times, and review distribution. This adds ~$2 per 1,000 places ($0.20 for 100 places). Continue? (y/n)"

2. If yes, add `"scrapePlaceDetailPage": true` to input

---

### Use Case 4: Review Collection ($)

Extract customer reviews for sentiment analysis or competitor research.

**Additional data:** Review text, author, rating, date, likes, response from owner

**Example: Get recent reviews for top coffee shops**

```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "compass/crawler-google-places" \
  --input '{
    "searchStringsArray": ["coffee shops"],
    "locationQuery": "Seattle, USA",
    "maxCrawledPlacesPerSearch": 20,
    "language": "en",
    "maxReviews": 50,
    "reviewsSort": "newest"
  }' \
  --output coffee-reviews.json \
  --format json
```

**Cost:** ~$0.08 for 20 places + ~$0.05 for 1,000 reviews

**AI Workflow:**
1. When user asks for "reviews" or "customer feedback", ask:

   > "How many reviews per place should I collect? (default: 50)"

2. Explain cost if large number requested
3. Suggest reviewsSort options: "newest", "mostRelevant", "highestRanking", "lowestRanking"

---

### Use Case 5: High-Quality Filtered Leads ($)

Use filters to find only businesses matching specific criteria.

**Filters available:**
- Minimum star rating (2.0 to 4.5 stars)
- Specific categories (4,000+ available)
- Website presence (with/without website)
- Exclude closed businesses

**Example: Find only highly-rated coffee shops with websites**

```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "compass/crawler-google-places" \
  --input '{
    "searchStringsArray": ["coffee shops"],
    "locationQuery": "Seattle, USA",
    "maxCrawledPlacesPerSearch": 100,
    "language": "en",
    "placeMinimumStars": "four",
    "website": "withWebsite",
    "skipClosedPlaces": true
  }' \
  --output high-quality-coffee-shops.csv \
  --format csv
```

**Cost:** ~$0.50 for 100 results (+$0.10 for filters)

**AI Workflow:**
1. When user mentions quality criteria ("highly rated", "with website", "open now"):

   > "I can apply filters for minimum rating, website presence, and exclude closed places. This adds ~$1 per 1,000 places ($0.10 for 100 places). Continue? (y/n)"

2. Map user requirements to filter parameters

---

### Use Case 6: B2B Lead Generation with Decision Makers ($$$)

⚠️ **Premium feature - High cost**

Extract decision-maker contacts (names, titles, emails, LinkedIn profiles) from businesses.

**Additional data:** Employee names, job titles, work emails, LinkedIn URLs

**Example: Find restaurant owners/managers**

```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "compass/crawler-google-places" \
  --input '{
    "searchStringsArray": ["restaurants"],
    "locationQuery": "Seattle, USA",
    "maxCrawledPlacesPerSearch": 20,
    "language": "en",
    "maximumLeadsEnrichmentRecords": 5,
    "leadsEnrichmentDepartments": ["c_suite", "sales"]
  }' \
  --output restaurant-decision-makers.json \
  --format json
```

**Cost:** ~$2.00 for 20 places (base) + ~$2.00 (premium add-on) = ~$4.00 for 20 places 🚨

**AI Workflow:**
1. When user asks for "decision makers", "employee contacts", or "people at company":

   > "🚨 **Warning:** Business leads enrichment is a premium feature that costs $100 per 1,000 places (~$10 for 100 places, $2 for 20 places).
   >
   > This provides decision-maker names, job titles, work emails, and LinkedIn profiles.
   >
   > This is expensive and should only be used for high-value B2B outreach.
   >
   > Continue? (y/n)"

2. If yes, set `maximumLeadsEnrichmentRecords` (max leads per place)
3. Optionally set `leadsEnrichmentDepartments` to filter by role

---

### Use Case 7: Social Media Analytics ($$$)

⚠️ **Premium feature - High cost**

Get detailed social media analytics (follower counts, verification status, descriptions).

**Additional data:** Facebook/Instagram/YouTube/TikTok/Twitter follower counts, verification badges, bios

**Example: Coffee shops with Instagram analytics**

```bash
uv run --with python-dotenv --with requests \
  ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.py \
  --actor "compass/crawler-google-places" \
  --input '{
    "searchStringsArray": ["coffee shops"],
    "locationQuery": "Seattle, USA",
    "maxCrawledPlacesPerSearch": 20,
    "language": "en",
    "scrapeSocialMediaProfiles": {
      "instagrams": true,
      "facebooks": true
    }
  }' \
  --output coffee-social-analytics.json \
  --format json
```

**Cost:** ~$0.08 for 20 places (base) + ~$2.00 (premium add-on) = ~$2.08 for 20 places 🚨

**AI Workflow:**
1. When user asks for "follower counts", "social media analytics", or "Instagram stats":

   > "🚨 **Warning:** Social media profile enrichment costs $100 per 1,000 places (~$10 for 100 places, $2 for 20 places).
   >
   > This provides detailed analytics: follower counts, verification status, profile descriptions.
   >
   > For basic social profile URLs (no analytics), use the free "scrapeContacts" option instead (+$2 per 1,000 places).
   >
   > Continue with full analytics? (y/n)"

2. If no, suggest using `scrapeContacts: true` instead for basic URLs
3. If yes, configure which platforms to analyze

---

## Cost Management Guidelines for AI

### Default Behavior
- Always start with FREE tier (searchStringsArray, locationQuery, maxCrawledPlacesPerSearch, language)
- Never enable paid features without user confirmation

### When to Ask About Paid Features

**Low-cost add-ons (+$0.50 to +$2 per 1,000 places):**
- User says "get emails" → Offer scrapeContacts
- User says "opening hours" → Offer scrapePlaceDetailPage
- User says "reviews" → Offer maxReviews
- User says "highly rated only" → Offer filters

**Prompt format:**
> "I can enable [feature name] which adds ~$X per 1,000 places ($Y for Z places). Continue? (y/n)"

**Premium add-ons (+$100 per 1,000 places):**
- User says "decision makers", "employee contacts" → Warn about business leads enrichment
- User says "follower counts", "social analytics" → Warn about social media enrichment

**Prompt format:**
> "🚨 **Warning:** [Feature name] is a premium feature that costs $100 per 1,000 places (~$N for your request).
>
> [Explain what data it provides]
>
> This is expensive and should only be used for [appropriate use case].
>
> Continue? (y/n)"

### Cost Estimation

Always show cost estimate before running:
- Count how many places will be scraped (maxCrawledPlacesPerSearch)
- Calculate: (places / 1000) × (base cost + add-on costs)
- Show estimate: "Estimated cost: $X.XX"

### Alternative Suggestions

If user declines premium features, suggest free/cheaper alternatives:
- "Decision makers" → "I can get basic contact info with scrapeContacts instead (+$2/1,000)"
- "Social analytics" → "I can get social profile URLs with scrapeContacts instead (+$2/1,000)"

## Search Filters & Categories ($)

| Parameter | Type | Description |
|-----------|------|-------------|
| `categoryFilterWords` | array | Filter by place categories (e.g., "restaurant", "hotel"). See 4,000+ [available categories](https://api.apify.com/v2/key-value-stores/epxZwNRgmnzzBpNJd/records/categories) |
| `searchMatching` | string | Name matching: "all" (default), "only_includes", or "only_exact" |
| `placeMinimumStars` | string | Min star rating: "two", "twoAndHalf", "three", "threeAndHalf", "four", "fourAndHalf" |
| `website` | string | Filter by website: "allPlaces" (default), "withWebsite", "withoutWebsite" |
| `skipClosedPlaces` | boolean | Skip temporarily or permanently closed places (default: false) |

## Place Details ($)

| Parameter | Type | Description |
|-----------|------|-------------|
| `scrapePlaceDetailPage` | boolean | Scrape detail page for additional fields like opening hours, popular times, reviews distribution (default: false) |
| `scrapeTableReservationProvider` | boolean | Scrape restaurant reservation provider data (name, email, phone) |
| `includeWebResults` | boolean | Include "Web results" section from place listing |
| `scrapeDirectories` | boolean | Scrape businesses inside malls/shopping centers |
| `maxQuestions` | integer | Number of questions to extract (0 = first question only, 999 = all) |

## Reviews

| Parameter | Type | Description |
|-----------|------|-------------|
| `maxReviews` | integer | Number of reviews per place (leave empty for all, max 5,000 per output item) |
| `reviewsStartDate` | string | Extract reviews after date (e.g., "2024-05-03" or "8 days", "3 months") |
| `reviewsSort` | string | Sort by: "newest" (default), "mostRelevant", "highestRanking", "lowestRanking" |
| `reviewsFilterString` | string | Filter reviews by keywords (leave blank for all) |
| `reviewsOrigin` | string | Review source: "all" (default) or "google" only |
| `scrapeReviewsPersonalData` | boolean | Include reviewer ID, name, URL, photo (default: true) |

## Images ($)

| Parameter | Type | Description |
|-----------|------|-------------|
| `maxImages` | integer | Number of images per place (leave empty for all) |
| `scrapeImageAuthors` | boolean | Include image author names (slower processing) |

## Add-ons ($)

| Parameter | Type | Description |
|-----------|------|-------------|
| `scrapeContacts` | boolean | Company contacts enrichment from website (emails, social media profiles) |
| `scrapeSocialMediaProfiles` | object | Detailed social media profile enrichment (follower counts, descriptions, verification) |
| `scrapeSocialMediaProfiles.facebooks` | boolean | Enable Facebook profile scraping |
| `scrapeSocialMediaProfiles.instagrams` | boolean | Enable Instagram profile scraping |
| `scrapeSocialMediaProfiles.youtubes` | boolean | Enable YouTube channel scraping |
| `scrapeSocialMediaProfiles.tiktoks` | boolean | Enable TikTok profile scraping |
| `scrapeSocialMediaProfiles.twitters` | boolean | Enable X (Twitter) profile scraping |
| `maximumLeadsEnrichmentRecords` | integer | Business leads enrichment - max leads per place (default: 0) |
| `leadsEnrichmentDepartments` | array | Filter leads by department: "c_suite", "sales", "marketing", "product", "engineering_technical", etc. |

## Geolocation Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `countryCode` | string | Country code (e.g., "us", "uk", "de") |
| `city` | string | City name (do not include state/country here) |
| `state` | string | State/province name |
| `county` | string | County/regional district/département |
| `postalCode` | string | Postal code (combine only with countryCode, not city) |
| `customGeolocation` | object | Custom search area using GeoJSON (Polygon, MultiPolygon, Point with radiusKm) |

## Direct Input

| Parameter | Type | Description |
|-----------|------|-------------|
| `startUrls` | array | Google Maps URLs (max 300 results per URL) |
| `placeIds` | array | List of Google Place IDs (format: "ChIJreV9aqYWdkgROM_boL6YbwA") |

## Output Fields

### Basic Information

| Field | Description |
|-------|-------------|
| `title` | Business name |
| `subTitle` | Subtitle (if available) |
| `categoryName` | Primary business category |
| `categories` | Array of all business categories |
| `description` | Place description |
| `price` | Price level (e.g., "$10–20", "$$") |

### Contact & Location

| Field | Description |
|-------|-------------|
| `address` | Full address with street, city, state, zip, country |
| `street` | Street address |
| `city` | City name |
| `postalCode` | Postal/ZIP code |
| `state` | State/province |
| `countryCode` | Country code |
| `neighborhood` | Neighborhood name |
| `phone` | Formatted phone number |
| `phoneUnformatted` | Phone in international format (e.g., +17183565168) |
| `website` | Website URL |
| `location` | Object with latitude (lat) and longitude (lng) coordinates |
| `plusCode` | Google Plus Code |

### Identifiers

| Field | Description |
|-------|-------------|
| `placeId` | Google Place ID |
| `cid` | Google CID (Company ID) |
| `fid` | Google FID |
| `url` | Google Maps URL |
| `searchPageUrl` | Original search page URL |

### Ratings & Reviews

| Field | Description |
|-------|-------------|
| `totalScore` | Average rating (1-5) |
| `reviewsCount` | Total number of reviews |
| `reviewsDistribution` | Object with review counts by star rating (oneStar, twoStar, etc.) |
| `reviews` | Array of review objects (if maxReviews > 0) |
| `reviewsTags` | Popular review topics with counts |

### Images

| Field | Description |
|-------|-------------|
| `imageUrl` | Primary image URL |
| `imagesCount` | Total number of images |
| `imageCategories` | Array of image categories (e.g., "Menu", "Food & drink", "Vibe") |
| `images` | Array of image objects with URL, author, upload date (if maxImages > 0) |
| `imageUrls` | Array of all image URLs |

### Business Details

| Field | Description |
|-------|-------------|
| `openingHours` | Array of operating hours by day |
| `permanentlyClosed` | Boolean flag for permanently closed |
| `temporarilyClosed` | Boolean flag for temporarily closed |
| `claimThisBusiness` | Boolean flag indicating if business is unclaimed |
| `isAdvertisement` | Boolean flag for ad placements |
| `locatedIn` | Parent location (for businesses inside malls, etc.) |

### Additional Features

| Field | Description |
|-------|-------------|
| `additionalInfo` | Object with detailed characteristics (service options, accessibility, payments, etc.) |
| `menu` | Menu URL |
| `peopleAlsoSearch` | Array of similar places users search for |
| `placesTags` | Array of place-related tags |
| `questionsAndAnswers` | Q&A section data (if maxQuestions > 0) |
| `updatesFromCustomers` | Customer updates/posts |
| `ownerUpdates` | Updates from business owner |

### Restaurant-Specific

| Field | Description |
|-------|-------------|
| `reserveTableUrl` | Table reservation URL |
| `tableReservationLinks` | Array of reservation provider links |
| `orderBy` | Array of online ordering options |
| `restaurantData` | Object with restaurant-specific data (reservation provider info) |

### Hotel-Specific

| Field | Description |
|-------|-------------|
| `hotelStars` | Hotel star rating |
| `hotelDescription` | Hotel description text |
| `checkInDate` | Check-in date (if provided in input) |
| `checkOutDate` | Check-out date (if provided in input) |
| `similarHotelsNearby` | Array of similar hotels with pricing |
| `hotelAds` | Array of hotel booking ads |
| `hotelReviewSummary` | Summary of hotel reviews |

### Enrichment Data (Add-ons)

| Field | Description |
|-------|-------------|
| `emails` | Extracted email addresses (from scrapeContacts) |
| `instagrams` | Instagram profile URLs (from scrapeContacts) |
| `facebooks` | Facebook page/profile URLs (from scrapeContacts) |
| `linkedIns` | LinkedIn profile URLs (from scrapeContacts) |
| `youtubes` | YouTube channel URLs (from scrapeContacts) |
| `tiktoks` | TikTok profile URLs (from scrapeContacts) |
| `twitters` | Twitter/X profile URLs (from scrapeContacts) |
| `pinterests` | Pinterest profile URLs (from scrapeContacts) |
| `discords` | Discord server URLs (from scrapeContacts) |
| `leadsEnrichment` | Array of business leads with full name, email, job title, LinkedIn (from maximumLeadsEnrichmentRecords) |

### Metadata

| Field | Description |
|-------|-------------|
| `searchString` | Original search string used |
| `rank` | Result ranking position |
| `scrapedAt` | Timestamp when place was scraped |
| `webResults` | Web search results (if includeWebResults enabled) |

## Essential Fields

For quick answers and basic data exports, these fields are most relevant (in priority order):

| Priority | Field | Description |
|----------|-------|-------------|
| 1 | `title` | Business name |
| 2 | `url` | Google Maps link |
| 3 | `address` | Full address |
| 4 | `phone` | Phone number |
| 5 | `website` | Website URL |
| 6 | `totalScore` | Rating (1-5) |
| 7 | `reviewsCount` | Number of reviews |
| 8 | `categoryName` | Primary category |
