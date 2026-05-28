# Sample Output

This shows the expected output format from the lessons-extractor skill.

## docs/ai/lessons-extractor/lessons.md

```markdown
# Lessons Learned

Last updated: 2026-01-22

## Summary

- Total lessons: 5
- By category: workflow (2), debugging (2), tool-specific (1)

## Workflow

### Always verify changes with tests

**ID:** lesson-001
**Confidence:** 0.95

After making any code changes, immediately run the relevant tests to verify the fix works and doesn't introduce regressions. Don't wait until multiple changes accumulate.

**Example:**
After editing `parser.ts` to fix empty string handling, run `npm test` before moving on.

**Caveats:**
- For very large test suites, run focused tests first (`npm test -- parser`)

---

### Read before editing

**ID:** lesson-002
**Confidence:** 0.9

Always read a file's contents before attempting to edit it. This ensures you understand the current state and can make accurate edits.

**Example:**
Use the Read tool on `src/utils/parser.ts` before using Edit to modify it.

---

## Debugging

### Check for edge cases in string handling

**ID:** lesson-003
**Confidence:** 0.85

When debugging string processing code, always test with: empty strings, strings with only whitespace, very long strings, and strings with special characters.

**Example:**
The parser failed on empty strings because it assumed input.length > 0.

---

### Verify error messages match actual behavior

**ID:** lesson-004
**Confidence:** 0.8

When a test fails, carefully read the error message and verify it matches the actual problematic behavior. Don't assume the error message is accurate.

---

## Tool-Specific

### Use focused test runs for faster feedback

**ID:** lesson-005
**Confidence:** 0.85

When working on a specific file, run only the related tests instead of the full suite. Most test frameworks support filtering by file or pattern.

**Example:**
`npm test -- --grep "parser"` or `npm test -- parser.test.ts`

**Related:** lesson-001
```

## docs/ai/lessons-extractor/lessons.jsonl

```jsonl
{"id":"lesson-001","category":"workflow","title":"Always verify changes with tests","description":"After making any code changes, immediately run the relevant tests to verify the fix works and doesn't introduce regressions.","confidence":0.95,"examples":["After editing parser.ts, run npm test before moving on"],"caveats":["For large test suites, run focused tests first"],"related":[]}
{"id":"lesson-002","category":"workflow","title":"Read before editing","description":"Always read a file's contents before attempting to edit it.","confidence":0.9,"examples":["Use Read tool on src/utils/parser.ts before Edit"],"caveats":[],"related":[]}
{"id":"lesson-003","category":"debugging","title":"Check for edge cases in string handling","description":"When debugging string processing code, test with empty strings, whitespace-only, long strings, and special characters.","confidence":0.85,"examples":["Parser failed on empty strings"],"caveats":[],"related":[]}
{"id":"lesson-004","category":"debugging","title":"Verify error messages match actual behavior","description":"When a test fails, verify the error message matches actual problematic behavior.","confidence":0.8,"examples":[],"caveats":[],"related":[]}
{"id":"lesson-005","category":"tool-specific","title":"Use focused test runs for faster feedback","description":"Run only related tests instead of full suite when working on specific files.","confidence":0.85,"examples":["npm test -- --grep parser"],"caveats":[],"related":["lesson-001"]}
```

## Notes

- The markdown format is human-readable and renders well on GitHub
- The JSONL format allows machine processing and search
- Confidence scores help prioritize which lessons to focus on
- Cross-references (`related`) connect complementary lessons
