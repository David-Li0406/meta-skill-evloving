---
name: csharp-code-standards
description: Use this skill for C# coding conventions, naming patterns, and file organization standards in the MotoRent project.
---

# Code Standards

These guidelines direct the GitHub Copilot CLI agent when analyzing or modifying C# files in MotoRent to ensure every automated change matches human expectations.

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
  - Prefix for constants is UPPERCASE_WITH_UNDERSCORES
- **XML Comments**: Avoid inserting `<summary>` for all methods; ensure method names and parameters are descriptive.

## Service Injection Pattern
```csharp
// In ServicesExtensions.cs
builder.Services.AddScoped<IMotorbikeService, MotorbikeService>();
services.AddSingleton<IRepository<Motorbike>, SqlJsonRepository<Motorbike>>();
```

```csharp
// Use constructor injection
public class MotorbikeService : IMotorbikeService
{
    private RentalDataContext Context { get; }

    public MotorbikeService(RentalDataContext context)
    {
        this.Context = context;
    }

    public async Task DoSomethingAsync(int id)
    {
        var motorbike = await this.Context.LoadOneAsync<Motorbike>(m => m.MotorbikeId == id);
        // Additional code...
    }
}
```

## Pattern Matching
```csharp
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
    private List<Rental> m_cachedRentals = [];

    // 7. Properties
    public int ShopId { get; set; }

    // 8. Public methods
    public async Task<Rental?> GetRentalAsync(int id)
    {
        return await this.Context.LoadOneAsync<Rental>(r => r.RentalId == id);
    }

    // 9. Private methods
    private void ValidateRental(Rental rental)
    {
        // Validation logic...
    }
}
```

## Partial Class File Splitting (NO #region)
**NEVER use `#region` and `#endregion`** - instead, split large classes into partial class files.

### Naming Convention
```
ClassName.<lowercase_section_name>.cs
```

### Examples
For a service class with logical sections:
```
RentalService.cs              # Core: constructor, properties, DTOs
RentalService.validation.cs    # Validation rules
RentalService.search.cs        # Search/query helpers
```

### Structure of Partial Files
Each partial file should:
1. Have its own usings (only what's needed for that file)
2. Include a summary comment describing the section
3. Contain logically related methods

## Expression-Bodied Members
```csharp
// Properties
public int RentalId { get; set; }
public string FullName => $"{this.FirstName} {this.LastName}";

// Methods (single expression)
public override int GetId() => this.RentalId;
```

## Null Handling
```csharp
public string? OptionalField { get; set; }
public string RequiredField { get; set; } = string.Empty;

if (rental is null)
    return;

if (shop is { IsActive: true }) // Correct
```

## Collections
```csharp
private List<Rental> Rentals { get; } = [];
private Dictionary<int, Rental> Cache { get; } = [];

// LINQ patterns
var activeRentals = this.Rentals
    .Where(r => r.Status == "Active")
    .OrderByDescending(r => r.StartDate)
    .ToList();
```

## Async/Await
```csharp
public async Task<Rental?> LoadRentalAsync(int id)
{
    await this.DoWorkAsync();
}
```

## Entity Patterns
```csharp
public class Rental : Entity
{
    public int RentalId { get; set; }
    public int ShopId { get; set; }
    public string Status { get; set; } = "Reserved";
}
```

## Error Handling
```csharp
try
{
    await this.ProcessRentalAsync(rental);
}
catch (ValidationException ex)
{
    this.ToastService.ShowWarning(ex.Message);
}
catch (Exception ex)
{
    this.Logger.LogError(ex, "Failed to process rental {RentalId}", rental.RentalId);
    throw;
}
```

## Comments
```csharp
// Single-line for brief explanations
// Calculate total including insurance

/// <summary>
/// XML doc for public APIs
/// </summary>
public async Task<Rental?> GetRentalAsync(int rentalId)
```

## The `this` Keyword Rule (IMPORTANT)
**Always use `this` when referencing instance members:**
```csharp
this.m_loading = true;
this.DataContext.LoadAsync(query);
```

## Source
- Based on: `E:\project\work\rx-erp` patterns
- Microsoft C# Coding Conventions

## Blazor & Razor files
Use blazor development skill and CSS styling skill.

## Data Access and Persistence
Database-repository **MUST** be observed for tenant data access and persistence.