# Prefab Tools Parameters

## assets-prefab-create

Creates a prefab from a scene GameObject.

| Parameter                     | Type          | Required | Default | Description                               |
| ----------------------------- | ------------- | -------- | ------- | ----------------------------------------- |
| `prefabAssetPath`             | string        | Yes      | -       | Path like "Assets/Prefabs/My.prefab"      |
| `gameObjectRef`               | GameObjectRef | Yes      | -       | Source GameObject                         |
| `replaceGameObjectWithPrefab` | bool          | No       | true    | Replace scene object with prefab instance |

**Example:**

```json
{
  "prefabAssetPath": "Assets/Prefabs/Tiles/NewTile.prefab",
  "gameObjectRef": { "path": "TileManager/Tile_Template" },
  "replaceGameObjectWithPrefab": true
}
```

## assets-prefab-instantiate

Creates an instance of a prefab in the scene.

| Parameter             | Type          | Required | Default | Description          |
| --------------------- | ------------- | -------- | ------- | -------------------- |
| `prefabAssetPath`     | string        | Yes      | -       | Path to prefab asset |
| `parentGameObjectRef` | GameObjectRef | No       | null    | Parent for instance  |
| `position`            | Vector3       | No       | (0,0,0) | Position             |
| `rotation`            | Vector3       | No       | (0,0,0) | Rotation (Euler)     |
| `scale`               | Vector3       | No       | (1,1,1) | Scale                |
| `isLocalSpace`        | bool          | No       | false   | Local vs world space |

**Example:**

```json
{
  "prefabAssetPath": "Assets/Prefabs/TilePrefab.prefab",
  "parentGameObjectRef": { "path": "TileManager" },
  "position": { "x": 4.0, "y": 0, "z": 0 }
}
```

## assets-prefab-open

Opens a prefab for editing in isolation mode.

| Parameter         | Type   | Required | Description    |
| ----------------- | ------ | -------- | -------------- |
| `prefabAssetPath` | string | Yes      | Path to prefab |

**Note:** Required before modifying prefab internals.

## assets-prefab-save

Saves changes to the currently open prefab.

No parameters. Saves the prefab currently in edit mode.

## assets-prefab-close

Closes the prefab edit mode, returning to scene view.

| Parameter     | Type | Required | Default | Description         |
| ------------- | ---- | -------- | ------- | ------------------- |
| `saveChanges` | bool | No       | true    | Save before closing |

## Prefab Editing Workflow

1. **Open prefab**: `assets-prefab-open`
2. **Modify contents**: Use `gameobject-*` and `component-*` tools
3. **Save changes**: `assets-prefab-save`
4. **Close**: `assets-prefab-close`

**Example Workflow:**

```json
// Step 1: Open
{ "prefabAssetPath": "Assets/Prefabs/TilePrefab.prefab" }

// Step 2: Modify (e.g., add component)
{
  "componentNames": ["UnityEngine.BoxCollider2D"],
  "gameObjectRef": { "path": "TilePrefab" }
}

// Step 3: Save
// (no params)

// Step 4: Close
{ "saveChanges": true }
```
