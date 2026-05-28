# Instagram Profile Scraper

**Actor ID:** `apify/instagram-profile-scraper`

Scrape Instagram profile data including followers, bio, and recent posts.

## Key Input Parameters

```json
{
  "usernames": ["humansofny"],
  "includeAboutSection": false
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `usernames` | array | Instagram usernames, IDs, or profile URLs (required) |
| `includeAboutSection` | boolean | Extract account info (date joined, country) - paid add-on (default: false) |

## Output Fields

### Basic Profile Information

| Field | Description |
|-------|-------------|
| `inputUrl` | Original input URL provided |
| `id` | Instagram profile ID |
| `username` | Instagram handle |
| `url` | Profile URL |
| `fullName` | Display name |
| `biography` | Profile bio |
| `followersCount` | Number of followers |
| `followsCount` | Number following |
| `postsCount` | Total posts |
| `highlightReelCount` | Number of highlight reels |
| `igtvVideoCount` | Number of IGTV videos |

### Account Status & Type

| Field | Description |
|-------|-------------|
| `isBusinessAccount` | Business account flag |
| `verified` | Verification status |
| `private` | Private account flag |
| `joinedRecently` | Boolean flag indicating if account is recently created |
| `hasChannel` | Boolean flag for channel status |
| `businessCategoryName` | Business category |

### External Links & URLs

| Field | Description |
|-------|-------------|
| `externalUrl` | Website link in bio |
| `externalUrlShimmed` | Shimmed version of external URL |
| `externalUrls` | Array of link objects with title, url, lynx_url, link_type |

### Profile Pictures

| Field | Description |
|-------|-------------|
| `profilePicUrl` | Standard resolution profile picture URL |
| `profilePicUrlHD` | High definition profile picture URL |

### Related Profiles

| Field | Description |
|-------|-------------|
| `relatedProfiles` | Array of related profile objects with id, username, full_name, is_verified, is_private, profile_pic_url |

### Latest Content

| Field | Description |
|-------|-------------|
| `latestPosts` | Array of most recent 12 posts with full details (id, type, shortCode, caption, hashtags, mentions, url, commentsCount, likesCount, timestamp, dimensions, displayUrl, images, videoUrl, videoViewCount, isPinned, isCommentsDisabled, childPosts, taggedUsers) |
| `latestIgtvVideos` | Array of latest IGTV videos (up to 12) with full details (id, type, shortCode, title, caption, url, likesCount, videoViewCount, videoDuration, timestamp, dimensions, hashtags, mentions, taggedUsers) |

### About Section (Add-on)

Available when `includeAboutSection` is enabled:

| Field | Description |
|-------|-------------|
| `about` | Object with detailed account information |
| `about.accounts_with_shared_followers` | Accounts with shared followers |
| `about.country` | Country of origin (if user filled in) |
| `about.date_joined` | Date joined Instagram (formatted string) |
| `about.date_joined_as_timestamp` | Date joined as Unix timestamp |
| `about.date_verified` | Date account was verified (formatted string) |
| `about.date_verified_as_timestamp` | Verification date as Unix timestamp |
| `about.former_usernames` | Number of times username was changed |
| `about.id` | Profile ID |
| `about.is_verified` | Verification status |
| `about.username` | Username |

## Essential Fields

For quick answers and basic data exports, these fields are most relevant (in priority order):

| Priority | Field | Description |
|----------|-------|-------------|
| 1 | `username` | Instagram handle |
| 2 | `url` | Profile URL |
| 3 | `fullName` | Display name |
| 4 | `followersCount` | Number of followers |
| 5 | `postsCount` | Total posts |
| 6 | `biography` | Profile bio |
| 7 | `externalUrl` | Website link |
| 8 | `verified` | Verified status |
