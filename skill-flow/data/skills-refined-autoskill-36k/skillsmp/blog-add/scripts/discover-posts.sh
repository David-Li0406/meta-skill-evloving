#!/bin/bash
# discover-posts.sh - extract all post URLs from a blog using agent-browser
#
# Usage: ./discover-posts.sh <blog-url> [output-file]

set -euo pipefail

BLOG_URL="$1"
OUTPUT="${2:-/tmp/discovered-posts.txt}"

echo "Discovering posts from: $BLOG_URL"

# detect platform
agent-browser open "$BLOG_URL"
agent-browser wait --load networkidle

GENERATOR=$(agent-browser eval "document.querySelector('meta[name=\"generator\"]')?.content || ''" 2>/dev/null || echo "")

# determine platform
PLATFORM="custom"
case "$BLOG_URL" in
  *substack.com*) PLATFORM="substack" ;;
  *medium.com*) PLATFORM="medium" ;;
esac

if [ -z "$PLATFORM" ] && [ -n "$GENERATOR" ]; then
  case "$GENERATOR" in
    Ghost*) PLATFORM="ghost" ;;
    WordPress*) PLATFORM="wordpress" ;;
  esac
fi

echo "Detected platform: $PLATFORM"

# platform-specific extraction
case "$PLATFORM" in
  substack)
    echo "Using Substack extraction..."
    agent-browser open "${BLOG_URL}/archive"
    agent-browser wait --load networkidle

    # scroll to load more
    for i in {1..10}; do
      agent-browser scroll down 1000
      agent-browser wait 1000
    done

    # extract post links
    agent-browser eval "
      Array.from(document.querySelectorAll('a.post-preview-title, a[href*=\"/p/\"]'))
        .map(a => a.href)
        .filter((url, i, arr) => arr.indexOf(url) === i)
        .join('\n')
    " | jq -r > "$OUTPUT"
    ;;

  medium)
    echo "Using Medium extraction..."
    # infinite scroll
    for i in {1..30}; do
      agent-browser scroll down 1500
      agent-browser wait 1500
    done

    # extract story links
    agent-browser eval "
      Array.from(document.querySelectorAll('article a[rel=\"noopener follow\"]'))
        .map(a => a.href)
        .filter(url => url.includes('/@') || url.includes('/p/'))
        .filter((url, i, arr) => arr.indexOf(url) === i)
        .join('\n')
    " | jq -r > "$OUTPUT"
    ;;

  ghost)
    echo "Using Ghost extraction..."
    # try sitemap first
    SITEMAP_URL="${BLOG_URL}/sitemap.xml"
    if curl -sf "$SITEMAP_URL" | grep -oP '<loc>\K[^<]+' | grep '/posts/' > "$OUTPUT" 2>/dev/null; then
      echo "Extracted from sitemap"
    else
      # fallback to page scraping
      echo "Sitemap failed, using page scraping..."
      agent-browser eval "
        Array.from(document.querySelectorAll('article a, .post-card a'))
          .map(a => a.href)
          .filter((url, i, arr) => arr.indexOf(url) === i)
          .join('\n')
      " | jq -r > "$OUTPUT"
    fi
    ;;

  wordpress)
    echo "Using WordPress extraction..."
    # try sitemap
    if curl -sf "${BLOG_URL}/sitemap.xml" | grep -oP '<loc>\K[^<]+' > "$OUTPUT" 2>/dev/null; then
      echo "Extracted from sitemap"
    else
      # fallback to archive
      echo "Sitemap failed, using archive page..."

      # find archive
      for path in /archives /blog /posts ""; do
        agent-browser open "${BLOG_URL}${path}"
        agent-browser wait --load networkidle

        if agent-browser is visible "article" 2>/dev/null; then
          echo "Found posts at ${path}"
          break
        fi
      done

      # extract with pagination
      PAGE=1
      > "$OUTPUT"  # clear file
      while true; do
        agent-browser eval "
          Array.from(document.querySelectorAll('article a.entry-title, article h2 a'))
            .map(a => a.href)
            .join('\n')
        " | jq -r >> "$OUTPUT"

        # check for next page
        if agent-browser is visible ".next, .pagination a[rel='next']" 2>/dev/null; then
          agent-browser click ".next, .pagination a[rel='next']"
          agent-browser wait --load networkidle
          PAGE=$((PAGE + 1))
        else
          break
        fi
      done
    fi
    ;;

  *)
    echo "Using generic extraction..."
    # get all internal links that look like posts
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
          /\/\d{4}\//.test(url)
        )
        .filter((url, i, arr) => arr.indexOf(url) === i)
        .join('\n')
    " | jq -r > "$OUTPUT"
    ;;
esac

# cleanup and validate
if [ -f "$OUTPUT" ]; then
  # dedupe and sort
  sort -u "$OUTPUT" -o "$OUTPUT"

  # make relative URLs absolute
  if grep -q '^/' "$OUTPUT"; then
    sed -i '' "s|^/|${BLOG_URL}/|" "$OUTPUT"
  fi

  COUNT=$(wc -l < "$OUTPUT" | tr -d ' ')
  echo "✓ Found $COUNT URLs"
  echo "Output: $OUTPUT"

  # show sample
  if [ "$COUNT" -gt 0 ]; then
    echo ""
    echo "Sample (first 3):"
    head -3 "$OUTPUT"
  fi

  if [ "$COUNT" -lt 5 ]; then
    echo "⚠ Warning: Suspiciously low count, verify extraction"
  fi
else
  echo "✗ No URLs found"
  exit 1
fi
