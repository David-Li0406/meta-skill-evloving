# EditMode Tests

## When to Use

- ScriptableObject validation
- Pure C# logic (no MonoBehaviour)
- Data structure integrity
- Configuration validation
- Fast iteration during development

## Location

```text
Assets/Tests/Editor/
├── TileDatabaseTests.cs
├── BoardLayoutConfigTests.cs
└── [YourTests].cs
```

## Assembly Definition

Requires `Assets/Tests/Editor/Tests.Editor.asmdef`:

```json
{
  "name": "Tests.Editor",
  "references": ["UnityEngine.TestRunner", "UnityEditor.TestRunner"],
  "includePlatforms": ["Editor"]
}
```

## Example: ScriptableObject Test

```csharp
using NUnit.Framework;
using UnityEngine;

[TestFixture]
public class TileDatabaseTests
{
    private TileDatabase database;

    [SetUp]
    public void SetUp()
    {
        database = Resources.Load<TileDatabase>("TileDatabase");
    }

    [Test]
    public void Load_DatabaseExists_ReturnsNonNull()
    {
        Assert.IsNotNull(database, "TileDatabase not found in Resources");
    }

    [Test]
    public void Tiles_Count_Returns25()
    {
        Assert.AreEqual(25, database.Tiles.Count);
    }
}
```

## Running EditMode Tests

1. Window > General > Test Runner
2. Select EditMode tab
3. Click Run All or select specific tests
