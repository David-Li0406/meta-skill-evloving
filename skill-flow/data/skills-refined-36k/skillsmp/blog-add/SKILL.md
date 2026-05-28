---
name: blog-add
description: "This skill should be used when adding blog posts to epub library, discovering new blogs to follow, or syncing blog archives. Triggers include 'add blog', 'harvest blog', 'get all posts from', 'add [author] blog', 'discover blogs', 'suggest blogs'."
---

# blog-add

harvest blog articles from individual author websites and convert to epub for reading on e-ink devices.

**Purpose**: This skill adds blog *articles* (individual posts from personal blogs) to the epub library, NOT topical feeds or actual books. The resulting epubs are organized in the `/blogs/` folder on the X4 device, grouped by author.

**Scope**: Individual author blogs (Simon Willison, Armin Ronacher, etc.), not curated topical feeds (use feed-create for r/soccer, AI digests, etc.).

## when to use

| use | skip |
|-----|------|
| adding all articles from an author's blog | single post conversion (use `epub url`) |
| discovering new individual author blogs | topical feeds like r/soccer (use feed-create) |
| batch harvesting blog archives | actual books (use `epub search`) |
| suggesting similar blogs based on library | agent documentation (use agents-digest) |

## decision tree: mode selection

```
What do you want to do?
├── add all posts from URL → harvest mode
├── add posts from author name → author mode (lookup URL first)
├── discover similar blogs → suggest mode (analyze library)
├── check what we have → inventory mode
└── unclear → ask which blog URL
```

## harvest mode

extract all post URLs from a blog and convert to epub.

### supported platforms

| platform | detection | extraction method |
|----------|-----------|-------------------|
| custom blogs | any HTML | agent-browser snapshot + link extraction |
| substack | `/archive` path | agent-browser + pagination |
| medium | `/@username` | agent-browser + infinite scroll |
| ghost | `/ghost/` in HTML | agent-browser + RSS fallback |
| wordpress | `/wp-content/` | agent-browser + sitemap |

### workflow

1. **discover**: use agent-browser to load blog and extract all post URLs
2. **dedupe**: check sqlite to skip existing posts
3. **convert**: batch process with epub CLI
4. **verify**: confirm count matches expected

### tool integration

```bash
# discover posts using agent-browser
agent-browser open https://example.com/blog
agent-browser snapshot -i -c
agent-browser get text "a[href*='/posts/']"  # extract post links

# check existing articles
sqlite3 ~/.epub/library.db "SELECT title FROM library_items WHERE author = 'Author Name'"

# batch convert
for url in $(cat /tmp/urls.txt); do
  node ~/Developer/utils/epub/bin/run.js url "$url" --author "Author Name"
done

# verify
sqlite3 ~/.epub/library.db "SELECT COUNT(*) FROM library_items WHERE author = 'Author Name'"
```

## author mode

look up author's blog URL then harvest.

### sources

| source | command | notes |
|--------|---------|-------|
| library | `sqlite3 ~/.epub/library.db "SELECT DISTINCT author FROM library_items"` | existing authors |
| assets | `cat ~/.claude/skills/blog-add/assets/supported-blogs.json` | curated list |
| search | agent-browser search `"[author] blog"` | fallback |

### workflow

1. **lookup**: find blog URL from author name
2. **confirm**: verify URL loads and matches author
3. **harvest**: run harvest mode with URL

## suggest mode

discover new blogs based on library patterns.

### discovery methods

| method | description | tool |
|--------|-------------|------|
| author mentions | blogs mentioned in existing posts | grep epub content |
| similar domains | same hosting/platform | domain analysis |
| blogroll links | "blogroll" sections in existing blogs | agent-browser extraction |
| related topics | tags/categories overlap | sqlite tag query |

### workflow

1. **analyze**: query library for patterns
2. **extract**: find candidate URLs
3. **rank**: score by relevance
4. **present**: show top 10 with stats

### tool integration

```bash
# get existing authors
sqlite3 ~/.epub/library.db "SELECT DISTINCT author FROM library_items ORDER BY author"

# analyze for mentions
for epub in ~/.epub/library/*.epub; do
  unzip -p "$epub" | grep -o 'https://[^"]*' | grep blog
done | sort | uniq -c | sort -rn | head -20
```

## inventory mode

check what's in the library and suggest additions.

### queries

```bash
# authors with < 10 posts (incomplete archives)
sqlite3 ~/.epub/library.db "
  SELECT author, COUNT(*) as count
  FROM library_items
  WHERE source IN ('feed', 'backfill', 'url')
  GROUP BY author
  HAVING count < 10
  ORDER BY count DESC
"

# authors missing from known blogs
comm -13 \
  <(sqlite3 ~/.epub/library.db "SELECT DISTINCT author FROM library_items WHERE source IN ('feed', 'backfill')" | sort) \
  <(jq -r '.[].author' ~/.claude/skills/blog-add/assets/supported-blogs.json | sort)

# oldest post dates (check for updates)
sqlite3 ~/.epub/library.db "
  SELECT author, MAX(created_at) as latest
  FROM library_items
  WHERE source IN ('feed', 'backfill')
  GROUP BY author
  ORDER BY latest ASC
  LIMIT 20
"
```

## batch conversion

convert multiple URLs efficiently.

### parallel processing

```bash
# sequential (safe)
cat urls.txt | while read url; do
  node ~/.epub/bin/run.js url "$url" --author "Author"
done

# parallel (faster, 4 workers)
cat urls.txt | xargs -P 4 -I {} node ~/.epub/bin/run.js url "{}" --author "Author"
```

### error handling

```bash
# with retry and logging
cat urls.txt | while read url; do
  if ! node ~/.epub/bin/run.js url "$url" --author "Author" 2>&1 | tee -a /tmp/conversion.log; then
    echo "$url" >> /tmp/failed.txt
  fi
  sleep 1  # rate limiting
done
```

## agent-browser patterns

### extract post list

```bash
# open blog archive
agent-browser open https://blog.example.com/archive

# wait for load
agent-browser wait --load networkidle

# get snapshot
agent-browser snapshot -i -c

# extract links
agent-browser eval "
  Array.from(document.querySelectorAll('a[href*=\"/posts/\"]'))
    .map(a => a.href)
    .join('\\n')
" > /tmp/urls.txt
```

### handle pagination

```bash
# click "load more" until exhausted
while agent-browser is visible ".load-more"; do
  agent-browser click ".load-more"
  agent-browser wait 2000
done

# extract all loaded links
agent-browser eval "Array.from(document.querySelectorAll('article a')).map(a => a.href).join('\\n')"
```

### infinite scroll

```bash
# scroll to bottom repeatedly
for i in {1..20}; do
  agent-browser scroll down 1000
  agent-browser wait 1000
done

# extract all visible posts
agent-browser snapshot -i -c
```

## validation

### post conversion

```bash
# verify epub created
test -f ~/.epub/library/*.epub && echo "✓ epub exists"

# verify in database
sqlite3 ~/.epub/library.db "SELECT title FROM library_items WHERE id = '$ID'"

# verify author set
sqlite3 ~/.epub/library.db "SELECT author FROM library_items WHERE id = '$ID'" | grep -q "Author Name"
```

### batch completion

```bash
# expected vs actual count
EXPECTED=$(wc -l < urls.txt)
ACTUAL=$(sqlite3 ~/.epub/library.db "SELECT COUNT(*) FROM library_items WHERE author = 'Author' AND source IN ('url', 'backfill')")
echo "Expected: $EXPECTED, Actual: $ACTUAL"

# check for failures
test -f /tmp/failed.txt && echo "⚠ $(wc -l < /tmp/failed.txt) failures"
```

## references

- [references/blog-platforms.md](references/blog-platforms.md) - platform detection and extraction strategies
- [references/author-discovery.md](references/author-discovery.md) - finding and ranking new blogs
- [references/epub-cli.md](references/epub-cli.md) - epub CLI usage and troubleshooting

## scripts

- [scripts/discover-posts.sh](scripts/discover-posts.sh) - extract post URLs using agent-browser
- [scripts/batch-convert.sh](scripts/batch-convert.sh) - parallel epub conversion with error handling

## assets

- [assets/supported-blogs.json](assets/supported-blogs.json) - curated blog list with URLs and authors

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| **calling these "books"** | misleading - they're blog articles | say "articles" or "posts", not "books" |
| **using blog-add for topical feeds** | blog-add is for individual authors, not r/soccer | use feed-create skill for curated topics |
| **confusing blogs/ and feeds/** | blogs/=authors, feeds/=topics | remember the distinction |
| using WebFetch for extraction | fails on JS-heavy blogs | use agent-browser with snapshot |
| no deduplication | re-converts existing posts | check sqlite before converting |
| sequential conversion only | slow for 100+ posts | use xargs -P for parallelization |
| missing author name | posts go to Unknown/ | always pass --author flag |
| no error logging | can't retry failures | log errors to file, save failed URLs |
| no rate limiting | gets blocked | add sleep between requests |
