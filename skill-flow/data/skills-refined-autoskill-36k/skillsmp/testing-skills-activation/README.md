# Testing Skills Activation

Quick reference for using the skill activation testing workflow.

## Quick Start

```bash
# 1. Navigate to skill directory
cd /path/to/skill-being-tested

# 2. Create test cases
cat > test-cases.json << 'EOF'
[
  {
    "id": 1,
    "user_message": "your test message",
    "project_context": "project tech stack",
    "expected_activation": true,
    "rationale": "why this should activate"
  }
]
EOF

# 3. Run tests
/path/to/testing-skills-activation/run-tests.sh

# 4. View results
cat /tmp/claude/test-report-*.md | tail -100

# 5. Iterate on SKILL.md description

# 6. Re-run and compare
/path/to/testing-skills-activation/run-tests.sh
```

## Example: using-live-documentation

### Test Cases Created

22 test cases covering:
- react-query, FastAPI, pydantic, Django, Express, pandas, Next.js, NestJS, Celery, pytest, Pinia
- Implementation, debugging, and API questions
- Negative cases: built-ins, standard library, pure algorithms

### Results

**Baseline (Before iteration):**
```
Description: "Use when implementing features, debugging, or answering
questions about code, specially if it involves libraries/frameworks..."

Accuracy: 50% (11/22)
Issues: Too broad, buried the lead, competing with explore-first pattern
```

**Iteration 1 (After refinement):**
```
Description: "Use when working with third-party libraries or frameworks
(react-query, FastAPI, pydantic, Django, Express, pandas, Next.js, NestJS,
Celery, pytest, Pinia, etc.) for implementing features, debugging
library-specific behavior, or answering API questions - fetches current
documentation ensuring accurate implementation. Do NOT use for language
built-ins (Python dict/list, JavaScript Array), standard library
(fs, json, os.path), or pure algorithms."

Accuracy: 73% (16/22)
Improvement: +23 percentage points
```

**Key changes:**
- Led with "third-party libraries or frameworks"
- Added specific library names
- Explicit negative examples
- Removed implementation details

## Files

- **SKILL.md** - Full documentation of the testing process
- **run-tests.sh** - Test runner script
- **README.md** - This quick reference

## Process Summary

1. **Research** - Understand best practices for skill descriptions
2. **Generate** - Create 15-25 diverse test cases (60/40 positive/negative)
3. **Baseline** - Run tests, document current accuracy
4. **Analyze** - Identify patterns in false positives/negatives
5. **Iterate** - Refine description based on failures
6. **Re-test** - Measure improvement, repeat until 90%+

## Test Case Format

```json
{
  "id": 1,
  "user_message": "What the user actually says",
  "project_context": "Tech stack and project type",
  "expected_activation": true,
  "rationale": "Why this should or shouldn't activate"
}
```

## Output Locations

- **Results JSON:** `/tmp/claude/test-results-TIMESTAMP.json`
- **Report MD:** `/tmp/claude/test-report-TIMESTAMP.md`
- **Test cases:** `test-cases.json` (in skill directory)

## Metrics

- **Accuracy:** % of correct predictions (target: 90%+)
- **True Positives (TP):** Correctly activated
- **True Negatives (TN):** Correctly didn't activate
- **False Positives (FP):** Activated when shouldn't (too broad)
- **False Negatives (FN):** Didn't activate when should (missing triggers)

## Best Practices Reference

See `best-practices-reference.md` in this directory for comprehensive guidelines.

Key principles:
- Lead with strongest triggers
- Include specific technology names
- State what IS and is NOT in scope
- Use user language
- Target 90%+ accuracy
