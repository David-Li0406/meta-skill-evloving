# TikTok Followers Scraper

**Actor ID:** `clockworks/tiktok-followers-scraper`

Scrape TikTok followers and following profiles from any account. Input a profile name, and get detailed lists of followers and following profiles with complete metadata. Perfect for lead generation, audience analysis, and segmentation.

## Key Input Parameters

```json
{
  "profiles": ["khaby.lame"],
  "maxFollowersPerProfile": 50,
  "maxFollowingPerProfile": 50
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `profiles` | array | TikTok usernames to scrape (required) |
| `maxFollowersPerProfile` | integer | Maximum number of followers per profile (default: 50) |
| `maxFollowingPerProfile` | integer | Maximum number of following profiles per profile (default: 50) |

## Output Fields

### Connection Information

| Field | Description |
|-------|-------------|
| `connectionType` | Type of connection: "follower" or "following" |
| `connectionDescription` | Human-readable description of the connection |

### Author Metadata (Connected Profile)

| Field | Description |
|-------|-------------|
| `authorMeta` | Object containing all metadata about the connected profile |
| `authorMeta.id` | Profile ID |
| `authorMeta.name` | Profile username |
| `authorMeta.profileUrl` | Profile URL (https://www.tiktok.com/@username) |
| `authorMeta.nickName` | Display name |
| `authorMeta.verified` | Verification status (boolean) |
| `authorMeta.signature` | Profile bio/signature |
| `authorMeta.bioLink` | Link in bio |
| `authorMeta.originalAvatarUrl` | Original resolution avatar URL |
| `authorMeta.avatar` | Avatar URL |
| `authorMeta.privateAccount` | Whether account is private (boolean) |
| `authorMeta.ttSeller` | Whether account is a TikTok seller (boolean) |
| `authorMeta.following` | Number of accounts following |
| `authorMeta.friends` | Number of friends |
| `authorMeta.fans` | Number of followers |
| `authorMeta.heart` | Total likes received |
| `authorMeta.video` | Number of videos posted |
| `authorMeta.digg` | Number of likes given |

### Connected To Profile (Original Profile)

| Field | Description |
|-------|-------------|
| `connectedTo` | Object containing metadata about the original profile being scraped |
| `connectedTo.id` | Profile ID |
| `connectedTo.name` | Profile username |
| `connectedTo.profileUrl` | Profile URL |
| `connectedTo.nickName` | Display name |
| `connectedTo.verified` | Verification status (boolean) |
| `connectedTo.signature` | Profile bio/signature |
| `connectedTo.bioLink` | Link in bio |
| `connectedTo.originalAvatarUrl` | Original resolution avatar URL |
| `connectedTo.avatar` | Avatar URL |
| `connectedTo.privateAccount` | Whether account is private (boolean) |
| `connectedTo.ttSeller` | Whether account is a TikTok seller (boolean) |
| `connectedTo.following` | Number of accounts following |
| `connectedTo.friends` | Number of friends |
| `connectedTo.fans` | Number of followers |
| `connectedTo.heart` | Total likes received |
| `connectedTo.video` | Number of videos posted |
| `connectedTo.digg` | Number of likes given |

## Essential Fields

For quick answers and basic data exports, these fields are most relevant (in priority order):

| Priority | Field | Description |
|----------|-------|-------------|
| 1 | `authorMeta.name` | Username |
| 2 | `authorMeta.profileUrl` | Profile URL |
| 3 | `authorMeta.nickName` | Display name |
| 4 | `authorMeta.fans` | Followers |
| 5 | `authorMeta.verified` | Verified status |
| 6 | `authorMeta.bioLink` | Bio link |
| 7 | `connectionType` | Follower/following |
