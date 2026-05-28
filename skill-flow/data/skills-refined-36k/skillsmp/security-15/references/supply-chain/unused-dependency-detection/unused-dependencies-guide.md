# Unused Dependency Detection and Removal

## Overview

Unused dependencies increase security risk, slow build times, and waste resources. Regularly auditing and removing unused packages is essential for supply chain hygiene.

## Why Remove Unused Dependencies?

### Security Benefits
- **Reduced attack surface**: Fewer packages = fewer potential vulnerabilities
- **Smaller supply chain**: Less code to audit and trust
- **Faster patching**: Less noise in vulnerability scans

### Performance Benefits
- **Faster installs**: Fewer packages to download and install
- **Smaller bundles**: Less code shipped to users (frontend)
- **Faster builds**: Less code to parse and compile
- **Reduced CI/CD costs**: Lower compute time and storage

### Maintenance Benefits
- **Cleaner codebase**: Easier to understand actual dependencies
- **Fewer updates**: Less maintenance burden
- **Clearer audit trail**: Know exactly what you depend on

## Tools by Ecosystem

### Node.js / npm

#### depcheck
The gold standard for finding unused npm dependencies.

```bash
# Install globally
npm install -g depcheck

# Run in project directory
depcheck

# Output unused dependencies
depcheck --json

# Ignore specific patterns
depcheck --ignores="@types/*,eslint-*"

# Check specific directories
depcheck --ignore-dirs="dist,build"
```

**Sample Output:**
```
Unused dependencies
* lodash
* moment

Unused devDependencies
* @types/lodash
* jest-extended

Missing dependencies
* chalk
```

#### npm-check
Interactive tool for managing dependencies.

```bash
# Install
npm install -g npm-check

# Check for unused packages
npm-check

# Interactive update mode
npm-check -u

# Skip unused check (just updates)
npm-check -s
```

#### knip
Modern alternative with broader detection.

```bash
# Install
npm install -g knip

# Run analysis
knip

# With configuration
# knip.json:
{
  "entry": ["src/index.ts"],
  "project": ["src/**/*.ts"],
  "ignore": ["**/*.test.ts"]
}
```

### Python

#### pipreqs
Regenerates requirements.txt based on actual imports.

```bash
# Install
pip install pipreqs

# Generate new requirements from imports
pipreqs . --force

# Compare with existing requirements
pipreqs . --print
```

#### vulture
Finds dead code including unused imports.

```bash
# Install
pip install vulture

# Find unused code
vulture myproject/

# With minimum confidence threshold
vulture myproject/ --min-confidence 80

# Generate whitelist for false positives
vulture myproject/ --make-whitelist > whitelist.py
```

#### pip-autoremove
Removes packages and their unused dependencies.

```bash
# Install
pip install pip-autoremove

# Remove package and unused deps
pip-autoremove package-name -y

# List what would be removed
pip-autoremove package-name --list
```

#### deptry
Modern dependency checker for Python.

```bash
# Install
pip install deptry

# Run analysis
deptry .

# Output formats
deptry . --json-output report.json
```

### Go

```bash
# Built-in unused import detection
go build ./...  # Fails on unused imports

# Find unused dependencies
go mod tidy  # Removes unused from go.mod

# Analyze what's used
go mod why -m github.com/some/package
```

### Rust

```bash
# Find unused dependencies
cargo machete

# Or use cargo-udeps
cargo install cargo-udeps
cargo +nightly udeps
```

### Java / Maven

```xml
<!-- Maven dependency plugin -->
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-dependency-plugin</artifactId>
    <version>3.6.0</version>
    <executions>
        <execution>
            <id>analyze</id>
            <goals>
                <goal>analyze</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

```bash
mvn dependency:analyze
```

## Tree Shaking for Frontend Bundles

### Webpack Configuration

```javascript
// webpack.config.js
module.exports = {
  mode: 'production',  // Enables tree shaking
  optimization: {
    usedExports: true,  // Mark unused exports
    minimize: true,     // Remove marked code
    sideEffects: true,  // Respect sideEffects flag
  }
};
```

### package.json sideEffects

```json
{
  "name": "my-package",
  "sideEffects": false,  // All modules are pure
  // Or specify files with side effects:
  "sideEffects": [
    "*.css",
    "./src/polyfills.js"
  ]
}
```

### ESM Import Best Practices

```javascript
// BAD - imports entire library
import _ from 'lodash';
const result = _.get(obj, 'path');

// GOOD - imports only what's needed
import get from 'lodash/get';
const result = get(obj, 'path');

// BEST - use ES module version
import { get } from 'lodash-es';
const result = get(obj, 'path');
```

### Bundle Analysis

```bash
# Webpack bundle analyzer
npm install --save-dev webpack-bundle-analyzer

# Add to webpack config
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin()
  ]
};

# Vite
npm install --save-dev rollup-plugin-visualizer

# esbuild
npx esbuild-visualizer
```

## Automated Detection Script

```bash
#!/bin/bash
# unused-deps-checker.sh

check_npm_unused() {
    local project_dir="$1"
    echo "=== Checking npm dependencies ==="

    if [[ -f "$project_dir/package.json" ]]; then
        cd "$project_dir"
        npx depcheck --json 2>/dev/null | jq '{
            unused_deps: .dependencies,
            unused_devDeps: .devDependencies,
            missing: .missing
        }'
    fi
}

check_python_unused() {
    local project_dir="$1"
    echo "=== Checking Python dependencies ==="

    if [[ -f "$project_dir/requirements.txt" ]]; then
        cd "$project_dir"

        # Generate requirements from actual imports
        pipreqs . --print --force 2>/dev/null > /tmp/actual_reqs.txt

        # Compare with existing
        echo "Potentially unused:"
        comm -23 <(sort requirements.txt | cut -d'=' -f1 | tr '[:upper:]' '[:lower:]') \
                 <(sort /tmp/actual_reqs.txt | cut -d'=' -f1 | tr '[:upper:]' '[:lower:]')
    fi
}

check_bundle_size() {
    local project_dir="$1"
    echo "=== Checking bundle size ==="

    if [[ -f "$project_dir/package.json" ]]; then
        cd "$project_dir"

        # Check for large dependencies
        npx cost-of-modules 2>/dev/null | head -20
    fi
}

# Main
PROJECT_DIR="${1:-.}"
check_npm_unused "$PROJECT_DIR"
check_python_unused "$PROJECT_DIR"
check_bundle_size "$PROJECT_DIR"
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Dependency Audit

on:
  pull_request:
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  check-unused:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check unused npm dependencies
        run: |
          npm install
          npx depcheck --json > unused-deps.json
          if [ $(jq '.dependencies | length' unused-deps.json) -gt 0 ]; then
            echo "::warning::Found unused dependencies"
            jq '.dependencies' unused-deps.json
          fi

      - name: Analyze bundle size
        run: |
          npm run build
          npx bundlesize
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: check-unused-deps
        name: Check unused dependencies
        entry: npx depcheck --ignores="@types/*"
        language: system
        pass_filenames: false
        always_run: true
```

## Best Practices

### Regular Audits
- Run unused dependency checks weekly
- Include in PR review process
- Track bundle size over time

### Safe Removal Process
1. **Identify**: Run detection tools
2. **Verify**: Search codebase for usage
3. **Test**: Run full test suite after removal
4. **Monitor**: Check production for issues

### Common False Positives
- TypeScript type definitions (`@types/*`)
- Webpack loaders and plugins
- Babel presets and plugins
- ESLint plugins and configs
- Peer dependencies
- Build tools (only used in scripts)

### Handling False Positives

```javascript
// depcheck config (.depcheckrc)
{
  "ignores": [
    "@types/*",
    "eslint-*",
    "prettier"
  ],
  "specials": [
    "eslint",
    "webpack",
    "babel"
  ]
}
```

## Metrics to Track

| Metric | Description | Target |
|--------|-------------|--------|
| Dependency count | Total packages in lockfile | Minimize |
| Bundle size | Production JS size | < 200KB gzipped |
| Install time | `npm ci` duration | < 60s |
| Unused ratio | Unused / Total deps | 0% |
| Deep deps | Transitive dependencies | Audit regularly |

## References

- [depcheck](https://github.com/depcheck/depcheck)
- [npm-check](https://github.com/dylang/npm-check)
- [vulture](https://github.com/jendrikseipp/vulture)
- [pipreqs](https://github.com/bndr/pipreqs)
- [Webpack Tree Shaking](https://webpack.js.org/guides/tree-shaking/)
- [web.dev - Reduce JavaScript payloads](https://web.dev/articles/reduce-javascript-payloads-with-tree-shaking)
