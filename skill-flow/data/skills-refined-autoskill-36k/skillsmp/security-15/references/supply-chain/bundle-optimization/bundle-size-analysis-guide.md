# Bundle Size Analysis and Optimization Guide

## Overview

Bundle size directly impacts application performance, user experience, and infrastructure costs. Large bundles increase load times, consume more bandwidth, and hurt Core Web Vitals scores.

## Performance Targets (2024)

| Metric | Target | Impact |
|--------|--------|--------|
| Initial bundle (gzipped) | < 200KB | Fast First Contentful Paint |
| Total JS (gzipped) | < 500KB | Good Time to Interactive |
| Largest chunk | < 150KB | Avoid long tasks |
| Per-route chunks | < 50KB | Fast navigation |

## Analysis Tools

### 1. Webpack Bundle Analyzer

Interactive treemap visualization of bundle contents.

```bash
# Install
npm install --save-dev webpack-bundle-analyzer

# Add to webpack.config.js
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      reportFilename: 'bundle-report.html',
      openAnalyzer: false
    })
  ]
};

# Generate report
npm run build -- --profile --json > stats.json
npx webpack-bundle-analyzer stats.json
```

**Key Metrics:**
- **Stat size**: Original file size before processing
- **Parsed size**: Size after webpack processing
- **Gzipped size**: Network transfer size (most important)

### 2. Source Map Explorer

Analyzes bundles using source maps without requiring webpack.

```bash
# Install
npm install --save-dev source-map-explorer

# Build with source maps
npm run build

# Analyze
npx source-map-explorer 'dist/**/*.js'

# Generate HTML report
npx source-map-explorer 'dist/main.*.js' --html report.html
```

### 3. BundlePhobia

Check package size before installing.

```bash
# Web interface
# Visit: https://bundlephobia.com/package/lodash

# API for automation
curl -s "https://bundlephobia.com/api/size?package=lodash" | jq '{
    name: .name,
    size: .size,
    gzip: .gzip,
    dependencyCount: .dependencyCount
}'

# VS Code extension: Import Cost
# Shows inline size of imported packages
```

### 4. Size Limit

CI-integrated bundle size checking.

```bash
# Install
npm install --save-dev size-limit @size-limit/preset-app

# package.json
{
  "size-limit": [
    {
      "path": "dist/js/*.js",
      "limit": "200 KB"
    }
  ],
  "scripts": {
    "size": "size-limit",
    "size-check": "size-limit --ci"
  }
}

# GitHub Action
# Automatically comments on PRs with size changes
```

### 5. Bundlewatch

Track bundle size over time in CI.

```bash
# Install
npm install --save-dev bundlewatch

# bundlewatch.config.js
module.exports = {
  files: [
    {
      path: './dist/js/*.js',
      maxSize: '200KB'
    },
    {
      path: './dist/css/*.css',
      maxSize: '50KB'
    }
  ],
  ci: {
    trackBranches: ['main', 'develop']
  }
};
```

## Optimization Techniques

### 1. Tree Shaking

Remove unused code from bundles.

```javascript
// BAD: Imports entire library
import _ from 'lodash';
const result = _.get(obj, 'path');

// GOOD: Named imports (tree-shakeable)
import { get } from 'lodash-es';
const result = get(obj, 'path');

// BEST: Direct module import
import get from 'lodash/get';
const result = get(obj, 'path');
```

**Enable in package.json:**
```json
{
  "sideEffects": false,
  // Or specify files with side effects:
  "sideEffects": [
    "*.css",
    "*.scss",
    "./src/polyfills.js"
  ]
}
```

### 2. Code Splitting

Split code into smaller chunks loaded on demand.

```javascript
// React lazy loading
import React, { Suspense, lazy } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <HeavyComponent />
    </Suspense>
  );
}

// Route-based splitting
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Settings = lazy(() => import('./pages/Settings'));
```

**Webpack magic comments:**
```javascript
// Named chunks for debugging
const Component = lazy(() =>
  import(/* webpackChunkName: "dashboard" */ './Dashboard')
);

// Prefetch for anticipated navigation
const Settings = lazy(() =>
  import(/* webpackPrefetch: true */ './Settings')
);
```

### 3. Dynamic Imports

Load modules only when needed.

```javascript
// Load on user action
async function handleExport() {
  const { exportToPDF } = await import('./exportUtils');
  exportToPDF(data);
}

// Conditional loading
if (needsCharting) {
  const Chart = await import('chart.js');
}
```

### 4. Replace Heavy Libraries

| Heavy Library | Size | Alternative | Size |
|--------------|------|-------------|------|
| moment | 329KB | date-fns | 8KB* |
| moment | 329KB | dayjs | 2KB |
| lodash | 71KB | lodash-es | 8KB* |
| lodash | 71KB | just-* | <1KB each |
| axios | 14KB | ky | 4KB |
| axios | 14KB | fetch (native) | 0KB |
| uuid | 9KB | nanoid | 130B |
| classnames | 1KB | clsx | 516B |
| validator | 58KB | tiny-validation | 2KB |

*With tree shaking

### 5. Externalize Dependencies

Load from CDN instead of bundling.

```javascript
// webpack.config.js
module.exports = {
  externals: {
    react: 'React',
    'react-dom': 'ReactDOM',
    lodash: '_'
  }
};

// index.html
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
```

### 6. Avoid Barrel Files

Barrel files can prevent tree shaking.

```javascript
// BAD: components/index.js (barrel file)
export { Button } from './Button';
export { Modal } from './Modal';
export { Table } from './Table';
// Importing Button may pull in Modal and Table

// GOOD: Direct imports
import { Button } from './components/Button';
```

## Automated Bundle Analysis Script

```bash
#!/bin/bash
# bundle-analyzer.sh

analyze_npm_bundle() {
    local project_dir="$1"
    local report_dir="${2:-./bundle-reports}"

    mkdir -p "$report_dir"

    cd "$project_dir"

    # Check if package.json exists
    if [[ ! -f "package.json" ]]; then
        echo '{"error": "No package.json found"}'
        return 1
    fi

    # Analyze each dependency
    local deps=$(jq -r '.dependencies // {} | keys[]' package.json)
    local results=()

    for pkg in $deps; do
        local size_info=$(curl -s "https://bundlephobia.com/api/size?package=${pkg}" 2>/dev/null)

        if [[ $? -eq 0 ]] && [[ -n "$size_info" ]]; then
            local size=$(echo "$size_info" | jq -r '.size // 0')
            local gzip=$(echo "$size_info" | jq -r '.gzip // 0')
            local deps_count=$(echo "$size_info" | jq -r '.dependencyCount // 0')
            local has_esm=$(echo "$size_info" | jq -r '.hasJSModule // false')

            results+=("{
                \"name\": \"$pkg\",
                \"size\": $size,
                \"gzip\": $gzip,
                \"dependencies\": $deps_count,
                \"treeshakeable\": $has_esm
            }")
        fi
    done

    # Generate report
    echo "{
        \"project\": \"$(basename "$project_dir")\",
        \"analyzed_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
        \"packages\": [$(IFS=,; echo "${results[*]}")],
        \"summary\": $(generate_summary "${results[@]}")
    }" | jq '.' > "$report_dir/bundle-analysis.json"
}

generate_summary() {
    local total_size=0
    local total_gzip=0
    local large_packages=()

    for result in "$@"; do
        local size=$(echo "$result" | jq -r '.size')
        local gzip=$(echo "$result" | jq -r '.gzip')
        local name=$(echo "$result" | jq -r '.name')

        total_size=$((total_size + size))
        total_gzip=$((total_gzip + gzip))

        # Flag packages > 50KB gzipped
        if [[ $gzip -gt 51200 ]]; then
            large_packages+=("$name")
        fi
    done

    echo "{
        \"total_size_bytes\": $total_size,
        \"total_gzip_bytes\": $total_gzip,
        \"total_size_human\": \"$(numfmt --to=iec $total_size)B\",
        \"total_gzip_human\": \"$(numfmt --to=iec $total_gzip)B\",
        \"large_packages\": $(printf '%s\n' "${large_packages[@]}" | jq -R . | jq -s .)
    }"
}

# Find optimization opportunities
find_optimizations() {
    local manifest="$1"
    local recommendations=()

    # Check for known heavy packages with lighter alternatives
    declare -A ALTERNATIVES=(
        ["moment"]="date-fns or dayjs"
        ["lodash"]="lodash-es with named imports"
        ["axios"]="ky or native fetch"
        ["uuid"]="nanoid"
        ["validator"]="smaller validation library"
        ["jquery"]="native DOM APIs"
        ["underscore"]="lodash-es"
    )

    local deps=$(jq -r '.dependencies // {} | keys[]' "$manifest")

    for pkg in $deps; do
        if [[ -n "${ALTERNATIVES[$pkg]}" ]]; then
            recommendations+=("{
                \"package\": \"$pkg\",
                \"recommendation\": \"Consider replacing with ${ALTERNATIVES[$pkg]}\",
                \"reason\": \"Smaller bundle size available\"
            }")
        fi
    done

    # Check for packages without ESM support
    for pkg in $deps; do
        local info=$(curl -s "https://bundlephobia.com/api/size?package=${pkg}" 2>/dev/null)
        local has_esm=$(echo "$info" | jq -r '.hasJSModule // false')

        if [[ "$has_esm" == "false" ]]; then
            recommendations+=("{
                \"package\": \"$pkg\",
                \"recommendation\": \"Package lacks ESM support\",
                \"reason\": \"Tree shaking may be limited\"
            }")
        fi
    done

    printf '%s\n' "${recommendations[@]}" | jq -s '.'
}
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
name: Bundle Size Check

on:
  pull_request:
    branches: [main]

jobs:
  bundle-size:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Analyze bundle
        run: npx source-map-explorer 'dist/**/*.js' --json > bundle-stats.json

      - name: Check size limits
        run: npx size-limit --ci

      - name: Comment on PR
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const stats = JSON.parse(fs.readFileSync('bundle-stats.json'));
            // Format and post comment
```

### Size Limit Config

```json
{
  "size-limit": [
    {
      "name": "Initial JS",
      "path": "dist/js/main.*.js",
      "limit": "150 KB",
      "gzip": true
    },
    {
      "name": "Initial CSS",
      "path": "dist/css/main.*.css",
      "limit": "30 KB",
      "gzip": true
    },
    {
      "name": "Total bundle",
      "path": "dist/**/*.js",
      "limit": "400 KB",
      "gzip": true
    }
  ]
}
```

## Reporting Format

### JSON Output

```json
{
  "analysis_date": "2024-01-15T10:30:00Z",
  "project": "my-app",
  "bundle_stats": {
    "total_size": 524288,
    "total_gzip": 156000,
    "chunk_count": 12,
    "largest_chunk": {
      "name": "vendor.js",
      "size": 245000,
      "gzip": 78000
    }
  },
  "packages": [
    {
      "name": "lodash",
      "size": 71000,
      "gzip": 25000,
      "percentage": 16.0,
      "treeshakeable": false,
      "recommendation": "Replace with lodash-es"
    }
  ],
  "optimizations": [
    {
      "type": "replace_library",
      "package": "moment",
      "alternative": "date-fns",
      "potential_savings": "320KB"
    },
    {
      "type": "enable_treeshaking",
      "package": "lodash",
      "action": "Switch to named imports from lodash-es"
    }
  ],
  "score": {
    "current": 65,
    "target": 85,
    "grade": "C"
  }
}
```

### Markdown Report

```markdown
# Bundle Size Analysis Report

**Project:** my-app
**Date:** 2024-01-15

## Summary

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Total JS (gzip) | 156 KB | < 200 KB | ✅ |
| Initial bundle | 78 KB | < 150 KB | ✅ |
| Largest chunk | 78 KB | < 100 KB | ✅ |

## Large Packages (> 20KB gzipped)

| Package | Size | Gzip | % of Bundle |
|---------|------|------|-------------|
| lodash | 71 KB | 25 KB | 16% |
| moment | 329 KB | 72 KB | 46% |
| react-dom | 42 KB | 13 KB | 8% |

## Optimization Opportunities

### 🔴 Critical: Replace moment.js
- **Current size:** 329 KB (72 KB gzipped)
- **Alternative:** date-fns (8 KB gzipped with tree-shaking)
- **Potential savings:** 64 KB gzipped (41% reduction)

### 🟡 Recommended: Use lodash-es
- **Current size:** 71 KB (25 KB gzipped)
- **Alternative:** Named imports from lodash-es
- **Potential savings:** 20 KB gzipped (tree-shaking)

### 🟢 Good Practice: Enable code splitting
- Split vendor chunks
- Lazy load routes
- Dynamic import heavy components
```

## References

- [Webpack Bundle Analyzer](https://github.com/webpack-contrib/webpack-bundle-analyzer)
- [Source Map Explorer](https://github.com/danvk/source-map-explorer)
- [BundlePhobia](https://bundlephobia.com/)
- [Size Limit](https://github.com/ai/size-limit)
- [Bundlewatch](https://github.com/bundlewatch/bundlewatch)
- [awesome-bundle-size](https://github.com/kristerkari/awesome-bundle-size)
- [Codecov - 8 Ways to Optimize Bundle Size](https://about.codecov.io/blog/8-ways-to-optimize-your-javascript-bundle-size/)
