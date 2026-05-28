# Version Normalization Guide

## Overview

Version normalization is critical for **engineering reliability** - ensuring consistent, reproducible builds and accurate dependency resolution across diverse development environments. It also improves vulnerability matching accuracy by standardizing version strings.

## Why Reliability Matters

Version normalization supports standardized engineering environments by:
- Ensuring consistent dependency resolution across dev, staging, and production
- Enabling reproducible builds regardless of which developer or CI system runs them
- Providing accurate vulnerability matching through normalized version comparison
- Supporting standardized container images (see: gold-images-guide.md) with predictable dependency versions

## The Problem

SBOM tools and build systems often fail because:
- Version strings differ between ecosystems (npm vs PyPI vs Maven)
- Pre-release versions have inconsistent formats
- Local version segments are handled differently
- Build metadata may or may not be included
- Same logical version resolves differently across environments

## Ecosystem-Specific Normalization Rules

### PyPI (Python) - PEP 440

```python
# Normalization rules per PEP 503/440
# 1. Lowercase everything
# 2. Replace _ and - with .
# 3. Remove leading zeros in numeric segments
# 4. Normalize pre-release tags

# Examples:
"1.0.0-alpha1"  -> "1.0.0a1"
"1.0.0_beta.2"  -> "1.0.0b2"
"1.0.0.RC1"     -> "1.0.0rc1"
"01.02.03"      -> "1.2.3"

# Local versions (ignored for comparison)
"1.0.0+local"   -> "1.0.0" (for matching)
```

### npm (Node.js) - SemVer

```javascript
// npm follows semver spec with extensions
// 1. Numeric-only versions padded to 3 segments
// 2. Pre-release tags after hyphen
// 3. Build metadata after + (ignored for precedence)

// Examples:
"1"           -> "1.0.0"
"1.2"         -> "1.2.0"
"v1.2.3"      -> "1.2.3"
"1.2.3-alpha" -> "1.2.3-alpha"
"1.2.3+build" -> "1.2.3" (for comparison)
```

### Maven (Java)

```xml
<!-- Maven versioning is complex -->
<!-- 1. Qualifiers: alpha < beta < milestone < rc < snapshot < final < ga -->
<!-- 2. Missing qualifier equals "release" -->
<!-- 3. Numeric segments compared numerically -->

<!-- Examples: -->
"1.0-alpha"    < "1.0-beta" < "1.0-rc1" < "1.0" < "1.0-sp1"
"1.0.0"        = "1.0" (trailing zeros ignored)
"1.0-SNAPSHOT" < "1.0" (snapshot is pre-release)
```

### NuGet (.NET)

```csharp
// NuGet uses SemVer 2.0 with extensions
// 1. Fourth segment for revision (legacy)
// 2. Pre-release identifiers are case-insensitive
// 3. Build metadata is ignored

// Examples:
"1.0.0.0"       -> "1.0.0" (fourth segment often dropped)
"1.0.0-Alpha"   = "1.0.0-alpha"
"1.0.0-alpha.1" < "1.0.0-alpha.2"
```

### Go Modules

```go
// Go uses pseudo-versions for non-tagged commits
// Format: vX.Y.Z-yyyymmddhhmmss-abcdefabcdef

// Canonical versions:
"v1.2.3"
"v1.2.3-pre.0.20210901120000-abcdef123456" // pseudo-version

// Incompatible versions (major version in path):
"v2.0.0" -> module path includes /v2
```

### RubyGems

```ruby
# Ruby uses relaxed versioning
# 1. Any number of numeric segments
# 2. Pre-release indicated by letters

# Examples:
"1.0.0.alpha"   < "1.0.0"
"1.0.0.pre.1"   < "1.0.0"
"1.0.0.1"       > "1.0.0"  # revision
```

## Implementation Patterns

### Normalizer Function

```bash
normalize_version() {
    local version="$1"
    local ecosystem="$2"

    case "$ecosystem" in
        npm|node)
            # Remove 'v' prefix, pad to semver
            echo "$version" | sed 's/^v//' | awk -F. '{
                printf "%d.%d.%d", $1+0, ($2=="" ? 0 : $2+0), ($3=="" ? 0 : $3+0)
            }'
            ;;
        pypi|python)
            # Lowercase, replace separators, normalize pre-release
            echo "$version" | tr '[:upper:]' '[:lower:]' | \
                sed 's/[_-]/./g' | \
                sed 's/\.alpha/a/g; s/\.beta/b/g; s/\.rc/rc/g' | \
                sed 's/^0*//'
            ;;
        maven|java)
            # Lowercase qualifiers, handle SNAPSHOT
            echo "$version" | tr '[:upper:]' '[:lower:]'
            ;;
        nuget|dotnet)
            # Remove fourth segment if zero, lowercase
            echo "$version" | sed 's/\.0$//' | tr '[:upper:]' '[:lower:]'
            ;;
        *)
            echo "$version"
            ;;
    esac
}
```

### Version Comparison

```bash
compare_semver() {
    local v1="$1"
    local v2="$2"

    # Split into components
    IFS='.' read -ra V1 <<< "${v1%%[-+]*}"
    IFS='.' read -ra V2 <<< "${v2%%[-+]*}"

    # Compare numeric segments
    for i in 0 1 2; do
        local n1="${V1[$i]:-0}"
        local n2="${V2[$i]:-0}"
        if (( n1 > n2 )); then echo "1"; return; fi
        if (( n1 < n2 )); then echo "-1"; return; fi
    done

    # Compare pre-release (presence means lower)
    local pre1="${v1#*-}"
    local pre2="${v2#*-}"
    [[ "$pre1" == "$v1" ]] && pre1=""
    [[ "$pre2" == "$v2" ]] && pre2=""

    if [[ -z "$pre1" && -n "$pre2" ]]; then echo "1"; return; fi
    if [[ -n "$pre1" && -z "$pre2" ]]; then echo "-1"; return; fi

    echo "0"
}
```

## deps.dev API for Version Intelligence

deps.dev provides normalized version data:

```bash
# Get version info
curl -s "https://api.deps.dev/v3alpha/systems/npm/packages/lodash/versions/4.17.21" | \
    jq '{
        version: .version,
        publishedAt: .publishedAt,
        isDefault: .isDefault,
        links: .links
    }'

# Get all versions for ordering
curl -s "https://api.deps.dev/v3alpha/systems/npm/packages/lodash" | \
    jq '.versions | map(.version)'
```

## Vulnerability Matching Best Practices

1. **Always normalize before comparison**
   - Store both original and normalized versions
   - Use normalized for matching, original for display

2. **Handle version ranges correctly**
   - `>=1.0.0, <2.0.0` needs proper range parsing
   - Consider using ecosystem-specific range parsers

3. **Account for ecosystem quirks**
   - Some ecosystems allow non-semver versions
   - Historic packages may have inconsistent versioning

4. **Use authoritative sources**
   - deps.dev provides canonical version ordering
   - OSV.dev uses ecosystem-specific version comparison

## Common Pitfalls

| Issue | Example | Solution |
|-------|---------|----------|
| Leading zeros | `01.02.03` vs `1.2.3` | Strip leading zeros |
| Mixed separators | `1_0_0` vs `1.0.0` | Normalize to dots |
| Case sensitivity | `Alpha` vs `alpha` | Lowercase all |
| Build metadata | `1.0.0+build123` | Strip for comparison |
| Fourth segment | `1.0.0.0` | Handle ecosystem-specifically |

## Integration with SBOM

When generating SBOMs:

```json
{
  "components": [{
    "name": "lodash",
    "version": "4.17.21",
    "properties": [{
      "name": "normalized_version",
      "value": "4.17.21"
    }, {
      "name": "version_scheme",
      "value": "semver"
    }]
  }]
}
```

## References

- [PEP 440 - Version Identification](https://peps.python.org/pep-0440/)
- [SemVer 2.0 Specification](https://semver.org/)
- [Maven Version Order](https://maven.apache.org/pom.html#version-order-specification)
- [NuGet Versioning](https://docs.microsoft.com/en-us/nuget/concepts/package-versioning)
- [deps.dev API](https://docs.deps.dev/api/v3alpha/)
