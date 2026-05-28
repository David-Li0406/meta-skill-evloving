# Smart Completeness Estimation

Logic for automatically estimating document completeness based on content
analysis.

## Overview

Smart completeness estimation analyzes document content to suggest accurate
completeness percentages, helping maintain consistency between declared and
actual completion.

## Estimation Algorithm

### 1. Section Analysis

Analyze each major section:

**Required Sections:**

- Overview
- Current State
- Rationale

**Optional Sections:**

- Implementation Details
- Future Enhancements
- Examples
- Best Practices

**Scoring:**

For each section:

- Empty/placeholder only: 0 points
- Brief content (<100 words): 5 points
- Moderate content (100-500 words): 10 points
- Comprehensive content (>500 words): 15 points

### 2. Placeholder Analysis

Count placeholder markers:

**Placeholder Patterns:**

- `{Placeholder}` - Template marker
- `{TODO}` - Todo marker
- `{...}` - Ellipsis marker
- `TBD` - To be determined

**Calculation:**

```text
Total sections: X
Sections with placeholders: Y
Placeholder ratio: Y / X

Penalty = placeholder_ratio * 20
```

### 3. Content Depth Analysis

Assess content depth:

**Code Examples:**

- No code examples: 0 points
- Generic examples: 5 points
- Specific, relevant examples: 10 points

**Technical Detail:**

- Generic descriptions: 0 points
- Some specifics (file names, APIs): 5 points
- Detailed technical info (code locations, patterns): 10 points

**Completeness Indicators:**

- Links to code/files: +5
- Metrics/measurements: +5
- Diagrams/tables: +5
- Real examples (not template): +5

### 4. Structural Completeness

Check document structure:

**TOC:**

- Missing: -5 points
- Present but incomplete: 0 points
- Complete and accurate: +5 points

**Frontmatter:**

- All fields populated: +5 points
- Some fields empty: 0 points
- Missing fields: -5 points

**Footer:**

- Related Documentation section: +5 points
- Proper cross-references: +5 points

## Completeness Formula

```text
Base Score = (Section Points / Max Section Points) * 60

Content Depth Bonus = min(20, Content Depth Points)

Structure Bonus = min(10, Structure Points)

Placeholder Penalty = min(30, Placeholder Count * 3)

Estimated Completeness = Base Score + Content Depth Bonus
                       + Structure Bonus - Placeholder Penalty

Final = max(0, min(100, Estimated_Completeness))
```

## Estimation Categories

### Stub (0-20%)

**Characteristics:**

- Mostly placeholders
- Only section headings present
- No real implementation details
- Template content not customized

**Example:**

```markdown
## Overview

{Placeholder: Provide overview of this system}

## Current State

{TODO: Document current implementation}

## Rationale

{Placeholder: Explain design decisions}
```

**Estimated:** 5-10%

### Early Draft (21-40%)

**Characteristics:**

- Some sections filled in
- Brief descriptions, lacking detail
- Mix of placeholders and real content
- Few specific examples

**Example:**

```markdown
## Overview

This system handles type loading for the API extractor.

## Current State

{TODO: Document implementation}

## Rationale

We chose this approach because it's simpler.
```

**Estimated:** 25-35%

### Mid Draft (41-60%)

**Characteristics:**

- Most sections have content
- Moderate detail level
- Some placeholders remain
- Few code examples

**Example:**

```markdown
## Overview

This system handles type loading for the API extractor by fetching
type definitions from npm packages and creating a virtual file system.

## Current State

Implemented in `src/type-loader.ts` with caching support.

## Rationale

{TODO: Explain alternatives considered}
```

**Estimated:** 45-55%

### Late Draft (61-80%)

**Characteristics:**

- All major sections complete
- Good detail level
- Minimal placeholders
- Code examples present

**Example:**

```markdown
## Overview

[Comprehensive overview with problem statement and solution]

## Current State

[Detailed implementation with file locations, APIs, metrics]

## Rationale

[Multiple alternatives considered, trade-offs documented]

## Implementation Details

[Code examples and patterns]
{TODO: Add error handling section}
```

**Estimated:** 65-75%

### Nearly Complete (81-95%)

**Characteristics:**

- All sections comprehensive
- High detail level
- No major placeholders
- Multiple code examples
- Cross-references complete

**Example:**

```markdown
[All sections fully documented with code examples, metrics,
patterns, best practices. Minor TODOs for optional enhancements.]
```

**Estimated:** 85-95%

### Complete (96-100%)

**Characteristics:**

- No placeholders
- Comprehensive coverage
- Code examples throughout
- Cross-references bidirectional
- Future enhancements documented

**Estimated:** 95-100%

## Smart Suggestions

### When to Suggest Completeness Updates

Suggest updating completeness when:

1. **Declared vs Estimated Differs by >20%**
   - Current: 45%
   - Estimated: 70%
   - Suggestion: "Content suggests 70% complete, update from 45%?"

2. **Status Doesn't Match Estimated**
   - Status: stub
   - Estimated: 55%
   - Suggestion: "Content is draft-level (55%), update status?"

3. **Recent Content Changes**
   - Section added/updated
   - Completeness unchanged
   - Suggestion: "Added Implementation section, increase completeness?"

### Suggesting Status Updates

Based on estimated completeness:

```text
if estimated_completeness <= 20:
    suggested_status = "stub"
elif estimated_completeness <= 60:
    suggested_status = "draft"
elif estimated_completeness <= 90:
    suggested_status = "current" or "needs-review"
else:
    suggested_status = "current"
```

## Interactive Estimation

### Prompt User for Estimation

When user updates content significantly:

```text
I've analyzed the document content. Based on:
- X filled sections out of Y total
- Z placeholders remaining
- Code examples and technical detail

Estimated completeness: {X}%
Current declared: {Y}%

Would you like to update completeness to {X}%?
Options:
1. Yes, use estimated {X}%
2. No, keep current {Y}%
3. Enter custom value
```

### Estimation Report

Provide detailed estimation reasoning:

```markdown
## Completeness Estimation

**Current Declared:** 45%
**Estimated:** 70%
**Difference:** +25%

### Analysis

**Section Completeness:**
- ✅ Overview: Complete (15/15 points)
- ✅ Current State: Complete (15/15 points)
- ✅ Rationale: Complete (15/15 points)
- ⚠️ Implementation: Partial (7/15 points)
- ❌ Future Enhancements: Empty (0/15 points)

**Content Quality:**
- Code examples: 2 found (+10 points)
- Technical detail: Good (+8 points)
- Placeholders: 3 found (-9 points)

**Recommendation:**
Update completeness to 70% and status to 'current' to accurately reflect
the well-documented core sections. Consider completing Implementation
section to reach 85%.
```

## Validation Against Estimation

When user sets completeness manually, validate:

**If declared > estimated + 20:**

```text
Warning: Declared completeness (85%) seems high based on content
analysis (estimated 60%).

Issues found:
- 5 sections with placeholders
- Missing code examples
- Implementation section incomplete

Recommendation: Review estimation or complete remaining sections.
```

**If declared < estimated - 20:**

```text
Note: Content analysis suggests higher completeness (75%) than
declared (50%).

Completed sections found:
- Comprehensive Overview
- Detailed Current State
- Well-documented Rationale
- Multiple code examples

Recommendation: Consider updating to 75%.
```

## Continuous Estimation

Re-estimate completeness automatically when:

1. Content sections updated
2. Placeholders filled in
3. New sections added
4. Code examples added
5. Cross-references updated

Store estimation alongside declared completeness for comparison.
