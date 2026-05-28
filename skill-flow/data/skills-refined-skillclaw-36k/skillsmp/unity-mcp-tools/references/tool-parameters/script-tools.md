# Script Tools Parameters

## script-update-or-create

Creates or updates a C# script file. Validates syntax before writing.

| Parameter  | Type   | Required | Description                            |
| ---------- | ------ | -------- | -------------------------------------- |
| `filePath` | string | Yes      | Path like "Assets/Scripts/MyScript.cs" |
| `content`  | string | Yes      | Full C# code content                   |

**Behavior:**

- Validates C# syntax before writing
- Creates directories if needed
- Triggers AssetDatabase.Refresh()
- Returns compilation errors if any

**Example:**

```json
{
  "filePath": "Assets/Scripts/Core/NewManager.cs",
  "content": "using UnityEngine;\n\nnamespace ZeroDayAttack.Core\n{\n    public class NewManager : MonoBehaviour\n    {\n        // Implementation\n    }\n}"
}
```

**Response:**

- Returns `[Processing]` while compiling
- Sends completion notification after domain reload
- Reports syntax errors if validation fails

## script-read

Reads a script file's content.

| Parameter  | Type   | Required | Description      |
| ---------- | ------ | -------- | ---------------- |
| `filePath` | string | Yes      | Path to .cs file |

## script-delete

Deletes a script file.

| Parameter  | Type   | Required | Description                |
| ---------- | ------ | -------- | -------------------------- |
| `filePath` | string | Yes      | Path to .cs file to delete |

**Warning:** Triggers domain reload if script was compiled.

## script-execute

Executes arbitrary C# code at runtime.

| Parameter | Type   | Required | Description        |
| --------- | ------ | -------- | ------------------ |
| `code`    | string | Yes      | C# code to execute |

**Use Cases:**

- Quick debugging
- One-off operations
- Testing logic

**Note:** Code runs in Unity's main thread context.
