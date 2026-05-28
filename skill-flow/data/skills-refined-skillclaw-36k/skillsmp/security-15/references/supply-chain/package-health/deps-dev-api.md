<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# deps.dev API v3alpha Reference

Comprehensive reference for the deps.dev API - Google's open-source dependency intelligence service.

## Overview

**Base URL**: `https://api.deps.dev`
**Version**: v3alpha
**Authentication**: None required (public API)
**Rate Limits**: Not publicly documented (be respectful)
**Format**: JSON

## Core Concepts

### Package Systems

Supported ecosystems:
- `npm` - Node.js packages
- `pypi` - Python packages
- `go` - Go modules
- `maven` - Java/Maven packages
- `cargo` - Rust crates
- `nuget` - .NET packages
- `rubygems` - Ruby gems

### Package URLs (purl)

Format: `pkg:{system}/{namespace}/{name}@{version}`

Examples:
```
pkg:npm/express@4.18.2
pkg:pypi/requests@2.28.0
pkg:maven/org.springframework.boot/spring-boot@3.0.0
pkg:cargo/serde@1.0.0
```

## API Endpoints

### 1. Get Package Information

**Endpoint**: `GET /v3alpha/systems/{system}/packages/{package}`

Retrieve overall package information including all versions.

**Parameters**:
- `system` (path): Package system (npm, pypi, go, etc.)
- `package` (path): Package name (URL-encoded if contains special chars)

**Example Request**:
```bash
curl https://api.deps.dev/v3alpha/systems/npm/packages/express
```

**Response Schema**:
```json
{
  "packageKey": {
    "system": "NPM",
    "name": "express"
  },
  "versions": [
    {
      "versionKey": {
        "system": "NPM",
        "name": "express",
        "version": "4.18.2"
      },
      "publishedAt": "2022-10-08T22:14:16Z",
      "isDefault": true,
      "licenses": ["MIT"],
      "links": {
        "homepage": "http://expressjs.com/",
        "issues": "https://github.com/expressjs/express/issues",
        "source": "https://github.com/expressjs/express"
      }
    }
  ]
}
```

### 2. Get Version Details

**Endpoint**: `GET /v3alpha/systems/{system}/packages/{package}/versions/{version}`

Detailed information for a specific package version.

**Parameters**:
- `system` (path): Package system
- `package` (path): Package name
- `version` (path): Version string

**Example Request**:
```bash
curl https://api.deps.dev/v3alpha/systems/npm/packages/express/versions/4.18.2
```

**Response Schema**:
```json
{
  "versionKey": {
    "system": "NPM",
    "name": "express",
    "version": "4.18.2"
  },
  "publishedAt": "2022-10-08T22:14:16Z",
  "isDefault": true,
  "licenses": ["MIT"],
  "advisoryKeys": [],
  "links": {
    "homepage": "http://expressjs.com/",
    "issues": "https://github.com/expressjs/express/issues",
    "source": "https://github.com/expressjs/express"
  },
  "slsaProvenances": [
    {
      "sourceRepository": "https://github.com/expressjs/express",
      "verified": true
    }
  ],
  "projects": [
    {
      "projectKey": {
        "id": "github.com/expressjs/express"
      },
      "scorecard": {
        "date": "2024-11-01",
        "score": 7.2,
        "checks": [
          {
            "name": "Code-Review",
            "score": 10,
            "reason": "All changes are code reviewed",
            "details": ["..."]
          }
        ]
      }
    }
  ],
  "dependencies": [
    {
      "versionKey": {
        "system": "NPM",
        "name": "body-parser",
        "version": "1.20.1"
      },
      "relation": "DIRECT"
    }
  ]
}
```

### 3. Get Dependencies

**Endpoint**: `GET /v3alpha/systems/{system}/packages/{package}/versions/{version}:dependencies`

Resolved dependency graph for a version.

**Parameters**:
- `system`, `package`, `version`: As above

**Response**: Complete dependency tree with transitive dependencies.

### 4. Get Advisory Information

**Endpoint**: `GET /v3alpha/advisories/{advisoryId}`

Security advisory details.

**Parameters**:
- `advisoryId` (path): Advisory identifier (e.g., `GHSA-xxxx-yyyy-zzzz`)

**Example Request**:
```bash
curl https://api.deps.dev/v3alpha/advisories/GHSA-xxxx-yyyy-zzzz
```

**Response Schema**:
```json
{
  "advisoryKey": {
    "id": "GHSA-xxxx-yyyy-zzzz"
  },
  "url": "https://github.com/advisories/GHSA-xxxx-yyyy-zzzz",
  "title": "Vulnerability Title",
  "aliases": ["CVE-2023-12345"],
  "cvss3Score": 7.5,
  "cvss3Vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N",
  "affectedPackages": [
    {
      "versionKey": {
        "system": "NPM",
        "name": "vulnerable-package",
        "version": "1.0.0"
      }
    }
  ]
}
```

### 5. Get Project Information

**Endpoint**: `GET /v3alpha/projects/{projectKey}`

Source repository/project information.

**Parameters**:
- `projectKey` (path): Project identifier (URL-encoded, e.g., `github.com/owner/repo`)

**Example Request**:
```bash
curl https://api.deps.dev/v3alpha/projects/github.com%2Fexpressjs%2Fexpress
```

**Response**: Project metadata, scorecard, and health signals.

## OpenSSF Scorecard Integration

### Scorecard Object Structure

```json
{
  "scorecard": {
    "date": "2024-11-01T00:00:00Z",
    "repository": "github.com/expressjs/express",
    "score": 7.2,
    "checks": [
      {
        "name": "Binary-Artifacts",
        "score": 10,
        "reason": "No binary artifacts found",
        "details": ["..."]
      },
      {
        "name": "Branch-Protection",
        "score": 5,
        "reason": "Branch protection not maximal",
        "details": [
          "Warn: Status checks are not required",
          "Warn: Approving review not required"
        ]
      }
    ]
  }
}
```

### Available Scorecard Checks

1. **Binary-Artifacts** (0-10)
   - Checks for binary artifacts in source repository
   - Score 10: No binaries found
   - Score 0: Binary artifacts present

2. **Branch-Protection** (0-10)
   - Evaluates branch protection rules
   - Checks for required reviews, status checks
   - Score based on protection strength

3. **CI-Tests** (0-10)
   - Presence of continuous integration
   - Tests run on all commits
   - Score based on CI coverage

4. **CII-Best-Practices** (0-10)
   - OpenSSF Best Practices badge level
   - 10: Gold badge
   - 5: Silver badge
   - 2: Passing badge

5. **Code-Review** (0-10)
   - Code review requirements
   - Score 10: All changes reviewed
   - Considers PR review settings

6. **Contributors** (0-10)
   - Number of active contributors
   - Score based on contributor diversity

7. **Dangerous-Workflow** (0-10)
   - Checks for dangerous workflow patterns
   - Untrusted code execution
   - Score 10: No dangerous patterns

8. **Dependency-Update-Tool** (0-10)
   - Automated dependency updates
   - Renovate, Dependabot, etc.
   - Score 10: Tool configured

9. **Fuzzing** (0-10)
   - Fuzz testing integration
   - OSS-Fuzz, ClusterFuzz, etc.
   - Score 10: Fuzzing enabled

10. **License** (0-10)
    - Valid license file present
    - Recognized license format
    - Score 10: Valid license

11. **Maintained** (0-10)
    - Active maintenance signals
    - Recent commits, issue responses
    - Score based on activity

12. **Pinned-Dependencies** (0-10)
    - Dependencies pinned to specific versions
    - Checks CI/CD configs
    - Score 10: All pinned

13. **SAST** (0-10)
    - Static analysis security testing
    - CodeQL, Semgrep, etc.
    - Score 10: SAST integrated

14. **Security-Policy** (0-10)
    - SECURITY.md file present
    - Vulnerability reporting process
    - Score 10: Policy exists

15. **Signed-Releases** (0-10)
    - Release artifacts signed
    - Signature verification possible
    - Score 10: Releases signed

16. **Token-Permissions** (0-10)
    - GitHub Actions token permissions
    - Minimal permission principle
    - Score 10: Minimal permissions

17. **Vulnerabilities** (0-10)
    - Known vulnerabilities in package
    - Score 10: No vulnerabilities
    - Lower scores for unfixed issues

## Usage Patterns

### Check Package Health

```bash
#!/bin/bash

get_package_health() {
    local system="$1"
    local package="$2"
    local version="$3"

    # Get version details with scorecard
    local data=$(curl -s "https://api.deps.dev/v3alpha/systems/${system}/packages/${package}/versions/${version}")

    # Extract overall score
    local score=$(echo "$data" | jq -r '.projects[0].scorecard.score // 0')

    # Extract key metrics
    local maintained=$(echo "$data" | jq -r '.projects[0].scorecard.checks[] | select(.name=="Maintained") | .score')
    local vulnerabilities=$(echo "$data" | jq -r '.projects[0].scorecard.checks[] | select(.name=="Vulnerabilities") | .score')

    echo "Package: ${package}@${version}"
    echo "Overall Score: ${score}/10"
    echo "Maintained: ${maintained}/10"
    echo "Vulnerabilities: ${vulnerabilities}/10"
}

# Usage
get_package_health "npm" "express" "4.18.2"
```

### Find Deprecated Packages

```bash
check_deprecation() {
    local system="$1"
    local package="$2"

    local data=$(curl -s "https://api.deps.dev/v3alpha/systems/${system}/packages/${package}")

    # Check for deprecation in latest version
    local deprecated=$(echo "$data" | jq -r '.versions[] | select(.isDefault==true) | .deprecationReason // "Not deprecated"')

    if [[ "$deprecated" != "Not deprecated" ]]; then
        echo "⚠ ${package} is DEPRECATED"
        echo "Reason: $deprecated"
    fi
}
```

### Analyze Dependencies

```bash
analyze_dependencies() {
    local system="$1"
    local package="$2"
    local version="$3"

    local data=$(curl -s "https://api.deps.dev/v3alpha/systems/${system}/packages/${package}/versions/${version}")

    # Count direct vs transitive
    local direct=$(echo "$data" | jq '[.dependencies[] | select(.relation=="DIRECT")] | length')
    local transitive=$(echo "$data" | jq '[.dependencies[] | select(.relation=="INDIRECT")] | length')

    echo "Dependencies:"
    echo "  Direct: $direct"
    echo "  Transitive: $transitive"
    echo "  Total: $((direct + transitive))"
}
```

## Response Fields Reference

### VersionKey
```json
{
  "system": "NPM",
  "name": "package-name",
  "version": "1.0.0"
}
```

### Links
```json
{
  "homepage": "https://example.com",
  "issues": "https://github.com/owner/repo/issues",
  "source": "https://github.com/owner/repo",
  "documentation": "https://docs.example.com"
}
```

### Dependency Relation Types
- `DIRECT`: Direct dependency
- `INDIRECT`: Transitive dependency
- `DEV`: Development dependency

### SLSA Provenance
```json
{
  "sourceRepository": "https://github.com/owner/repo",
  "commit": "abc123...",
  "verified": true,
  "level": "SLSA_BUILD_LEVEL_3"
}
```

## Best Practices

### Rate Limiting
- Implement exponential backoff
- Cache responses when possible
- Batch requests efficiently
- Respect 429 responses

### Error Handling
```bash
make_api_request() {
    local url="$1"
    local max_retries=3
    local retry=0

    while [ $retry -lt $max_retries ]; do
        local response=$(curl -s -w "\n%{http_code}" "$url")
        local body=$(echo "$response" | head -n -1)
        local status=$(echo "$response" | tail -n 1)

        if [ "$status" = "200" ]; then
            echo "$body"
            return 0
        elif [ "$status" = "429" ]; then
            echo "Rate limited, waiting..." >&2
            sleep $((2 ** retry))
            ((retry++))
        else
            echo "Error: HTTP $status" >&2
            return 1
        fi
    done

    return 1
}
```

### Data Caching
- Cache scorecard data (updates weekly)
- Cache package metadata (changes infrequently)
- Use ETags when available
- Implement local cache with expiry

## Limitations

### Known Limitations
- Not all packages have scorecard data
- Scorecard updates weekly (may be stale)
- Some ecosystems have limited coverage
- Private packages not accessible
- Historical data not available via API

### Fallback Strategies
- Use npm registry API for npm-specific data
- Query GitHub API directly for missing data
- Implement local scorecard calculation
- Use OSV.dev for vulnerability data

## Related APIs

### npm Registry API
```
GET https://registry.npmjs.org/{package}
GET https://registry.npmjs.org/{package}/{version}
```

### PyPI API
```
GET https://pypi.org/pypi/{package}/json
GET https://pypi.org/pypi/{package}/{version}/json
```

### GitHub API
```
GET https://api.github.com/repos/{owner}/{repo}
GET https://api.github.com/repos/{owner}/{repo}/commits
```

## Example Integration

Complete example of deps.dev integration for package health:

```bash
#!/bin/bash

analyze_package_health() {
    local system="$1"
    local package="$2"
    local version="$3"

    echo "Analyzing ${package}@${version}..."

    # Get full package data
    local data=$(curl -s "https://api.deps.dev/v3alpha/systems/${system}/packages/${package}/versions/${version}")

    # Extract scorecard
    local scorecard=$(echo "$data" | jq '.projects[0].scorecard')
    local overall_score=$(echo "$scorecard" | jq -r '.score // 0')

    echo ""
    echo "OpenSSF Scorecard: ${overall_score}/10"
    echo ""

    # Show critical checks
    echo "$scorecard" | jq -r '.checks[] |
        select(.score < 5) |
        "⚠ \(.name): \(.score)/10 - \(.reason)"'

    # Check for advisories
    local advisories=$(echo "$data" | jq -r '.advisoryKeys | length')
    if [ "$advisories" -gt 0 ]; then
        echo ""
        echo "⚠ ${advisories} security advisories found"
    fi

    # Dependency count
    local deps=$(echo "$data" | jq '.dependencies | length')
    echo ""
    echo "Dependencies: $deps"
}
```

## References

- Official Documentation: https://docs.deps.dev/
- OpenSSF Scorecard: https://github.com/ossf/scorecard
- API Status: https://status.deps.dev/
- Community: https://github.com/google/deps.dev
