---
name: browser-cookie-refresh
description: Refresh session cookies from websites that require login. Use when user says "refresh cookie", "update session", or mentions cookie expiration for services like Forkable.
argument-hint: <service-name> (e.g., forkable)
---

# Browser Cookie Refresh (HITL/CITL)

This skill helps refresh session cookies for services that don't offer API keys.
It uses Chrome DevTools MCP to extract cookies after the user logs in.

## Supported Services

### Forkable
- **Cookie name**: `_easyorder_session`
- **Login URL**: `https://forkable.com/mc/admin/members`
- **Env var**: `FORKABLE_SESSION_COOKIE`
- **Update script**: `./scripts/update-forkable-cookie.sh`

## Workflow

When user asks to refresh a cookie (e.g., "refresh the forkable cookie"):

### Step 1: Open the login page
```
Use mcp__chrome-devtools__new_page to open the service's login URL
```

**If you get a "browser is already running" error:**
1. Kill the stale browser process:
   ```bash
   pkill -f "chrome-devtools-mcp/chrome-profile"
   ```
2. Retry opening the page with `mcp__chrome-devtools__new_page`

### Step 2: Wait for user to log in
```
Ask user: "Please log in to [service] in the browser window. Let me know when you're logged in and see the admin/dashboard page."
```

### Step 3: Trigger a request to capture cookies
```
Use mcp__chrome-devtools__navigate_page to reload or navigate within the site
This ensures fresh network requests with cookies
```

### Step 4: Extract the cookie
```
Use mcp__chrome-devtools__list_network_requests to find recent requests
Use mcp__chrome-devtools__get_network_request to get the request details
Parse the cookie value from the request headers
```

### Step 5: Update the cookie
```
Run the update script with the extracted cookie value
Report success and expiration date if available
```

## Example Flow for Forkable

1. `mcp__chrome-devtools__new_page` with url `https://forkable.com/mc/admin/members`
   - If "browser is already running" error: run `pkill -f "chrome-devtools-mcp/chrome-profile"` then retry
2. Ask user to log in, wait for confirmation
3. `mcp__chrome-devtools__list_network_requests` with `resourceTypes: ["fetch", "xhr", "document"]`
4. `mcp__chrome-devtools__get_network_request` for a forkable.com request (prefer GraphQL or API requests)
5. Extract `_easyorder_session` from the `cookie` request header (not response)
6. Run `./scripts/update-forkable-cookie.sh <cookie-value>`
7. Report: "Cookie updated! Expires ~45 days from now."

## Adding New Services

To add a new service, create a script at `./scripts/update-<service>-cookie.sh` and add the service config above.
