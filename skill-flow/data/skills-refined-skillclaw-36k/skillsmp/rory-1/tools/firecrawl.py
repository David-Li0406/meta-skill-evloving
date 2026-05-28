"""
Firecrawl API Client

Firecrawl provides web scraping, screenshots, and site crawling.
https://firecrawl.dev

Features:
- Scrape any webpage to markdown/text
- Take screenshots of any URL
- Crawl entire websites
- Handle JavaScript-rendered pages

Usage:
    from tools.firecrawl import FirecrawlClient
    
    client = FirecrawlClient()
    
    # Scrape a page
    content = client.scrape("https://example.com")
    
    # Take screenshot
    screenshot = client.screenshot("https://example.com")
    
    # Crawl a site
    pages = client.crawl("https://example.com", max_pages=10)
"""

import base64
from typing import Optional, Any
from tools.base import BaseAPIClient, get_credential, has_credential, clean_url
from tools.errors import format_missing_credential_error, format_error_message


class FirecrawlClient(BaseAPIClient):
    """Firecrawl API client for web scraping and screenshots."""

    BASE_URL = "https://api.firecrawl.dev/v1"
    SERVICE_NAME = "firecrawl"

    def __init__(self):
        self._is_available = has_credential(self.SERVICE_NAME, "api_key")
        if self._is_available:
            super().__init__()

    @property
    def is_available(self) -> bool:
        """Check if the client has valid credentials configured."""
        return self._is_available

    def get_availability_error(self) -> dict[str, Any]:
        """Get structured error information when credentials are missing."""
        return format_missing_credential_error(self.SERVICE_NAME)

    def get_availability_message(self) -> str:
        """Get human-readable error message when credentials are missing."""
        return format_error_message(self.get_availability_error())

    def _check_availability(self) -> Optional[dict[str, Any]]:
        """Check if client is available, return error dict if not."""
        if not self._is_available:
            error = self.get_availability_error()
            error["data"] = None
            return error
        return None

    def _get_headers(self) -> dict[str, str]:
        api_key = get_credential("firecrawl", "api_key")
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def scrape(
        self,
        url: str,
        formats: list[str] = ["markdown"],
        only_main_content: bool = True,
        wait_for: int = 0,
        timeout: int = 30000
    ) -> dict[str, Any]:
        """
        Scrape a webpage and return its content.

        Args:
            url: URL to scrape
            formats: Output formats - "markdown", "html", "text", "links"
            only_main_content: Extract only main content (remove nav, footer, etc.)
            wait_for: Milliseconds to wait for JS rendering
            timeout: Request timeout in milliseconds

        Returns:
            {
                "success": bool,
                "data": {
                    "markdown": "...",
                    "metadata": {
                        "title": "...",
                        "description": "...",
                        "language": "...",
                        "sourceURL": "..."
                    }
                }
            }
            Or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        payload = {
            "url": clean_url(url),
            "formats": formats,
            "onlyMainContent": only_main_content,
            "waitFor": wait_for,
            "timeout": timeout
        }
        
        return self.post("/scrape", json=payload)
    
    def screenshot(
        self,
        url: str,
        full_page: bool = False
    ) -> dict[str, Any]:
        """
        Take a screenshot of a webpage.

        Args:
            url: URL to screenshot
            full_page: Capture full page or just viewport

        Returns:
            {
                "success": bool,
                "data": {
                    "screenshot": "base64_encoded_image",
                    "metadata": {...}
                }
            }
            Or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        payload = {
            "url": clean_url(url),
            "formats": ["screenshot"],
            "screenshot": {
                "fullPage": full_page
            }
        }
        
        return self.post("/scrape", json=payload)
    
    def save_screenshot(
        self,
        url: str,
        output_path: str,
        full_page: bool = False
    ) -> str | dict[str, Any]:
        """
        Take screenshot and save to file.

        Args:
            url: URL to screenshot
            output_path: Path to save PNG file
            full_page: Capture full page or just viewport

        Returns:
            Path to saved file, or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        result = self.screenshot(url, full_page)
        
        if result.get("success") and result.get("data", {}).get("screenshot"):
            screenshot_b64 = result["data"]["screenshot"]
            # Remove data URL prefix if present
            if "base64," in screenshot_b64:
                screenshot_b64 = screenshot_b64.split("base64,")[1]
            
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(screenshot_b64))
            
            return output_path
        
        raise ValueError(f"Screenshot failed: {result}")
    
    def crawl(
        self,
        url: str,
        max_pages: int = 10,
        include_patterns: Optional[list[str]] = None,
        exclude_patterns: Optional[list[str]] = None,
        formats: list[str] = ["markdown"]
    ) -> dict[str, Any]:
        """
        Crawl a website starting from a URL.

        Args:
            url: Starting URL
            max_pages: Maximum pages to crawl
            include_patterns: Glob patterns for URLs to include
            exclude_patterns: Glob patterns for URLs to exclude
            formats: Output formats for each page

        Returns:
            {
                "success": bool,
                "id": "crawl_job_id",
                "url": "status_check_url"
            }
            Or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        payload = {
            "url": clean_url(url),
            "limit": max_pages,
            "scrapeOptions": {
                "formats": formats
            }
        }
        
        if include_patterns:
            payload["includePaths"] = include_patterns
        if exclude_patterns:
            payload["excludePaths"] = exclude_patterns
        
        return self.post("/crawl", json=payload)
    
    def get_crawl_status(self, crawl_id: str) -> dict[str, Any]:
        """
        Check status of a crawl job.

        Args:
            crawl_id: Crawl job ID from crawl() response

        Returns:
            {
                "status": "scraping" | "completed" | "failed",
                "total": int,
                "completed": int,
                "data": [...] (when completed)
            }
            Or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        return self.get(f"/crawl/{crawl_id}")
    
    def crawl_and_wait(
        self,
        url: str,
        max_pages: int = 10,
        poll_interval: float = 2.0,
        max_wait: float = 300.0,
        **kwargs
    ) -> list[dict[str, Any]] | dict[str, Any]:
        """
        Crawl a website and wait for completion.

        Args:
            url: Starting URL
            max_pages: Maximum pages to crawl
            poll_interval: Seconds between status checks
            max_wait: Maximum seconds to wait
            **kwargs: Additional args for crawl()

        Returns:
            List of scraped page data, or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        import time

        # Start crawl
        result = self.crawl(url, max_pages, **kwargs)
        
        if not result.get("success"):
            raise ValueError(f"Crawl failed to start: {result}")
        
        crawl_id = result["id"]
        start_time = time.time()
        
        # Poll for completion
        while time.time() - start_time < max_wait:
            status = self.get_crawl_status(crawl_id)
            
            if status.get("status") == "completed":
                return status.get("data", [])
            
            if status.get("status") == "failed":
                raise ValueError(f"Crawl failed: {status}")
            
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Crawl did not complete within {max_wait} seconds")
    
    def extract_links(self, url: str) -> list[str] | dict[str, Any]:
        """
        Extract all links from a webpage.

        Args:
            url: URL to scrape

        Returns:
            List of URLs found on the page, or error dict with recovery steps if credentials missing.
        """
        # Check if credentials are available
        error = self._check_availability()
        if error:
            return error

        result = self.scrape(url, formats=["links"])
        
        if result.get("success") and result.get("data"):
            return result["data"].get("links", [])
        
        return []


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """CLI entry point for Firecrawl tools."""
    import argparse
    import json
    import sys

    parser = argparse.ArgumentParser(description="Firecrawl web scraping tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Scrape command
    scrape_parser = subparsers.add_parser("scrape", help="Scrape a webpage")
    scrape_parser.add_argument("url", help="URL to scrape")
    scrape_parser.add_argument("--format", choices=["markdown", "html", "text"], default="markdown")
    scrape_parser.add_argument("--full", action="store_true", help="Include all content (not just main)")

    # Screenshot command
    screenshot_parser = subparsers.add_parser("screenshot", help="Take screenshot of webpage")
    screenshot_parser.add_argument("url", help="URL to screenshot")
    screenshot_parser.add_argument("--output", "-o", default="screenshot.png", help="Output file path")
    screenshot_parser.add_argument("--full-page", action="store_true", help="Capture full page")

    # Crawl command
    crawl_parser = subparsers.add_parser("crawl", help="Crawl a website")
    crawl_parser.add_argument("url", help="Starting URL")
    crawl_parser.add_argument("--max-pages", type=int, default=10, help="Max pages to crawl")
    crawl_parser.add_argument("--output", "-o", help="Output JSON file")

    # Links command
    links_parser = subparsers.add_parser("links", help="Extract links from webpage")
    links_parser.add_argument("url", help="URL to extract links from")

    args = parser.parse_args()
    client = FirecrawlClient()

    # Check if credentials are available
    if not client.is_available:
        print(client.get_availability_message(), file=sys.stderr)
        sys.exit(1)

    try:
        if args.command == "scrape":
            result = client.scrape(
                args.url,
                formats=[args.format],
                only_main_content=not args.full
            )
            if result.get("success"):
                print(result["data"].get(args.format, ""))
            else:
                print(f"Error: {result}", file=__import__("sys").stderr)
        
        elif args.command == "screenshot":
            path = client.save_screenshot(args.url, args.output, args.full_page)
            print(f"Screenshot saved to: {path}")
        
        elif args.command == "crawl":
            pages = client.crawl_and_wait(args.url, args.max_pages)
            output = json.dumps(pages, indent=2)
            if args.output:
                with open(args.output, "w") as f:
                    f.write(output)
                print(f"Crawl results saved to: {args.output}")
            else:
                print(output)
        
        elif args.command == "links":
            links = client.extract_links(args.url)
            for link in links:
                print(link)
    
    finally:
        client.close()


if __name__ == "__main__":
    main()
