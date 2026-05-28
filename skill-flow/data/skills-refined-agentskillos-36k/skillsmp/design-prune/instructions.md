# Design Prune Detailed Instructions

Complete step-by-step workflow for removing historical cruft from design
documentation.

## Detailed Workflow

### 1. Parse Parameters

Extract module and pruning options from user request.

**Parameter parsing examples:**

- `/design-prune effect-type-registry` → module: `effect-type-registry`
- `/design-prune module --aggressive` → aggressive pruning mode
- `/design-prune module observability.md --dry-run` → test run only

### 2. Load Configuration

Read `.claude/design/design.config.json` to get:

- Module configuration
- Design docs path
- Pruning rules (if configured)

**Configuration structure:**

```json
{
  "modules": {
    "module-name": {
      "path": ".claude/design/module-name"
    }
  },
  "pruning": {
    "aggressive": false,
    "keepHistoricalSections": true
  }
}
```

### 3. Read Design Document

Load document and parse structure:

- Extract sections
- Identify content types
- Detect patterns indicating historical content
- Map cross-references

### 4. Detect Historical Content

See [content-patterns.md](content-patterns.md) for detection patterns.

**Common historical patterns:**

- "Originally we tried..."
- "In version 1.0..."
- "Historical note:"
- "UPDATE (date): ..."
- Crossed-out text
- Commented-out sections

**Detection algorithm:**

```javascript
function isHistoricalContent(section) {
  const historicalKeywords = [
    /originally/i,
    /initially/i,
    /at first/i,
    /version \d+\.\d+/,
    /UPDATE \(/,
    /historical note/i,
    /deprecated since/i
  ]

  for (pattern of historicalKeywords) {
    if (section.text.match(pattern)) {
      return true
    }
  }

  // Check for strikethrough
  if (section.text.includes('~~')) {
    return true
  }

  // Check for commented sections
  if (section.text.match(/^\s*<!--.*-->$/m)) {
    return true
  }

  return false
}
```

### 5. Calculate Staleness Score

Assess how outdated content is.

**Scoring factors:**

```javascript
function calculateStalenessScore(content) {
  let score = 0

  // Age-based scoring
  const ageInDays = daysSince(content.lastModified)
  if (ageInDays > 365) score += 30
  else if (ageInDays > 180) score += 20
  else if (ageInDays > 90) score += 10

  // Historical marker scoring
  if (content.hasHistoricalMarkers) score += 25

  // Redundancy scoring
  if (content.isDuplicateOfCurrent) score += 35

  // Cross-reference scoring
  if (content.crossReferences === 0) score += 10

  // Total score 0-100
  return Math.min(score, 100)
}
```

**Staleness categories:**

- 0-25: Fresh (keep)
- 26-50: Aging (review)
- 51-75: Stale (consider pruning)
- 76-100: Very stale (prune)

### 6. Generate Pruning Plan

See [pruning-strategies.md](pruning-strategies.md) for strategy details.

**Plan structure:**

```markdown
# Pruning Plan - {module}/{doc}

## Summary

- Total sections: {count}
- Historical sections detected: {count}
- Sections to prune: {count}
- Estimated reduction: {percentage}%

## Pruning Actions

### Remove Historical Implementation Notes

**Section:** "Original Architecture (v1.0)"
**Reason:** Superseded by current architecture section
**Staleness:** 85/100
**Action:** Remove entirely

### Condense Update History

**Section:** Multiple UPDATE markers
**Reason:** Update history too verbose
**Staleness:** 65/100
**Action:** Condense to single "History" section

### Archive Deprecated Patterns

**Section:** "Old Caching Strategy"
**Reason:** No longer used, documented elsewhere
**Staleness:** 90/100
**Action:** Move to archive or remove
```

### 7. Apply Pruning

Execute pruning plan with appropriate safety checks.

**Pruning modes:**

**Conservative (default):**

- Only remove clearly outdated content
- Preserve historical context markers
- Keep one summary of changes

**Aggressive:**

- Remove all historical content
- Remove update markers
- Focus only on current state

**Dry-run:**

- Show what would be pruned
- Don't modify files
- Generate preview

**Pruning execution:**

```javascript
function applypruning(plan, mode, dryRun) {
  const results = {
    removed: [],
    condensed: [],
    archived: [],
    errors: []
  }

  for (action of plan.actions) {
    if (dryRun) {
      reportWouldPrune(action)
      continue
    }

    try {
      switch (action.type) {
        case 'remove':
          removeSection(action.section)
          results.removed.push(action.section)
          break

        case 'condense':
          condenseContent(action.section, action.target)
          results.condensed.push(action.section)
          break

        case 'archive':
          archiveSection(action.section)
          results.archived.push(action.section)
          break
      }
    } catch (error) {
      results.errors.push({ action, error })
    }
  }

  return results
}
```

### 8. Update Frontmatter

Update document metadata after pruning:

```yaml
---
last-pruned: 2026-01-17
prune-reduction: 15%  # Percentage of content removed
pruning-mode: conservative
---
```

### 9. Validate Result

Ensure pruned document is still valid:

- Run frontmatter validation
- Check markdown structure
- Verify cross-references still valid
- Confirm no broken links

### 10. Generate Pruning Report

Create summary of actions taken:

```markdown
# Pruning Report - {module}

**Date:** 2026-01-17
**Mode:** conservative
**Documents processed:** {count}

## Summary

- Total content before: {before-lines} lines
- Total content after: {after-lines} lines
- Reduction: {percentage}% ({lines} lines removed)

## Actions by Document

### {doc-name}

✅ Removed 3 historical sections (85 lines)
✅ Condensed 2 update histories (23 lines)
⚠️  Preserved 1 historical section (cross-referenced)

## Validation

✅ All pruned documents pass validation
✅ No broken cross-references
✅ Markdown structure intact

## Next Steps

1. Review preserved historical sections
2. Consider archiving if no longer needed
3. Re-run /design-validate to confirm
```

## Pruning Strategies

### Remove Entirely

**When to use:**

- Content completely superseded
- No cross-references
- Staleness score >75

**Example:**

Remove "Original Implementation (v1.0)" when current implementation is
fully documented.

### Condense to Summary

**When to use:**

- Historical context valuable
- Too much detail
- Staleness score 50-75

**Example:**

Condense 200 lines of update history to 20-line "Evolution" section.

### Archive

**When to use:**

- Might need reference later
- Educational value
- Staleness score >60

**Example:**

Move "Deprecated Caching Strategy" to `_archive/old-caching.md` with link.

### Preserve with Marker

**When to use:**

- Cross-referenced elsewhere
- Provides important context
- Staleness score <50

**Example:**

Keep section but add marker: "**Historical Note:** This approach was used
in v1.0..."

## Edge Cases

### Cross-Referenced Historical Content

**Scenario:** Historical section is referenced by other docs.

**Solution:**

1. Check all references
2. If references are also historical, prune both
3. If references are current, preserve or update references

### Partially Historical

**Scenario:** Section contains mix of current and historical content.

**Solution:**

1. Split section into current and historical parts
2. Keep current content
3. Prune or summarize historical parts

### Conflicting Dates

**Scenario:** UPDATE markers with inconsistent dates.

**Solution:**

1. Verify dates against git history
2. Correct or consolidate markers
3. Ensure chronological order

### Too Much Pruned

**Scenario:** Pruning removes >50% of content.

**Solution:**

1. Review aggressiveness setting
2. Check if document is mostly historical
3. Consider if document should be archived entirely
