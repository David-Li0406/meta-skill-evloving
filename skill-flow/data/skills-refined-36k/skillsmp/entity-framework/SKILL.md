---
name: entity-framework
description: Data access patterns, GUID primary keys, JSON configuration, entity configuration, and transaction handling for PostgreSQL. Use this skill when working with Entity Framework Core and database operations.
---

# Entity Framework Core Patterns

## Data Access Patterns

- MUST use repository and unit of work patterns for data access abstraction
- MUST use eager loading with `Include()` to prevent N+1 query problems
- MUST apply `AsNoTracking()` for read-only queries to optimize performance
- MUST configure entities using Fluent API (AVOID data annotations)
- SHOULD implement compiled queries for frequently executed operations

---

## GUID Primary Keys

**MUST use `Guid.CreateVersion7()` for all GUID generation** (NOT `Guid.NewGuid()`)

**Why Version 7 GUIDs?**
- Time-ordered (sequential) - better database performance
- Improved indexing and clustering in PostgreSQL
- Reduces index fragmentation
- Better page splits behavior

**Entity Configuration**:
```csharp
public class ApplicationUser
{
    public Guid Id { get; init; }  // Don't set default value here
    // ... other properties
}

// In entity configuration
builder.HasKey(x => x.Id);
builder.Property(x => x.Id).ValueGeneratedNever();  // Application controls GUID generation
```

**Creating Entities**:
```csharp
// ✅ CORRECT: Use CreateVersion7()
var user = new ApplicationUser
{
    Id = Guid.CreateVersion7(),  // Time-ordered GUID
    Email = "user@example.com",
    // ...
};

// ❌ WRONG: Don't use NewGuid()
var user = new ApplicationUser
{
    Id = Guid.NewGuid(),  // Random GUID - worse performance
    // ...
};
```

---

## Type-Safe JSON Properties (CRITICAL)

**NEVER use string properties for JSON data**

❌ **WRONG**:
```csharp
public class Feed {
    public string Selectors { get; set; }  // Don't do this!
}
```

✅ **CORRECT**:
```csharp
// Create strongly-typed model in Models/ directory
public class FeedSelectors {
    public string Title { get; set; }
    public string Content { get; set; }
}

public class Feed {
    public FeedSelectors Selectors { get; set; }  // Type-safe!
}

// Configure with Fluent API
builder.OwnsOne(x => x.Selectors, b => b.ToJson());
```

**Benefits**: Compile-time type safety, IntelliSense support, better maintainability

---

## Entity Configuration Organization

**MUST create separate configuration classes for each entity**

**Location**: `src/RSSVibe.Data/Configurations/` (note: plural "Configurations")

**Pattern**:
```csharp
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using RSSVibe.Data.Entities;

namespace RSSVibe.Data.Configurations;

/// <summary>
/// Entity Framework configuration for MyEntity.
/// </summary>
internal sealed class MyEntityConfiguration : IEntityTypeConfiguration<MyEntity>
{
    public void Configure(EntityTypeBuilder<MyEntity> builder)
    {
        builder.ToTable("MyEntities");

        // Configure properties, indexes, relationships, etc.
    }
}
```

**DbContext Integration**:
```csharp
protected override void OnModelCreating(ModelBuilder builder)
{
    base.OnModelCreating(builder);

    // Automatically discovers and applies all IEntityTypeConfiguration implementations
    builder.ApplyConfigurationsFromAssembly(typeof(RssVibeDbContext).Assembly);
}
```

**Key Points**:
- Configuration classes are `internal sealed`
- Located in `Configurations` folder (plural, not "Configuration")
- Automatically discovered via `ApplyConfigurationsFromAssembly()`
- No manual registration needed in DbContext

---

## Minimal Configuration Approach

**ONLY configure what EF Core cannot infer automatically**

❌ **AVOID** (EF Core infers these automatically):
```csharp
.HasColumnName("id")
.HasColumnType("text")
.IsRequired()  // for non-nullable properties
.ToTable("feed")
```

✅ **DO** (meaningful business rules only):
```csharp
.HasMaxLength(200)
.HasDefaultValue(60)
.HasDefaultValueSql("now()")
.HasCheckConstraint("check_positive", "value > 0")
.ValueGeneratedNever()  // for GUIDs
```

- ONLY specify column types for database-specific features (e.g., `jsonb`, `text[]` for PostgreSQL)

---

## Transaction Handling with PostgreSQL

**CRITICAL: MUST use execution strategy for all manual transactions in PostgreSQL**

PostgreSQL provider requires wrapping transactions in an execution strategy for proper retry handling and transaction management.

### Pattern: Execution Strategy with Transactions

✅ **CORRECT** (recommended - with state parameters to avoid closures):
```csharp
// 1. Create execution strategy from DbContext
var strategy = dbContext.Database.CreateExecutionStrategy();

// 2. Prepare state tuple to avoid closures
var state = (entity, newEntity, dbContext, logger);

// 3. Use ExecuteAsync with state parameters
return await strategy.ExecuteAsync(
    state,
    static async (state, ct) =>
    {
        var (entity, newEntity, dbContext, logger) = state;

        await using var transaction = await dbContext.Database.BeginTransactionAsync(ct);

        try
        {
            // Perform operations
            entity.SomeProperty = newValue;
            dbContext.SomeEntities.Add(newEntity);

            await dbContext.SaveChangesAsync(ct);
            await transaction.CommitAsync(ct);

            logger.LogInformation("Transaction completed successfully");
            return successResult;
        }
        catch
        {
            await transaction.RollbackAsync(ct);
            throw;
        }
    },
    cancellationToken);
```

✅ **ALSO CORRECT** (without state parameters - uses closures):
```csharp
var strategy = dbContext.Database.CreateExecutionStrategy();

return await strategy.ExecuteAsync(async () =>
{
    await using var transaction = await dbContext.Database.BeginTransactionAsync(cancellationToken);

    try
    {
        // Perform operations
        entity.SomeProperty = newValue;
        dbContext.SomeEntities.Add(newEntity);

        await dbContext.SaveChangesAsync(cancellationToken);
        await transaction.CommitAsync(cancellationToken);

        return successResult;
    }
    catch
    {
        await transaction.RollbackAsync(cancellationToken);
        throw;
    }
});
```

❌ **WRONG** (will cause issues in PostgreSQL):
```csharp
// Don't use transactions directly without execution strategy
await using var transaction = await dbContext.Database.BeginTransactionAsync(cancellationToken);
try
{
    // operations...
    await transaction.CommitAsync(cancellationToken);
}
catch
{
    await transaction.RollbackAsync(cancellationToken);
    throw;
}
```

### Why Execution Strategy?

- **PostgreSQL-specific requirement**: The Npgsql provider needs execution strategy for transaction retry logic
- **Handles transient failures**: Automatically retries on connection issues
- **Prevents deadlocks**: Proper transaction scope management
- **Testing compatibility**: Works correctly in test scenarios with in-memory database state

### Best Practices

**Always use state parameters to avoid closures**:
- Pass dependencies as state tuple
- Use `static async` lambda to prevent accidental closure capture
- Improves performance by avoiding closure allocations
- Makes dependencies explicit

**Use ExecuteAsync with manual transactions when returning values**:
- `ExecuteInTransactionAsync` is ideal for void operations (no return value)
- For operations that return results, use `ExecuteAsync` with manual transaction handling
- Always wrap in `await using var transaction` with try-catch-rollback pattern
- Use `await using` for proper async disposal of IAsyncDisposable resources
- This is the recommended approach for PostgreSQL with Npgsql provider

### When to Use

MUST use execution strategy when:
- Creating manual transactions with `BeginTransactionAsync()`
- Performing multiple operations that must be atomic
- Implementing complex business logic requiring rollback capability

NOT needed for:
- Simple `SaveChangesAsync()` calls (already wrapped in implicit transaction)
- Read-only operations
- Single entity modifications

---

## Migration Management

**MUST use the migration script**: `src/RSSVibe.Data/add_migration.sh`

```bash
# Navigate to Data project directory
cd src/RSSVibe.Data

# Create migration (use PascalCase)
bash add_migration.sh AddUserPreferences
```

**Important**:
- MUST execute script from `src/RSSVibe.Data/` directory
- MUST review generated migration file before applying
- NEVER modify migration files manually (remove and regenerate instead)
- Script handles correct project and startup project paths automatically
