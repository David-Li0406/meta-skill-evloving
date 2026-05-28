# feed sources

Known blogs and archive patterns for epub curation.

## subscribed feeds

current feeds in epub library:

| blog | RSS URL | archive pattern |
|------|---------|-----------------|
| Simon Willison | `https://simonwillison.net/atom/everything/` | `/{year}/` |
| Armin Ronacher | `https://lucumr.pocoo.org/feed.atom` | `/{year}/` |

## recommended feeds

blogs worth adding:

| blog | RSS URL | topics |
|------|---------|--------|
| Eugene Yan | `https://eugeneyan.com/rss/` | ML systems, LLMs |
| Chip Huyen | `https://huyenchip.com/feed.xml` | ML engineering |
| Lenny's Newsletter | `https://www.lennysnewsletter.com/feed` | product |
| Paul Graham | `https://www.paulgraham.com/rss.html` | essays |
| Dan Luu | `https://danluu.com/atom.xml` | systems |

## archive backfill

supported domains with known archive patterns:

```bash
# Simon Willison - yearly archives
epub feed backfill simonwillison.net --year 2024

# Armin Ronacher - yearly archives
epub feed backfill lucumr.pocoo.org --year 2024
```

## adding new feeds

```bash
# add feed
epub feed add https://example.com/feed.xml

# sync new posts
epub feed sync

# check what was added
epub library list --source feed
```

## backfill implementation

the backfill command:
1. fetches archive page at `https://{domain}/{year}/`
2. extracts article URLs via href patterns
3. filters URLs already in library
4. converts each new URL to epub
5. marks as seen to avoid re-fetching

supported archive patterns:
- `/{year}/` - yearly archive pages
- `/{year}/{month}/` - monthly archives
- `/archive/` - single archive page

## feed sync behavior

| scenario | behavior |
|----------|----------|
| new feed | fetch up to 10 recent posts |
| existing feed | fetch only unseen posts |
| --limit N | cap at N posts per feed |
| error on post | mark as seen, skip to next |

## content quality

some feeds include:
- full content (preferred)
- excerpts only (requires URL fetch)
- images (embedded in epub)
- code blocks (preserved)

readability extraction handles most blog layouts.

## troubleshooting

| issue | cause | fix |
|-------|-------|-----|
| no articles found | feed URL wrong | check feed URL in browser |
| articles missing content | excerpt-only feed | content fetched from URL |
| backfill finds 0 posts | archive pattern unknown | add pattern to KNOWN_ARCHIVES |
| duplicate posts | feed item URL changed | check sourceUrl in library |
