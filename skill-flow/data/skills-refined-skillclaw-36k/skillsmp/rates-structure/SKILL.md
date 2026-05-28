---
name: rates-structure
description: Understanding the Rates microservice C# codebase structure, coding standards, and architectural patterns. Use when working with rate calculations, pricing, and carrier contract configurations.
license: MIT
metadata:
  author: shipitsmarter
  version: "1.0"
---

# Rates Microservice Structure

The `rates` repository is a C# microservice that calculates shipping rates, transit times, and pricing for carriers based on contract configurations stored in MongoDB.

---

## Coding Standards

### General C# Conventions
- Use **file-scoped namespaces** (single line `namespace X;`)
- Use **primary constructors** for dependency injection
- Use **collection expressions** (`[]` syntax) for list/array initialization
- Use **expression-bodied members** where appropriate
- Use `var` for local variables when the type is obvious
- Use **nullable reference types** - the codebase has nullable enabled
- Prefer `ConvertAll()` over `Select().ToList()` for list transformations
- Use `record` types for immutable data transfer objects
- **Single-line code blocks** without braces, but with newline and indentation

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Interfaces | `I` prefix | `IGetRatesUseCase` |
| Async methods | `Async` suffix | `GetDistanceAsync` |
| Private fields | `_` prefix | `_distanceProvider` |
| Constants | `PascalCase` | `MaxRetries` |

### XML Documentation
- **Contracts project**: All public classes and properties MUST have XML docs with `<summary>` tags
- **Core/Api projects**: XML docs optional, mainly for complex logic
- Use `<inheritdoc />` when overriding documented base members

---

## Solution Structure

```
Rates.sln
├── src/
│   ├── Rates.Api/           # ASP.NET Core Web API
│   ├── Rates.Contracts/     # Public API contracts (request/response DTOs)
│   ├── Rates.Core/          # Business logic, entities, repositories, services
│   └── Rates.Shared/        # Shared utilities, enums, helpers
└── test/
    └── Rates.Tests/         # Unit and integration tests
```

---

## Project Responsibilities

### Rates.Contracts
- **Purpose**: Defines all public-facing API models (DTOs)
- **Contains**: Request/response models, versioned under `v1/` folder
- **Key rule**: All properties must have XML documentation for Swagger
- **No business logic** - pure data structures

```
Rates.Contracts/v1/
├── GetRates/
│   ├── Request/          # RatesRequest, RatesShipment, etc.
│   └── Response/         # RatesResponse, CalculationDetails, etc.
└── RatesContract/        # Contract configuration models
    ├── Price/
    ├── TransitTime/
    └── BillableWeight/
```

**Contract Class Rules:**

1. **No explicit constructors** - Use implicit constructors with `required` properties for JSON serialization/deserialization compatibility:

```csharp
// CORRECT - implicit constructor with required properties
public class RatesShipment
{
    public required string Reference { get; set; }
    public required List<HandlingUnit> HandlingUnits { get; set; }
}

// AVOID - explicit constructor (breaks JSON deserialization)
public class RatesShipment
{
    public RatesShipment(string reference, List<HandlingUnit> handlingUnits)
    {
        Reference = reference;
        HandlingUnits = handlingUnits;
    }
    
    public string Reference { get; }
    public List<HandlingUnit> HandlingUnits { get; }
}
```

2. **Exception: Base class inheritance** - When inheriting from base classes with explicit constructors (e.g., `ListWrapper<T>` from viya-core), you must call the base constructor.

3. **XML documentation required** - All public properties must have `<summary>` documentation.

### Rates.Core
- **Purpose**: Domain logic, data access, external service integrations
- **Contains**: Entities, Repositories, Services, Helpers

```
Rates.Core/
├── Entities/RatesContract/   # MongoDB document models
├── Repositories/             # MongoDB data access
├── Services/                 # External API integrations
├── Models/                   # Internal domain models
├── Helpers/                  # Utility classes
└── Settings/                 # Configuration classes
```

### Rates.Api
- **Purpose**: HTTP layer, dependency injection, use cases
- **Contains**: Controllers, UseCases, Mappers

```
Rates.Api/v1/
├── Controllers/          # Thin controllers delegating to use cases
├── UseCases/             # Business logic orchestration
│   └── GetRates/
│       └── Generators/   # Price/transit calculation components
└── Mappers/              # Contract ↔ Core entity mapping
```

### Rates.Shared
- **Purpose**: Cross-cutting utilities shared between projects
- **Contains**: Enums, serialization helpers, generic utilities
- **No dependencies** on other Rates projects

---

## Key Patterns

### Controller Pattern
Controllers are **thin wrappers** delegating to use cases:

```csharp
[Route("v1/rates")]
[ApiController]
public class RateController : Controller
{
    [HttpPost]
    [Route("")]
    [ProducesResponseType(typeof(RatesResponse), StatusCodes.Status200OK)]
    public async Task<IActionResult> Get(
        [FromQuery] bool? showCalculationDetails, 
        [FromBody] RatesRequest request, 
        [FromServices] IGetRatesUseCase useCase)
    {
        var result = await useCase.Handle(new GetRatesUseCaseInput(request, showCalculationDetails ?? false));
        return Ok(result);
    }
}
```

### Use Case Pattern
Use cases implement a single business operation:

```csharp
public interface IGetRatesUseCase
{
    Task<RatesResponse> Handle(GetRatesUseCaseInput input);
}

public class GetRatesUseCase(
    ILogger<GetRatesUseCase> logger, 
    IRatesContractRepository contractRepository,
    IDistanceCalculationService distanceCalculationService) : IGetRatesUseCase
{
    public async Task<RatesResponse> Handle(GetRatesUseCaseInput useCaseInput)
    {
        // Implementation
    }
}
```

### Mapper Pattern
Two-way mapping between Contracts and Core entities:

```
RatesContractMapper.ToCore.cs    # Contract → Core
RatesContractMapper.ToContract.cs # Core → Contract
```

When adding new properties:
1. Add to both Contract and Core entity
2. Add mapping in both `ToCore` and `ToContract` files
3. Handle nullable types appropriately

### Repository Pattern
MongoDB repositories extend `BaseMongoRepository<TDocument, TData>`:

```csharp
public class RatesContractRepository(RatesUnitOfWork unitOfWork)
    : BaseMongoRepository<RatesContractDocument, RatesContract>(unitOfWork), IRatesContractRepository
{
    protected override string CollectionName => "contracts";
}
```

---

## Generator Architecture (GetRatesUseCase)

The rate calculation uses a hierarchy of **Generator** classes:

```
GetRatesUseCase
    └── ContractGenerator (per contract)
            └── ServiceLevelGenerator (per service level)
                    ├── ServiceLevelPriceCalculator
                    │       ├── FixedPriceCalculator
                    │       ├── PercentagePriceCalculator
                    │       ├── ConditionTablePriceCalculator
                    │       └── PriceTemplateTablePriceCalculator
                    └── TransitTimeCalculator
```

### Key Generator Files

```
src/Rates.Api/v1/UseCases/GetRates/Generators/
├── ServiceLevelPriceCalculator.cs   # Orchestrates all price calculations
├── FixedPriceCalculator.cs          # Fixed prices, multipliers, Source building
├── PercentagePriceCalculator.cs     # Percentage prices on top of fixed
├── ConditionTablePriceCalculator.cs # ConditionZonePriceTable calculations
├── PriceTemplateTablePriceCalculator.cs # PriceTemplateTable calculations
├── ServiceLevelGenerator.cs         # Maps PriceElement → RatesPriceDetails
└── BasePriceCalculator.cs           # Shared logic for calculation details
```

### Price Calculation Flow
1. Fixed prices calculated first (including ConditionTable and PriceTemplateTable)
2. Contract-level surcharges added if base prices exist
3. Percentage prices calculated on top of fixed prices
4. All results collected into `PriceElement` list

---

## Viya.Core Condition System

The codebase uses the **Viya.Core.Rules** condition system for dynamic rule evaluation.

### Condition Types
```csharp
// Leaf condition - compares a field value
public class CompareCondition : BaseCondition
{
    public BaseComparison Comparison { get; set; }
}

// Composite conditions - recursive structure
public class AndCondition : BaseCondition
{
    public List<BaseCondition> And { get; set; }  // All must be true
}

public class OrCondition : BaseCondition
{
    public List<BaseCondition> Or { get; set; }   // Any must be true
}
```

### Field Paths (JSONPath)
- `$.reference` - shipment reference
- `$.addresses.sender.countryCode` - sender country
- `$.handlingUnits[each].weight` - each handling unit's weight
- `$.calculated.weight.kgm` - calculated total weight

---

## Test Structure

```
test/Rates.Tests/
├── Helpers/
│   ├── IntegrationTestBase.cs    # Base class for integration tests
│   ├── UnitTestBase.cs           # Base class with test data builders
│   ├── CustomWebApplicationFactory.cs  # Test server setup
│   └── MongoDbFixture.cs         # In-memory MongoDB
├── IntegrationTests/v1/
│   ├── GetRates/
│   │   └── GivenGetRates.cs      # Comprehensive GetRates tests
│   └── Contract/                  # Contract CRUD tests
└── UnitTests/
    ├── Api/v1/UseCases/          # Use case unit tests
    ├── Core/                      # Core logic unit tests
    └── Contract/GetRates/         # Calculation logic tests
```

### Test Base Classes

**UnitTestBase** provides test data builders:
- `GetBaseContract()` - minimal valid contract
- `GetSimpleServiceLevel()` - basic service level
- `GetSimplePrice()` / `GetSimplestFixedPrice()` - price configurations
- `GetTestHandlingUnit()` - handling unit with dimensions
- `GetRatesRequest()` - standard API request

**IntegrationTestBase** extends with HTTP infrastructure:
- `Post()`, `Get()`, `Put()`, `Delete()` helper methods
- `InsertContract()`, `ClearContracts()` - database helpers
- `HttpMessageHandler.SetResponse()` - mock external HTTP calls

### Mocking External Services

```csharp
private void SetupDistanceServiceResponse(decimal distanceInMeters)
{
    var distanceResponse = new
    {
        routes = new[] { new { distanceMeters = (int)distanceInMeters } }
    };
    
    HttpMessageHandler.SetResponse(new HttpResponseMessage(HttpStatusCode.OK)
    {
        Content = new StringContent(JsonSerializer.Serialize(distanceResponse))
    });
}
```

---

## Common Commands

```bash
# Build entire solution
dotnet build

# Build specific project
dotnet build src/Rates.Api

# Run all tests
dotnet test test/Rates.Tests

# Run specific test by name filter
dotnet test test/Rates.Tests --filter "TestMethodName"

# Run tests matching a pattern
dotnet test test/Rates.Tests --filter "StackingInfo"

# List package dependencies
dotnet list src/Rates.Api package
```

---

## Error Handling

| Exception | Use Case | HTTP Status |
|-----------|----------|-------------|
| `LogicException(title, detail)` | Business logic errors | 400 Bad Request |
| `NotFoundException(message, reference)` | Entity not found | 404 Not Found |

Both handled by `ProblemDetailsExceptionHandler` for consistent error responses.

---

## Adding New Features Checklist

1. **Contract Model** (if new configuration):
   - Add to `Rates.Contracts` with XML docs
   - Add corresponding Core entity
   - Update mappers (ToCore + ToContract)

2. **Calculation Logic** (if affects GetRates):
   - Implement in appropriate Generator class
   - Update `CalculationDetails` response if needed
   - Add integration tests in `GivenGetRates.cs`

3. **External Service** (if new integration):
   - Create interface in `Core/Services`
   - Implement with `HttpClient`
   - Register with `AddHttpClient<>()` in DI
   - Mock with `HttpMessageHandler.SetResponse()` in tests

4. **Repository** (if new data access):
   - Extend `BaseMongoRepository`
   - Add interface to `IRepository<>`
   - Register in `Core/DependencyInjection/Register.cs`
