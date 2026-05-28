# Abandoned and Deprecated Package Detection

## Overview

Abandoned packages pose significant security risks as they no longer receive security updates, leaving vulnerabilities unpatched. Detecting and replacing unmaintained dependencies is critical for supply chain security.

## Risk Indicators

### High-Risk Signals

| Indicator | Risk Level | Threshold |
|-----------|------------|-----------|
| No commits | Critical | > 2 years |
| No releases | High | > 1 year |
| Unaddressed security issues | Critical | Any open CVE |
| Deprecated flag | High | Package marked deprecated |
| Archived repository | Critical | Repository archived |
| Maintainer inactive | Medium | No activity > 1 year |
| No response to issues | Medium | > 100 open, none addressed |
| Failing CI | Medium | Main branch broken |

### Maintenance Health Scoring

```bash
calculate_maintenance_score() {
    local pkg="$1"
    local ecosystem="$2"
    local score=100

    # Get package metadata
    local last_commit=$(get_last_commit_date "$pkg" "$ecosystem")
    local last_release=$(get_last_release_date "$pkg" "$ecosystem")
    local open_issues=$(get_open_issues_count "$pkg" "$ecosystem")
    local is_deprecated=$(check_deprecated "$pkg" "$ecosystem")
    local is_archived=$(check_archived "$pkg" "$ecosystem")

    # Deduct points for risk indicators
    local days_since_commit=$(days_since "$last_commit")
    local days_since_release=$(days_since "$last_release")

    # Critical: Archived repository
    if [[ "$is_archived" == "true" ]]; then
        score=$((score - 50))
    fi

    # Critical: Explicitly deprecated
    if [[ "$is_deprecated" == "true" ]]; then
        score=$((score - 40))
    fi

    # High: No recent commits
    if [[ $days_since_commit -gt 730 ]]; then  # 2 years
        score=$((score - 30))
    elif [[ $days_since_commit -gt 365 ]]; then  # 1 year
        score=$((score - 15))
    fi

    # Medium: No recent releases
    if [[ $days_since_release -gt 365 ]]; then
        score=$((score - 20))
    elif [[ $days_since_release -gt 180 ]]; then
        score=$((score - 10))
    fi

    # Medium: Too many open issues
    if [[ $open_issues -gt 500 ]]; then
        score=$((score - 15))
    elif [[ $open_issues -gt 100 ]]; then
        score=$((score - 5))
    fi

    echo "$score"
}
```

## Detection Methods

### OpenSSF Scorecard

OpenSSF Scorecard provides automated security health metrics:

```bash
# Install scorecard
brew install scorecard

# Check a GitHub repository
scorecard --repo=github.com/owner/repo

# Key checks for abandonment:
# - Maintained: Does the project have recent activity?
# - Contributors: Are there multiple active contributors?
# - Branch-Protection: Are security practices in place?

# API access
curl -s "https://api.securityscorecards.dev/projects/github.com/owner/repo" | \
    jq '{
        score: .score,
        maintained: .checks[] | select(.name == "Maintained"),
        contributors: .checks[] | select(.name == "Contributors")
    }'
```

### deps.dev API

```bash
# Get package health info
check_depsdev() {
    local pkg="$1"
    local ecosystem="$2"

    local url="https://api.deps.dev/v3alpha/systems/${ecosystem}/packages/${pkg}"
    local response=$(curl -s "$url")

    echo "$response" | jq '{
        name: .package.name,
        latest_version: .versions[-1].version,
        scorecard: .scorecardV2,
        links: .links
    }'
}

# Check for deprecation notices
check_deprecation() {
    local pkg="$1"
    local ecosystem="$2"

    case "$ecosystem" in
        npm)
            curl -s "https://registry.npmjs.org/$pkg" | \
                jq -r '.deprecated // "not deprecated"'
            ;;
        pypi)
            curl -s "https://pypi.org/pypi/$pkg/json" | \
                jq -r '.info.classifiers[] | select(contains("Development Status :: 7"))'
            ;;
    esac
}
```

### GitHub API

```bash
check_github_health() {
    local repo="$1"

    # Get repository info
    local repo_info=$(gh api "repos/$repo" 2>/dev/null)

    # Check if archived
    local archived=$(echo "$repo_info" | jq -r '.archived')

    # Get last commit date
    local last_commit=$(gh api "repos/$repo/commits?per_page=1" | \
        jq -r '.[0].commit.author.date')

    # Get open issues count
    local open_issues=$(echo "$repo_info" | jq -r '.open_issues_count')

    # Get last release
    local last_release=$(gh api "repos/$repo/releases/latest" 2>/dev/null | \
        jq -r '.published_at // "never"')

    echo "{
        \"archived\": $archived,
        \"last_commit\": \"$last_commit\",
        \"open_issues\": $open_issues,
        \"last_release\": \"$last_release\"
    }"
}
```

### npm Registry

```bash
check_npm_package() {
    local pkg="$1"
    local registry_url="https://registry.npmjs.org/$pkg"

    local metadata=$(curl -s "$registry_url")

    # Check deprecated status
    local deprecated=$(echo "$metadata" | jq -r '.deprecated // empty')

    # Get time of last publish
    local last_publish=$(echo "$metadata" | jq -r '.time | to_entries | .[-2].value')

    # Get maintainer info
    local maintainers=$(echo "$metadata" | jq '.maintainers | length')

    # Get repository URL for further checks
    local repo_url=$(echo "$metadata" | jq -r '.repository.url // empty')

    echo "{
        \"deprecated\": \"${deprecated:-false}\",
        \"last_publish\": \"$last_publish\",
        \"maintainer_count\": $maintainers,
        \"repository\": \"$repo_url\"
    }"
}
```

### PyPI

```bash
check_pypi_package() {
    local pkg="$1"
    local pypi_url="https://pypi.org/pypi/$pkg/json"

    local metadata=$(curl -s "$pypi_url")

    # Check development status classifiers
    local dev_status=$(echo "$metadata" | jq -r '
        .info.classifiers[] |
        select(startswith("Development Status"))
    ')

    # Check for inactive/deprecated status
    local is_inactive=$(echo "$dev_status" | grep -q "7 - Inactive" && echo "true" || echo "false")

    # Get last release date
    local last_release=$(echo "$metadata" | jq -r '.releases | to_entries | .[-1].value[0].upload_time')

    # Get maintainer info
    local author=$(echo "$metadata" | jq -r '.info.author')
    local maintainer=$(echo "$metadata" | jq -r '.info.maintainer')

    echo "{
        \"development_status\": \"$dev_status\",
        \"inactive\": $is_inactive,
        \"last_release\": \"$last_release\",
        \"author\": \"$author\"
    }"
}
```

## Automated Scanner Script

```bash
#!/bin/bash
# abandoned-pkg-scanner.sh

ABANDONED_THRESHOLD_DAYS=730  # 2 years
WARNING_THRESHOLD_DAYS=365    # 1 year

scan_dependencies() {
    local manifest="$1"
    local ecosystem="$2"

    case "$ecosystem" in
        npm)
            scan_npm_dependencies "$manifest"
            ;;
        pypi)
            scan_pypi_dependencies "$manifest"
            ;;
    esac
}

scan_npm_dependencies() {
    local package_json="$1"

    # Extract dependencies
    local deps=$(jq -r '.dependencies // {} | keys[]' "$package_json")
    local dev_deps=$(jq -r '.devDependencies // {} | keys[]' "$package_json")

    for pkg in $deps $dev_deps; do
        local status=$(check_npm_package "$pkg")
        local deprecated=$(echo "$status" | jq -r '.deprecated')
        local last_publish=$(echo "$status" | jq -r '.last_publish')

        # Calculate days since last publish
        local publish_date=$(date -d "$last_publish" +%s 2>/dev/null || echo 0)
        local now=$(date +%s)
        local days_since=$(( (now - publish_date) / 86400 ))

        # Report findings
        if [[ "$deprecated" != "false" && "$deprecated" != "null" ]]; then
            echo "CRITICAL: $pkg is DEPRECATED: $deprecated"
        elif [[ $days_since -gt $ABANDONED_THRESHOLD_DAYS ]]; then
            echo "WARNING: $pkg has not been updated in $days_since days"
        elif [[ $days_since -gt $WARNING_THRESHOLD_DAYS ]]; then
            echo "INFO: $pkg last updated $days_since days ago"
        fi
    done
}

# Main
if [[ -f "package.json" ]]; then
    scan_dependencies "package.json" "npm"
fi

if [[ -f "requirements.txt" ]]; then
    scan_dependencies "requirements.txt" "pypi"
fi
```

## Finding Alternatives

### Identifying Replacement Packages

```bash
find_alternatives() {
    local pkg="$1"
    local ecosystem="$2"

    # Search for similar packages
    case "$ecosystem" in
        npm)
            # Use npms.io search
            curl -s "https://api.npms.io/v2/search?q=$pkg" | \
                jq '.results[:5] | .[] | {name: .package.name, score: .score.final}'
            ;;
        pypi)
            # Use PyPI search API
            curl -s "https://pypi.org/search/?q=$pkg" | \
                grep -oP '(?<=href="/project/)[^/"]+' | head -5
            ;;
    esac
}
```

### Common Deprecated Package Replacements

| Deprecated | Replacement | Ecosystem |
|------------|-------------|-----------|
| request | axios, node-fetch, got | npm |
| moment | date-fns, dayjs, luxon | npm |
| node-uuid | uuid | npm |
| colors (compromised) | chalk, picocolors | npm |
| event-stream (compromised) | through2, pump | npm |
| nose | pytest | pypi |
| pycrypto | pycryptodome | pypi |

## Reporting Format

```json
{
    "scan_date": "2024-01-15T10:30:00Z",
    "project": "my-project",
    "abandoned_packages": [
        {
            "name": "old-package",
            "ecosystem": "npm",
            "risk_level": "critical",
            "last_update": "2021-03-15",
            "days_inactive": 1037,
            "deprecated": true,
            "deprecation_message": "Use new-package instead",
            "alternatives": ["new-package", "better-package"],
            "affected_files": ["package.json"]
        }
    ],
    "summary": {
        "total_dependencies": 150,
        "abandoned_critical": 2,
        "abandoned_warning": 5,
        "healthy": 143
    }
}
```

## CI/CD Integration

```yaml
# GitHub Actions workflow
name: Abandoned Package Check

on:
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday
  pull_request:
    paths:
      - 'package.json'
      - 'requirements.txt'

jobs:
  check-abandoned:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check for abandoned packages
        run: |
          ./scripts/abandoned-pkg-scanner.sh > report.json

      - name: Fail on critical findings
        run: |
          CRITICAL=$(jq '.abandoned_packages | map(select(.risk_level == "critical")) | length' report.json)
          if [ "$CRITICAL" -gt 0 ]; then
            echo "Found $CRITICAL critically abandoned packages"
            jq '.abandoned_packages | map(select(.risk_level == "critical"))' report.json
            exit 1
          fi
```

## References

- [OpenSSF Scorecard](https://github.com/ossf/scorecard)
- [deps.dev](https://deps.dev/)
- [npm deprecation policy](https://docs.npmjs.com/deprecating-and-undeprecating-packages-or-package-versions)
- [PyPI classifiers](https://pypi.org/classifiers/)
- [GitHub Archive Policy](https://docs.github.com/en/repositories/archiving-a-github-repository)
