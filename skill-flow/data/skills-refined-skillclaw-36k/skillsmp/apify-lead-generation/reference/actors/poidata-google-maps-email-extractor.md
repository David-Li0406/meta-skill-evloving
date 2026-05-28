# Google Maps Email Extractor

**Actor ID:** `poidata/google-maps-email-extractor`

Extract emails, phone numbers, and social media links directly from Google Maps listings and their websites. Supports coordinate radius and GeoJSON polygon searches for precise geographic targeting.

**Pricing:** $8 per 1,000 results ($0.008 per business record). Tiered pricing available (FREE tier: $0.01, BRONZE: $0.008, SILVER: $0.007, GOLD+: $0.006)

## Key Input Parameters

```json
{
  "term": ["Restaurant"],
  "location": "New York, USA",
  "total": 20,
  "has_website": true,
  "min_rating": "4.0"
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `term` | array | Search keywords (max 25 chars each, required). Multiple terms like ["cafe", "bakery"] |
| `location` | string | City or address (max 50 chars, e.g., "New York, USA") |
| `total` | integer | Max results per term (max 300 per term, max 4,500 for 50 terms, default: 20) |
| `language` | string | Language for search results (default: "en") |
| `country` | string | Country context for search results (default: "us") |

## Advanced Search Methods

**Search Priority:** Polygon > Geocoordinate > Location

### Coordinate Radius Search

| Parameter | Type | Description |
|-----------|------|-------------|
| `latitude` | string | Decimal latitude for coordinate search |
| `longitude` | string | Decimal longitude for coordinate search |
| `radius` | integer | Search radius in miles around coordinates (default: 1) |
| `totalAroundCoordinate` | integer | Max results within radius/polygon (max 300, default: 20) |

### GeoJSON Polygon Search

| Parameter | Type | Description |
|-----------|------|-------------|
| `polygon` | string | GeoJSON polygon coordinates defining custom search area. Use [Keene College Polyline Tool](https://www.keene.edu/campus/maps/tool/) to create polygons. |
| `totalAroundCoordinate` | integer | Max results within polygon (max 300, default: 20) |

## Email & Social Extraction Options

| Parameter | Type | Description |
|-----------|------|-------------|
| `has_email` | boolean | Only include businesses with extracted emails (default: false) |
| `tech_enabled` | boolean | Enable advanced email extraction techniques (default: true) |
| `social_enabled` | boolean | Extract social media links from websites (default: true) |

## Filters

| Parameter | Type | Description |
|-----------|------|-------------|
| `min_rating` | string | Minimum star rating 0-5, decimals allowed (default: "0") |
| `min_reviews` | integer | Minimum number of reviews (default: 0) |
| `min_photos` | integer | Minimum number of photos (default: 0) |
| `has_website` | boolean | Only include businesses with websites (default: false) |
| `name_filter` | string | Filter businesses by name (case-insensitive substring match) |
| `categories_filter` | array | Filter by business categories (comma-separated, case-insensitive) |

## Output Fields

### Basic Business Information

| Field | Description |
|-------|-------------|
| `name` | Business name |
| `address` | Full address |
| `street` | Street address |
| `neighborhood` | Neighborhood name |
| `city` | City name |
| `state` | State name |
| `zip` | Zip/postal code |
| `country` | Country code (e.g., "US") |
| `country_code` | Country code lowercase (e.g., "us") |
| `country_name` | Full country name (e.g., "United States") |

### Contact Information

| Field | Description |
|-------|-------------|
| `emails` | Array of extracted email addresses |
| `phone` | Phone number (formatted) |
| `phoneIsd` | International phone format (e.g., "+1 212-246-2183") |
| `website` | Website URL |
| `social` | Object with social media links (facebook, instagram, linkedin, youtube arrays) |

### Location Data

| Field | Description |
|-------|-------------|
| `latitude` | Latitude coordinate |
| `longitude` | Longitude coordinate |

### Ratings & Reviews

| Field | Description |
|-------|-------------|
| `rating` | Star rating (0-5) |
| `reviewCount` | Number of reviews |

### Identifiers & Links

| Field | Description |
|-------|-------------|
| `url` | Google Maps URL for the business |
| `placeId` | Google Place ID |
| `cid` | Google CID (Company ID) |
| `gid` | Google GID (unique identifier used for deduplication) |

### Media & Additional Info

| Field | Description |
|-------|-------------|
| `photo` | Primary photo URL |
| `photoCount` | Total number of photos |
| `additionalInfo` | Object with detailed business information (Accessibility, amenities, etc.) |

### Search Metadata

| Field | Description |
|-------|-------------|
| `searchTerm` | Original search term used |
| `searchLocation` | Original search location used |
| `original_rank` | Original ranking in Google Maps results |
| `display_rank` | Display ranking after filtering |
| `distance_miles` | Distance from search coordinates (when using coordinate/polygon search) |
| `timestamp` | Timestamp when data was scraped (ISO format) |

## Performance Features

- **Incremental Saving:** Results saved to dataset in real-time as they're processed
- **Deduplication:** Unique businesses identified by `gid`, prevents duplicates across multiple search terms
- **Concurrent Processing:** Websites processed at 5 requests per second for fast email extraction

## Essential Fields

For quick answers and basic data exports, these fields are most relevant (in priority order):

| Priority | Field | Description |
|----------|-------|-------------|
| 1 | `name` | Business name |
| 2 | `url` | Google Maps link |
| 3 | `address` | Full address |
| 4 | `phone` | Phone number |
| 5 | `emails` | Email addresses |
| 6 | `website` | Website URL |
| 7 | `rating` | Star rating |
| 8 | `social` | Social media links |
