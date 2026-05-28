# Facebook Page Contact Information Scraper

**Actor ID:** `apify/facebook-page-contact-information`

Extract contact details from Facebook business pages including addresses, email, phone numbers, website, likes, and check-ins data.

## Key Input Parameters

```json
{
  "pages": ["https://www.facebook.com/humansofnewyork/", "apifytech"],
  "language": "en-US"
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `pages` | array | Facebook page URLs or page IDs/usernames. Supports both full URLs (https://www.facebook.com/pagename/) and short handles (pagename) (required) |
| `language` | string | Language code that affects the dataset output format. Default: "en-US". Supports 100+ language codes (af-ZA, en-GB, es-ES, de-DE, fr-FR, ja-JP, zh-CN, etc.) |

### Supported Page Formats

**Full URLs:**
- `https://www.facebook.com/humansofnewyork/`
- `https://www.facebook.com/apifytech`

**Short Handles:**
- `humansofnewyork`
- `apifytech`

**Page IDs:**
- Any valid Facebook page ID

## Output Fields

### Basic Page Information

| Field | Description |
|-------|-------------|
| `pageUrl` | Full Facebook page URL |
| `pageId` | Facebook page ID |
| `pageName` | Business/page name |
| `category` | Business category |
| `likes` | Number of page likes |
| `checkins` | Number of check-ins (if available) |

### Contact Information

| Field | Description |
|-------|-------------|
| `email` | Email address (if publicly available) |
| `phone` | Phone number (if publicly available) |
| `website` | Website URL (if listed) |

### Address Information

| Field | Description |
|-------|-------------|
| `address` | Full street address |
| `city` | City name |
| `zip` | Postal/ZIP code |
| `country` | Country name |
| `latitude` | Geographic latitude |
| `longitude` | Geographic longitude |

### Additional Information

| Field | Description |
|-------|-------------|
| `about` | About section text |
| `description` | Page description |
| `hours` | Business hours information (if available) |
| `priceRange` | Price range indicator (e.g., "$", "$$", "$$$") |
| `rating` | Average rating score |
| `reviewCount` | Number of reviews |

## Essential Fields

For quick answers and basic data exports, these fields are most relevant (in priority order):

| Priority | Field | Description |
|----------|-------|-------------|
| 1 | `pageName` | Page name |
| 2 | `pageUrl` | Facebook URL |
| 3 | `email` | Email |
| 4 | `phone` | Phone |
| 5 | `website` | Website |
| 6 | `address` | Full address |
| 7 | `city` | City |
| 8 | `category` | Category |
