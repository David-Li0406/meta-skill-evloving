---
name: Lighthouse CI Audit
description: Run comprehensive Lighthouse performance, accessibility, SEO, and best practices audits using the project's Lighthouse CI configuration.
---

# Lighthouse CI Audit

This skill runs Lighthouse CI audits on the Bedriftsgrafen.no frontend, producing comprehensive performance, accessibility, SEO, and best practices reports.

## Prerequisites

1. **Dependencies installed**: Ensure `npm install` has been run at the root level (installs `@lhci/cli`).
2. **Frontend built**: The audit runs against the production build, not the dev server.
3. **No backend required**: The audit tests static pages only (pages requiring backend data are excluded).

## Quick Run

```bash
# From project root - builds frontend first, then runs Lighthouse CI
npm run lighthouse
```

## What Gets Audited

The following pages are audited (configured in `lighthouserc.cjs`):

| Page | URL | Purpose |
|------|-----|---------|
| Home | `/` | Main landing/search page |
| Search | `/search` | Search results page |
| About | `/om` | About page |
| Industries | `/bransjer` | Industry explorer |
| Bankruptcies | `/konkurser` | Bankruptcy listings |
| New Establishments | `/nyetableringer` | New company listings |
| Explore | `/utforsk` | Data exploration |

**Excluded pages**: `/kart` (requires backend), `/bedrift/:orgnr` (dynamic data)

> **Note**: The preview server runs on port **5174** (configured in `vite.config.ts`).

## Thresholds

Current score thresholds (defined in `lighthouserc.cjs`):

| Category | Minimum Score | Level |
|----------|---------------|-------|
| **Accessibility** | 85% | Error (blocks CI) |
| **SEO** | 90% | Warn |
| **Best Practices** | 80% | Warn |
| **Performance** | 50% | Warn |

> **Note**: Performance is relaxed due to third-party scripts and dynamic content. Focus on accessibility and SEO first.

## Report Output

After running, Lighthouse CI:
1. Creates reports in `.lighthouseci/` directory
2. Uploads to **temporary-public-storage** (auto-deletes after 7 days)
3. Prints a **shareable link** to view the full report online

## Interpreting Results

### Pass Example
```
✅ All assertions passed.
```

### Failure Example
```
❌ categories:accessibility assertion failed.
   Expected minScore >= 0.85, got 0.78
   
   URL: http://localhost:4173/konkurser
   
   Failing audit: button-name
   - Fix: Add accessible names to all buttons
```

## Manual Steps

### Step 1: Build Frontend
```bash
cd frontend && npm run build
```

### Step 2: Run Lighthouse CI
```bash
# From project root
npx lhci autorun
```

### Step 3: Review Report
- Check terminal output for summary
- Click the temporary-public-storage link for full interactive report
- Review `.lighthouseci/` directory for JSON reports

## Troubleshooting

### "No Chrome found"
Lighthouse needs Chrome/Chromium. Install with:
```bash
# Ubuntu/Debian
sudo apt install chromium-browser

# Or set Chrome path
export CHROME_PATH=/path/to/chrome
```

### "Port 5174 in use"
Kill existing preview servers:
```bash
fuser -k 5174/tcp
```

### Slow Performance Scores
For local testing, scores may vary. Use `--numberOfRuns=5` for more stable results:
```bash
npx lhci autorun --collect.numberOfRuns=5
```

## Configuration Reference

| File | Purpose |
|------|---------|
| `lighthouserc.cjs` | Main Lighthouse CI config |
| `package.json` | Contains `npm run lighthouse` script |
| `.lighthouseci/` | Report output directory (gitignored) |

## Disabled Audits

The following audits are intentionally disabled:
- `valid-source-maps` - Not needed in production
- `uses-http2` - Environment-dependent
- `errors-in-console` - Only issues if backend not running
- `unused-javascript` - Informational, not actionable
- Individual performance metrics - Tracked via category score only

## Best Practices

1. **Run before major releases** to catch accessibility regressions
2. **Compare report links** over time to track improvements
3. **Fix accessibility issues first** - they have the strictest threshold
4. **Don't chase 100 Performance** - focus on Core Web Vitals that matter
