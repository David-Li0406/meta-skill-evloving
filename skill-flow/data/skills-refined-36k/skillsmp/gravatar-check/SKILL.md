---
name: gravatar-check
description: Check if a Gravatar exists for an email address. Use when the user wants to verify if someone has a Gravatar, check avatar availability, or validate email addresses against Gravatar's database.
---

# Check Gravatar Availability

Check if a Gravatar avatar exists for an email address.

## Script Execution (Preferred)

```bash
npx tsx scripts/check.ts <email> [options]
```

Options:
- `--no-cache` - Bypass cache and fetch fresh data

Run from the gravatar plugin directory: `~/.claude/plugins/cache/gravatar/`

## How It Works

Uses a HEAD request with `d=404` parameter to check if a Gravatar exists:
- If Gravatar exists: Returns 200 OK
- If no Gravatar: Returns 404 Not Found

Results are cached for 24 hours to avoid redundant API calls.

## Usage

```bash
npx tsx scripts/check.ts <email> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `email` | Yes | Email address to check for Gravatar |

### Options

| Option | Description |
|--------|-------------|
| `--no-cache` | Bypass cache and fetch fresh data from Gravatar |

### Output

When Gravatar exists:
```
Checking: user@example.com

✓ Gravatar exists
  Hash: b48bf4373d7b7374351c0544f36f7fc3
  URL: https://www.gravatar.com/avatar/b48bf4373d7b7374351c0544f36f7fc3
  Profile: https://www.gravatar.com/b48bf4373d7b7374351c0544f36f7fc3
```

When no Gravatar found:
```
Checking: nonexistent@example.com

✗ No Gravatar found
  Hash: abc123def456789...
  This email does not have a Gravatar image.
  A default image will be shown.
```

## Examples

Check if developer has Gravatar:
```bash
npx tsx scripts/check.ts beau@dentedreality.com.au
```

Bypass cache for fresh check:
```bash
npx tsx scripts/check.ts user@example.com --no-cache
```

## Use Cases

### Validate Email Addresses
Check if an email is associated with a Gravatar profile:
```bash
npx tsx scripts/check.ts contact@company.com
```

### Bulk User Verification
Check multiple team members:
```bash
for email in dev1@company.com dev2@company.com; do
  npx tsx scripts/check.ts "$email"
done
```

### Conditional Avatar Display
Verify Gravatar exists before displaying avatar in UI:
```bash
npx tsx scripts/check.ts user@example.com && echo "Show Gravatar" || echo "Show default"
```

## Caching

Results are cached for 24 hours. Since Gravatars change infrequently, caching improves performance while maintaining accuracy.

Use `--no-cache` when you need real-time verification.

## Exit Codes

- `0` - Success (Gravatar exists or check completed)
- `1` - Error (invalid usage or network error)

Note: A "No Gravatar found" result is still exit code 0 - it's a successful check that returned no avatar.

## Related

- Use `gravatar-url` skill to generate Gravatar URLs
- Use `gravatar-download` skill to download Gravatar images
- Combine with GitHub/npm user lookups to check developer avatars
