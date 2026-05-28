# MCP Tool Groups

Complete group definitions for `/unity-mcp-enable`.

## Group Definitions

### scene-read

```json
["scene-get-data", "scene-list-opened", "console-get-logs"]
```

### scene-write

```json
[
  "scene-create",
  "scene-save",
  "scene-open",
  "scene-set-active",
  "scene-unload",
  "console-get-logs"
]
```

### gameobject

```json
[
  "gameobject-create",
  "gameobject-find",
  "gameobject-modify",
  "gameobject-destroy",
  "gameobject-duplicate",
  "gameobject-set-parent",
  "scene-save",
  "console-get-logs"
]
```

### component

```json
[
  "gameobject-component-add",
  "gameobject-component-get",
  "gameobject-component-modify",
  "gameobject-component-destroy",
  "component-list",
  "scene-save",
  "console-get-logs"
]
```

### script

```json
[
  "script-read",
  "script-update-or-create",
  "script-delete",
  "script-execute",
  "assets-refresh",
  "editor-application-get-state",
  "console-get-logs"
]
```

### prefab

```json
[
  "assets-prefab-create",
  "assets-prefab-instantiate",
  "assets-prefab-open",
  "assets-prefab-save",
  "assets-prefab-close",
  "assets-refresh",
  "editor-application-get-state",
  "console-get-logs"
]
```

### assets

```json
[
  "assets-find",
  "assets-create-folder",
  "assets-copy",
  "assets-move",
  "assets-delete",
  "assets-get-data",
  "assets-modify",
  "assets-refresh",
  "assets-material-create",
  "assets-shader-list-all",
  "console-get-logs"
]
```

### testing

```json
["tests-run", "editor-application-get-state", "console-get-logs"]
```

### editor

```json
[
  "editor-application-get-state",
  "editor-application-set-state",
  "console-get-logs",
  "editor-selection-get",
  "editor-selection-set"
]
```

### packages

```json
[
  "package-list",
  "package-add",
  "package-remove",
  "package-search",
  "console-get-logs"
]
```

### reflection

```json
["reflection-method-find", "reflection-method-call", "console-get-logs"]
```

## Cross-cutting Utilities

These tools are auto-included when enabling related groups:

| Tool                         | Auto-included with      |
| ---------------------------- | ----------------------- |
| console-get-logs             | ALL groups              |
| editor-application-get-state | script, testing, prefab |
| assets-refresh               | script, prefab          |
| scene-save                   | gameobject, component   |

## Usage

Enable single group:

```text
/unity-mcp-enable gameobject
```

Enable multiple groups:

```text
/unity-mcp-enable gameobject component prefab
```

Check status:

```text
/unity-mcp-status
```

Reset all:

```text
/unity-mcp-reset
```
