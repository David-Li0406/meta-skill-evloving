# epub CLI

usage and troubleshooting for the epub library manager at `/Users/luke/Developer/utils/epub`.

## core commands

### url conversion

convert web URL to epub.

```bash
cd ~/Developer/utils/epub
node ./bin/run.js url "<url>" --author "Author Name"
```

**flags:**

| flag | purpose | example |
|------|---------|---------|
| `--author` | set author metadata | `--author "Linus Lee"` |
| `--title` | override title | `--title "Custom Title"` |
| `--source` | set source type | `--source backfill` |

**source routing:**

| source | destination | use case |
|--------|-------------|----------|
| `url` | `/books/Author/` | one-off conversions |
| `backfill` | `/blogs/Author/` | blog archives |
| `rss` | `/blogs/Author/` | RSS feed items |

### library queries

check what's in the database.

```bash
# list all books
sqlite3 ~/.epub/library.db "SELECT title, author FROM books LIMIT 10"

# count by author
sqlite3 ~/.epub/library.db "
  SELECT author, COUNT(*) as count
  FROM books
  GROUP BY author
  ORDER BY count DESC
"

# search by title
sqlite3 ~/.epub/library.db "
  SELECT title, author, created_at
  FROM books
  WHERE title LIKE '%keyword%'
"

# get book details
sqlite3 ~/.epub/library.db "
  SELECT * FROM books WHERE id = 'ABC123'
"
```

### device sync

sync epubs to X4 device (via x4-sync skill, not directly here).

```bash
# check device available
curl -s http://10.0.0.61:8080/api/list/

# sync is handled by x4-sync skill
# blog-add focuses on conversion only
```

## database schema

sqlite structure at `~/.epub/library.db`.

### books table

| column | type | notes |
|--------|------|-------|
| id | TEXT PRIMARY KEY | unique book ID |
| title | TEXT | book title |
| author | TEXT | author name |
| path | TEXT | filesystem path to epub |
| source | TEXT | `url`, `backfill`, or `rss` |
| url | TEXT | original URL |
| created_at | TIMESTAMP | when added |
| updated_at | TIMESTAMP | last modified |

### querying patterns

```bash
# books missing author
sqlite3 ~/.epub/library.db "
  SELECT id, title FROM books
  WHERE author IS NULL OR author = 'Unknown'
"

# duplicate titles
sqlite3 ~/.epub/library.db "
  SELECT title, COUNT(*) as dupes
  FROM books
  GROUP BY title
  HAVING dupes > 1
"

# recent additions
sqlite3 ~/.epub/library.db "
  SELECT title, author, created_at
  FROM books
  ORDER BY created_at DESC
  LIMIT 20
"

# books by source
sqlite3 ~/.epub/library.db "
  SELECT source, COUNT(*) as count
  FROM books
  GROUP BY source
"
```

## conversion process

what happens when you run `url` command.

### steps

1. **fetch**: download HTML from URL
2. **extract**: parse title, author, content
3. **convert**: generate epub with Readability
4. **save**: write to `~/.epub/library/<hash>.epub`
5. **database**: insert metadata into sqlite
6. **return**: output book ID and path

### success indicators

```bash
# check conversion succeeded
test -f ~/.epub/library/*.epub && echo "✓ epub created"

# verify database entry
ID=$(sqlite3 ~/.epub/library.db "SELECT id FROM books ORDER BY created_at DESC LIMIT 1")
sqlite3 ~/.epub/library.db "SELECT title, author FROM books WHERE id = '$ID'"
```

## troubleshooting

common issues and fixes.

### author not set (goes to Unknown/)

**symptom**: book added but author is NULL

```bash
# check
sqlite3 ~/.epub/library.db "SELECT id, title, author FROM books WHERE author IS NULL"
```

**fix**: always pass `--author` flag

```bash
node ./bin/run.js url "$URL" --author "Correct Author"
```

**fix existing**: update database

```bash
sqlite3 ~/.epub/library.db "
  UPDATE books
  SET author = 'Correct Author', source = 'backfill'
  WHERE id IN ('id1', 'id2', 'id3')
"
```

### conversion fails (timeout/error)

**symptom**: command exits with error

```bash
# common errors
# - ECONNREFUSED: site blocked request
# - ETIMEDOUT: slow site or network issue
# - Parse error: Readability couldn't extract content
```

**fix**: retry with delay

```bash
sleep 5
node ./bin/run.js url "$URL" --author "Author"
```

**fix**: check URL is accessible

```bash
curl -I "$URL"  # should return 200
```

### duplicate conversions

**symptom**: same article converted multiple times

```bash
# check for duplicates
sqlite3 ~/.epub/library.db "
  SELECT url, COUNT(*) as count
  FROM books
  GROUP BY url
  HAVING count > 1
"
```

**fix**: check before converting

```bash
# deduplication check
EXISTS=$(sqlite3 ~/.epub/library.db "SELECT id FROM books WHERE url = '$URL'")
if [ -z "$EXISTS" ]; then
  node ./bin/run.js url "$URL" --author "Author"
else
  echo "Already exists: $EXISTS"
fi
```

### title cleanup needed

**symptom**: titles have " | Blog Name" suffix

```bash
# find titles with suffixes
sqlite3 ~/.epub/library.db "
  SELECT id, title FROM books
  WHERE title LIKE '%|%' OR title LIKE '%·%'
"
```

**fix**: clean in database

```bash
# remove suffix patterns
sqlite3 ~/.epub/library.db "
  UPDATE books
  SET title = REPLACE(title, ' | thesephist.com', '')
  WHERE title LIKE '%thesephist.com'
"

sqlite3 ~/.epub/library.db "
  UPDATE books
  SET title = REPLACE(title, 'Frank Chimero · ', '')
  WHERE title LIKE 'Frank Chimero%'
"
```

### source routing incorrect

**symptom**: backfill posts went to `/books/` instead of `/blogs/`

**cause**: source field was `url` instead of `backfill`

**fix**: update source field

```bash
sqlite3 ~/.epub/library.db "
  UPDATE books
  SET source = 'backfill'
  WHERE author IN ('Linus Lee', 'Nikita Prokopov', 'Salvatore Sanfilippo')
    AND source = 'url'
"
```

**prevent**: always use `--source backfill` for blog harvesting... wait, need to check if CLI supports this flag.

Actually the epub CLI determines routing based on source field, which is set internally. The CLI doesn't expose a --source flag, so we control routing by:
1. Using RSS sync for feeds (sets source='rss')
2. Manually updating source in DB after conversion for backfills

So the workflow is:
```bash
# convert posts (defaults to source='url')
node ./bin/run.js url "$URL" --author "Author"

# batch update source after conversion
sqlite3 ~/.epub/library.db "
  UPDATE books
  SET source = 'backfill'
  WHERE author = 'Author' AND source = 'url'
"
```

## batch conversion patterns

efficient patterns for converting many posts.

### sequential with logging

```bash
cat urls.txt | while read url; do
  echo "Converting: $url"
  if node ./bin/run.js url "$url" --author "Author" 2>&1 | tee -a /tmp/conversion.log; then
    echo "✓ $url" >> /tmp/success.txt
  else
    echo "✗ $url" >> /tmp/failed.txt
  fi
  sleep 1  # rate limiting
done
```

### parallel with xargs

```bash
# 4 parallel workers
cat urls.txt | xargs -P 4 -I {} sh -c '
  node ~/Developer/utils/epub/bin/run.js url "{}" --author "Author" 2>&1 && echo "✓ {}" || echo "✗ {}"
'
```

### parallel with gnu parallel (if installed)

```bash
parallel -j 4 \
  'node ~/Developer/utils/epub/bin/run.js url {} --author "Author"' \
  :::: urls.txt
```

### with deduplication

```bash
cat urls.txt | while read url; do
  # check if URL already converted
  EXISTS=$(sqlite3 ~/.epub/library.db "SELECT id FROM books WHERE url = '$url'")

  if [ -z "$EXISTS" ]; then
    echo "Converting: $url"
    node ./bin/run.js url "$url" --author "Author"
    sleep 1
  else
    echo "Skip (exists): $url"
  fi
done
```

## post-conversion cleanup

standard cleanup after batch conversion.

```bash
#!/bin/bash
# cleanup-after-conversion.sh <author>

AUTHOR="$1"

# 1. update source to backfill
sqlite3 ~/.epub/library.db "
  UPDATE books
  SET source = 'backfill'
  WHERE author = '$AUTHOR' AND source = 'url'
"

# 2. clean title suffixes
sqlite3 ~/.epub/library.db "
  UPDATE books
  SET title = REPLACE(title, ' | ${AUTHOR}', '')
  WHERE author = '$AUTHOR' AND title LIKE '%|%'
"

# 3. verify count
COUNT=$(sqlite3 ~/.epub/library.db "SELECT COUNT(*) FROM books WHERE author = '$AUTHOR'")
echo "✓ $COUNT posts for $AUTHOR"

# 4. check for missing authors
MISSING=$(sqlite3 ~/.epub/library.db "SELECT COUNT(*) FROM books WHERE author IS NULL")
if [ $MISSING -gt 0 ]; then
  echo "⚠ $MISSING books with missing author"
fi
```

## performance tips

optimize batch conversions.

### parallel processing

- use `-P 4` for 4 workers (don't exceed 8)
- add `sleep 1` between requests to avoid rate limiting
- log errors for retry

### deduplication

- check sqlite before converting
- use URL as deduplication key
- batch check URLs first, then filter

### error handling

- log failures to separate file
- retry failed URLs with backoff
- validate epub created before marking success

### database optimization

```bash
# vacuum database after large batch
sqlite3 ~/.epub/library.db "VACUUM"

# create index on author for faster queries
sqlite3 ~/.epub/library.db "CREATE INDEX IF NOT EXISTS idx_author ON books(author)"

# create index on URL for deduplication
sqlite3 ~/.epub/library.db "CREATE INDEX IF NOT EXISTS idx_url ON books(url)"
```

## integration with x4-sync

epub CLI converts, x4-sync handles device transfer.

```bash
# 1. convert blog posts with epub CLI (blog-add skill)
for url in $(cat urls.txt); do
  node ~/Developer/utils/epub/bin/run.js url "$url" --author "Author"
done

# 2. update source for routing
sqlite3 ~/.epub/library.db "UPDATE books SET source = 'backfill' WHERE author = 'Author' AND source = 'url'"

# 3. sync to device with x4-sync skill
# (handled separately, not in blog-add scope)
```

the division:
- **blog-add**: discovers URLs, converts to epub, manages library
- **x4-sync**: syncs epubs to X4 device, manages feeds, device tree
