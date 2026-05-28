---
name: database-repository
description: Use this skill when implementing a custom repository pattern with JSON-based storage and computed columns for efficient data management.
---

# Database Repository Pattern

This skill outlines a custom repository pattern utilizing JSON storage, designed for efficient data management with computed columns.

## Pattern Overview

| Component | Description |
|-----------|-------------|
| **Entity** | Base class with WebId and audit fields. |
| **DataContext** | Query entry point with IQueryable properties. |
| **PersistenceSession** | Unit of Work for managing transactions. |
| **Repository** | Provides CRUD operations for each entity type. |

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
);

CREATE INDEX IX_Rental_ShopId_Status ON [MotoRent].[Rental]([ShopId], [Status]);
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

    public async Task<T?> LoadOneAsync<T>(Expression<Func<T, bool>> predicate) where T : Entity, new()
    {
        // Implementation for loading a single entity based on the predicate
    }
}
```

## Query Method Selection Guide

| Method | Use When | SQL Output |
|--------|----------|------------|
| `LoadAsync` | Need full entity for editing/saving | `SELECT [Id], [Json] ...` |
| `LoadOneAsync` | Need a single entity based on a condition | `SELECT [Id], [Json] ... WHERE ...` |

This skill provides a comprehensive approach to implementing a database repository pattern with JSON storage, ensuring efficient data handling and retrieval.