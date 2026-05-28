---
name: uloop-get-hierarchy
description: Use this skill when you need to inspect the Unity scene structure, explore GameObjects, and check parent-child relationships within the hierarchy.
---

# Skill body

Get Unity Hierarchy structure.

## Usage

```bash
uloop get-hierarchy [options]
```

## Parameters

| Parameter            | Type     | Default | Description                             |
|----------------------|----------|---------|-----------------------------------------|
| `--root-path`        | string   | -       | Root GameObject path to start from      |
| `--max-depth`        | integer  | `-1`    | Maximum depth (-1 for unlimited)        |
| `--include-components`| boolean  | `true`  | Include component information            |
| `--include-inactive` | boolean  | `true`  | Include inactive GameObjects             |
| `--include-paths`    | boolean  | `false` | Include full path information            |

## Examples

```bash
# Get entire hierarchy
uloop get-hierarchy

# Get hierarchy from specific root
uloop get-hierarchy --root-path "Canvas/UI"

# Limit depth
uloop get-hierarchy --max-depth 2

# Without components
uloop get-hierarchy --include-components false
```

## Output

Returns JSON with the hierarchical structure of GameObjects and their components.