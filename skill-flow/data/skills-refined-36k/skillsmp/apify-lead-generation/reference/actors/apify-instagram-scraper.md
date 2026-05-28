# Instagram Scraper

**Actor ID:** `apify/instagram-scraper`

Scrape posts from Instagram profiles, hashtags, places, or extract comments from posts. Universal Instagram scraper for comprehensive data collection.

## Key Input Parameters

```json
{
  "directUrls": ["https://www.instagram.com/humansofny/"],
  "resultsType": "posts",
  "resultsLimit": 200
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `directUrls` | array | Instagram URLs to scrape (profiles, posts, hashtags, or places) |
| `resultsType` | string | What to scrape: "posts", "comments", "details", "mentions", "reels", "stories" (default: "posts") |
| `resultsLimit` | integer | Max results per URL (max 50 comments per post for comments type) (default: 200) |
| `onlyPostsNewerThan` | string | Scrape posts from date to present (YYYY-MM-DD, ISO timestamp, or relative like "1 days", "2 months", "3 years") |
| `search` | string | Search query for finding profiles, hashtags, or places |
| `searchType` | string | Search type: "user", "hashtag", "place" (default: "hashtag") |
| `searchLimit` | integer | Number of search results to return (default: 1) |
| `addParentData` | boolean | Add data source metadata to results (default: false) |

## Output Fields

### Posts Output

When `resultsType` is "posts":

#### Basic Post Information

| Field | Description |
|-------|-------------|
| `inputUrl` | Original input URL |
| `url` | Direct post URL |
| `type` | Post type: "Image", "Video", "Sidecar" (carousel) |
| `shortCode` | Instagram post short code |
| `id` | Post ID |
| `caption` | Post caption text |
| `timestamp` | Post timestamp (ISO format) |

#### Post Content

| Field | Description |
|-------|-------------|
| `hashtags` | Array of hashtags used in caption |
| `mentions` | Array of mentioned usernames |
| `alt` | Alt text description |
| `displayUrl` | Main display image URL |
| `images` | Array of image URLs (for carousel posts) |
| `dimensionsHeight` | Image/video height in pixels |
| `dimensionsWidth` | Image/video width in pixels |

#### Engagement Metrics

| Field | Description |
|-------|-------------|
| `likesCount` | Number of likes |
| `commentsCount` | Number of comments |
| `firstComment` | First comment text |
| `latestComments` | Array of recent comments |

#### Author Information

| Field | Description |
|-------|-------------|
| `ownerFullName` | Post author's full name |
| `ownerUsername` | Post author's username |
| `ownerId` | Post author's ID |

#### Child Posts (Carousel)

| Field | Description |
|-------|-------------|
| `childPosts` | Array of child post objects for carousel posts |

### Comments Output

When `resultsType` is "comments":

| Field | Description |
|-------|-------------|
| `id` | Comment ID |
| `postId` | Parent post ID |
| `text` | Comment text |
| `position` | Comment position |
| `timestamp` | Comment timestamp (ISO format) |
| `ownerId` | Commenter's ID |
| `ownerIsVerified` | Commenter's verification status |
| `ownerUsername` | Commenter's username |
| `ownerProfilePicUrl` | Commenter's profile picture URL |

### Profile Details Output

When `resultsType` is "details" for profile URLs:

#### Basic Information

| Field | Description |
|-------|-------------|
| `id` | Profile ID |
| `username` | Instagram handle |
| `fullName` | Display name |
| `biography` | Profile bio |
| `externalUrl` | Website link in bio |
| `externalUrlShimmed` | Shimmed version of external URL |

#### Account Status

| Field | Description |
|-------|-------------|
| `private` | Private account flag |
| `verified` | Verification status |
| `isBusinessAccount` | Business account flag |
| `businessCategoryName` | Business category |
| `joinedRecently` | Recently created account flag |
| `hasChannel` | Channel status flag |

#### Statistics

| Field | Description |
|-------|-------------|
| `followersCount` | Number of followers |
| `followsCount` | Number following |
| `postsCount` | Total posts count |
| `highlightReelCount` | Number of highlight reels |
| `igtvVideoCount` | Number of IGTV videos |

#### Profile Pictures

| Field | Description |
|-------|-------------|
| `profilePicUrl` | Standard resolution profile picture URL (150x150) |
| `profilePicUrlHD` | HD profile picture URL (320x320) |

#### Latest Content

| Field | Description |
|-------|-------------|
| `latestPosts` | Array of recent posts with full details |
| `latestIgtvVideos` | Array of recent IGTV videos with full details |
| `following` | Array of following users (if available) |
| `followedBy` | Array of followers (if available) |

#### Social Connections

| Field | Description |
|-------|-------------|
| `facebookPage` | Connected Facebook page info |

### Hashtag Details Output

When `resultsType` is "details" for hashtag URLs:

| Field | Description |
|-------|-------------|
| `id` | Hashtag ID |
| `name` | Hashtag name |
| `topPostsOnly` | Boolean flag |
| `profilePicUrl` | Hashtag profile picture URL |
| `postsCount` | Total posts using this hashtag |
| `topPosts` | Array of top posts for this hashtag |
| `latestPosts` | Array of latest posts using this hashtag |

### Place Details Output

When `resultsType` is "details" for place URLs:

#### Basic Place Information

| Field | Description |
|-------|-------------|
| `id` | Place ID |
| `name` | Place name |
| `slug` | URL slug |
| `public` | Public visibility flag |
| `lat` | Latitude coordinate |
| `lng` | Longitude coordinate |

#### Location Details

| Field | Description |
|-------|-------------|
| `addressStreetAddress` | Street address |
| `addressZipCode` | ZIP/postal code |
| `addressCityName` | City name |
| `addressRegionName` | Region/state name |
| `addressCountryCode` | Country code (ISO) |
| `addressExactCityMatch` | Boolean flag |
| `addressExactRegionMatch` | Boolean flag |
| `addressExactCountryMatch` | Boolean flag |

#### Place Content

| Field | Description |
|-------|-------------|
| `description` | Place description |
| `website` | Website URL |
| `phone` | Phone number |
| `aliasOnFacebook` | Facebook alias |
| `profilePicUrl` | Place profile picture URL |
| `postsCount` | Total posts from this location |
| `topPosts` | Array of top posts from this location |
| `latestPosts` | Array of latest posts from this location |

### Post Details Output

When `resultsType` is "details" for post URLs:

| Field | Description |
|-------|-------------|
| `type` | Post type: "Image", "Video", "Sidecar" |
| `shortCode` | Post short code |
| `caption` | Post caption |
| `hashtags` | Array of hashtags |
| `mentions` | Array of mentions |
| `url` | Post URL |
| `commentsCount` | Number of comments |
| `latestComments` | Array of recent comment objects with ownerUsername and text |
| `dimensionsHeight` | Height in pixels |
| `dimensionsWidth` | Width in pixels |
| `displayUrl` | Main display URL |
| `id` | Post ID |
| `firstComment` | First comment text |
| `likesCount` | Number of likes |
| `timestamp` | Post timestamp (ISO format) |
| `locationName` | Location name |
| `locationId` | Location ID |
| `locationSlug` | Location URL slug |
| `ownerFullName` | Author's full name |
| `ownerUsername` | Author's username |
| `ownerId` | Author's ID |
| `captionIsEdited` | Caption edited flag |
| `hasRankedComments` | Ranked comments flag |
| `commentsDisabled` | Comments disabled flag |
| `displayResourceUrls` | Array of resource URLs |
| `childPosts` | Array of child posts (for carousels) |
| `isAdvertisement` | Advertisement flag |
| `taggedUsers` | Array of tagged users |
| `likedBy` | Array of users who liked (if available) |

## Essential Fields

For quick answers and basic data exports, these fields are most relevant (in priority order):

| Priority | Field | Description |
|----------|-------|-------------|
| 1 | `url` | Post URL |
| 2 | `ownerUsername` | Author username |
| 3 | `caption` | Post caption |
| 4 | `likesCount` | Number of likes |
| 5 | `commentsCount` | Number of comments |
| 6 | `timestamp` | Post date |
