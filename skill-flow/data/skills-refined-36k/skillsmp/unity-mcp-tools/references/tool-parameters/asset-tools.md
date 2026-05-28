# Asset Tools Parameters

## assets-find

Searches the asset database using Unity's search filter syntax.

| Parameter         | Type     | Required | Default | Description               |
| ----------------- | -------- | -------- | ------- | ------------------------- |
| `filter`          | string   | No       | null    | Search filter (see below) |
| `searchInFolders` | string[] | No       | null    | Limit search to folders   |
| `maxResults`      | int      | No       | 10      | Maximum results to return |

**Filter Syntax:**

- **Name**: `test asset` - matches filename containing words
- **Labels**: `l:important` - assets with label
- **Types**: `t:Prefab`, `t:Script`, `t:Material`, `t:Texture`, etc.
- **Bundles**: `b:mybundle` - assets in bundle
- **Area**: `a:assets`, `a:packages`, `a:all`
- **Glob**: `glob:Editor/*` - glob pattern matching

**Common Types:**
`t:AnimationClip`, `t:AudioClip`, `t:Font`, `t:Material`, `t:Mesh`, `t:Prefab`, `t:Scene`, `t:Script`, `t:Shader`, `t:Sprite`, `t:Texture`

**Example:**

```json
{
  "filter": "t:Prefab Tile",
  "searchInFolders": ["Assets/Prefabs"],
  "maxResults": 20
}
```

## assets-copy

Copies an asset to a new location.

| Parameter         | Type   | Required | Description       |
| ----------------- | ------ | -------- | ----------------- |
| `sourcePath`      | string | Yes      | Source asset path |
| `destinationPath` | string | Yes      | Destination path  |

## assets-move

Moves an asset to a new location.

| Parameter         | Type   | Required | Description       |
| ----------------- | ------ | -------- | ----------------- |
| `sourcePath`      | string | Yes      | Source asset path |
| `destinationPath` | string | Yes      | Destination path  |

## assets-delete

Deletes an asset.

| Parameter   | Type   | Required | Description             |
| ----------- | ------ | -------- | ----------------------- |
| `assetPath` | string | Yes      | Path to asset to delete |

## assets-create-folders

Creates folder structure.

| Parameter       | Type   | Required | Description              |
| --------------- | ------ | -------- | ------------------------ |
| `parentFolder`  | string | Yes      | Parent folder path       |
| `newFolderName` | string | Yes      | Name of folder to create |

## assets-get-data

Gets detailed data about an asset.

| Parameter   | Type   | Required | Description   |
| ----------- | ------ | -------- | ------------- |
| `assetPath` | string | Yes      | Path to asset |

## assets-modify

Modifies asset properties.

| Parameter   | Type             | Required | Description          |
| ----------- | ---------------- | -------- | -------------------- |
| `assetPath` | string           | Yes      | Path to asset        |
| `assetDiff` | SerializedMember | Yes      | Properties to modify |

## assets-refresh

Refreshes the AssetDatabase. No parameters.

**Use After:** Script creation, external file changes, bulk operations.
