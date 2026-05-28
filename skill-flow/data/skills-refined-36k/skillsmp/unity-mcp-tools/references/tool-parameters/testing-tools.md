# Testing Tools Parameters

## tests-run

Executes Unity tests with detailed filtering and output control.

### Filter Parameters

| Parameter       | Type     | Required | Default  | Description                                             |
| --------------- | -------- | -------- | -------- | ------------------------------------------------------- |
| `testMode`      | TestMode | No       | EditMode | `EditMode` or `PlayMode`                                |
| `testAssembly`  | string   | No       | null     | Assembly name (e.g., "Assembly-CSharp-Editor-testable") |
| `testNamespace` | string   | No       | null     | Namespace filter (e.g., "ZeroDayAttack.Tests")          |
| `testClass`     | string   | No       | null     | Class name filter (e.g., "TileDatabaseTests")           |
| `testMethod`    | string   | No       | null     | Fully qualified method (e.g., "Namespace.Class.Method") |

### Output Control Parameters

| Parameter             | Type | Required | Default | Description                       |
| --------------------- | ---- | -------- | ------- | --------------------------------- |
| `includePassingTests` | bool | No       | false   | Include details for passing tests |
| `includeMessages`     | bool | No       | true    | Include result messages           |
| `includeStacktrace`   | bool | No       | false   | Include stack traces for failures |

### Log Parameters

| Parameter               | Type    | Required | Default | Description                                           |
| ----------------------- | ------- | -------- | ------- | ----------------------------------------------------- |
| `includeLogs`           | bool    | No       | false   | Include console logs                                  |
| `logType`               | LogType | No       | Warning | Min log level: Log, Warning, Assert, Error, Exception |
| `includeLogsStacktrace` | bool    | No       | false   | Include log stack traces (large output)               |

### Examples

**Run all EditMode tests:**

```json
{
  "testMode": "EditMode"
}
```

**Run specific test class:**

```json
{
  "testMode": "EditMode",
  "testClass": "TileDatabaseTests",
  "includeMessages": true
}
```

**Run with full diagnostics:**

```json
{
  "testMode": "EditMode",
  "testNamespace": "ZeroDayAttack.Tests",
  "includePassingTests": true,
  "includeStacktrace": true,
  "includeLogs": true,
  "logType": "Log"
}
```

**Run PlayMode tests:**

```json
{
  "testMode": "PlayMode",
  "testClass": "GameInitializationTests"
}
```

### Response Structure

```json
{
  "status": "Completed",
  "summary": {
    "total": 10,
    "passed": 9,
    "failed": 1,
    "skipped": 0
  },
  "results": [
    {
      "name": "TestMethod",
      "status": "Failed",
      "message": "Expected 5 but was 4",
      "stackTrace": "...",
      "logs": [...]
    }
  ]
}
```

### Notes

- **EditMode recommended** for faster iteration during development
- Fails immediately if project has compilation errors
- Returns `[Processing]` status while tests run
- Final results sent via notification after completion
- Filter validation runs before test execution
