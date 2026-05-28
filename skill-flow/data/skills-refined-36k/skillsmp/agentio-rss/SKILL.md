---
name: agentio-rss
description: Use when reading RSS/Atom feeds - list articles, get article content, or get feed info from any blog URL. Auto-discovers feed URLs from blog home pages.
---

# RSS Feed Operations with agentio

Use `agentio rss` commands to read RSS/Atom feeds. Just provide a blog URL - the feed will be auto-discovered.

## List Articles

```bash
agentio rss articles <url> [--limit N] [--since YYYY-MM-DD]
```

Options:
- `--limit <n>`: Number of articles (default: 20)
- `--since <date>`: Only articles after this date

Examples:
```bash
agentio rss articles https://simonwillison.net --limit 5
agentio rss articles https://steipete.me --since 2025-01-01
```

## Get Article Content

```bash
agentio rss get <url> <article-id>
```

The article-id can be the article URL or GUID from the articles list.

Example:
```bash
agentio rss get https://blog.fsck.com https://blog.fsck.com/2025/12/27/streamlinear/
```

## Get Feed Info

```bash
agentio rss info <url>
```

Shows feed title, description, discovered feed URL, and article count.

Example:
```bash
agentio rss info https://kau.sh
```

## Feed Auto-Discovery

The URL can be:
- A blog home page (e.g., `https://simonwillison.net`)
- A direct feed URL (e.g., `https://example.com/feed.xml`)

Auto-discovery checks:
1. HTML `<link rel="alternate">` tags
2. Common paths: `/feed`, `/feed.xml`, `/rss.xml`, `/atom.xml`, `/index.xml`
