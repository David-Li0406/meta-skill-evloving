# EF Core Migration Commands

This document provides the equivalent EF Core commands for Laravel Artisan migration commands.

## Creating Migrations

| Laravel | EF Core |
|---------|---------|
| `php artisan make:migration create_products_table` | `dotnet ef migrations add CreateProductsTable` |
| `php artisan make:migration add_status_to_products_table` | `dotnet ef migrations add AddStatusToProducts` |

```powershell
# Create a new migration
dotnet ef migrations add MigrationName

# Create migration with specific project/startup
dotnet ef migrations add MigrationName --project src/ProjectName.Data --startup-project src/ProjectName.Web
```

## Running Migrations

| Laravel | EF Core |
|---------|---------|
| `php artisan migrate` | `dotnet ef database update` |
| `php artisan migrate --seed` | `dotnet ef database update` + custom seeder |

```powershell
# Apply all pending migrations
dotnet ef database update

# Apply migrations to specific point
dotnet ef database update MigrationName
```

## Rolling Back Migrations

| Laravel | EF Core |
|---------|---------|
| `php artisan migrate:rollback` | `dotnet ef database update PreviousMigrationName` |
| `php artisan migrate:rollback --step=3` | `dotnet ef database update TargetMigrationName` |
| `php artisan migrate:reset` | `dotnet ef database update 0` |
| `php artisan migrate:fresh` | Drop DB + `dotnet ef database update` |

```powershell
# Rollback to specific migration
dotnet ef database update PreviousMigrationName

# Rollback all migrations (reset)
dotnet ef database update 0

# Remove last migration (if not applied)
dotnet ef migrations remove
```

## Generating SQL Scripts

| Laravel | EF Core |
|---------|---------|
| `php artisan migrate --pretend` | `dotnet ef migrations script` |

```powershell
# Generate SQL script for all migrations
dotnet ef migrations script -o migration.sql

# Generate script from specific migration
dotnet ef migrations script FromMigration ToMigration -o migration.sql

# Generate idempotent script (safe to run multiple times)
dotnet ef migrations script --idempotent -o migration.sql
```

## Listing Migrations

| Laravel | EF Core |
|---------|---------|
| `php artisan migrate:status` | `dotnet ef migrations list` |

```powershell
# List all migrations
dotnet ef migrations list

# List with applied status (requires database connection)
dotnet ef migrations list --context ApplicationDbContext
```

## Seeding Data

| Laravel | EF Core |
|---------|---------|
| `php artisan db:seed` | Custom code in Program.cs or migration |
| `php artisan db:seed --class=ProductSeeder` | Custom seeder class |

```csharp
// In Program.cs after building the app
using (var scope = app.Services.CreateScope())
{
    var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
    await DbSeeder.SeedAsync(context);
}
```

## Fresh Start (Development Only)

| Laravel | EF Core |
|---------|---------|
| `php artisan migrate:fresh --seed` | Drop + Update + Seed |

```powershell
# Drop database and recreate (DEVELOPMENT ONLY!)
dotnet ef database drop --force
dotnet ef database update
# Then run your seeder
```

## Bundle for Production

```powershell
# Create migration bundle executable (for production deployments)
dotnet ef migrations bundle --self-contained

# Run the bundle
./efbundle.exe --connection "your-connection-string"
```

## Common Options

```powershell
# Specify DbContext (if multiple)
dotnet ef migrations add Name --context ApplicationDbContext

# Specify project paths
dotnet ef migrations add Name \
    --project src/ProjectName.Data \
    --startup-project src/ProjectName.Web

# Verbose output
dotnet ef migrations add Name --verbose

# Use specific configuration
dotnet ef database update --configuration Release
```

## Connection String Override

```powershell
# Use specific connection string
dotnet ef database update --connection "Server=...;Database=...;..."
```

## Troubleshooting

### "No migrations were found"
- Ensure migrations are in the correct assembly
- Check the `--project` flag points to the data project

### "Unable to create an object of type 'DbContext'"
Add a design-time factory:

```csharp
public class ApplicationDbContextFactory : IDesignTimeDbContextFactory<ApplicationDbContext>
{
    public ApplicationDbContext CreateDbContext(string[] args)
    {
        var optionsBuilder = new DbContextOptionsBuilder<ApplicationDbContext>();
        optionsBuilder.UseSqlServer("Server=(localdb)\\mssqllocaldb;Database=DesignTimeDb;");
        return new ApplicationDbContext(optionsBuilder.Options);
    }
}
```

### Force recreation of migration
```powershell
# Remove and recreate
dotnet ef migrations remove
dotnet ef migrations add CorrectMigrationName
```
