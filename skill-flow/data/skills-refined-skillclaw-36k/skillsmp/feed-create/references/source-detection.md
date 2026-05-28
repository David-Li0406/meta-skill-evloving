# Source Type Detection

URL → source type detection rules for feed-create discovery mode.

## Detection Flow

```
1. Parse URL
2. Check domain patterns (reddit, github, known sites)
3. Fetch HTML head
4. Check RSS autodiscovery tags
5. Parse content for feed hints
6. Fallback to generic scraper
```

## URL Pattern Rules

| Pattern | Source Type | Confidence |
|---------|-------------|------------|
| `reddit.com/r/{sub}` | reddit | 100% |
| `github.com/{owner}/{repo}/issues` | github | 100% |
| `*/feed.xml`, `*/rss`, `*/atom` | rss | 100% |
| `*.wordpress.com/*` | rss (autodiscover) | 90% |
| `*.substack.com/*` | rss (autodiscover) | 90% |
| `*.medium.com/*` | rss (autodiscover) | 80% |

## RSS Autodiscovery

Check HTML `<head>` for alternate link tags:

```html
<link rel="alternate" type="application/rss+xml" href="/feed.xml">
<link rel="alternate" type="application/atom+xml" href="/atom.xml">
```

**Detection logic:**
```typescript
const rssLink = doc.querySelector('link[rel="alternate"][type*="rss"]');
const atomLink = doc.querySelector('link[rel="alternate"][type*="atom"]');
return rssLink?.href || atomLink?.href;
```

## Reddit Detection

### Subreddit patterns

| URL Format | Feed URL |
|------------|----------|
| `https://reddit.com/r/soccer` | Use Reddit API |
| `https://reddit.com/r/soccer/.rss` | Direct RSS |
| `https://old.reddit.com/r/soccer` | Use Reddit API |

**Config generation:**
```yaml
source:
  type: reddit
  subreddit: soccer  # Extract from URL
  sort: top
  period: day
```

### Comment thread patterns

| URL Format | Handling |
|------------|----------|
| `/comments/{id}` | Single post + comments |
| `/user/{name}` | User posts (use API) |

## GitHub Detection

### Repository patterns

| URL Format | Source Type | Config |
|------------|-------------|--------|
| `/{owner}/{repo}` | github | type: github, repo: owner/repo |
| `/{owner}/{repo}/issues` | github | type: github, repo: owner/repo, kind: issues |
| `/{owner}/{repo}/releases` | rss | Use releases.atom feed |

**Config generation:**
```yaml
source:
  type: github
  repo: owner/repo
  kind: issues  # or: releases, pulls
  labels: [bug, enhancement]  # Optional filter
```

## Blog Platform Detection

### Substack

All Substack blogs have RSS at `/feed`:

```
https://example.substack.com/ → https://example.substack.com/feed
```

**Config:**
```yaml
source: https://example.substack.com/feed
transform: [readability, sanitize_html]
```

### Medium

Medium RSS requires username:

```
https://medium.com/@username → https://medium.com/feed/@username
```

**Config:**
```yaml
source: https://medium.com/feed/@username
transform: [readability, sanitize_html]  # Removes paywalls
```

### WordPress

WordPress sites typically have `/feed/` or `/?feed=rss2`:

```
https://example.com/ → https://example.com/feed/
```

**Detection:**
- Check `<link>` autodiscovery first
- Fallback to `/feed/`
- Fallback to `/?feed=rss2`

## Personal Blog Detection

For unknown sites, probe common feed paths:

```bash
# Common feed locations (in order)
/feed.xml
/rss.xml
/atom.xml
/feed/
/rss/
/blog/feed.xml
/index.xml
```

**Detection script:**
```bash
for path in /feed.xml /rss.xml /atom.xml /feed/ /rss/ /blog/feed.xml /index.xml; do
  if curl -fsL "${URL}${path}" -I | grep -q "application/.*xml"; then
    echo "${URL}${path}"
    break
  fi
done
```

## Content Hints

Parse HTML for indicators:

| Signal | Source Type | Evidence |
|--------|-------------|----------|
| `<article>` tags | blog | Modern semantic HTML |
| Disqus/comments | blog | Likely has RSS |
| Date in permalink | blog | Time-series content |
| Archive page | blog | Historical posts |

## Fallback Strategy

If no feed detected:

```
1. Check robots.txt for sitemap.xml
2. Parse sitemap for blog posts
3. Generate feed from scraped content
4. Use generic URL scraper source type
```

**Config for fallback:**
```yaml
source:
  type: scraper
  url: https://example.com
  selector: article  # CSS selector for content
  pagination: a.next  # Next page link
```

## Decision Tree

```
Given URL, detect source:
├── Match reddit.com/r/* → reddit
├── Match github.com/*/* → github
├── Ends with /feed.xml, /rss, /atom → rss (direct)
├── HTML has <link rel="alternate" type="rss"> → rss (autodiscover)
├── Domain in known-sites.json → rss (lookup feed URL)
├── Probe common feed paths → rss (found)
└── No feed found → scraper (fallback)
```

## Metadata Extraction

After detecting source, extract metadata:

```typescript
interface DiscoveredFeed {
  url: string;
  sourceType: "rss" | "reddit" | "github" | "scraper";
  metadata: {
    title?: string;        // From <title> or feed
    description?: string;  // From meta description
    author?: string;       // From meta author
    icon?: string;         // Favicon URL
    language?: string;     // From <html lang>
  };
  suggested: {
    id: string;            // Slug from title/URL
    styleProfile: string;  // Inferred from content
    frequency: string;     // Based on archive
  };
}
```

## Content-Based Inference

Infer style profile from content:

| Signal | Style Profile | Confidence |
|--------|---------------|------------|
| 5+ code blocks in recent posts | technical | high |
| Technical keywords (API, function, class) | technical | medium |
| Long paragraphs, no code | narrative | high |
| Short posts, images | minimal | medium |

## Update Frequency Inference

Guess `select.since` from archive:

| Archive Pattern | Frequency | `since` |
|-----------------|-----------|---------|
| Daily posts | daily | 48h |
| 2-3x per week | regular | 7d |
| Weekly | weekly | 14d |
| Monthly | monthly | 30d |

## Known Sites Database

Maintain JSON of known blogs with feed URLs:

```json
{
  "simonwillison.net": {
    "feed": "https://simonwillison.net/atom/everything/",
    "style": "technical"
  },
  "craigmod.com": {
    "feed": "https://craigmod.com/essays/feed.xml",
    "style": "narrative"
  }
}
```

**Usage:**
```typescript
const knownSite = knownSites[domain];
if (knownSite) {
  return {
    url: knownSite.feed,
    sourceType: "rss",
    suggested: { styleProfile: knownSite.style }
  };
}
```

## Testing Detection

```bash
# Test URL detection
feed-create discover "https://simonwillison.net"

# Expected output:
# ✓ Detected: RSS feed
# URL: https://simonwillison.net/atom/everything/
# Title: Simon Willison's Weblog
# Style: technical (inferred from content)
# Frequency: weekly (2-3 posts/week)
```
