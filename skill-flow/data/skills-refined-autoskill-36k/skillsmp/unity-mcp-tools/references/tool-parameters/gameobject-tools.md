# GameObject Tools Parameters

## gameobject-create

Creates a new GameObject in scene or opened prefab.

| Parameter             | Type          | Required | Default | Description                           |
| --------------------- | ------------- | -------- | ------- | ------------------------------------- |
| `name`                | string        | Yes      | -       | Name of new GameObject                |
| `parentGameObjectRef` | GameObjectRef | No       | null    | Parent reference (see below)          |
| `position`            | Vector3       | No       | (0,0,0) | Transform position                    |
| `rotation`            | Vector3       | No       | (0,0,0) | Euler angles in degrees               |
| `scale`               | Vector3       | No       | (1,1,1) | Transform scale                       |
| `isLocalSpace`        | bool          | No       | false   | Use local vs world space              |
| `primitiveType`       | PrimitiveType | No       | null    | Create primitive (Cube, Sphere, etc.) |

**GameObjectRef Structure:**

```json
{
  "instanceID": 12345, // OR
  "path": "Parent/Child/Name", // OR
  "sceneName": "GameplayScene",
  "gameObjectName": "TileManager"
}
```

**Example:**

```json
{
  "name": "NewTile",
  "parentGameObjectRef": { "path": "TileManager" },
  "position": { "x": 2.0, "y": 0, "z": 0 },
  "scale": { "x": 2.0, "y": 2.0, "z": 1.0 }
}
```

## gameobject-find

Finds GameObjects by name or path.

| Parameter       | Type          | Required | Description       |
| --------------- | ------------- | -------- | ----------------- |
| `gameObjectRef` | GameObjectRef | Yes      | Reference to find |

## gameobject-modify

Modifies GameObject properties.

| Parameter       | Type          | Required | Description          |
| --------------- | ------------- | -------- | -------------------- |
| `gameObjectRef` | GameObjectRef | Yes      | Target GameObject    |
| `name`          | string        | No       | New name             |
| `isActive`      | bool          | No       | Active state         |
| `position`      | Vector3       | No       | New position         |
| `rotation`      | Vector3       | No       | New rotation (Euler) |
| `scale`         | Vector3       | No       | New scale            |
| `isLocalSpace`  | bool          | No       | Local vs world space |

## gameobject-destroy

Destroys a GameObject.

| Parameter       | Type          | Required | Description       |
| --------------- | ------------- | -------- | ----------------- |
| `gameObjectRef` | GameObjectRef | Yes      | Target to destroy |

## gameobject-duplicate

Duplicates a GameObject.

| Parameter       | Type          | Required | Description         |
| --------------- | ------------- | -------- | ------------------- |
| `gameObjectRef` | GameObjectRef | Yes      | Target to duplicate |

## gameobject-set-parent

Changes GameObject parent.

| Parameter             | Type          | Required | Description              |
| --------------------- | ------------- | -------- | ------------------------ |
| `gameObjectRef`       | GameObjectRef | Yes      | Target GameObject        |
| `parentGameObjectRef` | GameObjectRef | No       | New parent (null = root) |
| `worldPositionStays`  | bool          | No       | Preserve world position  |
