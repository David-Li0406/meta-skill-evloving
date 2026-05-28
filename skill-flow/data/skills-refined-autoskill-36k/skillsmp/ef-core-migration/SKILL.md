---
name: ef-core-migration
description: Entity Framework Core migration patterns for PHP Eloquent/Doctrine to EF Core. Use when converting Eloquent models to EF Core entities, migrating relationships, creating DbContext, or setting up EF Core migrations.
---

# EF Core Migration from PHP ORM

Use this skill when migrating PHP ORM (Eloquent/Doctrine) to Entity Framework Core.

## When to Use This Skill

- Converting Eloquent models to EF Core entities
- Migrating Doctrine entities to EF Core
- Setting up relationships (hasMany, belongsTo, belongsToMany)
- Creating and running EF Core migrations
- Configuring soft deletes, timestamps, and scopes

## Template Files

See the [templates](./templates/) directory:
- [Entity.cs](./templates/Entity.cs) - Sample entity with relationships
- [DbContext.cs](./templates/DbContext.cs) - DbContext with configuration
- [Migration commands](./templates/migration-commands.md) - Common EF Core commands

## Eloquent to EF Core Mapping

### Model Properties

| Eloquent | EF Core |
|----------|---------|
| `protected $table = 'users'` | `[Table("users")]` or Fluent API |
| `protected $primaryKey = 'user_id'` | `[Key]` or `HasKey()` |
| `public $incrementing = false` | `ValueGeneratedNever()` |
| `protected $keyType = 'string'` | Use `string` type for key |
| `public $timestamps = false` | Don't add timestamp properties |
| `protected $fillable = [...]` | Not needed (use DTOs) |
| `protected $guarded = [...]` | Not needed (use DTOs) |
| `protected $hidden = [...]` | `[JsonIgnore]` or DTO mapping |
| `protected $casts = [...]` | Data annotations or value converters |

### Relationship Mapping

| Eloquent Method | EF Core |
|-----------------|---------|
| `hasOne()` | Navigation property + `HasOne().WithOne()` |
| `hasMany()` | `ICollection<T>` + `HasMany().WithOne()` |
| `belongsTo()` | Navigation property + `HasOne().WithMany()` |
| `belongsToMany()` | Join entity + two `HasMany()` |
| `morphTo()` | Discriminator pattern |
| `morphMany()` | Polymorphic with discriminator |

### Common Patterns

#### Soft Deletes

```csharp
// Entity
public DateTime? DeletedAt { get; set; }

// DbContext
entity.HasQueryFilter(e => e.DeletedAt == null);
```

#### Timestamps

```csharp
public override Task<int> SaveChangesAsync(...)
{
    foreach (var entry in ChangeTracker.Entries<IHasTimestamps>())
    {
        if (entry.State == EntityState.Added)
            entry.Entity.CreatedAt = DateTime.UtcNow;
        entry.Entity.UpdatedAt = DateTime.UtcNow;
    }
    return base.SaveChangesAsync(...);
}
```

#### Scopes → Extension Methods

```csharp
// Eloquent: $query->active()->inCategory($id)
// EF Core:
public static IQueryable<Product> Active(this IQueryable<Product> query)
    => query.Where(p => p.IsActive);

public static IQueryable<Product> InCategory(this IQueryable<Product> query, int id)
    => query.Where(p => p.CategoryId == id);

// Usage:
var products = await _context.Products
    .Active()
    .InCategory(5)
    .ToListAsync();
```

## Migration Commands

```powershell
# Create initial migration
dotnet ef migrations add InitialCreate

# Apply migrations
dotnet ef database update

# Generate SQL script
dotnet ef migrations script -o migration.sql

# Remove last migration (if not applied)
dotnet ef migrations remove

# Revert to specific migration
dotnet ef database update MigrationName
```

## Data Type Mapping

| PHP/MySQL | C#/.NET | SQL Server |
|-----------|---------|------------|
| `int` | `int` | `int` |
| `bigint` | `long` | `bigint` |
| `decimal(10,2)` | `decimal` | `decimal(18,2)` |
| `varchar(255)` | `string` | `nvarchar(255)` |
| `text` | `string` | `nvarchar(max)` |
| `boolean` / `tinyint(1)` | `bool` | `bit` |
| `datetime` | `DateTime` | `datetime2` |
| `date` | `DateOnly` | `date` |
| `time` | `TimeOnly` | `time` |
| `json` | `string` (with converter) | `nvarchar(max)` |
| `enum` | `enum` | `int` or `nvarchar` |

## Best Practices

1. **Use migrations** - Never modify database schema manually
2. **Configure in Fluent API** - Prefer Fluent API over data annotations for complex config
3. **Split configurations** - Use `IEntityTypeConfiguration<T>` for large entities
4. **Use async** - Always use `ToListAsync()`, `FirstOrDefaultAsync()`, etc.
5. **Project to DTOs** - Use `.Select()` to project to DTOs instead of loading full entities
6. **Include explicitly** - Use `.Include()` for eager loading, avoid lazy loading
7. **Use no-tracking** - Use `AsNoTracking()` for read-only queries
