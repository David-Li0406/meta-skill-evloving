# TikTok User Search Scraper

**Actor ID:** `clockworks/tiktok-user-search-scraper`

Extract data about users based on TikTok user search. Get full user profiles including name, nickname, signature, number of followers, number of videos, bio link, and author's ID.

## Key Input Parameters

```json
{
  "searchQueries": ["cats"],
  "maxProfilesPerQuery": 10
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `searchQueries` | array | Search keywords for finding TikTok profiles (required) - works on any query that works on TikTok |
| `maxProfilesPerQuery` | integer | Maximum number of profiles to extract per query (default: 10) |

## Output Fields

### Profile Information

| Field | Description |
|-------|-------------|
| `id` | User's unique TikTok ID |
| `name` | Username/handle |
| `nickName` | Display name |
| `avatar` | Profile picture URL |
| `verified` | Boolean flag indicating if account is verified |
| `signature` | User bio/signature text |
| `bioLink` | Link in bio (if present) |

### Account Statistics

| Field | Description |
|-------|-------------|
| `fans` | Number of followers |
| `video` | Total number of videos posted |

### Account Type

| Field | Description |
|-------|-------------|
| `privateAccount` | Boolean flag indicating if account is private |
| `ttSeller` | Boolean flag indicating if user is a TikTok seller |

## Essential Fields

For quick answers and basic data exports, these fields are most relevant (in priority order):

| Priority | Field | Description |
|----------|-------|-------------|
| 1 | `name` | Username |
| 2 | `nickName` | Display name |
| 3 | `fans` | Followers |
| 4 | `video` | Video count |
| 5 | `verified` | Verified status |
| 6 | `signature` | Bio |
| 7 | `bioLink` | Bio link |
