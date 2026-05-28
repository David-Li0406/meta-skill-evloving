# Content Identification Patterns

Specific patterns for identifying different types of prunable content in design
documentation.

## Overview

This document provides regex patterns, text markers, and structural indicators
for identifying content categories that may need pruning.

## Historical Implementation Notes

### Pattern 1: Dated Implementation Descriptions

**Text markers:**

- "On [date], we implemented..."
- "Initially, we..."
- "In version X, we..."
- "The first implementation..."
- "Originally, the system..."

**Regex patterns:**

```regex
^(On|In) \d{4}-\d{2}-\d{2}
^Initially,
^Originally,
^The (first|original) implementation
^Version \d+\.\d+ (used|introduced|implemented)
```

**Example:**

```markdown
On 2024-06-15, we implemented the disk cache using a simple LRU eviction
strategy. Initially, we considered Redis but decided against it.
```

**Action:** Move to History section or remove

### Pattern 2: Implementation Timeline

**Structural markers:**

- Sections titled "History", "Timeline", "Evolution"
- Chronological lists with dates
- Version-by-version progression

**Example:**

```markdown
## Implementation History

### Phase 1 (June 2024)
Basic caching with Map

### Phase 2 (July 2024)
Added LRU eviction

### Phase 3 (August 2024)
Disk persistence
```

**Action:** Remove entire section or condense to brief summary

### Pattern 3: Past Decision Rationales

**Text markers:**

- "We chose X because..."
- "The decision to use Y..."
- "Considered Z but rejected because..."
- "At the time, we..."

**Example:**

```markdown
We chose disk-based caching over Redis because:
1. No external dependencies
2. Lower operational cost
3. Sufficient for our use case at the time
```

**Action:** Keep if still relevant, remove if superseded

## Migration Content

### Pattern 4: Migration Instructions

**Section titles:**

- "Migrating from vX"
- "Upgrade Guide"
- "Breaking Changes"
- "Migration Steps"

**Text markers:**

- "To migrate from..."
- "If upgrading from..."
- "Legacy users should..."
- "Breaking change in v..."

**Example:**

```markdown
## Migrating from v1 to v2

1. Replace oldMethod() with newMethod()
2. Update configuration format
3. Run migration script: `npm run migrate`
```

**Action:**

- < 3 months old: Keep
- 3-6 months: Review
- > 6 months: Remove or archive

### Pattern 5: Compatibility Notes

**Text markers:**

- "For backward compatibility..."
- "Legacy support for..."
- "Deprecated but still available..."
- "Transitional period..."

**Example:**

```markdown
For backward compatibility, the old API is still available but will be
removed in v3.0.
```

**Action:** Remove if transitional period ended

## Deprecated Features

### Pattern 6: Deprecation Notices

**Text markers:**

- "⚠️ DEPRECATED"
- "❌ REMOVED"
- "🚫 Do not use"
- "Prefer X over Y (Y is deprecated)"

**Example:**

```markdown
⚠️ **DEPRECATED:** `oldMethod()` is deprecated. Use `newMethod()` instead.

The following event types are deprecated:
- `cache.hit` → use `cache:hit`
- `cache.miss` → use `cache:miss`
```

**Action:**

- If feature removed from code: Delete notice
- If deprecated > 6 months: Remove
- If deprecated recently: Keep

### Pattern 7: Feature Removal Notes

**Text markers:**

- "This feature was removed in..."
- "No longer supported as of..."
- "Removed in favor of..."

**Example:**

```markdown
Redis caching was removed in v2.0 in favor of local disk cache.
```

**Action:** Remove unless provides critical context

## Redundant Content

### Pattern 8: Duplicate Sections

**Detection method:**

Compare section content similarity using:

```text
similarity_score = matching_sentences / total_sentences

If similarity > 0.7, sections are duplicates
```

**Example:**

```markdown
## Overview
The observability system provides logging and event tracking...

## Introduction
The observability system provides logging and event tracking...
```

**Action:** Keep one, remove the other

### Pattern 9: Obvious Statements

**Text markers:**

- "This file is written in TypeScript"
- "The code is located in src/"
- "Tests verify the implementation"
- "Functions perform operations"

**Example:**

```markdown
The TypeRegistry.ts file is written in TypeScript and contains the
TypeRegistry class. The file is located in the src directory.
```

**Action:** Remove self-evident information

### Pattern 10: Over-Documented APIs

**Indicators:**

- Full API reference in design doc
- Line-by-line code explanations
- Detailed parameter descriptions
- Return value documentation

**Example:**

```markdown
## API Reference

### fetchPackage(name: string, version?: string): Promise<Package>

Fetches a package from the registry.

**Parameters:**
- `name` (string, required): The name of the package to fetch
- `version` (string, optional): The version to fetch. If not provided,
  fetches latest.

**Returns:**
Promise<Package>: A promise that resolves to a Package object

**Throws:**
- FetchError: If package not found
- NetworkError: If network request fails

**Example:**
```typescript
const pkg = await fetchPackage('zod', '3.22.0');
```

**Action:** Replace with link to auto-generated API docs

## Obsolete Information

### Pattern 11: Old Benchmarks

**Text markers:**

- "Benchmark results from [old date]"
- "As of [date], performance was..."
- "Measured on [old date]"

**Date threshold:** > 6 months old

**Example:**

```markdown
Benchmark results from June 2024:
- Cache hit: 0.05ms (avg)
- Cache miss: 15ms (avg)
- Eviction: 0.02ms (avg)
```

**Action:** Remove or update with current benchmarks

### Pattern 12: Outdated Metrics

**Text markers:**

- "Current cache hit rate: X%"
- "As of [date], we have..."
- "Recent measurements show..."

**Example:**

```markdown
As of January 2024, cache hit rate is 85% in production.
```

**Action:** Update with current metrics or remove specific date

### Pattern 13: Old Architecture References

**Detection method:**

Compare documented architecture with actual code structure:

```bash
# Documented: "Uses Redis for caching"
# Actual code: No Redis imports, uses disk cache

grep -r "redis" src/  # No matches
grep -r "DiskCache" src/  # Found

Action: Update architecture description
```

**Example:**

```markdown
The system uses Redis for distributed caching with automatic failover to
local memory cache.
```

**When code shows:** No Redis, only disk cache

**Action:** Update to reflect current architecture

### Pattern 14: Dead Links

**Detection method:**

```bash
# Extract markdown links
grep -o '\[.*\](.*.md)' doc.md

# Check if target exists
for link in ${links[@]}; do
  [ -f "$link" ] || echo "Dead link: $link"
done
```

**Example:**

```markdown
See [old implementation](./old-cache.md) for historical context.
For migration details, refer to [migration guide](./migrate-v1-v2.md).
```

**When files deleted:**

**Action:** Remove references or update to current docs

## Excessive Detail

### Pattern 15: Overly Verbose Explanations

**Indicators:**

- Paragraphs > 10 lines explaining simple concepts
- Step-by-step obvious processes
- Excessive examples

**Example:**

```markdown
The function takes a parameter called 'name' which is of type string, and
this parameter represents the name of the package that you want to fetch.
The function then makes an HTTP request to the package registry, and if
the request is successful, it returns a Promise that resolves to a Package
object, which contains all the information about the package including its
name, version, dependencies, and other metadata.
```

**Simplified version:**

```markdown
Fetches package metadata from the registry by name.
```

**Action:** Simplify to essential information

### Pattern 16: Redundant Examples

**Indicators:**

- > 3 examples showing same concept
- Examples that differ only slightly
- Obvious use cases

**Example:**

```markdown
Example 1:
```typescript
fetchPackage('zod');
```

Example 2:

```typescript
fetchPackage('effect');
```

Example 3:

```typescript
fetchPackage('ts-pattern');
```

Example 4:

```typescript
fetchPackage('@effect/schema');
```

**Action:** Keep 1-2 representative examples, remove rest

## Structural Patterns

### Pattern 17: Empty or Stub Sections

**Indicators:**

- Headings with no content
- "TODO" placeholders
- "Coming soon" notes

**Example:**

```markdown
## Performance Optimization

TODO: Document optimization strategies

## Advanced Usage

Coming soon
```

**Action:**

- If still stub after > 3 months: Remove section
- Or note as "Not yet documented"

### Pattern 18: Orphaned TODOs

**Text markers:**

- "TODO:"
- "FIXME:"
- "@todo"
- "To be completed:"

**Example:**

```markdown
TODO: Add benchmarks for cache performance
FIXME: Update this section with actual implementation details
```

**Action:**

- If TODO > 6 months old: Remove or convert to issue
- If completed: Remove TODO marker

### Pattern 19: Historical Placeholders

**Text markers:**

- "{To be filled in}"
- "{Details TBD}"
- "[Content placeholder]"
- "{Update this section}"

**Example:**

```markdown
## Cache Eviction

{Details of eviction strategy to be filled in once implemented}
```

**Action:** Remove placeholders or replace with actual content

## Age-Based Patterns

### Pattern 20: Date-Based Content

**Detection method:**

```bash
# Find all dates in document
grep -oE '\b(19|20)[0-9]{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])\b' doc.md

# Calculate age
current_date=$(date +%s)
for doc_date in ${dates[@]}; do
  age_days=$(( (current_date - doc_date_seconds) / 86400 ))
  if [ $age_days -gt 180 ]; then
    echo "Old date found: $doc_date ($age_days days old)"
  fi
done
```

**Action:**

- Dates > 1 year old: Review for staleness
- Specific dates in current state: Consider removing specificity

## Combined Pattern Analysis

### Multi-Pattern Detection

Some content exhibits multiple pruning patterns:

**Example:**

```markdown
## Implementation History

On 2024-06-15, we implemented the initial cache using Redis. Initially,
we considered local caching but decided against it. The first implementation
used a simple LRU strategy.

⚠️ **DEPRECATED:** Redis caching is deprecated as of v2.0.

For users migrating from v1.x, see the migration guide below.
```

**Patterns detected:**

1. Implementation History (title)
2. Dated implementation (On 2024-06-15)
3. Initially/considered pattern
4. Deprecation marker
5. Migration reference

**Staleness indicators:**

- Historical section: ✓
- Old dates: ✓
- Past tense: ✓
- Deprecated: ✓

**Recommendation:** High priority for removal (all patterns present)

## Pattern Priority

When multiple patterns detected, use this priority:

1. **Critical (remove first):**
   - Dead links
   - Obvious errors
   - Removed features

2. **High (likely remove):**
   - Old migrations (> 6 months)
   - Old deprecations (> 6 months)
   - Duplicate content

3. **Medium (review):**
   - Historical implementations
   - Old benchmarks
   - Excessive detail

4. **Low (keep if valuable):**
   - Past design decisions
   - Context-providing history

## Validation Patterns

After pruning, check for these anti-patterns:

### Anti-Pattern 1: Broken Flow

**Indicator:**

Section references removed content:

```markdown
As mentioned in the previous section...
(but previous section was removed)
```

**Action:** Fix references or remove orphaned text

### Anti-Pattern 2: Orphaned Headings

**Indicator:**

Heading with no content below it:

```markdown
## Performance

## Implementation
```

**Action:** Remove empty heading

### Anti-Pattern 3: Dangling Lists

**Indicator:**

Incomplete list after pruning:

```markdown
Features:
1. Caching

(items 2-5 were removed)
```

**Action:** Renumber or reformat
