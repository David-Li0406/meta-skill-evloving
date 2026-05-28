# Session Registry Format

Schema documentation for `.session-chain-cache.json`.

## Location

```
~/.claude/projects/{encoded-path}/.session-chain-cache.json
```

Path encoding: `/Users/terryli/foo` → `-Users-terryli-foo`

## Schema

```json
{
  "version": 1,
  "currentSessionId": "c1c1c149-1abe-45f3-8572-fd77aa046232",
  "chain": [
    {
      "sessionId": "c1c1c149-1abe-45f3-8572-fd77aa046232",
      "shortId": "c1c1c149",
      "timestamp": "2026-01-15T21:30:00.000Z"
    }
  ],
  "updatedAt": 1768042226189,
  "_managedBy": "session-registry-plugin@1.0.0",
  "_userExtensions": {
    "repoHash": "a1b2c3d4e5f6",
    "repoName": "cc-skills",
    "gitBranch": "main",
    "model": "opus-4",
    "costUsd": 0.42
  }
}
```

## Field Reference

| Field               | Type   | Description               |
| ------------------- | ------ | ------------------------- |
| `version`           | number | Schema version (always 1) |
| `currentSessionId`  | string | Current session UUID      |
| `chain`             | array  | Session history (max 50)  |
| `chain[].sessionId` | string | Full session UUID         |
| `chain[].shortId`   | string | First 8 chars of UUID     |
| `chain[].timestamp` | string | ISO 8601 timestamp        |
| `updatedAt`         | number | Unix timestamp (ms)       |
| `_managedBy`        | string | Provenance marker         |
| `_userExtensions`   | object | Plugin metadata           |

## User Extensions

| Field       | Type   | Description                          |
| ----------- | ------ | ------------------------------------ |
| `repoHash`  | string | SHA256[cwd](0:12) for privacy        |
| `repoName`  | string | Repository name from git or basename |
| `gitBranch` | string | Current git branch                   |
| `model`     | string | Claude model name                    |
| `costUsd`   | number | Session cost in USD                  |

## Forward Compatibility

Fields prefixed with `_` (underscore) follow JSON-LD convention: "ignore if unknown".

- `_managedBy`: Identifies our plugin as the writer
- `_userExtensions`: All custom fields grouped here

If Claude Code resumes native writes, it will likely remove or ignore these fields. Our plugin detects this by checking if `_managedBy` is missing or changed.

## Security

- File permissions: `600` (owner read/write only)
- `repoHash` instead of full path prevents PII in registry
- Symlink check before write prevents symlink attacks
