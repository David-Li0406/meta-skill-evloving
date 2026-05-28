# Analysis Checks

Comprehensive health check criteria for analyzing design documentation.

## 1. Frontmatter Health

### Status Progression

Check if documents are progressing appropriately:

**Stub Documents (0-20% complete):**

- ⚠️ No updates in >30 days
- 🔴 No updates in >90 days (abandoned)
- Check: Compare `updated` date to current date

**Draft Documents (21-60% complete):**

- ⚠️ No updates in >60 days
- 🔴 No updates in >180 days (stalled)
- Check: Track completeness changes over time

**Needs Review (any completeness):**

- ⚠️ In needs-review for >7 days
- 🔴 In needs-review for >14 days (review overdue)
- Check: Status hasn't changed despite age

### Completeness Accuracy

Validate completeness matches actual state:

**Status-Completeness Mismatch:**

- Stub status with completeness >20%
- Draft status with completeness <21% or >60%
- Current status with completeness <61%
- Needs-review with completeness <80%

**Placeholder Analysis:**

- Count `{Placeholder}` markers in content
- Estimate expected completeness from filled sections
- Compare to declared completeness
- Flag if difference >20%

**Completeness Staleness:**

- Completeness unchanged for >30 days
- File has git commits but completeness not updated
- Recent changes suggest higher completeness than declared

### Staleness Indicators

Identify stale or neglected documentation:

**Never Synced:**

- `last-synced: never` for current/complete docs
- Impact: May be outdated with codebase
- Recommendation: Run `/design-sync` to verify accuracy

**Old Updates:**

- `updated` date >90 days ago for active modules
- No git commits in >180 days
- Technology/patterns may have evolved

**Created = Updated:**

- Same date for `created` and `updated`
- Status beyond stub
- Suggests no real updates since creation

### Cross-Reference Issues

Problems with related and dependencies arrays:

**Empty Arrays:**

- Empty `related` array when clear relationships exist
- Empty `dependencies` array for implementation docs
- Missing obvious connections (e.g., architecture ↔ observability)

**Broken References:**

- Paths in `related` that don't exist
- Paths in `dependencies` that don't exist
- Check: Use Read or Glob to verify file existence

**One-Way References:**

- Doc A references Doc B, but B doesn't reference A
- Should be bidirectional for "related" relationships
- Check cross-reference symmetry

## 2. Content Quality

### Overview Section

Assess overview quality and usefulness:

**Length Issues:**

- Too brief (<100 words): May lack context
- Too verbose (>1000 words): Should be summarized
- Optimal: 200-500 words

**Content Issues:**

- No clear problem statement
- Missing "when to reference this document" guidance
- Generic template text not customized
- Filled with placeholders instead of real content

**Quality Indicators:**

- ✅ Clear problem/purpose statement
- ✅ Explains when to consult this doc
- ✅ Provides context without overwhelming detail
- ✅ Links to related concepts

### Current State

Evaluate implementation documentation:

**Missing Details:**

- No concrete implementation information
- Missing code locations or file paths
- No metrics or measurements
- No version/release information

**Placeholder Content:**

- Sections still filled with `{Placeholder}` markers
- Template boilerplate not customized
- No actual state documented

**Quality Indicators:**

- ✅ Specific code locations (files, functions, classes)
- ✅ Current metrics or measurements
- ✅ Version information
- ✅ Integration points documented
- ✅ Dependencies listed

### Rationale

Check decision documentation quality:

**Missing Documentation:**

- No rationale section at all
- Section exists but empty or placeholder
- Decisions stated without reasoning

**Insufficient Analysis:**

- No alternatives considered
- Missing trade-offs analysis
- No explanation of why chosen approach
- Decisions without context

**Quality Indicators:**

- ✅ Multiple alternatives considered
- ✅ Trade-offs explicitly documented
- ✅ Decision criteria explained
- ✅ Constraints and limitations noted
- ✅ Why other options rejected

### Implementation Details

Assess technical depth and usefulness:

**Generic Content:**

- Template content not customized
- No specific code examples
- Missing patterns or best practices
- Insufficient detail for implementation

**Missing Integration:**

- No integration points documented
- Missing API contracts
- No error handling patterns
- Configuration not documented

**Quality Indicators:**

- ✅ Concrete code examples
- ✅ Patterns and anti-patterns documented
- ✅ Integration points clear
- ✅ Configuration examples
- ✅ Error handling documented

### Future Enhancements

Check planning and roadmap quality:

**Empty Planning:**

- All phases empty or generic
- No timeline or priority indicated
- Missing effort estimates
- Not connected to current limitations

**Quality Indicators:**

- ✅ Phased approach defined
- ✅ Priorities indicated
- ✅ Connected to current limitations
- ✅ Effort estimates provided
- ✅ Dependencies noted

## 3. Structure Quality

### Section Structure

Validate document organization:

**Missing Sections:**

- Required sections not present
- Check against config `minSections`
- Compare to category-specific requirements

**Section Order:**

- Sections not in logical order
- Frontmatter not first
- Overview not after title

**Empty Sections:**

- Headings with no content
- Just placeholders, no real information
- Remove or populate

**Duplicate Sections:**

- Same section heading appears multiple times
- May indicate merge conflict or copy-paste error

### Table of Contents

Validate TOC completeness and accuracy:

**Missing TOC:**

- Required by config but not present
- Document >500 lines without TOC

**TOC Issues:**

- Links don't match section headings
- Incomplete (missing sections)
- Outdated (references non-existent sections)
- Wrong heading levels

**Validation:**

- Extract TOC links
- Extract actual section headings
- Compare and report mismatches

### Formatting Quality

Check markdown formatting:

**Heading Issues:**

- Inconsistent heading levels (skip from H1 to H3)
- Multiple H1 headings
- Headings not incrementing properly

**Code Block Issues:**

- Unclosed code fences
- Missing language specifiers
- Inconsistent fence style (``` vs ~~~)

**Line Length:**

- Lines >120 characters in prose
- Should wrap for readability
- Code blocks exempt

**List Issues:**

- Malformed lists (inconsistent bullets)
- Wrong indentation
- Missing blank lines around lists

## 4. Cross-Reference Health

### Related Documentation

Validate relationship quality:

**One-Way References:**

- Doc A → Doc B but B doesn't → A
- Should be bidirectional for "related"
- Identify and recommend reciprocal links

**Missing Relationships:**

- Obvious relationships not documented
- Example: architecture.md ↔ observability.md
- Use category overlap to suggest connections

**Circular Dependencies:**

- A depends on B, B depends on A
- May indicate architectural issue
- Flag for review if unjustified

### Internal Links

Check link validity:

**Broken Links:**

- Links to other design docs that don't exist
- Links to moved or renamed files
- Use Read/Glob to verify existence

**External vs Relative:**

- External links to internal docs
- Should use relative paths
- Makes repo portable

**Link Format:**

- Inconsistent link styles
- Should use markdown links
- Anchor links to sections should work

### CLAUDE.md Integration

Validate context file integration:

**Missing Reference:**

- Design doc not referenced in module's CLAUDE.md
- Important docs should be pointed to
- Check CLAUDE.md for `@` pointers

**Wrong Path:**

- CLAUDE.md reference uses wrong path
- Path doesn't match actual file location
- May have been moved

**No Load Guidance:**

- Reference exists but no "when to load" guidance
- Should specify when Claude should read the doc
- Example: "Load when working on {feature}"

## 5. Maintenance Health

### Abandonment Detection

Identify neglected documentation:

**Stub Abandonment:**

- Stub status for >90 days
- No updates in that time
- Likely won't be completed

**Draft Stalling:**

- Draft status for >180 days
- No progress on completeness
- May need help or should be archived

**Git Activity:**

- No git commits touching file in >365 days
- Even if status is "current"
- May be obsolete or forgotten

### Scope Issues

Detect documentation scope problems:

**Scope Creep:**

- Document covers too many topics
- Multiple unrelated concerns
- Should be split into separate docs

**Indicators:**

- Document >1000 lines
- Many top-level sections (>10)
- Multiple categories would fit
- Table of contents is very long

**Recommendation:**

- Split into focused documents
- One doc per major concern
- Use cross-references to connect

### Duplication

Find duplicated content:

**Content Duplication:**

- Same information in multiple design docs
- Should reference instead of duplicate
- Creates maintenance burden

**Detection:**

- Look for similar section headings across docs
- Compare content between related docs
- Flag exact matches or near-duplicates

**Resolution:**

- Keep canonical version in one doc
- Reference from others
- Update cross-references

## Analysis Priorities

When analyzing docs, prioritize checking:

1. **Critical Issues** (block usage):
   - Missing frontmatter
   - Broken references
   - Abandoned stubs

2. **High Priority** (affects quality):
   - Status/completeness mismatches
   - Missing required sections
   - Stale content (>180 days)

3. **Medium Priority** (improvement):
   - Empty cross-reference arrays
   - Brief or generic content
   - Missing CLAUDE.md integration

4. **Low Priority** (nice to have):
   - TOC formatting
   - Line length issues
   - Minor formatting inconsistencies
