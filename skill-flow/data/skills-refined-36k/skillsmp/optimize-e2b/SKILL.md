---
name: optimize-e2b
description: Run accessibility and SEO audits in cloud sandboxes, generate remediation specs, and implement fixes. Use when optimizing a website for accessibility (a11y, WCAG) or SEO, or when the user says "optimize", "audit", or "fix accessibility issues".
---

# E2B Optimize Pipeline

Full optimization pipeline: runs automated audits in cloud sandboxes, generates remediation specs, and implements fixes locally.

## Prerequisites

- `E2B_API_KEY` environment variable must be set
- `bun` installed globally (`curl -fsSL https://bun.sh/install | bash`)
- For local audits: project must have `npm run dev` that starts a dev server

## Quick Start

Run audit against a live URL:

```bash
bun .claude/skills/optimize-e2b/scripts/run-audit.ts --url https://your-site.com
```

Or for local development (uploads codebase, starts dev server in sandbox):

```bash
bun .claude/skills/optimize-e2b/scripts/run-audit.ts
```

Options:
- `--url, -u` - Target URL (defaults to localhost:4321)
- `--output, -o` - Output directory (default: `docs/audits/raw`)
- `--tools, -t` - Comma-separated tools (default: `lighthouse,axe,pa11y`)
- `--verbose, -v` - Show detailed output
- `--dev-command` - Dev server command (default: `npm run dev`)
- `--dev-port` - Dev server port (default: `4321`)

## Pipeline Steps

### Step 1: Check for Recent Reports

Check if audit reports exist and are recent (< 1 hour old):

```
docs/audits/raw/axe-results.json
docs/audits/raw/pa11y-results.json
docs/audits/raw/lighthouse-results.json
```

To check file age on macOS:
```bash
stat -f %m docs/audits/raw/axe-results.json
```

Compare to current timestamp. If ALL 3 files exist AND all are < 1 hour old AND user didn't request fresh audits, skip to Step 3.

### Step 2: Run Cloud Audits

Execute the audit script:

```bash
bun .claude/skills/optimize-e2b/scripts/run-audit.ts --url <target-url> --verbose
```

For local testing (uploads codebase, runs dev server in sandbox):

```bash
bun .claude/skills/optimize-e2b/scripts/run-audit.ts --verbose
```

**On failure:** Stop immediately and report the error.

**On success:** Results saved to `docs/audits/raw/`

### Step 3: Parse Audit Reports

Read each JSON report and extract issues. See [parsing-guide.md](parsing-guide.md) for detailed extraction logic.

**Priority mapping:**
| Tool | Severity | Priority |
|------|----------|----------|
| axe | critical | 1 |
| axe | serious | 2 |
| axe | moderate | 3 |
| axe | minor | 4 |
| pa11y | error | 2 |
| pa11y | warning | 3 |
| pa11y | notice | 4 |
| Lighthouse | score 0 | 1 |
| Lighthouse | score <0.5 | 2 |
| Lighthouse | score <0.9 | 3 |

### Step 4: Deduplicate Issues

Many tools report the same issue. Deduplicate by:

1. Normalize selectors (trim whitespace, lowercase tag names)
2. Group by issue type (color-contrast, missing-alt, etc.)
3. For duplicates, keep the report with most detail
4. Merge affected elements lists

### Step 5: Generate Remediation Specs

For each unique issue, create a spec file:

- **Accessibility:** `docs/accessibility/specs/pending/spec-NNN-<slug>.md`
- **SEO:** `docs/seo/specs/pending/spec-NNN-<slug>.md`

See [spec-format.md](spec-format.md) for the required spec format.

### Step 6: Implement Fixes

Execute specs using wave-based implementation:

1. **Discover:** Read all pending specs from `docs/*/specs/pending/*.md`
2. **Build waves:** Group by dependencies (Wave 1 = no deps, Wave 2 = depends on Wave 1, etc.)
3. **Execute each wave:**
   - Move specs to `in-progress/`
   - For parallel-safe specs, use Task tool to spawn parallel agents
   - Each agent implements one spec
4. **Verify:** Run `npm run build` after each wave
5. **Complete:** Move specs to `completed/`
6. **Commit:** `git add -A && git commit -m "fix: implement wave N accessibility/seo fixes"`

### Step 7: Final Verification

```bash
npm run build
npm run test:run
```

### Step 8: Report Summary

Output a summary:

```
========================================
OPTIMIZATION COMPLETE
========================================

Audit Phase:
  - axe-core: X violations found
  - pa11y: X issues found
  - Lighthouse: accessibility X/100, seo X/100

Specs Generated: X
  - Accessibility: X
  - SEO: X

Implementation:
  - Waves executed: X
  - Specs completed: X
  - Files modified: X

Verification:
  - Build: PASS/FAIL
  - Tests: PASS/FAIL

Commits created: X
```

## Directory Structure

```
docs/
├── audits/
│   └── raw/                    # JSON from e2b pipeline
│       ├── axe-results.json
│       ├── pa11y-results.json
│       └── lighthouse-results.json
├── accessibility/
│   └── specs/
│       ├── pending/
│       ├── in-progress/
│       └── completed/
└── seo/
    └── specs/
        ├── pending/
        ├── in-progress/
        └── completed/
```

## Error Handling

| Error | Action |
|-------|--------|
| E2B_API_KEY not set | Stop, tell user to set it |
| Audit CLI fails | Stop, report error, do not proceed |
| JSON parse error | Report which file, skip that report, continue |
| No issues found | Report "No issues found", exit successfully |
| Build fails after wave | Stop, report error, leave specs in `in-progress/` |
| Test fails | Report which tests failed, still mark complete |
