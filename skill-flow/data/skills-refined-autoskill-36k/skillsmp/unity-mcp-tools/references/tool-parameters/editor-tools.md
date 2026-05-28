# Editor Tools Parameters

## editor-application-get-state

Gets current Unity Editor state. No parameters.

**Returns:**

- `isPlaying`: Whether in Play mode
- `isPaused`: Whether paused
- `isCompiling`: Whether scripts are compiling
- `platform`: Current build target

## editor-application-set-state

Controls Unity Editor Play mode.

| Parameter   | Type | Required | Default | Description            |
| ----------- | ---- | -------- | ------- | ---------------------- |
| `isPlaying` | bool | No       | false   | Start/stop Play mode   |
| `isPaused`  | bool | No       | false   | Pause/resume Play mode |

**Examples:**

```json
// Start Play mode
{ "isPlaying": true }

// Pause
{ "isPlaying": true, "isPaused": true }

// Stop Play mode
{ "isPlaying": false }
```

**Note:** Fails if project has compilation errors.

## console-get-logs

Retrieves Unity Console logs.

| Parameter           | Type    | Required | Default | Description                                    |
| ------------------- | ------- | -------- | ------- | ---------------------------------------------- |
| `maxEntries`        | int     | No       | 100     | Max entries (min: 1)                           |
| `logTypeFilter`     | LogType | No       | null    | Filter: Log, Warning, Error, Exception, Assert |
| `includeStackTrace` | bool    | No       | false   | Include stack traces                           |
| `lastMinutes`       | int     | No       | 0       | Only logs from last N minutes (0 = all)        |

**LogType Values:** `Log`, `Warning`, `Error`, `Exception`, `Assert`

**Example:**

```json
{
  "maxEntries": 50,
  "logTypeFilter": "Error",
  "includeStackTrace": true,
  "lastMinutes": 5
}
```

## editor-selection-get

Gets currently selected objects in Editor. No parameters.

**Returns:** Array of selected object references.

## editor-selection-set

Sets Editor selection.

| Parameter        | Type            | Required | Description       |
| ---------------- | --------------- | -------- | ----------------- |
| `gameObjectRefs` | GameObjectRef[] | Yes      | Objects to select |

**Example:**

```json
{
  "gameObjectRefs": [{ "path": "TileManager" }, { "path": "TokenManager" }]
}
```

## Cross-Cutting Inclusions

`console-get-logs` is auto-included with ALL tool groups for debugging.

`editor-application-get-state` is auto-included with:

- script group
- testing group
- prefab group
