# TikTok Scraper

**Actor ID:** `clockworks/tiktok-scraper`

Extract data from TikTok videos, hashtags, and users. Use URLs or search queries to scrape TikTok profiles, hashtags, posts, URLs, shares, followers, hearts, names, video, and music-related data.

## Key Input Parameters

```json
{
  "hashtags": ["fyp"],
  "resultsPerPage": 100,
  "profiles": ["username"],
  "searchQueries": ["keyword"],
  "postURLs": ["https://www.tiktok.com/@user/video/123"],
  "scrapeRelatedVideos": false,
  "proxyCountryCode": "None"
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `hashtags` | array | TikTok hashtags to scrape (e.g., ["fyp", "tiktok"]) |
| `resultsPerPage` | integer | Number of videos per hashtag, profile, or search (default: 1) |
| `profiles` | array | TikTok usernames to scrape |
| `profileScrapeSections` | array | Profile sections: "videos", "reposts" (default: ["videos"]) |
| `profileSorting` | string | Video sorting: "latest", "popular", "oldest" (default: "latest") |
| `excludePinnedPosts` | boolean | Exclude pinned posts from profiles (default: false) |
| `searchQueries` | array | Keywords for search (applies to videos and profiles) |
| `searchSection` | string | Search filter: "" (Top), "/video" (Videos), "/user" (Profiles) |
| `maxProfilesPerQuery` | integer | Number of profiles per search query (default: 10) |
| `postURLs` | array | Direct URLs of TikTok videos to scrape |
| `scrapeRelatedVideos` | boolean | Scrape related videos for post URLs (default: false) |
| `proxyCountryCode` | string | Country code for proxy (default: "None") |

### Date Filters (Charged Add-on)

| Parameter | Type | Description |
|-----------|------|-------------|
| `oldestPostDateUnified` | string | Scrape videos published after date (YYYY-MM-DD or days, e.g., "1" for today) |
| `newestPostDate` | string | Scrape videos published before date (YYYY-MM-DD) |

### Popularity Filters (Charged Add-on)

| Parameter | Type | Description |
|-----------|------|-------------|
| `mostDiggs` | integer | Scrape videos with hearts < [number] |
| `leastDiggs` | integer | Scrape videos with hearts ≥ [number] |

### Search Filters (Charged Add-on)

| Parameter | Type | Description |
|-----------|------|-------------|
| `searchSorting` | string | Sort search results: "0" (Top), "1" (Relevant), "3" (Recent) |
| `searchDatePosted` | string | Date range filter: "0" (All time), "1" (Past 24h), "2" (Past week), "3" (Past month), "4" (Past 3 months), "5" (Past year) |

### Followers/Following (Charged Add-on)

| Parameter | Type | Description |
|-----------|------|-------------|
| `maxFollowersPerProfile` | integer | Number of followers profiles to scrape |
| `maxFollowingPerProfile` | integer | Number of following profiles to scrape |

### Download Options (Charged Add-on)

| Parameter | Type | Description |
|-----------|------|-------------|
| `shouldDownloadVideos` | boolean | Download TikTok videos (default: false) |
| `shouldDownloadCovers` | boolean | Download video thumbnails (default: false) |
| `shouldDownloadSubtitles` | boolean | Download video subtitles (default: false) |
| `shouldDownloadSlideshowImages` | boolean | Download slideshow images (default: false) |
| `shouldDownloadAvatars` | boolean | Download profile avatars (default: false) |
| `shouldDownloadMusicCovers` | boolean | Download sound cover images (default: false) |
| `videoKvStoreIdOrName` | string | Key-Value Store name for storing videos |

### Comments

| Parameter | Type | Description |
|-----------|------|-------------|
| `commentsPerPost` | integer | Maximum comments per post to scrape |
| `maxRepliesPerComment` | integer | Maximum replies per comment (default: 0) |

## Output Fields

### Basic Video Information

| Field | Description |
|-------|-------------|
| `id` | Video ID |
| `text` | Video description |
| `textLanguage` | Text language code |
| `createTime` | Timestamp (Unix) |
| `createTimeISO` | Timestamp (ISO format) |
| `locationCreated` | Country code where video was created |
| `webVideoUrl` | Direct TikTok video URL |
| `isAd` | Whether video is an ad |
| `isPinned` | Whether video is pinned |
| `isSponsored` | Whether video is sponsored |
| `isSlideshow` | Whether post is a slideshow |

### Author Information

| Field | Description |
|-------|-------------|
| `authorMeta` | Object with author details |
| `authorMeta.id` | Author ID |
| `authorMeta.name` | Author username |
| `authorMeta.profileUrl` | Author profile URL |
| `authorMeta.nickName` | Author display name |
| `authorMeta.verified` | Verification status |
| `authorMeta.signature` | Author bio |
| `authorMeta.bioLink` | Bio link URL |
| `authorMeta.avatar` | Profile picture URL |
| `authorMeta.originalAvatarUrl` | Original profile picture URL |
| `authorMeta.privateAccount` | Whether account is private |
| `authorMeta.following` | Following count |
| `authorMeta.friends` | Friends count |
| `authorMeta.fans` | Followers count |
| `authorMeta.heart` | Total hearts received |
| `authorMeta.video` | Total videos posted |
| `authorMeta.digg` | Total likes given |

### Engagement Metrics

| Field | Description |
|-------|-------------|
| `diggCount` | Number of likes (hearts) |
| `shareCount` | Number of shares |
| `playCount` | Number of plays |
| `collectCount` | Number of bookmarks |
| `commentCount` | Number of comments |

### Video Metadata

| Field | Description |
|-------|-------------|
| `videoMeta` | Object with video details |
| `videoMeta.height` | Video height in pixels |
| `videoMeta.width` | Video width in pixels |
| `videoMeta.duration` | Video duration in seconds |
| `videoMeta.coverUrl` | Video cover/thumbnail URL |
| `videoMeta.originalCoverUrl` | Original cover URL |
| `videoMeta.definition` | Video quality (e.g., "540p") |
| `videoMeta.format` | Video format (e.g., "mp4") |
| `videoMeta.subtitleLinks` | Array of subtitle objects |

### Music Information

| Field | Description |
|-------|-------------|
| `musicMeta` | Object with music details |
| `musicMeta.musicName` | Music track name |
| `musicMeta.musicAuthor` | Music author name |
| `musicMeta.musicOriginal` | Whether music is original |
| `musicMeta.playUrl` | Music track URL |
| `musicMeta.coverMediumUrl` | Music cover image URL |
| `musicMeta.originalCoverMediumUrl` | Original music cover URL |
| `musicMeta.musicId` | Music ID |

### Content Details

| Field | Description |
|-------|-------------|
| `hashtags` | Array of hashtag objects (id, name, title, cover) |
| `mentions` | Array of mentioned users |
| `detailedMentions` | Array of detailed mention objects |
| `effectStickers` | Array of effect/filter objects used |
| `slideshowImageLinks` | Array of slideshow image URLs (if applicable) |

### Search Results (When Using searchQueries)

| Field | Description |
|-------|-------------|
| `searchQuery` | The search query that returned this result |

### Profile Scraping (When Using profiles)

| Field | Description |
|-------|-------------|
| `input` | The profile username input |
| `fromProfileSection` | Section scraped: "videos" or "reposts" |

### Video URLs (When Using postURLs)

| Field | Description |
|-------|-------------|
| `submittedVideoUrl` | The original submitted video URL |

### Followers/Following (When Using Add-on)

| Field | Description |
|-------|-------------|
| `connectedTo` | Object with the profile this connection relates to |
| `connectionType` | Type: "follower" or "following" |
| `connectionDescription` | Human-readable connection description |

### Comments (When Scraping Comments)

Comments are stored in a separate dataset referenced by `commentsDatasetURL` field in the output.

### Downloaded Media (When Using Download Options)

Downloaded videos and media are stored in a Key-Value Store, accessible via the storage tab.

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
| 7 | `commentCount` | Comments |
| 8 | `authorMeta.fans` | Follower count |
