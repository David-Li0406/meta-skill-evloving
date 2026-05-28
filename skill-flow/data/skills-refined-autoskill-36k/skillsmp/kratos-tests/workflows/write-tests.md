# Workflow: Write Tests for Existing Code

<required_reading>
**Read these reference files NOW based on what you're testing:**

For data layer (internal/data/repo/*): references/data-layer-tests.md
For biz layer (internal/biz/*): references/biz-layer-tests.md
For service layer (internal/service/*): references/service-layer-tests.md
For mapper functions: references/service-layer-tests.md (includes mapper patterns)

**Always read**: references/test-helpers.md, references/table-driven-tests.md
</required_reading>

<process>
## Step 1: Identify Service and Layer

Ask user or infer from context:
- Which microservice? (e.g., symbol-service)
- Which file to test? (e.g., internal/biz/symbols.go)
- Layer: data, biz, or service

## Step 2: Analyze Existing Test Patterns

**Read existing test files in the same service:**

```bash
# Find existing tests in the service
find {service-dir}/internal -name "*_test.go" -type f
```

For each test file found:
- Read the file to understand patterns
- Note helper function names and structures
- Identify mock patterns used
- Observe table-driven test structure
- Extract validation patterns

**Key patterns to identify:**
- How are valid domain objects created?
- How are mocks initialized?
- How are test tables structured?
- What assertions are used?
- How are errors checked?

## Step 3: Read Implementation File

Read the file you're testing to understand:
- Struct and interface definitions
- Method signatures and parameters
- Business logic and validation rules
- Dependencies (repos, use cases)
- Error returns

## Step 4: Determine Test Scope

Based on layer, decide what to test:

**Data Layer** (internal/data/repo/):
- Create, Update, FindByID, List, Delete operations
- Entity ↔ Domain transformations
- GORM error mapping
- Edge cases (nil data, empty results)

**Biz Layer** (internal/biz/):
- Use case methods
- Domain validation
- Business logic
- Error handling

**Service Layer** (internal/service/):
- gRPC/HTTP handlers
- Proto ↔ Domain mapping
- Request validation
- Response formatting

## Step 5: Generate Test Helpers

Create helpers matching existing patterns in the service:

**For data layer:**
```go
func setupTestDB(t *testing.T) *gorm.DB
func cleanupDB(db *gorm.DB)
func validDomainX() *biz.X
func validEntityX() *model.X
type mockTransaction struct{}
```

**For biz layer:**
```go
type MockXRepo struct { mock.Mock }
func setupXUseCase(mockRepo *MockXRepo) XUseCase
func validX() *X
```

**For service layer:**
```go
type mockXUseCase struct { mock.Mock }
func validX() *X
```

## Step 6: Generate Test Cases

For each method/function, create table-driven tests:

**Standard test table structure:**
```go
tests := []struct {
    name        string
    input       InputType
    setup       func(deps)
    wantErr     bool
    checkError  func(*testing.T, error)
    checkResult func(*testing.T, ResultType)
}{
    // Test cases
}
```

**Comprehensive scenarios:**
1. **Happy path**: Valid inputs, successful operation
2. **Validation errors**: Invalid/missing required fields
3. **Edge cases**: Nil values, empty data, boundaries
4. **Repository/database errors**: Not found, duplicate, connection errors

## Step 7: Write Test File

Create test file following this structure:

```go
package {package}

import (
    "context"
    "testing"
    // ... other imports matching existing tests

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

// Test helpers first
// Mocks second
// Test functions last
```

**Follow existing test file organization in the service.**

## Step 8: Verify Imports

Ensure all imports are correct:
- Internal packages use full path (e.g., `symbol-service/internal/biz`)
- External packages include version if needed
- testify/assert and testify/mock for all tests
- GORM/SQLite only for data layer tests

## Step 9: Write and Save

Write the complete test file to `{original-filename}_test.go` in the same directory.

## Step 10: Validate Tests

Run tests to verify they work:

```bash
cd {service-directory}
make test
```

If tests fail:
- Read error output carefully
- Fix import paths
- Fix mock setup
- Fix assertion logic
- Re-run until all pass

## Step 11: Check Coverage (Optional)

Generate coverage report:

```bash
cd {service-directory}
make coverage
```

Review coverage.html to verify comprehensive coverage.
</process>

<success_criteria>
This workflow is complete when:
- [ ] Existing test patterns analyzed and understood
- [ ] Implementation file read and scoped
- [ ] Test helpers generated matching service patterns
- [ ] Comprehensive test cases written (happy path, validation, edge cases, errors)
- [ ] Test file written to correct location
- [ ] Imports verified and correct
- [ ] `make test` passes successfully
- [ ] All mocks have AssertExpectations called
- [ ] Tests follow table-driven pattern
</success_criteria>