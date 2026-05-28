#!/usr/bin/env python3
"""Capture screenshots of URLs for documentation.

Usage:
    uv run python .claude/skills/validate-urls/screenshot.py <url1> <url2> ...
    uv run python .claude/skills/validate-urls/screenshot.py --from-file urls.txt
"""
import argparse
import asyncio
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from playwright.async_api import async_playwright


def url_to_filename(url: str) -> str:
    """Generate a consistent filename from a URL using MD5 hash."""
    url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
    return f"{url_hash}.png"


async def screenshot_url(url: str, output_dir: Path, timeout: int = 30000) -> dict:
    """Take a screenshot of a URL and return metadata."""
    filename = url_to_filename(url)
    filepath = output_dir / filename

    result = {
        "url": url,
        "domain": urlparse(url).netloc,
        "filename": filename,
        "status": "pending",
        "http_status": None,
        "title": None,
        "error": None,
        "captured_at": datetime.now(timezone.utc).isoformat(),
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 720})

        try:
            response = await page.goto(url, timeout=timeout, wait_until="networkidle")
            result["http_status"] = response.status if response else None

            if response and response.ok:
                result["status"] = "success"
                result["title"] = await page.title()
                await page.screenshot(path=str(filepath), full_page=False)
            else:
                result["status"] = f"http_error"
                result["error"] = (
                    f"HTTP {response.status}" if response else "No response"
                )

        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        finally:
            await browser.close()

    return result


def find_urls_in_codebase(root: Path, include_assets: bool = False) -> list[str]:
    """Find all external URLs in the codebase."""
    url_pattern = re.compile(r'https?://[^\s<>")\]\'\`]+')
    extensions = {
        ".md",
        ".py",
        ".json",
        ".yaml",
        ".yml",
        ".toml",
        ".txt",
        ".rst",
        ".html",
    }

    # Domains to exclude (unless include_assets is True)
    asset_domains = {
        "fonts.googleapis.com",
        "fonts.gstatic.com",
        "cdn.jsdelivr.net",
        "unpkg.com",
        "cdnjs.cloudflare.com",
    }

    urls = set()

    for ext in extensions:
        for filepath in root.rglob(f"*{ext}"):
            # Skip hidden directories and common non-source dirs
            if any(part.startswith(".") for part in filepath.parts[len(root.parts) :]):
                if ".claude" not in str(filepath):  # Allow .claude directory
                    continue
            if any(
                skip in filepath.parts
                for skip in ["node_modules", "venv", ".venv", "__pycache__"]
            ):
                continue

            try:
                content = filepath.read_text(encoding="utf-8", errors="ignore")
                found = url_pattern.findall(content)
                urls.update(found)
            except Exception:
                continue

    # Filter URLs
    filtered = set()
    for url in urls:
        # Clean trailing punctuation
        url = url.rstrip(".,;:!?)")

        parsed = urlparse(url)

        # Skip localhost
        if parsed.netloc in ("localhost", "127.0.0.1") or parsed.netloc.startswith(
            "localhost:"
        ):
            continue

        # Skip asset CDNs unless requested
        if not include_assets and parsed.netloc in asset_domains:
            continue

        filtered.add(url)

    return sorted(filtered)


def generate_report(results: list[dict], output_dir: Path) -> str:
    """Generate a markdown report from screenshot results."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Group by domain
    by_domain: dict[str, list[dict]] = {}
    for r in results:
        domain = r["domain"]
        if domain not in by_domain:
            by_domain[domain] = []
        by_domain[domain].append(r)

    # Count statuses
    total = len(results)
    success = sum(1 for r in results if r["status"] == "success")
    errors = sum(1 for r in results if r["status"] in ("error", "http_error"))

    lines = [
        "# URL Screenshot Archive",
        "",
        f"Generated: {now}",
        "",
        "This archive documents external URLs referenced in the codebase.",
        "",
        "## Summary",
        "",
        f"- **Total URLs**: {total}",
        f"- **Valid**: {success}",
        f"- **Errors**: {errors}",
        "",
        "## URLs by Domain",
        "",
    ]

    for domain in sorted(by_domain.keys()):
        domain_results = by_domain[domain]
        lines.append(f"### {domain}")
        lines.append("")
        lines.append("| URL | Status | Screenshot | Title |")
        lines.append("|-----|--------|------------|-------|")

        for r in domain_results:
            url = r["url"]
            status = r["status"]
            title = r.get("title") or "-"
            if r["status"] == "success":
                screenshot = f"![{r['filename']}]({r['filename']})"
            else:
                screenshot = f"Error: {r.get('error', 'Unknown')}"

            # Truncate long URLs for display
            display_url = url if len(url) < 60 else url[:57] + "..."
            lines.append(f"| {display_url} | {status} | {screenshot} | {title} |")

        lines.append("")

    # Broken URLs section
    broken = [r for r in results if r["status"] != "success"]
    if broken:
        lines.append("## Broken URLs")
        lines.append("")
        lines.append("| URL | Error |")
        lines.append("|-----|-------|")
        for r in broken:
            lines.append(f"| {r['url']} | {r.get('error', 'Unknown error')} |")
        lines.append("")

    return "\n".join(lines)


async def main():
    parser = argparse.ArgumentParser(description="Capture screenshots of URLs")
    parser.add_argument("urls", nargs="*", help="URLs to screenshot")
    parser.add_argument("--from-file", "-f", help="Read URLs from file (one per line)")
    parser.add_argument(
        "--scan", "-s", action="store_true", help="Scan codebase for URLs"
    )
    parser.add_argument(
        "--include-assets", action="store_true", help="Include CDN/font URLs"
    )
    parser.add_argument(
        "--output", "-o", default=".claude/url-screenshots", help="Output directory"
    )
    parser.add_argument(
        "--timeout", "-t", type=int, default=30000, help="Timeout in ms"
    )

    args = parser.parse_args()

    urls = list(args.urls)

    if args.from_file:
        with open(args.from_file) as f:
            urls.extend(
                line.strip() for line in f if line.strip() and not line.startswith("#")
            )

    if args.scan:
        print("Scanning codebase for URLs...")
        found = find_urls_in_codebase(Path("."), include_assets=args.include_assets)
        print(f"Found {len(found)} URLs")
        urls.extend(found)

    if not urls:
        print("No URLs provided. Use positional args, --from-file, or --scan")
        sys.exit(1)

    # Deduplicate
    urls = sorted(set(urls))
    print(f"Processing {len(urls)} unique URLs...")

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url}")
        result = await screenshot_url(url, output_dir, timeout=args.timeout)
        results.append(result)
        print(f"  -> {result['status']}")

    # Save manifest
    manifest_path = output_dir / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nManifest saved to {manifest_path}")

    # Generate report
    report = generate_report(results, output_dir)
    report_path = output_dir / "README.md"
    with open(report_path, "w") as f:
        f.write(report)
    print(f"Report saved to {report_path}")

    # Summary
    success = sum(1 for r in results if r["status"] == "success")
    print(f"\nDone! {success}/{len(results)} URLs captured successfully")

    if success < len(results):
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
