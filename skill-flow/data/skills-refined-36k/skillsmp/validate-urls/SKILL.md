---
name: validate-urls
description: This skill should be used when the user asks to "validate external URLs", "check for link rot", "screenshot URLs", "archive external links", or wants to verify and document external web resources (http/https) referenced in the codebase. This is for external URLs only, not internal file paths.
disable-model-invocation: true
---

# /validate-urls

Validate all external URLs in the codebase and capture screenshots for documentation.

## Purpose

External URLs in documentation, code comments, and config files can become stale (link rot). This skill:

- Finds all external URLs in the project
- Validates each URL is accessible
- Captures screenshots as visual documentation
- Generates a report mapping URLs to their screenshots

## Instructions

1. **Find all external URLs** in the codebase:

   ```bash
   # Search for URLs in common file types
   uv run grep -rEoh 'https?://[^\s<>")\]]+' . \
     --include='*.md' --include='*.py' --include='*.json' \
     --include='*.yaml' --include='*.yml' --include='*.toml' \
     --include='*.txt' --include='*.rst' \
     2>/dev/null | sort -u
   ```

   Alternatively, use the Grep tool with pattern: `https?://[^\s<>")\]]+`

2. **Filter URLs**:
   - Exclude localhost/127.0.0.1 URLs
   - Exclude file:// URLs
   - Exclude common CDN/asset URLs (fonts, icons) unless specifically requested
   - Deduplicate URLs
   - Group by domain for organized reporting

3. **Create screenshots directory**:

   ```bash
   mkdir -p .claude/url-screenshots
   ```

4. **Validate and screenshot each URL**:

   For each URL, use the WebFetch tool to:
   - Verify the URL is accessible (returns 200 OK)
   - Note any redirects
   - Capture the page title and description

   For screenshots, use Playwright (preferred) or Puppeteer:

   ```bash
   # Install playwright if needed
   uv add --dev playwright
   uv run playwright install chromium
   ```

   Create a screenshot script at `.claude/skills/validate-urls/screenshot.py`:

   ```python
   #!/usr/bin/env python3
   """Capture screenshots of URLs for documentation."""
   import asyncio
   import hashlib
   import json
   import sys
   from pathlib import Path
   from playwright.async_api import async_playwright

   async def screenshot_url(url: str, output_dir: Path) -> dict:
       """Take a screenshot of a URL and return metadata."""
       url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
       filename = f"{url_hash}.png"
       filepath = output_dir / filename

       result = {
           "url": url,
           "filename": filename,
           "status": "pending",
           "title": None,
           "error": None
       }

       async with async_playwright() as p:
           browser = await p.chromium.launch()
           page = await browser.new_page(viewport={"width": 1280, "height": 720})

           try:
               response = await page.goto(url, timeout=30000)
               result["status"] = "success" if response.ok else f"http_{response.status}"
               result["title"] = await page.title()
               await page.screenshot(path=str(filepath), full_page=False)
           except Exception as e:
               result["status"] = "error"
               result["error"] = str(e)
           finally:
               await browser.close()

       return result

   async def main(urls: list[str], output_dir: str):
       output_path = Path(output_dir)
       output_path.mkdir(parents=True, exist_ok=True)

       results = []
       for url in urls:
           print(f"Processing: {url}")
           result = await screenshot_url(url, output_path)
           results.append(result)

       # Save manifest
       manifest_path = output_path / "manifest.json"
       with open(manifest_path, "w") as f:
           json.dump(results, f, indent=2)

       return results

   if __name__ == "__main__":
       urls = sys.argv[1:]
       if not urls:
           print("Usage: screenshot.py <url1> <url2> ...")
           sys.exit(1)
       asyncio.run(main(urls, ".claude/url-screenshots"))
   ```

5. **Run the screenshot capture**:

   ```bash
   uv run python .claude/skills/validate-urls/screenshot.py \
     "https://example1.com" "https://example2.com" ...
   ```

6. **Generate the report** at `.claude/url-screenshots/README.md`:

   ```markdown
   # URL Screenshot Archive

   Generated: YYYY-MM-DD HH:MM

   This archive documents external URLs referenced in the codebase.

   ## URLs by Domain

   ### example.com

   | URL                      | Status | Screenshot      | Title      |
   | ------------------------ | ------ | --------------- | ---------- |
   | https://example.com/page | OK     | ![](abc123.png) | Page Title |

   ### another-domain.org

   ...

   ## Summary

   - Total URLs: X
   - Valid: X
   - Broken: X
   - Redirected: X

   ## Broken URLs

   | URL | Location in Codebase | Error         |
   | --- | -------------------- | ------------- |
   | ... | file.md:42           | 404 Not Found |
   ```

7. **Report findings to user**:
   - Total URLs found
   - Number of valid/broken/redirected URLs
   - Location of screenshots directory
   - Any URLs that need attention (broken, redirected to different domain)

## Output Structure

```
.claude/url-screenshots/
├── README.md           # Generated report with URL table
├── manifest.json       # Machine-readable URL metadata
├── abc123def456.png    # Screenshots (named by URL hash)
├── ...
```

## Options

When invoking, the user may specify:

- `--include-assets`: Include CDN/font/icon URLs (default: excluded)
- `--skip-screenshots`: Only validate URLs, don't capture screenshots
- `--path <dir>`: Only scan specific directory
- `--update`: Re-validate and re-screenshot all URLs (default: skip existing)

## Notes

- Screenshots are named by MD5 hash of URL for consistency
- The manifest.json allows programmatic access to results
- Run periodically to catch link rot early
- Consider adding to CI for automated link checking (skip screenshots in CI)
