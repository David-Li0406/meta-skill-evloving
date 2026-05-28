---
name: deps-dev
description: Look up the latest version of any package using deps.dev API. Use this skill when checking package versions, updating dependencies, adding new packages to a project, or when the user asks about the current version of a library.
---

# Latest Package Version Lookup

Query the deps.dev API to get the latest stable version of open source packages.

## API Quick Reference

| Endpoint | Purpose |
| -------- | ------- |
| `GET /v3/systems/{system}/packages/{name}` | Get package info with all versions |
| `GET /v3/systems/{system}/packages/{name}/versions/{version}` | Get specific version details |

## Supported Ecosystems

| Ecosystem | System ID | Example Package |
| --------- | --------- | --------------- |
| npm | `NPM` | `express`, `@types/node` |
| PyPI | `PYPI` | `requests`, `django` |
| Go | `GO` | `github.com/gin-gonic/gin` |
| Cargo | `CARGO` | `serde`, `tokio` |
| Maven | `MAVEN` | `org.apache.logging.log4j:log4j-core` |
| NuGet | `NUGET` | `Newtonsoft.Json` |
| RubyGems | `RUBYGEMS` | `rails`, `rake` |

## Usage

### Get Package Info (includes all versions)

```bash
# npm package
curl -s "https://api.deps.dev/v3/systems/NPM/packages/express"

# Scoped npm package (URL-encode @ and /)
curl -s "https://api.deps.dev/v3/systems/NPM/packages/%40types%2Fnode"

# PyPI package
curl -s "https://api.deps.dev/v3/systems/PYPI/packages/requests"

# Go module (URL-encode /)
curl -s "https://api.deps.dev/v3/systems/GO/packages/github.com%2Fgin-gonic%2Fgin"

# Cargo crate
curl -s "https://api.deps.dev/v3/systems/CARGO/packages/serde"

# Maven artifact (use : separator, URL-encode)
curl -s "https://api.deps.dev/v3/systems/MAVEN/packages/org.springframework%3Aspring-core"
```

### Get Specific Version Details

```bash
curl -s "https://api.deps.dev/v3/systems/NPM/packages/express/versions/5.0.0"
```

## Workflow

Think step-by-step:

1. **Identify the ecosystem** from context:
   - `package.json` or `node_modules` → NPM
   - `requirements.txt`, `pyproject.toml`, `setup.py` → PYPI
   - `go.mod`, `go.sum` → GO
   - `Cargo.toml` → CARGO
   - `pom.xml`, `build.gradle` → MAVEN
   - `*.csproj`, `packages.config` → NUGET
   - `Gemfile` → RUBYGEMS
   - If unclear, ask the user

2. **Query the API** with curl (URL-encode special characters)

3. **Find the default version** - look for `"isDefault": true` in the versions array

## Response Structure

### GetPackage Response

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
        "version": "5.0.0"
      },
      "publishedAt": "2024-09-10T04:40:34Z",
      "isDefault": true
    }
  ]
}
```

The version with `"isDefault": true` is the latest stable version.

### GetVersion Response

```json
{
  "versionKey": {
    "system": "NPM",
    "name": "express",
    "version": "5.0.0"
  },
  "publishedAt": "2024-09-10T04:40:34Z",
  "isDefault": true,
  "licenses": ["MIT"],
  "advisoryKeys": []
}
```

## URL Encoding

Special characters must be percent-encoded:

| Character | Encoded |
| --------- | ------- |
| `@` | `%40` |
| `/` | `%2F` |
| `:` | `%3A` |

### Encode with Command Line

```bash
# Using printf and sed
printf '%s' "@types/node" | sed 's/@/%40/g; s|/|%2F|g; s/:/%3A/g'
# Output: %40types%2Fnode

# Using jq (if available)
jq -rn --arg s "@types/node" '$s | @uri'
# Output: %40types%2Fnode

# Using python
python3 -c "import urllib.parse; print(urllib.parse.quote('github.com/gin-gonic/gin', safe=''))"
# Output: github.com%2Fgin-gonic%2Fgin
```

### Examples

- `@types/node` → `%40types%2Fnode`
- `github.com/gin-gonic/gin` → `github.com%2Fgin-gonic%2Fgin`
- `org.springframework:spring-core` → `org.springframework%3Aspring-core`

## Error Handling

- **HTTP 404**: Package not found - check spelling and ecosystem
- **Empty versions**: Package exists but has no published versions
- **Network error**: deps.dev API may be temporarily unavailable

## Rules

- URL-encode package names with special characters (`@`, `/`, `:`)
- The default version (`isDefault: true`) is typically the latest stable release
- Use `advisoryKeys` to check for known security vulnerabilities
- Use `licenses` field to verify package licensing
