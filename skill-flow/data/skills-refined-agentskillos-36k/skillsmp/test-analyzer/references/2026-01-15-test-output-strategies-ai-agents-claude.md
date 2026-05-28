---
date: 2026-01-15T15:38:00Z
researcher: Claude (Web Research)
git_commit: ffa5ebc520dc15eaf6dccaf3564145adf3dd1b44
branch: improve-testing
repository: altego-monorepo
topic: "Context-efficient test output strategies for AI coding agents"
tags: [research, web-research, testing, vitest, pytest, playwright, turborepo, ai-agents, ctrf]
status: complete
last_updated: 2026-01-15
last_updated_by: Claude
source: "Deep web research by Claude"
---

# Research: Context-Efficient Test Output Strategies for AI Coding Agents

**Date**: 2026-01-15T15:38:00Z
**Researcher**: Claude (Web Research)
**Git Commit**: ffa5ebc520dc15eaf6dccaf3564145adf3dd1b44
**Branch**: improve-testing
**Repository**: altego-monorepo
**Source**: Deep web research by Claude

## Research Question

How can we minimize test output for AI coding agents to reduce context consumption while preserving essential failure information for debugging? What are the best strategies across Vitest, Pytest, and Playwright in a Docker Compose monorepo environment?

## Summary

The most effective approach to minimizing test output for AI context windows combines **framework-specific minimal reporters**, **CTRF structured output**, and **bash wrapper scripts** that implement "success = checkmark, failure = verbose" patterns. Each of the three target frameworks—Vitest, Pytest, and Playwright—has native and third-party options that can reduce test output by **70-90%** while preserving the failure information needed for debugging.

The optimal strategy for the Altego monorepo context is a **three-layer approach**:
1. Framework-specific minimal reporters (vitest-tiny-reporter, pytest-instafail, Playwright quiet mode)
2. Turborepo orchestration with `--output-logs=errors-only`
3. CTRF structured output for AI consumption

## Detailed Findings

### Vitest: Near-Silent Success with Third-Party Reporters

The **`vitest-tiny-reporter`** package delivers the most minimal output available for Vitest, reducing context consumption by approximately 90% compared to the default reporter. On success, it outputs only a single summary line; on failure, it shows only the essential failure information.

```bash
npm install -D vitest-tiny-reporter
npx vitest --reporter=vitest-tiny-reporter --bail=1 --silent=passed-only
```

Native Vitest options provide incrementally quieter output but cannot achieve complete silence on success:

| Configuration | Output Level | Use Case |
|--------------|--------------|----------|
| `--reporter=dot` | Minimal (one dot per test) | CI pipelines |
| `--silent` | Suppresses console.log from tests | Clean output |
| `--silent=passed-only` | Shows logs only for failures | Debugging |
| `--reporter=json --outputFile=x` | Zero terminal output | Programmatic parsing |

The optimal `vitest.config.ts` for AI agents combines fail-fast behavior with structured output:

```typescript
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    bail: 1,
    silent: 'passed-only',
    reporters: [
      'dot',
      ['json', { outputFile: './test-results.json' }]
    ],
  },
})
```

### Pytest: Requires Plugins for True Silence

Native pytest cannot fully suppress output on success—an acknowledged limitation tracked in GitHub issue #13224. However, combining flags achieves near-minimal output:

```bash
pytest -q --tb=short -rf --no-header -x
```

The flag breakdown:
- **`-q`**: quiet mode with dots
- **`--tb=short`**: shortens tracebacks
- **`-rf`**: reports only failures in summary
- **`--no-header`**: removes version info
- **`-x`**: stops on first failure

**`pytest-instafail`** best implements the "success=silent, failure=verbose immediately" pattern by showing failures the moment they occur rather than batching them at the end:

```bash
pip install pytest-instafail
pytest --instafail -q --tb=short
```

For structured JSON output ideal for AI parsing, **`pytest-json-report`** offers configurable verbosity:

```bash
pip install pytest-json-report
pytest --json-report --json-report-file=results.json --json-report-omit keywords streams log -q --tb=no
```

The recommended `pyproject.toml` configuration for AI agents:

```toml
[tool.pytest.ini_options]
addopts = [
    "-q", "--tb=short", "-x", "-rf", "--no-header",
    "--json-report", "--json-report-file=.test-results.json",
    "--json-report-omit=keywords,streams"
]
```

### Playwright: Native Quiet Mode and Minimal Reporters

Playwright Test has the strongest native support for quiet output among the three frameworks. The **`quiet: true`** configuration option suppresses stdout/stderr from tests, while the **`dot`** reporter reduces terminal output to single characters per test.

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  quiet: true,
  reporter: 'dot',
  reportSlowTests: null,
  maxFailures: 1,
  preserveOutput: 'failures-only',
  use: {
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'off',
  },
})
```

For completely silent success with structured failure data, write results to a file:

```typescript
reporter: [['json', { outputFile: 'test-results.json' }]]
```

### CTRF: Universal Structured Format for AI Consumption

The **Common Test Report Format (CTRF)** provides a universal JSON schema across all test frameworks, with native AI integration through the `ai-ctrf` tool. Reporters exist for:
- Vitest: `@d2t/vitest-ctrf-json-reporter`
- Pytest: `pytest-json-ctrf`
- Playwright: `playwright-ctrf-json-reporter`

The minimal CTRF output structure contains only essential fields:

```json
{
  "results": {
    "summary": { "tests": 10, "passed": 9, "failed": 1 },
    "tests": [
      { "name": "test name", "status": "passed", "duration": 100 }
    ]
  }
}
```

The **`ai-ctrf`** package processes CTRF reports through **300+ AI models** including Claude, generating summaries and structured analysis:

```bash
npx ai-ctrf claude ctrf-report.json --maxMessages 5 --consolidate --json-analysis
```

The `--json-analysis` flag produces structured output ideal for AI agents:

```json
{
  "summary": "High-level overview of failures",
  "code_issues": "Code-related problems identified",
  "recommendations": "Actionable fixes"
}
```

### Bash Wrapper Scripts: Fundamental Pattern

The core "run_silent" pattern captures output and conditionally displays based on exit code:

```bash
#!/bin/bash
run_silent() {
  local output
  output=$("$@" 2>&1)
  local exit_code=$?

  if [ $exit_code -eq 0 ]; then
    echo "✓"
  else
    echo "✗ Command failed (exit: $exit_code)"
    echo "$output"
    return $exit_code
  fi
}

# Usage: run_silent npm test
```

For extracting test counts from silenced output:

```bash
run_tests_silent() {
  local output
  output=$(npm test 2>&1)
  local exit_code=$?

  if [ $exit_code -eq 0 ]; then
    local passed=$(echo "$output" | grep -oP '\d+(?= passed)')
    echo "✓ ${passed:-all} tests passed"
  else
    echo "$output" | grep -A 10 "FAIL\|Error:\|Expected"
    return $exit_code
  fi
}
```

### Turborepo: Monorepo Test Aggregation

For the Docker Compose-based monorepo context, **Turborepo's `--output-logs` flag** offers granular control over test output across packages:

```json
// turbo.json
{
  "tasks": {
    "test": {
      "outputs": ["coverage/**"],
      "outputLogs": "errors-only"
    }
  }
}
```

The available options:
- **`errors-only`**: shows only failures (ideal for AI)
- **`new-only`**: shows output for cache misses only
- **`hash-only`**: shows just task hashes
- **`none`**: suppresses all output

A Just task runner can orchestrate this efficiently:

```just
# justfile
test:
    turbo run test --output-logs=errors-only

test-verbose:
    turbo run test --output-logs=full
```

### Alternative E2E Tools Designed for AI Agents

**Shortest** by Antiwork (5.4k GitHub stars) represents the most AI-native E2E testing approach. Built on Playwright and integrated with Claude, it accepts natural language test definitions:

```typescript
import { shortest } from "@antiwork/shortest"

shortest("Login to the app using email and password", {
  username: process.env.USERNAME,
  password: process.env.PASSWORD,
})
```

Other emerging tools include:
- **Checksum**: auto-generates and maintains Playwright tests
- **Momentic**: intent-based testing with AI maintenance
- **Midscene.js**: E2E AI Agent with LLM integration

## Recommended Complete Configuration for Claude Code

For a Docker Compose monorepo targeting the **~75k token smart zone**, implement this three-layer strategy:

### Layer 1: Framework-Specific Minimal Reporters

```typescript
// vitest.config.ts
reporters: ['vitest-tiny-reporter', ['@d2t/vitest-ctrf-json-reporter', { minimal: true }]]
```

```toml
# pyproject.toml
addopts = ["-q", "--tb=short", "-x", "-rf", "--no-header", "--json-report"]
```

```typescript
// playwright.config.ts
quiet: true, reporter: [['dot'], ['playwright-ctrf-json-reporter', { minimal: true }]]
```

### Layer 2: Turborepo Orchestration

```json
{ "tasks": { "test": { "outputLogs": "errors-only" } } }
```

### Layer 3: Wrapper Script in CLAUDE.md

```markdown
## Test Commands
- `just test` - Runs all tests (silent on success)
- `just test-verbose` - Full output for debugging
- On failure, automatically re-run with `--output-logs=full`
```

The combination achieves the "context-efficient backpressure" goal: a single checkmark on success, focused failure information showing only what's needed to fix the issue.

## Architecture Documentation

### Current Testing Infrastructure in Altego Monorepo

The monorepo currently uses:
- **Vitest** for TypeScript/Next.js unit and integration tests (notion-paper-sync)
- **Pytest** for Python tests (rm-render-server)
- **Playwright** for E2E tests (tests directory)
- **Just task runner** for orchestrating test commands across containers
- **Docker Compose** for running tests in consistent environments

### Proposed Testing Output Strategy

```
Developer/AI -> just test
            -> turbo run test --output-logs=errors-only
            -> [Per-framework minimal reporters]
            -> ✓ (on success) | Focused failure info (on failure)
            -> CTRF JSON files for structured analysis
```

### Integration Points

1. **Justfile modifications**: Update test recipes to use new reporters
2. **Framework configs**: Add minimal reporters to each framework's config
3. **Docker**: Ensure reporter packages are installed in containers
4. **CI/CD**: Update pipelines to use new output modes
5. **CLAUDE.md**: Document new test command patterns for AI agents

## Open Questions

1. **Turborepo adoption**: Should we introduce Turborepo for test orchestration, or continue with Just + Docker Compose?
2. **CTRF integration**: Should we standardize on CTRF across all frameworks for consistent AI consumption?
3. **CI/CD compatibility**: How do these minimal reporters work with GitHub Actions and other CI systems?
4. **Debug mode**: What's the best UX for switching between minimal and verbose output during debugging?
5. **Test isolation**: How do these strategies affect test isolation and parallelization?

## Related Research

- Should cross-reference with existing testing infrastructure documentation
- Future research needed on Gemini and ChatGPT perspectives on test output strategies
- Related to ongoing work in `improve-testing` branch

## Conclusion

Achieving minimal test output for AI coding agents requires combining **framework-specific reporters** (vitest-tiny-reporter, pytest-instafail, Playwright's quiet mode), **CTRF as the standardized structured format** with its built-in AI integration, **bash wrappers** implementing the run_silent pattern, and **Turborepo's `--output-logs=errors-only`** for monorepo aggregation.

The ecosystem has matured significantly in 2025, with CTRF adoption growing and tools like `ai-ctrf` providing direct AI model integration. The gap remains in truly native "AI-friendly" test runners—Shortest represents the current frontier, but wrapper scripts remain essential for established frameworks.

For the Altego monorepo, the recommended approach is to implement framework-specific minimal reporters first, then evaluate Turborepo adoption for cross-package test orchestration.
