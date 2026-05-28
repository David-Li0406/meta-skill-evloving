---
name: code-standards
description: C# coding conventions, naming patterns, and file organization standards for the MotoRent project.
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
  - Prefix for constants is `c_` or PascalCase

## Service Injection Pattern
```csharp
// In ServicesExtensions.cs
builder.Services.AddScoped<IMotorbikeService, MotorbikeService>();
services.AddSingleton<IRepository<Motorbike>, SqlJsonRepository<Motorbike>>();
```

```csharp
// use constructor injection
// ALWAYS use "this" keyword when referencing any instance member of the current class
// ALWAYS use "base" keyword when referencing any base class member
public class MotorbikeService(RentalDataContext context) : IMotorbikeService
{
    // use private get property
    private RentalDataContext Context {get;} = context;

    public async Task DoSomethingAsync(int id)
    {
        // do NOT omit `this` keyword
        var motorbike = await this.Context.LoadOneAsync<Motorbike>(m => m.MotorbikeId == id);
        // the rest of the code

        if (SelectedShopId > 0 && rc.ShopId != SelectedShopId) // WRONG
        if (this.SelectedShopId > 0 && rc.ShopId != this.SelectedShopId) // CORRECT
    }
}
```

## Pattern Matching
```csharp
var boolVar = isTrue ? "yes" : "no";
// for a simple boolean, but when isTrue is complex expression, use pattern
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
    private const int c_maxRentalDays = 30;

    // 5. Static fields
    private static readonly JsonSerializerOptions s_options = new();

    // 6. Instance fields (m_ prefix)
    private readonly RentalDataContext m_context;
    private List<Rental> m_cachedRentals = [];

    // 7. Constructor
    public RentalService(RentalDataContext context)
    {
        m_context = context;
    }

    // 8. Properties
    public int ShopId { get; set; }

    // 9. Public methods
    public async Task<Rental?> GetRentalAsync(int id)
    {
        return await this.m_context.LoadOneAsync<Rental>(r => r.RentalId == id);
    }

    // 10. Private methods
    private void ValidateRental(Rental rental)
    {
        // ...
    }


    //  DO NOT user #region and #endregion, instead use partial class for example:
    // Rental.search.cs for search related members
    // Rental.validation.cs for validation rules etc
}


```

## Expression-Bodied Members

```csharp
// Properties
public int RentalId { get; set; }
public string FullName => $"{this.FirstName} {this.LastName}";

// Methods (single expression)
public override int GetId() => this.RentalId;
public override void SetId(int value) => this.RentalId = value;

// Methods (multiple statements - use block body)
public async Task SaveAsync()
{
    using var session = this.m_context.OpenSession();
    session.Attach(this);
    await session.SubmitChanges("Save");
}
```

## Null Handling

```csharp
// Nullable reference types (enabled in project)
public string? OptionalField { get; set; }
public string RequiredField { get; set; } = string.Empty;

// Null checks
if (rental is null)
    return;

// Pattern matching
if (rental is { Status: "Active" })
    ProcessActive(rental);

// Null coalescing
var name = rental?.RenterName ?? "Unknown";

// Null-forgiving (only when certain)
var item = list.FirstOrDefault()!;
```

## Collections

```csharp
// Use collection expressions
private List<Rental> m_rentals = [];
private Dictionary<int, Rental> m_cache = [];

// LINQ patterns
var activeRentals = this.m_rentals
    .Where(r => r.Status == "Active")
    .OrderByDescending(r => r.StartDate)
    .ToList();

// Prefer foreach for side effects
foreach (var rental in rentals)
{
    rental.Status = "Completed";
}
```

## Async/Await

```csharp
// Always use async suffix
public async Task<Rental?> LoadRentalAsync(int id)

// Always await or return
public async Task ProcessAsync()
{
    await this.DoWorkAsync();
}

// Fire and forget (rare, use with caution)
_ = Task.Run(async () => await this.BackgroundWorkAsync());

// Parallel operations
await Task.WhenAll(
    this.LoadRentalsAsync(),
    this.LoadMotorbikesAsync(),
    this.LoadRentersAsync()
);
```

## Entity Patterns

```csharp
public class Rental : Entity
{
    // Primary key
    public int RentalId { get; set; }

    // Foreign keys
    public int ShopId { get; set; }
    public int RenterId { get; set; }
    public int MotorbikeId { get; set; }

    // Required strings
    public string Status { get; set; } = "Reserved";

    // Optional strings
    public string? Notes { get; set; }

    // Dates
    public DateTimeOffset StartDate { get; set; }
    public DateTimeOffset? ActualEndDate { get; set; }

    // Money
    public decimal DailyRate { get; set; }
    public decimal TotalAmount { get; set; }

    // Entity base implementation
    public override int GetId() => this.RentalId;
    public override void SetId(int value) => this.RentalId = value;
}
```

## Blazor Components

```razor
@* Component file naming: PascalCase.razor *@
@* Code-behind: PascalCase.razor.cs *@

@page "/rentals"
@inject RentalDataContext DataContext
@inject ToastService ToastService

<MotoRentPageTitle>Rentals</MotoRentPageTitle>

@* Component markup *@

@code {
    // Fields with m_ prefix
    private List<Rental> m_rentals = [];
    private bool m_loading;

    // Lifecycle methods
    protected override async Task OnInitializedAsync()
    {
        await this.LoadDataAsync();
    }

    // Event handlers
    private async Task OnSaveClicked()
    {
        // ...
    }

    // Private methods
    private async Task LoadDataAsync()
    {
        if (this.m_loading) return; // Prevent double loading
        this.m_loading = true;
        try
        {
            var result = await this.DataContext.LoadAsync(this.DataContext.Rentals);
            this.m_rentals = result.ItemCollection.ToList();
        }
        finally
        {
            this.m_loading = false;
        }
    }
}
```

## Error Handling

```csharp
// Use try-catch for expected errors
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
    this.ToastService.ShowError("An error occurred");
}

// Throw for programming errors
if (rental is null)
    throw new ArgumentNullException(nameof(rental));
```

## Comments

```csharp
// Single-line for brief explanations
// Calculate total including insurance

/// <summary>
/// XML doc for public APIs
/// </summary>
/// <param name="rentalId">The rental identifier</param>
/// <returns>The rental or null if not found</returns>
public async Task<Rental?> GetRentalAsync(int rentalId)

// Avoid obvious comments
// BAD: Increment counter
// GOOD: (no comment needed for i++)
```

## The `this` Keyword Rule (IMPORTANT)

**Always use `this` when referencing instance members:**

```csharp
// WRONG - missing this keyword
m_loading = true;
DataContext.LoadAsync(query);
ShowSuccess("Saved");

// CORRECT - always use this
this.m_loading = true;
this.DataContext.LoadAsync(query);
this.ShowSuccess("Saved");
```

This applies to:
- Private fields (`this.m_field`)
- Properties (`this.PropertyName`)
- Methods (`this.MethodName()`)
- Injected services (`this.DataContext`, `this.DialogService`)

**Why?**
- Clearer distinction between local variables and instance members
- Prevents accidental shadowing
- Consistent with rx-erp codebase patterns
- Easier to identify dependencies in code

## Source
- Based on: `E:\project\work\rx-erp` patterns
- Microsoft C# Coding Conventions
