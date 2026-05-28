# Ads Agent

> AI-powered management of paid advertising campaigns across Google Ads, LinkedIn Ads, and Meta Ads.

## ⚠️ Safety First

This agent implements strict safety rails:

1. **Draft Mode Only**: All new campaigns are created in PAUSED/DRAFT status - never automatically activated
2. **Budget Limits**: Default budget is $0. Configure limits in `ads_config.yaml`
3. **Confirmation Required**: Destructive actions (activate, delete, increase budget) require explicit confirmation
4. **Test Your Own Account**: Designed for testing on personal accounts first

---

## Quick Start

### 1. Install Dependencies

```bash
cd /path/to/cmo-agent

# Google Ads
pip install google-ads python-dotenv pyyaml

# LinkedIn Ads  
pip install httpx python-dotenv pyyaml

# All tools
pip install google-ads httpx python-dotenv pyyaml
```

### 2. Configure Credentials

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your API credentials (see setup guides below).

### 3. Test Connection

```bash
# Check all platforms
python tools/ads_unified.py status

# Test Google Ads
python tools/google_ads.py accounts

# Test LinkedIn Ads
python tools/linkedin_ads.py accounts
```

---

## Platform Setup

### Google Ads Setup

**Required Credentials:**
- Developer Token
- OAuth 2.0 Client ID & Secret
- Refresh Token
- Customer ID (your account or manager account)

**Step-by-Step:**

1. **Get Developer Token:**
   ```
   1. Sign in to Google Ads: https://ads.google.com
   2. Go to Tools & Settings (wrench icon) > Setup > API Center
   3. Apply for Developer Token
   4. Test token is approved instantly (production needs review)
   ```

2. **Create OAuth Credentials:**
   ```
   1. Go to Google Cloud Console: https://console.cloud.google.com
   2. Create a project or select existing
   3. Enable "Google Ads API" in APIs & Services > Library
   4. Go to APIs & Services > Credentials
   5. Create OAuth 2.0 Client ID (Desktop application)
   6. Download the credentials JSON
   ```

3. **Generate Refresh Token:**
   ```bash
   # Option A: Use Google's OAuth Playground
   # https://developers.google.com/oauthplayground
   
   # Option B: Use google-ads library helper
   pip install google-ads
   google-ads-auth-generate-refresh-token
   # Follow prompts and authorize
   ```

4. **Get Customer ID:**
   ```
   1. Sign in to Google Ads
   2. Look at the top right - your Customer ID is displayed (e.g., 123-456-7890)
   3. Remove dashes when adding to .env (e.g., 1234567890)
   ```

5. **Configure .env:**
   ```bash
   GOOGLE_ADS_DEVELOPER_TOKEN=your_developer_token
   GOOGLE_ADS_CLIENT_ID=your_client_id.apps.googleusercontent.com
   GOOGLE_ADS_CLIENT_SECRET=your_client_secret
   GOOGLE_ADS_REFRESH_TOKEN=your_refresh_token
   GOOGLE_ADS_LOGIN_CUSTOMER_ID=1234567890
   ```

**Verify Setup:**
```bash
python tools/google_ads.py accounts
```

---

### LinkedIn Ads Setup

**Required Credentials:**
- Client ID & Secret (from LinkedIn Developer App)
- Access Token (via OAuth flow)
- Ad Account ID

**Step-by-Step:**

1. **Create LinkedIn Developer App:**
   ```
   1. Go to: https://www.linkedin.com/developers/apps
   2. Click "Create app"
   3. Fill in:
      - App name: "CMO Agent" (or your choice)
      - LinkedIn Page: Select your company page
      - App logo: Upload any image
   4. Accept terms and create
   ```

2. **Add Marketing API Product:**
   ```
   1. In your app, go to "Products" tab
   2. Find "Marketing Developer Platform"
   3. Click "Request access"
   4. Fill out the access form with your use case
   5. Wait for approval (can take 1-5 business days)
   ```

3. **Configure OAuth Settings:**
   ```
   1. Go to "Auth" tab in your app
   2. Under "OAuth 2.0 scopes", ensure you have:
      - r_ads (read ads)
      - rw_ads (read/write ads)
      - r_ads_reporting (analytics)
   3. Add Redirect URL: http://localhost:8080/callback
   4. Note your Client ID and Client Secret
   ```

4. **Generate Access Token:**
   ```bash
   # Simple method - use LinkedIn's Token Generator
   1. Go to your app's "Auth" tab
   2. Scroll to "OAuth 2.0 tools"
   3. Click "Generate token"
   4. Select required scopes
   5. Authorize and copy the token
   
   # Note: Token expires in 60 days - set a reminder to refresh
   ```

5. **Find Ad Account ID:**
   ```
   1. Go to LinkedIn Campaign Manager: https://www.linkedin.com/campaignmanager
   2. Your Account ID is in the URL: /accounts/{ACCOUNT_ID}/
   3. Or run: python tools/linkedin_ads.py accounts
   ```

6. **Configure .env:**
   ```bash
   LINKEDIN_CLIENT_ID=your_client_id
   LINKEDIN_CLIENT_SECRET=your_client_secret
   LINKEDIN_ACCESS_TOKEN=your_access_token
   LINKEDIN_AD_ACCOUNT_ID=123456789
   ```

**Verify Setup:**
```bash
python tools/linkedin_ads.py accounts
```

---

## Usage

### Google Ads

```bash
# List accounts
python tools/google_ads.py accounts

# List campaigns
python tools/google_ads.py campaigns --customer-id 1234567890

# Get performance (last 30 days)
python tools/google_ads.py performance --customer-id 1234567890 --days 30

# Run GAQL query
python tools/google_ads.py query --customer-id 1234567890 \
  --gaql "SELECT campaign.name, metrics.clicks FROM campaign"

# Create campaign (DRAFT mode)
python tools/google_ads.py create \
  --customer-id 1234567890 \
  --name "Test Campaign" \
  --type SEARCH \
  --budget 0 \
  --confirm

# Update campaign status
python tools/google_ads.py update \
  --customer-id 1234567890 \
  --campaign-id 123456 \
  --status PAUSED
```

### LinkedIn Ads

```bash
# List ad accounts
python tools/linkedin_ads.py accounts

# List campaigns
python tools/linkedin_ads.py campaigns --account-id 123456789

# Get campaign analytics
python tools/linkedin_ads.py analytics --campaign-id 123456 --days 30

# Explore targeting options
python tools/linkedin_ads.py targeting --facets
python tools/linkedin_ads.py targeting --search "Marketing" --facet titles

# Create campaign (DRAFT mode)
python tools/linkedin_ads.py create \
  --account-id 123456789 \
  --name "Test LinkedIn Campaign" \
  --objective WEBSITE_VISITS \
  --budget 0 \
  --confirm

# Update campaign
python tools/linkedin_ads.py update \
  --campaign-id 123456 \
  --status PAUSED
```

### Cross-Platform

```bash
# Check credential status
python tools/ads_unified.py status

# Get summary across platforms
python tools/ads_unified.py summary

# Compare performance
python tools/ads_unified.py compare \
  --days 30 \
  --google-customer-id 1234567890

# List all campaigns
python tools/ads_unified.py campaigns \
  --google-customer-id 1234567890
```

---

## Configuration

### Budget Limits (`tools/ads_config.yaml`)

Edit the config file to set budget limits:

```yaml
budgets:
  google_ads:
    max_daily_budget: 50      # Max $50/day per campaign
    max_total_budget: 1000    # Max $1000 lifetime
    max_cpc_bid: 5.00         # Max $5 CPC bid
    
  linkedin_ads:
    max_daily_budget: 100     # Max $100/day per campaign
    max_total_budget: 3000    # Max $3000 lifetime
    max_cpc_bid: 10.00        # Max $10 CPC bid
```

Set to `0` to prevent any spend (default).

### Safety Settings

```yaml
safety:
  force_draft_mode: true      # Always create in PAUSED/DRAFT
  require_confirmation: true  # Confirm destructive actions
```

---

## MCP Server Integration

For Claude Desktop or other MCP-compatible tools, you can use existing MCP servers:

### Google Ads MCP

```bash
# Clone the MCP server
git clone https://github.com/cohnen/mcp-google-ads.git
cd mcp-google-ads

# Setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure (see their README)
```

Add to Claude Desktop config (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "googleAdsServer": {
      "command": "/path/to/mcp-google-ads/.venv/bin/python",
      "args": ["/path/to/mcp-google-ads/google_ads_server.py"],
      "env": {
        "GOOGLE_ADS_DEVELOPER_TOKEN": "your_token",
        "GOOGLE_ADS_LOGIN_CUSTOMER_ID": "1234567890"
      }
    }
  }
}
```

---

## File Structure

```
cmo-agent/
├── agents/
│   └── ads/
│       ├── SKILL.md              # Main orchestrator
│       ├── google-ads.md         # Google Ads playbook
│       ├── linkedin-ads.md       # LinkedIn Ads playbook
│       ├── README.md             # This file
│       └── PLANNING.md           # Architecture plan
│
└── tools/
    ├── google_ads.py             # Google Ads CLI tool
    ├── linkedin_ads.py           # LinkedIn Ads CLI tool
    ├── ads_unified.py            # Cross-platform CLI
    └── ads_config.yaml           # Configuration
```

---

## Troubleshooting

### Google Ads

| Error | Cause | Solution |
|-------|-------|----------|
| `CUSTOMER_NOT_FOUND` | Wrong customer ID | Use 10-digit ID without dashes |
| `OAUTH_TOKEN_INVALID` | Expired refresh token | Regenerate refresh token |
| `DEVELOPER_TOKEN_NOT_APPROVED` | Test token limits | Apply for Standard access |
| `PERMISSION_DENIED` | Account access issue | Check you have access to account |

### LinkedIn Ads

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Token expired | Regenerate access token (60-day expiry) |
| `403 Forbidden` | Missing permissions | Check app has rw_ads scope |
| `AUDIENCE_TOO_SMALL` | < 300 members | Broaden targeting |

### General

1. **Check credentials:** `python tools/ads_unified.py status`
2. **Verify .env file:** Ensure no extra spaces or quotes
3. **Check API access:** Log into each platform's UI to verify account access
4. **Review logs:** Check `logs/ads_agent.log` if enabled

---

## Support

- **Google Ads API Docs:** https://developers.google.com/google-ads/api/docs/start
- **LinkedIn Marketing API:** https://learn.microsoft.com/en-us/linkedin/marketing/
- **MCP Server (Google):** https://github.com/cohnen/mcp-google-ads

---

## Roadmap

- [x] Google Ads (read/write)
- [x] LinkedIn Ads (read/write)
- [ ] Meta Ads (Facebook/Instagram)
- [ ] Cross-platform reporting dashboard
- [ ] Automated optimization rules
- [ ] A/B test management
