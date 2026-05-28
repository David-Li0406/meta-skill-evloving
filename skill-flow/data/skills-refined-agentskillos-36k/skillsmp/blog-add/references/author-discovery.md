# author discovery

finding and ranking new blogs based on library patterns.

## discovery sources

where to find candidate blogs.

### existing library analysis

mine current epub library for patterns and mentions.

```bash
# get all authors
sqlite3 ~/.epub/library.db "
  SELECT DISTINCT author, COUNT(*) as posts
  FROM books
  WHERE author IS NOT NULL AND author != 'Unknown'
  GROUP BY author
  ORDER BY posts DESC
"

# authors with < 10 posts (might have more available)
sqlite3 ~/.epub/library.db "
  SELECT author, COUNT(*) as count
  FROM books
  WHERE author IS NOT NULL
  GROUP BY author
  HAVING count < 10
  ORDER BY count DESC
"

# find blog mentions in content
for epub in ~/.epub/library/*.epub; do
  unzip -p "$epub" | strings | grep -oE 'https?://[a-zA-Z0-9.-]+\.(com|net|org)/[^ ]*' | grep -E 'blog|writing|essay|posts'
done | sort | uniq -c | sort -rn | head -50 > /tmp/mentioned-blogs.txt
```

### blogroll extraction

blogs often link to other blogs they read.

```bash
# for each author's blog, find blogroll
for author in $(sqlite3 ~/.epub/library.db "SELECT DISTINCT author FROM books LIMIT 10"); do
  # lookup blog URL from assets
  BLOG_URL=$(jq -r ".[] | select(.author == \"$author\") | .url" ~/.claude/skills/blog-add/assets/supported-blogs.json)

  if [ -n "$BLOG_URL" ]; then
    # open blog
    agent-browser open "$BLOG_URL"
    agent-browser wait --load networkidle

    # find blogroll or links page
    if agent-browser find text "blogroll" click 2>/dev/null; then
      agent-browser wait --load networkidle

      # extract links
      agent-browser eval "
        Array.from(document.querySelectorAll('a'))
          .filter(a => !a.href.includes('$BLOG_URL'))
          .map(a => ({url: a.href, text: a.textContent.trim()}))
          .filter(l => l.text.length > 0)
          .map(l => JSON.stringify(l))
          .join('\n')
      " >> /tmp/blogroll-links.json
    fi
  fi
done

# aggregate and rank
cat /tmp/blogroll-links.json | jq -r '.url' | sort | uniq -c | sort -rn | head -30
```

### topic/tag overlap

find blogs in similar topic spaces.

```bash
# analyze tags in library (if epub has metadata)
sqlite3 ~/.epub/library.db "
  SELECT tags, COUNT(*) as count
  FROM books
  WHERE tags IS NOT NULL
  GROUP BY tags
  ORDER BY count DESC
  LIMIT 20
"

# search for blogs with same tags using agent-browser
POPULAR_TAG="programming"  # from above query

agent-browser open "https://www.google.com/search?q=${POPULAR_TAG}+blog"
agent-browser wait --load networkidle
agent-browser snapshot -i -c

# extract blog URLs from search results
agent-browser eval "
  Array.from(document.querySelectorAll('a'))
    .map(a => a.href)
    .filter(url => /blog|writing|essays/.test(url))
    .filter(url => !/google|facebook|twitter/.test(url))
    .slice(0, 20)
    .join('\n')
" > /tmp/tag-blogs-${POPULAR_TAG}.txt
```

### social media discovery

find blogs from social profiles of existing authors.

```bash
# search for author's social profiles
AUTHOR="Linus Lee"  # from library

agent-browser open "https://www.google.com/search?q=${AUTHOR}+blog+OR+website"
agent-browser wait --load networkidle

# extract top results
agent-browser eval "
  Array.from(document.querySelectorAll('.g a'))
    .map(a => a.href)
    .filter(url => !url.includes('google.com'))
    .slice(0, 5)
    .join('\n')
" > /tmp/author-${AUTHOR// /-}-search.txt
```

## ranking candidates

score discovered blogs by relevance and quality.

### scoring dimensions

| dimension | weight | measurement |
|-----------|--------|-------------|
| mention count | 3x | times mentioned in library epubs |
| blogroll frequency | 2x | times linked in blogrolls |
| topic overlap | 2x | shared tags/keywords |
| post frequency | 1x | posts/year estimate |
| content depth | 1x | avg post word count |
| author reputation | 1x | follower count, references |

### scoring script

```bash
#!/bin/bash
# score-blog.sh <blog-url>

BLOG_URL="$1"

# mention count (from epub content)
MENTIONS=$(grep -r "$BLOG_URL" ~/.epub/library/ 2>/dev/null | wc -l)
MENTION_SCORE=$((MENTIONS * 3))

# check if in known blogrolls
BLOGROLL_COUNT=$(grep -c "$BLOG_URL" /tmp/blogroll-links.json 2>/dev/null || echo 0)
BLOGROLL_SCORE=$((BLOGROLL_COUNT * 2))

# estimate post frequency via agent-browser
agent-browser open "$BLOG_URL" --session score
agent-browser wait --load networkidle --session score

# count visible posts
POST_COUNT=$(agent-browser eval "document.querySelectorAll('article, .post').length" --session score)

# check date range
LATEST_DATE=$(agent-browser eval "
  const dates = Array.from(document.querySelectorAll('time[datetime]'))
    .map(t => t.getAttribute('datetime'));
  dates[0] || '';
" --session score)

agent-browser close --session score

# frequency score (placeholder)
FREQ_SCORE=$((POST_COUNT / 10))

# total score
TOTAL=$((MENTION_SCORE + BLOGROLL_SCORE + FREQ_SCORE))

echo "$TOTAL|$BLOG_URL|mentions:$MENTIONS|blogrolls:$BLOGROLL_COUNT|posts:$POST_COUNT"
```

### ranking output

```bash
# score all candidates
cat /tmp/candidate-blogs.txt | while read url; do
  ./score-blog.sh "$url"
done | sort -t'|' -k1 -rn | head -20 > /tmp/ranked-blogs.txt

# format for review
cat /tmp/ranked-blogs.txt | while IFS='|' read score url metrics; do
  echo "[$score] $url"
  echo "    $metrics"
done
```

## validation

verify discovered blogs are worth adding.

### quality checks

```bash
#!/bin/bash
# validate-blog.sh <blog-url>

BLOG_URL="$1"

agent-browser open "$BLOG_URL"
agent-browser wait --load networkidle

# check 1: has recent posts
LATEST_DATE=$(agent-browser eval "
  const dates = Array.from(document.querySelectorAll('time[datetime]'))
    .map(t => new Date(t.getAttribute('datetime')));
  dates.length > 0 ? dates[0].toISOString() : '';
")

if [ -n "$LATEST_DATE" ]; then
  DAYS_AGO=$(( ($(date +%s) - $(date -j -f "%Y-%m-%dT%H:%M:%S" "${LATEST_DATE:0:19}" +%s)) / 86400 ))
  if [ $DAYS_AGO -gt 365 ]; then
    echo "⚠ Blog inactive: latest post $DAYS_AGO days ago"
  fi
fi

# check 2: has content (not empty/404)
if ! agent-browser is visible "article, .post, main"; then
  echo "✗ No content found"
  exit 1
fi

# check 3: has multiple posts
POST_COUNT=$(agent-browser eval "document.querySelectorAll('article, .post').length")
if [ "$POST_COUNT" -lt 3 ]; then
  echo "⚠ Only $POST_COUNT posts visible"
fi

# check 4: identify author
AUTHOR=$(agent-browser eval "
  document.querySelector('meta[name=\"author\"]')?.content ||
  document.querySelector('.author')?.textContent.trim() ||
  '';
")

if [ -z "$AUTHOR" ]; then
  echo "⚠ Author not detected"
else
  echo "✓ Author: $AUTHOR"
fi

echo "✓ Blog validated"
```

### manual review checklist

before adding a discovered blog:

- [ ] blog has > 10 posts
- [ ] latest post within last year
- [ ] author is identifiable
- [ ] content matches library topics
- [ ] RSS feed or archive page exists
- [ ] no paywall or login required

## curated lists

known high-quality blog sources.

### tech/programming blogrolls

| source | URL | notes |
|--------|-----|-------|
| Hacker News who is hiring | news.ycombinator.com | monthly threads with blog links |
| lobste.rs | lobste.rs/recent | aggregator with quality blogs |
| planet.emacslife.com | planet.emacslife.com | emacs community blogs |
| programming.dev | programming.dev | community aggregator |

### personal knowledge management

| source | URL | notes |
|--------|-----|-------|
| Andy Matuschak's friends | notes.andymatuschak.org | evergreen notes network |
| Maggie Appleton | maggieappleton.com | digital gardening |
| Gordon Brander | subconscious.substack.com | tools for thought |

### essay/longform

| source | URL | notes |
|--------|-----|-------|
| Ribbonfarm | ribbonfarm.com | longform essays |
| Gwern | gwern.net | deep research |
| Paul Graham | paulgraham.com | startup essays |
| Wait But Why | waitbutwhy.com | illustrated longform |

## discovery automation

automate finding blogs from existing patterns.

### weekly discovery job

```bash
#!/bin/bash
# discover-blogs-weekly.sh

# 1. extract new mentions from recent epubs
sqlite3 ~/.epub/library.db "
  SELECT path FROM books
  WHERE created_at > datetime('now', '-7 days')
" | while read epub; do
  unzip -p "$epub" | strings | grep -oE 'https?://[^ ]+' | grep -E 'blog|writing'
done | sort -u > /tmp/new-mentions.txt

# 2. score and rank
cat /tmp/new-mentions.txt | while read url; do
  ./score-blog.sh "$url"
done | sort -t'|' -k1 -rn | head -10 > /tmp/new-candidates.txt

# 3. output for review
echo "New blog candidates (last 7 days):"
cat /tmp/new-candidates.txt | while IFS='|' read score url metrics; do
  echo "[$score] $url - $metrics"
done
```

### similarity detection

find blogs similar to favorites.

```bash
# get top 5 authors by post count
FAVORITES=$(sqlite3 ~/.epub/library.db "
  SELECT author FROM books
  GROUP BY author
  ORDER BY COUNT(*) DESC
  LIMIT 5
")

# for each favorite, search for similar blogs
echo "$FAVORITES" | while read author; do
  agent-browser open "https://www.google.com/search?q=blogs+like+${author// /+}"
  agent-browser wait --load networkidle

  agent-browser eval "
    Array.from(document.querySelectorAll('.g a'))
      .map(a => a.href)
      .filter(url => !/google|facebook|twitter/.test(url))
      .slice(0, 5)
      .join('\n')
  " >> /tmp/similar-to-${author// /-}.txt
done

# aggregate and dedupe
cat /tmp/similar-to-*.txt | sort -u > /tmp/similar-blogs.txt
```

## integration with library

once blogs are discovered and validated, add to assets.

```bash
# add to supported-blogs.json
jq '. += [{
  "author": "New Author",
  "url": "https://newblog.com",
  "platform": "ghost",
  "added": "'$(date -I)'",
  "status": "active"
}]' ~/.claude/skills/blog-add/assets/supported-blogs.json > /tmp/updated.json

mv /tmp/updated.json ~/.claude/skills/blog-add/assets/supported-blogs.json

# trigger harvest
node ~/.epub/bin/run.js url "https://newblog.com/first-post" --author "New Author"
```
