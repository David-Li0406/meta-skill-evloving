"""DOI scraper client for fetching abstracts from publisher pages."""

from __future__ import annotations

import logging
import re
import urllib.error
import urllib.request
from html import unescape
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from collections.abc import Callable

logger = logging.getLogger(__name__)

# Browser-like user agent to avoid blocking
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


class DOIScraperClient:
    """Scrapes abstracts from publisher pages by following DOI redirects.

    This is a fallback for when APIs (CrossRef, OpenAlex) don't have abstracts.
    Abstracts are typically visible on publisher pages even for paywalled articles.

    Currently supports:
    - ScienceDirect (Elsevier) - 10.1016/*
    - Springer/Nature - 10.1007/*, 10.1038/*
    - Wiley - 10.1002/*
    - IEEE - 10.1109/*
    - ACM - 10.1145/*
    - JMLR - jmlr.org
    - Generic fallback using og:description meta tag

    Known limitations (bot protection):
    - SPIE (10.1117) - Incapsula
    - Oxford (10.1093) - Cloudflare
    - ASCE (10.1061) - Cloudflare
    - Taylor & Francis (10.1080) - 403 Forbidden
    """

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

        # Publisher-specific parsers keyed by DOI prefix
        self._parsers: dict[str, Callable[[str], str | None]] = {
            "10.1016": self._parse_sciencedirect,  # Elsevier
            "10.1007": self._parse_springer,        # Springer
            "10.1038": self._parse_nature,          # Nature
            "10.1002": self._parse_wiley,           # Wiley
            "10.1109": self._parse_ieee,            # IEEE
            "10.1145": self._parse_acm,             # ACM
            "10.5555": self._parse_jmlr_or_acm,     # JMLR or ACM alternate
        }

    def get_abstract(self, doi: str) -> str | None:
        """Fetch abstract by scraping the publisher page.

        Args:
            doi: DOI (e.g., "10.1016/j.example.2025.123456")

        Returns:
            Abstract text if found, None otherwise
        """
        # Normalize DOI
        clean_doi = doi
        if doi.startswith('https://doi.org/'):
            clean_doi = doi[16:]
        elif doi.startswith('http://doi.org/'):
            clean_doi = doi[15:]

        # Get the publisher page HTML
        html = self._fetch_publisher_page(clean_doi)
        if not html:
            return None

        # Find appropriate parser based on DOI prefix
        prefix = clean_doi.split('/')[0] if '/' in clean_doi else None
        parser = self._parsers.get(prefix, self._parse_generic) if prefix else self._parse_generic

        try:
            abstract = parser(html)
            if abstract:
                # Clean up the abstract
                abstract = self._clean_abstract(abstract)
                if len(abstract) > 50:  # Sanity check - abstracts should be substantial
                    return abstract
        except Exception as e:
            logger.debug("Parse error for %s: %s", doi, e)

        # Fallback to generic parser if specific parser failed
        if parser != self._parse_generic:
            try:
                abstract = self._parse_generic(html)
                if abstract:
                    abstract = self._clean_abstract(abstract)
                    if len(abstract) > 50:
                        return abstract
            except Exception as e:
                logger.debug("Generic parse error for %s: %s", doi, e)

        return None

    def _fetch_publisher_page(self, doi: str) -> str | None:
        """Fetch the publisher page by following DOI redirect."""
        url = f"https://doi.org/{doi}"

        req = urllib.request.Request(url)
        req.add_header('User-Agent', BROWSER_USER_AGENT)
        req.add_header('Accept', 'text/html,application/xhtml+xml')
        req.add_header('Accept-Language', 'en-US,en;q=0.9')

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                # Check if we got redirected to a JS-only page
                html = resp.read().decode('utf-8', errors='ignore')

                # Handle Elsevier's intermediate redirect page
                if 'sciencedirect.com' in resp.url or 'elsevier' in resp.url.lower():
                    # Check for meta refresh or JS redirect
                    pii_match = re.search(r'pii/([A-Z0-9]+)', resp.url) or \
                                re.search(r'identifierValue\s*:\s*[\'"]([A-Z0-9]+)[\'"]', html)
                    if pii_match:
                        pii = pii_match.group(1)
                        return self._fetch_sciencedirect_direct(pii)

                return html

        except urllib.error.HTTPError as e:
            logger.debug("HTTP error fetching %s: %s", doi, e.code)
            return None
        except urllib.error.URLError as e:
            logger.debug("URL error fetching %s: %s", doi, e.reason)
            return None
        except Exception as e:
            logger.debug("Error fetching %s: %s", doi, e)
            return None

    def _fetch_sciencedirect_direct(self, pii: str) -> str | None:
        """Fetch ScienceDirect page directly using PII."""
        url = f"https://www.sciencedirect.com/science/article/pii/{pii}"

        req = urllib.request.Request(url)
        req.add_header('User-Agent', BROWSER_USER_AGENT)
        req.add_header('Accept', 'text/html,application/xhtml+xml')

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return resp.read().decode('utf-8', errors='ignore')
        except Exception as e:
            logger.debug("Error fetching ScienceDirect PII %s: %s", pii, e)
            return None

    def _parse_sciencedirect(self, html: str) -> str | None:
        """Parse abstract from ScienceDirect (Elsevier) page."""
        # Find all abstract-like divs and filter
        patterns = [
            r'<div[^>]*class="Abstracts[^"]*"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*abstract[^"]*"[^>]*>(.*?)</div>',
            r'<section[^>]*class="[^"]*abstract[^"]*"[^>]*>(.*?)</section>',
        ]

        candidates: list[str] = []
        for pattern in patterns:
            for match in re.finditer(pattern, html, re.DOTALL | re.IGNORECASE):
                text = self._strip_html_tags(match.group(1))
                # Remove "Abstract" prefix if present
                text = re.sub(r'^Abstract\s*', '', text, flags=re.IGNORECASE)
                # Skip if this is actually "Highlights" section
                if text.startswith('Highlights') or text.startswith('•'):
                    continue
                if text and len(text) > 50:
                    candidates.append(text)

        # Return the longest candidate (real abstracts are longer than snippets)
        if candidates:
            return cast("str", max(candidates, key=len))

        return None

    def _parse_springer(self, html: str) -> str | None:
        """Parse abstract from Springer page."""
        patterns = [
            r'<section[^>]*class="[^"]*Abstract[^"]*"[^>]*>(.*?)</section>',
            r'<div[^>]*id="Abs1-content"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*c-article-section__content[^"]*"[^>]*>(.*?)</div>',
        ]

        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
            if match:
                text = self._strip_html_tags(match.group(1))
                text = re.sub(r'^Abstract\s*', '', text, flags=re.IGNORECASE)
                if text and len(text) > 50:
                    return text

        return None

    def _parse_nature(self, html: str) -> str | None:
        """Parse abstract from Nature page."""
        patterns = [
            r'<div[^>]*id="Abs1-content"[^>]*>(.*?)</div>',
            r'<div[^>]*class="[^"]*c-article-section__content[^"]*"[^>]*>(.*?)</div>',
            r'<section[^>]*aria-labelledby="abstract"[^>]*>(.*?)</section>',
        ]

        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
            if match:
                text = self._strip_html_tags(match.group(1))
                if text and len(text) > 50:
                    return text

        return None

    def _parse_wiley(self, html: str) -> str | None:
        """Parse abstract from Wiley page."""
        patterns = [
            r'<section[^>]*class="[^"]*article-section--abstract[^"]*"[^>]*>(.*?)</section>',
            r'<div[^>]*class="[^"]*abstract-group[^"]*"[^>]*>(.*?)</div>',
        ]

        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
            if match:
                text = self._strip_html_tags(match.group(1))
                text = re.sub(r'^Abstract\s*', '', text, flags=re.IGNORECASE)
                if text and len(text) > 50:
                    return text

        return None

    def _parse_ieee(self, html: str) -> str | None:
        """Parse abstract from IEEE page."""
        # IEEE often uses JSON-LD or specific divs
        patterns = [
            r'"abstract"\s*:\s*"([^"]+)"',
            r'<div[^>]*class="[^"]*abstract-text[^"]*"[^>]*>(.*?)</div>',
        ]

        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
            if match:
                text = match.group(1)
                if '<' in text:  # HTML content
                    text = self._strip_html_tags(text)
                if text and len(text) > 50:
                    return text

        return None

    def _parse_acm(self, html: str) -> str | None:
        """Parse abstract from ACM Digital Library page."""
        patterns = [
            r'<section[^>]*class="[^"]*abstract[^"]*"[^>]*>(.*?)</section>',
            r'<div[^>]*class="[^"]*abstractSection[^"]*"[^>]*>(.*?)</div>',
            r'<p[^>]*class="[^"]*abstract[^"]*"[^>]*>(.*?)</p>',
        ]

        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
            if match:
                text = self._strip_html_tags(match.group(1))
                if text and len(text) > 50:
                    return text

        return None

    def _parse_jmlr_or_acm(self, html: str) -> str | None:
        """Parse abstract from JMLR or ACM page (10.5555 DOIs)."""
        # Check if this is a JMLR page
        if 'jmlr.org' in html.lower():
            return self._parse_jmlr(html)
        # Otherwise try ACM parser
        return self._parse_acm(html)

    def _parse_jmlr(self, html: str) -> str | None:
        """Parse abstract from JMLR page."""
        # JMLR has a simple structure: <h3>Abstract</h3> followed by the abstract text
        patterns = [
            r'<h3>Abstract</h3>\s*(.*?)</div>',
            r'<h3>Abstract</h3>\s*<p>(.*?)</p>',
            r'class="abstract"[^>]*>(.*?)</div>',
        ]

        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
            if match:
                text = self._strip_html_tags(match.group(1))
                if text and len(text) > 50:
                    return text

        return None

    def get_abstract_by_dblp_key(self, dblp_key: str) -> str | None:
        """Fetch abstract from JMLR using DBLP key.

        Args:
            dblp_key: DBLP key like "journals/jmlr/SrivastavaHKSS14"

        Returns:
            Abstract text if found, None otherwise
        """
        if not dblp_key or not dblp_key.startswith('journals/jmlr/'):
            return None

        # Fetch DBLP record to get volume and author info
        try:
            dblp_url = f"https://dblp.org/rec/{dblp_key}.xml"
            req = urllib.request.Request(dblp_url)
            req.add_header('User-Agent', BROWSER_USER_AGENT)

            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                xml_data = resp.read().decode('utf-8')

            # Parse volume and first author from XML
            volume_match = re.search(r'<volume>(\d+)</volume>', xml_data)
            author_match = re.search(r'<author>([^<]+)</author>', xml_data)
            year_match = re.search(r'<year>(\d+)</year>', xml_data)

            if not (volume_match and author_match and year_match):
                return None

            volume = volume_match.group(1)
            # JMLR uses last name - get last word of author name
            first_author = author_match.group(1).split()[-1].lower()
            year = year_match.group(1)[-2:]  # Last 2 digits

            # Try common letter suffixes (a, b, c)
            for letter in ['a', 'b', 'c', 'd', 'e', '']:
                jmlr_url = f"https://www.jmlr.org/papers/v{volume}/{first_author}{year}{letter}.html"
                abstract = self.get_abstract_from_jmlr_url(jmlr_url)
                if abstract:
                    return abstract

        except Exception as e:
            logger.debug("Error fetching DBLP record %s: %s", dblp_key, e)

        return None

    def search_dblp_for_jmlr(self, title: str) -> str | None:
        """Search DBLP for a paper and fetch abstract if it's from JMLR.

        Args:
            title: Paper title to search for

        Returns:
            Abstract text if found on JMLR, None otherwise
        """
        try:
            import json
            # Search DBLP
            search_url = f"https://dblp.org/search/publ/api?q={urllib.parse.quote(title)}&format=json&h=1"
            req = urllib.request.Request(search_url)
            req.add_header('User-Agent', BROWSER_USER_AGENT)

            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode('utf-8'))

            hits = data.get('result', {}).get('hits', {}).get('hit', [])
            if not hits:
                return None

            info = hits[0].get('info', {})
            dblp_url = info.get('url', '')

            # Check if it's a JMLR paper
            if 'journals/jmlr/' in dblp_url:
                dblp_key = dblp_url.replace('https://dblp.org/rec/', '')
                return self.get_abstract_by_dblp_key(dblp_key)

        except Exception as e:
            logger.debug("Error searching DBLP for %s: %s", title, e)

        return None

    def get_abstract_from_jmlr_url(self, url: str) -> str | None:
        """Fetch abstract directly from a JMLR URL."""
        if 'jmlr.org' not in url:
            return None

        req = urllib.request.Request(url)
        req.add_header('User-Agent', BROWSER_USER_AGENT)

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                return self._parse_jmlr(html)
        except Exception as e:
            logger.debug("Error fetching JMLR URL %s: %s", url, e)
            return None

    def _parse_generic(self, html: str) -> str | None:
        """Generic parser using common meta tags."""
        # Try various meta tags that commonly contain abstracts
        patterns = [
            r'<meta[^>]*name="description"[^>]*content="([^"]+)"',
            r'<meta[^>]*content="([^"]+)"[^>]*name="description"',
            r'<meta[^>]*property="og:description"[^>]*content="([^"]+)"',
            r'<meta[^>]*content="([^"]+)"[^>]*property="og:description"',
            r'<meta[^>]*name="DC\.description"[^>]*content="([^"]+)"',
            r'<meta[^>]*name="citation_abstract"[^>]*content="([^"]+)"',
        ]

        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                text = match.group(1)
                # Skip if truncated (ends with ...)
                if text.endswith('…') or text.endswith('...'):
                    continue
                if text and len(text) > 100:
                    return text

        return None

    def _strip_html_tags(self, text: str) -> str:
        """Remove HTML tags from text."""
        # Remove script and style elements
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
        # Remove all HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        # Unescape HTML entities
        text = unescape(text)
        return text

    def _clean_abstract(self, text: str) -> str:
        """Clean up extracted abstract text."""
        # Normalize whitespace
        text = ' '.join(text.split())
        # Remove common prefixes
        text = re.sub(r'^(Abstract|Summary|ABSTRACT|SUMMARY)[:\s]*', '', text)
        # Remove trailing "Read more" or similar
        text = re.sub(r'\s*(Read more|Show more|\.\.\.|\…)\s*$', '', text)
        return text.strip()
