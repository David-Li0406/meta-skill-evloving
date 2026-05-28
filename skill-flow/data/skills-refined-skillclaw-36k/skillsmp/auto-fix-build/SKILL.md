---
name: auto-fix-build
description: Automatically detect and fix build errors
trigger: "build fails OR compilation error OR dotnet build fails"
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash(dotnet build)
  - Bash(dotnet restore)
  - Glob
  - Grep
---

# Auto Fix Build Errors

This skill automatically activates when build errors are detected and provides intelligent fixes.

## Trigger Conditions

- `dotnet build` returns non-zero exit code
- Compilation errors in output
- CS#### error codes detected

## Error Categories & Auto-Fix Strategies

### 1. Missing Using Statements (CS0246, CS0234)

**Detection Pattern:**
```
error CS0246: The type or namespace name 'X' could not be found
error CS0234: The type or namespace name 'X' does not exist in the namespace 'Y'
```

**Auto-Fix Strategy:**
1. Identify the missing type
2. Search codebase for existing usage: `grep -rn "using.*{TypeName}" --include="*.cs"`
3. Check common namespaces:
   - System types: `System`, `System.Collections.Generic`, `System.Linq`
   - Domain types: `Merge.Domain.Entities`, `Merge.Domain.ValueObjects`
   - Application types: `Merge.Application.DTOs`, `Merge.Application.Services`
   - Infrastructure: `Microsoft.EntityFrameworkCore`
4. Add the correct using statement at the top of the file

**Common Mappings:**
```csharp
// Domain Layer
Entity → Merge.Domain.Entities
ValueObject → Merge.Domain.ValueObjects
DomainEvent → Merge.Domain.Events
Specification → Merge.Domain.Specifications
Guard → Merge.Domain.SharedKernel

// Application Layer
IRequest → MediatR
IRequestHandler → MediatR
IMapper → AutoMapper
ValidationResult → FluentValidation.Results
AbstractValidator → FluentValidation

// Infrastructure Layer
DbContext → Microsoft.EntityFrameworkCore
IConfiguration → Microsoft.Extensions.Configuration

// Common
Guid → System
Task → System.Threading.Tasks
List<> → System.Collections.Generic
CancellationToken → System.Threading
```

### 2. Missing Method Implementation (CS0535)

**Detection Pattern:**
```
error CS0535: 'X' does not implement interface member 'Y.Z'
```

**Auto-Fix Strategy:**
1. Identify the interface and missing method
2. Find interface definition: `grep -rn "interface IXxx" --include="*.cs"`
3. Read the interface to get method signature
4. Generate implementation with appropriate pattern:

```csharp
// For IRequestHandler<TRequest, TResponse>
public async Task<TResponse> Handle(TRequest request, CancellationToken cancellationToken)
{
    // TODO: Implement
    throw new NotImplementedException();
}

// For IRepository<T>
public async Task<T?> GetByIdAsync(Guid id, CancellationToken ct = default)
{
    return await _dbContext.Set<T>().FindAsync([id], ct);
}
```

### 3. Ambiguous Reference (CS0104)

**Detection Pattern:**
```
error CS0104: 'X' is an ambiguous reference between 'Y.X' and 'Z.X'
```

**Auto-Fix Strategy:**
1. Identify the conflicting types
2. Use fully qualified name for the less common one
3. Or add using alias:
```csharp
using DomainProduct = Merge.Domain.Entities.Product;
using DtoProduct = Merge.Application.DTOs.ProductDto;
```

### 4. Accessibility Errors (CS0122, CS0051)

**Detection Pattern:**
```
error CS0122: 'X' is inaccessible due to its protection level
error CS0051: Inconsistent accessibility
```

**Auto-Fix Strategy:**
1. Check if the type should be public
2. For internal types exposed in public API → make public
3. For protected members accessed externally → consider design change
4. Common fixes:
   - Entity constructors: Keep private, add factory method
   - DTO properties: Make public
   - Interface implementations: Match interface accessibility

### 5. Nullable Reference Warnings (CS8600, CS8602, CS8603, CS8618)

**Detection Pattern:**
```
error CS8618: Non-nullable property 'X' must contain a non-null value
warning CS8602: Dereference of a possibly null reference
```

**Auto-Fix Strategy:**
```csharp
// CS8618: Uninitialized non-nullable
// Before:
public string Name { get; set; }

// After (Option 1: Initialize):
public string Name { get; set; } = string.Empty;

// After (Option 2: Make nullable):
public string? Name { get; set; }

// After (Option 3: Required property):
public required string Name { get; set; }

// CS8602: Possible null dereference
// Before:
var name = user.Name.ToUpper();

// After:
var name = user.Name?.ToUpper() ?? string.Empty;
// Or with null check:
if (user.Name is not null)
{
    var name = user.Name.ToUpper();
}
```

### 6. Async/Await Issues (CS1998, CS4014)

**Detection Pattern:**
```
warning CS1998: This async method lacks 'await' operators
warning CS4014: Because this call is not awaited
```

**Auto-Fix Strategy:**
```csharp
// CS1998: No await in async method
// Option 1: Remove async if not needed
public Task<int> GetCountAsync() => Task.FromResult(42);

// Option 2: Add await
public async Task<int> GetCountAsync()
{
    return await _repository.CountAsync();
}

// CS4014: Call not awaited
// Before:
ProcessAsync(); // Fire and forget (BAD)

// After:
await ProcessAsync(); // Properly awaited

// Or if intentional fire-and-forget:
_ = ProcessAsync(); // Explicit discard
```

### 7. Type Conversion Errors (CS0029, CS0266)

**Detection Pattern:**
```
error CS0029: Cannot implicitly convert type 'X' to 'Y'
error CS0266: Cannot implicitly convert type 'X' to 'Y'. An explicit conversion exists
```

**Auto-Fix Strategy:**
```csharp
// Guid to string
var idString = id.ToString();

// string to Guid
var id = Guid.Parse(idString);
// Or safe:
if (Guid.TryParse(idString, out var id)) { }

// int to enum
var status = (OrderStatus)statusInt;

// Entity to DTO
var dto = _mapper.Map<ProductDto>(entity);

// Nullable to non-nullable
var value = nullableValue ?? defaultValue;
var value = nullableValue!; // If you're sure it's not null
```

### 8. Constructor Errors (CS1729, CS7036)

**Detection Pattern:**
```
error CS1729: 'X' does not contain a constructor that takes N arguments
error CS7036: There is no argument given that corresponds to required parameter
```

**Auto-Fix Strategy:**
1. Check the class/record definition
2. For DDD entities: Use factory method, not constructor
3. For records with primary constructor: Provide all parameters
4. For dependency injection: Register the missing service

```csharp
// Wrong: Direct construction
var product = new Product(name, price); // CS1729 if wrong params

// Correct: Factory method
var product = Product.Create(name, price, categoryId);

// For handlers with DI
public class Handler(
    IRepository<Product> repository,  // Must be registered in DI
    IUnitOfWork unitOfWork,
    IMapper mapper
) { }
```

## Execution Flow

```
1. Detect Error
   ↓
2. Parse Error Code & Message
   ↓
3. Locate File & Line
   ↓
4. Read Context (±10 lines)
   ↓
5. Identify Pattern
   ↓
6. Search Codebase for Examples
   ↓
7. Generate Fix
   ↓
8. Apply Fix
   ↓
9. Re-run Build
   ↓
10. If more errors → Loop
```

## Commands

```bash
# Run build and capture errors
dotnet build 2>&1 | tee build-output.txt

# Parse error locations
grep -E "error CS[0-9]{4}:" build-output.txt

# Find similar patterns in codebase
grep -rn "similar_code_pattern" --include="*.cs"
```

## Auto-Fix Limits

**DO Auto-Fix:**
- Missing using statements
- Simple null safety issues
- Missing interface implementations (scaffold)
- Obvious type conversions

**DO NOT Auto-Fix:**
- Architectural violations
- Business logic errors
- Security-related code
- Database migration issues

**ALWAYS:**
- Re-run build after fixes
- Report all changes made
- Stop after 3 failed attempts
- Ask user if unsure
