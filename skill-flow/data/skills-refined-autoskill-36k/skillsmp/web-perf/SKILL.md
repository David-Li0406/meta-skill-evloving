---
name: web-perf
description: Audits web performance using Chrome DevTools MCP. Measures Core Web Vitals, finds render-blocking resources, dependency chains, layout shifts, caching issues, and accessibility gaps. Use for audits, profiling, debugging, or optimising page load performance and Lighthouse scores.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Web Performance Skill

## Tooling Notes

This skill relies on Chrome DevTools MCP. If the MCP server is missing, stop and ask the user to configure it.

## First: Verify MCP Tools Available

Run a quick check before starting. If `navigate_page` or `performance_start_trace` is unavailable, stop and ask the user to add the MCP config.

```json
"chrome-devtools": {
  "type": "local",
  "command": ["npx", "-y", "chrome-devtools-mcp@latest"]
}
```

## Key Guidelines

- **Be assertive** and verify claims with network, DOM, or codebase evidence.
- **Verify before recommending** any removals or refactors.
- **Quantify impact** using estimated savings; skip 0ms impact changes.
- **Skip non-issues**: document low impact without recommending changes.
- **Be specific**: name exact assets and sizes when suggesting optimisation.
- **Prioritise ruthlessly**: excellent metrics should be called out as such.

## Workflow

Copy this checklist and use it to track progress through the audit:

```markdown
Audit Progress

- [ ] Phase 1: Performance trace (navigate + record)
- [ ] Phase 2: Core Web Vitals analysis (includes CLS culprits)
- [ ] Phase 3: Network analysis
- [ ] Phase 4: Accessibility snapshot
- [ ] Phase 5: Codebase analysis (skip if third-party site)
```

### Phase 1: Performance Trace

The problem is unknown page performance; capture a cold-load trace so you can diagnose it.

1. Navigate to the target URL:
   ```
   navigate_page(url: "<target-url>")
   ```

2. Start a performance trace with reload:
   ```
   performance_start_trace(autoStop: true, reload: true)
   ```

3. Wait for trace completion and capture the results.

Troubleshooting:
- If the trace is empty, confirm the page loaded via `navigate_page`.
- If insight names do not match, inspect the trace response to list available insights.

### Phase 2: Core Web Vitals Analysis

Use `performance_analyze_insight` to extract key metrics. If an insight name fails, use the `insightSetId` from the trace response to discover available insights.

Common insight names:

| Metric | Insight Name | What to Look For |
|--------|--------------|------------------|
| LCP | `LCPBreakdown` | TTFB, resource load, render delay |
| CLS | `CLSCulprits` | Images without dimensions, injected content, font swaps |
| Render Blocking | `RenderBlocking` | CSS/JS blocking first paint |
| Document Latency | `DocumentLatency` | Server response time issues |
| Network Dependencies | `NetworkRequestsDepGraph` | Chains delaying critical resources |

Example:
```
performance_analyze_insight(insightSetId: "<id-from-trace>", insightName: "LCPBreakdown")
```

Key thresholds (good/needs-improvement/poor):
- TTFB: < 800ms / < 1.8s / > 1.8s
- FCP: < 1.8s / < 3s / > 3s
- LCP: < 2.5s / < 4s / > 4s
- INP: < 200ms / < 500ms / > 500ms
- TBT: < 200ms / < 600ms / > 600ms
- CLS: < 0.1 / < 0.25 / > 0.25
- Speed Index: < 3.4s / < 5.8s / > 5.8s

### Phase 3: Network Analysis

List requests to identify optimisation opportunities:
```
list_network_requests(resourceTypes: ["Script", "Stylesheet", "Document", "Font", "Image"])
```

Look for:

1. **Render-blocking resources**: JS/CSS in `<head>` without `async`/`defer`/`media`.
2. **Network chains**: late-discovered resources that delay critical assets.
3. **Missing preloads**: fonts, hero images, key scripts without preload.
4. **Caching issues**: weak `Cache-Control`, missing `ETag`/`Last-Modified`.
5. **Large payloads**: oversized or uncompressed JS/CSS.
6. **Unused preconnects**: confirm zero requests to the origin before removal.

For details:
```
get_network_request(reqid: <id>)
```

### Phase 4: Accessibility Snapshot

Take an accessibility tree snapshot:
```
take_snapshot(verbose: true)
```

Flag high-level gaps:
- Missing or duplicate ARIA IDs.
- Poor contrast ratios (WCAG AA: 4.5:1 normal text, 3:1 large text).
- Focus traps or missing focus indicators.
- Interactive elements without accessible names.

### Phase 5: Codebase Analysis

Skip if auditing a third-party site without codebase access.

Detect the stack by searching for config files:

| Tool | Config Files |
|------|--------------|
| Webpack | `webpack.config.js`, `webpack.*.js` |
| Vite | `vite.config.js`, `vite.config.ts` |
| Rollup | `rollup.config.js`, `rollup.config.mjs` |
| esbuild | `esbuild.config.js`, build scripts with `esbuild` |
| Parcel | `.parcelrc`, `package.json` (parcel field) |
| Next.js | `next.config.js`, `next.config.mjs` |
| Nuxt | `nuxt.config.js`, `nuxt.config.ts` |
| SvelteKit | `svelte.config.js` |
| Astro | `astro.config.mjs` |

Also check `package.json` for framework dependencies and build scripts.

Tree-shaking and dead code:
- **Webpack**: confirm `mode: "production"`, `sideEffects`, and `usedExports`.
- **Vite/Rollup**: tree-shaking is default; check `treeshake` options.
- Watch for barrel files and large libraries imported wholesale.

Unused JS/CSS:
- Check for CSS-in-JS versus static extraction.
- Look for PurgeCSS/UnCSS, or Tailwind `content` config.
- Identify dynamic imports versus eager loading.

Polyfills:
- Check `@babel/preset-env` targets and `useBuiltIns`.
- Look for oversized `core-js` imports.
- Verify `browserslist` is not overly broad.

Compression and minification:
- Check for `terser`, `esbuild`, or `swc` minification.
- Verify gzip/brotli compression in server config.
- Confirm source maps are external or disabled in production.

## Output Format

Present findings in this order:

1. **Core Web Vitals Summary**: table with metric, value, rating.
2. **Top Issues**: prioritised list with estimated impact (high/medium/low).
3. **Recommendations**: specific, actionable fixes with snippets.
4. **Codebase Findings**: framework/bundler and optimisation notes (omit if no codebase access).
