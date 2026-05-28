# Existing Test Inventory

## EditMode Tests

| Test File                   | Purpose                                      | Tests                                              |
| --------------------------- | -------------------------------------------- | -------------------------------------------------- |
| `TileDatabaseTests.cs`      | Validates TileDatabase loading and integrity | Database loads, 25 tiles present, all have sprites |
| `BoardLayoutConfigTests.cs` | Validates LayoutConfig constants             | Grid dimensions, zone boundaries, calculations     |

## PlayMode Tests

| Test File                      | Purpose                                     | Tests                                           |
| ------------------------------ | ------------------------------------------- | ----------------------------------------------- |
| `CoordinateConversionTests.cs` | Validates TileManager coordinate conversion | Grid-to-world mapping, center tile position     |
| `GameInitializationTests.cs`   | Validates GameManager startup               | Scene loads, managers exist, center tile placed |

## Test Locations

```text
Assets/Tests/
├── Editor/
│   ├── TileDatabaseTests.cs
│   └── BoardLayoutConfigTests.cs
└── Runtime/
    ├── CoordinateConversionTests.cs
    └── GameInitializationTests.cs
```

## Running Tests

### Via Unity

1. Window > General > Test Runner
2. Select EditMode or PlayMode tab
3. Run All or select specific tests

### Via MCP

```json
{
  "testMode": "EditMode",
  "testClass": "TileDatabaseTests"
}
```

## Coverage Areas

| Area            | EditMode | PlayMode |
| --------------- | -------- | -------- |
| Data loading    | Yes      | -        |
| Configuration   | Yes      | -        |
| Scene setup     | -        | Yes      |
| Component init  | -        | Yes      |
| Coordinate math | Yes      | Yes      |
