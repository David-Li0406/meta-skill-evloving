---
name: package-version-lookup
description: Use this skill when checking the latest version of any package across various ecosystems using the deps.dev API.
---

# Latest Package Version Lookup

Query the deps.dev API to get the latest stable version of open source packages.

## Supported Ecosystems

| Ecosystem | System ID | Example Package                    |
| --------- | --------- | ---------------------------------- |
| npm       | `npm`     | `express`, `@types/node`           |
| PyPI      | `pypi`    | `requests`, `django`               |
| Go        | `go`      | `github.com/gin-gonic/gin`         |
| Cargo     | `cargo`   | `serde`, `tokio`                   |
| Maven     | `maven`   | `org.springframework:spring-core`  |
| NuGet     | `nuget`   | `Newtonsoft.Json`                  |

## Workflow

1. **Identify the ecosystem** from context:
   - `package.json` or `node_modules` → npm
   - `requirements.txt`, `pyproject.toml`, `setup.py` → pypi
   - `go.mod`, `go.sum` → go
   - `Cargo.toml` → cargo
   - `pom.xml`, `build.gradle` → maven
   - `*.csproj`, `packages.config` → nuget
   - If unclear, ask the user.

2. **Run the version lookup** using the appropriate method:

### Using Curl

To get package info (includes all versions):

```bash
curl -s "https://api.deps.dev/v3/systems/{system}/packages/{name}"
```

To get specific version details:

```bash
curl -s "https://api.deps.dev/v3/systems/{system}/packages/{name}/versions/{version}"
```

### Using Script

Run the get-versions script:

```bash
SCRIPT=scripts/get-versions.py
python3 $SCRIPT <system> <pkg1> [pkg2] ...
```

**Single package:**

```bash
python3 scripts/get-versions.py npm express
```

**Multiple packages:**

```bash
python3 scripts/get-versions.py npm express lodash @types/node
```

**Different ecosystems:**

```bash
python3 scripts/get-versions.py pypi requests django flask
python3 scripts/get-versions.py go github.com/gin-gonic/gin
python3 scripts/get-versions.py maven org.springframework:spring-core
```

## Response Structure

### Curl Response

The response for getting package info will look like this:

```json
{
  "packageKey": {
    "system": "npm",
    "name": "express"
  },
  "versions": [
    {
      "versionKey": {
        "system": "npm",
        "name": "express",
        "version": "5.0.0"
      },
      "publishedAt": "2024-09-10T04:40:34Z",
      "isDefault": true
    }
  ]
}
```

### Script Output

The script outputs JSON with the following structure:

```json
{
  "system": "npm",
  "packages": [
    {
      "package": "express",
      "version": "5.0.0",
      "publishedAt": "2024-09-10T04:40:34Z",
      "isDeprecated": false
    }
  ]
}
```

## Error Handling

- **HTTP 404**: Package not found - check spelling and ecosystem.
- **Network error**: deps.dev API may be temporarily unavailable.
- **No default version**: The script returns the latest available version with a note.

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
```

## Rules

- Always use the script instead of manual curl commands.
- The script handles URL encoding automatically.
- Multiple packages are fetched in parallel for efficiency.
- Use `isDeprecated` field to warn users about deprecated packages.
- The default version (`isDefault: true`) is typically the latest stable release.
- Use `advisoryKeys` to check for known security vulnerabilities.
- Use `licenses` field to verify package licensing.