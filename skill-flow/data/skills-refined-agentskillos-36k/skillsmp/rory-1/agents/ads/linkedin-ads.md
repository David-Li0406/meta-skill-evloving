# LinkedIn Ads Playbook

> Detailed guide for LinkedIn Ads operations via the LinkedIn Marketing API.

## Overview

LinkedIn Ads uses this hierarchy:
```
Ad Account
└── Campaign Group (optional - for budget/schedule grouping)
    └── Campaign (objective, targeting, budget)
        └── Creative (ad content)
```

## Authentication Setup

### Required Credentials

1. **Client ID** - From LinkedIn Developer Portal
2. **Client Secret** - From LinkedIn Developer Portal
3. **Access Token** - Generated via OAuth 2.0 flow
4. **Ad Account ID** - Your LinkedIn Ads account ID

### Setup Steps

1. **Create LinkedIn App:**
   ```
   1. Go to https://www.linkedin.com/developers/apps
   2. Click "Create app"
   3. Fill in app details
   4. Add "Marketing Developer Platform" product
   5. Complete access request form
   ```

2. **Configure OAuth:**
   ```
   1. In app settings, go to "Auth" tab
   2. Add redirect URL: http://localhost:8080/callback
   3. Note Client ID and Client Secret
   4. Request these scopes:
      - r_ads (read ads)
      - rw_ads (read/write ads)
      - r_ads_reporting (analytics)
   ```

3. **Generate Access Token:**
   ```bash
   # Use the LinkedIn auth helper
   python linkedin_ads_auth.py
   # Follow browser prompts to authorize
   # Token is valid for 60 days
   ```

4. **Find Ad Account ID:**
   ```bash
   # List your ad accounts
   python linkedin_ads.py accounts
   ```

5. **Configure Environment:**
   ```bash
   # .env file
   LINKEDIN_CLIENT_ID=your_client_id
   LINKEDIN_CLIENT_SECRET=your_client_secret
   LINKEDIN_ACCESS_TOKEN=your_access_token
   LINKEDIN_AD_ACCOUNT_ID=123456789
   ```

---

## Campaign Types

| Type | API Value | Use For |
|------|-----------|---------|
| Sponsored Content | `TEXT_AD` | Feed posts |
| Message Ads | `SPONSORED_INMAILS` | Direct messages |
| Dynamic Ads | `DYNAMIC` | Personalized ads |
| Text Ads | `TEXT_AD` | Sidebar text ads |

## Campaign Objectives

| Objective | API Value | Optimization |
|-----------|-----------|--------------|
| Brand Awareness | `BRAND_AWARENESS` | Impressions |
| Website Visits | `WEBSITE_VISITS` | Clicks |
| Engagement | `ENGAGEMENT` | Social actions |
| Video Views | `VIDEO_VIEWS` | Views |
| Lead Generation | `LEAD_GENERATION` | Form fills |
| Website Conversions | `WEBSITE_CONVERSIONS` | Conversions |
| Job Applicants | `JOB_APPLICANTS` | Applications |

---

## Targeting Options

LinkedIn's B2B targeting is its key differentiator:

### Professional Targeting

| Facet | Description | Example |
|-------|-------------|---------|
| `titles` | Job titles | "VP of Marketing" |
| `titlesSeniority` | Seniority level | "VP", "Director", "Manager" |
| `functions` | Job function | "Marketing", "Sales" |
| `industries` | Company industry | "Computer Software" |
| `companySizes` | Employee count | "51-200", "201-500" |
| `companies` | Specific companies | Company URNs |
| `skills` | Member skills | "Digital Marketing" |
| `degrees` | Education level | "Bachelor's", "Master's" |
| `fieldsOfStudy` | Study field | "Business Administration" |
| `schools` | Universities | School URNs |

### Geographic Targeting

| Facet | Description |
|-------|-------------|
| `locations` | Countries, states, cities |
| `geoURNs` | Geographic URN codes |

### Audience Expansion

| Option | Description |
|--------|-------------|
| `enableAudienceExpansion` | Let LinkedIn find similar audiences |
| `excludedAudienceExpansion` | Expand exclusions |

---

## Common Operations

### List Ad Accounts

```bash
python linkedin_ads.py accounts
```

**API Call:**
```
GET https://api.linkedin.com/rest/adAccounts?q=search
```

### List Campaigns

```bash
python linkedin_ads.py campaigns --account-id 123456789
```

**API Call:**
```
GET https://api.linkedin.com/rest/adCampaigns?q=search&search=(account:(values:List(urn:li:sponsoredAccount:123456789)))
```

### Get Campaign Analytics

```bash
python linkedin_ads.py analytics --campaign-id 123456 --days 30
```

**API Call:**
```
GET https://api.linkedin.com/rest/adAnalytics?q=analytics
  &pivot=CAMPAIGN
  &dateRange=(start:(year:2024,month:1,day:1),end:(year:2024,month:1,day:31))
  &campaigns=List(urn:li:sponsoredCampaign:123456)
  &fields=impressions,clicks,costInLocalCurrency,externalWebsiteConversions
```

### Create Campaign (DRAFT)

⚠️ **Safety:** All campaigns created via API are set to DRAFT status.

```bash
python linkedin_ads.py create \
  --account-id 123456789 \
  --name "LinkedIn - VP Marketing" \
  --objective WEBSITE_VISITS \
  --budget 100.00 \
  --targeting "titles:VP of Marketing,CMO;industries:Computer Software"
```

### Update Campaign

```bash
python linkedin_ads.py update \
  --campaign-id 123456 \
  --budget 150.00
```

### Explore Targeting

```bash
# List available targeting facets
python linkedin_ads.py targeting --facets

# Search for specific targeting values
python linkedin_ads.py targeting --search "Marketing" --facet titles
```

---

## Campaign Creation Template

### Sponsored Content Campaign

```python
campaign_config = {
    "account": "urn:li:sponsoredAccount:123456789",
    "name": "Sponsored Content - Q1 2024",
    "status": "DRAFT",  # Always DRAFT
    "type": "SPONSORED_UPDATES",
    "objectiveType": "WEBSITE_VISITS",
    "costType": "CPC",
    "unitCost": {
        "currencyCode": "USD",
        "amount": "5.00"  # Max CPC bid
    },
    "dailyBudget": {
        "currencyCode": "USD",
        "amount": "100.00"
    },
    "totalBudget": {
        "currencyCode": "USD",
        "amount": "3000.00"
    },
    "runSchedule": {
        "start": 1704067200000,  # Unix timestamp ms
        "end": 1706745600000
    },
    "targetingCriteria": {
        "include": {
            "and": [
                {
                    "or": {
                        "urn:li:adTargetingFacet:titles": [
                            "urn:li:title:123",  # VP of Marketing
                            "urn:li:title:456"   # CMO
                        ]
                    }
                },
                {
                    "or": {
                        "urn:li:adTargetingFacet:industries": [
                            "urn:li:industry:4"  # Computer Software
                        ]
                    }
                },
                {
                    "or": {
                        "urn:li:adTargetingFacet:companySizes": [
                            "urn:li:companySizeRange:(51,200)",
                            "urn:li:companySizeRange:(201,500)"
                        ]
                    }
                }
            ]
        }
    },
    "locale": {
        "country": "US",
        "language": "en"
    }
}
```

### Lead Gen Campaign

```python
campaign_config = {
    "account": "urn:li:sponsoredAccount:123456789",
    "name": "Lead Gen - Whitepaper Download",
    "status": "DRAFT",
    "type": "SPONSORED_UPDATES",
    "objectiveType": "LEAD_GENERATION",
    "optimizationTargetType": "MAX_LEAD",
    "costType": "CPM",
    "dailyBudget": {
        "currencyCode": "USD",
        "amount": "150.00"
    },
    # Lead gen form must be created separately
    "associatedEntity": "urn:li:organization:12345"
}
```

---

## Creative (Ad) Creation

### Single Image Ad

```python
creative_config = {
    "campaign": "urn:li:sponsoredCampaign:123456",
    "status": "DRAFT",
    "type": "SPONSORED_STATUS_UPDATE",
    "variables": {
        "data": {
            "com.linkedin.ads.SponsoredUpdateCreativeVariables": {
                "activity": "urn:li:activity:123456789",  # LinkedIn post URN
                # OR create new content:
                "content": {
                    "contentEntities": [
                        {
                            "entityLocation": "https://example.com/landing",
                            "thumbnails": [
                                {"resolvedUrl": "https://example.com/image.jpg"}
                            ]
                        }
                    ],
                    "title": "Ad Headline Here",
                    "description": "Ad description text"
                },
                "commentary": "Introductory text that appears above the ad"
            }
        }
    }
}
```

---

## Analytics Metrics

### Available Metrics

| Metric | Description |
|--------|-------------|
| `impressions` | Times ad was shown |
| `clicks` | Total clicks |
| `costInLocalCurrency` | Spend in account currency |
| `externalWebsiteConversions` | Website conversions |
| `leadGenerationMailContactInfoShares` | Lead form submits |
| `reactions` | Post reactions |
| `comments` | Post comments |
| `shares` | Post shares |
| `follows` | Page follows |
| `videoViews` | Video views |
| `videoCompletions` | Full video watches |

### Pivot Options

| Pivot | Description |
|-------|-------------|
| `CAMPAIGN` | By campaign |
| `CREATIVE` | By creative/ad |
| `COMPANY` | By company (ABM) |
| `MEMBER_INDUSTRY` | By member industry |
| `MEMBER_SENIORITY` | By seniority level |
| `MEMBER_JOB_FUNCTION` | By job function |

---

## Audience Sizing

Before launching, check audience size:

```bash
python linkedin_ads.py audience-count --targeting "titles:VP Marketing;industries:Software"
```

**API Call:**
```
POST https://api.linkedin.com/rest/adTargetingEstimates
{
  "targetingCriteria": { ... },
  "campaignType": "SPONSORED_UPDATES"
}
```

**Response:**
```json
{
  "totalCount": 45000,
  "activeCount": 38000
}
```

⚠️ **Note:** LinkedIn requires minimum 300 audience members for campaigns to run.

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `UNAUTHORIZED` | Token expired | Regenerate access token (60-day expiry) |
| `FORBIDDEN` | Missing permissions | Check app has rw_ads scope |
| `AUDIENCE_TOO_SMALL` | < 300 members | Broaden targeting criteria |
| `INVALID_URN` | Wrong URN format | Use correct URN syntax |
| `RATE_LIMITED` | Too many requests | Implement backoff |

### URN Format

LinkedIn uses URNs (Uniform Resource Names):
```
urn:li:sponsoredAccount:123456789
urn:li:sponsoredCampaign:123456
urn:li:sponsoredCreative:123456
urn:li:organization:123456
urn:li:title:123
urn:li:industry:4
```

---

## Best Practices

1. **Start with DRAFT:** Never create campaigns in ACTIVE status
2. **Check Audience Size:** Ensure > 300 members before activating
3. **Use Specific Titles:** Job title targeting is most effective
4. **Layer Targeting:** Combine titles + industry + company size
5. **Set Budget Caps:** Use both daily and total budgets
6. **A/B Test Creatives:** Run multiple ad variations
7. **Refresh Tokens:** Access tokens expire in 60 days
8. **Use Campaign Groups:** Organize related campaigns together

---

## API Versioning

LinkedIn Marketing API uses dated versions:

```
Header: LinkedIn-Version: 202401
```

Always specify version to avoid breaking changes. Current stable: `202401`

Check recent changes: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/recent-changes
