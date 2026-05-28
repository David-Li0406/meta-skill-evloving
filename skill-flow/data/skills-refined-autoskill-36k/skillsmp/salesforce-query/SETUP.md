# Salesforce Query Skill - Setup Guide

This guide will help you set up bearer token authentication for the Salesforce Query skill.

## Prerequisites

- Python 3.7 or higher
- A Salesforce account (Developer Edition, Sandbox, or Production)
- Access to Salesforce Developer Console or existing OAuth setup

## Step 1: Install Python Dependencies

```bash
cd .claude/skills/salesforce-query
pip install -r requirements.txt
```

## Step 2: Obtain a Bearer Token

This skill uses **bearer token authentication**. You need to provide a valid bearer token - the skill does NOT manage OAuth flows or store credentials.

### Method A: Session ID (Recommended - Quick & Simple)

**Best for**: Quick queries, ad-hoc usage, testing

1. **Log into Salesforce**
   - Navigate to your Salesforce instance

2. **Open Developer Console**:
   - Click Setup (gear icon) → Developer Console
   - Or go to: Setup → Developer Console

3. **Get Session ID**:
   - In Developer Console, go to Debug → Open Execute Anonymous Window
   - Enter this code:
     ```apex
     System.debug(UserInfo.getSessionId());
     ```
   - Click "Execute"
   - Go to Logs tab → Double-click the newest log
   - Find the line with `USER_DEBUG` containing your session ID
   - Copy the session ID (long alphanumeric string starting with `00D`)

4. **Session Expiration**:
   - Sessions expire after 2 hours of inactivity
   - When expired, simply get a new session ID using the same steps

**Example Session ID**:
```
00D5g000007xxxx!AQcAQHxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

### Method B: OAuth Access Token (For Existing OAuth Setups)

**Best for**: Production integrations, existing OAuth infrastructure

If you already have an OAuth setup (Connected App, external OAuth provider), you can use the access token directly:

1. **Obtain Access Token** via your existing OAuth flow
2. **Use the access token** as the bearer token for this skill

**Note**: This skill does NOT:
- Manage OAuth authorization flows
- Exchange authorization codes for tokens
- Refresh expired tokens
- Store or persist tokens

You must handle OAuth outside of this skill and provide the resulting access token.

---

### Method C: API-Only User Token

**Best for**: Automated systems, service accounts

1. **Create an API-Only User** in Salesforce (Setup → Users)
2. **Generate a token** via your preferred OAuth method
3. **Use the token** with this skill

---

## Step 3: Validate Your Bearer Token (Optional)

Test that your token works:

```bash
python scripts/validate_token.py https://your-instance.salesforce.com YOUR_BEARER_TOKEN
```

**Example**:
```bash
python scripts/validate_token.py https://orgfarm-924bfe02e7-dev-ed.develop.lightning.force.com 00D5g000007xxxx!AQcAQ...
```

**Output**:
```json
{
  "success": true,
  "message": "Token is valid and has API access",
  "api_usage": {
    "daily_api_requests_used": 142,
    "daily_api_requests_limit": 15000
  }
}
```

---

## Step 4: Test the Setup

Try a simple query:

```bash
python scripts/query.py https://your-instance.salesforce.com YOUR_BEARER_TOKEN "SELECT Id, Name FROM Account LIMIT 5" --verbose
```

Or use the skill from Claude Code:

```
/salesforce-query show me all accounts
```

When prompted, provide:
- Instance URL: `https://yourorg.my.salesforce.com`
- Bearer Token: Your session ID or OAuth access token

---

## Token Format

The scripts accept tokens in multiple formats:

- **Plain token**: `00D5g000007xxxx!AQcAQ...`
- **Bearer prefix**: `Bearer 00D5g000007xxxx!AQcAQ...`
- **OAuth prefix**: `OAuth 00D5g000007xxxx!AQcAQ...`

The skill will automatically add the `Bearer ` prefix if not present.

---

## Security Best Practices

1. **Never share tokens** - They provide full access to your Salesforce org
2. **Never commit tokens** - Don't store in code, config files, or version control
3. **Use short-lived tokens** - Session IDs expire after 2 hours (recommended)
4. **Use sandboxes for testing** - Test on sandbox instances when possible
5. **Monitor API usage** - Check Salesforce API usage reports regularly
6. **Rotate tokens regularly** - Get fresh session IDs/tokens frequently

### What This Skill Does NOT Do

- ❌ Store tokens locally
- ❌ Persist credentials between sessions
- ❌ Manage OAuth flows
- ❌ Refresh expired tokens
- ❌ Cache authentication state

### What This Skill DOES

- ✅ Accept pre-obtained bearer tokens
- ✅ Validate tokens (optional)
- ✅ Use tokens for API queries only
- ✅ Keep tokens in memory only during session
- ✅ Require fresh tokens each session

---

## Troubleshooting

### "Authentication failed" or 401 Error

**Causes**:
- Token expired (session IDs expire after 2 hours of inactivity)
- Token invalid or malformed
- Instance URL doesn't match the token's org

**Solutions**:
1. Get a fresh session ID using Method A above
2. Verify instance URL matches your org
3. Check token wasn't truncated when copying

---

### "Invalid Session ID" When Getting Token

**Causes**:
- Trying to debug session ID in Salesforce sandbox with IP restrictions
- Browser session expired

**Solutions**:
1. Log out and log back in to Salesforce
2. Check IP restrictions in Setup → Session Settings
3. Try from a different browser

---

### Token Works but Queries Fail

**Causes**:
- User doesn't have read permissions on the object
- Object doesn't exist in the org
- API version mismatch

**Solutions**:
1. Verify your user profile has read access to the objects
2. Check that the object exists (standard objects: Account, Contact, etc.)
3. Contact your Salesforce admin if permission issues persist

---

### Port 8080 Error (if you see this, report it!)

This skill should NOT use port 8080 (that was for OAuth flows which are now removed). If you see port-related errors, the skill may still have OAuth remnants - please report this issue.

---

## API Rate Limits

**Salesforce API Limits** (Developer Edition):
- 15,000 API calls per 24 hours
- Limits reset at midnight UTC

**This skill's usage**:
- ~1-3 API calls per query (depends on schema fetching)
- You can run thousands of queries per day safely

**Check your usage**:
```bash
python scripts/validate_token.py <instance_url> <token>
```

---

## Next Steps

Once you have your bearer token, use natural language queries:

```
/salesforce-query find all opportunities closing this quarter
/salesforce-query show contacts from California accounts
/salesforce-query list high-value accounts in the technology industry
```

The skill will automatically:
- Generate appropriate SOQL queries
- Handle authentication with your bearer token
- Format results as tables
- Handle pagination for large result sets

**Important**: You'll need to provide your instance URL and bearer token at the start of each Claude Code session. Tokens are never persisted.

---

## Alternative: Setting Up OAuth (Advanced)

If you want to set up your own OAuth flow **outside** of this skill:

1. **Create a Connected App** in Salesforce:
   - Setup → App Manager → New Connected App
   - Enable OAuth Settings
   - Set scopes: `api`, `refresh_token`
   - Set callback URL for your OAuth implementation

2. **Implement OAuth flow** using your preferred method:
   - Salesforce OAuth libraries
   - Postman OAuth flow
   - Custom implementation

3. **Extract access token** from OAuth response

4. **Use access token** with this skill as the bearer token

This approach gives you longer-lived tokens and refresh capabilities, but you must manage the OAuth flow yourself.

---

Enjoy querying Salesforce with natural language!
