# Database Integrations Reference

## Quick Reference

| Database | Hosting Package | Client Package | Add Method |
|----------|----------------|----------------|------------|
| PostgreSQL | `Aspire.Hosting.PostgreSQL` | `Aspire.Npgsql` | `AddPostgres()` |
| SQL Server | `Aspire.Hosting.SqlServer` | `Aspire.Microsoft.Data.SqlClient` | `AddSqlServer()` |
| MySQL | `Aspire.Hosting.MySql` | `Aspire.MySqlConnector` | `AddMySql()` |
| MongoDB | `Aspire.Hosting.MongoDB` | `Aspire.MongoDB.Driver` | `AddMongoDB()` |
| Oracle | `Aspire.Hosting.Oracle` | `Aspire.Oracle.EntityFrameworkCore` | `AddOracle()` |
| SQLite | N/A | `Aspire.Microsoft.Data.Sqlite` | N/A |

## PostgreSQL

### Hosting Integration
```csharp
// Package: Aspire.Hosting.PostgreSQL
var postgres = builder.AddPostgres("postgres")
    .WithDataVolume()                    // Persist data
    .WithPgAdmin();                      // Add pgAdmin UI

var db = postgres.AddDatabase("mydb");

builder.AddProject<Projects.Api>("api")
    .WithReference(db)
    .WaitFor(db);
```

### Client Integration
```csharp
// Package: Aspire.Npgsql
builder.AddNpgsqlDataSource("mydb");

// With Entity Framework
// Package: Aspire.Npgsql.EntityFrameworkCore.PostgreSQL
builder.AddNpgsqlDbContext<MyDbContext>("mydb");
```

### Configuration
```json
{
  "Aspire": {
    "Npgsql": {
      "DisableHealthChecks": false,
      "DisableTracing": false,
      "DisableMetrics": false
    }
  }
}
```

### Use in Services
```csharp
public class MyService(NpgsqlDataSource dataSource)
{
    public async Task<List<Item>> GetItems()
    {
        await using var conn = await dataSource.OpenConnectionAsync();
        // Use connection...
    }
}
```

## SQL Server

### Hosting Integration
```csharp
// Package: Aspire.Hosting.SqlServer
var sql = builder.AddSqlServer("sql")
    .WithDataVolume();

var db = sql.AddDatabase("mydb");

builder.AddProject<Projects.Api>("api")
    .WithReference(db)
    .WaitFor(db);
```

### Client Integration
```csharp
// Package: Aspire.Microsoft.Data.SqlClient
builder.AddSqlServerClient("mydb");

// With Entity Framework
// Package: Aspire.Microsoft.EntityFrameworkCore.SqlServer
builder.AddSqlServerDbContext<MyDbContext>("mydb");
```

### Persistent Password
```bash
dotnet user-secrets set Parameters:sql-password "YourPassword123!"
```

```csharp
var password = builder.AddParameter("sql-password", secret: true);
var sql = builder.AddSqlServer("sql", password: password)
    .WithDataVolume();
```

## MySQL

### Hosting Integration
```csharp
// Package: Aspire.Hosting.MySql
var mysql = builder.AddMySql("mysql")
    .WithDataVolume()
    .WithPhpMyAdmin();  // Add phpMyAdmin UI

var db = mysql.AddDatabase("mydb");
```

### Client Integration
```csharp
// Package: Aspire.MySqlConnector
builder.AddMySqlDataSource("mydb");

// With Entity Framework (Pomelo)
// Package: Aspire.Pomelo.EntityFrameworkCore.MySql
builder.AddMySqlDbContext<MyDbContext>("mydb");
```

## MongoDB

### Hosting Integration
```csharp
// Package: Aspire.Hosting.MongoDB
var mongo = builder.AddMongoDB("mongo")
    .WithDataVolume()
    .WithMongoExpress();  // Add Mongo Express UI

var db = mongo.AddDatabase("mydb");
```

### Client Integration
```csharp
// Package: Aspire.MongoDB.Driver
builder.AddMongoDBClient("mydb");
```

### Use in Services
```csharp
public class MyService(IMongoClient client)
{
    private readonly IMongoDatabase _db = client.GetDatabase("mydb");
    
    public async Task<List<Item>> GetItems()
    {
        var collection = _db.GetCollection<Item>("items");
        return await collection.Find(_ => true).ToListAsync();
    }
}
```

## Oracle

### Hosting Integration
```csharp
// Package: Aspire.Hosting.Oracle
var oracle = builder.AddOracle("oracle")
    .WithDataVolume();

var db = oracle.AddDatabase("mydb");
```

### Client Integration
```csharp
// Package: Aspire.Oracle.EntityFrameworkCore
builder.AddOracleDatabaseDbContext<MyDbContext>("mydb");
```

## Common Patterns

### Data Volumes (Persist Data)
```csharp
// Auto-named volume (recommended)
builder.AddPostgres("db").WithDataVolume();

// Custom volume name
builder.AddPostgres("db")
    .WithVolume(name: "pg-data", target: "/var/lib/postgresql/data");
```

### Bind Mounts
```csharp
builder.AddPostgres("db")
    .WithDataBindMount(source: "./data/postgres");
```

### Health Checks
```csharp
// Wait for database to be running
api.WaitFor(db);

// Wait for database to be healthy (if health check configured)
api.WaitForHealthy(db);
```

### Connection String Override
```csharp
// Use external database via connection string
var db = builder.AddConnectionString("mydb");

// appsettings.json:
// { "ConnectionStrings": { "mydb": "Host=prod.db.com;..." } }
```

## Entity Framework Migrations

### Run Migrations on Startup
```csharp
// In consuming project
public class MigrationService(MyDbContext context) : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        await context.Database.MigrateAsync(ct);
    }
}
```

### Use aspire exec for EF Commands
```bash
# Run EF migrations with proper connection string
aspire exec --resource api -- dotnet ef migrations add Init

# Apply migrations
aspire exec --resource api -- dotnet ef database update
```

## Database Admin UIs

### PostgreSQL - pgAdmin
```csharp
builder.AddPostgres("postgres").WithPgAdmin();
```

### MySQL - phpMyAdmin
```csharp
builder.AddMySql("mysql").WithPhpMyAdmin();
```

### MongoDB - Mongo Express
```csharp
builder.AddMongoDB("mongo").WithMongoExpress();
```

### PostgreSQL - pgWeb
```csharp
builder.AddPostgres("postgres").WithPgWeb();
```

## Environment Variables Injected

When using `WithReference(db)`, Aspire injects:

| Variable | Example |
|----------|---------|
| `ConnectionStrings__mydb` | Full connection string |
| `MYDB_HOST` | `localhost` |
| `MYDB_PORT` | `5432` |
| `MYDB_DATABASE` | `mydb` |
| `MYDB_USERNAME` | `postgres` |
| `MYDB_PASSWORD` | (secret) |

## Polyglot Database Access

### Python
```python
import os
import psycopg

conn_str = os.getenv("CONNECTIONSTRINGS__MYDB")
async with await psycopg.AsyncConnection.connect(conn_str) as conn:
    # Use connection
```

### JavaScript/Node.js
```javascript
import pg from 'pg';

const client = new pg.Client({
  host: process.env.MYDB_HOST,
  port: process.env.MYDB_PORT,
  database: process.env.MYDB_DATABASE,
  user: process.env.MYDB_USERNAME,
  password: process.env.MYDB_PASSWORD,
});
await client.connect();
```
