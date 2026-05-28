---
name: staging-browser-localhost
description: Open a headless browser authenticated with Aircall staging credentials for localhost development
---

# Staging Browser (Localhost)

Opens an agent-browser instance authenticated with staging credentials for localhost development.

## Usage

Use this skill when you need to open a browser at `http://localhost:<PORT>` authenticated against the Aircall staging environment.

## Steps to Execute

### 1. Get the Staging Token

Invoke the `/staging-token` skill to retrieve the JWT token. Extract `idToken` and `refreshToken` from the JSON response.

### 2. Navigate to SSO Callback with Tokens

Navigate directly to the SSO callback URL with tokens as query parameters:

```bash
agent-browser --session staging open "http://localhost:<PORT>/sso/callback?token=$ID_TOKEN&refresh_token=$REFRESH_TOKEN&redirect=$TARGET_PATH"
```

Where:
- `$ID_TOKEN` - the `idToken` from step 1
- `$REFRESH_TOKEN` - the `refreshToken` from step 1
- `$TARGET_PATH` - the path to redirect to after auth (e.g., `/playground`)

The app will read the tokens from query params, store them, and redirect to the target page authenticated.

### 3. Interact with Page

```bash
# Get accessibility snapshot for AI interaction
agent-browser --session staging snapshot -i -c

# Take screenshot if needed
agent-browser --session staging screenshot /tmp/staging-screenshot.png
```

## Arguments

- **URL** (optional): The localhost URL to navigate to. If a path is provided (e.g., `/playground`), use it as the `redirect` param.

## Technical Details

- **SSO Callback Route**: `/sso/callback`
- **Query Params**: `token`, `refresh_token`, `redirect`
- **Session Name**: `staging`
- **Browser Mode**: Headless (default), use `--headed` for visible browser

## Session Management

- Uses `--session staging` for isolated browser context
- Session persists until explicitly closed with `agent-browser --session staging close`
