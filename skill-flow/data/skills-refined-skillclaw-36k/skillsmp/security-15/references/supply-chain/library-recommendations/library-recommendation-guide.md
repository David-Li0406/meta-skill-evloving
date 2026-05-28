# Library Recommendation Guide

## Overview

Library recommendations help developers choose better alternatives to their current dependencies based on security, performance, maintainability, and community health metrics.

## Recommendation Criteria

### 1. Security Score (Weight: 35%)

| Factor | Description | Data Source |
|--------|-------------|-------------|
| CVE History | Number and severity of past vulnerabilities | OSV.dev, NVD |
| Time to Patch | Average time to fix reported vulnerabilities | deps.dev |
| Security Practices | Signed releases, SLSA compliance, 2FA | OpenSSF Scorecard |
| Dependency Risk | Transitive vulnerability exposure | deps.dev |

**Scoring:**
```
security_score = (
    (10 - min(cve_count * severity_weight, 10)) * 0.3 +
    (patch_speed_score) * 0.3 +
    (scorecard.security) * 0.25 +
    (10 - transitive_vuln_score) * 0.15
)
```

### 2. Maintenance Health (Weight: 25%)

| Factor | Description | Data Source |
|--------|-------------|-------------|
| Release Frequency | Regular releases indicate active maintenance | Registry API |
| Commit Activity | Recent commits in past 90 days | GitHub API |
| Issue Response | Time to first response on issues | GitHub API |
| PR Merge Time | Time from PR open to merge | GitHub API |
| Maintainer Count | Number of active maintainers | deps.dev |

**Scoring:**
```
maintenance_score = (
    (release_recency) * 0.25 +
    (commit_activity) * 0.25 +
    (issue_response_speed) * 0.2 +
    (pr_merge_efficiency) * 0.15 +
    (maintainer_diversity) * 0.15
)
```

### 3. Performance & Reliability (Weight: 20%)

| Factor | Description | Data Source |
|--------|-------------|-------------|
| Bundle Size | Smaller is generally better | bundlephobia.com |
| Tree-shaking | ESM support for dead code elimination | Package analysis |
| Runtime Performance | Benchmarks where available | Community benchmarks |
| Breaking Changes | Frequency of major version bumps | Changelog analysis |

### 4. Community Health (Weight: 10%)

| Factor | Description | Data Source |
|--------|-------------|-------------|
| Download Trend | Growing vs declining usage | npm/PyPI stats |
| GitHub Stars | Community interest indicator | GitHub API |
| Stack Overflow | Questions and answers | SO API |
| Documentation | Quality of docs | Heuristic analysis |

### 5. Compatibility (Weight: 10%)

| Factor | Description | Data Source |
|--------|-------------|-------------|
| License Compatibility | Compatible with project license | SPDX analysis |
| API Compatibility | Similar API surface | AI analysis |
| Breaking Changes | Migration effort required | Changelog analysis |
| Platform Support | Same runtime/platform support | Package metadata |

## Data Sources and APIs

### deps.dev API

Primary source for package health and security data:

```bash
# Get package info with scorecard
get_package_info() {
    local pkg="$1"
    local ecosystem="$2"

    curl -s "https://api.deps.dev/v3alpha/systems/${ecosystem}/packages/${pkg}" | jq '{
        versions: [.versions[].version],
        default_version: .versions | map(select(.isDefault)) | .[0].version,
        scorecard: .scorecardV2,
        links: .links
    }'
}

# Get version-specific info
get_version_info() {
    local pkg="$1"
    local version="$2"
    local ecosystem="$3"

    curl -s "https://api.deps.dev/v3alpha/systems/${ecosystem}/packages/${pkg}/versions/${version}" | jq '{
        publishedAt: .publishedAt,
        licenses: .licenses,
        dependencies: .dependencies,
        advisories: .advisories
    }'
}
```

### Snyk Advisor

Provides package health scores and comparisons:

```bash
# Snyk Advisor URL pattern
# https://snyk.io/advisor/npm-package/{package}
# https://snyk.io/advisor/python/{package}

# Snyk has a public API for package health (limited)
get_snyk_score() {
    local pkg="$1"
    # Note: May require API key for programmatic access
    curl -s "https://snyk.io/advisor/npm-package/${pkg}" | \
        grep -oP 'package-health-score.*?([0-9]+)' | head -1
}
```

### Libraries.io

Provides package metadata and alternatives:

```bash
# Libraries.io API
# Requires API key from https://libraries.io/api
get_package_alternatives() {
    local pkg="$1"
    local platform="$2"  # npm, pypi, etc.
    local api_key="$LIBRARIES_IO_KEY"

    curl -s "https://libraries.io/api/${platform}/${pkg}?api_key=${api_key}" | jq '{
        name: .name,
        description: .description,
        rank: .rank,
        dependent_repos_count: .dependent_repos_count,
        dependents_count: .dependents_count,
        latest_release: .latest_release_number,
        keywords: .keywords
    }'
}
```

### npm Registry

```bash
# Get package metadata
get_npm_info() {
    local pkg="$1"
    curl -s "https://registry.npmjs.org/${pkg}" | jq '{
        name: .name,
        description: .description,
        keywords: .keywords,
        latest: ."dist-tags".latest,
        deprecated: .deprecated,
        maintainers: .maintainers | length,
        repository: .repository.url
    }'
}

# Get download stats
get_npm_downloads() {
    local pkg="$1"
    curl -s "https://api.npmjs.org/downloads/point/last-month/${pkg}" | jq '.downloads'
}
```

### Bundle Size (bundlephobia.com)

```bash
# Get bundle size for npm packages
get_bundle_size() {
    local pkg="$1"
    curl -s "https://bundlephobia.com/api/size?package=${pkg}" | jq '{
        size: .size,
        gzip: .gzip,
        dependencyCount: .dependencyCount
    }'
}
```

## Common Library Alternatives

### JavaScript/npm

| Current | Alternative | Reason |
|---------|-------------|--------|
| moment | date-fns, dayjs, luxon | Smaller size, tree-shakeable, actively maintained |
| request | axios, node-fetch, got, ky | request is deprecated |
| lodash | lodash-es, ramda, just-* | Better tree-shaking |
| underscore | lodash-es | More features, better maintained |
| colors | chalk, picocolors | colors had supply chain attack |
| faker | @faker-js/faker | faker was sabotaged |
| event-stream | through2, pump | event-stream was compromised |
| uuid (v1-v3) | uuid v9+, nanoid | Security improvements |
| express-validator | zod, yup, joi | Better TypeScript support |
| bcrypt | argon2, bcryptjs | argon2 is more secure |
| crypto (node) | libsodium, tweetnacl | Purpose-built crypto |
| node-sass | sass (dart-sass) | node-sass deprecated |
| tslint | eslint + typescript-eslint | tslint deprecated |

### Python/PyPI

| Current | Alternative | Reason |
|---------|-------------|--------|
| pycrypto | pycryptodome, cryptography | pycrypto unmaintained |
| nose | pytest | nose is deprecated |
| fabric | fabric2, invoke | Major rewrite, better maintained |
| urllib2 | requests, httpx | Better API, maintained |
| optparse | argparse, click, typer | optparse deprecated |
| mysql-python | mysqlclient, PyMySQL | mysql-python unmaintained |
| PIL | Pillow | PIL unmaintained, Pillow is fork |
| pyOpenSSL | cryptography | Better API, security |
| python-dateutil | pendulum, arrow | More features |

### Go Modules

| Current | Alternative | Reason |
|---------|-------------|--------|
| gorilla/mux | chi, gin, echo | gorilla archived |
| go-kit | kratos, micro | More active development |

## AI-Powered Recommendation Engine

### Claude Analysis Prompt

```markdown
You are a library recommendation engine analyzing package dependencies. Given the following package information, recommend better alternatives if available.

## Current Package
- Name: {package_name}
- Ecosystem: {ecosystem}
- Current Version: {version}
- Security Score: {security_score}/10
- Maintenance Score: {maintenance_score}/10
- Last Update: {last_update}
- Open CVEs: {cve_count}
- Downloads/month: {downloads}

## Known Issues
{known_issues}

## Analysis Request
1. Is this package still the best choice for its purpose?
2. Are there better alternatives based on:
   - Security record
   - Performance characteristics
   - Bundle size (for frontend)
   - Maintenance activity
   - Community health
3. What would be the migration effort?
4. Are there any red flags about this package?

## Output Format
{
    "current_package": "package-name",
    "recommendation": "keep" | "consider_alternative" | "replace_urgently",
    "alternatives": [
        {
            "name": "alternative-package",
            "reason": "Why this is better",
            "migration_effort": "low" | "medium" | "high",
            "security_improvement": "+2 points",
            "size_reduction": "50KB smaller",
            "compatibility": "Drop-in replacement" | "API changes required"
        }
    ],
    "rationale": "Overall analysis and recommendation",
    "priority": "critical" | "high" | "medium" | "low"
}
```

### Recommendation Categories

1. **Replace Urgently** (Priority: Critical)
   - Known security compromises (supply chain attacks)
   - Explicitly deprecated with security issues
   - Unmaintained with unpatched CVEs

2. **Consider Alternative** (Priority: High)
   - Deprecated but functional
   - Better alternatives exist with significant improvements
   - Declining maintenance activity

3. **Keep** (Priority: Low)
   - Package is healthy
   - No clearly better alternatives
   - Migration effort outweighs benefits

## Implementation Pattern

```bash
#!/bin/bash
# library-recommender.sh

recommend_alternatives() {
    local manifest="$1"
    local ecosystem="$2"

    # Extract dependencies
    local deps=$(extract_dependencies "$manifest" "$ecosystem")

    # Analyze each dependency
    for dep in $deps; do
        local info=$(get_package_health "$dep" "$ecosystem")
        local security_score=$(echo "$info" | jq -r '.security_score')
        local maintenance_score=$(echo "$info" | jq -r '.maintenance_score')

        # Check against known replacements
        local replacement=$(check_known_replacements "$dep" "$ecosystem")

        # If package has issues or known replacement exists
        if [[ $security_score -lt 6 ]] || [[ -n "$replacement" ]]; then
            # Use Claude for intelligent recommendation
            local recommendation=$(get_ai_recommendation "$dep" "$info" "$replacement")
            echo "$recommendation"
        fi
    done
}

get_ai_recommendation() {
    local pkg="$1"
    local info="$2"
    local known_replacement="$3"

    # Load RAG context
    local rag_context=$(cat "$RAG_DIR/library-recommendations/*.md")

    # Call Claude API with context
    local prompt="Analyze $pkg and recommend alternatives if needed.
Package info: $info
Known replacement: $known_replacement
Context: $rag_context"

    call_claude_api "$prompt"
}
```

## Output Formats

### Human-Readable Markdown

```markdown
# Library Recommendations Report

## Urgent Replacements

### 🔴 moment → date-fns
**Current**: moment@2.29.4
**Recommended**: date-fns@3.0.0

**Why Replace:**
- moment is in maintenance mode (no new features)
- Bundle size: 329KB → 8KB (tree-shaken)
- Better TypeScript support
- Immutable by design

**Migration Effort:** Medium
- Most date formatting functions have direct equivalents
- Some locale handling differs
- [Migration Guide](https://github.com/date-fns/date-fns/blob/main/docs/unicodeTokens.md)

---

## Consider Alternatives

### 🟡 lodash → lodash-es
**Current**: lodash@4.17.21
**Recommended**: lodash-es@4.17.21

**Why Consider:**
- Enable tree-shaking (reduce bundle by ~80%)
- Same API, drop-in replacement
- Better for modern bundlers

**Migration Effort:** Low
- Change imports from `import _ from 'lodash'`
- To `import { map, filter } from 'lodash-es'`

---

## Healthy Packages (No Changes Needed)

✅ axios@1.6.0 - Well maintained, no alternatives clearly better
✅ express@4.18.2 - Industry standard, excellent security record
```

### JSON Output

```json
{
    "scan_date": "2024-01-15T10:30:00Z",
    "manifest": "package.json",
    "recommendations": [
        {
            "current": {
                "name": "moment",
                "version": "2.29.4",
                "security_score": 7,
                "maintenance_score": 4
            },
            "recommendation": "replace_urgently",
            "alternative": {
                "name": "date-fns",
                "version": "3.0.0",
                "security_score": 9,
                "maintenance_score": 9,
                "size_reduction": "97%"
            },
            "rationale": "moment is in maintenance mode with no new features planned",
            "migration_effort": "medium",
            "priority": "high"
        }
    ],
    "summary": {
        "total_dependencies": 45,
        "urgent_replacements": 2,
        "consider_alternatives": 5,
        "healthy": 38
    }
}
```

## References

- [Snyk Advisor](https://snyk.io/advisor/) - Package health and comparisons
- [deps.dev](https://deps.dev/) - Open Source Insights
- [bundlephobia](https://bundlephobia.com/) - npm bundle size analysis
- [Libraries.io](https://libraries.io/) - Package discovery and metadata
- [OpenSSF Scorecard](https://github.com/ossf/scorecard) - Security health metrics
- [Socket.dev](https://socket.dev/) - Supply chain security
