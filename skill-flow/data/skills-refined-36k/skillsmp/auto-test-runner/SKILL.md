---
name: auto-test-runner
description: Automatically run relevant tests after code changes
trigger: "file saved OR code change OR pre commit OR run tests"
allowed-tools:
  - Bash(dotnet test)
  - Bash(dotnet build)
  - Glob
  - Grep
  - Read
---

# Auto Test Runner

Automatically identifies and runs relevant tests after code changes.

## Trigger Conditions

- Code file saved/modified
- Before commit operations
- After refactoring operations
- When explicitly requested

## Test Discovery Strategy

### 1. Direct Test File Mapping

```
Source File → Test File Pattern
─────────────────────────────────────────────────
Merge.Domain/Entities/Product.cs
  → Merge.Tests/Domain/Entities/ProductTests.cs
  → Merge.Tests/Unit/Domain/ProductTests.cs

Merge.Application/Products/Commands/CreateProduct/CreateProductCommandHandler.cs
  → Merge.Tests/Application/Products/Commands/CreateProductCommandHandlerTests.cs
  → Merge.Tests/Unit/Handlers/CreateProductCommandHandlerTests.cs

Merge.API/Controllers/ProductsController.cs
  → Merge.Tests/Integration/Controllers/ProductsControllerTests.cs
  → Merge.Tests/API/ProductsControllerIntegrationTests.cs
```

### 2. Search Commands

```bash
# Find test files for a source file
SOURCE_FILE="Product.cs"
find Merge.Tests -name "*${SOURCE_FILE%.*}*Tests.cs" -o -name "*${SOURCE_FILE%.*}*Test.cs"

# Find tests that reference a class
grep -rln "Product" Merge.Tests --include="*.cs"

# Find tests in specific category
grep -rln "\[Trait.*Category.*Unit\]" Merge.Tests --include="*.cs"
```

### 3. Test Categories

```csharp
// Unit Tests - Fast, isolated
[Trait("Category", "Unit")]
public class ProductTests { }

// Integration Tests - With database
[Trait("Category", "Integration")]
public class ProductRepositoryTests { }

// API Tests - Full HTTP stack
[Trait("Category", "API")]
public class ProductsControllerTests { }

// Slow Tests - Performance, load
[Trait("Category", "Slow")]
public class PerformanceTests { }
```

## Execution Strategy

### After Domain Entity Change

```bash
# Run domain unit tests
dotnet test Merge.Tests --filter "Category=Unit&FullyQualifiedName~Domain"

# Run specification tests
dotnet test Merge.Tests --filter "FullyQualifiedName~Specification"
```

### After Application Handler Change

```bash
# Run handler unit tests
dotnet test Merge.Tests --filter "Category=Unit&FullyQualifiedName~Handler"

# Run validator tests
dotnet test Merge.Tests --filter "FullyQualifiedName~Validator"
```

### After Repository Change

```bash
# Run repository integration tests
dotnet test Merge.Tests --filter "Category=Integration&FullyQualifiedName~Repository"
```

### After Controller Change

```bash
# Run API integration tests
dotnet test Merge.Tests --filter "Category=Integration&FullyQualifiedName~Controller"
```

### Before Commit (Full Suite)

```bash
# Run all unit tests first (fast)
dotnet test Merge.Tests --filter "Category=Unit" --no-build

# Then integration tests
dotnet test Merge.Tests --filter "Category=Integration" --no-build

# Skip slow tests in pre-commit
# They run in CI/CD
```

## Test Run Configuration

### Parallel Execution

```bash
# Run tests in parallel (default)
dotnet test Merge.Tests

# Limit parallelism for resource-heavy tests
dotnet test Merge.Tests --settings test.runsettings

# Sequential for debugging
dotnet test Merge.Tests -- xUnit.ParallelizeTestCollections=false
```

### Output Verbosity

```bash
# Minimal output (CI/CD)
dotnet test --verbosity minimal

# Detailed output (debugging)
dotnet test --verbosity detailed

# With console output
dotnet test --logger "console;verbosity=detailed"
```

### Specific Test Selection

```bash
# Run single test
dotnet test --filter "FullyQualifiedName=Merge.Tests.Domain.ProductTests.Create_WithValidData_ReturnsProduct"

# Run tests matching pattern
dotnet test --filter "FullyQualifiedName~Product"

# Run tests in namespace
dotnet test --filter "Namespace=Merge.Tests.Domain.Entities"

# Run by trait
dotnet test --filter "Category=Unit"

# Combine filters
dotnet test --filter "Category=Unit&FullyQualifiedName~Product"
```

## Failure Handling

### Parse Test Output

```bash
# Run and capture results
dotnet test --logger "trx;LogFileName=results.trx" 2>&1 | tee test-output.txt

# Extract failed tests
grep -A 5 "Failed" test-output.txt
```

### Common Failure Patterns

**1. Database Connection (Integration Tests)**
```
Error: Npgsql.NpgsqlException: Failed to connect
Fix: Ensure Docker containers are running
     docker-compose up -d postgres redis
```

**2. Test Isolation Issues**
```
Error: Test passed in isolation but fails in suite
Fix: Check for shared state, use fresh fixtures
     Add [Collection("Sequential")] if needed
```

**3. Async Deadlock**
```
Error: Test hangs indefinitely
Fix: Use .GetAwaiter().GetResult() sparingly
     Prefer async Task over async void
     Check for ConfigureAwait issues
```

**4. Mock Setup Issues**
```
Error: Moq.MockException: Expected invocation not performed
Fix: Verify mock setup matches actual usage
     Check parameter matchers (It.IsAny vs specific)
```

## Test Coverage

### Generate Coverage Report

```bash
# With coverlet
dotnet test Merge.Tests \
  --collect:"XPlat Code Coverage" \
  --results-directory ./coverage

# Generate HTML report
reportgenerator \
  -reports:"./coverage/**/coverage.cobertura.xml" \
  -targetdir:"./coverage/report" \
  -reporttypes:Html
```

### Coverage Thresholds

```bash
# Fail if below threshold
dotnet test Merge.Tests \
  /p:CollectCoverage=true \
  /p:Threshold=60 \
  /p:ThresholdType=line
```

## Intelligent Test Selection

### Change Impact Analysis

```
Changed File          → Tests to Run
─────────────────────────────────────────────────────
Product.cs            → ProductTests, ProductSpecTests,
                        CreateProductHandlerTests,
                        ProductRepositoryTests

IProductRepository.cs → All tests using IProductRepository
                        (search for mock setups)

ProductDto.cs         → Handler tests, Controller tests,
                        Mapping tests

appsettings.json      → Integration tests, API tests
```

### Dependency Graph

```bash
# Find what depends on changed file
grep -rln "using.*Product" --include="*.cs" | \
  xargs grep -l "class.*Tests"

# Find test files that instantiate the class
grep -rln "new Product\|Product.Create\|Mock<.*Product>" \
  Merge.Tests --include="*.cs"
```

## Execution Flow

```
1. Detect File Change
   ↓
2. Identify Changed Component
   (Entity, Handler, Repository, Controller)
   ↓
3. Find Related Test Files
   ↓
4. Determine Test Category
   (Unit, Integration, API)
   ↓
5. Run Unit Tests First
   ↓
6. If Pass → Run Integration Tests
   ↓
7. Report Results
   ↓
8. If Failures → Parse & Suggest Fixes
```

## Output Format

```markdown
## Test Results

**Changed Files:**
- Merge.Domain/Entities/Product.cs

**Tests Executed:** 15
**Passed:** 14
**Failed:** 1

### Failed Tests

1. `ProductTests.Create_WithEmptyName_ThrowsException`
   - **Error:** Expected: DomainException, Actual: No exception
   - **File:** Merge.Tests/Domain/ProductTests.cs:45
   - **Suggestion:** Add Guard.AgainstNullOrEmpty in Product.Create()

### Coverage Impact
- Product.cs: 85% → 87% (+2%)
- Overall: 62.3%
```

## Skip Conditions

**DO NOT auto-run tests when:**
- Only documentation changed (.md files)
- Only comments changed
- Git operations (merge, rebase)
- Configuration files (unless test-related)

**ALWAYS run tests when:**
- Entity/Value Object changed
- Handler/Service changed
- Repository changed
- Controller changed
- Validation rules changed
