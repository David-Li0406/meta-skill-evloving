---
date: 2026-01-15T21:35:13+01:00
researcher: GPT-5.2 Thinking
git_commit: null
branch: null
repository: null
topic: "Summarising test runner output for AI agents (Vitest, Pytest, Playwright)"
tags: [research, testing, ai-agents, backpressure, vitest, pytest, playwright, ctrf]
status: complete
last_updated: 2026-01-15
last_updated_by: GPT-5.2 Thinking
---

# Research: Summarising test runner output for AI agents

**Date:** 2026-01-15T21:35:13+01:00  
**Researcher:** GPT-5.2 Thinking

## Research Question

You’re looking for ways to **summarise test runner output** (Vitest, Pytest, Playwright) via:

- runner configuration (reporters / flags)
- wrapper scripts
- optionally switching runners if it materially improves output

Constraints / preferences you stated:

- **Simple + machine-readable**
- **One line per test** is good (but not at the expense of huge success output)
- **Silent on success** is attractive / very token efficient
- Primary consumer is an **AI coding agent**
- You don’t yet have strong intuition for CTRF

## Summary

The cleanest “AI-agent-friendly” solution is a **two-channel design**:

1. **Terminal (agent-facing)**: extremely small.
   - Success: one line like `✓ unit`.
   - Failure: one line like `✗ unit`, plus **one line per failing test** (and optionally a short reason).
2. **Artifact (machine-facing)**: always write a structured report file.
   - Prefer a unified JSON schema across stacks.

This is exactly what the “context-efficient backpressure” pattern advocates: swallow success output; surface failure output only.

A practical way to get unified JSON across Vitest + Pytest + Playwright is **CTRF (Common Test Report Format)**, which is a lightweight, consistent JSON schema and has integrations for pytest and Playwright, plus third‑party reporters for Vitest.

## Detailed Findings

### 1) Source document review: `AI-Friendly-Testing-Infrastructure.md`

Your doc already outlines the right direction:

- a `run_silent` wrapper (✓ on success, dump captured output on failure)
- a `just`-based command surface (`just test frontend`, etc.)
- framework flags/reporters to reduce verbosity
- interest in CTRF as a unifying report format

This research focuses on **concrete runner settings + report formats** to make those ideas real.

### 2) Context-efficient backpressure (HumanLayer blog)

The blog describes a pattern used in practice:

- If the command exits 0: emit a tiny success marker.
- Otherwise: emit a failure marker and show the saved output.

This is a wrapper-level concern; it composes well with any runner.

### 3) CTRF: what it is and why it’s relevant

CTRF is a universal JSON schema shaped roughly like:

- `results.tool` → tool name
- `results.summary` → counts and timing
- `results.tests[]` → array of test records (at minimum name/status/duration)

Minimal example shape:

```json
{
  "results": {
    "tool": { "name": "AnyTool" },
    "summary": { "tests": 1, "passed": 1, "failed": 0, "skipped": 0 },
    "tests": [
      { "name": "should be able to login", "status": "passed", "duration": 801 }
    ]
  }
}
```

Why this helps:

- One parser for all frameworks.
- Easy to make **one-line-per-test** summaries with `jq`.
- Easy to print **failures only** to the terminal, while keeping full detail in artifacts.

### 4) Vitest: minimal terminal + JSON/CTRF artifacts

**Terminal output**

- `dot` reporter prints a dot per test with summary (very small on success).
- `verbose` reporter prints one line per test case (great for debugging, but noisier).

**Structured artifacts**

- Vitest can write `json` output to a file using `outputFile`, and can combine multiple reporters.

Example: `dot` for terminal + JSON artifact:

```ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    reporters: ['dot', 'json'],
    outputFile: { json: 'artifacts/test/vitest.json' },
  },
})
```

**CTRF option**

- `vitest-ctrf-json-reporter` is a third-party reporter that emits CTRF.

### 5) Pytest: quiet mode, tiny tracebacks, CTRF artifacts

**Terminal shaping**

Pytest has built-in flags for compact output:

- `-q` / `--quiet` reduces noise.
- `--tb=line` yields one line per failure; `--tb=short` is also compact.
- `-v` gives one line per test (PASSED/FAILED) when you want it.
- `-x` / `--exitfirst` fail-fast (useful for “one failure at a time”).

Typical compact terminal mode:

```bash
pytest -q --tb=line
```

**Structured artifacts**

- Built-in: `--junitxml=...`.
- CTRF: `pytest-json-ctrf` provides:

```bash
pytest --ctrf artifacts/test/pytest.ctrf.json
```

### 6) Playwright: concise terminal + JSON/CTRF artifacts

**Terminal shaping**

- Playwright supports concise reporters and notes `dot` is the default on CI.
- For “one line per test” when you want it, `line` or `list` are common.

**Structured artifacts**

- Built-in `json` reporter supports `outputFile` in config.

```ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  reporter: [
    ['dot'],
    ['json', { outputFile: 'artifacts/test/playwright.json' }],
  ],
})
```

**CTRF option**

- `playwright-ctrf-json-reporter` emits CTRF JSON.
- It supports output options (`outputFile`, `outputDir`) and a `minimal: true` mode.

## Practical Recipes

### Recipe A: Minimal terminal, CTRF everywhere (recommended)

Goal: **near-silent success** + **one line per failing test** + unified artifacts.

**Vitest**
- Terminal: `dot` (or nothing if wrapped)
- Artifact: CTRF via `vitest-ctrf-json-reporter`

**Pytest**
- Terminal: `-q --tb=line`
- Artifact: `pytest --ctrf artifacts/test/pytest.ctrf.json`

**Playwright**
- Terminal: `dot`
- Artifact: CTRF via `playwright-ctrf-json-reporter` with `minimal: true`

Then standardize on one summariser:

```bash
# Failures only, one line per failing test
jq -r '.results.tests[] | select(.status != "passed") | "\(.status|ascii_upcase) \(.name)"' artifacts/test/*.ctrf.json
```

### Recipe B: Built-in outputs per tool (no CTRF yet)

- Vitest JSON -> `artifacts/test/vitest.json`
- Playwright JSON -> `artifacts/test/playwright.json`
- Pytest JUnit -> `artifacts/test/pytest.xml`

Still workable, but you now have 2–3 schemas.

### Recipe C: “One line per test” mode for debugging

When you explicitly want streaming one-line-per-test:

- Vitest: `--reporter=verbose`
- Pytest: `-v`
- Playwright: `--reporter=line` (or `list`)

Keep “Recipe A” as the default for agent loops.

## Wrapper Pattern

Your existing `run_silent` wrapper is correct. A safer version avoids `eval`:

```bash
run_silent() {
  local description="$1"; shift
  local tmp_file
  tmp_file="$(mktemp)"

  if "$@" >"$tmp_file" 2>&1; then
    printf "✓ %s\n" "$description"
    rm -f "$tmp_file"
    return 0
  else
    local exit_code=$?
    printf "✗ %s\n" "$description"
    cat "$tmp_file"
    rm -f "$tmp_file"
    return "$exit_code"
  fi
}
```

If you always write CTRF artifacts, you can replace `cat "$tmp_file"` with a tiny “failures-only” summary derived from the artifact, and keep the full output saved on disk.

## Code References

- `AI-Friendly-Testing-Infrastructure.md`:
  - run_silent wrapper
  - Just-based invocation surface
  - framework flags/reporters shortlist

## Switching runners

You probably **don’t need to switch** away from Vitest/Pytest/Playwright to meet your stated goals because:

- each can reduce terminal verbosity significantly
- each can produce structured artifacts
- CTRF can unify the schema across the set

Switching becomes attractive mainly if you require a single unified schema **without** third-party reporters.

## Open Questions

(Not blockers; these just influence defaults.)

- Do you want terminal output to be **one line per stage** only, or also **one line per failing test**?
- Where should artifacts live (e.g., `artifacts/test/` vs `.cache/test-reports/`)?

## Sources

- Context-efficient backpressure pattern: https://www.hlyr.dev/blog/context-efficient-backpressure
- Vitest reporters & `outputFile`: https://vitest.dev/guide/reporters
- Pytest output controls (`-q`, `-v`, `--tb=*`): https://docs.pytest.org/en/stable/how-to/output.html
- Playwright reporters & JSON/JUnit output: https://playwright.dev/docs/test-reporters
- CTRF intro/spec example: https://ctrf.io/docs/intro
- Pytest CTRF integration: https://pypi.org/project/pytest-json-ctrf/
- Playwright CTRF reporter: https://github.com/ctrf-io/playwright-ctrf-json-reporter
- Vitest CTRF reporter: https://github.com/avinyaweb/vitest-ctrf-json-reporter
