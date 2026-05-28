---
name: csharp-code-standards
description: Use this skill when you need to follow C# coding conventions, naming patterns, and file organization standards for the MotoRent project.
---

# Code Standards

These guidelines direct the GitHub Copilot CLI agent when analyzing or modifying C# files in MotoRent so every automated change matches human expectations.

## C# Coding Standards
- **Framework**: .NET 10
- **Language Version**: C# 14 or latest
- **Nullable Reference Types**: Enabled
- **Pattern**: Use modern C# features (pattern matching, records, init-only properties)
- **Async/Await**: Prefer async methods for I/O operations
- **Naming Conventions**:
  - PascalCase for classes, methods, properties
  - camelCase for local variables and parameters
  - Prefix interfaces with `I`
  - Prefix for private instance members is `m_`
  - Prefix for static fields is `s_`
  - Prefix for constants is `UPPERCASE_WITH_UNDERSCORES`
- **XML Comments**: Do not insert `<summary>` tags; all methods, arguments, and properties should have descriptive names.

## Service Injection Pattern
```csharp
// In ServicesExtensions.cs
builder.Services.AddScoped<IMotorbikeService, MotorbikeService>();
services.AddSingleton<IRepository<Motorbike>, SqlJsonRepository<Motorbike>>();
```

```csharp
// Use constructor injection
// ALWAYS use "this" keyword when referencing any instance member of the current class
// ALWAYS use "base" keyword when referencing any base class member
public class MotorbikeService : IMotorbikeService
{
    private RentalDataContext Context { get; }

    public MotorbikeService(RentalDataContext context)
    {
        this.Context = context;
    }

    public async Task DoSomethingAsync(int id)
    {
        // Do NOT omit `this` keyword
        var motorbike = await this.Context.LoadOneAsync<Motorbike>(m => m.MotorbikeId == id);
        // The rest of the code

        if (this.SelectedShopId > 0 && rc.ShopId != this.SelectedShopId) // CORRECT
    }
}
```

## Pattern Matching
```csharp
var boolVar = isTrue ? "yes" : "no";
// For a simple boolean, but when isTrue is a complex expression, use pattern matching
var result = someValue switch
{
    > 0 => "positive",
    < 0 => "negative",
    _ => "zero"
};
```

## File Organization
```csharp
// 1. Usings (sorted, no unnecessary)
using System.Text.Json;
using MotoRent.Domain.Entities;

// 2. Namespace
namespace MotoRent.Services;

// 3. Type declaration
public class RentalService
{
    // 4. Constants
    private const int MAX_RENTAL_DAYS = 30;

    // 5. Static fields
    private static readonly JsonSerializerOptions s_options = new();

    // 6. Instance fields (m_ prefix)
    private List<Rental> m_rentals;
}
```