# Search Usage Examples

Complete examples of design-search skill usage in different scenarios.

## Example 1: Simple Keyword Search

**User request:**

> Search for "observability"

**Execution:**

1. Parse query: "observability"
2. No filters specified
3. Search all design docs
4. Rank and format results

**Output:**

```markdown
# Design Documentation Search Results

**Query:** "observability"
**Results:** 12 matches in 4 documents

---

## effect-type-registry/observability.md (observability)

**Status:** current | **Completeness:** 85% | **Updated:** 2026-01-15

### Match 1: Line 15 (Overview)

**Context:**

```text
This design document covers the observability architecture for the
>>> effect-type-registry package. The observability system uses an
event-based approach with structured logging.

**Full document:**
`.claude/design/effect-type-registry/observability.md:15`

### Match 2: Line 245 (Event System)

**Context:**

```text
## Event System

>>> The observability event system emits structured events that can be
consumed by logging, metrics, and monitoring systems.

**Full document:**
`.claude/design/effect-type-registry/observability.md:245`

---

## rspress-plugin-api-extractor/performance-observability.md (performance)

**Status:** current | **Completeness:** 70% | **Updated:** 2026-01-10

### Match 1: Line 32 (Overview)

**Context:**

```text
This document describes the performance observability features for
>>> tracking build times, cache hit rates, and other performance metrics
in the API extractor plugin.

**Full document:**
`.claude/design/rspress-plugin-api-extractor/performance-observability.md:32`

---

## Example 1 Summary

**Top Results:**

1. effect-type-registry/observability.md - 7 matches (primary doc)
2. rspress-plugin-api-extractor/performance-observability.md - 3 matches
3. effect-type-registry/architecture.md - 2 mentions

**Related Topics:**

- logging (3 docs)
- events (2 docs)
- metrics (2 docs)

**Suggestions:**

- Review effect-type-registry/observability.md for comprehensive
  observability docs
- See performance-observability.md for build performance tracking


## Example 2: Category-Filtered Search

**User request:**

> Find architecture docs about "data flow"

**Execution:**

1. Parse query: "data flow"
2. Filter: category=architecture
3. Find all architecture docs
4. Search within filtered docs
5. Rank and format

**Output:**

```markdown
# Design Documentation Search Results

**Query:** "data flow"
**Filters:** category=architecture
**Results:** 5 matches in 2 documents

---

## rspress-plugin-api-extractor/build-architecture.md (architecture)

**Status:** current | **Completeness:** 90% | **Updated:** 2026-01-12

### Match 1: Line 156 (Data Flow)

**Section:** Data Flow

**Context:**

```text
## Data Flow

>>> The data flow through the build system follows this pattern:
1. API Extractor reads source files
2. Type definitions are loaded via effect-type-registry

**Full document:**
`.claude/design/rspress-plugin-api-extractor/build-architecture.md:156`

### Match 2: Line 203 (Pipeline)

**Context:**

```text
The pipeline processes data in stages, with each stage transforming
>>> the data flow before passing to the next stage. This ensures clear
separation of concerns and testability.

**Full document:**
`.claude/design/rspress-plugin-api-extractor/build-architecture.md:203`

---

## effect-type-registry/architecture.md (architecture)

**Status:** current | **Completeness:** 85% | **Updated:** 2026-01-10

### Match 1: Line 89 (Component Interaction)

**Context:**

```text
## Component Interaction

>>> Components communicate through well-defined interfaces. The data flow
starts with the PackageFetcher and flows through the cache layer.

**Full document:**
`.claude/design/effect-type-registry/architecture.md:89`

---

## Example 2 Summary

**All architecture docs searched:** 3
**Matching docs:** 2
**Total matches:** 5

**Suggestion:** Both docs describe data flow in their respective systems.
Review build-architecture.md for comprehensive pipeline documentation.


## Example 3: Section-Specific Search

**User request:**

> Find all Rationale sections mentioning "performance"

**Execution:**

1. Parse query: "performance"
2. Filter: section=Rationale
3. Read all design docs
4. Extract Rationale sections
5. Search within Rationale only
6. Return with decision context

**Output:**

```markdown
# Design Documentation Search Results

**Query:** "performance"
**Filters:** section=Rationale
**Results:** 8 matches in 5 documents

---

## effect-type-registry/cache-optimization.md

**Decision Found:** Disk-based caching over in-memory

**Context:** Chose disk caching to reduce memory usage while maintaining
good performance. Trade-off: slightly slower access times for significant
memory savings.

**Rationale (excerpt):**

```text
## Rationale

We chose disk-based caching over in-memory for several reasons:

1. **Memory efficiency:** Large type definitions consume significant memory
2. **Performance:** Disk I/O is fast enough for our use case (<10ms reads)
>>> 3. **Persistence:** Survives process restarts, better performance
   across sessions

**Full rationale:**
`.claude/design/effect-type-registry/cache-optimization.md:125`

---

## rspress-plugin-api-extractor/snapshot-tracking-system.md

**Decision Found:** SHA-based change detection

**Context:** SHA comparison chosen for performance over deep equality checks.

**Rationale (excerpt):**

```text
## Rationale

>>> SHA-based change detection provides excellent performance compared to
deep object equality checks. Computing SHA-256 of JSON is O(n) where n is
the serialized size, but deep equality is O(n*m) for nested structures.

**Full rationale:**
`.claude/design/rspress-plugin-api-extractor/snapshot-tracking-system.md:203`

---

## Example 3 Summary

**Performance-related decisions found:** 8

**Common themes:**

- Caching strategies (3 docs)
- Optimization techniques (2 docs)
- Benchmarking (2 docs)

**Insights:**

Performance considerations appear frequently in Rationale sections,
indicating careful analysis of trade-offs. Most decisions prioritize
measurable performance gains.


## Example 4: Module-Filtered Search

**User request:**

> Search effect-type-registry docs for "cache"

**Execution:**

1. Parse query: "cache"
2. Filter: module=effect-type-registry
3. Find all docs in module
4. Search and rank

**Output:**

```markdown
# Design Documentation Search Results

**Query:** "cache"
**Filters:** module=effect-type-registry
**Results:** 23 matches in 3 documents

---

## effect-type-registry/cache-optimization.md (performance)

**Status:** current | **Completeness:** 80% | **Updated:** 2026-01-15

### Match 1: Line 12 (Overview)

**Context:**

```text
# Cache Optimization

>>> This document describes the cache optimization strategies used in
effect-type-registry to minimize redundant package fetches.

**Full document:**
`.claude/design/effect-type-registry/cache-optimization.md:12`

**Additional matches:** 15 more matches in this document

---

## effect-type-registry/observability.md (observability)

**Status:** current | **Completeness:** 85% | **Updated:** 2026-01-15

### Match 1: Line 156 (Metrics)

**Context:**

```text
## Metrics

>>> Cache hit rates are tracked via the observability system:
- cache_hit: Successful cache retrieval
- cache_miss: Cache miss, fetch required

**Full document:**
`.claude/design/effect-type-registry/observability.md:156`

**Additional matches:** 4 more matches in this document

---

## effect-type-registry/architecture.md (architecture)

**Status:** current | **Completeness:** 85% | **Updated:** 2026-01-10

### Match 1: Line 203 (Components)

**Context:**

```text
## Cache Layer

>>> The cache layer sits between the PackageFetcher and consumers,
providing transparent caching of type definitions.

**Full document:**
`.claude/design/effect-type-registry/architecture.md:203`

**Additional matches:** 2 more matches in this document

---

## Example 4 Summary

**Top Results:**

1. cache-optimization.md - 16 matches (primary doc)
2. observability.md - 5 matches (metrics and events)
3. architecture.md - 3 matches (component overview)

**Recommendation:**

Start with cache-optimization.md for comprehensive cache documentation.
See observability.md for cache metrics and monitoring.


## Example 5: Multi-Filter Search

**User request:**

> Find current performance docs mentioning "optimization"

**Execution:**

1. Parse query: "optimization"
2. Filters: status=current, category=performance
3. Apply filters in order
4. Search filtered set

**Output:**

```markdown
# Design Documentation Search Results

**Query:** "optimization"
**Filters:** status=current, category=performance
**Results:** 18 matches in 2 documents

---

## effect-type-registry/cache-optimization.md (performance)

**Status:** current | **Completeness:** 80% | **Updated:** 2026-01-15

**Matches:** 12 occurrences

**Key sections:**

- Overview: Cache optimization strategies
- Rationale: Why disk-based caching
- Implementation: Optimization techniques
- Benchmarks: Performance improvements

**Top match:**

```text
>>> Cache optimization reduced package fetch times by 90% for repeated
builds, from average 450ms to 45ms per package.

**Full document:**
`.claude/design/effect-type-registry/cache-optimization.md`

---

## rspress-plugin-api-extractor/performance-observability.md (performance)

**Status:** current | **Completeness:** 70% | **Updated:** 2026-01-10

**Matches:** 6 occurrences

**Key sections:**

- Overview: Performance tracking
- Metrics: Optimization metrics
- Future: Planned optimizations

**Top match:**

```text
>>> Performance optimization opportunities are identified through
continuous monitoring of build times and cache metrics.

**Full document:**
`.claude/design/rspress-plugin-api-extractor/performance-observability.md`

---

## Example 5 Summary

**Documents searched:** 2 current performance docs
**Total matches:** 18

Both docs focus on optimization strategies with measurable results.
cache-optimization.md has more detailed optimization techniques.


## Example 6: No Results

**User request:**

> Search for "kubernetes"

**Execution:**

1. Parse query: "kubernetes"
2. Search all docs
3. No matches found

**Output:**

```text
INFO: No matches found

**Query:** "kubernetes"
**Documents searched:** 15

**Suggestions:**

- Try broader search terms (e.g., "container", "deployment")
- Check spelling
- Search for related concepts
- This topic may not be documented yet

## Example 7: Too Many Results

**User request:**

> Search for "system"

**Execution:**

1. Parse query: "system"
2. Search finds 150+ matches
3. Warn and show top results

**Output:**

```text
WARNING: Too many results (157 matches)

**Query:** "system"
**Results:** 157 matches in 12 documents

**Suggestions:**

- Add filters (module, category, status)
- Use more specific search terms
- Search in specific section

**Showing top 20 results...**

---

## effect-type-registry/observability.md

### Match 1: Line 15

```text
>>> The observability system uses an event-based approach for tracking
package fetches, cache operations, and errors.

... (19 more top results) ...

---

**Filter to narrow results:**

By module:

- effect-type-registry (89 matches)
- rspress-plugin-api-extractor (68 matches)

By category:

- architecture (56 matches)
- observability (45 matches)
- performance (32 matches)


## Example 8: Find Implementation Locations

**User request:**

> Search for "src/TypeRegistry.ts"

**Execution:**

1. Parse query: "src/TypeRegistry.ts"
2. Search for file path references
3. Return implementation docs

**Output:**

```markdown
# Design Documentation Search Results

**Query:** "src/TypeRegistry.ts"
**Results:** 5 matches in 2 documents

---

## effect-type-registry/architecture.md

**Implementation Found:** TypeRegistry core component

**Location:** `src/TypeRegistry.ts`

**Status:** Implemented (current)

**Context:**

```text
## Core Components

### TypeRegistry

>>> Implemented in `src/TypeRegistry.ts`, the TypeRegistry maintains
the registry of loaded type definitions and provides the main API.

**Full details:**
`.claude/design/effect-type-registry/architecture.md:89`

---

## effect-type-registry/observability.md

**References to TypeRegistry implementation:**

```text
>>> Events are emitted from `src/TypeRegistry.ts` when packages are
loaded, cached, or fail to load.

**Full details:**
`.claude/design/effect-type-registry/observability.md:203`

---

## Example 8 Summary

**Implementation documentation found for:** src/TypeRegistry.ts

**Covered in:**

1. architecture.md - Component overview and design
2. observability.md - Event emission points

**Related files mentioned:**

- src/PackageFetcher.ts
- src/cache/DiskCache.ts


## Example 9: Find Decisions

**User request:**

> Search Rationale sections for "chose"

**Execution:**

1. Parse query: "chose"
2. Filter: section=Rationale
3. Extract decision context

**Output:**

```markdown
# Design Documentation Search Results

**Query:** "chose"
**Filters:** section=Rationale
**Results:** 6 decisions found

---

## Decision 1: Disk-based caching

**Document:** effect-type-registry/cache-optimization.md

**Decision:**

```text
>>> We chose disk-based caching over in-memory caching for persistence
and memory efficiency.

**Options considered:** In-memory, disk-based, hybrid

**Trade-offs:** Slower access (10ms) vs memory savings (95% reduction)

**Full rationale:** Line 125

---

## Decision 2: SHA-256 for change detection

**Document:** rspress-plugin-api-extractor/snapshot-tracking-system.md

**Decision:**

```text
>>> We chose SHA-256 over deep equality for performance and reliability.

**Options considered:** Deep equality, SHA-256, timestamps

**Trade-offs:** Hash computation overhead vs deep comparison complexity

**Full rationale:** Line 203

---

## Example 9 Summary

**Decisions found:** 6
**Average completeness:** 82%

All decisions include alternatives considered and clear rationale for
the chosen approach.

