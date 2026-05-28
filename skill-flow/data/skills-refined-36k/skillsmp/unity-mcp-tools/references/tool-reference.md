# Unity MCP Tool Reference

Complete reference for all 50 Unity MCP tools organized by category.

## Scene Operations

| Tool                | Purpose               | When to Use                     |
| ------------------- | --------------------- | ------------------------------- |
| `scene-get-data`    | Query scene hierarchy | Inspect current scene structure |
| `scene-create`      | Create new scene      | Starting fresh scene            |
| `scene-save`        | Save current scene    | After modifications             |
| `scene-open`        | Open scene file       | Switch to different scene       |
| `scene-list-opened` | List open scenes      | Check what's loaded             |
| `scene-set-active`  | Set active scene      | Multiple scenes loaded          |
| `scene-unload`      | Unload additive scene | Remove loaded scene             |

## GameObject Operations

| Tool                    | Purpose                      | When to Use                 |
| ----------------------- | ---------------------------- | --------------------------- |
| `gameobject-create`     | Create new GameObject        | Adding objects to scene     |
| `gameobject-find`       | Find GameObject by path/name | Locating existing objects   |
| `gameobject-modify`     | Modify GameObject properties | Changing name, active state |
| `gameobject-destroy`    | Delete GameObject            | Removing objects            |
| `gameobject-duplicate`  | Clone GameObject             | Copying objects             |
| `gameobject-set-parent` | Change hierarchy             | Reorganizing scene          |

## Component Operations

| Tool                           | Purpose                     | When to Use              |
| ------------------------------ | --------------------------- | ------------------------ |
| `gameobject-component-add`     | Add component to GameObject | Adding behaviors         |
| `gameobject-component-get`     | Inspect component data      | Reading component values |
| `gameobject-component-modify`  | Change component values     | Updating settings        |
| `gameobject-component-destroy` | Remove component            | Cleaning up              |
| `component-list`               | List available components   | Finding component types  |

## Script Operations

| Tool                      | Purpose               | When to Use                 |
| ------------------------- | --------------------- | --------------------------- |
| `script-read`             | Read C# file contents | Inspecting code             |
| `script-update-or-create` | Write/modify C# file  | Creating or editing scripts |
| `script-delete`           | Delete script file    | Removing scripts            |
| `script-execute`          | Run arbitrary C# code | One-time operations         |

## Asset Operations

| Tool                     | Purpose                | When to Use               |
| ------------------------ | ---------------------- | ------------------------- |
| `assets-find`            | Search for assets      | Locating files            |
| `assets-create-folder`   | Create folder          | Organizing project        |
| `assets-copy`            | Copy asset             | Duplicating files         |
| `assets-move`            | Move/rename asset      | Reorganizing              |
| `assets-delete`          | Delete asset           | Cleanup                   |
| `assets-get-data`        | Get asset details      | Inspecting assets         |
| `assets-modify`          | Modify asset           | Updating asset properties |
| `assets-refresh`         | Force database refresh | After external changes    |
| `assets-material-create` | Create new Material    | Adding materials          |
| `assets-shader-list-all` | List available shaders | Finding shader options    |

## Prefab Operations

| Tool                        | Purpose                       | When to Use             |
| --------------------------- | ----------------------------- | ----------------------- |
| `assets-prefab-create`      | Create prefab from GameObject | Saving reusable objects |
| `assets-prefab-instantiate` | Spawn prefab instance         | Adding prefab to scene  |
| `assets-prefab-open`        | Enter prefab edit mode        | Modifying prefab        |
| `assets-prefab-save`        | Save prefab changes           | After editing           |
| `assets-prefab-close`       | Exit prefab edit mode         | Done editing            |

## Editor Control

| Tool                           | Purpose               | When to Use                     |
| ------------------------------ | --------------------- | ------------------------------- |
| `editor-application-get-state` | Check editor state    | Verify play mode, compilation   |
| `editor-application-set-state` | Control editor        | Start/stop play mode            |
| `console-get-logs`             | Get console output    | Debugging, checking errors      |
| `editor-selection-get`         | Get current selection | Check what's selected           |
| `editor-selection-set`         | Set selection         | Select objects programmatically |

## Testing

| Tool        | Purpose             | When to Use                     |
| ----------- | ------------------- | ------------------------------- |
| `tests-run` | Execute Unity tests | Running EditMode/PlayMode tests |

### Test Parameters

```json
{
  "testMode": "EditMode",
  "includePassingTests": false,
  "includeMessages": true
}
```

## Package Management

| Tool             | Purpose                 | When to Use                |
| ---------------- | ----------------------- | -------------------------- |
| `package-list`   | List installed packages | Check dependencies         |
| `package-add`    | Add package             | Installing new packages    |
| `package-remove` | Remove package          | Uninstalling packages      |
| `package-search` | Search registry         | Finding available packages |

## Reflection Tools

For advanced operations when standard tools are insufficient:

| Tool                     | Purpose                             |
| ------------------------ | ----------------------------------- |
| `reflection-method-find` | Find methods by name                |
| `reflection-method-call` | Call any method (including private) |

Use cautiously - prefer standard tools when possible.

## Tool Selection Guide

### For Creating Things

| Want to Create | Use Tool                                        |
| -------------- | ----------------------------------------------- |
| New GameObject | `gameobject-create`                             |
| New C# script  | `script-update-or-create`                       |
| New prefab     | `gameobject-create` then `assets-prefab-create` |
| New folder     | `assets-create-folder`                          |
| New scene      | `scene-create`                                  |
| New material   | `assets-material-create`                        |

### For Finding Things

| Want to Find        | Use Tool                   |
| ------------------- | -------------------------- |
| GameObject in scene | `gameobject-find`          |
| Asset in project    | `assets-find`              |
| Component data      | `gameobject-component-get` |
| Script contents     | `script-read`              |
| Available shaders   | `assets-shader-list-all`   |
| Component types     | `component-list`           |

### For Modifying Things

| Want to Modify        | Use Tool                      |
| --------------------- | ----------------------------- |
| GameObject properties | `gameobject-modify`           |
| Component values      | `gameobject-component-modify` |
| Script code           | `script-update-or-create`     |
| Asset properties      | `assets-modify`               |
| Scene hierarchy       | `gameobject-set-parent`       |

## Best Practices

### Use Specific References

Prefer `instanceID` or `path` over `name` for reliable object finding:

```json
{
  "gameObjectRef": {
    "instanceID": 12345,
    "path": "TileManager/Tiles/Tile_2_2"
  }
}
```

### Batch Operations

When modifying multiple objects, use array parameters where supported to reduce round trips.

### Check Compilation

After `script-update-or-create`, the tool provides compilation feedback. Always check for errors before proceeding.

### Minimal Tool Calls

Prefer fewer, well-targeted tool calls over many exploratory ones:

- Use `scene-get-data` with appropriate depth
- Use `gameobject-component-get` with `includeFields: true` when needed

### Test After Changes

Run `tests-run` after significant code changes.

## Component Type Names

When adding components, use full type names:

| Common Component | Full Name                     |
| ---------------- | ----------------------------- |
| Transform        | `UnityEngine.Transform`       |
| SpriteRenderer   | `UnityEngine.SpriteRenderer`  |
| BoxCollider2D    | `UnityEngine.BoxCollider2D`   |
| Rigidbody2D      | `UnityEngine.Rigidbody2D`     |
| Image            | `UnityEngine.UI.Image`        |
| Text             | `UnityEngine.UI.Text`         |
| Canvas           | `UnityEngine.Canvas`          |
| Custom Script    | `ZeroDayAttack.View.TileView` |
