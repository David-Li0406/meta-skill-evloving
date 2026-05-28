# Instagram Search Scraper

**Actor ID:** `apify/instagram-search-scraper`

Scrape Instagram search results for places, businesses, locations, users, and hashtags. Extract contact details, categories, metrics, recent posts, and hashtag popularity.

## Key Input Parameters

```json
{
  "search": "restaurant prague",
  "searchType": "place",
  "searchLimit": 10,
  "enhanceUserSearchWithFacebookPage": false
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string | Keyword(s) to search for. Can be comma-separated for multiple searches (required) |
| `searchType` | string | Type of search: "place", "user", or "hashtag" (required) |
| `searchLimit` | integer | Maximum number of results per search term |
| `enhanceUserSearchWithFacebookPage` | boolean | For user searches (top 10), extract Facebook page and email if available (higher credit usage) |

## Output Fields

### Place Search Results

#### Basic Place Information

| Field | Description |
|-------|-------------|
| `searchTerm` | Original search keyword |
| `searchSource` | Source of the search (google, facebook-ads, threads) |
| `inputUrl` | Instagram location URL |
| `name` | Place name |
| `category` | Business category (e.g., "Bakery", "Restaurant") |
| `phone` | Phone number |
| `price_range` | Price range indicator (0-4) |
| `slug` | URL slug |
| `location_id` | Instagram location ID |

#### Location Details

| Field | Description |
|-------|-------------|
| `lat` | Latitude coordinate |
| `lng` | Longitude coordinate |
| `location_address` | Street address |
| `location_city` | City name |
| `location_zip` | ZIP code |

#### Place Metrics

| Field | Description |
|-------|-------------|
| `media_count` | Number of posts tagged at this location |
| `ig_business` | Instagram business profile information object |
| `ig_business.profile.username` | Business Instagram username |
| `ig_business.profile.id` | Business Instagram ID |
| `ig_business.profile.profile_pic_url` | Business profile picture URL |

#### Opening Hours

| Field | Description |
|-------|-------------|
| `hours` | Opening hours information object |
| `hours.status` | Current status (e.g., "Open until 4:00 PM", "Closed") |

### Profile/User Search Results

#### Basic Account Information

| Field | Description |
|-------|-------------|
| `searchTerm` | Original search keyword |
| `searchSource` | Source of the search |
| `inputUrl` | Facebook API URL or Instagram profile URL |
| `id` | Instagram user ID |
| `username` | Instagram username |
| `url` | Instagram profile URL |
| `fullName` | Full display name |
| `biography` | Profile bio text |
| `externalUrl` | Main external URL from bio |
| `externalUrlShimmed` | Instagram-wrapped external URL |
| `externalUrls` | Array of external URL objects with title, url, lynx_url, link_type |

#### Profile Metrics

| Field | Description |
|-------|-------------|
| `followersCount` | Number of followers |
| `followsCount` | Number of accounts followed |
| `postsCount` | Total number of posts |
| `hasChannel` | Has Instagram channel (boolean) |
| `highlightReelCount` | Number of highlight reels |
| `private` | Is private account (boolean) |
| `verified` | Is verified account (boolean) |

#### Business Account Information

| Field | Description |
|-------|-------------|
| `isBusinessAccount` | Is business account (boolean) |
| `joinedRecently` | Recently joined Instagram (boolean) |
| `businessCategoryName` | Business category/categories |
| `facebookPage` | Facebook page information object |
| `facebookPage.page_id` | Facebook page ID |
| `facebookPage.name` | Facebook page name |
| `facebookPage.category` | Facebook page category |
| `facebookPage.ig_username` | Instagram username |
| `facebookPage.ig_followers` | Instagram follower count |
| `facebookPage.verification` | Verification status |

#### Profile Images

| Field | Description |
|-------|-------------|
| `profilePicUrl` | Profile picture URL (150x150) |
| `profilePicUrlHD` | HD profile picture URL (320x320) |

#### Latest Posts

| Field | Description |
|-------|-------------|
| `latestPosts` | Array of latest post objects (up to 12 posts) |
| `latestIgtvVideos` | Array of latest IGTV video objects |

Latest post object fields:

| Field | Description |
|-------|-------------|
| `id` | Post ID |
| `type` | Post type (Image, Video, Sidecar) |
| `shortCode` | Post shortcode |
| `url` | Post URL |
| `caption` | Post caption text |
| `hashtags` | Array of hashtags used |
| `mentions` | Array of mentioned accounts |
| `timestamp` | Post timestamp (ISO format) |
| `likesCount` | Number of likes |
| `commentsCount` | Number of comments |
| `videoViewCount` | Video view count (if video) |
| `displayUrl` | Image/thumbnail URL |
| `dimensionsHeight` | Image height |
| `dimensionsWidth` | Image width |
| `locationName` | Tagged location name |
| `locationId` | Tagged location ID |

### Hashtag Search Results

#### Basic Hashtag Information

| Field | Description |
|-------|-------------|
| `searchTerm` | Original search keyword |
| `searchSource` | Source of the search |
| `name` | Hashtag name |
| `id` | Hashtag ID |
| `url` | Instagram hashtag URL |
| `postsCount` | Number of posts using this hashtag |
| `posts` | Formatted post count (e.g., "70.35 K") |
| `postsPerDay` | Posts per day metric |
| `difficulty` | Hashtag difficulty score |

#### Related Hashtags

| Field | Description |
|-------|-------------|
| `related` | Array of related hashtag objects (hash, info) |
| `frequent` | Array of frequently used hashtag objects |
| `average` | Array of average usage hashtag objects |
| `rare` | Array of rarely used hashtag objects |
| `relatedFrequent` | Array of related frequent hashtag objects |
| `relatedAverage` | Array of related average hashtag objects |
| `relatedRare` | Array of related rare hashtag objects |

Related hashtag object fields:

| Field | Description |
|-------|-------------|
| `hash` | Hashtag with # symbol |
| `info` | Usage volume (e.g., "1.49 m", "70.35 k") |

## Essential Fields

For quick answers and basic data exports, these fields are most relevant (in priority order):

### Place Search
| Priority | Field | Description |
|----------|-------|-------------|
| 1 | `name` | Place name |
| 2 | `inputUrl` | Instagram URL |
| 3 | `category` | Business category |
| 4 | `phone` | Phone number |
| 5 | `location_address` | Address |
| 6 | `location_city` | City |
| 7 | `media_count` | Posts at location |

### User Search
| Priority | Field | Description |
|----------|-------|-------------|
| 1 | `username` | Instagram handle |
| 2 | `url` | Profile URL |
| 3 | `fullName` | Display name |
| 4 | `followersCount` | Followers |
| 5 | `biography` | Bio |
| 6 | `externalUrl` | Website |
| 7 | `verified` | Verified status |
