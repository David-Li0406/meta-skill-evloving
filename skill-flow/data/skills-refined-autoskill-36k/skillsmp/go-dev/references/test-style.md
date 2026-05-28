# Go Test Style Guidelines

## Table of Contents

- [General Principles](#general-principles)
- [Test Naming Conventions](#test-naming-conventions)
- [Table-Driven Tests](#table-driven-tests)
- [Error Assertions](#error-assertions)
- [Unit Tests](#unit-tests)
- [Integration Tests](#integration-tests)
- [Using Mocks](#using-mocks)
- [Tech Stack](#tech-stack)

---

## General Principles

- Use the `testify` library for all testing in Go.
- Always use the `require` package from `testify` when checking the `error` type.
- Each test should verify a single behavior or property. Do not test multiple behaviors in a single test.

---

## Test Naming Conventions

Name tests using descriptive and natural language (literate test names).

**Format:** `Test_<DescriptiveStatement>`

**Guidelines:**

- Test names should describe what the test does and what it verifies, not implementation details.
- Use the `Test_` prefix for test functions.
- If a condition is crucial to the test, include it in the test name.
- Prefer `Should` statements when they fit naturally.

**Examples:**

```go
// Good: describes behavior
func Test_CompatibilityConfigCanBeLoadedFromFile(t *testing.T)
func Test_CompatibilityConfigCanBeLoadedFromFileWhenFileExists(t *testing.T)
func Test_CreatingClientShouldLoadCompatibilityMapFromFile(t *testing.T)

// Bad: describes implementation
func Test_LoadConfig(t *testing.T)
func Test_ConfigLoader_Success(t *testing.T)
```

---

## Table-Driven Tests

Use table-driven tests when testing multiple scenarios. This pattern makes it easy to add new test cases and keeps the code clean.

```go
func Test_VerbosityLevelDetermination(t *testing.T) {
    tests := []struct {
        name     string
        verbose  bool
        extra    bool
        expected VerbosityLevel
    }{
        {"default returns normal", false, false, VerbosityNormal},
        {"verbose flag returns verbose", true, false, VerbosityVerbose},
        {"both flags returns extra verbose", true, true, VerbosityExtraVerbose},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := determineVerbosity(tt.verbose, tt.extra)
            require.Equal(t, tt.expected, result)
        })
    }
}
```

---

## Error Assertions

When expecting an error, don't match the error message directly. Instead, use specific keywords that are pivotal to the error.

```go
// Good: checks for key error indicator
err := loadConfig("nonexistent.yaml")
require.Error(t, err)
require.Contains(t, err.Error(), "not found")

// Bad: matches entire error message
require.EqualError(t, err, "file could not be found in the path /config/nonexistent.yaml")
```

---

## Unit Tests

Unit tests verify a single function or method in isolation.

**Characteristics:**

- Use mocks to isolate the function or method being tested.
- Place unit tests in the same package as the code being tested.

```go
// File: lib/brew/brew_test.go
package brew  // Same package as implementation

func Test_BrewPackageManagerInstallsPackageSuccessfully(t *testing.T) {
    // Arrange
    commander := &MoqCommander{
        RunCommandFunc: func(ctx context.Context, name string, args []string, opts ...Option) (Result, error) {
            return Result{ExitCode: 0}, nil
        },
    }
    pm := NewBrewPackageManager(logger, commander, osManager, "/opt/homebrew/bin/brew")

    // Act
    err := pm.InstallPackage(ctx, RequestedPackageInfo{Name: "git"})

    // Assert
    require.NoError(t, err)
}
```

---

## Integration Tests

Integration tests verify the interaction between multiple functions or methods, including OS-dependent interactions.

**Characteristics:**

- Cover OS-dependent interactions (anything beyond CPU and memory).
- Allow opting out using `testing.Short()`.
- Place in the test package (e.g., `lib_test` for `lib` package).
- Write in BDD-style "given-when-then".

**Naming Format:** `Test_<gerund>_Should_<expected-behavior>_When_<condition>`

```go
// File: lib/brew/integration_test.go
package brew_test  // Test package (external)

func Test_InstallingPackage_Should_SucceedWithoutError_When_BrewIsAvailable(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping integration test in short mode")
    }

    // Given
    pm := NewBrewPackageManager(/* real dependencies */)

    // When
    err := pm.InstallPackage(ctx, RequestedPackageInfo{Name: "tree"})

    // Then
    require.NoError(t, err)
}
```

---

## Using Mocks

Mocks are generated using `mockery` with `moq` template.

**Key Points:**

- Assume mocks are already generated.
- If a mock is missing, run `mockery` in the project root (no arguments).
- Prefix mock types with `Moq` as expected by the moq library.
- Pass function implementations to the mock constructor.
- Mock files are placed next to the interface they mock.

**Mock File Naming:** `{interfacename}_mock.go` (lowercase)

**Example:**

```go
// For interface Logger, mock file is: logger_mock.go
// Mock type is: MoqLogger

func Test_ServiceLogsErrors(t *testing.T) {
    var loggedMessage string
    logger := &MoqLogger{
        ErrorFunc: func(format string, args ...any) {
            loggedMessage = fmt.Sprintf(format, args...)
        },
    }

    svc := NewService(logger)
    svc.DoSomethingThatFails()

    require.Contains(t, loggedMessage, "failed")
}
```

**Regenerating Mocks:**

```bash
cd installer
mockery
```

---

## Tech Stack

| Tool | Purpose | Link |
|------|---------|------|
| testify | Assertions and test utilities | [github.com/stretchr/testify](https://github.com/stretchr/testify) |
| moq | Mock generation template | [github.com/matryer/moq](https://github.com/matryer/moq) |
| mockery | Mock generation tool | [github.com/vektra/mockery](https://github.com/vektra/mockery) |
