---
name: clean-code
description: Clean code principles including DRY, KISS, and YAGNI for .NET. Use when writing or reviewing code to ensure maintainability and simplicity.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Clean Code Principles

## DRY - Don't Repeat Yourself

> Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

### Code Duplication

```csharp
// BAD: Duplicated validation logic
public class UserService
{
    public void CreateUser(string email, string name)
    {
        if (string.IsNullOrWhiteSpace(email) || !email.Contains("@"))
            throw new ArgumentException("Invalid email");
        // ...
    }

    public void UpdateEmail(int userId, string newEmail)
    {
        if (string.IsNullOrWhiteSpace(newEmail) || !newEmail.Contains("@"))
            throw new ArgumentException("Invalid email");
        // ...
    }
}

// GOOD: Single source of truth
public class UserService
{
    private readonly IEmailValidator _emailValidator;

    public void CreateUser(string email, string name)
    {
        _emailValidator.ValidateOrThrow(email);
        // ...
    }

    public void UpdateEmail(int userId, string newEmail)
    {
        _emailValidator.ValidateOrThrow(newEmail);
        // ...
    }
}

public class EmailValidator : IEmailValidator
{
    public bool IsValid(string email) =>
        !string.IsNullOrWhiteSpace(email) && email.Contains("@");

    public void ValidateOrThrow(string email)
    {
        if (!IsValid(email))
            throw new ArgumentException("Invalid email", nameof(email));
    }
}
```

### Magic Numbers and Strings

```csharp
// BAD: Magic values scattered throughout code
public decimal CalculateDiscount(decimal total)
{
    if (total > 100)
        return total * 0.1m;  // What is 100? What is 0.1?
    return 0;
}

public bool IsEligibleForFreeShipping(decimal total)
{
    return total > 100;  // Duplicated magic number!
}

// GOOD: Named constants
public static class OrderThresholds
{
    public const decimal FreeShippingMinimum = 100m;
    public const decimal StandardDiscountRate = 0.10m;
}

public decimal CalculateDiscount(decimal total)
{
    if (total > OrderThresholds.FreeShippingMinimum)
        return total * OrderThresholds.StandardDiscountRate;
    return 0;
}

public bool IsEligibleForFreeShipping(decimal total)
{
    return total > OrderThresholds.FreeShippingMinimum;
}
```

### Configuration Duplication

```csharp
// BAD: Connection strings in multiple places
public class OrderRepository
{
    private readonly string _conn = "Server=prod;Database=Orders;";
}

public class CustomerRepository
{
    private readonly string _conn = "Server=prod;Database=Orders;";
}

// GOOD: Centralized configuration
public class DatabaseOptions
{
    public string ConnectionString { get; set; } = string.Empty;
}

// In startup
services.Configure<DatabaseOptions>(configuration.GetSection("Database"));

// In repositories
public class OrderRepository
{
    private readonly string _connectionString;

    public OrderRepository(IOptions<DatabaseOptions> options)
    {
        _connectionString = options.Value.ConnectionString;
    }
}
```

### When DRY Goes Wrong (WET is Sometimes Better)

```csharp
// Over-DRY: Forced abstraction hurts readability
public T ProcessEntity<T>(T entity, Func<T, bool> validator, Action<T> processor)
    where T : class
{
    if (!validator(entity))
        throw new ValidationException();
    processor(entity);
    return entity;
}

// Better: Some duplication is acceptable for clarity
public Order ProcessOrder(Order order)
{
    ValidateOrder(order);
    SaveOrder(order);
    return order;
}

public Customer ProcessCustomer(Customer customer)
{
    ValidateCustomer(customer);
    SaveCustomer(customer);
    return customer;
}
```

### Rule of Three
Only extract duplication after you've seen it THREE times:
1. First occurrence - just write the code
2. Second occurrence - note it, consider extraction
3. Third occurrence - refactor to remove duplication

---

## KISS - Keep It Simple, Stupid

> The simplest solution is usually the best solution.

### Over-Engineering

```csharp
// BAD: Over-engineered for simple use case
public interface IUserNameFormatter
{
    string Format(User user);
}

public abstract class UserNameFormatterBase : IUserNameFormatter
{
    protected abstract string GetFirstNamePart(User user);
    protected abstract string GetLastNamePart(User user);

    public string Format(User user) =>
        $"{GetFirstNamePart(user)} {GetLastNamePart(user)}";
}

public class StandardUserNameFormatter : UserNameFormatterBase
{
    protected override string GetFirstNamePart(User user) => user.FirstName;
    protected override string GetLastNamePart(User user) => user.LastName;
}

public class UserNameFormatterFactory
{
    public IUserNameFormatter Create(string type) => type switch
    {
        "standard" => new StandardUserNameFormatter(),
        _ => throw new NotSupportedException()
    };
}

// GOOD: Simple and direct
public static class UserExtensions
{
    public static string GetFullName(this User user) =>
        $"{user.FirstName} {user.LastName}";
}
```

### Premature Abstraction

```csharp
// BAD: Abstraction for one implementation
public interface IOrderIdGenerator
{
    string Generate();
}

public class GuidOrderIdGenerator : IOrderIdGenerator
{
    public string Generate() => Guid.NewGuid().ToString();
}

// Registration
services.AddSingleton<IOrderIdGenerator, GuidOrderIdGenerator>();

// GOOD: Direct until you need flexibility
public class Order
{
    public string Id { get; } = Guid.NewGuid().ToString();
}

// Add abstraction ONLY when you need a second implementation
```

### Complex LINQ vs Simple Loops

```csharp
// BAD: Hard to understand nested LINQ
var result = orders
    .Where(o => o.Status == OrderStatus.Completed)
    .GroupBy(o => o.CustomerId)
    .Select(g => new
    {
        CustomerId = g.Key,
        TotalSpent = g.Sum(o => o.Total),
        OrderCount = g.Count(),
        AverageOrder = g.Average(o => o.Total)
    })
    .Where(x => x.TotalSpent > 1000)
    .OrderByDescending(x => x.TotalSpent)
    .Take(10)
    .SelectMany(x => customers.Where(c => c.Id == x.CustomerId)
        .Select(c => new CustomerReport
        {
            Name = c.Name,
            Email = c.Email,
            TotalSpent = x.TotalSpent,
            OrderCount = x.OrderCount
        }))
    .ToList();

// GOOD: Break into readable steps
var completedOrders = orders.Where(o => o.Status == OrderStatus.Completed);

var customerOrderSummaries = completedOrders
    .GroupBy(o => o.CustomerId)
    .Select(g => new CustomerOrderSummary(
        CustomerId: g.Key,
        TotalSpent: g.Sum(o => o.Total),
        OrderCount: g.Count()))
    .Where(s => s.TotalSpent > 1000)
    .OrderByDescending(s => s.TotalSpent)
    .Take(10)
    .ToList();

var customerLookup = customers.ToDictionary(c => c.Id);

var reports = customerOrderSummaries
    .Select(s => CreateReport(s, customerLookup[s.CustomerId]))
    .ToList();
```

### Boolean Parameters

```csharp
// BAD: What does 'true' mean?
SendEmail(user, "Welcome!", true, false, true);

// GOOD: Named parameters or dedicated methods
SendEmail(user, "Welcome!",
    isHtml: true,
    includeAttachments: false,
    trackOpens: true);

// Even better: Specific methods
SendWelcomeEmail(user);
SendPasswordResetEmail(user);
```

### Excessive Inheritance

```csharp
// BAD: Deep inheritance hierarchy
public abstract class Entity { }
public abstract class AuditableEntity : Entity { }
public abstract class SoftDeletableAuditableEntity : AuditableEntity { }
public class Order : SoftDeletableAuditableEntity { }

// GOOD: Composition and interfaces
public interface IAuditable
{
    DateTime CreatedAt { get; }
    DateTime? ModifiedAt { get; }
}

public interface ISoftDeletable
{
    bool IsDeleted { get; }
    DateTime? DeletedAt { get; }
}

public class Order : IAuditable, ISoftDeletable
{
    public DateTime CreatedAt { get; init; }
    public DateTime? ModifiedAt { get; private set; }
    public bool IsDeleted { get; private set; }
    public DateTime? DeletedAt { get; private set; }
}
```

---

## YAGNI - You Aren't Gonna Need It

> Don't implement something until it is necessary.

### Feature Creep

```csharp
// BAD: Building for hypothetical future requirements
public class UserService
{
    public User CreateUser(
        string email,
        string name,
        string? middleName = null,           // No requirement for this
        string? suffix = null,                // No requirement for this
        string? preferredName = null,         // No requirement for this
        bool enableTwoFactor = false,         // No requirement for this
        string? backupEmail = null,           // No requirement for this
        Dictionary<string, string>? metadata = null)  // "Might need it later"
    {
        // ...
    }
}

// GOOD: Only what's needed now
public class UserService
{
    public User CreateUser(string email, string name)
    {
        return new User
        {
            Id = Guid.NewGuid(),
            Email = email,
            Name = name,
            CreatedAt = DateTime.UtcNow
        };
    }
}
```

### Unnecessary Flexibility

```csharp
// BAD: Configurable everything (but we only use JSON)
public interface ISerializer
{
    string Serialize<T>(T obj);
    T Deserialize<T>(string data);
}

public class JsonSerializer : ISerializer { }
public class XmlSerializer : ISerializer { }
public class YamlSerializer : ISerializer { }
public class BinarySerializer : ISerializer { }
public class MessagePackSerializer : ISerializer { }

public class SerializerFactory
{
    public ISerializer Create(string format) => // ...
}

// GOOD: Use what you need
public static class JsonHelper
{
    private static readonly JsonSerializerOptions Options = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
    };

    public static string Serialize<T>(T obj) =>
        System.Text.Json.JsonSerializer.Serialize(obj, Options);

    public static T? Deserialize<T>(string json) =>
        System.Text.Json.JsonSerializer.Deserialize<T>(json, Options);
}
```

### Unused Abstractions

```csharp
// BAD: Interface with single implementation, no plans for others
public interface IEmailSender
{
    Task SendAsync(string to, string subject, string body);
}

public class SmtpEmailSender : IEmailSender
{
    public Task SendAsync(string to, string subject, string body)
    {
        // Only implementation we'll ever have
    }
}

// GOOD: Just use the class directly
public class EmailSender
{
    public async Task SendAsync(string to, string subject, string body)
    {
        // ...
    }
}

// Add interface WHEN you actually need a second implementation
```

### Premature Optimization

```csharp
// BAD: Caching before measuring
public class ProductService
{
    private readonly IMemoryCache _cache;
    private readonly IDistributedCache _distributedCache;
    private readonly IProductRepository _repository;

    public async Task<Product?> GetByIdAsync(int id)
    {
        var cacheKey = $"product_{id}";

        // Check L1 cache
        if (_cache.TryGetValue(cacheKey, out Product? product))
            return product;

        // Check L2 cache
        var cached = await _distributedCache.GetStringAsync(cacheKey);
        if (cached != null)
        {
            product = JsonSerializer.Deserialize<Product>(cached);
            _cache.Set(cacheKey, product, TimeSpan.FromMinutes(5));
            return product;
        }

        // Database fallback
        product = await _repository.GetByIdAsync(id);
        if (product != null)
        {
            var serialized = JsonSerializer.Serialize(product);
            await _distributedCache.SetStringAsync(cacheKey, serialized);
            _cache.Set(cacheKey, product, TimeSpan.FromMinutes(5));
        }

        return product;
    }
}

// GOOD: Start simple, optimize when needed
public class ProductService
{
    private readonly IProductRepository _repository;

    public Task<Product?> GetByIdAsync(int id) =>
        _repository.GetByIdAsync(id);
}

// Add caching AFTER you've identified it as a bottleneck
```

### The Cost of YAGNI Violations

1. **Development time**: Building unused features
2. **Maintenance burden**: More code to maintain
3. **Complexity**: Harder to understand system
4. **Testing overhead**: More tests for unused code
5. **Technical debt**: May become outdated or incompatible

---

## Clean Code Checklist

### Naming
- [ ] Names reveal intent
- [ ] Names are searchable
- [ ] No encoded type information (Hungarian notation)
- [ ] Consistent naming conventions

### Functions
- [ ] Small (< 20 lines preferred)
- [ ] Do one thing
- [ ] One level of abstraction
- [ ] Few parameters (< 3 preferred)
- [ ] No side effects
- [ ] Command/Query separation

### Comments
- [ ] Code is self-documenting
- [ ] Comments explain WHY, not WHAT
- [ ] No commented-out code
- [ ] XML docs for public APIs

### Formatting
- [ ] Consistent indentation
- [ ] Logical grouping of related code
- [ ] Blank lines separate concepts
- [ ] Team style guide followed

### Error Handling
- [ ] Exceptions, not error codes
- [ ] Specific exception types
- [ ] No empty catch blocks
- [ ] Fail fast principle

See [reference.md](reference.md) for more examples.
