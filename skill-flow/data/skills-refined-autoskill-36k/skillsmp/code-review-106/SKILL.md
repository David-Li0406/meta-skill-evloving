---
name: code-review
description: Automatic code review for pull requests and commits
trigger: "review request OR pull request OR code change OR check PR"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash(git diff)
  - Bash(git log)
  - Bash(dotnet build)
---

# Automatic Code Review

Performs comprehensive code review based on project standards and best practices.

## Trigger Conditions

- Pull request created/updated
- Pre-commit hook triggered
- User requests code review
- Code changes detected

## Review Categories

### 1. Architecture Compliance

**Clean Architecture Rules:**
```
❌ Domain → Infrastructure (FORBIDDEN)
❌ Application → API (FORBIDDEN)
❌ Application → Infrastructure concrete classes (FORBIDDEN)

✅ API → Application → Domain
✅ Infrastructure implements Domain interfaces
```

**Detection:**
```bash
# Check Domain for forbidden dependencies
grep -rn "using Merge.Infrastructure" Merge.Domain/ --include="*.cs"
grep -rn "using Microsoft.EntityFrameworkCore" Merge.Domain/ --include="*.cs"
grep -rn "using Merge.API" Merge.Domain/ --include="*.cs"

# Check Application for forbidden dependencies
grep -rn "using Merge.API" Merge.Application/ --include="*.cs"
grep -rn "using Merge.Infrastructure" Merge.Application/ --include="*.cs" | grep -v "DependencyInjection"
```

**Report:**
```markdown
### Architecture Violations

❌ **CRITICAL:** Domain depends on Infrastructure
   - File: Merge.Domain/Entities/Product.cs:5
   - Issue: `using Merge.Infrastructure.Data;`
   - Fix: Remove dependency, use domain interfaces
```

### 2. DDD Pattern Compliance

**Entity Rules:**
```csharp
// ❌ BAD: Public constructor
public class Product
{
    public Product(string name) { }  // VIOLATION
}

// ✅ GOOD: Factory method
public class Product
{
    private Product() { }  // Private ctor for EF

    public static Product Create(string name)
    {
        Guard.AgainstNullOrEmpty(name, nameof(name));
        var product = new Product { Name = name };
        product.AddDomainEvent(new ProductCreatedEvent(product.Id));
        return product;
    }
}
```

**Detection:**
```bash
# Find public constructors in entities
grep -rn "public.*Entity.*\(" Merge.Domain/Entities/ --include="*.cs" | grep -v "static"

# Find public setters
grep -rn "{ get; set; }" Merge.Domain/Entities/ --include="*.cs"

# Find direct property assignments
grep -rn "entity\.Property = " --include="*.cs" | grep -v "Tests"
```

**Report:**
```markdown
### DDD Violations

⚠️ **MEDIUM:** Public setter found
   - File: Merge.Domain/Entities/Product.cs:15
   - Issue: `public string Name { get; set; }`
   - Fix: Use `{ get; private set; }` with domain method

⚠️ **MEDIUM:** Missing domain event
   - File: Merge.Domain/Entities/Order.cs:45
   - Issue: State change without event in `SetStatus()`
   - Fix: Add `AddDomainEvent(new OrderStatusChangedEvent(...))`
```

### 3. CQRS Compliance

**Command Rules:**
```csharp
// ❌ BAD: Command returns entity
public record CreateProductCommand : IRequest<Product>;

// ✅ GOOD: Command returns DTO
public record CreateProductCommand : IRequest<ProductDto>;

// ❌ BAD: Query modifies state
public class GetProductQueryHandler
{
    public async Task<ProductDto> Handle(...)
    {
        product.ViewCount++;  // VIOLATION: Query changes state
        await _unitOfWork.SaveChangesAsync();  // VIOLATION
    }
}

// ✅ GOOD: Query is read-only
public class GetProductQueryHandler
{
    public async Task<ProductDto?> Handle(...)
    {
        return await _context.Products
            .AsNoTracking()  // Read-only
            .Where(p => p.Id == request.Id)
            .ProjectTo<ProductDto>(_mapper)
            .FirstOrDefaultAsync(ct);
    }
}
```

**Detection:**
```bash
# Find queries that call SaveChanges
grep -rln "Query" Merge.Application/ --include="*.cs" | \
  xargs grep -l "SaveChanges"

# Find commands returning entities
grep -rn "IRequest<.*Entity>" Merge.Application/ --include="*.cs"
```

### 4. Security Review

**Critical Checks:**
```csharp
// ❌ CRITICAL: Hardcoded secrets
var key = "MySecretKey123";  // VIOLATION
var connectionString = "Host=localhost;Password=admin";  // VIOLATION

// ❌ CRITICAL: PII in logs
_logger.LogInformation("User email: {Email}", user.Email);  // VIOLATION
_logger.LogInformation("Processing card {CardNumber}", card.Number);  // VIOLATION

// ❌ HIGH: Missing authorization
[HttpDelete("{id}")]  // No [Authorize] attribute
public async Task<IActionResult> Delete(Guid id) { }

// ❌ HIGH: IDOR vulnerability
public async Task<OrderDto> GetOrder(Guid orderId)
{
    return await _context.Orders.FindAsync(orderId);  // No ownership check
}

// ✅ GOOD: IDOR protection
public async Task<OrderDto> GetOrder(Guid orderId)
{
    var order = await _context.Orders.FindAsync(orderId);
    if (order.UserId != _currentUser.Id && !_currentUser.IsAdmin)
        throw new ForbiddenException();
    return _mapper.Map<OrderDto>(order);
}
```

**Detection:**
```bash
# Find hardcoded secrets
grep -rn "password.*=.*\"" --include="*.cs" | grep -v "Test"
grep -rn "secret.*=.*\"" --include="*.cs" | grep -v "Test"
grep -rn "apikey.*=.*\"" --include="*.cs" -i

# Find PII in logs
grep -rn "Log.*Email\|Log.*Password\|Log.*Token\|Log.*Card" --include="*.cs"

# Find endpoints without authorization
grep -rn "\[Http" Merge.API/Controllers/ --include="*.cs" -A1 | \
  grep -v "Authorize\|AllowAnonymous"
```

### 5. Performance Review

**Database Queries:**
```csharp
// ❌ BAD: Missing AsNoTracking for read
var products = await _context.Products.ToListAsync();

// ✅ GOOD
var products = await _context.Products.AsNoTracking().ToListAsync();

// ❌ BAD: N+1 query
var orders = await _context.Orders.ToListAsync();
foreach (var order in orders)
{
    var items = order.Items;  // Lazy load = N queries
}

// ✅ GOOD: Eager load
var orders = await _context.Orders
    .Include(o => o.Items)
    .AsSplitQuery()
    .ToListAsync();

// ❌ BAD: Loading all columns
var products = await _context.Products.ToListAsync();
return products.Select(p => p.Name);

// ✅ GOOD: Projection
var names = await _context.Products
    .Select(p => p.Name)
    .ToListAsync();
```

**Detection:**
```bash
# Find queries without AsNoTracking
grep -rln "QueryHandler" Merge.Application/ --include="*.cs" | \
  xargs grep -L "AsNoTracking"

# Find potential N+1
grep -rn "foreach.*await" --include="*.cs" | grep -v "Tests"

# Find ToList without projection
grep -rn "ToListAsync\(\)" --include="*.cs" -B5 | grep -v "Select\|Project"
```

### 6. Error Handling Review

**Patterns:**
```csharp
// ❌ BAD: Catching all exceptions
catch (Exception ex)
{
    _logger.LogError("Error");
    return null;  // Swallowing exception
}

// ✅ GOOD: Specific exception handling
catch (DomainException ex)
{
    _logger.LogWarning(ex, "Domain error for {EntityId}", entityId);
    throw;  // Re-throw for global handler
}

// ❌ BAD: No validation
public async Task Handle(CreateProductCommand request)
{
    var product = Product.Create(request.Name, request.Price);  // No validation
}

// ✅ GOOD: With FluentValidation
public class CreateProductCommandValidator : AbstractValidator<CreateProductCommand>
{
    public CreateProductCommandValidator()
    {
        RuleFor(x => x.Name).NotEmpty().MaximumLength(200);
        RuleFor(x => x.Price).GreaterThan(0);
    }
}
```

### 7. Code Style Review

**C# 12 Patterns:**
```csharp
// ❌ AVOID: Traditional constructor
public class ProductService
{
    private readonly IRepository _repo;
    public ProductService(IRepository repo) { _repo = repo; }
}

// ✅ PREFER: Primary constructor
public class ProductService(IRepository repo)
{
    public async Task<Product> GetAsync(Guid id) => await repo.GetAsync(id);
}

// ❌ AVOID: new List<T>()
var items = new List<string>();

// ✅ PREFER: Collection expression
List<string> items = [];

// ❌ AVOID: Mutable DTO
public class ProductDto
{
    public Guid Id { get; set; }
}

// ✅ PREFER: Record
public record ProductDto(Guid Id, string Name, decimal Price);
```

### 8. Test Coverage Review

```bash
# Check if new code has tests
# For each new/modified file
NEW_FILE="ProductService.cs"
TEST_FILE=$(find Merge.Tests -name "*${NEW_FILE%.*}*Test*.cs" 2>/dev/null)

if [ -z "$TEST_FILE" ]; then
    echo "⚠️ Missing test file for $NEW_FILE"
fi

# Check test coverage percentage
dotnet test --collect:"XPlat Code Coverage" --results-directory ./coverage
```

## Review Output Format

```markdown
# Code Review Report

**Commit:** abc123
**Author:** developer@example.com
**Files Changed:** 5

## Summary

| Category | Issues |
|----------|--------|
| 🔴 Critical | 1 |
| 🟠 High | 2 |
| 🟡 Medium | 5 |
| 🔵 Low | 3 |

## Critical Issues

### 1. Security: Hardcoded Secret
- **File:** Merge.API/appsettings.json:15
- **Issue:** JWT secret key in configuration file
- **Fix:** Use environment variable or secrets manager
```json
// Before
"JwtSecret": "MyHardcodedSecret123"

// After
"JwtSecret": "${JWT_SECRET}"
```

## High Issues

### 2. Architecture: Domain → Infrastructure Dependency
- **File:** Merge.Domain/Entities/Product.cs:5
- **Issue:** Domain layer references Infrastructure
- **Fix:** Remove using statement, use domain interface

## Suggestions

1. Consider adding caching to `GetProductByIdQueryHandler`
2. `ProductService` class is 450 lines - consider splitting
3. Add XML documentation to public API methods

## Checklist

- [ ] All critical issues resolved
- [ ] Tests pass
- [ ] No security vulnerabilities
- [ ] Code follows project patterns
- [ ] Documentation updated (if needed)
```

## Execution Flow

```
1. Receive Code Changes (PR/Commit)
   ↓
2. Run Static Analysis
   - Architecture check
   - Security scan
   - Style check
   ↓
3. Run Dynamic Analysis
   - Build verification
   - Test execution
   ↓
4. Generate Review Report
   ↓
5. Categorize Issues by Severity
   ↓
6. Provide Fix Suggestions
   ↓
7. Output Formatted Report
```

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| 🔴 Critical | Security vulnerability, data loss risk | Block merge |
| 🟠 High | Architecture violation, breaking change | Requires fix |
| 🟡 Medium | Pattern violation, missing test | Should fix |
| 🔵 Low | Style issue, suggestion | Optional |
| ℹ️ Info | Observation, documentation | FYI |
