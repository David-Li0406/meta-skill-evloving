# Reflection Tools Parameters

## reflection-method-find

Finds C# methods by filter criteria.

| Parameter              | Type      | Required | Default | Description                |
| ---------------------- | --------- | -------- | ------- | -------------------------- |
| `filter`               | MethodRef | Yes      | -       | Method filter (see below)  |
| `knownNamespace`       | bool      | No       | false   | Namespace is exact match   |
| `typeNameMatchLevel`   | int       | No       | 1       | Type name matching (0-6)   |
| `methodNameMatchLevel` | int       | No       | 1       | Method name matching (0-6) |
| `maxResults`           | int       | No       | 10      | Max methods to return      |

**MethodRef Structure:**

```json
{
  "Namespace": "ZeroDayAttack.Core",
  "TypeName": "GameManager",
  "MethodName": "Initialize"
}
```

**Match Levels:**

- 0: Ignore field
- 1: Contains, ignore case (default)
- 2: Contains, case sensitive
- 3: Starts with, ignore case
- 4: Starts with, case sensitive
- 5: Equals, ignore case
- 6: Equals, case sensitive

## reflection-method-call

Calls any C# method, including private methods.

| Parameter              | Type                 | Required | Default | Description              |
| ---------------------- | -------------------- | -------- | ------- | ------------------------ |
| `filter`               | MethodRef            | Yes      | -       | Method to call           |
| `knownNamespace`       | bool                 | No       | false   | Namespace is exact       |
| `typeNameMatchLevel`   | int                  | No       | 1       | Type matching            |
| `methodNameMatchLevel` | int                  | No       | 1       | Method matching          |
| `parametersMatchLevel` | int                  | No       | 2       | Parameter matching (0-2) |
| `targetObject`         | SerializedMember     | No       | null    | Instance to call on      |
| `inputParameters`      | SerializedMemberList | No       | null    | Method arguments         |
| `executeInMainThread`  | bool                 | No       | true    | Run on Unity main thread |

**Parameter Match Levels:**

- 0: Ignore parameters
- 1: Parameter count matches
- 2: Exact match (default)

**Example - Call Static Method:**

```json
{
  "filter": {
    "Namespace": "ZeroDayAttack.Core",
    "TypeName": "GameManager",
    "MethodName": "ResetGame"
  },
  "knownNamespace": true,
  "typeNameMatchLevel": 6,
  "methodNameMatchLevel": 6
}
```

**Example - Call Instance Method with Parameters:**

```json
{
  "filter": {
    "TypeName": "TileManager",
    "MethodName": "SpawnTile"
  },
  "targetObject": {
    "typeName": "ZeroDayAttack.View.TileManager",
    "value": null
  },
  "inputParameters": [
    {
      "name": "gridPosition",
      "typeName": "UnityEngine.Vector2Int",
      "value": { "x": 2, "y": 3 }
    }
  ]
}
```

**Notes:**

- Use `reflection-method-find` first to discover method signatures
- `targetObject` null for static methods
- For instance methods with null `targetObject`, creates new instance
- Returns serialized result of method return value
