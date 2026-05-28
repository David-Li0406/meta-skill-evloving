# Scene Tools Parameters

## scene-get-data

Retrieves root GameObjects and hierarchy from a scene.

| Parameter                | Type   | Required | Default | Description                             |
| ------------------------ | ------ | -------- | ------- | --------------------------------------- |
| `openedSceneName`        | string | No       | null    | Scene name. If empty, uses active scene |
| `includeRootGameObjects` | bool   | No       | false   | Include root GameObjects in response    |
| `includeChildrenDepth`   | int    | No       | 3       | Hierarchy depth to include              |
| `deepSerialization`      | bool   | No       | false   | Deep serialize GameObjects              |
| `includeBounds`          | bool   | No       | false   | Include bounding box info               |
| `includeData`            | bool   | No       | false   | Include component data                  |

**Example:**

```json
{
  "openedSceneName": "GameplayScene",
  "includeRootGameObjects": true,
  "includeChildrenDepth": 2,
  "includeData": true
}
```

## scene-list-opened

Lists all currently opened scenes. No parameters.

## scene-create

Creates a new scene.

| Parameter   | Type   | Required | Description                              |
| ----------- | ------ | -------- | ---------------------------------------- |
| `scenePath` | string | Yes      | Path like "Assets/Scenes/NewScene.unity" |

## scene-open

Opens an existing scene.

| Parameter   | Type   | Required | Description        |
| ----------- | ------ | -------- | ------------------ |
| `scenePath` | string | Yes      | Path to scene file |

## scene-save

Saves the current scene. No parameters required.

## scene-set-active

Sets a scene as the active scene.

| Parameter   | Type   | Required | Description                      |
| ----------- | ------ | -------- | -------------------------------- |
| `sceneName` | string | Yes      | Name of opened scene to activate |

## scene-unload

Unloads a scene from the hierarchy.

| Parameter   | Type   | Required | Description             |
| ----------- | ------ | -------- | ----------------------- |
| `sceneName` | string | Yes      | Name of scene to unload |
