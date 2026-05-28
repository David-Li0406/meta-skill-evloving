# Google Ads Playbook

> Detailed guide for Google Ads operations via the Google Ads API.

## Overview

Google Ads uses a hierarchical structure:
```
Account (Customer ID)
└── Campaign (budget, bidding strategy, objective)
    └── Ad Group (targeting, default bids)
        └── Ad (creative content)
        └── Keywords (search targeting)
```

## Authentication Setup

### Required Credentials

1. **Developer Token** - From Google Ads API Center
2. **OAuth 2.0 Client ID** - From Google Cloud Console
3. **Refresh Token** - Generated via OAuth flow
4. **Customer ID** - Your Google Ads account ID (or Manager account)

### Setup Steps

1. **Create Google Cloud Project:**
   ```
   1. Go to https://console.cloud.google.com
   2. Create new project or select existing
   3. Enable "Google Ads API"
   ```

2. **Create OAuth Credentials:**
   ```
   1. Go to APIs & Services > Credentials
   2. Create OAuth 2.0 Client ID (Desktop app)
   3. Download client_secret.json
   ```

3. **Get Developer Token:**
   ```
   1. Sign into Google Ads
   2. Go to Tools & Settings > API Center
   3. Apply for Developer Token (test token is instant)
   ```

4. **Generate Refresh Token:**
   ```bash
   # Use the Google Ads auth helper
   python -c "from google_ads_auth import get_refresh_token; get_refresh_token()"
   # Follow browser prompts to authorize
   ```

5. **Configure Environment:**
   ```bash
   # .env file
   GOOGLE_ADS_DEVELOPER_TOKEN=your_developer_token
   GOOGLE_ADS_CLIENT_ID=your_client_id.apps.googleusercontent.com
   GOOGLE_ADS_CLIENT_SECRET=your_client_secret
   GOOGLE_ADS_REFRESH_TOKEN=your_refresh_token
   GOOGLE_ADS_LOGIN_CUSTOMER_ID=1234567890  # Manager account (no dashes)
   ```

---

## Campaign Types

| Type | Use For | API Value |
|------|---------|-----------|
| Search | Text ads on Google Search | `SEARCH` |
| Display | Banner ads on websites | `DISPLAY` |
| Shopping | Product listing ads | `SHOPPING` |
| Video | YouTube ads | `VIDEO` |
| Performance Max | AI-optimized across channels | `PERFORMANCE_MAX` |
| Demand Gen | Discovery + YouTube | `DEMAND_GEN` |

## Bidding Strategies

| Strategy | Objective | API Value |
|----------|-----------|-----------|
| Maximize Clicks | Traffic | `MAXIMIZE_CLICKS` |
| Maximize Conversions | Leads/Sales | `MAXIMIZE_CONVERSIONS` |
| Target CPA | Cost per acquisition | `TARGET_CPA` |
| Target ROAS | Return on ad spend | `TARGET_ROAS` |
| Manual CPC | Full control | `MANUAL_CPC` |

---

## Common Operations

### List Campaigns

```bash
python google_ads.py campaigns --customer-id 1234567890
```

**GAQL Query:**
```sql
SELECT
  campaign.id,
  campaign.name,
  campaign.status,
  campaign.advertising_channel_type,
  campaign_budget.amount_micros
FROM campaign
ORDER BY campaign.name
```

### Get Campaign Performance

```bash
python google_ads.py performance --customer-id 1234567890 --days 30
```

**GAQL Query:**
```sql
SELECT
  campaign.id,
  campaign.name,
  metrics.impressions,
  metrics.clicks,
  metrics.ctr,
  metrics.average_cpc,
  metrics.cost_micros,
  metrics.conversions,
  metrics.cost_per_conversion
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
```

### Create Campaign (DRAFT)

⚠️ **Safety:** All campaigns created via API are set to PAUSED status.

```bash
python google_ads.py create \
  --customer-id 1234567890 \
  --name "My New Campaign" \
  --type SEARCH \
  --budget 50.00 \
  --bidding MAXIMIZE_CLICKS
```

**Required Fields:**
- `name` - Campaign name
- `advertising_channel_type` - Campaign type
- `campaign_budget` - Daily budget in account currency
- `bidding_strategy_type` - How to optimize
- `status` - Always set to `PAUSED`

### Update Campaign

```bash
python google_ads.py update \
  --customer-id 1234567890 \
  --campaign-id 123456 \
  --budget 75.00
```

### Pause/Enable Campaign

```bash
# Pause
python google_ads.py update \
  --customer-id 1234567890 \
  --campaign-id 123456 \
  --status PAUSED

# Enable (requires confirmation)
python google_ads.py update \
  --customer-id 1234567890 \
  --campaign-id 123456 \
  --status ENABLED \
  --confirm
```

---

## GAQL Reference

### Query Structure

```sql
SELECT
  [fields]
FROM [resource]
WHERE [conditions]
ORDER BY [field] [ASC|DESC]
LIMIT [number]
```

### Common Resources

| Resource | Description |
|----------|-------------|
| `campaign` | Campaign-level data |
| `ad_group` | Ad group data |
| `ad_group_ad` | Ad data |
| `keyword_view` | Keyword performance |
| `geographic_view` | Geo performance |
| `device_view` | Device breakdown |

### Common Metrics

| Metric | Description |
|--------|-------------|
| `metrics.impressions` | Times ad shown |
| `metrics.clicks` | Number of clicks |
| `metrics.ctr` | Click-through rate |
| `metrics.cost_micros` | Spend in micros (divide by 1,000,000) |
| `metrics.conversions` | Conversion count |
| `metrics.average_cpc` | Avg cost per click |
| `metrics.cost_per_conversion` | CPA |

### Common Segments

| Segment | Description |
|---------|-------------|
| `segments.date` | Daily breakdown |
| `segments.device` | By device type |
| `segments.ad_network_type` | Search vs Display |
| `segments.conversion_action` | By conversion type |

### Date Filters

```sql
-- Predefined ranges
WHERE segments.date DURING LAST_7_DAYS
WHERE segments.date DURING LAST_30_DAYS
WHERE segments.date DURING THIS_MONTH
WHERE segments.date DURING LAST_MONTH

-- Custom range
WHERE segments.date BETWEEN '2024-01-01' AND '2024-01-31'
```

---

## Campaign Creation Template

### Search Campaign

```python
campaign_config = {
    "name": "Search - Brand Terms",
    "advertising_channel_type": "SEARCH",
    "status": "PAUSED",  # Always PAUSED
    "campaign_budget": {
        "amount_micros": 50_000_000,  # $50/day
        "delivery_method": "STANDARD"
    },
    "bidding_strategy_type": "MAXIMIZE_CLICKS",
    "network_settings": {
        "target_google_search": True,
        "target_search_network": True,
        "target_content_network": False
    },
    "geo_target_type_setting": {
        "positive_geo_target_type": "PRESENCE_OR_INTEREST",
        "negative_geo_target_type": "PRESENCE_OR_INTEREST"
    }
}
```

### Display Campaign

```python
campaign_config = {
    "name": "Display - Remarketing",
    "advertising_channel_type": "DISPLAY",
    "status": "PAUSED",
    "campaign_budget": {
        "amount_micros": 30_000_000,  # $30/day
        "delivery_method": "STANDARD"
    },
    "bidding_strategy_type": "TARGET_CPA",
    "target_cpa_micros": 25_000_000,  # $25 target CPA
}
```

---

## Ad Group Creation

```python
ad_group_config = {
    "name": "Ad Group - Core Keywords",
    "campaign": "customers/{customer_id}/campaigns/{campaign_id}",
    "status": "PAUSED",
    "type": "SEARCH_STANDARD",
    "cpc_bid_micros": 2_000_000  # $2.00 max CPC
}
```

---

## Responsive Search Ad Creation

```python
ad_config = {
    "ad_group": "customers/{customer_id}/adGroups/{ad_group_id}",
    "status": "PAUSED",
    "ad": {
        "responsive_search_ad": {
            "headlines": [
                {"text": "Headline 1", "pinned_field": "HEADLINE_1"},
                {"text": "Headline 2"},
                {"text": "Headline 3"},
                # ... up to 15 headlines
            ],
            "descriptions": [
                {"text": "Description 1"},
                {"text": "Description 2"},
                # ... up to 4 descriptions
            ],
            "path1": "path1",
            "path2": "path2"
        },
        "final_urls": ["https://example.com/landing-page"]
    }
}
```

---

## Keyword Addition

```python
keyword_config = {
    "ad_group": "customers/{customer_id}/adGroups/{ad_group_id}",
    "status": "ENABLED",
    "keyword": {
        "text": "buy widgets online",
        "match_type": "PHRASE"  # EXACT, PHRASE, BROAD
    },
    "cpc_bid_micros": 1_500_000  # $1.50 bid
}
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| `CUSTOMER_NOT_FOUND` | Wrong customer ID | Use correct 10-digit ID (no dashes) |
| `OAUTH_TOKEN_INVALID` | Expired token | Regenerate refresh token |
| `DEVELOPER_TOKEN_NOT_APPROVED` | Test token limitations | Apply for production access |
| `MUTATE_ERROR` | Invalid field value | Check API documentation |
| `QUOTA_ERROR` | Rate limited | Implement backoff, wait |

### Test Mode Limitations

With a test developer token:
- Can only access accounts you own
- Some features restricted
- Apply for Standard/Basic access for production

---

## Best Practices

1. **Always Start Paused:** Never create campaigns in ENABLED state
2. **Use Descriptive Names:** Include date, objective in campaign names
3. **Set Budget Limits:** Configure max budget in `ads_config.yaml`
4. **Test Queries First:** Run SELECT before UPDATE/DELETE
5. **Log All Changes:** Keep audit trail of modifications
6. **Use Micros:** Remember amounts are in micros (1 USD = 1,000,000 micros)
