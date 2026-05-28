# Comparison Formats

Different output formats for comparing design documentation versions.

## Overview

The design-compare skill supports multiple output formats, each suited for
different use cases:

1. **Unified** - Standard diff format
2. **Side-by-side** - Visual comparison
3. **Summary** - High-level statistics
4. **Semantic** - Section-level changes

## Format 1: Unified Diff

Standard unified diff format showing changes line by line.

### When to Use Unified

- Detailed code review
- Tracking specific edits
- Understanding exact modifications
- Git-style workflow

### Unified Format Structure

```diff
diff --git a/.claude/design/module/doc.md
index abc123..def456 100644
--- a/.claude/design/module/doc.md
+++ b/.claude/design/module/doc.md
@@ -45,7 +45,12 @@ The observability system provides:

 ## Event System

-Basic event emitter for tracking operations.
+Comprehensive event-based observability architecture:
+
+- Event emission for all operations
+- Structured event payloads
+- Type-safe event handlers
+- Performance tracking

 ## Future Enhancements
```

### Unified Format Components

**Header:**

```diff
diff --git a/.claude/design/module/doc.md
index abc123..def456 100644
```

- File path being compared
- Old and new blob hashes

**File markers:**

```diff
--- a/.claude/design/module/doc.md
+++ b/.claude/design/module/doc.md
```

- `---` marks old version
- `+++` marks new version

**Hunk header:**

```diff
@@ -45,7 +45,12 @@
```

- `-45,7`: Starting at line 45, 7 lines in old version
- `+45,12`: Starting at line 45, 12 lines in new version

**Change markers:**

- ` ` (space): Unchanged context line
- `-`: Removed line
- `+`: Added line

### Unified Generation Command

```bash
git diff --unified=${context_lines} \
  ${ref_commit} ${base_commit} -- ${doc_path}
```

**Parameters:**

- `context_lines`: Lines of context around changes (default: 3)
- `ref_commit`: Older commit to compare from
- `base_commit`: Newer commit to compare to
- `doc_path`: Path to design document

### Unified Example Output

```markdown
# Unified Diff Comparison

**Document:** observability.md
**Module:** effect-type-registry
**Format:** Unified (3 lines context)

## Versions

**Base:** abc123 (2026-01-15) - "Add observability"
**Current:** def456 (2026-01-17) - "Update with events"

## Diff

```diff
diff --git a/.claude/design/effect-type-registry/observability.md
index abc123..def456 100644
--- a/.claude/design/effect-type-registry/observability.md
+++ b/.claude/design/effect-type-registry/observability.md
@@ -1,7 +1,7 @@
 ---
 status: draft
-completeness: 60
-updated: 2026-01-15
+completeness: 85
+updated: 2026-01-17
 ---

 # Observability System
@@ -23,8 +23,15 @@ Provides event-based observability.

 ## Event System

-Basic event emitter for tracking operations.
+Comprehensive event-based observability:

+### Features
+
+- Event emission for all operations
+- Structured event payloads
+- Type-safe event handlers
+- Performance tracking
+
+See [Event Architecture](./event-architecture.md) for details.

 ## Metrics
```

**Statistics:** +12 lines, -2 lines (10 net addition)

## Format 2: Side-by-Side

Visual side-by-side comparison showing old and new versions.

### When to Use Side-by-Side

- Visual review
- Understanding content evolution
- Presenting to stakeholders
- High-level comparison

### Side-by-Side Generation

```bash
# Using git's word diff
git diff --color-words --word-diff=porcelain \
  ${ref_commit} ${base_commit} -- ${doc_path}

# Using delta (if available)
git diff ${ref_commit} ${base_commit} -- ${doc_path} | delta --side-by-side

# Fallback: generate manually
diff --side-by-side --width=120 <(git show ${ref}:${path}) <(git show ${base}:${path})
```

### Side-by-Side Format Structure

```text
Base (abc123)                     | Current (def456)
----------------------------------|----------------------------------
status: draft                     | status: current
completeness: 60                  | completeness: 85
                                  |
## Event System                   | ## Event System
                                  |
Basic event emitter               | Comprehensive event-based
                                  | observability:
                                  |
                                  | ### Features
                                  |
                                  | - Event emission
                                  | - Structured payloads
```

### Side-by-Side Example Output

```markdown
# Side-by-Side Comparison

**Document:** observability.md
**Module:** effect-type-registry

## Versions

Left: abc123 (2026-01-15) - Base
Right: def456 (2026-01-17) - Current

## Visual Comparison

```text
BASE (abc123)                           CURRENT (def456)
====================================    ====================================

---                                     ---
status: draft                           status: current
completeness: 60                        completeness: 85
updated: 2026-01-15                     updated: 2026-01-17
---                                     ---

# Observability System                 # Observability System

Event-based observability for           Event-based observability for
the type registry.                      the type registry.

## Overview                             ## Overview

Provides monitoring and tracking.       Provides comprehensive monitoring,
                                        tracking, and performance analysis.

## Event System                         ## Event System

Basic event emitter for tracking        Comprehensive event-based
operations.                             observability architecture:

                                        ### Features

                                        - Event emission for all operations
                                        - Structured event payloads
                                        - Type-safe event handlers
                                        - Performance tracking
```

**Key differences:**

- Status: draft → current
- Completeness: +25%
- Added Features section with 4 items

## Format 3: Summary

High-level statistical summary without line-by-line details.

### When to Use Summary

- Quick overview
- Progress tracking
- Metrics reporting
- High-level audit

### Summary Generation

```bash
# Get diff statistics
git diff --stat ${ref_commit} ${base_commit} -- ${doc_path}

# Count changes
git diff --numstat ${ref_commit} ${base_commit} -- ${doc_path}

# Word diff for word count
git diff --word-diff=porcelain ${ref_commit} ${base_commit} -- ${doc_path}
```

### Summary Format Structure

```markdown
# Comparison Summary

**Document:** {doc}
**Module:** {module}

## Versions

**Base:** {commit} ({date})
**Current:** {commit} ({date})
**Time span:** {duration}

## Statistics

- **Lines added:** {count}
- **Lines removed:** {count}
- **Net change:** {+/-count}
- **Words added:** {count}
- **Words removed:** {count}
- **Sections modified:** {count}
- **Code blocks added:** {count}

## Significant Changes

- {highlight 1}
- {highlight 2}
- {highlight 3}
```

### Summary Example Output

```markdown
# Comparison Summary

**Document:** observability.md
**Module:** effect-type-registry
**Format:** Summary

## Versions Compared

### Base (Reference)

- **Commit:** abc123def456
- **Date:** 2026-01-15 14:30 UTC
- **Author:** John Doe
- **Message:** "Add observability system"

### Current (Comparing)

- **Commit:** def456abc789
- **Date:** 2026-01-17 10:15 UTC
- **Author:** Jane Smith
- **Message:** "Update with event architecture"

**Time span:** 2 days

## Change Statistics

**Lines:**

- Added: +45 lines
- Removed: -8 lines
- Net change: +37 lines (12% increase)

**Words:**

- Added: +340 words
- Removed: -45 words
- Net change: +295 words (58% increase)

**Structure:**

- Sections modified: 3
- New sections: 2
- Removed sections: 1
- Code blocks added: 3

## Significant Changes

⚠️ **Status Change:** draft → current (promoted to production)

📈 **Completeness Jump:** 60% → 85% (+25%)

✨ **Major Addition:** Event System Architecture (+45 lines)

🔧 **Structural Change:** Added 2 new major sections

📝 **Content Expansion:** 58% increase in word count

## Quick Insights

- Document matured significantly (draft to current)
- Major feature addition (Event System)
- Completeness improved substantially
- Content nearly doubled in size
- Ready for production use
```

## Format 4: Semantic

Section-level semantic analysis of changes.

### When to Use Semantic

- Understanding structural changes
- Tracking content organization
- Documentation evolution
- Architecture review

### Semantic Analysis Process

#### Step 1: Extract sections

```bash
# Get section headings from base
git show ${ref}:${path} | grep '^##' | sed 's/^## //'

# Get section headings from current
git show ${base}:${path} | grep '^##' | sed 's/^## //'
```

#### Step 2: Compare sections

- Identify added sections
- Identify removed sections
- Identify modified sections
- Calculate change magnitude

#### Step 3: Analyze content

For each section:

- Count line changes
- Detect content type changes (text, code, lists)
- Identify nature of changes (expansion, clarification, reorganization)

### Semantic Format Structure

```markdown
# Semantic Comparison

## Sections Added

- {Section name} ({lines})
  - {Description}

## Sections Removed

- {Section name} ({lines})
  - {Reason}

## Sections Modified

### {Section name} ({lines changed})

- {Nature of changes}
- {Key modifications}

## Sections Unchanged

- {Section name}
```

### Semantic Example Output

```markdown
# Semantic Comparison

**Document:** observability.md
**Module:** effect-type-registry
**Format:** Semantic (section-level analysis)

## Versions

**Base:** abc123 (2026-01-15)
**Current:** def456 (2026-01-17)

## Sections Added (2)

### 1. Event System Architecture

**Lines:** 45
**Location:** After Overview section

**Content:**

- Comprehensive event architecture description
- Type-safe event handler system
- Event emission patterns
- Performance tracking integration

**Significance:** Major feature addition

### 2. Performance Characteristics

**Lines:** 28
**Location:** Before Future Enhancements

**Content:**

- Benchmark results
- Performance metrics
- Overhead analysis
- Optimization notes

**Significance:** Production readiness documentation

## Sections Removed (1)

### 1. Old Implementation Notes

**Lines:** 8
**Previously:** After Current State

**Content removed:**

- Historical implementation timeline
- Early prototype notes

**Reason:** Pruned historical content, no longer relevant

## Sections Modified (3)

### 1. Overview (+12 lines)

**Nature:** Content expansion

**Changes:**

- Added event-based approach description
- Expanded system capabilities list
- Updated terminology

**Impact:** Better introduction for new readers

### 2. Current State (+23 lines)

**Nature:** Implementation details added

**Changes:**

- Added code examples (3 blocks)
- Expanded architecture explanation
- Added cross-references to new sections

**Impact:** Much more comprehensive implementation guide

### 3. Future Enhancements (+5 lines)

**Nature:** Roadmap update

**Changes:**

- Added Phase 2 items
- Updated priorities
- Removed completed items

**Impact:** Clearer development direction

## Sections Unchanged (2)

- **Rationale** - Design rationale remains valid
- **Related Documentation** - Links still current

## Overall Assessment

**Structural maturity:** Significantly improved

- Added 2 major sections
- Enhanced 3 existing sections
- Pruned 1 obsolete section

**Content quality:** Substantial improvement

- 12% more content
- Better organization
- Production-ready documentation

**Documentation status:** Ready for release

- Promoted from draft to current
- Completeness up 25%
- Comprehensive coverage
```

## Format Selection Guide

### Quick Reference

| Use Case | Best Format | Why |
| :--------- | :------------ | :---- |
| Code review | Unified | Line-by-line details |
| Visual presentation | Side-by-side | Easy comparison |
| Progress report | Summary | High-level stats |
| Architecture review | Semantic | Structural changes |
| Detailed analysis | Unified + Semantic | Comprehensive |
| Quick check | Summary | Fast overview |

### Format Combinations

Sometimes combining formats is most effective:

#### Example: Complete review

1. Start with **Summary** for overview
2. Use **Semantic** for structural understanding
3. Review **Unified** for specific changes
4. Present with **Side-by-side** for stakeholders

## Custom Format Options

### Context Lines

Control amount of context in unified diff:

```bash
# Minimal context (1 line)
--unified=1

# Standard context (3 lines)
--unified=3

# Extended context (10 lines)
--unified=10
```

### Color Output

Enable color-coded diff output:

```bash
git diff --color-words ${ref} ${base} -- ${path}
```

### Ignore Whitespace

Ignore whitespace-only changes:

```bash
git diff --ignore-all-space ${ref} ${base} -- ${path}
```

### Word-Level Diff

Show word-by-word changes instead of line-by-line:

```bash
git diff --word-diff ${ref} ${base} -- ${path}
```

## Output Examples

### Unified with Minimal Context

```diff
@@ -45 +45,5 @@
-Basic event emitter
+Comprehensive event-based observability:
+- Event emission
+- Structured payloads
+- Type-safe handlers
```

### Output Example: Word-Level Diff

```text
Event [-emitter-]{+architecture:+}
{+
- Event emission
- Structured payloads+}
```

### Statistics Only

```text
observability.md | 37 ++++++++++++++++++++++++-------
1 file changed, 45 insertions(+), 8 deletions(-)
```
