# Pruning Strategies

Guidelines for different pruning modes and content categorization.

## Overview

Design doc pruning uses different strategies based on:

1. How aggressive the pruning should be
2. What content categories to target
3. Whether to preserve historical context
4. Document size and health

## Pruning Modes

### Conservative Mode

Only remove obviously outdated content with minimal risk.

#### Conservative Targets

**Remove:**

- Completed migrations (> 1 year old)
- Very old benchmarks (> 1 year old)
- Deprecated features (> 1 year old and fully removed from code)
- Clear duplicates (exact repetition)

**Keep:**

- Historical context (even if old)
- Design rationales
- Migration guides (even if old)
- Deprecated features (< 1 year)

#### Conservative Use Cases

- First-time pruning
- Critical documentation
- Regulatory/compliance docs
- Risk-averse environments

#### Conservative Example

```markdown
Before: 1,000 lines
After: 920 lines
Reduction: 80 lines (8%)

Removed:
- Migration from v1.0 (18 months old) - 45 lines
- Benchmarks from 2024 - 25 lines
- Duplicate overview section - 10 lines
```

### Normal Mode (Default)

Balanced pruning that removes stale content while preserving valuable context.

#### Normal Targets

**Remove:**

- Implementation history (unless critical context)
- Old migrations (> 6 months)
- Old benchmarks (> 6 months)
- Deprecated features (> 6 months)
- Redundant sections
- Excessive API documentation (link to auto-generated docs instead)

**Keep:**

- Important design rationales
- Recent decisions (< 6 months)
- Valuable historical context
- Current implementation details

#### Normal Use Cases

- Regular maintenance
- Quarterly doc reviews
- After major refactors
- Preparing for releases

#### Normal Example

```markdown
Before: 1,000 lines
After: 720 lines
Reduction: 280 lines (28%)

Removed:
- Implementation timeline - 78 lines
- Migration guides - 67 lines
- Old benchmarks - 24 lines
- Deprecated events - 30 lines
- Redundant sections - 81 lines
```

### Aggressive Mode

Maximum reduction, removing all historical content to focus only on current
state.

#### Aggressive Targets

**Remove:**

- All historical content
- All migration guides
- All old rationales
- Excessive detail
- Redundant explanations
- All deprecation notices
- Past design decisions
- Implementation timelines

**Keep:**

- Current implementation only
- Active design decisions
- Essential rationale
- Future enhancements

#### Aggressive Use Cases

- Stub docs to complete
- Overly historical docs
- Fresh start after major rewrite
- Minimalist documentation philosophy

#### Aggressive Example

```markdown
Before: 1,000 lines
After: 600 lines
Reduction: 400 lines (40%)

Removed:
- All history sections - 180 lines
- All migration content - 95 lines
- Old decision rationales - 65 lines
- Excessive detail - 60 lines
```

## Content Categories

### Category 1: Keep Always

Content that should never be pruned.

#### Current Implementation

**Description:** How the system currently works

**Examples:**

- Current architecture
- Active components
- Live API endpoints
- Production configuration

**Why keep:** Essential reference for working with the system

#### Active Design Decisions

**Description:** Why current approach was chosen

**Examples:**

- "We use Effect-TS for fault tolerance"
- "Cache uses LRU eviction for memory efficiency"
- "TypeScript strict mode enabled for type safety"

**Why keep:** Prevents repeating past mistakes, guides future changes

#### Recent Information

**Description:** Content from last 3-6 months

**Examples:**

- Recent benchmarks
- New features added
- Latest architecture changes

**Why keep:** Still current and relevant

#### Future Enhancements

**Description:** Planned work and roadmap

**Examples:**

- Phase 2: Add metrics collection
- TODO: Optimize cache eviction
- Future: Support streaming responses

**Why keep:** Guides development direction

### Category 2: Review Carefully

Content that might be valuable but could be pruned.

#### Historical Context

**Description:** How things used to work or why changes were made

**Decision criteria:**

- Is this context needed to understand current state?
- Does it explain a non-obvious decision?
- Would removing it cause confusion?

**Examples to keep:**

```markdown
Why we don't use Redis:

Considered Redis for distributed caching but chose local disk cache because:
- Deployment complexity (no Redis dependency)
- Cost (no Redis hosting)
- Performance sufficient for use case

This decision still stands.
```

**Examples to remove:**

```markdown
Version History:

v1.0 (June 2024): Initial release with basic caching
v1.1 (July 2024): Added TTL support
v1.2 (August 2024): Improved eviction
...
```

#### Old Design Decisions

**Description:** Past decisions that may no longer apply

**Decision criteria:**

- Does it explain current architecture?
- Is it referenced elsewhere?
- Could it prevent future rework?

**Keep if:** Still provides valuable context
**Remove if:** Superseded by current decisions

#### Migration Guides

**Description:** Instructions for upgrading from old versions

**Decision criteria:**

- How old is the version being migrated from?
- Do users still need this?
- Is migration window closed?

**Age thresholds:**

- < 3 months: Keep
- 3-6 months: Review
- 6-12 months: Likely remove
- > 12 months: Definitely remove

#### Deprecated Features

**Description:** Features marked for removal

**Decision criteria:**

- Is feature still in code?
- How long ago was it deprecated?
- Are users still migrating?

**Status-based:**

- Deprecated but active: Keep notice
- Deprecated > 6 months: Remove notice
- Fully removed from code: Remove entirely

### Category 3: Remove Freely

Content that should almost always be pruned.

#### Old Implementations

**Description:** How things used to work

**Examples:**

```markdown
Original Implementation (2024):

The cache originally used a simple Map with manual eviction...
```

**Action:** Remove unless critical context

#### Completed Migrations

**Description:** Past upgrade instructions

**Examples:**

```markdown
Migrating from v1 to v2:

1. Replace oldMethod() with newMethod()
2. Update config format
3. Run migration script
```

**Action:** Remove if migration window closed (> 6 months)

#### Obsolete Benchmarks

**Description:** Old performance measurements

**Examples:**

```markdown
Benchmark (June 2024):
- Cache hit: 0.05ms
- Fetch: 15ms
```

**Action:** Remove if > 6 months old or architecture changed

#### Clear Redundancy

**Description:** Duplicate information

**Examples:**

- Same paragraph in multiple sections
- API docs repeated from auto-generated docs
- Obvious statements

**Action:** Always remove, keep single copy in best location

#### Dead Links

**Description:** References to deleted content

**Examples:**

```markdown
See old-architecture.md for details (deleted)
Refer to the deprecated section above (removed)
```

**Action:** Always remove or update

## Staleness Scoring

### Staleness Algorithm

```text
staleness_score = (
  age_factor * 0.3 +
  date_mentions * 0.2 +
  past_tense_ratio * 0.2 +
  deprecation_markers * 0.2 +
  redundancy_score * 0.1
) * 100

Where:
- age_factor = days_since_update / 365 (capped at 1.0)
- date_mentions = count of specific dates / section_lines
- past_tense_ratio = past_tense_verbs / total_verbs
- deprecation_markers = presence of "deprecated", "old", "legacy" (0 or 1)
- redundancy_score = similarity to other sections (0.0-1.0)
```

### Staleness Thresholds

**0-30: Fresh** ✅

- Recently updated
- Current information
- Keep as-is

**31-60: Aging** ⚠️

- Getting old but still relevant
- Review for accuracy
- Update or keep

**61-80: Stale** 🟡

- Likely outdated
- Strong candidate for pruning
- Archive or update

**81-100: Very Stale** 🔴

- Definitely outdated
- Prune immediately
- Archive if valuable

### Staleness Example

#### Section: "Implementation History"

```text
Content:
"In June 2024, we implemented the initial cache system using Redis.
By July 2024, we had switched to disk-based caching.
The old Redis implementation was deprecated in August 2024."

Analysis:
- age_factor: 7 months / 12 = 0.58
- date_mentions: 3 dates / 3 lines = 1.0
- past_tense_ratio: 5 past / 5 total = 1.0
- deprecation_markers: 1 (contains "deprecated")
- redundancy_score: 0.3 (similar to other sections)

staleness_score = (0.58 * 0.3 + 1.0 * 0.2 + 1.0 * 0.2 +
                   1.0 * 0.2 + 0.3 * 0.1) * 100
               = (0.174 + 0.2 + 0.2 + 0.2 + 0.03) * 100
               = 0.804 * 100
               = 80.4

Result: Stale (80.4/100) - strong candidate for removal
```

## Decision Framework

Use this framework to decide what to prune:

### Step 1: Identify Content Type

Is it:

- Current implementation? → Keep Always
- Active decision? → Keep Always
- Recent addition? → Keep Always
- Future plan? → Keep Always
- Historical context? → Review Carefully
- Old decision? → Review Carefully
- Migration guide? → Review Carefully
- Deprecated feature? → Review Carefully
- Old implementation? → Remove Freely
- Completed migration? → Remove Freely
- Old benchmark? → Remove Freely
- Duplicate content? → Remove Freely
- Dead link? → Remove Freely

### Step 2: Check Staleness

- Fresh (0-30)? → Keep
- Aging (31-60)? → Review
- Stale (61-80)? → Likely prune
- Very stale (81-100)? → Definitely prune

### Step 3: Consider Mode

- Conservative? → Only remove if > 1 year old and obvious
- Normal? → Remove if stale and not critical
- Aggressive? → Remove all historical content

### Step 4: Archive Decision

Should removed content be archived?

**Archive if:**

- Provides historical value
- May be needed for reference
- Explains past decisions
- Migration guide still needed by some

**Don't archive if:**

- Clearly wrong information
- No historical value
- Fully superseded
- Pure duplication

## Mode Selection Guide

### When to Use Conservative

- First pruning session
- Documentation is critical
- Compliance requirements
- Uncertain about impact
- Users depend on history

### When to Use Normal

- Regular maintenance
- Balanced approach needed
- After major changes
- Preparing for release
- Quarterly reviews

### When to Use Aggressive

- Starting fresh
- Doc is 90% history
- Major rewrite completed
- Minimalist preference
- After archiving old version

## Success Metrics

### Pruning Effectiveness

**Good pruning:**

- 10-30% size reduction
- Improved focus
- Easier to maintain
- Faster to read

**Too conservative:**

- < 10% reduction
- Still has cruft
- Missed opportunities

**Too aggressive:**

- > 40% reduction
- Lost valuable context
- May need to restore

### Quality Indicators

**After pruning, check:**

- ✅ Current state well documented
- ✅ Active decisions explained
- ✅ No broken references
- ✅ Clear and focused
- ✅ Valuable history archived
- ✅ No essential information lost
