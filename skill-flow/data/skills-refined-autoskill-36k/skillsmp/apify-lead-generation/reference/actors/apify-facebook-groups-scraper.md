# Facebook Groups Scraper

**Actor ID:** `apify/facebook-groups-scraper`

Scrape posts from Facebook groups to find buying intent.

## Key Input Parameters

```json
{
  "startUrls": [{"url": "https://www.facebook.com/groups/874728723021553"}],
  "resultsLimit": 20,
  "viewOption": "CHRONOLOGICAL"
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `startUrls` | array | Public Facebook group URLs (required) |
| `resultsLimit` | integer | Number of posts to scrape (default: 20) |
| `viewOption` | string | Sorting order: "CHRONOLOGICAL", "RECENT_ACTIVITY", "TOP_POSTS", "CHRONOLOGICAL_LISTINGS" (default: "CHRONOLOGICAL") - CHRONOLOGICAL_LISTINGS is for BuySell groups |
| `searchGroupKeyword` | string | Search by letter or keywords (limited without login) |
| `searchGroupYear` | string | Filter posts by year (requires searchGroupKeyword) |
| `onlyPostsNewerThan` | string | Scrape posts from date to present (YYYY-MM-DD, ISO timestamp, or relative like "1 days", "2 months", "3 years", "1 hour", "2 minutes") |

## Output Fields

### Basic Post Information

| Field | Description |
|-------|-------------|
| `facebookUrl` | Facebook group URL |
| `url` | Direct post URL |
| `time` | Post timestamp (ISO format) |
| `text` | Post content |
| `id` | Post ID |
| `legacyId` | Legacy post ID |
| `feedbackId` | Feedback ID |
| `facebookId` | Facebook ID |
| `inputUrl` | Original input URL |

### Author Information

| Field | Description |
|-------|-------------|
| `user` | Object with author information |
| `user.id` | Post author ID |
| `user.name` | Post author name |

### Group Information

| Field | Description |
|-------|-------------|
| `groupTitle` | Group name |
| `pageAdLibrary` | Ad library information object (is_business_page_active, id) |

### Engagement Metrics

| Field | Description |
|-------|-------------|
| `topReactionsCount` | Top reactions count |
| `reactionLikeCount` | Number of like reactions |
| `reactionLoveCount` | Number of love reactions (if available) |
| `likesCount` | Total likes |
| `sharesCount` | Share count |
| `commentsCount` | Comment count |

### Comments

| Field | Description |
|-------|-------------|
| `topComments` | Array of top comment objects with detailed information |

Top comment object fields:

| Field | Description |
|-------|-------------|
| `commentUrl` | Direct comment URL |
| `id` | Comment ID |
| `feedbackId` | Comment feedback ID |
| `date` | Comment timestamp (ISO format) |
| `text` | Comment text |
| `profileUrl` | Commenter's profile URL |
| `profilePicture` | Commenter's profile picture URL |
| `profileId` | Commenter's profile ID |
| `profileName` | Commenter's name |
| `likesCount` | Number of likes on comment |
| `threadingDepth` | Comment thread depth (0 for top-level comments) |

## Essential Fields

For quick answers and basic data exports, these fields are most relevant (in priority order):

| Priority | Field | Description |
|----------|-------|-------------|
| 1 | `url` | Post URL |
| 2 | `user.name` | Author name |
| 3 | `text` | Post content |
| 4 | `time` | Post date |
| 5 | `likesCount` | Likes |
| 6 | `commentsCount` | Comments |
| 7 | `groupTitle` | Group name |
