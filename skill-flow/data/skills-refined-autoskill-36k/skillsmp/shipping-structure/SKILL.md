---
name: shipping-structure
description: Understanding the Shipping microservice C# codebase structure, coding standards, and architectural patterns. Use when working with shipments, consignments, tracking, and carrier integrations.
license: MIT
metadata:
  author: shipitsmarter
  version: "1.0"
---

# Shipping Microservice Structure

The `shipping` repository is a C# microservice that handles the core shipping operations: shipments, consignments, handling units, tracking, invoices, carrier integrations, and document management.

---

## Architecture Rules

### Constants - Single Source of Truth

Before introducing a constant, **search the entire repository** to check if it already exists.

```csharp
// WRONG - duplicates the collection name, bypasses playground logic
var collection = db.GetCollection<ConsignmentDocument>("consignments");

// CORRECT - uses the repository's constant
var collection = db.GetSet<ConsignmentDocument>(ConsignmentRepository.CollectionNameExternal);
```

**Why:** Constants like MongoDB collection names have runtime behavior (e.g., `"consignments"` becomes `"consignments_playground"` in test mode). Duplicating raw strings bypasses this logic.

### Database Logic - Repository Layer Only

All database operations must go through `src/Shipping.Core/MongoDb/`. Never place database queries in use-cases, handlers, or controllers.

```csharp
// WRONG - database logic in use-case
var filter = Builders<ConsignmentDocument>.Filter.Eq(x => x.Data.Status, status);
var results = await db.GetCollection<ConsignmentDocument>("consignments").Find(filter).ToListAsync();

// CORRECT - use repository
var filter = consignmentRepository.Filter.Eq(x => x.Data.Status, status);
var results = await consignmentRepository.Search(filter, sort, pagination);
```

**Why:** Repositories encapsulate permissions, playground context, and search text generation. Direct DB access bypasses these.

### Controller Logic - Keep Controllers Thin

Controllers handle HTTP only. Use **method-level injection** (`[FromServices]`) for use-cases and mappers:

```csharp
// CORRECT - method-level injection
[HttpGet]
[Route("{shipmentId:guid}")]
public async Task<IActionResult> GetById(
    Guid shipmentId,
    [FromServices] IGetShipmentUseCase useCase,
    [FromServices] CoreToContract.ShipmentMapper mapper)
{
    var shipment = await dispatcher.Handle(useCase, shipmentId);
    return Ok(mapper.From(shipment));
}

// AVOID - constructor injection for use-cases
public class ShipmentController
{
    private readonly IGetShipmentUseCase _getShipmentUseCase; // Don't do this
}
```

### Enums - Keep as Enums

Never convert enums to strings unless absolutely necessary:

```csharp
// AVOID
var statusFilter = filter.Eq(x => x.Status, status.ToString());

// PREFER
var statusFilter = filter.Eq(x => x.Status, status);
```

---

## Solution Structure

```
Shipping.sln
├── src/
│   ├── Shipping.Api/           # ASP.NET Core Web API, controllers, handlers
│   ├── Shipping.Analytics/     # Analytics query compilation and validation
│   ├── Shipping.Contracts/     # Public API contracts (request/response DTOs)
│   ├── Shipping.Core/          # Business logic, entities, repositories, use-cases
│   ├── Shipping.Events/        # Domain events (SNS/SQS)
│   ├── Shipping.Migrations/    # MongoDB data migrations
│   └── Shipping.StitchContracts/ # Carrier integration (stitch) contracts
├── test/
│   └── Shipping.Tests/         # Unit and integration tests
├── packages/                   # Shared utilities
├── charts/                     # Helm charts
└── docs/                       # Documentation
```

---

## Project Responsibilities

### Shipping.Core

The heart of the codebase - all business logic lives here.

```
Shipping.Core/
├── DependencyInjection/    # Service registration
├── Entities/               # MongoDB document models
│   ├── Consignments/
│   ├── Shipments/
│   ├── HandlingUnits/
│   ├── Tracking/
│   ├── Invoice/
│   └── ...
├── Enums/                  # Domain enums
├── Extensions/             # Extension methods
├── Framework/              # Cross-cutting concerns
│   ├── CarrierIntegrating/ # Carrier integration helpers
│   ├── Constants/
│   ├── Context/            # Request context
│   ├── Services/           # Shared services
│   └── ...
├── Models/                 # Internal domain models (non-document)
├── MongoDb/                # Data access layer
│   ├── Filters/            # Query filter builders
│   ├── Indexes/            # Index definitions (IIndexCollection)
│   └── Repositories/       # Repository implementations
└── UseCases/               # Business logic per domain
    ├── Consignments/
    ├── Shipments/
    ├── HandlingUnits/
    ├── Tracking/
    ├── Invoices/
    └── ...
```

### Shipping.Api

HTTP layer with versioned controllers.

```
Shipping.Api/
├── DependencyInjection/    # API-level DI setup
├── Handlers/               # Message handlers (Dapr, files)
│   └── FileHandlers/       # File processing handlers
├── v4/                     # API version 4
│   ├── Controllers/        # Thin controllers
│   ├── Mappings/           # CoreToContract, ContractToCore mappers
│   └── Extensions/
└── Program.cs              # Application entry point
```

### Shipping.Contracts

Public API models - all properties must have XML documentation.

```
Shipping.Contracts/v4/
├── DespatchAdvice/         # Despatch advice models
├── FlexibleConfig/         # Dynamic configuration
├── Models/                 # Request/response models
│   └── Lists/              # Query parameter classes
└── CustomAnnotations/      # Validation attributes
```

**Contract Class Rules:**

1. **No explicit constructors** - Use implicit constructors with `required` properties for JSON serialization/deserialization compatibility:

```csharp
// CORRECT - implicit constructor with required properties
public class InvoiceListItem
{
    public required Guid Id { get; set; }
    public required string InvoiceNumber { get; set; }
    public required string CarrierReference { get; set; }
}

// AVOID - explicit constructor (breaks JSON deserialization)
public class InvoiceListItem
{
    public InvoiceListItem(Guid id, string invoiceNumber, string carrierReference)
    {
        Id = id;
        InvoiceNumber = invoiceNumber;
        CarrierReference = carrierReference;
    }
    
    public Guid Id { get; }
    public string InvoiceNumber { get; }
    public string CarrierReference { get; }
}
```

2. **Exception: Base class inheritance** - When inheriting from base classes with explicit constructors (e.g., `ListWrapper<T>` from viya-core), you must call the base constructor:

```csharp
// OK - required when base class has explicit constructor
public class InvoiceListWrapper : ListWrapper<InvoiceListItem>
{
    public InvoiceListWrapper(
        long totalCount, int pageNumber, int pageSize, Uri url,
        List<InvoiceListItem> items,
        List<UnclosedInvoicesByCarrier> unclosedInvoicesByCarrier)
        : base(totalCount, pageNumber, pageSize, url, items)
    {
        UnclosedInvoicesByCarrier = unclosedInvoicesByCarrier;
    }

    public List<UnclosedInvoicesByCarrier> UnclosedInvoicesByCarrier { get; }
}
```

3. **XML documentation required** - All public properties must have `<summary>` documentation.

### Shipping.Migrations

MongoDB data migrations for schema changes.

```
Shipping.Migrations/
├── Migrations/             # Individual migrations
│   └── YYYYMMDD_{Description}/
│       └── Migration_YYYYMMDD.cs
├── Seeding/                # Data seeding
├── Framework/              # Migration helpers
└── Models/                 # Migration-specific models
```

---

## Key Patterns

### Use Case Pattern

Use cases contain business logic for a single operation:

```csharp
public class CreateShipmentUseCase(
    ILogger<CreateShipmentUseCase> logger,
    IShipmentRepository shipmentRepository,
    IHandlingUnitService handlingUnitService
) : ICreateShipmentUseCase
{
    public async Task<CreateUpdateShipmentResult> Handle(CreateShipmentUseCaseInput input)
    {
        // Business logic here
    }
}
```

**Directory structure:**
```
UseCases/Shipments/CreateShipment/
├── CreateShipmentUseCase.cs
├── CreateShipmentUseCaseInput.cs
└── ICreateShipmentUseCase.cs
```

**When to use Services vs Use Cases:**

| Use Cases | Services |
|-----------|----------|
| Single operation logic | Shared/reusable logic |
| Auto-registered (no DI setup) | Must be registered in DI |
| Called from controllers | Called from use cases |
| One public method (`Handle`) | Multiple methods allowed |

Register services in `CoreRegistrations.cs`:
```csharp
services.AddScoped<IMyNewService, MyNewService>();
```

### Repository Pattern

All repositories extend base functionality with the repository's `Filter` property:

```csharp
// PREFER - repository Filter property
var filter = consignmentRepository.Filter.Eq(x => x.Data.Status, status);

// AVOID - verbose Builders syntax
var filter = Builders<ConsignmentDocument>.Filter.Eq(x => x.Data.Status, status);
```

Available base methods: `Get`, `Search`, `GetAll`, `GetPaginated`, `Exists`, `Count`, `Insert`, `Update`, `Delete`.

### Index Management

All indexes defined in `src/Shipping.Core/MongoDb/Indexes/`:

```csharp
public class ShipmentIndexes : IIndexCollection
{
    public string CollectionName => ShipmentRepository.CollectionNameExternal;

    public List<IndexDefinition> Indexes => new()
    {
        new IndexDefinition
        {
            Name = "Reference",
            Keys = Builders<BsonDocument>.IndexKeys.Ascending("Data.Reference")
        }
    };
}
```

**Behavior:** Removing an index from these files drops it from the database. Renaming drops the old one and creates a new one.

### Query Parameter Classes

For 5+ query parameters, extract to a class in `Shipping.Contracts/v4/Models/Lists/`:

```csharp
// AVOID - many inline parameters
public async Task<ActionResult<List<Shipment>>> GetList(
    string? search, int? page, int? pageSize, string? sortBy, ...)

// PREFER - extract to class
public async Task<ActionResult<List<Shipment>>> GetList(
    [FromQuery] GetShipmentListQueryParams query)
```

---

## MongoDB Migrations

**Location:** `src/Shipping.Migrations/Migrations/YYYYMMDD_{Description}/`

### Creating a Migration

1. Create directory: `Migrations/YYYYMMDD_{Description}/`
2. Create class: `Migration_YYYYMMDD.cs` implementing `IMigration`
3. Override `CreatedDate`, `BatchSize` (default 1000)
4. Implement `Up` method
5. **Always process both production and playground collections**
6. **Always update SchemaVersion**

```csharp
public async Task<BatchResult> Up(MongoDbUnitOfWork unitOfWork, IServiceProvider provider)
{
    var summaries = new List<EntitySummary>
    {
        await MigrateBatch(unitOfWork, isPlayground: false),
        await MigrateBatch(unitOfWork, isPlayground: true)
    };
    
    return new BatchResult
    {
        Success = true,
        EntitySummaries = summaries.Where(s => s.Count > 0).ToList()
    };
}
```

### Key Migration Patterns

```csharp
// Filter by SchemaVersion
var filter = Builders<TDocument>.Filter.Lt(x => x.SchemaVersion, newVersion);

// Always increment SchemaVersion after processing
document.SchemaVersion = newSchemaVersion;

// For simple migrations, consider UpdateMany
await collection.UpdateManyAsync(filter, update);
```

**Backwards compatibility:**
- **Non-nullable field:** Do NOT remove the old field in this migration. Remove in a subsequent migration.
- **Nullable field:** May remove the old field in this migration.

---

## LINQ Best Practices

Prefer `Where` + `Select` over `SelectMany` with conditionals:

```csharp
// AVOID - SelectMany with conditional
var items = collection
    .SelectMany(x => x.IsActive ? new[] { x.Item } : Array.Empty<ItemType>());

// PREFER - Where + Select
var items = collection
    .Where(x => x.IsActive)
    .Select(x => x.Item);
```

---

## BsonDocument Handling

When reading `BsonDocument` (for migrations or dynamic access), convert to concrete types immediately:

```csharp
// AVOID - working with BsonDocument throughout
var status = doc["Data"]["Status"].AsString;

// PREFER - convert to concrete type ASAP
var entity = BsonSerializer.Deserialize<ConcreteType>(doc);
var status = entity.Data.Status;
```

---

## Test Structure

```
test/Shipping.Tests/
├── Helpers/                # Test utilities
├── IntegrationTests/       # API-level tests
└── UnitTests/              # Core logic tests
```

**Local test infrastructure:** `test/compose.yaml` provides MongoDB and LocalStack for integration tests.

---

## Common Commands

```bash
# Build entire solution
dotnet build

# Build specific project
dotnet build src/Shipping.Api

# Run all tests
dotnet test test/Shipping.Tests

# Run specific test by filter
dotnet test test/Shipping.Tests --filter "TestMethodName"

# Run migrations (locally)
# See Shipping.Migrations documentation
```

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| **rates-structure** | Working with the Rates microservice |
| **mongodb-development** | MongoDB queries and aggregations |
| **technical-architect** | Architecture decisions |
