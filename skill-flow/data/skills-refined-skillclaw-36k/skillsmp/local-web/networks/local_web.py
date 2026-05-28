#!/usr/bin/env python3
"""
Local Web Access - Fetch HTML and screenshots from local/LAN URLs.

AI CLI tools (Claude Code, Codex, etc.) cannot access private network URLs
because their requests go through cloud servers. This module runs locally
and can access any URL your machine can reach.

Features:
- Fetch HTML content from local/LAN URLs
- Take screenshots using headless browser (playwright)
- LLM-optimized output (JSON, minimal) and human-friendly output
"""
import base64
import json
import logging
import socket
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, Tuple, Dict, Any, Literal
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

# Browser type for playwright
BrowserType = Literal["chromium", "firefox", "webkit"]


def _launch_browser(playwright, browser: BrowserType = "firefox"):
    """Launch specified browser type."""
    if browser == "firefox":
        return playwright.firefox.launch(headless=True)
    elif browser == "chromium":
        return playwright.chromium.launch(headless=True)
    elif browser == "webkit":
        return playwright.webkit.launch(headless=True)
    else:
        raise ValueError(f"Unknown browser: {browser}")


@dataclass
class FetchResult:
    """Result of fetching a URL."""
    url: str
    success: bool
    status_code: Optional[int] = None
    content_type: Optional[str] = None
    content: Optional[str] = None
    content_length: Optional[int] = None
    error: Optional[str] = None
    headers: Optional[Dict[str, str]] = None

    def to_json(self) -> str:
        """Serialize to JSON for LLM consumption."""
        return json.dumps(asdict(self), indent=2)

    def to_human(self) -> str:
        """Format for human-readable output."""
        if not self.success:
            return f"✗ Failed to fetch {self.url}\n  Error: {self.error}"

        lines = [
            f"✓ {self.url}",
            f"  Status: {self.status_code}",
            f"  Type: {self.content_type}",
            f"  Size: {self.content_length} bytes",
        ]
        if self.content:
            preview = self.content[:500] + "..." if len(self.content) > 500 else self.content
            lines.append(f"\n{preview}")
        return "\n".join(lines)


@dataclass
class ScreenshotResult:
    """Result of taking a screenshot."""
    url: str
    success: bool
    output_path: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    error: Optional[str] = None
    base64_data: Optional[str] = None  # For inline LLM consumption

    def to_json(self) -> str:
        """Serialize to JSON for LLM consumption."""
        data = asdict(self)
        # Don't include huge base64 in JSON by default
        if self.base64_data and len(self.base64_data) > 1000:
            data['base64_data'] = f"<{len(self.base64_data)} bytes - use --inline to include>"
        return json.dumps(data, indent=2)

    def to_human(self) -> str:
        """Format for human-readable output."""
        if not self.success:
            return f"✗ Failed to screenshot {self.url}\n  Error: {self.error}"
        return f"✓ Screenshot saved: {self.output_path} ({self.width}x{self.height})"


def is_local_url(url: str) -> bool:
    """Check if URL points to local/private network."""
    parsed = urlparse(url)
    host = parsed.hostname or ""

    # Localhost variants
    if host in ('localhost', '127.0.0.1', '::1'):
        return True

    # Private IP ranges
    try:
        import ipaddress
        ip = ipaddress.ip_address(host)
        return ip.is_private or ip.is_loopback
    except ValueError:
        # Not an IP, could be a hostname
        pass

    # .local domains
    if host.endswith('.local'):
        return True

    return False


def fetch_url(
    url: str,
    timeout: float = 10.0,
    include_headers: bool = False,
    verify_ssl: bool = True,
) -> FetchResult:
    """
    Fetch HTML content from a URL.

    Works with local/LAN URLs that cloud AI tools cannot access.

    Args:
        url: The URL to fetch
        timeout: Request timeout in seconds
        include_headers: Include response headers in result
        verify_ssl: Verify SSL certificates (disable for self-signed)

    Returns:
        FetchResult with content or error information
    """
    logger.info(f"Fetching URL: {url}")

    try:
        # Create SSL context if needed
        context = None
        if not verify_ssl:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

        # Create request with user agent
        request = urllib.request.Request(
            url,
            headers={'User-Agent': 'local-web/1.0 (AI Agent Tool)'}
        )

        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            content = response.read()
            charset = response.headers.get_content_charset() or 'utf-8'

            try:
                content_str = content.decode(charset)
            except UnicodeDecodeError:
                content_str = content.decode('utf-8', errors='replace')

            headers = dict(response.headers) if include_headers else None

            return FetchResult(
                url=url,
                success=True,
                status_code=response.status,
                content_type=response.headers.get('Content-Type'),
                content=content_str,
                content_length=len(content),
                headers=headers,
            )

    except urllib.error.HTTPError as e:
        return FetchResult(
            url=url,
            success=False,
            status_code=e.code,
            error=f"HTTP {e.code}: {e.reason}",
        )
    except urllib.error.URLError as e:
        return FetchResult(
            url=url,
            success=False,
            error=f"URL Error: {e.reason}",
        )
    except socket.timeout:
        return FetchResult(
            url=url,
            success=False,
            error=f"Timeout after {timeout}s",
        )
    except Exception as e:
        return FetchResult(
            url=url,
            success=False,
            error=str(e),
        )


def screenshot_url(
    url: str,
    output_path: Optional[Path] = None,
    width: int = 1280,
    height: int = 720,
    full_page: bool = True,
    timeout: float = 30.0,
    include_base64: bool = False,
    browser: BrowserType = "firefox",
) -> ScreenshotResult:
    """
    Take a screenshot of a URL using headless browser.

    Requires playwright to be installed:
        pip install playwright
        playwright install firefox  # or chromium

    Args:
        url: The URL to screenshot
        output_path: Where to save the screenshot (default: temp file)
        width: Viewport width
        height: Viewport height
        full_page: Capture full scrollable page
        timeout: Page load timeout in seconds
        include_base64: Include base64 data in result for LLM inline viewing
        browser: Browser to use (firefox, chromium, webkit)

    Returns:
        ScreenshotResult with file path or error information
    """
    logger.info(f"Taking screenshot of: {url}")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return ScreenshotResult(
            url=url,
            success=False,
            error="playwright not installed. Run: pip install playwright && playwright install firefox",
        )

    # Default output path
    if output_path is None:
        import tempfile
        output_path = Path(tempfile.mktemp(suffix='.png', prefix='screenshot_'))
    else:
        output_path = Path(output_path)

    try:
        with sync_playwright() as p:
            b = _launch_browser(p, browser)
            page = b.new_page(viewport={'width': width, 'height': height})

            # Navigate with timeout
            page.goto(url, wait_until='networkidle', timeout=timeout * 1000)

            # Take screenshot
            page.screenshot(path=str(output_path), full_page=full_page)

            b.close()

        # Read base64 if requested
        base64_data = None
        if include_base64:
            with open(output_path, 'rb') as f:
                base64_data = base64.b64encode(f.read()).decode('ascii')

        return ScreenshotResult(
            url=url,
            success=True,
            output_path=str(output_path),
            width=width,
            height=height,
            base64_data=base64_data,
        )

    except Exception as e:
        return ScreenshotResult(
            url=url,
            success=False,
            error=str(e),
        )


def check_local_access(url: str, timeout: float = 5.0) -> Tuple[bool, str]:
    """
    Quick check if a local URL is accessible.

    Args:
        url: URL to check
        timeout: Connection timeout

    Returns:
        Tuple of (is_accessible, message)
    """
    parsed = urlparse(url)
    host = parsed.hostname or 'localhost'
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)

    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        return True, f"✓ {host}:{port} is accessible"
    except socket.timeout:
        return False, f"✗ {host}:{port} timed out after {timeout}s"
    except ConnectionRefusedError:
        return False, f"✗ {host}:{port} connection refused (service not running?)"
    except socket.gaierror as e:
        return False, f"✗ {host} - DNS resolution failed: {e}"
    except Exception as e:
        return False, f"✗ {host}:{port} - {e}"


# ============== Browser Automation ==============

@dataclass
class InteractionResult:
    """Result of a browser interaction."""
    url: str
    action: str
    success: bool
    selector: Optional[str] = None
    before_screenshot: Optional[str] = None  # base64 or path
    after_screenshot: Optional[str] = None   # base64 or path
    page_content: Optional[str] = None
    error: Optional[str] = None
    elements_found: int = 0
    
    def to_json(self) -> str:
        data = asdict(self)
        # Truncate large base64 for readability
        for key in ('before_screenshot', 'after_screenshot'):
            if data.get(key) and len(data[key]) > 200:
                data[key] = f"<base64 {len(data[key])} bytes>"
        if data.get('page_content') and len(data['page_content']) > 500:
            data['page_content'] = data['page_content'][:500] + '...'
        return json.dumps(data, indent=2)
    
    def to_human(self) -> str:
        if not self.success:
            return f"✗ {self.action} failed on {self.url}\n  Error: {self.error}"
        return f"✓ {self.action} on {self.selector or self.url}\n  Elements found: {self.elements_found}"


@dataclass
class CrawlResult:
    """Result of crawling a site."""
    base_url: str
    success: bool
    pages_crawled: int = 0
    pages: Optional[list] = None  # List of {url, title, screenshot_path, links}
    error: Optional[str] = None
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)
    
    def to_human(self) -> str:
        if not self.success:
            return f"✗ Crawl failed: {self.error}"
        lines = [f"✓ Crawled {self.pages_crawled} pages from {self.base_url}"]
        if self.pages:
            for p in self.pages[:10]:
                lines.append(f"  - {p.get('title', 'Untitled')}: {p.get('url')}")
            if len(self.pages) > 10:
                lines.append(f"  ... and {len(self.pages) - 10} more")
        return "\n".join(lines)


def interact_with_page(
    url: str,
    action: str = "click",
    selector: Optional[str] = None,
    text: Optional[str] = None,
    wait_after: float = 1.0,
    screenshot_before: bool = True,
    screenshot_after: bool = True,
    timeout: float = 30.0,
    browser: BrowserType = "firefox",
) -> InteractionResult:
    """
    Interact with a webpage element using headless browser.
    
    Actions:
    - click: Click an element (by selector or text)
    - type: Type text into an input (requires selector and text)
    - hover: Hover over an element
    - scroll: Scroll the page (selector optional)
    - wait: Just wait and observe
    
    Args:
        url: The URL to interact with
        action: Action to perform (click, type, hover, scroll, wait)
        selector: CSS selector or text to find element
        text: Text to type (for 'type' action) or text content to find
        wait_after: Seconds to wait after action for effects
        screenshot_before: Capture screenshot before action
        screenshot_after: Capture screenshot after action
        timeout: Page load timeout
        browser: Browser to use (firefox, chromium, webkit)
    
    Returns:
        InteractionResult with before/after state
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return InteractionResult(
            url=url,
            action=action,
            success=False,
            error="playwright not installed. Run: pip install playwright && playwright install firefox",
        )
    
    import tempfile
    before_path = None
    after_path = None
    
    try:
        with sync_playwright() as p:
            b = _launch_browser(p, browser)
            page = b.new_page(viewport={'width': 1280, 'height': 720})
            page.goto(url, wait_until='networkidle', timeout=timeout * 1000)
            
            # Screenshot before
            if screenshot_before:
                before_path = tempfile.mktemp(suffix='_before.png', prefix='interact_')
                page.screenshot(path=before_path, full_page=False)
            
            elements_found = 0
            target = None
            
            # Find element
            if selector:
                # Try CSS selector first
                try:
                    target = page.locator(selector)
                    elements_found = target.count()
                except:
                    pass
                
                # If not found, try text match
                if elements_found == 0 and text is None:
                    target = page.get_by_text(selector)
                    elements_found = target.count()
            elif text:
                target = page.get_by_text(text)
                elements_found = target.count()
            
            # Perform action
            if action == "click" and target and elements_found > 0:
                target.first.click()
            elif action == "type" and target and text:
                target.first.fill(text)
            elif action == "hover" and target and elements_found > 0:
                target.first.hover()
            elif action == "scroll":
                if selector:
                    page.locator(selector).first.scroll_into_view_if_needed()
                else:
                    page.evaluate("window.scrollBy(0, 500)")
            elif action == "wait":
                pass  # Just wait
            
            # Wait for effects
            page.wait_for_timeout(wait_after * 1000)
            
            # Screenshot after
            if screenshot_after:
                after_path = tempfile.mktemp(suffix='_after.png', prefix='interact_')
                page.screenshot(path=after_path, full_page=False)
            
            # Get page content
            content = page.content()
            
            b.close()
            
            return InteractionResult(
                url=url,
                action=action,
                success=True,
                selector=selector or text,
                before_screenshot=before_path,
                after_screenshot=after_path,
                page_content=content,
                elements_found=elements_found,
            )
    
    except Exception as e:
        return InteractionResult(
            url=url,
            action=action,
            success=False,
            selector=selector,
            error=str(e),
        )


def crawl_site(
    url: str,
    max_pages: int = 20,
    screenshot_each: bool = True,
    same_origin_only: bool = True,
    timeout: float = 30.0,
    output_dir: Optional[Path] = None,
    browser: BrowserType = "firefox",
) -> CrawlResult:
    """
    Crawl a website, capturing screenshots and discovering pages.
    
    Args:
        url: Starting URL
        max_pages: Maximum pages to crawl
        screenshot_each: Take screenshot of each page
        same_origin_only: Only follow links to same origin
        timeout: Page load timeout per page
        output_dir: Directory to save screenshots (default: temp dir)
        browser: Browser to use (firefox, chromium, webkit)
    
    Returns:
        CrawlResult with all discovered pages
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return CrawlResult(
            base_url=url,
            success=False,
            error="playwright not installed. Run: pip install playwright && playwright install firefox",
        )
    
    import tempfile
    from urllib.parse import urljoin
    
    if output_dir is None:
        output_dir = Path(tempfile.mkdtemp(prefix='crawl_'))
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    parsed_base = urlparse(url)
    base_origin = f"{parsed_base.scheme}://{parsed_base.netloc}"
    
    visited = set()
    to_visit = [url]
    pages = []
    
    try:
        with sync_playwright() as p:
            b = _launch_browser(p, browser)
            page = b.new_page(viewport={'width': 1280, 'height': 720})
            
            while to_visit and len(visited) < max_pages:
                current_url = to_visit.pop(0)
                
                # Normalize URL
                if current_url in visited:
                    continue
                
                # Skip non-http
                if not current_url.startswith(('http://', 'https://')):
                    continue
                
                # Same origin check
                if same_origin_only:
                    parsed = urlparse(current_url)
                    if f"{parsed.scheme}://{parsed.netloc}" != base_origin:
                        continue
                
                visited.add(current_url)
                
                try:
                    page.goto(current_url, wait_until='networkidle', timeout=timeout * 1000)
                    
                    title = page.title()
                    
                    # Screenshot
                    screenshot_path = None
                    if screenshot_each:
                        safe_name = current_url.replace('://', '_').replace('/', '_')[:50]
                        screenshot_path = str(output_dir / f"{len(pages):03d}_{safe_name}.png")
                        page.screenshot(path=screenshot_path, full_page=True)
                    
                    # Find links
                    links = page.eval_on_selector_all('a[href]', 'els => els.map(e => e.href)')
                    
                    # Add new links to queue
                    for link in links:
                        if link and link not in visited:
                            to_visit.append(link)
                    
                    pages.append({
                        'url': current_url,
                        'title': title,
                        'screenshot_path': screenshot_path,
                        'links_found': len(links),
                    })
                    
                except Exception as e:
                    logger.warning(f"Failed to crawl {current_url}: {e}")
                    pages.append({
                        'url': current_url,
                        'title': None,
                        'error': str(e),
                    })
            
            b.close()
        
        return CrawlResult(
            base_url=url,
            success=True,
            pages_crawled=len(pages),
            pages=pages,
        )
    
    except Exception as e:
        return CrawlResult(
            base_url=url,
            success=False,
            error=str(e),
        )


def list_elements(
    url: str,
    element_type: str = "button",
    timeout: float = 30.0,
    browser: BrowserType = "firefox",
) -> dict:
    """
    List interactive elements on a page.
    
    Args:
        url: The URL to analyze
        element_type: Type of elements to find (button, link, input, form, all)
        timeout: Page load timeout
        browser: Browser to use (firefox, chromium, webkit)
    
    Returns:
        Dict with elements found
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {"success": False, "error": "playwright not installed"}
    
    selectors = {
        "button": "button, [role='button'], input[type='button'], input[type='submit']",
        "link": "a[href]",
        "input": "input, textarea, select",
        "form": "form",
        "all": "button, a[href], input, textarea, select, [role='button']",
    }
    
    selector = selectors.get(element_type, element_type)
    
    try:
        with sync_playwright() as p:
            b = _launch_browser(p, browser)
            page = b.new_page(viewport={'width': 1280, 'height': 720})
            page.goto(url, wait_until='networkidle', timeout=timeout * 1000)
            
            elements = page.eval_on_selector_all(
                selector,
                '''els => els.map(e => ({
                    tag: e.tagName.toLowerCase(),
                    text: e.innerText?.slice(0, 100) || '',
                    id: e.id || null,
                    class: e.className || null,
                    type: e.type || null,
                    href: e.href || null,
                    name: e.name || null,
                    value: e.value?.slice(0, 50) || null,
                }))'''
            )
            
            b.close()
            
            return {
                "success": True,
                "url": url,
                "element_type": element_type,
                "count": len(elements),
                "elements": elements,
            }
    
    except Exception as e:
        return {"success": False, "error": str(e)}


# Convenience aliases for LLM-friendly naming
fetch = fetch_url
screenshot = screenshot_url
check = check_local_access
interact = interact_with_page
crawl = crawl_site
list_ui = list_elements
