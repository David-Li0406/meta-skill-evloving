#!/usr/bin/env python3
"""
Async Web Scraper Module - Parallel URL fetching with rate limiting

Phase 2 Enhancement: 병렬 스크래핑으로 5-10배 속도 향상
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Optional imports with fallback
_aiohttp_available = False
_bs4_available = False

try:
    import aiohttp
    _aiohttp_available = True
except ImportError:
    aiohttp = None

try:
    from bs4 import BeautifulSoup
    _bs4_available = True
except ImportError:
    BeautifulSoup = None


@dataclass
class FetchResult:
    """Result from fetching a single URL."""
    url: str
    content: str
    success: bool
    error: Optional[str] = None
    title: Optional[str] = None


class AsyncWebScraper:
    """Async web scraper with parallel fetching and rate limiting.
    
    Features:
    - Semaphore-based concurrency control
    - Configurable delay between requests
    - Graceful error handling for individual URLs
    """
    
    def __init__(
        self,
        max_concurrent: int = 5,
        delay: float = 0.5,
        timeout: int = 10
    ):
        """Initialize the async scraper.
        
        Args:
            max_concurrent: Maximum number of concurrent requests
            delay: Delay between requests in seconds (rate limiting)
            timeout: Request timeout in seconds
        """
        self.max_concurrent = max_concurrent
        self.delay = delay
        self.timeout = timeout
        self._semaphore: Optional[asyncio.Semaphore] = None
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    async def fetch_all(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Fetch multiple URLs in parallel.
        
        Args:
            urls: List of URLs to fetch
            
        Returns:
            List of result dictionaries with url, content, success, error keys
        """
        if not _aiohttp_available:
            logger.warning("aiohttp not installed, falling back to sync scraper")
            return self._sync_fallback(urls)
        
        self._semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async with aiohttp.ClientSession(
            headers=self.headers,
            timeout=aiohttp.ClientTimeout(total=self.timeout)
        ) as session:
            tasks = [self._fetch_with_limit(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert results to dicts
        output = []
        for url, result in zip(urls, results):
            if isinstance(result, Exception):
                output.append({
                    "url": url,
                    "content": "",
                    "success": False,
                    "error": str(result)
                })
            else:
                output.append(result)
        
        return output
    
    async def _fetch_with_limit(
        self,
        session: "aiohttp.ClientSession",
        url: str
    ) -> Dict[str, Any]:
        """Fetch a single URL with rate limiting.
        
        Args:
            session: aiohttp session
            url: URL to fetch
            
        Returns:
            Result dictionary
        """
        async with self._semaphore:
            # Rate limiting delay
            if self.delay > 0:
                await asyncio.sleep(self.delay)
            
            return await self._fetch_one(url, session)
    
    async def _fetch_one(
        self,
        url: str,
        session: Optional["aiohttp.ClientSession"] = None
    ) -> Dict[str, Any]:
        """Fetch and parse a single URL.
        
        Args:
            url: URL to fetch
            session: Optional aiohttp session
            
        Returns:
            Result dictionary with url, content, success, error
        """
        try:
            logger.info(f"Async fetching: {url}")
            
            if session is None:
                # Create a new session if not provided
                async with aiohttp.ClientSession(
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as new_session:
                    return await self._do_fetch(new_session, url)
            else:
                return await self._do_fetch(session, url)
                
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return {
                "url": url,
                "content": "",
                "success": False,
                "error": str(e)
            }
    
    async def _do_fetch(
        self,
        session: "aiohttp.ClientSession",
        url: str
    ) -> Dict[str, Any]:
        """Actually perform the fetch operation.
        
        Args:
            session: aiohttp session
            url: URL to fetch
            
        Returns:
            Result dictionary
        """
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    return {
                        "url": url,
                        "content": "",
                        "success": False,
                        "error": f"HTTP {response.status}"
                    }
                
                html = await response.text()
                
                # Parse with BeautifulSoup if available
                if _bs4_available and BeautifulSoup:
                    content = self._parse_html(html)
                else:
                    content = html[:5000]  # Raw HTML fallback
                
                return {
                    "url": url,
                    "content": content,
                    "success": True,
                    "error": None
                }
                
        except asyncio.TimeoutError:
            return {
                "url": url,
                "content": "",
                "success": False,
                "error": "Timeout"
            }
        except Exception as e:
            return {
                "url": url,
                "content": "",
                "success": False,
                "error": str(e)
            }
    
    def _parse_html(self, html: str) -> str:
        """Parse HTML and extract clean text.
        
        Args:
            html: Raw HTML string
            
        Returns:
            Cleaned text content
        """
        soup = BeautifulSoup(html, "html.parser")
        
        # Remove unwanted elements
        for tag in soup(
            ["script", "style", "nav", "footer", "header", "iframe", "noscript"]
        ):
            tag.decompose()
        
        # Extract text
        text = soup.get_text(separator="\n\n")
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = "\n".join(chunk for chunk in chunks if chunk)
        
        return text
    
    def _sync_fallback(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Synchronous fallback when aiohttp is not available.
        
        Args:
            urls: List of URLs to fetch
            
        Returns:
            List of result dictionaries
        """
        try:
            from scraper import WebScraper
            sync_scraper = WebScraper(timeout=self.timeout)
            
            results = []
            for url in urls:
                content = sync_scraper.fetch_content(url)
                results.append({
                    "url": url,
                    "content": content,
                    "success": bool(content),
                    "error": None if content else "Failed to fetch"
                })
            return results
            
        except Exception as e:
            logger.error(f"Sync fallback failed: {e}")
            return [
                {"url": url, "content": "", "success": False, "error": str(e)}
                for url in urls
            ]


def fetch_urls_parallel(
    urls: List[str],
    max_concurrent: int = 5,
    delay: float = 0.5
) -> List[Dict[str, Any]]:
    """Convenience function to fetch URLs in parallel.
    
    Args:
        urls: List of URLs to fetch
        max_concurrent: Maximum concurrent requests
        delay: Delay between requests
        
    Returns:
        List of result dictionaries
    """
    scraper = AsyncWebScraper(max_concurrent=max_concurrent, delay=delay)
    return asyncio.run(scraper.fetch_all(urls))
