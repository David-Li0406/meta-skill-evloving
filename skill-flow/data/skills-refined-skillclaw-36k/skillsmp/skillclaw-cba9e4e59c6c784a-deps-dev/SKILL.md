---
name: deps-dev
description: Use this skill when checking package versions, updating dependencies, adding new packages to a project, or when the user asks about the current version of a library using the deps.dev API.
---

# Latest Package Version Lookup

Query the deps.dev API to get the latest stable version of open source packages.

## Supported Ecosystems

| Ecosystem | System ID | Example Package                    |
| --------- | --------- | ---------------------------------- |
| npm       | `NPM`     | `express`, `@types/node`           |
| PyPI      | `PYPI`    | `requests`, `django`               |
| Go        | `GO`      | `github.com/gin-gonic/gin`         |
| Cargo     | `CARGO`   | `serde`, `tokio`                   |
| Maven     | `MAVEN`   | `org.springframework:spring-core`  |
| NuGet     | `NUGET`   | `Newtonsoft.Json`                  |
| RubyGems  | `RUBYGEMS`| `rails`, `rake`                    |

## API Quick Reference

| Endpoint | Purpose |
| -------- | ------- |
| `GET /v3/systems/{system}/packages/{name}` | Get package info with all versions |
| `GET /v3/systems/{system}/packages/{name}/versions/{version}` | Get specific version details |

## Workflow

1. **Identify the ecosystem** from context:
   - `package.json` or `node_modules` → NPM
   - `requirements.txt`, `pyproject.toml`, `setup.py` → PYPI
   - `go.mod`, `go.sum` → GO
   - `Cargo.toml` → CARGO
   - `pom.xml`, `build.gradle` → MAVEN
   - `*.csproj`, `packages.config` → NUGET
   - `Gemfile` → RUBYGEMS
   - If unclear, ask the user

2. **Query the API** with curl (URL-encode special characters) or run the get-versions script:
   ```bash
   # Using curl
   curl -s "https://api.deps.dev/v3/systems/NPM/packages/express"

   # Using the script
   SCRIPT=scripts/get-versions.py
   python3 $SCRIPT <system> <pkg1> [pkg2] ...
   ```

3. **Find the default version** - look for `"isDefault": true` in the versions array.

## Response Structure

### GetPackage Response

```json
{
  "packageKey": {
    "system": "NPM",
    "name": "express"
  },
  ...
}
```

### Script Output Format

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
    },
    ...
  ]
}
```

**Error response:**

```json
{
  "system": "npm",
  "packages": [
    {
      "package": "nonexistent-pkg",
      "error": "HTTP 404: Not Found"
    }
  ]
}
```

## Error Handling

- **HTTP 404**: Package not found - check spelling and try again.