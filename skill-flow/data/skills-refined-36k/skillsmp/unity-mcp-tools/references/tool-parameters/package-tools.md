# Package Tools Parameters

## package-list

Lists all installed packages. No parameters.

**Returns:** Array of package info with name, version, source.

## package-add

Installs a package from registry, Git, or local path.

| Parameter   | Type   | Required | Description                            |
| ----------- | ------ | -------- | -------------------------------------- |
| `packageId` | string | Yes      | Package identifier (see formats below) |

**Package ID Formats:**

- **Registry**: `com.unity.textmeshpro` (latest compatible)
- **With version**: `com.unity.textmeshpro@3.0.6`
- **Git URL**: `https://github.com/user/repo.git`
- **Git with tag**: `https://github.com/user/repo.git#v1.0.0`
- **Local path**: `file:../MyPackage`

**Examples:**

```json
// Install from Unity Registry
{ "packageId": "com.unity.inputsystem" }

// Install specific version
{ "packageId": "com.unity.inputsystem@1.7.0" }

// Install from Git
{ "packageId": "https://github.com/IvanMurzak/Unity-MCP.git" }

// Install from local
{ "packageId": "file:../../packages/my-package" }
```

**Notes:**

- Modifies `manifest.json`
- May trigger domain reload
- Returns `[Processing]` while installing
- Completion notification sent after reload

## package-remove

Removes an installed package.

| Parameter   | Type   | Required | Description            |
| ----------- | ------ | -------- | ---------------------- |
| `packageId` | string | Yes      | Package name to remove |

**Example:**

```json
{ "packageId": "com.unity.textmeshpro" }
```

## package-search

Searches Unity Package Registry.

| Parameter    | Type   | Required | Default | Description  |
| ------------ | ------ | -------- | ------- | ------------ |
| `searchText` | string | No       | null    | Search query |
| `maxResults` | int    | No       | 20      | Max results  |

**Example:**

```json
{
  "searchText": "input",
  "maxResults": 10
}
```

**Returns:** Matching packages with name, version, description.
