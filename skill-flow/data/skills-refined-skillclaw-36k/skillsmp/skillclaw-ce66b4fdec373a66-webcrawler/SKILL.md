---
name: webcrawler
description: Use this skill when you need to crawl documentation websites and extract structured content about specific subjects to build offline knowledge bases or organize technical documentation.
---

# Webcrawler Skill

Intelligent documentation harvesting agent that recursively crawls documentation websites and extracts structured content about specific subjects.

> **Last Updated:** 2026-01-23

---

## Quick Start

```bash
# Crawl Python documentation about async/await
python skills/webcrawler/scripts/crawl_docs.py \
  --url "https://docs.python.org/3/library/asyncio.html" \
  --subject "asyncio" \
  --depth 2 \
  --output .tmp/docs/python-asyncio/

# Crawl AWS EKS documentation
python skills/webcrawler/scripts/crawl_docs.py \
  --url "https://docs.aws.amazon.com/eks/latest/userguide/" \
  --subject "EKS" \
  --depth 3 \
  --output .tmp/docs/aws-eks/

# Extract only API reference pages
python skills/webcrawler/scripts/crawl_docs.py \
  --url "https://developer.hashicorp.com/consul/api-docs" \
  --subject "Consul API" \
  --filter "api" \
  --output .tmp/docs/consul-api/
```

---

## Core Workflow

1. **Initialize Crawl** — Provide base URL and subject focus.
2. **Discover Pages** — Recursively find all linked documentation pages.
3. **Filter Content** — Keep only pages matching the subject criteria.
4. **Extract Content** — Convert HTML to clean markdown.
5. **Organize Output** — Structure files in a navigable hierarchy.
6. **Generate Index** — Create a master index with all harvested pages.

---

## Scripts

### `crawl_docs.py` — Main Documentation Crawler

The primary crawling script that handles recursive page discovery and content extraction.

```bash
python skills/webcrawler/scripts/crawl_docs.py \
  --url <base-url>           # Starting URL (required)
  --subject <topic>          # Subject focus for filtering (required)
  --output <directory>       # Output directory (default: .tmp/crawled/)
  --depth <n>                # Max crawl depth (default: 2)
  --filter <pattern>         # URL path filter pattern (optional)
  --delay <seconds>          # Delay between requests (default: 0.5)
```