# Comparison Checklist

Use this checklist in Phase 3 to validate the optimized document against the original.

## Validation Categories

### 1. Content Completeness

| Check                     | How to Verify                                     |
| ------------------------- | ------------------------------------------------- |
| All headings preserved    | Compare heading text (may be reorganized/renamed) |
| All code examples present | Match code blocks, verify none deleted            |
| All commands included     | List commands from both, verify parity            |
| All facts retained        | Check dates, versions, names, numbers             |
| All links preserved       | Extract and compare link URLs                     |
| Cross-references intact   | Verify file path references still valid           |

### 2. Information Accuracy

| Check                          | How to Verify                              |
| ------------------------------ | ------------------------------------------ |
| No meaning changed             | Read key instructions, confirm same intent |
| Technical details correct      | Verify code syntax, command flags          |
| Order preserved where critical | Step-by-step sequences maintain order      |
| Conditionals intact            | If/then logic, edge cases preserved        |

### 3. Structural Improvements

These are expected changes (not errors):

| Change                      | Acceptable When                |
| --------------------------- | ------------------------------ |
| Heading reorganization      | Hierarchy fixed (H1→H2→H3)     |
| Prose → tables              | Related items tabulated        |
| Paragraphs → bullets        | Dense text made scannable      |
| Section splits              | Mixed topics separated         |
| Content moved to references | Progressive disclosure applied |

---

## Comparison Process

### Step 1: Extract Original Elements

From the original document, extract:

- [ ] All heading text (with level)
- [ ] All code block contents
- [ ] All commands/CLI invocations
- [ ] All links (URL and anchor text)
- [ ] All specific facts (dates, versions, counts)
- [ ] All named entities (files, functions, variables)

### Step 2: Verify in Optimized

For each extracted element:

- [ ] Locate in optimized document
- [ ] Confirm present (may be reformatted)
- [ ] Note if intentionally removed (with reason)

### Step 3: Identify Gaps

Create a gap list:

```markdown
## Missing from Optimized

| Item               | Type    | Original Location | Action                |
| ------------------ | ------- | ----------------- | --------------------- |
| `npm run lint`     | command | Line 45           | Add to Commands table |
| Deployment section | heading | Line 120          | Add section           |
```

### Step 4: Second Pass

For each gap:

1. Determine if omission was intentional (redundant, outdated)
2. If needed, add to optimized document
3. Mark gap as resolved

---

## Red Flags

Stop and investigate if:

| Red Flag                          | Possible Cause          |
| --------------------------------- | ----------------------- |
| Major section entirely missing    | Transformation error    |
| Code example with different logic | Accidental modification |
| URL pointing to wrong destination | Link corruption         |
| Version number changed            | Copy error              |
| Step missing from sequence        | Order disruption        |

---

## Gap Resolution Strategies

### Missing Command

Add to commands table:

```markdown
| `command` | Description from original |
```

### Missing Code Example

Locate in original, copy with improvements:

- Add language to code fence
- Add inline comments if helpful
- Ensure complete and runnable

### Missing Section

Options:

1. Add section with optimized formatting
2. If content is detailed, create reference file
3. If redundant with existing content, note in comparison report

### Missing Link

Restore link with:

- Original URL
- Descriptive anchor text (not "click here")

---

## Comparison Report Format

Generate report for Phase 5:

```markdown
## Optimization Summary

**Original**: [filename] ([X] lines)
**Optimized**: [filename].optimized.md ([Y] lines)
**Reduction**: [Z]%

### Key Changes

1. Converted [N] paragraphs to bullet lists
2. Created [N] tables from prose
3. Fixed heading hierarchy ([details])
4. Applied XML tags to [N] sections
5. [Other significant changes]

### Content Verified

- [x] headings preserved
- [x] code examples intact
- [x] commands included
- [x] links working
- [x] facts accurate

### Gaps Filled (Second Pass)

- Added: [item 1]
- Added: [item 2]

### Recommendation

[Replace original / Keep both / Manual review needed]
```
