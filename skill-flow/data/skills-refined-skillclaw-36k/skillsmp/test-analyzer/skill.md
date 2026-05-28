---
name: test-analyzer
description: Analyze test failures from CTRF reports using jq for deterministic parsing
invocationPattern: when user asks to analyze test failures, investigate failing tests, or understand test patterns
---

# Test Analyzer Skill

## Purpose

Analyze CTRF test reports to identify failure patterns, suggest fixes, and provide insights into test health. Uses deterministic jq parsing for efficient, token-friendly analysis.

## When to Use

Call this skill when:
- Tests have failed and user wants analysis
- User asks "what tests failed?", "analyze test failures", or "why did tests fail?"
- User wants to understand test failure patterns or trends
- User asks about slow tests, flaky tests, or test coverage

## Quick Reference

**Using ctrf-utils.sh:**
```bash
ctrf-utils.sh summary <file>           # Show pass/fail summary
ctrf-utils.sh failures <file...>       # List failed test names
ctrf-utils.sh failures-detail <file>   # Show failures with error messages
ctrf-utils.sh flaky <file>             # Show tests with retry attempts
ctrf-utils.sh slowest <N> <file>       # Show N slowest tests
```

**Direct jq commands:**
```bash
jq '.results.summary' report.ctrf.json
jq -r '.results.tests[] | select(.status == "failed") | .name' report.ctrf.json
```

## CTRF Schema Overview

CTRF reports have this structure:

```json
{
  "results": {
    "tool": { "name": "vitest" },
    "summary": { "tests": 50, "passed": 48, "failed": 2, "skipped": 0 },
    "tests": [
      {
        "name": "should validate user input",
        "status": "failed",
        "duration": 156,
        "suite": "UserForm",
        "message": "Expected true, received false",
        "filePath": "src/components/UserForm.test.ts",
        "line": 23
      }
    ]
  }
}
```

**Required fields per test:** `name`, `status`, `duration`
**Full schema:** [ctrf-schema.json](./ctrf-schema.json)

## Essential jq Examples (~10 most common)

### 1. Summary statistics
```bash
jq '.results.summary' /workspace/artifacts/test/vitest.ctrf.json
```

### 2. One-line summary
```bash
jq -r '.results.summary | "Tests: \(.tests) | Passed: \(.passed) | Failed: \(.failed)"' /workspace/artifacts/test/vitest.ctrf.json
```

### 3. List failed test names
```bash
jq -r '.results.tests[] | select(.status == "failed") | .name' /workspace/artifacts/test/*.ctrf.json
```

### 4. Failed tests with error messages
```bash
jq -r '.results.tests[] | select(.status == "failed") | "❌ \(.name): \(.message // "No message")"' /workspace/artifacts/test/*.ctrf.json
```

### 5. Group failures by error pattern
```bash
jq '[.results.tests[] | select(.status == "failed")] | group_by(.message) | map({error: .[0].message, count: length, tests: map(.name)}) | sort_by(.count) | reverse' /workspace/artifacts/test/*.ctrf.json
```

### 6. Slowest 10 tests
```bash
jq '.results.tests | sort_by(.duration) | reverse | limit(10; .[]) | {name, duration}' /workspace/artifacts/test/vitest.ctrf.json
```

### 7. Flaky tests (with retries)
```bash
jq -r '.results.tests[] | select(.retries > 0 or .flaky == true) | "⚠️ \(.name) (retries: \(.retries // 0))"' /workspace/artifacts/test/*.ctrf.json
```

### 8. Extract file paths for failed tests
```bash
jq -r '[.results.tests[] | select(.status == "failed") | .filePath] | unique | .[]' /workspace/artifacts/test/vitest.ctrf.json
```

### 9. Cross-project failure summary
```bash
jq -s '{vitest: .[0].results.summary.failed, pytest: .[1].results.summary.failed, total: ((.[0].results.summary.failed // 0) + (.[1].results.summary.failed // 0))}' /workspace/artifacts/test/vitest.ctrf.json /workspace/artifacts/test/pytest.ctrf.json
```

### 10. AI-friendly compact summary
```bash
jq -c '{summary: .results.summary, failures: [.results.tests[] | select(.status == "failed") | {name, suite, message, file: "\(.filePath):\(.line)"}]}' /workspace/artifacts/test/*.ctrf.json
```

## More jq Examples

For comprehensive examples (24+), see: [jq-examples-comprehensive.md](./jq-examples-comprehensive.md)

## Scripts Reference

Implementation scripts:
- [ctrf-utils.sh](./ctrf-utils.sh) - CTRF utilities for deterministic parsing (used by skill)
- [references/run-silent.sh](./references/run-silent.sh) - Silent-on-success wrapper pattern (reference)

## Research Background

Context and research behind this approach:
- [references/2026-01-15-context-efficient-backpressure-blogpost.md](./references/2026-01-15-context-efficient-backpressure-blogpost.md)
- [references/2026-01-15-test-output-strategies-ai-agents-claude.md](./references/2026-01-15-test-output-strategies-ai-agents-claude.md)
- [references/2026-01-15-test-output-strategies-ai-agents-gemini.md](./references/2026-01-15-test-output-strategies-ai-agents-gemini.md)
- [references/2026-01-15-research-test-output-summarization-chatgpt.md](./references/2026-01-15-research-test-output-summarization-chatgpt.md)

## Skill Behavior

When invoked:

1. **Locate CTRF reports** (common locations: `artifacts/test/`, `test-results/`, project root)

2. **Get summary:**
   ```bash
   jq -r '.results.summary | "Tests: \(.tests) | Passed: \(.passed) | Failed: \(.failed)"' *.ctrf.json
   ```

3. **If failures exist, list them:**
   ```bash
   jq -r '.results.tests[] | select(.status == "failed") | "❌ \(.name): \(.message // "No message")"' *.ctrf.json
   ```

4. **Analyze patterns** (group similar errors):
   ```bash
   jq '[.results.tests[] | select(.status == "failed")] | group_by(.message) | map({error: .[0].message, count: length})' *.ctrf.json
   ```

5. **Read source files for failed tests** (extract file paths with jq, then read)

6. **Suggest fixes based on patterns** (group similar errors, identify root causes)
