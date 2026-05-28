# Facebook Events Scraper

**Actor ID:** `apify/facebook-events-scraper`

Scrape Facebook events to discover networking opportunities, community gatherings, industry conferences, and potential leads through event participation data.

## Key Input Parameters

```json
{
  "searchQueries": ["Sport New York"],
  "startUrls": [],
  "maxEvents": 30
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `searchQueries` | array | Search queries to discover events. Can be topics ("Comedy"), places ("New York"), or combined ("Comedy New York") |
| `startUrls` | array | Direct URLs to scrape. Supports event details, search/explore URLs, page events, and group events |
| `maxEvents` | integer | Maximum number of events to scrape. Leave empty for unlimited (default: 30) |
| `proxy` | object | Proxy configuration. Recommended: `{"apifyProxyGroups": ["RESIDENTIAL"]}` for best results |
| `debugMode` | boolean | Enable debug logging (default: false) |

### Supported URL Formats

**Event Detail URLs:**
- `https://www.facebook.com/events/1023978871819924`

**Search URLs:**
- `https://www.facebook.com/events/search/?q=Party`
- `https://www.facebook.com/events/search?q=Comedy&filters=...` (with filters)

**Explore URLs:**
- `https://www.facebook.com/events/explore/fr-paris/110774245616525`

**Page Events:**
- `https://www.facebook.com/dcimprovcomedyclub/upcoming_hosted_events`
- `https://www.facebook.com/O.Vienna/past_hosted_events`

**Group Events:**
- `https://www.facebook.com/groups/freerussiansglobal/events`

**Note:** The pattern `https://www.facebook.com/PAGENAME/events` requires login and won't work. Use `upcoming_hosted_events` or `past_hosted_events` patterns instead.

## Output Fields

### Basic Event Information

| Field | Description |
|-------|-------------|
| `url` | Direct event URL |
| `id` | Event ID |
| `name` | Event name/title |
| `description` | Event description text |
| `imageUrl` | Event image URL |
| `imageCaption` | Image alt text/caption |
| `eventType` | Event type (e.g., "PUBLIC", "PRIVATE") |

### Date and Time

| Field | Description |
|-------|-------------|
| `dateTimeSentence` | Human-readable date/time (e.g., "SAT, FEB 25") |
| `utcStartDate` | Start date in UTC ISO format |
| `duration` | Event duration (e.g., "337 days" for recurring events) |
| `isPast` | Boolean indicating if event has already occurred |

### Location Information

The `location` object contains:

| Field | Description |
|-------|-------------|
| `url` | Location page URL (if available) |
| `id` | Location ID |
| `name` | Location name |
| `contextualName` | Full location context (e.g., "New York, NY, United States") |
| `placeType` | Type: "PLACE" or "TEXT" |
| `latitude` | Geographic latitude |
| `longitude` | Geographic longitude |
| `countryCode` | ISO country code |
| `streetAddress` | Street address |
| `city` | City name |

### Engagement Metrics

| Field | Description |
|-------|-------------|
| `usersGoing` | Number of users marked as "Going" |
| `usersInterested` | Number of users marked as "Interested" |
| `usersResponded` | Total number of users who responded |

### Organizer Information

| Field | Description |
|-------|-------------|
| `organizedBy` | Text description of organizers |
| `organizators` | Array of organizer objects |
| `privacyInfo` | Privacy and hosting information |

Each organizer object contains:

| Field | Description |
|-------|-------------|
| `id` | Organizer ID |
| `url` | Organizer profile/page URL |
| `name` | Organizer name |
| `isVerified` | Whether organizer is verified |

### Ticketing Information

The `ticketsInfo` object (if tickets are available):

| Field | Description |
|-------|-------------|
| `buyUrl` | Ticket purchase URL |
| `price` | Ticket price (if available) |
| `title` | Ticket information title (e.g., "Tickets · $5") |
| `subtitle` | Additional info (e.g., "via Eventbrite") |
| `ticketProvider` | Ticket platform name |

### Event Categories and Classification

| Field | Description |
|-------|-------------|
| `isOnline` | Boolean: Online event indicator |
| `paidContent` | Boolean: Paid event indicator |
| `isClassEvent` | Boolean: Class/educational event |
| `isLiveAudioRoom` | Boolean: Live audio room event |
| `isRemoteLearningClass` | Boolean: Remote learning class |
| `isRemoteLearningCourse` | Boolean: Remote learning course |
| `hasRecordingAvailable` | Boolean: Recording available after event |
| `groupEventPinnedToFeatured` | Boolean: Featured group event |
| `discoveryCategories` | Array of category objects with `url` and `label` |

### Additional Information

| Field | Description |
|-------|-------------|
| `externalLinks` | Array of external URLs mentioned in the event |

## Use Cases for Lead Generation

### 1. Industry Event Networking
Identify relevant industry conferences and trade shows where potential clients gather. Extract attendee interest levels and organizer information.

### 2. Local Business Outreach
Find local events where your target audience congregates. Use location data to identify geographic opportunities.

### 3. Competitor Analysis
Monitor events organized by competitors or industry players to understand market positioning and attendance patterns.

### 4. Partnership Opportunities
Discover organizations hosting events aligned with your business goals. Contact organizers for sponsorship or partnership discussions.

### 5. Community Engagement
Track community events to identify active groups and engaged audiences within your target market.

### 6. Event Marketing Intelligence
Analyze successful events (high attendance, engagement metrics) to inform your own event planning strategy.

## Example Searches for Lead Generation

**B2B Technology Events:**
```json
{
  "searchQueries": ["startup tech San Francisco", "business networking NYC"],
  "maxEvents": 50
}
```

**Local Market Research:**
```json
{
  "searchQueries": ["small business Chicago", "entrepreneur meetup Boston"],
  "maxEvents": 100
}
```

**Industry-Specific:**
```json
{
  "searchQueries": ["real estate conference", "marketing summit", "developer meetup"],
  "maxEvents": 75
}
```

**Search with Filters:**
Use Facebook's event search to apply filters (date range, online/offline, free/paid), then copy the URL:
```json
{
  "startUrls": [
    "https://www.facebook.com/events/search?q=Comedy&filters=eyJmaWx0ZXJfZXZlbnRzX2NhdGVnb3J5..."
  ],
  "maxEvents": 50
}
```

## Notes

- **No Login Required:** The scraper works without Facebook credentials for public events
- **Proxy Recommended:** Use residential proxies for better results and discovery diversity
- **Rate Limits:** Can scrape 2000+ events on average, but varies by search complexity
- **Private Events:** Only public events are accessible
- **Page Events:** For pages, use `upcoming_hosted_events` or `past_hosted_events` patterns, not `/events`
- **Group Events:** Use `/events` pattern for groups only
- **Personal Data:** Output may contain personal data (names, locations). Ensure compliance with data protection regulations

## Pricing

**Model:** Pay per event

- **Flat charge per run:** $0.001-$0.006 USD (tier-dependent)
- **Per event scraped:** $0.0021-$0.013 USD (tier-dependent)

Higher subscription tiers receive better per-event pricing.

## Related Actors for Social Media Lead Generation

- [Facebook Groups Scraper](apify-facebook-groups-scraper.md) - Find buying intent in group discussions
- [Facebook Pages Scraper](apify-facebook-pages-scraper.md) - Extract business page data
- [Facebook Posts Scraper](https://apify.com/apify/facebook-posts-scraper) - Scrape posts from profiles and pages
- [Facebook Comments Scraper](https://apify.com/apify/facebook-comments-scraper) - Extract comment discussions
- [Facebook Reviews Scraper](https://apify.com/apify/facebook-reviews-scraper) - Gather business reviews

## Essential Fields

For quick answers and basic data exports, these fields are most relevant (in priority order):

| Priority | Field | Description |
|----------|-------|-------------|
| 1 | `name` | Event name |
| 2 | `url` | Event URL |
| 3 | `dateTimeSentence` | Date/time |
| 4 | `location.name` | Venue name |
| 5 | `location.contextualName` | Location |
| 6 | `usersGoing` | Attendees |
| 7 | `usersInterested` | Interested |
| 8 | `organizedBy` | Organizer |
