---
name: uloop-execute-dynamic-code
description: Execute C# code dynamically in Unity Editor via uloop CLI for automation tasks like prefab/material wiring, reference wiring, and scene edits.
---

# uloop execute-dynamic-code

Execute C# code dynamically in Unity Editor.

## Usage

```bash
uloop execute-dynamic-code --code '<c# code>'
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `--code` | string | C# code to execute (direct statements, no class wrapper) |
| `--compile-only` | boolean | Compile without execution |
| `--auto-qualify-unity-types-once` | boolean | Auto-qualify Unity types |

## Code Format

Write direct statements only (no classes/namespaces/methods). Return is optional.

```csharp
// Using directives at top are hoisted
using UnityEngine;
var x = Mathf.PI;
return x;
```

## String Literals (Shell-specific)

| Shell | Method |
|-------|--------|
| bash/zsh/MINGW64/Git Bash | `'Debug.Log("Hello!");'` |
| PowerShell | `'Debug.Log(""Hello!"");'` |

## Allowed Operations

- Prefab/material wiring (PrefabUtility)
- AddComponent + reference wiring (SerializedObject)
- Scene/hierarchy edits
- Inspector modifications

## Forbidden Operations

- System.IO.* (File/Directory/Path)
- AssetDatabase.CreateFolder / file writes
- Create/edit .cs/.asmdef files

## Examples

### bash / zsh / MINGW64 / Git Bash

```bash
uloop execute-dynamic-code --code 'return Selection.activeGameObject?.name;'
uloop execute-dynamic-code --code 'new GameObject("MyObject");'
uloop execute-dynamic-code --code 'UnityEngine.Debug.Log("Hello from CLI!");'
```

### PowerShell

```powershell
uloop execute-dynamic-code --code 'return Selection.activeGameObject?.name;'
uloop execute-dynamic-code --code 'new GameObject(""MyObject"");'
uloop execute-dynamic-code --code 'UnityEngine.Debug.Log(""Hello from CLI!"");'
```

## Output

Returns JSON with execution result or compile errors.

## Notes

For file/directory operations, use terminal commands instead.

## Code Examples by Category

For detailed code examples, refer to these files:

- **Prefab operations**: Create prefabs, instantiate, add components, modify properties.
- **Material operations**: Create materials, set shaders/textures, modify properties.
- **Asset operations**: Find/search assets, duplicate, move, rename, load.
- **ScriptableObject**: Create ScriptableObjects, modify with SerializedObject.
- **Scene operations**: Create/modify GameObjects, set parents, wire references, load scenes.