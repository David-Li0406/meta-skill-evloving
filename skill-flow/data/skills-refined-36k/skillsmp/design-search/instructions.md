# Design Search Detailed Instructions

Complete step-by-step workflow for searching design documentation.

## Detailed Workflow

### 1. Parse Parameters

Extract query and optional filters from user request.

**Examples:**

- "Search for 'caching strategy'" → query: `caching strategy`
- "Find architecture docs about 'event system'" → query: `event system`,
  category: `architecture`

### 2. Load Configuration

Read `.claude/design/design.config.json` to get modules and paths.

**Configuration structure:**

```json
{
  "modules": {
    "module-name": {
      "path": ".claude/design/module-name",
      "description": "..."
    }
  }
}
```

### 3. Find Target Documents

Determine which documents to search based on filters.

**All modules:**

```bash
for module in ${modules[@]}; do
  glob "*.md" --path=".claude/design/${module}"
done
```

**Specific module:**

```bash
glob "*.md" --path=".claude/design/{module}"
```

**Apply frontmatter filters:**

- Category filter: `grep -l "category: {category}" *.md`
- Status filter: `grep -l "status: {status}" *.md`

### 4. Perform Search

Use Grep tool for full-text search:

```bash
grep -rin "{query}" .claude/design/ --include="*.md" --context={context-lines}
```

**Section-specific search:**

If `section` parameter provided, read files and extract section content before
searching.

**Algorithm:**

1. Read each target document
2. Parse markdown structure to identify sections
3. Extract content for specified section
4. Search within extracted content only
5. Report results with section context

### 5. Rank Results

Rank by match quality:

1. Exact phrase matches (highest)
2. All words present in order
3. All words present, any order
4. Most words present
5. Partial word matches (lowest)

**Secondary factors:**

- Document status (current > draft > stub)
- Match location (title > heading > body)
- Match frequency (multiple matches)
- Recency (recent updates)

**Ranking algorithm:**

```text
score = base_score + status_bonus + location_bonus + frequency_bonus + recency_bonus

base_score:
  - exact phrase: 100
  - all words in order: 75
  - all words any order: 50
  - most words: 25
  - partial: 10

status_bonus:
  - current: +20
  - draft: +10
  - stub: +0

location_bonus:
  - title: +15
  - heading: +10
  - body: +0

frequency_bonus:
  - per additional match: +5 (max +25)

recency_bonus:
  - updated this week: +10
  - updated this month: +5
  - older: +0
```

### 6. Read Frontmatter

For each matching document, extract metadata:

- module
- category
- status
- completeness
- updated date
- related docs

**Frontmatter parsing:**

```text
Read first 20 lines of document
Extract YAML between --- markers
Parse key-value pairs
Validate against schema
```

Use for filtering and ranking.

### 7. Format Results

Present results with context:

```markdown
# Design Documentation Search Results

**Query:** "{query}"
**Filters:** {filters if any}
**Results:** {count} matches in {doc-count} documents

---

## {module}/{doc-name} ({category})

**Status:** {status} | **Completeness:** {completeness}% |
**Updated:** {date}

### Match 1: Line {line-number}

**Section:** {section-name}

**Context:**

{before-context}
>>> {matched-line}
{after-context}

**Full document:** `.claude/design/{module}/{doc-name}.md:{line-number}`

---

## Summary

**Top Results:** {ranked-list}

**Related Topics:** {topics}

**Suggestions:** {recommendations}
```

**Formatting guidelines:**

- Show top 20 results by default
- Group results by document
- Highlight matched text with `>>>`
- Include 2 lines of context before/after
- Provide clickable file paths with line numbers
- Show document metadata for context

### 8. Provide Navigation

For each result, provide clear paths:

- **Read full doc:** `.claude/design/{module}/{doc}.md`
- **Jump to match:** `.claude/design/{module}/{doc}.md:{line}`
- **View section:** `.claude/design/{module}/{doc}.md#{section}`

**Navigation patterns:**

1. Direct file path for reading entire document
2. File path with line number for jumping to match
3. File path with anchor for viewing specific section
4. Related docs links from frontmatter

### 9. Handle Edge Cases

**No results:**

1. Confirm search was executed correctly
2. Try broader search terms
3. Remove filters one by one
4. Suggest related search terms
5. Check for typos in query

**Too many results:**

1. Show warning about result count
2. Display top 20 by ranking
3. Suggest adding filters
4. Recommend more specific query
5. Group results by module/category

**Invalid filters:**

1. Identify invalid filter name or value
2. Show valid options
3. Suggest correction
4. Continue search without invalid filter
5. Explain filter usage

### 10. Suggest Related Searches

Based on results, suggest:

- Related topics from frontmatter
- Linked documents
- Same category documents
- Same module documents
- Recent updates in related areas

## Performance Optimization

### Search Scope Reduction

1. Apply module filter first (biggest reduction)
2. Apply category filter second
3. Apply status filter last
4. Only then perform text search

### Caching Strategies

1. Cache frontmatter for all docs (5 minute TTL)
2. Cache module structure (10 minute TTL)
3. Don't cache search results (always fresh)

### Parallel Processing

1. Search multiple modules in parallel
2. Parse frontmatter in parallel
3. Rank results after all searches complete

### Result Limits

1. Default limit: 20 results
2. Maximum limit: 100 results
3. User can override with `--limit` parameter
4. Warn if truncating results

## Output Customization

### Format Options

- `--format=markdown` (default): Rich markdown output
- `--format=simple`: Just file paths and line numbers
- `--format=json`: Machine-readable JSON

### Context Control

- `--context=N`: Show N lines of context (default: 2)
- `--no-context`: Just show matched line
- `--full-section`: Show entire section containing match

### Grouping Options

- `--group-by=document` (default): Group by document
- `--group-by=module`: Group by module
- `--group-by=category`: Group by category
- `--no-group`: Flat list of matches
