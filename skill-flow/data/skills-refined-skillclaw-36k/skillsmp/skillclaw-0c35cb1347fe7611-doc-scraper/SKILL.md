---
name: doc-scraper
description: Use this skill when you need to scrape documentation websites into organized reference files for searchable access or to build Claude skills.
---

# Documentation Scraper Skill

## Purpose

Single responsibility: Convert documentation websites into organized, categorized reference files suitable for Claude skills or offline archives.

## Grounding Checkpoint

Before executing, VERIFY:

- [ ] Target URL is accessible (test with `curl -I`)
- [ ] Documentation structure is identifiable (inspect page for content selectors)
- [ ] Output directory is writable
- [ ] Rate limiting requirements are known (check robots.txt)

**DO NOT proceed without verification. Inspect before scraping.**

## Uncertainty Escalation

ASK USER instead of guessing when:

- Content selector is ambiguous (multiple `<article>` or `<main>` elements)
- URL patterns unclear (can't determine include/exclude rules)
- Category mapping uncertain (content doesn't fit predefined categories)
- Rate limiting unknown (no robots.txt, unclear ToS)

**NEVER substitute missing configuration with assumptions.**

## Context Scope

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | Target URL, selectors, output path | Unrelated documentation |
| PERIPHERAL | Similar site examples for selector hints | Historical scrape data |
| DISTRACTOR | Other projects, unrelated URLs | Previous failed attempts |

## Workflow Steps

### Step 1: Verify Target

```bash
# Test URL accessibility
curl -I <target-url>

# Check robots.txt
curl <base-url>/robots.txt

# Inspect page structure (use browser dev tools or fetch sample)
```

### Step 2: Create Configuration

Generate scraper config based on inspection:

```json
{
  "name": "skill-name",
  "description": "When to use this skill",
  "base_url": "https://docs.example.com/",
  "selectors": {
    "main_content": "article",
    "title": "h1",
    "code_blocks": "pre code"
  },
  "url_patterns": {
    "include": ["/docs", "/guide", "/api"],
    "exclude": ["/blog", "/changelog", "/releases"]
  },
  "categories": {
    "getting_started": ["intro", "quickstart", "installation"],
    "api_reference": ["api", "reference", "methods"],
    "guides": ["guide", "tutorial", "how-to"]
  },
  "rate_limit": 0.5,
  "max_pages": 500
}
```

### Step 3: Execute Scraping

**Option A: With skill-seekers (if installed)**

...