---
name: testing
description: Write tests using TDD principles with integration tests as default and minimal mocking. Use when writing code, fixing bugs, or when user mentions tests, TDD, unit tests, integration tests, or testing strategy.
---

# Testing Skill

Guide test-driven development with a pragmatic approach: integration tests by default, real dependencies over mocks, and just enough tests for confidence.

## Your Role: Test-First Engineer

You write tests before code and choose the right test type. You:

✅ **Write tests first** - TDD always, no code without tests
✅ **Default to integration** - Touch real boundaries
✅ **Use real dependencies** - Databases, filesystems, APIs
✅ **Avoid mock overuse** - Fakes over mocks, 2-mock ceiling
✅ **Test behaviors** - Not implementation details

❌ **Do NOT mock everything** - The mockist trap
❌ **Do NOT split artificially** - Related behaviors in one test
❌ **Do NOT skip tests** - Every change needs a test

## Core Principles

### Less Is More, But Enough
Write minimum tests that give you confidence. Don't split tests artificially (test_status, test_data, test_persistence), but don't combine unrelated behaviors either.

**✅ GOOD:** One test verifying status, data transformation, and persistence for a single operation
**❌ BAD:** Three separate tests for the same operation's different aspects

### Integration by Default
Unless you have a clear reason for unit testing, write integration tests.

**✅ GOOD:** Test calling actual CLI binary with real filesystem
**❌ BAD:** Unit test with 5 mocks simulating the world

### The Mock Trap
All mocks = testing nothing. You're only verifying mock wiring, not real behavior.

**✅ GOOD:** In-memory SQLite database with real queries
**❌ BAD:** Mock database that returns canned responses

### Fakes Over Mocks
Use in-memory implementations that behave like real dependencies.

**✅ GOOD:** `InMemoryRepository`, `FakeFileSystem`, stub data
**❌ BAD:** Full mock verifying call sequences

### Two-Mock Ceiling
If you need >2 mocks, write an integration test instead.

## Decision Logic

Use this flowchart to choose test type:

```
Pure function, no dependencies
   → Unit test, no mocks needed

Class with DI and 1-2 simple dependencies
   → Unit test with fakes/stubs

Touches database/API/filesystem
   → Integration test with real resources

CLI command
   → Integration test calling actual binary

Would require >2 mocks
   → Integration test

Unsure
   → Integration test
```

## Test Types

### Unit Tests

**When:** Component supports DI and you can substitute dependencies meaningfully.

**Approach:**
- Prefer fakes (in-memory implementations)
- Use stubs for canned data
- Mocks as last resort
- Never exceed 2 mocks

**Example:**
```go
// ✅ GOOD: Fake repository
type InMemoryUserRepo struct {
    users map[string]User
}

func TestUserService_CreateUser(t *testing.T) {
    repo := NewInMemoryUserRepo()
    service := NewUserService(repo)

    user, err := service.CreateUser("alice")

    assert.NoError(t, err)
    assert.Equal(t, "alice", user.Name)
    assert.NotEmpty(t, user.ID)
}
```

```go
// ❌ BAD: Everything mocked
func TestUserService_CreateUser_Mockist(t *testing.T) {
    mockRepo := new(MockUserRepo)
    mockValidator := new(MockValidator)
    mockLogger := new(MockLogger)
    mockMetrics := new(MockMetrics)

    mockRepo.On("Save", mock.Anything).Return(nil)
    mockValidator.On("Validate", mock.Anything).Return(nil)
    mockLogger.On("Info", mock.Anything)
    mockMetrics.On("Increment", "users.created")

    service := NewUserService(mockRepo, mockValidator, mockLogger, mockMetrics)
    service.CreateUser("alice")

    mockRepo.AssertExpectations(t)
    // Testing mock wiring, not behavior!
}
```

### Integration Tests

**When:** Default choice. Always prefer unless unit test is clearly better.

**Approach:**
- Use real databases (SQLite in-memory, testcontainers)
- Use real APIs (test/sandbox environments)
- Use real filesystem operations
- Only mock when explicitly requested
- Touch outer edges (near main() or entry point)

**Example - CLI Application:**
```go
func TestCLI_GenerateUUID(t *testing.T) {
    // Build actual binary
    binary := buildTestBinary(t)

    // Run with real arguments
    cmd := exec.Command(binary, "uuid", "generate")
    output, err := cmd.CombinedOutput()

    // Verify everything
    assert.NoError(t, err)
    assert.Equal(t, 0, cmd.ProcessState.ExitCode())

    uuid := strings.TrimSpace(string(output))
    assert.Regexp(t, `^[0-9a-f]{8}-[0-9a-f]{4}-`, uuid)
}
```

**Example - Database Operation:**
```go
func TestUserRepo_CreateAndFind(t *testing.T) {
    // Real in-memory SQLite
    db := setupTestDB(t)
    defer db.Close()

    repo := NewUserRepo(db)

    // Create
    user := User{Name: "alice", Email: "alice@example.com"}
    err := repo.Create(user)
    assert.NoError(t, err)

    // Find
    found, err := repo.FindByEmail("alice@example.com")
    assert.NoError(t, err)
    assert.Equal(t, "alice", found.Name)
}
```

## Acceptable Mock Scenarios

Only mock in these cases:

**Third-party APIs you don't control**
- Payment gateways, external SaaS
- Use thin wrapper you control

**Time-dependent behavior**
- Clock/date functions
- Use time provider interface

**Non-deterministic operations**
- Random, UUIDs
- Inject generator

**Hard-to-reproduce errors**
- Network timeouts, disk full
- Test error paths specifically

**Prefer thin wrappers:**
```go
// ✅ GOOD: Controllable wrapper
type Clock interface {
    Now() time.Time
}

type SystemClock struct{}
func (SystemClock) Now() time.Time { return time.Now() }

type FixedClock struct{ t time.Time }
func (f FixedClock) Now() time.Time { return f.t }

// Test with fixed time
func TestScheduler(t *testing.T) {
    clock := FixedClock{time.Date(2025, 1, 1, 0, 0, 0, 0, time.UTC)}
    scheduler := NewScheduler(clock)
    // ...
}
```

## Test Structure

One test can verify multiple related behaviors. Assert on status, data transformation, persistence, and side effects when they're part of the same operation.

**✅ GOOD: Single coherent test**
```go
func TestArticlePublish(t *testing.T) {
    repo := NewInMemoryArticleRepo()
    service := NewArticleService(repo)

    article, err := service.Publish("Title", "Content", "alice")

    // Status
    assert.NoError(t, err)
    assert.Equal(t, StatusPublished, article.Status)

    // Data transformation
    assert.Equal(t, "title", article.Slug)
    assert.NotZero(t, article.PublishedAt)

    // Persistence
    found, _ := repo.FindBySlug("title")
    assert.Equal(t, article.ID, found.ID)

    // Side effects (if part of publish operation)
    assert.Equal(t, 1, article.Version)
}
```

**❌ BAD: Artificial splitting**
```go
func TestArticlePublish_Status(t *testing.T) { /* ... */ }
func TestArticlePublish_Slug(t *testing.T) { /* ... */ }
func TestArticlePublish_Persistence(t *testing.T) { /* ... */ }
func TestArticlePublish_Version(t *testing.T) { /* ... */ }
// These are all testing the same operation!
```

## TDD Workflow

**Write failing test** - Red
**Make it pass** - Green
**Refactor** - Clean
**Repeat**

When given a request:
- Write test first
- Verify it fails
- Implement code
- Verify it passes
- Refactor if needed

When making a change:
- Write test for new behavior
- Verify existing tests still pass
- Implement change
- All tests green

## Common Pitfalls

**❌ Mistake:** Mocking everything because "unit tests are faster"
**✅ Solution:** Integration tests with real resources are fast enough and test real behavior

**❌ Mistake:** Testing implementation details (private methods, internal state)
**✅ Solution:** Test public API and observable behavior

**❌ Mistake:** One assertion per test
**✅ Solution:** Assert on all relevant aspects of the operation

**❌ Mistake:** Writing tests after code
**✅ Solution:** TDD always - test first, code second

**❌ Mistake:** Skipping tests for "simple" changes
**✅ Solution:** Every change needs a test, no exceptions

## Checklist

Before writing code:
- [ ] Test written first
- [ ] Test type chosen (integration by default)
- [ ] Using real dependencies (or fakes if unit test)
- [ ] Mock count ≤2 (or integration test instead)
- [ ] Testing behavior, not implementation
- [ ] Test fails before implementation

After implementation:
- [ ] Test passes
- [ ] Related behaviors tested together
- [ ] Error cases covered
- [ ] No artificial test splitting
- [ ] Code refactored if needed
