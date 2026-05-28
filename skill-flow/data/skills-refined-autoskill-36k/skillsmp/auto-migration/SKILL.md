---
name: auto-migration
description: Automatically detect schema changes and manage EF Core migrations
trigger: "entity change OR dbcontext change OR create migration"
allowed-tools:
  - Bash(dotnet ef)
  - Bash(dotnet build)
  - Bash(git diff)
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Auto Migration Manager

Automatically detects database schema changes and manages Entity Framework Core migrations.

## Trigger Conditions

- Entity class modified (properties added/removed/changed)
- Entity configuration modified (IEntityTypeConfiguration)
- DbContext modified (DbSet added/removed)
- Value object changed
- Index or constraint added

## Detection Strategy

### 1. Monitor Entity Changes

```bash
# Track changes in entity files
git diff --name-only HEAD | grep -E "Domain/.*/(Entities|ValueObjects)/.*\.cs$"

# Check for property changes
git diff HEAD -- "*.cs" | grep -E "^\+.*public.*\{ get;|^\-.*public.*\{ get;"
```

### 2. Schema Change Types

| Change Type | Example | Migration Impact |
|-------------|---------|------------------|
| Add Property | `public string Sku { get; }` | Add column |
| Remove Property | Delete property | Drop column (⚠️ Data loss) |
| Rename Property | Name → Title | Rename column |
| Change Type | `int` → `long` | Alter column |
| Add Relationship | Navigation property | Add foreign key |
| Add Index | `[Index]` attribute | Create index |
| Change Length | `MaxLength(50)` → `MaxLength(100)` | Alter column |

### 3. Detect Pending Changes

```bash
# Check if model has changes vs database
dotnet ef migrations has-pending-model-changes \
  --project Merge.Infrastructure \
  --startup-project Merge.API

# List pending migrations
dotnet ef migrations list \
  --project Merge.Infrastructure \
  --startup-project Merge.API
```

## Migration Generation

### Naming Convention

```
{Timestamp}_{Action}{Entity}{Detail}

Examples:
- 20240115_AddSkuToProduct
- 20240115_CreateReviewsTable
- 20240115_AddIndexOnOrderUserId
- 20240115_RemoveDeprecatedFields
- 20240115_RenameProductTitleToName
```

### Generate Migration

```bash
# Standard migration
dotnet ef migrations add AddSkuToProduct \
  --project Merge.Infrastructure \
  --startup-project Merge.API \
  --output-dir Data/Migrations

# With specific context (if multiple)
dotnet ef migrations add AddSkuToProduct \
  --context CatalogDbContext \
  --project Merge.Infrastructure \
  --startup-project Merge.API
```

### Review Before Apply

**ALWAYS review the generated migration:**

```csharp
// Check Up() method
protected override void Up(MigrationBuilder migrationBuilder)
{
    // ✅ Safe: Add column with default
    migrationBuilder.AddColumn<string>(
        name: "Sku",
        table: "Products",
        type: "character varying(50)",
        maxLength: 50,
        nullable: true);  // Start nullable for existing data

    // ⚠️ Dangerous: Drop column
    migrationBuilder.DropColumn(
        name: "OldField",
        table: "Products");

    // ⚠️ Very Dangerous: Drop table
    migrationBuilder.DropTable(name: "OldProducts");
}

// Check Down() method for reversibility
protected override void Down(MigrationBuilder migrationBuilder)
{
    // Should reverse Up() operations
}
```

## Safe Migration Patterns

### 1. Add Non-Nullable Column

```csharp
// Step 1: Add as nullable
migrationBuilder.AddColumn<string>(
    name: "Sku",
    table: "Products",
    nullable: true);

// Step 2: Populate data
migrationBuilder.Sql(
    "UPDATE \"Products\" SET \"Sku\" = 'SKU-' || \"Id\"::text WHERE \"Sku\" IS NULL");

// Step 3: Make non-nullable
migrationBuilder.AlterColumn<string>(
    name: "Sku",
    table: "Products",
    nullable: false);
```

### 2. Rename Column (Zero Downtime)

```csharp
// Step 1: Add new column
migrationBuilder.AddColumn<string>(
    name: "Title",
    table: "Products",
    nullable: true);

// Step 2: Copy data
migrationBuilder.Sql(
    "UPDATE \"Products\" SET \"Title\" = \"Name\"");

// Step 3: (Deploy code that reads both)

// Step 4: Drop old column (separate migration)
migrationBuilder.DropColumn(name: "Name", table: "Products");
```

### 3. Change Column Type

```csharp
// PostgreSQL specific - may need data conversion
migrationBuilder.Sql(@"
    ALTER TABLE ""Products""
    ALTER COLUMN ""Price"" TYPE numeric(18,4)
    USING ""Price""::numeric(18,4)");
```

### 4. Add Index Concurrently (PostgreSQL)

```csharp
// For large tables - don't lock
migrationBuilder.Sql(@"
    CREATE INDEX CONCURRENTLY ""IX_Orders_UserId""
    ON ""Orders"" (""UserId"")");

// Note: CONCURRENTLY cannot be in transaction
// Set in migration:
protected override void BuildTargetModel(ModelBuilder modelBuilder)
{
    // Mark as non-transactional
}
```

## Dangerous Operations Alert

### 🚨 HIGH RISK Operations

```csharp
// Data Loss Risk
migrationBuilder.DropTable("Products");     // All data lost
migrationBuilder.DropColumn("Price", ...);  // Column data lost

// Lock Table (Large tables)
migrationBuilder.AddColumn<string>(         // Table locked during ADD
    name: "NewColumn",
    nullable: false,                        // Requires default or rewrite
    defaultValue: "");

// Index Creation (Large tables)
migrationBuilder.CreateIndex(               // Table locked during CREATE
    name: "IX_Orders_UserId",
    table: "Orders",
    column: "UserId");
```

### Safe Alternatives

```csharp
// Instead of DROP COLUMN immediately
// 1. Stop writing to column
// 2. Deploy code ignoring column
// 3. Drop in future migration

// Instead of ADD non-nullable column
// Add as nullable → populate → alter to non-nullable

// Instead of CREATE INDEX
// Use CONCURRENTLY (PostgreSQL)
```

## Apply Migrations

### Development

```bash
# Apply all pending migrations
dotnet ef database update \
  --project Merge.Infrastructure \
  --startup-project Merge.API

# Apply specific migration
dotnet ef database update AddSkuToProduct \
  --project Merge.Infrastructure \
  --startup-project Merge.API

# Rollback to specific migration
dotnet ef database update PreviousMigrationName \
  --project Merge.Infrastructure \
  --startup-project Merge.API
```

### Production (Script-based)

```bash
# Generate SQL script
dotnet ef migrations script \
  --project Merge.Infrastructure \
  --startup-project Merge.API \
  --idempotent \
  --output migration.sql

# Review script before applying
cat migration.sql

# Apply via psql or database tool
psql -h localhost -U postgres -d merge -f migration.sql
```

### Idempotent Scripts

```bash
# Always use --idempotent for production
dotnet ef migrations script \
  --idempotent \
  --output migration.sql

# This generates:
IF NOT EXISTS(SELECT * FROM "__EFMigrationsHistory" WHERE "MigrationId" = '...')
BEGIN
    -- Migration code
END;
```

## Rollback Strategy

### Rollback Last Migration

```bash
# Remove last migration (if not applied)
dotnet ef migrations remove \
  --project Merge.Infrastructure \
  --startup-project Merge.API

# Revert applied migration
dotnet ef database update PreviousMigrationName \
  --project Merge.Infrastructure \
  --startup-project Merge.API
```

### Emergency Rollback

```sql
-- Manual rollback (PostgreSQL)
-- 1. Run Down() SQL manually
-- 2. Remove from history
DELETE FROM "__EFMigrationsHistory"
WHERE "MigrationId" = '20240115123456_AddSkuToProduct';
```

## Execution Flow

```
1. Entity/Configuration Change Detected
   ↓
2. Check for Pending Model Changes
   ↓
3. Generate Migration with Proper Name
   ↓
4. Review Generated Code
   ↓
5. Check for Dangerous Operations
   ↓
6. If Safe → Apply to Dev Database
   ↓
7. Run Tests
   ↓
8. Generate Idempotent Script for Prod
   ↓
9. Report Migration Status
```

## Output Format

```markdown
## Migration Analysis

**Changed Files:**
- Merge.Domain/Entities/Product.cs (+2 lines)

**Detected Changes:**
1. Added property: `public string Sku { get; private set; }`

**Generated Migration:** `20240115_AddSkuToProduct`

**Operations:**
| Operation | Risk | Impact |
|-----------|------|--------|
| ADD COLUMN Sku | Low | No data loss |

**Commands:**
```bash
# Preview
dotnet ef migrations script --idempotent

# Apply (Dev)
dotnet ef database update

# Apply (Prod)
psql -f migration.sql
```

**Warnings:** None
```

## Validation Checks

**Before Generation:**
- [ ] Entity configuration exists
- [ ] Property has proper type mapping
- [ ] Relationships properly defined
- [ ] No circular dependencies

**Before Apply:**
- [ ] Migration reviewed
- [ ] No DROP operations (or intentional)
- [ ] No large table locks
- [ ] Down() method works
- [ ] Tests pass

**After Apply:**
- [ ] Database accessible
- [ ] Application starts
- [ ] Queries work
- [ ] No performance regression
