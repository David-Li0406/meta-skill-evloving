# Typosquatting and Malicious Package Detection

## Overview

Typosquatting is a supply chain attack where malicious actors publish packages with names similar to popular legitimate packages, hoping developers will accidentally install them.

## Attack Vectors

### 1. Typosquatting Variants

| Type | Example | Target |
|------|---------|--------|
| Character swap | `loadsh` | `lodash` |
| Missing character | `reqests` | `requests` |
| Extra character | `expresss` | `express` |
| Adjacent key | `requsets` | `requests` |
| Homoglyph | `ŀodash` (ŀ vs l) | `lodash` |
| Separator confusion | `python-dateutil` vs `python_dateutil` |

### 2. Combosquatting

Adding prefixes/suffixes to legitimate names:
- `lodash-utils`
- `express-helper`
- `react-native-maps-community` (legitimate) vs `react-native-maps-com`

### 3. Dependency Confusion

Publishing internal package names to public registries:
- Company uses `@company/utils` internally
- Attacker publishes `company-utils` to npm

## Detection Methods

### Levenshtein Distance

Calculate edit distance between package name and known popular packages:

```bash
# Levenshtein distance calculation
levenshtein() {
    local s1="$1"
    local s2="$2"
    local len1=${#s1}
    local len2=${#s2}

    # Use Python for reliable calculation
    python3 -c "
import sys
def lev(s1, s2):
    if len(s1) < len(s2):
        return lev(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            curr.append(min(prev[j+1]+1, curr[j]+1, prev[j]+(c1!=c2)))
        prev = curr
    return prev[-1]
print(lev('$s1', '$s2'))
"
}

# Check if package name is suspiciously similar
check_typosquat() {
    local pkg="$1"
    local popular_packages=("lodash" "express" "react" "axios" "moment" "request" "chalk" "debug")

    for popular in "${popular_packages[@]}"; do
        local distance=$(levenshtein "$pkg" "$popular")
        local threshold=$((${#popular} / 3))  # Allow ~33% difference

        if [[ $distance -gt 0 && $distance -le $threshold ]]; then
            echo "WARNING: '$pkg' is similar to popular package '$popular' (distance: $distance)"
            return 1
        fi
    done
    return 0
}
```

### Behavioral Analysis (Socket.dev Approach)

Red flags to detect in package code:

```bash
# Behavioral indicators of malicious packages
MALICIOUS_PATTERNS=(
    # Network exfiltration
    "net.createConnection"
    "dns.lookup.*base64"
    "fetch.*env"
    "axios.*process.env"

    # Process manipulation
    "child_process.*exec"
    "spawn.*sh.*-c"
    "eval(.*require"

    # File system access
    "readFileSync.*/etc/passwd"
    "readFileSync.*\.ssh"
    "readFileSync.*\.npmrc"

    # Environment variable theft
    "process.env.NPM_TOKEN"
    "process.env.AWS_"
    "JSON.stringify.*process.env"

    # Obfuscation indicators
    "\\x[0-9a-fA-F]{2}"  # Hex encoding
    "Buffer.from.*base64"
    "atob|btoa"
    "String.fromCharCode"

    # Install script abuse
    "postinstall.*curl"
    "preinstall.*wget"
)

analyze_package_behavior() {
    local pkg_dir="$1"

    for pattern in "${MALICIOUS_PATTERNS[@]}"; do
        if grep -rE "$pattern" "$pkg_dir" 2>/dev/null; then
            echo "SUSPICIOUS: Found pattern '$pattern'"
        fi
    done
}
```

### Package Metadata Analysis

```bash
check_package_metadata() {
    local pkg="$1"
    local registry_url="https://registry.npmjs.org/$pkg"

    local metadata=$(curl -s "$registry_url")

    # Check maintainer count
    local maintainers=$(echo "$metadata" | jq '.maintainers | length')
    if [[ "$maintainers" -lt 1 ]]; then
        echo "WARNING: No maintainers listed"
    fi

    # Check package age
    local created=$(echo "$metadata" | jq -r '.time.created')
    local age_days=$(( ($(date +%s) - $(date -d "$created" +%s)) / 86400 ))
    if [[ "$age_days" -lt 7 ]]; then
        echo "WARNING: Package is only $age_days days old"
    fi

    # Check download count vs dependencies
    local weekly_downloads=$(curl -s "https://api.npmjs.org/downloads/point/last-week/$pkg" | jq '.downloads')
    if [[ "$weekly_downloads" -lt 100 ]]; then
        echo "WARNING: Very low download count ($weekly_downloads/week)"
    fi

    # Check for install scripts
    local scripts=$(echo "$metadata" | jq '.versions | to_entries | .[-1].value.scripts // {}')
    if echo "$scripts" | grep -qE '"(pre|post)install"'; then
        echo "WARNING: Package has install scripts - review carefully"
    fi
}
```

## Tools and APIs

### 1. Socket.dev

Commercial service with comprehensive detection:
- 70+ security indicators
- Real-time package analysis
- CI/CD integration

```bash
# Socket CLI (if available)
socket npm info lodash
socket scan package.json
```

### 2. GuardDog (Open Source)

```bash
# Install
pip install guarddog

# Scan PyPI package
guarddog pypi scan requests

# Scan npm package
guarddog npm scan express

# Scan local requirements.txt
guarddog pypi verify requirements.txt
```

### 3. Stacklok Trusty

```bash
# Check package trust score
curl -s "https://api.trustypkg.dev/v1/npm/lodash" | jq '{
    score: .score,
    activity: .activity,
    provenance: .provenance
}'
```

### 4. deps.dev

```bash
# Get package advisories and health
curl -s "https://api.deps.dev/v3alpha/systems/npm/packages/lodash" | jq '{
    scorecardV2: .scorecardV2,
    links: .links
}'
```

## Recommended Detection Pipeline

```bash
#!/bin/bash

check_dependency() {
    local pkg="$1"
    local ecosystem="$2"
    local alerts=()

    # 1. Typosquatting check
    if ! check_typosquat "$pkg"; then
        alerts+=("TYPOSQUAT_RISK")
    fi

    # 2. Package age check
    local age=$(get_package_age "$pkg" "$ecosystem")
    if [[ "$age" -lt 30 ]]; then
        alerts+=("NEW_PACKAGE")
    fi

    # 3. Maintainer reputation
    local maintainer_score=$(get_maintainer_score "$pkg" "$ecosystem")
    if [[ "$maintainer_score" -lt 50 ]]; then
        alerts+=("LOW_REPUTATION")
    fi

    # 4. Install script check
    if has_install_scripts "$pkg" "$ecosystem"; then
        alerts+=("HAS_INSTALL_SCRIPTS")
    fi

    # 5. Known malicious check
    if is_known_malicious "$pkg" "$ecosystem"; then
        alerts+=("KNOWN_MALICIOUS")
    fi

    # Return alerts
    printf '%s\n' "${alerts[@]}"
}
```

## Popular Package Lists

Maintain lists of popular packages per ecosystem for comparison:

### npm Top 100

```
lodash, express, react, axios, moment, request, chalk, debug,
commander, async, uuid, underscore, bluebird, yargs, fs-extra,
glob, mkdirp, semver, rimraf, colors, body-parser, dotenv,
webpack, babel-core, typescript, jest, mocha, eslint, prettier,
rxjs, redux, vue, angular, jquery, d3, three, socket.io,
mongoose, sequelize, pg, mysql, redis, aws-sdk, googleapis,
...
```

### PyPI Top 100

```
requests, boto3, urllib3, setuptools, six, python-dateutil,
certifi, idna, chardet, pip, pyyaml, numpy, typing-extensions,
cryptography, packaging, botocore, s3transfer, jmespath,
cffi, pyparsing, attrs, importlib-metadata, colorama,
...
```

## Response Actions

When malicious package detected:

1. **Immediate**: Block installation in CI/CD
2. **Alert**: Notify security team
3. **Audit**: Check if already installed in any environments
4. **Remediate**: Remove and replace with legitimate package
5. **Report**: Report to registry (npm, PyPI, etc.)

## References

- [Socket.dev Security Blog](https://socket.dev/blog)
- [GuardDog GitHub](https://github.com/DataDog/guarddog)
- [Stacklok Trusty](https://www.trustypkg.dev/)
- [npm Security Advisories](https://www.npmjs.com/advisories)
- [PyPI Malware Reports](https://blog.phylum.io/)
