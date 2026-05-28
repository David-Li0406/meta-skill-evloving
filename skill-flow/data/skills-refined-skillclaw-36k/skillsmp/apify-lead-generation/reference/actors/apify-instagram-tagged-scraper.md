# Instagram Mentions Scraper

**Actor ID:** `apify/instagram-tagged-scraper`

Extract data from tagged posts and mentions on Instagram. Scrape post text, hashtags, mentions, comments, images, likes, locations, and metadata from any public Instagram account.

## Key Input Parameters

```json
{
  "username": ["natgeo"],
  "resultsLimit": 20
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `username` | array | Instagram username(s) or URL(s) of profiles to scrape tagged posts from (required) |
| `resultsLimit` | integer | Maximum number of tagged posts per profile (default: 20) |

## Output Fields

### Basic Post Information

| Field | Description |
|-------|-------------|
| `id` | Post ID |
| `type` | Post type (e.g., "Sidecar") |
| `shortCode` | Short code identifier |
| `url` | Direct post URL |
| `caption` | Post text content |
| `timestamp` | Post timestamp (ISO format) |

### Engagement Metrics

| Field | Description |
|-------|-------------|
| `commentsCount` | Total number of comments |
| `firstComment` | Text of the first comment |
| `latestComments` | Array of latest comment objects |

### Content Details

| Field | Description |
|-------|-------------|
| `hashtags` | Array of hashtags used in post |
| `mentions` | Array of mentioned usernames |

### Comment Object Fields

Each comment in `latestComments` includes:

| Field | Description |
|-------|-------------|
| `id` | Comment ID |
| `text` | Comment text |
| `ownerUsername` | Username of commenter |
| `ownerProfilePicUrl` | Commenter's profile picture URL |
| `timestamp` | Comment timestamp (ISO format) |
| `likesCount` | Number of likes on comment |
| `repliesCount` | Number of replies to comment |
| `replies` | Array of reply objects |

## Essential Fields

For quick answers and basic data exports, these fields are most relevant (in priority order):

| Priority | Field | Description |
|----------|-------|-------------|
| 1 | `url` | Post URL |
| 2 | `caption` | Post text |
| 3 | `timestamp` | Post date |
| 4 | `commentsCount` | Number of comments |
| 5 | `hashtags` | Hashtags used |
