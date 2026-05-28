--- 
name: database-repository
description: Custom repository pattern and DataContext implementation for JSON-based storage with computed columns.
---
# Database Repository Pattern

Custom repository pattern with JSON storage, adapted from rx-erp.

## Pattern Overview

| Component | Description |
|-----------|-------------|
| **Entity** | Base class with WebId, audit fields |
| **DataContext** | Query entry point with IQueryable properties |
| **PersistenceSession** | Unit of Work for transactions |
| **Repository** | CRUD operations per entity type |

## Database Design (JSON with Computed Columns)

```sql
CREATE TABLE [MotoRent].[Rental]
(
    [RentalId] INT NOT NULL PRIMARY KEY IDENTITY(1,1),
    -- Computed columns for indexing/querying
    [Status] AS CAST(JSON_VALUE([Json], '$.Status') AS NVARCHAR(50)),
    [RenterId] AS CAST(JSON_VALUE([Json], '$.RenterId') AS INT),
    [MotorbikeId] AS CAST(JSON_VALUE([Json], '$.MotorbikeId') AS INT),
    [ShopId] AS CAST(JSON_VALUE([Json], '$.ShopId') AS INT),
    -- DO NOT use JSON_VALUE function for DATE, DATETIMEOFFSET columns
    [StartDate] AS CAST(JSON_VALUE([Json], '$.StartDate') AS DATE),
    -- USE PERSISTENT COLUMN INSTEAD
    [EndDate] DATE NULL,
    -- USE PERSISTENT COLUMN INSTEAD
    [CheckInTimestamp] DATETIMEOFFSET NULL,
    -- JSON storage
    [Json] NVARCHAR(MAX) NOT NULL,
    -- Audit columns
    [CreatedBy] VARCHAR(50) NOT NULL,
    [ChangedBy] VARCHAR(50) NOT NULL,
    [CreatedTimestamp] DATETIMEOFFSET NOT NULL,
    [ChangedTimestamp] DATETIMEOFFSET NOT NULL
)

CREATE INDEX IX_Rental_ShopId_Status ON [MotoRent].[Rental]([ShopId], [Status])
```

## Data Context Pattern

```csharp
// RentalDataContext.cs
public partial class RentalDataContext
{
    private QueryProvider QueryProvider { get; }

    public RentalDataContext() : this(ObjectBuilder.GetObject<QueryProvider>()) { }
     /// <summary>
    /// Creates a new query for the specified entity type.
    /// Preferred pattern over using Query properties directly.
    /// </summary>
    public Query<T> CreateQuery<T>() where T : Entity, new()
    {
        return new Query<T>(this.QueryProvider);
    }

    public RentalDataContext(QueryProvider provider)
    {
        this.QueryProvider = provider;
    }

    // Preferred: Use CreateQuery<T> instead of Query properties
    public Query<T> CreateQuery<T>() where T : Entity, new()
    {
        return new Query<T>(this.QueryProvider);
    }

    public async Task<T?> LoadOneAsync<T>(Expression<Func<T, bool>> predicate) where T : Entity
    {
        var query = new Query<T>(this.QueryProvider).Where(predicate);
        var repos = ObjectBuilder.GetObject<IRepository<T>>();
        return await repos.LoadOneAsync(query);
    }

    public async Task<LoadOperation<T>> LoadAsync<T>(IQueryable<T> query,
        int page = 1, int size = 40, bool includeTotalRows = false) where T : Entity
    {
        var repos = ObjectBuilder.GetObject<IRepository<T>>();
        return await repos.LoadAsync(query, page, size, includeTotalRows);
    }

    // Aggregate methods
    public async Task<int> GetCountAsync<T>(IQueryable<T> query) where T : Entity;
    public async Task<bool> ExistAsync<T>(IQueryable<T> query) where T : Entity;
    public async Task<TResult> GetSumAsync<T, TResult>(IQueryable<T> query, Expression<Func<T, TResult>> selector);
    public async Task<TResult> GetMaxAsync<T, TResult>(IQueryable<T> query, Expression<Func<T, TResult>> selector);
    public async Task<TResult> GetMinAsync<T, TResult>(IQueryable<T> query, Expression<Func<T, TResult>> selector);
    public async Task<decimal> GetAverageAsync<T>(IQueryable<T> query, Expression<Func<T, decimal>> selector);
    public async Task<TResult?> GetScalarAsync<T, TResult>(IQueryable<T> query, Expression<Func<T, TResult>> selector);
    public async Task<List<TResult>> GetDistinctAsync<T, TResult>(IQueryable<T> query, Expression<Func<T, TResult>> selector);

    public PersistenceSession OpenSession(string username = "system") => new PersistenceSession(this, username);
}
```

## Unit of Work (PersistenceSession)

```csharp
public sealed class PersistenceSession : IDisposable
{
    private RentalDataContext? m_context;
    internal ObjectCollection<Entity> AttachedCollection { get; } = [];
    internal ObjectCollection<Entity> DeletedCollection { get; } = [];

    public PersistenceSession(RentalDataContext context) => m_context = context;

    public void Attach<T>(params T[] items) where T : Entity
    {
        if (m_context == null)
            throw new ObjectDisposedException("Session has been completed");
        foreach (var item in items)
        {
            if (string.IsNullOrWhiteSpace(item.WebId))
                item.WebId = Guid.NewGuid().ToString();
            this.AttachedCollection.Add(item);
        }
    }

    public void Delete(params Entity[] entities)
    {
        if (m_context == null)
            throw new ObjectDisposedException("Session has been completed");
        this.DeletedCollection.AddRange(entities);
    }

    public async Task<SubmitOperation> SubmitChanges(string operation = "")
    {
        var so = await m_context!.SubmitChangesAsync(this, operation);
        this.AttachedCollection.Clear();
        this.DeletedCollection.Clear();
        m_context = null;
        return so;
    }

    public void Dispose() => m_context = null;
}
```

## Usage Examples

### Loading Data

```csharp
var context = new RentalDataContext();

// Load single entity
var rental = await context.LoadOneAsync<Rental>(r => r.RentalId == id);

// Load with pagination
var query = context.CreateQuery<Rental>()
    .Where(r => r.ShopId == shopId && r.Status == "Active")
    .OrderByDescending(r => r.StartDate);

var result = await context.LoadAsync(query, page: 1, size: 20, includeTotalRows: true);
var rentals = result.ItemCollection;
var totalCount = result.TotalRows;
```

### Saving Data

```csharp
// Create new rental
var rental = new Rental
{
    ShopId = shopId,
    RenterId = renterId,
    MotorbikeId = motorbikeId,
    StartDate = DateTimeOffset.Now,
    Status = "Active"
};

using var session = context.OpenSession();
session.Attach(rental);
await session.SubmitChanges("CheckIn");  // Publishes: Rental.Changed.CheckIn
```

### Update Pattern

```csharp
// Load, modify, save
var rental = await context.LoadOneAsync<Rental>(r => r.RentalId == id);
rental!.Status = "Completed";
rental.ActualEndDate = DateTimeOffset.Now;

using var session = context.OpenSession();
session.Attach(rental);
await session.SubmitChanges("CheckOut");
```

### Delete Pattern

```csharp
var rental = await context.LoadOneAsync<Rental>(r => r.RentalId == id);

using var session = context.OpenSession();
session.Delete(rental!);
await session.SubmitChanges("Delete");
```

### Aggregate Methods

Use aggregate methods instead of `LoadAsync` when you only need counts or sums:

```csharp
var context = new RentalDataContext();

// Count
var activeRentals = await context.GetCountAsync(
    context.Rentals.Where(r => r.ShopId == shopId && r.Status == "Active"));

// Exists check
var hasOverdue = await context.ExistAsync(
    context.Rentals.Where(r => r.ShopId == shopId && r.Status == "Overdue"));

// Sum
var totalRevenue = await context.GetSumAsync(
    context.Payments.Where(p => p.ShopId == shopId),
    p => p.Amount);

// Max/Min
var latestRentalDate = await context.GetMaxAsync(
    context.Rentals.Where(r => r.ShopId == shopId),
    r => r.StartDate);

// Average
var avgDailyRate = await context.GetAverageAsync(
    context.Rentals.Where(r => r.ShopId == shopId),
    r => r.DailyRate);

// Distinct values
var uniqueStatuses = await context.GetDistinctAsync(
    context.Rentals.Where(r => r.ShopId == shopId),
    r => r.Status);
```

### Using CreateQuery<T> (Preferred Pattern)

```csharp
// Instead of using Query properties:
var query = context.Rentals
    .Where(r => r.ShopId == shopId)
    .OrderByDescending(r => r.StartDate);

// Use CreateQuery<T> for better flexibility:
var query = context.CreateQuery<Rental>()
    .Where(r => r.ShopId == shopId)
    .OrderByDescending(r => r.StartDate);

var result = await context.LoadAsync(query, page: 1, size: 20);
```

### WHERE IN Queries (IsInList)

**IMPORTANT**: Due to C# 14 expression tree changes, you cannot use `.Contains()` directly in LINQ Where clauses for SQL IN translation. Use the `IsInList` extension method instead.

```csharp
using MotoRent.Domain.Extensions;

// WRONG - Does NOT translate to SQL IN clause:
var rentalIds = new[] { 1, 2, 3 };
var query = context.CreateQuery<Payment>()
    .Where(p => rentalIds.Contains(p.RentalId));  // Does NOT work!

// CORRECT - Use IsInList for SQL IN clause:
var rentalIds = new[] { 1, 2, 3 };
var query = context.CreateQuery<Payment>()
    .Where(p => rentalIds.IsInList(p.RentalId));  // Translates to: WHERE [RentalId] IN (1, 2, 3)

var result = await context.LoadAsync(query, page: 1, size: 100);
```

The `IsInList` extension method is defined in `MotoRent.Domain.Extensions.CollectionExtension`:

```csharp
namespace MotoRent.Domain.Extensions;

public static class CollectionExtension
{
    /// <summary>
    /// Checks if an item is in a list. This method is recognized by the query provider
    /// and translated to SQL IN clause. Use this instead of List.Contains() in LINQ Where clauses.
    /// </summary>
    public static bool IsInList<T>(this IEnumerable<T> list, T item)
    {
        return list.Contains(item);
    }
}
```

**Note**: For in-memory filtering (after data is loaded), you can still use `.Contains()`:
```csharp
// In-memory filtering - .Contains() is fine here:
var result = await context.LoadAsync(query, page: 1, size: 1000);
var filtered = result.ItemCollection.Where(r => rentalIds.Contains(r.RentalId)).ToList();
```

## Best Practices

| Practice | Description |
|----------|-------------|
| Short-lived sessions | Open session, do work, dispose |
| Descriptive operations | Use meaningful operation names for messaging |
| Clone for dialogs | Always clone entities before passing to edit dialogs |
| Batch related changes | Attach multiple entities in single session |
| Use aggregates for stats | Use `GetCountAsync`, `GetSumAsync` instead of loading all entities |
| CreateQuery over properties | Prefer `CreateQuery<T>()` over Query properties for flexibility |
| IsInList for WHERE IN | Use `ids.IsInList(e.Property)` for SQL IN clauses, not `.Contains()` |

## Source
- From: `E:\project\work\rx-erp` repository pattern
