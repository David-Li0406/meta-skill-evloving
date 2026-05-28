# PlayMode Tests

## When to Use

- MonoBehaviour testing
- Scene loading and initialization
- Component interactions
- Coroutines and async operations
- Integration tests

## Location

```text
Assets/Tests/Runtime/
├── CoordinateConversionTests.cs
├── GameInitializationTests.cs
└── [YourTests].cs
```

## Assembly Definition

Requires `Assets/Tests/Runtime/Tests.Runtime.asmdef`:

```json
{
  "name": "Tests.Runtime",
  "references": ["UnityEngine.TestRunner", "UnityEditor.TestRunner"],
  "includePlatforms": []
}
```

## Example: Scene Test

```csharp
using NUnit.Framework;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;
using System.Collections;

[TestFixture]
public class GameInitializationTests
{
    [UnitySetUp]
    public IEnumerator SetUp()
    {
        SceneManager.LoadScene("GameplayScene");
        yield return null;
    }

    [UnityTest]
    public IEnumerator GameManager_OnSceneLoad_Exists()
    {
        yield return null;
        var gm = Object.FindObjectOfType<GameManager>();
        Assert.IsNotNull(gm);
    }

    [UnityTest]
    public IEnumerator TileManager_AfterInit_HasCenterTile()
    {
        yield return new WaitForSeconds(0.1f);
        var tm = TileManager.Instance;
        Assert.IsNotNull(tm.GetTileAt(2, 2));
    }
}
```

## Coroutine Tests

Use `[UnityTest]` instead of `[Test]` for coroutines:

```csharp
[UnityTest]
public IEnumerator AsyncOperation_Completes_InTime()
{
    var operation = StartAsyncOperation();
    yield return new WaitForSeconds(1f);
    Assert.IsTrue(operation.IsComplete);
}
```
