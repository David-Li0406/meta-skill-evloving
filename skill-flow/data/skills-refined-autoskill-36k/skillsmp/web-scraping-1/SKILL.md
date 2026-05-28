---
name: web-scraping
description: Efficient web scraping patterns for data extraction from websites and APIs. Use when scraping content, fetching structured data, building ETL connectors, or processing web responses. Key principle - use programmatic extraction with uv scripts instead of reading raw HTML into context.
---

# Efficient Web Scraping

Extract data from websites efficiently using Python scripts. Never bloat context by reading raw HTML/JSON directly.

## Core Principle

### Programmatic extraction > Reading thousands of lines

| Approach                      | Tokens  | Quality   | Speed |
| ----------------------------- | ------- | --------- | ----- |
| Read raw HTML into context    | 50,000+ | Poor      | Slow  |
| Script + structured output    | ~200    | Excellent | Fast  |

## When This Applies

- Building ETL connectors (VA.gov, CareerOneStop, etc.)
- Scraping resource provider websites
- Fetching API responses
- Processing RSS/JSON feeds
- Crawling multiple pages

## The Pattern

### 1. Identify Target Data

Before writing code, specify exactly what you need:

```markdown
**Target**: VA.gov facility data
**Fields needed**: name, address, phone, services, hours
**Output format**: JSON matching ResourceCandidate schema
```

### 2. Write a Python Script

Create a script with proper error handling:

```python
#!/usr/bin/env python3
"""
Extract resource data from [target].
Output: Structured JSON to stdout matching ResourceCandidate.
"""
import json
import sys
import requests
from bs4 import BeautifulSoup

def extract_data(url: str) -> dict:
    """Extract target fields from URL."""
    response = requests.get(url, headers={
        "User-Agent": "Vibe4Vets Resource Aggregator (research)"
    })
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    # Extract ONLY the fields you need
    return {
        "name": soup.find("h1").get_text(strip=True) if soup.find("h1") else None,
        "description": soup.find("meta", {"name": "description"})["content"]
                       if soup.find("meta", {"name": "description"}) else None,
        "phone": extract_phone(soup),
        "address": extract_address(soup),
    }

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else None
    if not url:
        print("Usage: script.py <url>", file=sys.stderr)
        sys.exit(1)

    result = extract_data(url)
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

### 3. Run and Use Output

```bash
python script.py "https://example.com/page" > output.json
```

Then read only the small JSON output (~200 tokens) instead of the full page (~50,000 tokens).

## Vibe4Vets Connector Pattern

### Connector Interface

All connectors must implement the base interface:

```python
# backend/connectors/base.py
from typing import Protocol
from app.models.resource import ResourceCandidate

class Connector(Protocol):
    """Base connector interface."""

    def run(self) -> list[ResourceCandidate]:
        """Fetch and return resource candidates."""
        ...

    def metadata(self) -> dict:
        """Return connector metadata (source tier, name, etc.)."""
        ...
```

### Example: VA.gov Connector

```python
# backend/connectors/va_gov.py
import requests
from typing import Optional
from app.models.resource import ResourceCandidate
from app.core.taxonomy import CATEGORIES

class VAGovConnector:
    """Connector for VA.gov Lighthouse API."""

    BASE_URL = "https://api.va.gov/services/va_facilities/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "apikey": api_key,
            "Accept": "application/json",
        })

    def run(self) -> list[ResourceCandidate]:
        """Fetch VA facilities and convert to ResourceCandidates."""
        candidates = []

        for facility in self._fetch_facilities():
            candidate = self._to_candidate(facility)
            if candidate:
                candidates.append(candidate)

        return candidates

    def _fetch_facilities(self, state: Optional[str] = None):
        """Fetch facilities from VA API."""
        params = {"per_page": 100}
        if state:
            params["state"] = state

        response = self.session.get(f"{self.BASE_URL}/facilities", params=params)
        response.raise_for_status()

        data = response.json()
        return data.get("data", [])

    def _to_candidate(self, facility: dict) -> Optional[ResourceCandidate]:
        """Convert VA facility to ResourceCandidate."""
        attrs = facility.get("attributes", {})
        address = attrs.get("address", {}).get("physical", {})

        return ResourceCandidate(
            name=attrs.get("name"),
            description=self._build_description(attrs),
            category=self._map_category(attrs.get("facility_type")),
            phone=attrs.get("phone", {}).get("main"),
            website=attrs.get("website"),
            address_line1=address.get("address_1"),
            city=address.get("city"),
            state=address.get("state"),
            zip_code=address.get("zip"),
            source_url=f"https://www.va.gov/find-locations/facility/{facility.get('id')}",
            source_id=facility.get("id"),
        )

    def _map_category(self, facility_type: str) -> str:
        """Map VA facility type to our categories."""
        mapping = {
            "va_benefits_facility": "employment",
            "vet_center": "legal",
            "va_health_facility": "housing",  # Many offer SSVF
        }
        return mapping.get(facility_type, "employment")

    def metadata(self) -> dict:
        return {
            "name": "VA.gov Lighthouse API",
            "tier": 1,  # Official government source
            "reliability_score": 1.0,
        }
```

### Example: Web Scraping Connector

```python
# backend/connectors/state_agency.py
import requests
from bs4 import BeautifulSoup
from app.models.resource import ResourceCandidate

class StateVeteranAgencyConnector:
    """Scrape state veteran agency websites."""

    def __init__(self, state: str, url: str):
        self.state = state
        self.url = url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Vibe4Vets Resource Aggregator"
        })

    def run(self) -> list[ResourceCandidate]:
        """Scrape and return resource candidates."""
        response = self.session.get(self.url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        candidates = []

        for item in soup.select(".resource-item"):
            candidate = self._parse_item(item)
            if candidate:
                candidates.append(candidate)

        return candidates

    def _parse_item(self, item) -> Optional[ResourceCandidate]:
        """Parse a single resource item from HTML."""
        name = item.select_one("h3")
        if not name:
            return None

        return ResourceCandidate(
            name=name.get_text(strip=True),
            description=item.select_one(".description").get_text(strip=True)
                        if item.select_one(".description") else None,
            phone=self._extract_phone(item),
            website=item.select_one("a.website")["href"]
                    if item.select_one("a.website") else None,
            state=self.state,
            source_url=self.url,
        )

    def _extract_phone(self, item) -> Optional[str]:
        """Extract phone number from item."""
        phone_el = item.select_one(".phone")
        if not phone_el:
            return None

        import re
        phone_text = phone_el.get_text()
        match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', phone_text)
        return match.group() if match else None

    def metadata(self) -> dict:
        return {
            "name": f"{self.state} Veteran Agency",
            "tier": 3,  # State agency
            "reliability_score": 0.6,
        }
```

## Best Practices

### DO
- **Specify exact fields needed** before writing script
- **Limit results** (e.g., `[:100]`, pagination)
- **Output structured JSON** matching ResourceCandidate schema
- **Handle errors gracefully** with try/except
- **Add rate limiting** for multiple requests
- **Use CSS selectors** not regex for HTML
- **Include source URL** for traceability

### DON'T
- Read full page HTML into context
- Fetch data you won't use
- Skip error handling
- Make unlimited requests
- Parse HTML with regex
- Ignore robots.txt on production

## Error Handling

```python
try:
    result = extract_data(url)
    print(json.dumps(result, indent=2))
except requests.exceptions.HTTPError as e:
    print(json.dumps({
        "error": f"HTTP {e.response.status_code}",
        "url": url
    }))
    sys.exit(1)
except Exception as e:
    print(json.dumps({
        "error": str(e),
        "type": type(e).__name__
    }))
    sys.exit(1)
```

## Token Savings Example

| Scenario                 | Without Script | With Script |
| ------------------------ | -------------- | ----------- |
| VA.gov facility page     | ~45,000 tokens | ~150 tokens |
| State agency listing     | ~30,000 tokens | ~800 tokens |
| API response (100 items) | ~20,000 tokens | ~500 tokens |

**10-100x token reduction** = faster, cheaper, better context for reasoning.

## Quick Checklist

- [ ] Define exactly what fields are needed
- [ ] Write Python script with proper imports
- [ ] Extract ONLY needed fields
- [ ] Output structured JSON matching ResourceCandidate
- [ ] Run script, read JSON output (not raw HTML)
- [ ] Handle errors gracefully
- [ ] Include source metadata for trust scoring
