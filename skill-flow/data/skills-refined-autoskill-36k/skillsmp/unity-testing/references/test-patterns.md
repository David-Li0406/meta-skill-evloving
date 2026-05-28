# Test Patterns

## Arrange-Act-Assert

```csharp
[Test]
public void MethodName_Scenario_ExpectedResult()
{
    // Arrange - Set up test conditions
    var input = new TestInput();

    // Act - Execute the code under test
    var result = methodUnderTest.Execute(input);

    // Assert - Verify the results
    Assert.AreEqual(expected, result);
}
```

## Naming Convention

Format: `MethodName_Scenario_ExpectedResult`

Examples:

- `GetWorldPosition_CenterTile_ReturnsZero`
- `LoadDatabase_ValidPath_Returns25Tiles`
- `ValidateMove_InvalidPath_ReturnsFalse`

## Test Isolation

- Each test should be independent
- Use `[SetUp]` for common initialization
- Use `[TearDown]` for cleanup
- Avoid shared mutable state between tests

## Mocking Approaches

For Unity:

- Interface extraction for dependencies
- ScriptableObjects for test data
- Prefab instantiation in Play mode
- `Resources.Load()` for test assets
