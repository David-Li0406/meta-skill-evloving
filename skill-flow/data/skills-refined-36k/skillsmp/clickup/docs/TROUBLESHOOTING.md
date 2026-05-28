# Troubleshooting Guide

Common issues and solutions for the ClickUp CLI.

## Authentication Issues

### "CLICKUP_API_TOKEN is not set"

**Cause:** Missing or empty API token in `.env`

**Solution:**
1. Get your token: ClickUp Settings → Apps → API Token
2. Add to `.env`:
   ```
   CLICKUP_API_TOKEN=pk_your_token_here
   ```

### "Invalid API token" / 401 Error

**Cause:** Token is invalid, expired, or malformed

**Solution:**
1. Regenerate token in ClickUp Settings → Apps
2. Ensure no extra spaces or quotes in `.env`
3. Token should start with `pk_`

---

## Workspace Issues

### "CLICKUP_WORKSPACE_ID is not set"

**Cause:** Missing workspace ID in `.env`

**Solution:**
1. Find your workspace ID in the ClickUp URL: `app.clickup.com/WORKSPACE_ID/home`
2. Or list workspaces:
   ```bash
   npm run dev -- workspaces list
   ```
3. Add to `.env`:
   ```
   CLICKUP_WORKSPACE_ID=your_workspace_id
   ```

### Wrong Workspace Data

**Cause:** Multiple workspaces, using wrong ID

**Solution:**
1. List all workspaces:
   ```bash
   npm run dev -- workspaces list
   ```
2. Update `CLICKUP_WORKSPACE_ID` in `.env`

---

## Task Issues

### "Task not found"

**Cause:** Invalid task ID or task in different workspace

**Solutions:**
1. Verify task ID format:
   - Custom ID: `TCG-4752`
   - Internal ID: `86dz8kbp5`

2. Check task exists:
   ```bash
   npm run dev -- tasks search "task name"
   ```

3. Include closed tasks:
   ```bash
   npm run dev -- tasks search "task name" --include-closed
   ```

### Custom ID Not Resolving

**Cause:** Custom IDs must match exactly (case-insensitive)

**Solution:**
- Use exact format: `TCG-4752` not `tcg4752`
- Or use internal ID from task URL

---

## Time Entry Issues

### "No time entries found"

**Cause:** No entries in specified date range

**Solutions:**
1. Check date format: `YYYY-MM-DD`
2. Try broader range:
   ```bash
   npm run dev -- time list --start 2026-01-01 --end 2026-01-31
   ```

### Time Showing as 0 or Incorrect

**Cause:** Duration parsing issue

**Solution:** The CLI expects duration in milliseconds from API. If you see raw numbers like `3600000`, this is a display bug. Report it.

### Entry Shows "No task"

**Cause:** Time entry not linked to a task, or API response format issue

**Solution:** This is cosmetic - the entry was created/updated successfully. Verify with `time list`.

---

## Rate Limiting

### 429 "Too Many Requests"

**Cause:** Exceeded ClickUp API rate limits (100/min for free plans)

**Solution:**
1. Wait and retry - CLI handles this automatically
2. Reduce request frequency
3. Batch operations where possible

---

## Date/Time Issues

### Wrong Timezone

**Cause:** Times displayed in local timezone, but entered in different zone

**Solution:**
- Enter times in your local timezone
- The CLI uses your system timezone

### "Invalid date format"

**Cause:** Unsupported date format

**Supported formats:**
- `YYYY-MM-DD` - Date only
- `YYYY-MM-DD HH:MM` - Date and time
- `today`, `yesterday`, `tomorrow` - Keywords

---

## Network Issues

### Timeout / Connection Errors

**Cause:** Network issues or ClickUp API down

**Solutions:**
1. Check internet connection
2. Check ClickUp status: https://status.clickup.com/
3. Retry after a few minutes

---

## Getting Help

### Debug Mode

For detailed error info:
```bash
DEBUG=* npm run dev -- tasks search "test"
```

### Check Configuration

```bash
npm run dev -- config show
```

### API Response

Use `--json` to see raw API responses:
```bash
npm run dev -- tasks get TCG-4752 --json
```

### Find Your User ID

Your user ID is in your API token: `pk_USER_ID_...`

Or find it:
```bash
npm run dev -- members find "your@email.com"
```
