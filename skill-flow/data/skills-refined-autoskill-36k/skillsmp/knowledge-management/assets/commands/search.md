---
description: Search knowledge base by title, tags, or content
---

# Search - Knowledge Search

Search across learnings, knowledge base, retrospectives, and examples.

## Usage

```
/search [query]
/search --tag [tag-name]
/search --type [learning|knowledge|retrospective|example]
/search --reindex
```

## Instructions

### If `--reindex` flag is present

Rebuild the index:

```bash
bash scripts/build-index.sh "$PROJECT_ROOT"
```

### Otherwise: Search

1. **Check if index exists**, rebuild if not:

```bash
if [[ ! -f .knowledge-index.json ]]; then
    bash scripts/build-index.sh "$PROJECT_ROOT"
fi
```

2. **Search the index** based on query type:

#### By text query (default)
Search title, summary, and tags for matching terms:

```bash
jq --arg q "$QUERY" '
    .entries[] |
    select(
        (.title | ascii_downcase | contains($q | ascii_downcase)) or
        (.summary | ascii_downcase | contains($q | ascii_downcase)) or
        (.tags[] | ascii_downcase | contains($q | ascii_downcase))
    )
' .knowledge-index.json
```

#### By tag (`--tag`)
```bash
jq --arg tag "$TAG" '
    .entries[] | select(.tags[] == $tag)
' .knowledge-index.json
```

#### By type (`--type`)
```bash
jq --arg type "$TYPE" '
    .entries[] | select(.type == $type)
' .knowledge-index.json
```

3. **Present results** in a readable format:

```markdown
## Search Results for "[query]"

Found [N] results:

| # | Title | Type | Tags | Path |
|---|-------|------|------|------|
| 1 | [title] | [type] | [tags] | [path] |

### [1] [Title]
> [summary snippet]
Path: `[path]`
Tags: [tag1], [tag2]
```

4. **If no results**: Suggest related tags or broader search terms.

## Index Stats

Show index statistics:
```bash
jq '{total: .total, types: .types, generated: .generated}' .knowledge-index.json
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/mem` | Capture learnings (indexed) |
| `/distill` | Create knowledge entries (indexed) |
| `/example` | Save code examples (indexed) |
| `/search` | Search all knowledge (you are here) |
