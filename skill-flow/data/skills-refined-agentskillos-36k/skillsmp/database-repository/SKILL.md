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

## RentalDataContext Structure

The `RentalDataContext` is split into partial classes by logical function:

| File | Purpose |
|------|---------|
| `RentalDataContext.cs` | Core: constructor, CreateQuery, OpenSession |
| `RentalDataContext.Load.cs` | Loading: LoadOneAsync, LoadAsync |
| `RentalDataContext.Aggregate.cs` | Aggregates: Count, Sum, Max, Min, Average, Scalar, Distinct |
| `RentalDataContext.GroupBy.cs` | Group By: GetGroupByCountAsync, GetGroupBySumAsync |
| `RentalDataContext.List.cs` | Lists: GetListAsync (tuples, DataMap), GetReaderAsync |
| `RentalDataContext.Persistence.cs` | Persistence: SubmitChanges, CRUD operations |

## Query Method Selection Guide

| Method | Use When | SQL Output |
|--------|----------|------------|
| `LoadAsync` | Need full entity for editing/saving | `SELECT [Id], [Json] ...` |
| `LoadOneAsync` | Need single entity with all properties | `SELECT TOP 1 [Id], [Json] ...` |
| `GetListAsync` (DataMap) | Display list/table, dropdowns (N columns) | `SELECT [Col1], [Col2], ... [ColN]` |
| `GetListAsync` (Tuple) | Need 2-3 specific columns as tuples | `SELECT [Col1], [Col2]` |
| `GetCountAsync` | Count matching entities | `SELECT COUNT(*)` |
| `GetSumAsync` | Sum a column | `SELECT SUM([Column])` |
| `GetGroupByCountAsync` | Count grouped by key | `SELECT [Key], COUNT(*) GROUP BY [Key]` |
| `GetGroupBySumAsync` | Sum grouped by key(s) | `SELECT [Key], SUM([Val]) GROUP BY [Key]` |

### Performance Guidelines

- **AVOID**: Using `LoadAsync` just to display a list of names/IDs
- **PREFER**: `GetListAsync` with field selectors for read-only displays
- **PREFER**: `GetGroupByCountAsync` / `GetGroupBySumAsync` for dashboard stats
- **REASON**: Reduces SQL bytes transferred and eliminates JSON deserialization

## Usage Examples

### Loading Data

```csharp
var context = new RentalDataContext();

// Load single entity
var rental = await context.LoadOneAsync<Rental>(r => r.RentalId == id);

// Load with pagination
var query = context.CreateQuery<Rental>()
    .Where(r => r.ShopId == shopId)
    .Where(r => r.Status == "Active")
    .OrderByDescending(r => r.StartDate);

var result = await context.LoadAsync(query, page: 1, size: 20, includeTotalRows: true);
var rentals = result.ItemCollection;
var totalCount = result.TotalRows;
```

### Aggregate Methods

Use aggregate methods instead of `LoadAsync` when you only need counts or sums:

```csharp
var context = new RentalDataContext();

// Count
var activeRentals = await context.GetCountAsync<Rental>(
    r => r.ShopId == shopId && r.Status == RentalStatus.Active);

// Exists check
var query = context.CreateQuery<Rental>()
    .Where(r => r.ShopId == shopId)
    .Where(r => r.Status == RentalStatus.Overdue);
var hasOverdue = await context.ExistAsync(query);

// Sum
var totalRevenue = await context.GetSumAsync<Payment, decimal>(
    p => p.ShopId == shopId,
    p => p.Amount);

// Max/Min
var latestRentalDate = await context.GetMaxAsync<Rental, DateOnly>(
    r => r.ShopId == shopId,
    r => r.StartDate);

// Average
var avgDailyRate = await context.GetAverageAsync(
    context.CreateQuery<Rental>().Where(r => r.ShopId == shopId),
    r => r.DailyRate);

// Distinct values
var uniqueStatuses = await context.GetDistinctAsync<Rental, RentalStatus>(
    r => r.ShopId == shopId,
    r => r.Status);
```

### Group By Aggregations

Use `GetGroupByCountAsync` and `GetGroupBySumAsync` for dashboard statistics:

```csharp
var context = new RentalDataContext();

// Count by status (e.g., for dashboard pie chart)
var rentalsByStatus = await context.GetGroupByCountAsync<Rental, RentalStatus>(
    r => r.ShopId == shopId,
    r => r.Status);
// Returns: [(Active, 15), (Completed, 42), (Cancelled, 3)]

// Sum revenue by payment method
var revenueByMethod = await context.GetGroupBySumAsync<Payment, PaymentMethod, decimal>(
    p => p.ShopId == shopId && p.PaymentDate >= startDate,
    p => p.PaymentMethod,
    p => p.Amount);
// Returns: [(Cash, 50000), (Card, 35000), (PromptPay, 12000)]

// Sum revenue by shop and payment method (two keys)
var query = context.CreateQuery<Payment>()
    .Where(p => p.PaymentDate >= startDate);
var revenueByShopAndMethod = await context.GetGroupBySumAsync<Payment, int, PaymentMethod, decimal>(
    query,
    p => p.ShopId,
    p => p.PaymentMethod,
    p => p.Amount);
// Returns: [(1, Cash, 25000), (1, Card, 15000), (2, Cash, 25000), ...]
```

### DataMap Pattern (Performance Optimized)

For read-only displays, use `GetListAsync` with field selectors to get `DataMap<T>[]`:

```csharp
var context = new RentalDataContext();
var query = context.CreateQuery<TillSession>()
    .Where(t => t.Status == TillSessionStatus.Open);

// For read-only list display - only fetches specified columns
var results = await context.GetListAsync(query,
    t => t.TillSessionId,
    t => t.ShopId,
    t => t.StaffUserName,
    t => t.OpenedAt);

foreach (var row in results)
{
    var id = row.GetValue(t => t.TillSessionId);
    var shopId = row.GetValue(t => t.ShopId);
    var staff = row.GetValue(t => t.StaffUserName);
    var opened = row.GetValue(t => t.OpenedAt);
}

// For editing - use LoadOneAsync to get full entity
var session = await context.LoadOneAsync<TillSession>(t => t.TillSessionId == id);
session.ClosedAt = DateTimeOffset.Now;
// ... save
```

### Tuple-based Lists (2-3 Columns)

For simple lookups with 2-3 columns:

```csharp
// Get (Id, Name) pairs for dropdown
var shopList = await context.GetListAsync<Shop, int, string>(
    s => s.IsActive,
    s => s.ShopId,
    s => s.Name);

// Get (Id, Name, Status) tuples
var vehicleList = await context.GetListAsync<Vehicle, int, string, VehicleStatus>(
    v => v.ShopId == shopId,
    v => v.VehicleId,
    v => v.LicensePlate,
    v => v.Status);
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
    Status = RentalStatus.Active
};

using var session = context.OpenSession("username");
session.Attach(rental);
await session.SubmitChanges("CheckIn");
```

### Update Pattern

```csharp
// Load, modify, save
var rental = await context.LoadOneAsync<Rental>(r => r.RentalId == id);
rental!.Status = RentalStatus.Completed;
rental.ActualEndDate = DateTimeOffset.Now;

using var session = context.OpenSession("username");
session.Attach(rental);
await session.SubmitChanges("CheckOut");
```

### Delete Pattern

```csharp
var rental = await context.LoadOneAsync<Rental>(r => r.RentalId == id);

using var session = context.OpenSession("username");
session.Delete(rental!);
await session.SubmitChanges("Delete");
```

### WHERE IN Queries (IsInList)

**IMPORTANT**: Use the `IsInList` extension method for SQL IN translation.

```csharp
using MotoRent.Domain.Extensions;

// CORRECT - Use IsInList for SQL IN clause:
var rentalIds = new[] { 1, 2, 3 };
var query = context.CreateQuery<Payment>()
    .Where(p => rentalIds.IsInList(p.RentalId));  // Translates to: WHERE [RentalId] IN (1, 2, 3)

var result = await context.LoadAsync(query, page: 1, size: 100);
```

## Best Practices

| Practice | Description |
|----------|-------------|
| Short-lived sessions | Open session, do work, dispose |
| Descriptive operations | Use meaningful operation names for messaging |
| Clone for dialogs | Always clone entities before passing to edit dialogs |
| Batch related changes | Attach multiple entities in single session |
| Use aggregates for stats | Use `GetCountAsync`, `GetSumAsync` instead of loading all entities |
| Use GroupBy for dashboards | Use `GetGroupByCountAsync`, `GetGroupBySumAsync` for grouped stats |
| CreateQuery over properties | Prefer `CreateQuery<T>()` over Query properties for flexibility |
| IsInList for WHERE IN | Use `ids.IsInList(e.Property)` for SQL IN clauses, not `.Contains()` |
| DataMap for lists | Use `GetListAsync` with field selectors for read-only displays |

## Source
- From: `E:\project\work\rx-erp` repository pattern
