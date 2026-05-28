---
name: package-version-lookup
description: Use this skill when checking the latest version of packages across various ecosystems, updating dependencies, or adding new packages to a project.
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
   - For a single package:
     ```bash
     curl -s "https://api.deps.dev/v3/systems/<system>/packages/<package>"
     ```
   - For multiple packages, use the script:
     ```bash
     python3 scripts/get-versions.py <system> <pkg1> [pkg2] ...
     ```

3. **Report the results** from the JSON output.

## Response Structure

### Get Package Info Response

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

### Script Output Format

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
- **No default version**: The latest available version will be returned with a note.

## Rules

- URL-encode package names with special characters (`@`, `/`, `:`).
- Use the `isDeprecated` field to warn users about deprecated packages.
- The default version (`isDefault: true`) is typically the latest stable release.