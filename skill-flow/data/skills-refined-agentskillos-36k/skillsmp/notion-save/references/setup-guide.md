# Notion Integration Setup Guide

## Step 1: Create Notion Integration

1. Go to https://www.notion.so/my-integrations
2. Click "+ New integration"
3. Configure:
   - **Name**: `Claude Code Sync` (or your preference)
   - **Associated workspace**: Select your workspace
   - **Capabilities**: 
     - ✅ Read content
     - ✅ Update content  
     - ✅ Insert content
4. Click "Submit"
5. Copy the **Internal Integration Token** (starts with `ntn_` or `secret_`)

## Step 2: Share Database with Integration

1. Open your Notion database ("new day")
2. Click the "..." menu in the top-right corner
3. Scroll down to "Add connections"
4. Search for and select your integration ("Claude Code Sync")
5. Confirm the connection

## Step 3: Configure Claude Code

### Option A: Environment Variable (Recommended)

Add to your shell config (`~/.bashrc`, `~/.zshrc`, or Windows equivalent):

```bash
export NOTION_API_KEY="ntn_your_token_here"
```

Then reload:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### Option B: .env File

Create `.env` in your project directory:

```
NOTION_API_KEY=ntn_your_token_here
NOTION_DATABASE_ID=2decc7dd-3404-8002-a7e7-d64733a75885
```

### Option C: Claude Code Settings

If Claude Code supports environment configuration, add the API key there.

## Step 4: Verify Connection

Test the connection:

```bash
python3 scripts/save_to_notion.py --list
```

Expected output:
```
📋 Recent pages in database:

  • Page Title (2024-01-04)
    https://www.notion.so/...
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Check token is correct and not expired |
| 404 Not Found | Database not shared | Share database with your integration |
| 400 Bad Request | Property mismatch | Check property names match database schema |
| Connection timeout | Network issue | Check internet connection |

## Security Notes

- Never commit API keys to version control
- Use environment variables or secret managers
- Rotate keys periodically via Notion integrations page
- Integration only accesses pages explicitly shared with it
