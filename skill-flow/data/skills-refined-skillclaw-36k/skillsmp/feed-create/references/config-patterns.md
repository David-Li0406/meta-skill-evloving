# Feed Config Patterns

Common configuration recipes and shortcuts for feed-create.

## Quick Patterns

### Single-Source RSS

```yaml
version: 1
feeds:
  - id: blog-name
    source: https://example.com/feed.xml
```

Defaults applied:
- style: narrative
- select: { since: 48h, max_items: 25 }

### Multi-Source Aggregation

```yaml
version: 1
feeds:
  - id: tech-news
    title: "Tech News Roundup"
    sources:
      - https://hnrss.org/frontpage
      - https://lobste.rs/rss
      - https://news.ycombinator.com/rss
    select:
      since: 24h
      max_items: 50
```

### Reddit with Flair Filtering

```yaml
version: 1
feeds:
  - id: reddit-programming
    source:
      type: reddit
      subreddit: programming
    select:
      allow:
        - flair: ['Question', 'Project', 'Discussion']
```

## Style Patterns

### Technical Blog

```yaml
feeds:
  - id: dev-blog
    source: https://blog.example.com/feed.xml
    style:
      profile: technical
      features:
        syntax_highlighting: auto
        callouts: on
```

### Minimal (E-ink Safe)

```yaml
feeds:
  - id: news
    source: https://news.example.com/rss
    style:
      profile: minimal
      features:
        images: off
        tables: drop
```

### Custom Fonts

```yaml
style_profiles:
  custom:
    fonts:
      body: "Literata"
      mono: "Iosevka"
    features:
      syntax_highlighting: auto

feeds:
  - id: blog
    source: https://example.com/feed.xml
    style: custom
```

## Transform Patterns

### Basic Cleanup

```yaml
feeds:
  - id: blog
    source: https://example.com/feed.xml
    transform:
      - readability
      - sanitize_html
```

### Code Normalization

```yaml
feeds:
  - id: tech-blog
    source: https://example.com/feed.xml
    transform:
      - readability
      - sanitize_html
      - normalize_code_blocks
      - highlight_syntax
```

### Custom Transform Chain

```yaml
feeds:
  - id: newsletter
    source: https://example.com/feed.xml
    transform:
      - readability
      - remove_tracking_pixels
      - normalize_links
      - sanitize_html
```

## Frequency Patterns

### Daily Digest

```yaml
feeds:
  - id: daily-news
    source: https://news.example.com/rss
    select:
      since: 24h
      max_items: 30
    output:
      filename: 'daily-{{date}}.epub'
```

### Weekly Roundup

```yaml
feeds:
  - id: weekly-tech
    source: https://tech.example.com/feed.xml
    select:
      since: 7d
      max_items: 50
    output:
      filename: 'weekly-{{date}}.epub'
```

### Rolling Window

```yaml
feeds:
  - id: recent
    source: https://example.com/feed.xml
    select:
      since: 3d  # Last 3 days
      max_items: 100  # Up to 100 items
```

## Failure Handling Patterns

### Strict Mode

```yaml
defaults:
  failure_policy:
    mode: strict
    hard_fail_on:
      - style.font_missing
      - style.css_invalid
      - render.epub_build_failed
```

### Degrade Gracefully

```yaml
defaults:
  failure_policy:
    mode: degrade
    fallbacks:
      fonts: { body: serif, mono: monospace }
      syntax_highlighting: plain_code_blocks
      images: downscale_then_drop
```

### Quarantine Problematic

```yaml
defaults:
  failure_policy:
    mode: quarantine
    quarantine_on:
      - style.css_invalid
      - render.html_sanitized_aggressively
```

## Template Inheritance Patterns

### Extend and Override

```yaml
templates:
  base:
    select: { since: 48h, max_items: 25 }
    style: narrative

feeds:
  - id: custom
    extends: [base]
    style: technical  # Override
```

### Multiple Inheritance

```yaml
templates:
  reddit_base:
    source: { type: reddit }
    digest: { include_comments: top_3 }

  daily:
    select: { since: 24h, max_items: 20 }

feeds:
  - id: reddit-daily
    extends: [reddit_base, daily]
    source:
      subreddit: news
```

### Deep Merge

```yaml
templates:
  base:
    style:
      features: { syntax_highlighting: auto }

feeds:
  - id: custom
    extends: [base]
    style:
      features:
        callouts: on  # Merges with base features
```

## Output Patterns

### Dynamic Filenames

```yaml
feeds:
  - id: blog
    source: https://example.com/feed.xml
    output:
      filename: '{{feed_id}}-{{date}}.epub'  # blog-2026-01-22.epub
```

### Custom Paths

```yaml
feeds:
  - id: newsletter
    source: https://example.com/feed.xml
    output:
      path: ~/.epub/library/newsletters/
      filename: 'weekly-{{date}}.epub'
```

## Advanced Patterns

### Conditional Features

```yaml
feeds:
  - id: adaptive
    source: https://example.com/feed.xml
    style:
      features:
        syntax_highlighting: auto  # Only if code detected
        images: optimize  # Only if images present
        tables: simplify  # Only if tables present
```

### Multi-Feed Aggregation

```yaml
feeds:
  # Engineering sources
  - id: eng-news
    title: "Engineering News"
    sources:
      - https://blog.cloudflare.com/rss/
      - https://github.blog/feed/
      - https://stackoverflow.blog/feed/
    style: technical

  # Design sources
  - id: design-news
    title: "Design News"
    sources:
      - https://designbetter.co/feed
      - https://uxdesign.cc/feed
    style: narrative
```

### Platform-Specific

```yaml
feeds:
  - id: github-releases
    source:
      type: github
      repo: microsoft/vscode
      kind: releases
    select:
      since: 30d
    style: technical

  - id: reddit-threads
    source:
      type: reddit
      subreddit: programming
    digest:
      include_comments: top_5
      group_by: flair
```

## Shortcuts

### Agent-Friendly One-Liners

```yaml
# Minimal
feeds:
  - { id: hn, source: "https://hnrss.org/frontpage" }

# With style
feeds:
  - { id: blog, source: "https://example.com/feed.xml", style: technical }

# With frequency
feeds:
  - { id: weekly, source: "https://example.com/feed.xml", select: { since: 7d } }
```

### Common Abbreviations

| Full | Shorthand |
|------|-----------|
| `select: { since: "48h", max_items: 25 }` | Default (omit) |
| `style: { profile: "narrative" }` | `style: narrative` |
| `source: { url: "..." }` | `source: "..."` |
| `transform: ["readability"]` | Default for blogs |

## Pattern Selection

```
What do I need?
├── Simple RSS → single-source pattern
├── Multiple sources → multi-source aggregation
├── Reddit content → reddit with flair filtering
├── Code-heavy → technical blog pattern
├── High-volume → weekly roundup pattern
├── Unreliable source → failure handling pattern
└── Complex → template inheritance pattern
```
