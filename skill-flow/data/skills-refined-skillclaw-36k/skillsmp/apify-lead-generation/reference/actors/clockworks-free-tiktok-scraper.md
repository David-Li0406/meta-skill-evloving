# TikTok Data Extractor

**Actor ID:** `clockworks/free-tiktok-scraper`

Extract data about videos, users, and channels based on hashtags or scrape full user profiles including posts, total likes, name, nickname, numbers of comments, shares, followers, following, and more.

## Key Input Parameters

```json
{
  "hashtags": ["fyp"],
  "resultsPerPage": 100,
  "shouldDownloadCovers": false,
  "shouldDownloadSlideshowImages": false,
  "shouldDownloadSubtitles": false,
  "shouldDownloadVideos": false
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `hashtags` | array | TikTok hashtags to scrape videos from (e.g., ["fyp", "funny"]) |
| `resultsPerPage` | integer | Number of videos to scrape per hashtag, profile, or search query (default: 1) |
| `profiles` | array | TikTok usernames to scrape (e.g., ["khaby.lame"]) |
| `profileScrapeSections` | array | Profile sections to scrape: "videos" or "reposts" (default: ["videos"]) |
| `profileSorting` | string | Profile video sorting: "latest", "popular", or "oldest" (default: "latest") |
| `oldestPostDateUnified` | string | Scrape videos published after this date (YYYY-MM-DD) or number of days (e.g., "1" for today only) |
| `newestPostDate` | string | Scrape videos published before this date (YYYY-MM-DD) |
| `excludePinnedPosts` | boolean | Exclude pinned posts from profiles (default: false) |
| `searchQueries` | array | Keywords to search for videos and profiles |
| `searchSection` | string | Search sorting: "" (Top), "/video" (Videos only), "/user" (Profiles only) (default: "") |
| `maxProfilesPerQuery` | integer | Number of profiles per query (applies to profile searches) (default: 10) |
| `postURLs` | array | Direct URLs of specific TikTok videos to scrape |
| `shouldDownloadVideos` | boolean | Download TikTok videos (increases time and costs) (default: false) |
| `shouldDownloadCovers` | boolean | Download video thumbnails (increases time and costs) (default: false) |
| `shouldDownloadSubtitles` | boolean | Download video subtitles when present (increases time and costs) (default: false) |
| `shouldDownloadSlideshowImages` | boolean | Download slideshow images (increases time and costs) (default: false) |
| `videoKvStoreIdOrName` | string | Name or ID of Key Value Store for videos and media (optional, uses default if omitted) |

## Output Fields

### Basic Video Information

| Field | Description |
|-------|-------------|
| `id` | Video ID |
| `url` | Direct video URL (same as `webVideoUrl`) |
| `webVideoUrl` | TikTok web video URL |
| `text` | Video description/caption |
| `textLanguage` | Language of video text |
| `createTime` | Unix timestamp of video creation |
| `createTimeISO` | ISO format timestamp |
| `isAd` | Whether the video is an ad |
| `isPinned` | Whether the video is pinned |
| `isSlideshow` | Whether the video is a slideshow |
| `searchQuery` | Search query used (if applicable) |

### Author/Profile Information

| Field | Description |
|-------|-------------|
| `authorMeta` | Object containing author information |
| `authorMeta.id` | Author's user ID |
| `authorMeta.name` | Author's username |
| `authorMeta.nickName` | Author's display name |
| `authorMeta.profileUrl` | Author's profile URL |
| `authorMeta.avatar` | Author's profile picture URL |
| `authorMeta.originalAvatarUrl` | Original avatar URL |
| `authorMeta.verified` | Whether author is verified |
| `authorMeta.signature` | Author's bio/signature |
| `authorMeta.bioLink` | Bio link (if present) |
| `authorMeta.privateAccount` | Whether account is private |
| `authorMeta.following` | Number of accounts following |
| `authorMeta.friends` | Number of friends |
| `authorMeta.fans` | Number of followers |
| `authorMeta.heart` | Total likes received |
| `authorMeta.video` | Number of videos posted |
| `authorMeta.digg` | Number of likes given |
| `authorMeta.followDatasetUrl` | Follow dataset URL (if applicable) |

### Music Information

| Field | Description |
|-------|-------------|
| `musicMeta` | Object containing music information |
| `musicMeta.musicName` | Name of the music track |
| `musicMeta.musicAuthor` | Music author/artist |
| `musicMeta.musicOriginal` | Whether music is original |
| `musicMeta.musicId` | Music track ID |
| `musicMeta.playUrl` | URL to play the music |
| `musicMeta.coverMediumUrl` | Music cover image URL |
| `musicMeta.originalCoverMediumUrl` | Original cover image URL |

### Video Metadata

| Field | Description |
|-------|-------------|
| `videoMeta` | Object containing video metadata |
| `videoMeta.height` | Video height in pixels |
| `videoMeta.width` | Video width in pixels |
| `videoMeta.duration` | Video duration in seconds |
| `videoMeta.coverUrl` | Video cover/thumbnail URL |
| `videoMeta.originalCoverUrl` | Original cover URL |
| `videoMeta.definition` | Video quality definition (e.g., "540p") |
| `videoMeta.format` | Video format (e.g., "mp4") |
| `mediaUrls` | Array of media URLs (for slideshows) |

### Engagement Metrics

| Field | Description |
|-------|-------------|
| `diggCount` | Number of likes |
| `shareCount` | Number of shares |
| `playCount` | Number of plays/views |
| `collectCount` | Number of times collected/saved |
| `commentCount` | Number of comments |

### Content Tags

| Field | Description |
|-------|-------------|
| `hashtags` | Array of hashtag objects (id, name, title, cover) |
| `mentions` | Array of mentioned usernames |
| `detailedMentions` | Array of detailed mention objects |
| `effectStickers` | Array of effect stickers used |

## Essential Fields

For quick answers and basic data exports, these fields are most relevant (in priority order):

| Priority | Field | Description |
|----------|-------|-------------|
| 1 | `webVideoUrl` | Video URL |
| 2 | `authorMeta.name` | Username |
| 3 | `authorMeta.nickName` | Display name |
| 4 | `text` | Video caption |
| 5 | `playCount` | Views |
| 6 | `diggCount` | Likes |
| 7 | `authorMeta.fans` | Followers |
