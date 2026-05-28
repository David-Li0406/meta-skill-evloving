# blog platforms

detection and extraction strategies for common blog platforms.

## platform detection

identify blog platform from HTML/DOM patterns.

### detection signals

| platform | signal | reliability |
|----------|--------|-------------|
| substack | `substack.com` in URL or `<meta name="generator" content="Substack">` | high |
| medium | `medium.com/@` or `<meta property="al:ios:app_name" content="Medium">` | high |
| ghost | `<meta name="generator" content="Ghost">` | high |
| wordpress | `/wp-content/` in page source or `<meta name="generator" content="WordPress">` | high |
| custom | no generator meta tag | low |

### agent-browser detection

```bash
# open blog
agent-browser open "$BLOG_URL"
agent-browser wait --load networkidle

# check generator tag
GENERATOR=$(agent-browser eval "document.querySelector('meta[name=\"generator\"]')?.content || ''")

# check URL patterns
case "$BLOG_URL" in
  *substack.com*) PLATFORM="substack" ;;
  *medium.com*) PLATFORM="medium" ;;
  *) PLATFORM="$GENERATOR" ;;
esac

echo "Detected platform: $PLATFORM"
```

## extraction strategies

platform-specific methods for getting all post URLs.

### substack

**archive page pattern**: `https://example.substack.com/archive`

```bash
# load archive
agent-browser open "$BLOG_URL/archive"
agent-browser wait --load networkidle

# scroll to load all posts
for i in {1..10}; do
  agent-browser scroll down 1000
  agent-browser wait 1000
done

# extract post links
agent-browser eval "
  Array.from(document.querySelectorAll('a.post-preview-title'))
    .map(a => a.href)
    .filter(url => url.includes('/p/'))
    .join('\n')
" > posts.txt
```

**pagination pattern**: some substacks have paginated archives

```bash
PAGE=0
while true; do
  agent-browser open "$BLOG_URL/archive?sort=new&page=$PAGE"
  agent-browser wait --load networkidle

  # check if posts exist
  if ! agent-browser is visible ".post-preview-title"; then
    break
  fi

  # extract page posts
  agent-browser eval "Array.from(document.querySelectorAll('a.post-preview-title')).map(a => a.href).join('\n')" >> posts.txt

  PAGE=$((PAGE + 1))
done

# dedupe
sort -u posts.txt -o posts.txt
```

### medium

**user profile pattern**: `https://medium.com/@username`

```bash
# load profile
agent-browser open "https://medium.com/@$USERNAME"
agent-browser wait --load networkidle

# infinite scroll
for i in {1..30}; do
  agent-browser scroll down 1500
  agent-browser wait 1500
done

# extract story links
agent-browser eval "
  Array.from(document.querySelectorAll('article a[rel=\"noopener follow\"]'))
    .map(a => a.href)
    .filter(url => url.includes('/@'))
    .filter((url, i, arr) => arr.indexOf(url) === i)  // dedupe
    .join('\n')
" > posts.txt
```

**publication pattern**: `https://medium.com/publication-name`

similar to user profile, but use publication URL.

### ghost

**sitemap pattern**: most ghost blogs have `/sitemap.xml`

```bash
# try sitemap first
curl -s "$BLOG_URL/sitemap.xml" | grep -oP '<loc>\K[^<]+' | grep '/posts/' > posts.txt

# fallback to archive page
if [ ! -s posts.txt ]; then
  agent-browser open "$BLOG_URL"
  agent-browser find text "Archive" click || agent-browser find text "All posts" click
  agent-browser wait --load networkidle

  # extract links
  agent-browser eval "Array.from(document.querySelectorAll('article a')).map(a => a.href).join('\n')" > posts.txt
fi
```

**RSS pattern**: ghost blogs have `/rss/`

```bash
curl -s "$BLOG_URL/rss/" | grep -oP '<link>\K[^<]+' | grep -v 'rss' > posts.txt
```

### wordpress

**archive pattern**: `/archives` or `/blog`

```bash
# try common archive URLs
for path in /archives /blog /posts ""; do
  agent-browser open "$BLOG_URL$path"
  agent-browser wait --load networkidle

  if agent-browser is visible "article"; then
    break
  fi
done

# handle pagination
PAGE=1
while true; do
  agent-browser eval "Array.from(document.querySelectorAll('article a.entry-title, article h2 a')).map(a => a.href).join('\n')" >> posts.txt

  # check for next page
  if agent-browser is visible ".next, .pagination a[rel='next']"; then
    agent-browser click ".next, .pagination a[rel='next']"
    agent-browser wait --load networkidle
    PAGE=$((PAGE + 1))
  else
    break
  fi
done

# dedupe
sort -u posts.txt -o posts.txt
```

**sitemap.xml pattern**: wordpress generates sitemaps

```bash
curl -s "$BLOG_URL/sitemap.xml" | grep -oP '<loc>\K[^<]+' > posts.txt
# or
curl -s "$BLOG_URL/wp-sitemap-posts-post-1.xml" | grep -oP '<loc>\K[^<]+' > posts.txt
```

### custom/static blogs

**generic extraction**: works for any blog with visible post links

```bash
# load homepage
agent-browser open "$BLOG_URL"
agent-browser wait --load networkidle

# get all internal links
agent-browser eval "
  const baseUrl = new URL(window.location.href);
  Array.from(document.querySelectorAll('a'))
    .map(a => a.href)
    .filter(url => {
      try {
        const u = new URL(url);
        return u.hostname === baseUrl.hostname;
      } catch {
        return false;
      }
    })
    .filter(url =>
      url.includes('/post') ||
      url.includes('/blog') ||
      url.includes('/writing') ||
      url.includes('/essay') ||
      /\/\d{4}\//.test(url)  // date pattern
    )
    .filter((url, i, arr) => arr.indexOf(url) === i)
    .join('\n')
" > posts.txt
```

**archive page heuristics**: look for "archive", "all posts", "writing"

```bash
# find archive link
ARCHIVE_URL=$(agent-browser eval "
  const link = Array.from(document.querySelectorAll('a'))
    .find(a => /archive|all posts|writing|essays/i.test(a.textContent));
  link?.href || '';
")

if [ -n "$ARCHIVE_URL" ]; then
  agent-browser open "$ARCHIVE_URL"
  agent-browser wait --load networkidle

  # extract from archive
  agent-browser eval "Array.from(document.querySelectorAll('article a, .post-link')).map(a => a.href).join('\n')" > posts.txt
fi
```

## extraction quality checks

verify extracted URLs are valid post links.

### validation checks

```bash
# check URL count
COUNT=$(wc -l < posts.txt)
echo "Found $COUNT URLs"

# check URL pattern
if [ $COUNT -lt 5 ]; then
  echo "⚠ Suspiciously low count, check extraction"
fi

# verify URLs are absolute
if grep -q '^/' posts.txt; then
  echo "⚠ Relative URLs found, need to make absolute"
  sed -i '' "s|^/|$BLOG_URL/|" posts.txt
fi

# dedupe and sort
sort -u posts.txt -o posts.txt

# sample first 3
echo "Sample URLs:"
head -3 posts.txt
```

### error patterns

| error | symptom | fix |
|-------|---------|-----|
| no URLs found | empty posts.txt | try different selector or scroll more |
| duplicate URLs | same URL many times | use `sort -u` to dedupe |
| non-post URLs | homepage/about links | tighten filter regex |
| relative paths | URLs start with `/` | prepend blog base URL |
| too many URLs | > 1000 for personal blog | check filter is working |

## platform-specific quirks

### substack

- some archives require scrolling to trigger load
- post preview links sometimes have query params (`?s=r`)
- subscriber-only posts may be paywalled

### medium

- infinite scroll requires patience (30+ scrolls)
- member-only posts have different link format
- clap counts and reading time in DOM

### ghost

- sitemap is most reliable method
- archive page might be disabled
- tag pages have post listings too

### wordpress

- pagination varies by theme
- some themes use infinite scroll
- sitemap structure varies (may need `wp-sitemap-posts-post-1.xml`)

## testing new platforms

when encountering unknown platform:

1. **inspect HTML**: look for generator tags, class patterns
2. **try sitemap**: check `/sitemap.xml`, `/rss/`, `/feed/`
3. **find archive**: search for "archive", "all posts", "writing" links
4. **use generic extraction**: fall back to link pattern matching
5. **validate sample**: test first 3 URLs with epub CLI
6. **adjust filters**: refine selectors based on results
