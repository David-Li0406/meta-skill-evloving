# Contact Details Scraper

**Actor ID:** `vdrmota/contact-info-scraper`

Extract emails, phone numbers, and social media profiles from websites.

## Key Input Parameters

```json
{
  "startUrls": [{"url": "https://apify.com"}],
  "maxRequestsPerStartUrl": 20,
  "mergeContacts": true,
  "maxDepth": 2,
  "sameDomain": true,
  "proxyConfig": {"useApifyProxy": true}
}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `startUrls` | array | URLs to scrape (required) |
| `maxRequestsPerStartUrl` | integer | Max pages per URL (default: 20) |
| `mergeContacts` | boolean | Merge all contacts from same start URL into single row (default: true) |
| `maxDepth` | integer | Maximum link depth to follow from start URL (default: 2) |
| `maxRequests` | integer | Maximum pages for whole scrape (default: 9999999) |
| `sameDomain` | boolean | Stay within same domain (default: true) |
| `considerChildFrames` | boolean | Extract contact info from iframes (default: true) |
| `useBrowser` | boolean | Use browser for scraping (default: false) |
| `waitUntil` | string | Page load timing: "commit", "domcontentloaded", "load", "networkidle" (default: "domcontentloaded") |
| `proxyConfig` | object | Proxy configuration (required) |
| `maximumLeadsEnrichmentRecords` | integer | Max business leads per domain (default: 0) |
| `leadsEnrichmentDepartments` | array | Filter leads by department: "c_suite", "product", "engineering_technical", "design", "education", "finance", "human_resources", "information_technology", "legal", "marketing", "medical_health", "operations", "sales", "consulting" |
| `scrapeSocialMediaProfiles` | object | Enable detailed social media profile scraping |
| `scrapeSocialMediaProfiles.facebooks` | boolean | Enable Facebook profile scraping |
| `scrapeSocialMediaProfiles.instagrams` | boolean | Enable Instagram profile scraping |
| `scrapeSocialMediaProfiles.youtubes` | boolean | Enable YouTube channel scraping |
| `scrapeSocialMediaProfiles.tiktoks` | boolean | Enable TikTok profile scraping |
| `scrapeSocialMediaProfiles.twitters` | boolean | Enable X (Twitter) profile scraping |

## Output Fields

### Basic Contact Information

| Field | Description |
|-------|-------------|
| `originalStartUrl` | Original URL provided |
| `domain` | Website domain |
| `scrapedUrls` | Array of all pages scraped |
| `emails` | Email addresses found |
| `phones` | Phone numbers found |
| `phonesUncertain` | Uncertain phone numbers |

### Social Media URLs (Basic)

| Field | Description |
|-------|-------------|
| `linkedIns` | LinkedIn profile URLs |
| `twitters` | Twitter/X profile URLs |
| `instagrams` | Instagram profile URLs |
| `facebooks` | Facebook page/profile URLs |
| `youtubes` | YouTube channel URLs |
| `tiktoks` | TikTok profile URLs |
| `pinterests` | Pinterest profile URLs |
| `discords` | Discord server URLs |
| `snapchats` | Snapchat profile URLs |
| `threads` | Threads profile URLs |
| `telegrams` | Telegram profile/group URLs |
| `reddits` | Reddit page URLs |
| `whatsapps` | WhatsApp information |

### Enriched Social Media Profiles (Add-on)

Available when `scrapeSocialMediaProfiles` is enabled:

| Field | Description |
|-------|-------------|
| `facebookProfiles` | Array of enriched Facebook profile objects with follower counts, profile pictures, and more |
| `instagramProfiles` | Array of enriched Instagram profile objects with follower counts, profile pictures, and more |
| `youtubeProfiles` | Array of enriched YouTube channel objects with subscriber count, description, total videos, total views, verification status |
| `tiktokProfiles` | Array of enriched TikTok profile objects with follower counts, video count, profile pictures, and more |
| `twitterProfiles` | Array of enriched Twitter/X profile objects |

### Business Leads (Add-on)

| Field | Description |
|-------|-------------|
| `leadsEnrichment` | Array of enriched business leads with full name, email, job title, department, seniority, LinkedIn, company information |

## Essential Fields

For quick answers and basic data exports, these fields are most relevant (in priority order):

| Priority | Field | Description |
|----------|-------|-------------|
| 1 | `domain` | Website domain |
| 2 | `emails` | Email addresses |
| 3 | `phones` | Phone numbers |
| 4 | `linkedIns` | LinkedIn URLs |
| 5 | `facebooks` | Facebook URLs |
| 6 | `instagrams` | Instagram URLs |
| 7 | `twitters` | Twitter URLs |
