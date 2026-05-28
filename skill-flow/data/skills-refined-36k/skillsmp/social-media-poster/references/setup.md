# Social Media Poster Setup Guide

Complete setup instructions for LinkedIn and Twitter/X API access.

## Prerequisites

- Python 3.8+
- pip or pip3

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r scripts/requirements.txt

# Create .env file
cp .env.example .env
```

## LinkedIn Setup

### 1. Create LinkedIn Developer App

1. Go to https://www.linkedin.com/developers/apps
2. Click **"Create app"**
3. Fill in required fields:
   - App name: Any name (e.g., "My Poster")
   - LinkedIn Page: Select or create one
   - App logo: Upload any image
4. Click **"Create app"**

### 2. Request API Products

1. Go to your app's **Products** tab
2. Request access to:
   - **Share on LinkedIn** (required for posting)
   - **Sign In with LinkedIn using OpenID Connect** (required for auth)
3. Wait for approval (usually instant, sometimes 1-3 days)

### 3. Configure OAuth

1. Go to **Auth** tab
2. Add to **OAuth 2.0 Authorized Redirect URLs**:
   ```
   http://localhost:8000/callback
   ```
3. Save changes

### 4. Get Credentials

1. In **Auth** tab, copy:
   - **Client ID**
   - **Client Secret**
2. Add to your `.env` file:
   ```
   LINKEDIN_CLIENT_ID=your_client_id
   LINKEDIN_CLIENT_SECRET=your_client_secret
   ```

### 5. Generate Access Token

```bash
source venv/bin/activate
python scripts/get_token.py
```

This opens your browser for authorization, then outputs an access token.
Add it to `.env`:
```
LINKEDIN_ACCESS_TOKEN=your_access_token
```

**Note:** LinkedIn tokens expire in ~60 days. Run `get_token.py` again to refresh.

---

## Twitter/X Setup

### 1. Create Developer Account

1. Go to https://developer.x.com/en/portal/dashboard
2. Sign up for developer access
3. Choose **Free** tier (1,500 tweets/month) or **Basic** ($100/mo for 3,000 tweets)

### 2. Create Project & App

1. Create a new **Project**
2. Create an **App** within the project
3. Note down your app name

### 3. Configure User Authentication

**Critical step - this enables posting!**

1. Go to your App → **Settings**
2. Scroll to **User authentication settings**
3. Click **Set up** or **Edit**
4. Configure:
   - **App permissions**: Select **Read and Write**
   - **Type of App**: Web App, Automated App, or Bot
   - **Callback URI**: `http://localhost`
   - **Website URL**: `http://localhost`
5. **Save**

### 4. Get API Keys

1. Go to **Keys and Tokens** tab
2. Generate/copy these values:

| Key | Location |
|-----|----------|
| API Key | Consumer Keys section |
| API Key Secret | Consumer Keys section |
| Bearer Token | Authentication Tokens section |
| Access Token | Authentication Tokens section |
| Access Token Secret | Authentication Tokens section |

**Important:** After changing permissions to Read+Write, you MUST regenerate the Access Token and Access Token Secret.

### 5. Add to .env

```
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
```

---

## Troubleshooting

### LinkedIn: "Token expired"
Run `python scripts/get_token.py` to generate a new token.

### Twitter: "403 Forbidden"
Your app doesn't have write permissions:
1. Go to App Settings → User authentication settings
2. Enable **OAuth 1.0a**
3. Set permissions to **Read and Write**
4. **Regenerate** Access Token and Secret
5. Update `.env` with new tokens

### Twitter: "Rate limit exceeded"
Free tier allows only 1,500 tweets/month. Wait until next month or upgrade to Basic tier.

### "Module not found"
Ensure virtual environment is activated:
```bash
source venv/bin/activate
pip install -r scripts/requirements.txt
```

---

## .env Template

```
# LinkedIn API Credentials
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
LINKEDIN_ACCESS_TOKEN=

# Twitter/X API Credentials
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
TWITTER_BEARER_TOKEN=
```
