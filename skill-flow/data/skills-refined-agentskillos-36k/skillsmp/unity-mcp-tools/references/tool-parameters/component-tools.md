# Component Tools Parameters

## gameobject-component-add

Adds components to a GameObject.

| Parameter        | Type          | Required | Description                         |
| ---------------- | ------------- | -------- | ----------------------------------- |
| `componentNames` | string[]      | Yes      | Full type names including namespace |
| `gameObjectRef`  | GameObjectRef | Yes      | Target GameObject                   |

**Example:**

```json
{
  "componentNames": [
    "UnityEngine.BoxCollider2D",
    "ZeroDayAttack.View.TileView"
  ],
  "gameObjectRef": { "path": "TileManager/Tile_0" }
}
```

**Returns:**

- `AddedComponents`: List of successfully added components
- `Messages`: Success messages
- `Errors`: Any errors encountered

## gameobject-component-get

Gets component data from a GameObject.

| Parameter       | Type          | Required | Description         |
| --------------- | ------------- | -------- | ------------------- |
| `gameObjectRef` | GameObjectRef | Yes      | Target GameObject   |
| `componentRef`  | ComponentRef  | Yes      | Component reference |

**ComponentRef Structure:**

```json
{
  "instanceID": 12345, // OR
  "index": 0, // OR
  "typeName": "Transform" // Component type name
}
```

## gameobject-component-modify

Modifies component properties.

| Parameter       | Type             | Required | Description                 |
| --------------- | ---------------- | -------- | --------------------------- |
| `gameObjectRef` | GameObjectRef    | Yes      | Target GameObject           |
| `componentRef`  | ComponentRef     | Yes      | Component reference         |
| `componentDiff` | SerializedMember | Yes      | Fields/properties to modify |

**componentDiff Structure:**

```json
{
  "fields": {
    "fieldName": { "value": "newValue" }
  },
  "props": {
    "propertyName": { "value": 123 }
  }
}
```

**Example - Modify Transform:**

```json
{
  "gameObjectRef": { "path": "TileManager/Tile_0" },
  "componentRef": { "typeName": "Transform" },
  "componentDiff": {
    "props": {
      "localPosition": { "value": { "x": 2.0, "y": 0, "z": 0 } }
    }
  }
}
```

**Returns:**

- `success`: Whether modification succeeded
- `reference`: Component reference
- `component`: Updated component data
- `logs`: Modification log and warnings

## gameobject-component-destroy

Removes a component from a GameObject.

| Parameter       | Type          | Required | Description         |
| --------------- | ------------- | -------- | ------------------- |
| `gameObjectRef` | GameObjectRef | Yes      | Target GameObject   |
| `componentRef`  | ComponentRef  | Yes      | Component to remove |

## component-get-all

Lists all available component types.

| Parameter    | Type   | Required | Default | Description           |
| ------------ | ------ | -------- | ------- | --------------------- |
| `filter`     | string | No       | null    | Filter by type name   |
| `maxResults` | int    | No       | 50      | Max results to return |
