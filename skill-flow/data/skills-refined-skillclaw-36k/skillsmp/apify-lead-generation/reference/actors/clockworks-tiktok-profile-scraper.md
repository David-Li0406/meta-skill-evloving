# TikTok Profile Scraper

**Actor ID:** `clockworks/tiktok-profile-scraper`

Scrape TikTok profiles and their video content.

## Key Input Parameters

```json
{
  "profiles": ["apifyoffice"],
  "resultsPerPage": 100,
  "profileSorting": "latest",
  "profileScrapeSections": ["videos"]
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `profiles` | array | TikTok usernames (required) |
| `resultsPerPage` | integer | Max videos per profile (default: 100) |
| `profileSorting` | string | "latest", "popular", or "oldest" (default: "latest") - date filters only work with "latest" and "oldest" |
| `profileScrapeSections` | array | Sections to scrape: "videos" or "reposts" (default: ["videos"]) |
| `oldestPostDateUnified` | string | Scrape videos published after date (YYYY-MM-DD or relative like "1 day") |
| `newestPostDate` | string | Scrape videos published before date (YYYY-MM-DD) |
| `mostDiggs` | integer | Scrape videos with number of hearts less than specified number (doesn't work with date filters) |
| `leastDiggs` | integer | Scrape videos with number of hearts ≥ specified number (doesn't work with date filters) |
| `maxFollowersPerProfile` | integer | Charged filter - scrape only profiles with less followers than specified |
| `maxFollowingPerProfile` | integer | Charged filter - scrape only profiles with less following than specified |
| `excludePinnedPosts` | boolean | Exclude pinned posts from profiles (default: false) |
| `shouldDownloadVideos` | boolean | Download TikTok videos (increases time and costs, default: false) |
| `shouldDownloadCovers` | boolean | Download video cover images/thumbnails (increases time and costs, default: false) |
| `shouldDownloadSubtitles` | boolean | Download video subtitles when present (increases time and costs, default: false) |
| `shouldDownloadSlideshowImages` | boolean | Download slideshow images (increases time and costs, default: false) |
| `shouldDownloadAvatars` | boolean | Download authors' profile pictures (increases time and costs, default: false) |
| `videoKvStoreIdOrName` | string | Name or ID of Key Value Store for videos and media (omit to use default store) |

## Output Fields

### Basic Video Information

| Field | Description |
|-------|-------------|
| `id` | TikTok video ID |
| `text` | Video caption |
| `createTime` | Unix timestamp |
| `createTimeISO` | ISO timestamp |
| `webVideoUrl` | TikTok web URL |
| `input` | Original input username |
| `isAd` | Boolean flag indicating if video is an ad |
| `isSlideshow` | Boolean flag indicating if content is a slideshow |
| `isPinned` | Boolean flag indicating if video is pinned |

### Author Information (authorMeta)

| Field | Description |
|-------|-------------|
| `authorMeta.id` | Author ID |
| `authorMeta.name` | Username |
| `authorMeta.nickName` | Display name |
| `authorMeta.verified` | Verification status |
| `authorMeta.signature` | Bio |
| `authorMeta.bioLink` | Bio link URL |
| `authorMeta.avatar` | Profile picture URL |
| `authorMeta.privateAccount` | Boolean flag for private account |
| `authorMeta.region` | Account region/country code |
| `authorMeta.roomId` | Live room ID |
| `authorMeta.ttSeller` | Boolean flag for TikTok seller status |
| `authorMeta.following` | Number of accounts following |
| `authorMeta.friends` | Number of friends |
| `authorMeta.fans` | Follower count |
| `authorMeta.heart` | Total likes received |
| `authorMeta.video` | Total video count |
| `authorMeta.digg` | Number of videos liked by author |
| `authorMeta.commerceUserInfo` | Commerce user information object |

### Engagement Metrics

| Field | Description |
|-------|-------------|
| `playCount` | Video views |
| `diggCount` | Video likes (hearts) |
| `commentCount` | Video comments |
| `shareCount` | Video shares |
| `collectCount` | Number of times video was collected/bookmarked |

### Video & Media

| Field | Description |
|-------|-------------|
| `mediaUrls` | Array of video URLs |
| `videoMeta` | Object with video metadata (height, width, duration, coverUrl, originalCoverUrl, definition, format, downloadAddr, originalDownloadAddr, subtitleLinks) |

### Music Information (musicMeta)

| Field | Description |
|-------|-------------|
| `musicMeta.musicName` | Music track name |
| `musicMeta.musicAuthor` | Music author |
| `musicMeta.musicOriginal` | Boolean flag for original music |
| `musicMeta.musicId` | Music track ID |
| `musicMeta.playUrl` | Music play URL |
| `musicMeta.coverMediumUrl` | Music cover image URL |

### Content Tags

| Field | Description |
|-------|-------------|
| `hashtags` | Array of hashtag objects with name |
| `mentions` | Array of mentioned users |
| `effectStickers` | Array of effect stickers used in video |

## Essential Fields

For quick answers and basic data exports, these fields are most relevant (in priority order):

| Priority | Field | Description |
|----------|-------|-------------|
| 1 | `webVideoUrl` | Video URL |
| 2 | `authorMeta.name` | Username |
| 3 | `authorMeta.nickName` | Display name |
| 4 | `authorMeta.fans` | Followers |
| 5 | `authorMeta.bioLink` | Bio link |
| 6 | `playCount` | Views |
| 7 | `diggCount` | Likes |
