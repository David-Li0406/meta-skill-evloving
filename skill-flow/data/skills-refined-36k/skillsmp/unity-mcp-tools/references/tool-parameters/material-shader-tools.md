# Material & Shader Tools Parameters

## assets-material-create

Creates a new material asset.

| Parameter      | Type   | Required | Default    | Description                          |
| -------------- | ------ | -------- | ---------- | ------------------------------------ |
| `materialPath` | string | Yes      | -          | Path like "Assets/Materials/New.mat" |
| `shaderName`   | string | No       | "Standard" | Shader to use                        |

**Example:**

```json
{
  "materialPath": "Assets/Materials/TileGlow.mat",
  "shaderName": "Sprites/Default"
}
```

## assets-material-get

Gets material properties.

| Parameter   | Type   | Required | Description            |
| ----------- | ------ | -------- | ---------------------- |
| `assetPath` | string | Yes      | Path to material asset |

**Returns:** Material properties including colors, textures, shader params.

## assets-material-modify

Modifies material properties.

| Parameter      | Type             | Required | Description          |
| -------------- | ---------------- | -------- | -------------------- |
| `assetPath`    | string           | Yes      | Path to material     |
| `materialDiff` | SerializedMember | Yes      | Properties to modify |

**Example:**

```json
{
  "assetPath": "Assets/Materials/TileGlow.mat",
  "materialDiff": {
    "props": {
      "color": { "value": { "r": 1, "g": 0.5, "b": 0, "a": 1 } }
    }
  }
}
```

## assets-shader-list-all

Lists all available shaders. No parameters.

**Returns:** Array of shader names available in project.

**Common Shaders:**

- `Standard` - Default PBR
- `Sprites/Default` - 2D sprites
- `UI/Default` - UI elements
- `Unlit/Color` - Simple unlit
- `Unlit/Texture` - Textured unlit
