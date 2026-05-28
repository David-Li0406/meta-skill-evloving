---
name: tdd-workflow
description: Test-Driven Development workflow for .NET. Use when implementing features, fixing bugs, or writing new code. Guides RED-GREEN-REFACTOR cycle with proper test design.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Test-Driven Development Workflow

## The TDD Cycle: RED-GREEN-REFACTOR

```
    ┌─────────────────────────────────────┐
    │                                     │
    │   ┌─────┐    ┌───────┐    ┌─────┐  │
    │   │ RED │───▶│ GREEN │───▶│REFAC│──┘
    │   └─────┘    └───────┘    └─────┘
    │     │                        │
    │     │    Write failing test  │
    │     │                        │
    │     ▼                        │
    │   Make it pass (minimal)     │
    │                              │
    └──────────────────────────────┘
              Improve design
```

## Phase 1: RED - Write a Failing Test

### Rules for RED Phase
1. Write ONE test that fails
2. Test must fail for the RIGHT reason
3. Test must be meaningful and specific
4. Run the test to confirm it fails

### Test Naming Convention
```
{MethodUnderTest}_{Scenario}_{ExpectedBehavior}
```

**Examples:**
- `CreateOrder_WithValidItems_ReturnsOrder`
- `GetUser_WhenNotFound_ThrowsNotFoundException`
- `CalculateTotal_WithDiscount_AppliesCorrectPercentage`

### AAA Pattern (Arrange-Act-Assert)
```csharp
[Fact]
public void MethodName_Scenario_ExpectedResult()
{
    // Arrange - Set up preconditions
    var sut = new SystemUnderTest();
    var input = CreateValidInput();

    // Act - Execute the behavior
    var result = sut.Execute(input);

    // Assert - Verify outcome
    Assert.Equal(expected, result);
}
```

### Test Categories
```csharp
// Unit Test - Tests single unit in isolation
[Fact]
public void Calculator_Add_ReturnsSumOfNumbers() { }

// Integration Test - Tests component interaction
[Fact]
public void OrderService_CreateOrder_PersistsToDatabase() { }

// Acceptance Test - Tests user scenarios
[Fact]
public void User_CanCompleteCheckout_WithValidCart() { }
```

## Phase 2: GREEN - Make It Pass

### Rules for GREEN Phase
1. Write MINIMAL code to pass the test
2. Do NOT add extra features
3. Do NOT optimize yet
4. It's okay to be "ugly" - we'll fix it in REFACTOR
5. Run tests to confirm they pass

### The Simplest Thing That Works
```csharp
// BAD - Over-engineering in GREEN phase
public decimal CalculateDiscount(Order order)
{
    var strategy = _discountStrategyFactory.Create(order.CustomerType);
    return strategy.Calculate(order, _configService.GetDiscountRules());
}

// GOOD - Minimal implementation for GREEN
public decimal CalculateDiscount(Order order)
{
    return order.Total * 0.1m; // 10% discount
}
```

### Fake It Till You Make It
```csharp
// Test expects specific value
[Fact]
public void GetGreeting_ReturnsHello()
{
    var result = greeter.GetGreeting();
    Assert.Equal("Hello", result);
}

// GREEN: Just return what the test expects
public string GetGreeting() => "Hello";
```

## Phase 3: REFACTOR - Improve Design

### Rules for REFACTOR Phase
1. Tests MUST stay green
2. Improve structure, not behavior
3. Apply SOLID principles
4. Remove duplication (DRY)
5. Simplify (KISS)
6. Remove unused code (YAGNI)

### Refactoring Checklist
- [ ] Extract methods for clarity
- [ ] Rename for intent
- [ ] Remove duplication
- [ ] Apply design patterns if needed
- [ ] Check for SOLID violations
- [ ] Run tests after each change

### Common Refactorings
```csharp
// Before: Long method
public void ProcessOrder(Order order)
{
    // 50 lines of mixed concerns
}

// After: Single responsibility
public void ProcessOrder(Order order)
{
    ValidateOrder(order);
    CalculateTotals(order);
    ApplyDiscounts(order);
    PersistOrder(order);
    NotifyCustomer(order);
}
```

## Test Doubles

### Types of Test Doubles
```csharp
// Dummy - Passed but never used
var dummyLogger = new Mock<ILogger>().Object;

// Stub - Provides canned answers
var stubRepo = new Mock<IUserRepository>();
stubRepo.Setup(r => r.GetById(1)).Returns(new User { Id = 1 });

// Spy - Records interactions
var spyNotifier = new SpyNotifier();
service.Execute();
Assert.True(spyNotifier.WasCalled);

// Mock - Verifies interactions
var mockNotifier = new Mock<INotifier>();
service.Execute();
mockNotifier.Verify(n => n.Send(It.IsAny<Message>()), Times.Once);

// Fake - Working implementation (in-memory)
var fakeRepo = new InMemoryUserRepository();
```

### When to Use What
| Double | Use When |
|--------|----------|
| Dummy | Parameter required but unused |
| Stub | Need controlled return values |
| Spy | Need to verify calls were made |
| Mock | Need to verify specific interactions |
| Fake | Need realistic behavior without dependencies |

## Test Organization

### Project Structure
```
src/
├── MyApp.Domain/
│   └── Entities/
├── MyApp.Application/
│   └── Services/
└── MyApp.Infrastructure/
    └── Repositories/

tests/
├── MyApp.Domain.Tests/
│   └── Entities/
├── MyApp.Application.Tests/
│   └── Services/
└── MyApp.Integration.Tests/
    └── Repositories/
```

### Test Class Structure
```csharp
public class OrderServiceTests
{
    private readonly Mock<IOrderRepository> _mockRepository;
    private readonly Mock<INotificationService> _mockNotifier;
    private readonly OrderService _sut;

    public OrderServiceTests()
    {
        _mockRepository = new Mock<IOrderRepository>();
        _mockNotifier = new Mock<INotificationService>();
        _sut = new OrderService(_mockRepository.Object, _mockNotifier.Object);
    }

    [Fact]
    public void CreateOrder_WithValidData_PersistsOrder() { }

    [Fact]
    public void CreateOrder_WithInvalidData_ThrowsValidationException() { }
}
```

## Anti-Patterns to Avoid

### Test Smells
```csharp
// BAD: Testing implementation details
Assert.Equal(3, order.Items.Count);

// GOOD: Testing behavior
Assert.True(order.HasItems);

// BAD: Multiple assertions testing different behaviors
[Fact]
public void Order_Tests()
{
    Assert.NotNull(order.Id);
    Assert.Equal("Pending", order.Status);
    Assert.True(order.Total > 0);
}

// GOOD: One logical assertion per test
[Fact]
public void NewOrder_HasPendingStatus()
{
    Assert.Equal(OrderStatus.Pending, order.Status);
}

// BAD: Tests depending on order
[Fact]
public void Test1_CreateUser() { } // Creates user
[Fact]
public void Test2_GetUser() { }    // Assumes user exists

// GOOD: Independent tests
[Fact]
public void GetUser_WhenExists_ReturnsUser()
{
    var user = CreateUser(); // Arrange includes setup
    var result = _sut.GetUser(user.Id);
    Assert.NotNull(result);
}
```

## Quick Reference

### TDD Commands
```bash
# Run all tests
dotnet test

# Run with coverage
dotnet test /p:CollectCoverage=true

# Run specific test
dotnet test --filter "FullyQualifiedName~OrderServiceTests"

# Watch mode
dotnet watch test
```

### Test Attributes
```csharp
[Fact]              // Single test case
[Theory]            // Parameterized test
[InlineData(1, 2)]  // Test data
[Trait("Category", "Unit")] // Categorization
[Skip("Reason")]    // Skip test
```

See [patterns.md](patterns.md) for advanced testing patterns.
