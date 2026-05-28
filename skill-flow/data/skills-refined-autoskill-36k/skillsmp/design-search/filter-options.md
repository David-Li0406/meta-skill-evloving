# Filter Options and Result Processing

Filtering, ranking, and advanced result processing for design documentation
search.

## Search Parameters

### Required Parameters

**query** - Search query (keywords or phrase)

```text
Examples:
- "cache optimization"
- "event system"
- "performance"
```

### Optional Filter Parameters

**module** - Limit search to specific module

```text
Values: Any module name from design.config.json
Examples:
- effect-type-registry
- rspress-plugin-api-extractor
```

**category** - Limit to specific category

```text
Valid values:
- architecture
- performance
- observability
- testing
- integration
- other

Example:
- category: architecture
```

**status** - Filter by status

```text
Valid values:
- stub (0-20% complete)
- draft (21-60% complete)
- current (61-100% complete, up-to-date)
- needs-review (ready for review)
- archived (superseded or obsolete)

Example:
- status: current
```

**section** - Search only in specific sections

```text
Common sections:
- Overview
- Current State
- Rationale
- Implementation Details
- Future Enhancements
- Trade-offs
- Best Practices

Example:
- section: Rationale
```

**context** - Number of lines of context to show

```text
Default: 2
Range: 0-10

Examples:
- context: 0 (matched line only)
- context: 2 (2 lines before/after)
- context: 5 (5 lines before/after)
```

## Filtering Process

### Step 1: Find Target Documents

Determine which documents to search based on filters.

**All modules (no filter):**

```bash
for module in ${modules[@]}; do
  glob "*.md" --path=".claude/design/${module}"
done
```

**Specific module:**

```bash
glob "*.md" --path=".claude/design/{module}"
```

### Step 2: Apply Frontmatter Filters

**Filter by category:**

```bash
# Find docs with matching category
grep -l "category: {category}" .claude/design/**/*.md
```

**Filter by status:**

```bash
# Find docs with matching status
grep -l "status: {status}" .claude/design/**/*.md
```

**Combine filters:**

```bash
# Module + category + status
grep -l "category: architecture" .claude/design/{module}/*.md | \
  xargs grep -l "status: current"
```

### Step 3: Apply Content Filters

**Section-specific search:**

If `section` parameter provided:

1. Read each filtered file
2. Extract specified section content
3. Search within section only
4. Return matches with section context

**Example section extraction:**

```bash
# Extract content between "## Rationale" and next "##"
awk '/^## Rationale$/,/^## [^#]/' {file}
```

## Result Ranking

### Primary Ranking Factors

Results ranked by match quality:

1. **Exact phrase matches** (highest priority)
   - Query appears exactly as entered
   - Bonus for title/heading matches

2. **All words present in order**
   - All query terms found in same order
   - May have words between them

3. **All words present, any order**
   - All query terms found
   - Not necessarily in query order

4. **Most words present**
   - Subset of query terms matched
   - More terms = higher rank

5. **Partial word matches** (lowest priority)
   - Query terms partially matched
   - Substring matches

### Secondary Ranking Factors

Additional factors for tie-breaking:

**Document status weight:**

- current: +3 points
- needs-review: +2 points
- draft: +1 point
- stub: +0 points
- archived: -1 point

**Match location weight:**

- In document title: +5 points
- In section heading: +3 points
- In first paragraph: +2 points
- In body text: +1 point

**Match frequency:**

- Multiple matches in same doc: +1 point per additional match
- Matches in different sections: +2 points per section

**Recency:**

- Updated within 30 days: +2 points
- Updated within 90 days: +1 point
- Updated >180 days: -1 point

### Ranking Algorithm

```text
Score = Match_Quality_Score + Status_Weight + Location_Weight +
        Frequency_Bonus + Recency_Bonus

Sort results by Score descending
```

## Advanced Features

### Cross-Reference Analysis

When showing results, find related documentation:

**Extract related array:**

```bash
# In matched doc's frontmatter
grep -A 5 "^related:" {matched-doc}
```

**Show related docs:**

```markdown
**Related Documentation:**

- {module}/{related-doc-1}
- {module}/{related-doc-2}
```

**Find bidirectional refs:**

```bash
# Docs that reference the matched doc
grep -l "{matched-doc-name}" .claude/design/**/*.md
```

### Keyword Highlighting

Highlight matched terms in context output:

**Format:**

```text
Before context line
>>> This line contains the **MATCHED TERM** we searched for
After context line
```

**Implementation:**

- Wrap matching terms in `**...**` or `__...__`
- Preserve original capitalization
- Show full line even if match is mid-line

### Result Grouping

Group results by different dimensions:

**By Module:**

```markdown
## Module: effect-type-registry (8 matches)

- observability.md: 5 matches
- cache-optimization.md: 3 matches

## Module: rspress-plugin-api-extractor (4 matches)

- build-architecture.md: 4 matches
```

**By Category:**

```markdown
## Category: architecture (6 matches)

- build-architecture.md: 4 matches
- type-loading-vfs.md: 2 matches

## Category: performance (5 matches)

- cache-optimization.md: 3 matches
- performance-observability.md: 2 matches
```

**By Section:**

```markdown
## Section: Rationale (7 matches)

Decisions found in:
- cache-optimization.md: 3 decisions
- snapshot-tracking-system.md: 2 decisions
- observability.md: 2 decisions

## Section: Current State (5 matches)

Implementations found in:
- type-loading-vfs.md: 3 implementations
- build-architecture.md: 2 implementations
```

### Result Filtering (Post-Search)

After initial search, allow interactive filtering:

**Filter prompt:**

```markdown
## Filter Results

Found {count} matches across {modules} modules.

Available filters:

- By module: {list-modules-with-counts}
- By category: {list-categories-with-counts}
- By status: {list-statuses-with-counts}
- By section: {list-sections-with-counts}

Apply filter? (module/category/status/section/none)
```

**Example filter counts:**

```markdown
By module:
- effect-type-registry (8 matches)
- rspress-plugin-api-extractor (4 matches)

By category:
- architecture (6 matches)
- performance (5 matches)
- observability (1 match)

By status:
- current (10 matches)
- draft (2 matches)
```

## Frontmatter Extraction

For each matching document, extract metadata:

**Read frontmatter:**

```bash
head -20 {file} | grep -A 10 "^---"
```

**Extract fields:**

- `module` - Module name
- `category` - Document category
- `status` - Current status
- `completeness` - Completion percentage
- `updated` - Last update date
- `related` - Related documentation
- `dependencies` - Dependency documentation

**Use for filtering and ranking:**

```bash
# Parse frontmatter
STATUS=$(grep "^status:" {file} | cut -d' ' -f2)
CATEGORY=$(grep "^category:" {file} | cut -d' ' -f2)
COMPLETENESS=$(grep "^completeness:" {file} | cut -d' ' -f2)
UPDATED=$(grep "^updated:" {file} | cut -d' ' -f2)

# Apply to ranking
if [ "$STATUS" = "current" ]; then
  RANK_BOOST=3
fi
```

## Result Limits

### Maximum Results

**Default limits:**

- Show top 20 results
- If >20, group by relevance and show top groups
- Warn if >100 matches

**Handling too many results:**

```text
WARNING: {count} matches found

Showing top 20 results. Suggestions:
- Add filters (module, category, status)
- Use more specific search terms
- Search in specific section
```

### Result Pagination

For large result sets:

```markdown
## Results 1-20 of 87

... (show results) ...

**View more:**
- Next 20 results
- Jump to page: 1 | 2 | 3 | 4 | 5
- Show all results (warning: may be slow)
```

## Performance Optimization

### Incremental Filtering

Apply filters in order of selectivity:

1. **Module filter** (most selective if specified)
2. **Status filter** (good selectivity)
3. **Category filter** (moderate selectivity)
4. **Section filter** (requires file reading, apply last)

**Example:**

```bash
# Start with all docs
DOCS=(.claude/design/**/*.md)

# Apply module filter (if specified)
if [ -n "$MODULE" ]; then
  DOCS=(.claude/design/${MODULE}/*.md)
fi

# Apply status filter
if [ -n "$STATUS" ]; then
  DOCS=($(grep -l "status: $STATUS" "${DOCS[@]}"))
fi

# Apply category filter
if [ -n "$CATEGORY" ]; then
  DOCS=($(grep -l "category: $CATEGORY" "${DOCS[@]}"))
fi

# Now search within filtered docs
grep -rin "$QUERY" "${DOCS[@]}"
```

### Cache Frontmatter

For repeated searches, cache frontmatter:

```bash
# Cache frontmatter on first search
for doc in "${DOCS[@]}"; do
  head -20 "$doc" > "/tmp/frontmatter/$(basename $doc)"
done

# Subsequent searches read from cache
grep "status: current" /tmp/frontmatter/*.md
```

## Filter Validation

### Validate Filter Values

Before applying filters, validate:

**Module validation:**

```bash
# Check module exists in config
if ! grep -q "\"$MODULE\":" .claude/design/design.config.json; then
  echo "ERROR: Invalid module: $MODULE"
  echo "Valid modules: $(jq -r '.modules | keys[]' .claude/design/design.config.json)"
  exit 1
fi
```

**Category validation:**

```bash
VALID_CATEGORIES=(
  "architecture" "performance" "observability"
  "testing" "integration" "other"
)

if [[ ! " ${VALID_CATEGORIES[@]} " =~ " ${CATEGORY} " ]]; then
  echo "ERROR: Invalid category: $CATEGORY"
  echo "Valid categories: ${VALID_CATEGORIES[*]}"
  exit 1
fi
```

**Status validation:**

```bash
VALID_STATUSES=("stub" "draft" "current" "needs-review" "archived")

if [[ ! " ${VALID_STATUSES[@]} " =~ " ${STATUS} " ]]; then
  echo "ERROR: Invalid status: $STATUS"
  echo "Valid statuses: ${VALID_STATUSES[*]}"
  exit 1
fi
```

### Handle Missing Filters

Gracefully handle when filters match nothing:

```text
INFO: No documents match filters

**Filters:**
- module: {module}
- category: {category}
- status: {status}

**Suggestions:**
- Remove some filters
- Check filter values are correct
- Try different filter combination
```
