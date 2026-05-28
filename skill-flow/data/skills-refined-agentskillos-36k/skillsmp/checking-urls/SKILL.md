---
name: checking-urls
description: Validates all URLs (internal relative links and external URLs) in markdown files. Use when adding new content, after making changes, or when asked to check/audit links.
---

# URL Checking Skill

Validates all URLs in the repository to ensure they are active and valid.

## When to Use

- **Automatically** when new weekly entries or posts are added
- **On demand** when asked to check links
- **Periodically** to audit existing content

## Capabilities

1. **Internal links**: Validates relative paths to other markdown files
2. **External links**: Checks HTTP/HTTPS URLs are accessible (2xx/3xx status)
3. **Anchor links**: Validates `#section` references exist in target files
4. **Logging**: Records all checks to `logs/url-checks/YYYY-MM-DD.log`

## Workflow

### Run the Check Script

```bash
./scripts/check-urls.sh
```

This will:
1. Scan all `.md` files for URLs
2. Validate internal relative links
3. Check external URLs with HEAD requests
4. Write results to `logs/url-checks/YYYY-MM-DD.log`

### Log Format

```
[YYYY-MM-DD HH:MM:SS] CHECKING: source_file.md
[YYYY-MM-DD HH:MM:SS] ✓ VALID: ./weeks/2025/week-01/README.md
[YYYY-MM-DD HH:MM:SS] ✗ INVALID: <url> (404)
[YYYY-MM-DD HH:MM:SS] ✗ MISSING: ./weeks/2025/nonexistent.md
```

### When Invalid URLs Found

1. The script outputs a summary of broken links
2. **Alert the user** about each invalid URL
3. Continue alerting on subsequent runs until fixed
4. Check `logs/url-checks/` for history

## Invalid URL Tracking

The script maintains `logs/url-checks/UNRESOLVED.md` with currently broken links.
On each run, this file is updated. Use it to track what needs fixing.
