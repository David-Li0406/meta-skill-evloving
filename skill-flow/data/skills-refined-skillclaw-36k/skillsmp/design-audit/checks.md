# Design Audit Checks

Comprehensive validation checks and scoring criteria for design documentation
audits.

## Frontmatter Validation

### Required Fields Check

**Required fields:**

- `status`: Valid enum (stub, draft, current, needs-review, archived)
- `module`: Module name
- `category`: Category name
- `created`: ISO date
- `updated`: ISO date
- `completeness`: Integer 0-100

**Validation:**

- Field exists
- Correct data type
- Valid value range
- Date format: YYYY-MM-DD

**Score:** Pass = 100, each missing field -20

### Date Logic Check

**Validation:**

- `updated >= created`
- `last-synced >= created` (if present)
- Dates not in future

**Score:** Pass = 100, each violation -50

### Cross-References Check

**Validation:**

- All `related` paths exist
- All `dependencies` paths exist
- No circular dependencies

**Score:** Pass = 100, each broken reference -10

## Structure Validation

### Required Sections

**Required H2 sections:**

- Overview
- Current State
- Rationale

**Optional but recommended:**

- Future Enhancements
- Trade-offs
- Alternatives Considered

**Score:** All required = 100, missing section -30

### Heading Hierarchy

**Rules:**

- Single H1 (title)
- H2 sections present
- No heading level skips (H2 → H4)
- Logical heading order

**Score:** Pass = 100, each violation -15

## Content Quality

### Completeness Accuracy

**Check:** Does actual content match completeness percentage?

**Algorithm:**

```javascript
expectedSections = getExpectedSections(status)
actualSections = getActualSections(doc)
actualCompleteness = (actualSections.length / expectedSections.length) * 100

accuracy = 100 - Math.abs(actualCompleteness - doc.completeness)
```

**Score:** Accuracy score (0-100)

### Section Depth

**Check:** Are sections sufficiently detailed?

**Metrics:**

- Section word count >100 words
- Code examples present where relevant
- Subsections used appropriately

**Score:** Average depth across sections

### Code Examples

**Check:** Presence of code blocks in technical sections.

**Expected in:**

- Implementation sections
- API documentation
- Algorithm descriptions

**Score:** Has examples = 100, missing = 0

### Rationale Documentation

**Check:** Rationale section explains decisions.

**Quality criteria:**

- Why decision was made
- What alternatives considered
- Trade-offs documented

**Score:** Comprehensive = 100, partial = 50, missing = 0

## Cross-Reference Integrity

### Broken Links

**Check:** All markdown links resolve.

**Detection:**

```bash
grep -o '\[.*\](\.\/.*\.md)' doc.md | check each path exists
```

**Score:** No broken links = 100, each broken -20

### Circular Dependencies

**Check:** No dependency cycles.

**Algorithm:**

Depth-first search to detect cycles in dependency graph.

**Score:** No cycles = 100, each cycle -30

### Bidirectional Balance

**Check:** Related docs reference each other.

**Quality criteria:**

- If A relates to B, B should relate to A
- Bidirectional references >50%

**Score:** Balance ratio * 100

## Sync Status

### Last Synced

**Check:** Document synchronized with codebase.

**Thresholds:**

- Never synced (for current docs): Critical
- >60 days: High
- >30 days: Medium
- <30 days: Pass

**Score:**

- <30 days: 100
- 30-60 days: 70
- 60-90 days: 40
- >90 days or never: 0

### Code References

**Check:** Referenced code/files still exist.

**Validation:**

Extract file paths from doc content, verify existence.

**Score:** All exist = 100, each broken -15

## Technical Debt

### TODO Count

**Check:** Unresolved TODOs in document.

**Severity by count:**

- 0 TODOs: Pass
- 1-2 TODOs: Low
- 3-5 TODOs: Medium
- 6+ TODOs: High

**Score:** 100 - (todoCount * 10), min 0

### Incomplete Sections

**Check:** Sections marked as incomplete or placeholder.

**Patterns:**

- "TODO"
- "TBD"
- "Coming soon"
- Empty sections

**Score:** 100 - (incompleteCount * 15), min 0

## Overall Health Scoring

### Document Health

**Formula:**

```javascript
docHealth = (
  frontmatterScore * 0.25 +
  structureScore * 0.20 +
  contentScore * 0.30 +
  referencesScore * 0.15 +
  syncScore * 0.10
) * 100
```

**Weights explained:**

- Frontmatter (25%): Foundation metadata
- Structure (20%): Document organization
- Content (30%): Most important - actual information
- References (15%): Cross-linking quality
- Sync (10%): Code alignment

### Module Health

**Formula:**

Average of all document health scores in module.

### Overall Health

**Formula:**

Weighted average across modules (larger modules weighted higher).

## Health Ratings

**Score ranges:**

- 90-100: Excellent (A)
- 80-89: Good (B)
- 70-79: Fair (C)
- 60-69: Poor (D)
- 0-59: Critical (F)

## Strict Mode

When `strict: true`:

- All checks enforced
- Lower tolerance thresholds
- More detailed validation
- Additional best practice checks

**Strict-only checks:**

- Consistent terminology
- Link anchor validation
- Image references exist
- Table formatting correct
- Code block languages specified
