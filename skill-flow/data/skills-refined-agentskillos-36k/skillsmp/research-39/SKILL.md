---
name: research
description: Deep research within a specified domain. Use when the user wants to search a website comprehensively, gather information from multiple pages on a domain, or compile research from a specific site.
allowed-tools: Read, Bash, Write, Glob, Grep, WebFetch, WebSearch
---

# Domain Research Skill

Workflow guide for comprehensive research within a specified domain, gathering information from multiple pages and summarizing findings.

## Core Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│  YAML Config    │ ───▶ │    Discovery    │ ───▶ │   Collection    │ ───▶ │    Summary      │
│ (Domain/Goals)  │      │  (Find Pages)   │      │ (Gather Data)   │      │   (Report)      │
└─────────────────┘      └─────────────────┘      └─────────────────┘      └─────────────────┘
```

### Research Phases

| Phase | Purpose | Tools |
|-------|---------|-------|
| **Discovery** | Find relevant pages within domain | WebSearch, sitemap crawl |
| **Collection** | Extract content from discovered pages | WebFetch, Playwright |
| **Analysis** | Process and categorize information | Python scripts |
| **Summary** | Generate comprehensive report | Markdown/JSON output |

---

## Project Structure

```
projects/<research_project>/
├── configs/              # Research configuration
│   └── research.yaml
├── scripts/              # Execution scripts
│   ├── discover.py       # URL discovery
│   ├── collect.py        # Content collection
│   └── summarize.py      # Report generation
├── data/                 # Collected raw data
│   ├── pages/            # Cached page content
│   └── urls.json         # Discovered URLs
├── output/               # Final reports
│   ├── research_report.md
│   └── findings.json
└── docs/                 # Notes (optional)
```

---

## YAML Config: Define Research Scope

### Basic Structure

```yaml
version: "1.0"
name: "my_research"
description: "Research objectives and scope"

target:
  domain: "example.com"
  base_url: "https://example.com"
  scope:
    include_paths:
      - "/docs/*"
      - "/blog/*"
    exclude_paths:
      - "/admin/*"
      - "/login"
    max_depth: 3
    max_pages: 100

research:
  goals:
    - "Find all API documentation"
    - "Identify pricing information"
    - "Locate technical specifications"

  keywords:
    primary:
      - "API"
      - "pricing"
      - "integration"
    secondary:
      - "tutorial"
      - "example"
      - "guide"

  content_types:
    - documentation
    - blog_posts
    - product_pages

discovery:
  methods:
    - sitemap          # Check /sitemap.xml
    - robots           # Check /robots.txt for hints
    - search_engine    # Use WebSearch with site: operator
    - link_crawl       # Follow internal links

  search_queries:
    - "site:example.com API documentation"
    - "site:example.com pricing"
    - "site:example.com integration guide"

collection:
  extract:
    - title
    - main_content
    - headings
    - links
    - metadata

  filters:
    min_content_length: 200
    exclude_navigation: true
    exclude_footers: true

output:
  format: [markdown, json]
  path: "output/"
  include:
    - summary_report
    - page_index
    - key_findings
    - raw_data
```

### Config Sections

| Section | Purpose |
|---------|---------|
| `target` | Domain and scope constraints |
| `research` | Goals, keywords, content types |
| `discovery` | Methods for finding pages |
| `collection` | What to extract from pages |
| `output` | Report format and contents |

---

## Agent Workflow

### Phase 1: Configure Research

1. Create `configs/research.yaml` with target domain
2. Define research goals and keywords
3. Set scope constraints (paths, depth, max pages)

### Phase 2: Discovery

Use multiple methods to find relevant pages:

```python
#!/usr/bin/env python3
"""Discover pages within target domain."""

import yaml
import json
from urllib.parse import urljoin, urlparse
import requests

def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)

def check_sitemap(base_url):
    """Extract URLs from sitemap.xml."""
    urls = []
    sitemap_url = urljoin(base_url, '/sitemap.xml')
    try:
        resp = requests.get(sitemap_url, timeout=10)
        if resp.ok:
            # Parse sitemap XML for <loc> tags
            import re
            urls = re.findall(r'<loc>([^<]+)</loc>', resp.text)
    except Exception as e:
        print(f"Sitemap check failed: {e}")
    return urls

def search_domain(domain, queries):
    """Use search engine with site: operator."""
    # This would use WebSearch tool
    # Returns list of discovered URLs
    pass

def crawl_links(start_url, max_depth, max_pages, scope):
    """Crawl internal links within scope."""
    visited = set()
    to_visit = [(start_url, 0)]

    while to_visit and len(visited) < max_pages:
        url, depth = to_visit.pop(0)
        if depth > max_depth or url in visited:
            continue

        # Check scope
        if not is_in_scope(url, scope):
            continue

        visited.add(url)
        # Fetch page and extract internal links
        # Add new links with depth + 1

    return list(visited)

def main():
    config = load_config('configs/research.yaml')
    target = config['target']
    discovery = config['discovery']

    all_urls = set()

    # Method 1: Sitemap
    if 'sitemap' in discovery['methods']:
        all_urls.update(check_sitemap(target['base_url']))

    # Method 2: Search engine
    if 'search_engine' in discovery['methods']:
        for query in discovery.get('search_queries', []):
            # Use WebSearch tool
            pass

    # Method 3: Link crawling
    if 'link_crawl' in discovery['methods']:
        crawled = crawl_links(
            target['base_url'],
            target['scope']['max_depth'],
            target['scope']['max_pages'],
            target['scope']
        )
        all_urls.update(crawled)

    # Save discovered URLs
    with open('data/urls.json', 'w') as f:
        json.dump(list(all_urls), f, indent=2)

    print(f"Discovered {len(all_urls)} URLs")

if __name__ == '__main__':
    main()
```

### Phase 3: Collection

Collect content from discovered pages:

```python
#!/usr/bin/env python3
"""Collect content from discovered URLs."""

import yaml
import json
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib

def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)

def extract_content(html, config):
    """Extract relevant content from HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    collection = config['collection']

    # Remove navigation and footer if configured
    if collection['filters'].get('exclude_navigation'):
        for nav in soup.find_all(['nav', 'header']):
            nav.decompose()

    if collection['filters'].get('exclude_footers'):
        for footer in soup.find_all('footer'):
            footer.decompose()

    result = {}

    # Extract configured elements
    if 'title' in collection['extract']:
        title_tag = soup.find('title')
        result['title'] = title_tag.text.strip() if title_tag else ''

    if 'main_content' in collection['extract']:
        main = soup.find('main') or soup.find('article') or soup.find('body')
        result['content'] = main.get_text(separator='\n', strip=True) if main else ''

    if 'headings' in collection['extract']:
        result['headings'] = [h.text.strip() for h in soup.find_all(['h1','h2','h3','h4'])]

    if 'links' in collection['extract']:
        result['links'] = [a.get('href') for a in soup.find_all('a', href=True)]

    if 'metadata' in collection['extract']:
        result['metadata'] = {
            meta.get('name') or meta.get('property'): meta.get('content')
            for meta in soup.find_all('meta')
            if meta.get('content')
        }

    return result

def collect_pages(urls, config):
    """Collect content from all URLs."""
    collection_config = config['collection']
    min_length = collection_config['filters'].get('min_content_length', 0)

    pages = []
    for url in urls:
        # Use WebFetch or Playwright to get page
        # html = fetch_page(url)
        # content = extract_content(html, config)

        # Filter by content length
        # if len(content.get('content', '')) >= min_length:
        #     pages.append({'url': url, **content})
        pass

    return pages

def main():
    config = load_config('configs/research.yaml')

    # Load discovered URLs
    with open('data/urls.json') as f:
        urls = json.load(f)

    # Collect content
    pages = collect_pages(urls, config)

    # Save collected data
    Path('data/pages').mkdir(parents=True, exist_ok=True)
    with open('data/pages/collected.json', 'w') as f:
        json.dump(pages, f, indent=2)

    print(f"Collected content from {len(pages)} pages")

if __name__ == '__main__':
    main()
```

### Phase 4: Analysis & Summary

Generate comprehensive research report:

```python
#!/usr/bin/env python3
"""Analyze collected data and generate summary report."""

import yaml
import json
from pathlib import Path
from collections import Counter
import re

def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)

def analyze_content(pages, config):
    """Analyze collected pages against research goals."""
    research = config['research']
    keywords = research.get('keywords', {})
    goals = research.get('goals', [])

    analysis = {
        'total_pages': len(pages),
        'keyword_matches': {},
        'goal_findings': {goal: [] for goal in goals},
        'content_by_type': {},
        'key_topics': []
    }

    # Keyword frequency analysis
    all_keywords = keywords.get('primary', []) + keywords.get('secondary', [])
    for kw in all_keywords:
        matching_pages = [
            p for p in pages
            if kw.lower() in p.get('content', '').lower()
        ]
        analysis['keyword_matches'][kw] = {
            'count': len(matching_pages),
            'pages': [p['url'] for p in matching_pages[:5]]
        }

    # Extract key topics from headings
    all_headings = []
    for page in pages:
        all_headings.extend(page.get('headings', []))

    heading_counts = Counter(all_headings)
    analysis['key_topics'] = heading_counts.most_common(20)

    return analysis

def generate_report(analysis, config, pages):
    """Generate markdown research report."""
    target = config['target']
    research = config['research']

    report = f"""# Research Report: {target['domain']}

## Overview

- **Domain**: {target['domain']}
- **Pages Analyzed**: {analysis['total_pages']}
- **Research Goals**: {len(research.get('goals', []))}

## Research Goals

"""

    for goal in research.get('goals', []):
        findings = analysis['goal_findings'].get(goal, [])
        report += f"### {goal}\n\n"
        if findings:
            for finding in findings:
                report += f"- {finding}\n"
        else:
            report += "_No specific findings yet - manual review recommended_\n"
        report += "\n"

    report += """## Keyword Analysis

| Keyword | Matches | Sample Pages |
|---------|---------|--------------|
"""

    for kw, data in analysis['keyword_matches'].items():
        sample = ', '.join(data['pages'][:2]) if data['pages'] else '-'
        report += f"| {kw} | {data['count']} | {sample} |\n"

    report += """

## Key Topics Found

Based on page headings and content structure:

"""

    for topic, count in analysis['key_topics'][:15]:
        report += f"- **{topic}** ({count} occurrences)\n"

    report += """

## Page Index

| URL | Title | Keywords |
|-----|-------|----------|
"""

    for page in pages[:50]:
        title = page.get('title', 'Untitled')[:50]
        url = page.get('url', '')
        report += f"| {url} | {title} | - |\n"

    report += """

---
*Generated by Domain Research Skill*
"""

    return report

def main():
    config = load_config('configs/research.yaml')

    # Load collected data
    with open('data/pages/collected.json') as f:
        pages = json.load(f)

    # Analyze
    analysis = analyze_content(pages, config)

    # Generate report
    report = generate_report(analysis, config, pages)

    # Save outputs
    output_path = Path(config['output']['path'])
    output_path.mkdir(parents=True, exist_ok=True)

    with open(output_path / 'research_report.md', 'w') as f:
        f.write(report)

    with open(output_path / 'findings.json', 'w') as f:
        json.dump(analysis, f, indent=2)

    print(f"Report saved to {output_path / 'research_report.md'}")

if __name__ == '__main__':
    main()
```

---

## Discovery Methods

### 1. Sitemap Crawling

Check standard sitemap locations:
- `/sitemap.xml`
- `/sitemap_index.xml`
- `/sitemap/sitemap.xml`

### 2. Search Engine (site: operator)

Use WebSearch with domain restriction:
```
site:example.com "API documentation"
site:example.com pricing OR plans
site:example.com filetype:pdf
```

### 3. Robots.txt Analysis

Check `/robots.txt` for:
- Sitemap references
- Disallowed paths (often interesting content)
- Crawl-delay hints

### 4. Link Crawling

Follow internal links with constraints:
- Respect `max_depth`
- Stay within `include_paths`
- Avoid `exclude_paths`
- Deduplicate URLs

---

## Usage Examples

### Basic Domain Research

```yaml
# configs/research.yaml
version: "1.0"
name: "company_research"
description: "Research company website for product info"

target:
  domain: "acme.com"
  base_url: "https://www.acme.com"
  scope:
    max_depth: 2
    max_pages: 50

research:
  goals:
    - "Identify all products and services"
    - "Find pricing information"
    - "Locate contact and support info"

  keywords:
    primary: ["product", "pricing", "service"]
    secondary: ["support", "contact", "demo"]

discovery:
  methods: [sitemap, search_engine]
  search_queries:
    - "site:acme.com products"
    - "site:acme.com pricing"

output:
  format: [markdown, json]
  path: "output/"
```

### Technical Documentation Research

```yaml
version: "1.0"
name: "api_docs_research"
description: "Comprehensive API documentation research"

target:
  domain: "docs.example.com"
  base_url: "https://docs.example.com"
  scope:
    include_paths: ["/api/*", "/reference/*"]
    max_depth: 4
    max_pages: 200

research:
  goals:
    - "Map all API endpoints"
    - "Find authentication methods"
    - "Identify rate limits"
    - "Locate code examples"

  keywords:
    primary: ["endpoint", "authentication", "rate limit"]
    secondary: ["example", "tutorial", "SDK"]

discovery:
  methods: [sitemap, link_crawl]

collection:
  extract: [title, main_content, headings, metadata]
  filters:
    min_content_length: 100
    exclude_navigation: true

output:
  format: [markdown, json]
  path: "output/"
```

---

## Agent Execution Guide

When user requests domain research:

1. **Clarify scope**
   - Which domain to research?
   - What are the research goals?
   - Any specific keywords or topics?
   - Page/depth limits?

2. **Create config**
   - Generate `configs/research.yaml` with user's requirements

3. **Execute discovery**
   - Run sitemap check
   - Execute search queries using WebSearch
   - Optionally crawl links

4. **Collect content**
   - Fetch discovered pages using WebFetch
   - Extract relevant content

5. **Generate report**
   - Analyze content against goals
   - Create summary report
   - Save findings

---

## Important Rules

1. **Respect rate limits**: Add delays between requests
2. **Check robots.txt**: Respect crawl restrictions
3. **Stay in scope**: Don't crawl outside target domain
4. **Cache pages**: Save fetched content to avoid re-fetching
5. **Progressive updates**: Report findings as discovered
6. **Use virtual env**: `.venv/bin/python`
7. **Don't modify skill**: `.claude/skills/research/` is read-only
