# Feed Config Templates

Available templates for feed-create skill. Each template is a reusable YAML pattern optimized for common use cases.

## Template Catalog

| Template | Use Case | Features |
|----------|----------|----------|
| `minimal` | Basic RSS subscription | Simple feed with defaults |
| `reddit-digest` | Subreddit digests | Comments, flair grouping |
| `rss-readability` | Blog/article extraction | Readability transform |
| `technical-weekly` | Engineering feeds | Syntax highlighting, code blocks |

## minimal

Simplest possible config. Just RSS URL with all defaults.

```yaml
version: 1
feeds:
  - id: {{id}}
    source: {{url}}
```

**Variables:**
- `{{id}}` - feed identifier (slug)
- `{{url}}` - RSS/Atom feed URL

**Generated defaults:**
- style: narrative
- select: { since: 48h, max_items: 25 }
- no transforms

**When to use:**
- Simple RSS feeds
- Personal blogs
- Low-volume sources

## reddit-digest

Subreddit digest with top comments and flair grouping.

```yaml
version: 1

templates:
  reddit_digest:
    select:
      since: 24h
      max_items: 20
    digest:
      include_comments: top_3
      group_by: flair
    style:
      profile: narrative

feeds:
  - id: reddit-{{subreddit}}-digest
    title: 'r/{{subreddit}} — Daily Digest'
    extends: [reddit_digest]

    source:
      type: reddit
      subreddit: {{subreddit}}
      sort: top
      period: day

    select:
      allow:
        - flair: {{flair_list}}

    output:
      filename: 'r-{{subreddit}}-{{date}}.epub'
```

**Variables:**
- `{{subreddit}}` - subreddit name (no r/ prefix)
- `{{flair_list}}` - array of allowed flairs (optional)

**Features:**
- Top 3 comments per post
- Group posts by flair
- 24h rolling window
- Narrative style optimized for reading

**When to use:**
- Active subreddits
- Sports/news/discussion communities
- Content with meaningful comments

**Example instantiation:**
```yaml
# r/soccer digest
subreddit: soccer
flair_list: ['Match Thread', 'Post Match Thread', 'Transfer News']
```

## rss-readability

Blog/article feed with content extraction and sanitization.

```yaml
version: 1

templates:
  rss_readability:
    transform:
      - readability
      - sanitize_html
      - normalize_code_blocks

feeds:
  - id: {{id}}
    title: {{title}}
    extends: [rss_readability]

    source: {{url}}

    select:
      since: {{frequency}}
      max_items: {{max_items}}

    style: {{style_profile}}
```

**Variables:**
- `{{id}}` - feed identifier
- `{{title}}` - display title
- `{{url}}` - RSS feed URL
- `{{frequency}}` - 48h (daily), 7d (weekly)
- `{{max_items}}` - 25 (default), 40 (high-volume)
- `{{style_profile}}` - narrative or technical

**Transforms:**
- **readability** - extract main content
- **sanitize_html** - remove scripts/trackers
- **normalize_code_blocks** - standardize code formatting

**When to use:**
- Personal blogs
- News sites with paywalls
- Content with ads/clutter

**Example instantiation:**
```yaml
# Simon Willison's blog
id: simonwillison
title: "Simon Willison"
url: https://simonwillison.net/atom/everything/
frequency: 7d
max_items: 25
style_profile: technical
```

## technical-weekly

Engineering/technical feed with syntax highlighting and code-first layout.

```yaml
version: 1

style_profiles:
  technical:
    description: Code-first, dense, monospace friendly
    base_css: styles/base.css
    css: styles/technical.css
    features:
      syntax_highlighting: auto
      callouts: on
      inline_code: on

templates:
  rss_readability:
    transform:
      - readability
      - sanitize_html
      - normalize_code_blocks

feeds:
  - id: {{id}}
    title: {{title}}
    extends: [rss_readability]

    sources: {{source_list}}

    select:
      since: 7d
      max_items: 40

    style:
      profile: technical
      features:
        syntax_highlighting: auto
```

**Variables:**
- `{{id}}` - feed identifier
- `{{title}}` - display title
- `{{source_list}}` - array of RSS URLs

**Features:**
- **auto syntax highlighting** - detects code blocks, applies language-specific highlighting
- **callouts** - info/warning boxes preserved
- **inline code** - monospace formatting for `inline` code
- **technical CSS** - denser layout, code-optimized spacing

**When to use:**
- Engineering blogs
- Technical newsletters
- API documentation feeds
- GitHub release notes

**Example instantiation:**
```yaml
# Engineering weekly
id: engineering-weekly
title: "Engineering — Weekly"
source_list:
  - https://hnrss.org/frontpage
  - https://blog.cloudflare.com/rss/
  - https://github.blog/feed/
```

## Template Selection Decision Tree

```
What kind of content?
├── Reddit community → reddit-digest
├── Blog with lots of HTML → rss-readability
├── Technical/code content → technical-weekly
├── Simple RSS, no transforms → minimal
└── Multiple sources → technical-weekly or rss-readability
```

## Customization Patterns

### Override style profile

```yaml
# Start with template, override style
feeds:
  - id: my-feed
    extends: [rss_readability]
    style:
      profile: minimal  # Override template's narrative
```

### Add failure handling

```yaml
# Template + custom failure policy
feeds:
  - id: fragile-feed
    extends: [rss_readability]
    failure_policy:
      mode: quarantine  # More strict than default degrade
      quarantine_on: [render.html_sanitized_aggressively]
```

### Combine templates

```yaml
# Multiple template inheritance
feeds:
  - id: hybrid
    extends: [reddit_digest, rss_readability]  # Merge both
```

## Variable Substitution

feed-create replaces `{{var}}` placeholders during generation:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{id}}` | Feed identifier (slug) | `hn`, `reddit-soccer` |
| `{{title}}` | Display title | `"Hacker News"` |
| `{{url}}` | RSS feed URL | `https://...` |
| `{{subreddit}}` | Reddit subreddit name | `soccer` |
| `{{date}}` | Current date (YYYY-MM-DD) | `2026-01-22` |
| `{{frequency}}` | Time window | `48h`, `7d` |
| `{{max_items}}` | Item limit | `25`, `40` |
| `{{style_profile}}` | Style preset | `narrative`, `technical` |

## Adding New Templates

1. Create YAML in `assets/templates/{name}.yaml`
2. Document in this reference
3. Add to template selection decision tree
4. Update `scripts/list-templates.sh`

**Template requirements:**
- Must include `{{id}}` placeholder
- Must have `source` or `sources` field
- Should use `extends` for common patterns
- Must validate with zod schema

## Template Testing

```bash
# Generate from template
feed-create --template reddit-digest --var subreddit=soccer

# Validate output
~/Developer/utils/epub/scripts/validate-config.sh output.yaml

# Test fetch
epub feed test output.yaml --dry-run
```
