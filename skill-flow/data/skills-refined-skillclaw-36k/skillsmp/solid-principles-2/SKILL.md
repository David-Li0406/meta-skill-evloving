---
name: solid-principles
description: SOLID design principles for .NET. Use when designing classes, interfaces, and object relationships. Ensures maintainable, testable, and extensible code.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# SOLID Principles for .NET

## Overview

SOLID is an acronym for five principles that lead to maintainable, testable, and extensible object-oriented code.

| Principle | Summary |
|-----------|---------|
| **S** - Single Responsibility | One class, one reason to change |
| **O** - Open/Closed | Open for extension, closed for modification |
| **L** - Liskov Substitution | Subtypes must be substitutable for base types |
| **I** - Interface Segregation | Many specific interfaces > one general interface |
| **D** - Dependency Inversion | Depend on abstractions, not concretions |

---

## S - Single Responsibility Principle (SRP)

> A class should have only one reason to change.

### Violation Example
```csharp
// BAD: Multiple responsibilities
public class OrderService
{
    public Order CreateOrder(OrderRequest request)
    {
        // Validation logic
        if (string.IsNullOrEmpty(request.CustomerEmail))
            throw new ValidationException("Email required");

        // Business logic
        var order = new Order
        {
            Id = Guid.NewGuid(),
            Items = request.Items,
            Total = CalculateTotal(request.Items)
        };

        // Persistence logic
        using var connection = new SqlConnection(_connectionString);
        connection.Execute("INSERT INTO Orders...", order);

        // Notification logic
        var emailBody = $"Order {order.Id} confirmed!";
        _smtpClient.Send(request.CustomerEmail, "Order Confirmed", emailBody);

        // Logging logic
        File.AppendAllText("orders.log", $"{DateTime.Now}: Order {order.Id} created");

        return order;
    }
}
```

### Correct Implementation
```csharp
// GOOD: Single responsibility per class
public class OrderService
{
    private readonly IOrderValidator _validator;
    private readonly IOrderRepository _repository;
    private readonly IOrderNotifier _notifier;
    private readonly ILogger<OrderService> _logger;

    public OrderService(
        IOrderValidator validator,
        IOrderRepository repository,
        IOrderNotifier notifier,
        ILogger<OrderService> logger)
    {
        _validator = validator;
        _repository = repository;
        _notifier = notifier;
        _logger = logger;
    }

    public async Task<Order> CreateOrderAsync(OrderRequest request)
    {
        _validator.Validate(request);

        var order = Order.Create(request.Items);

        await _repository.AddAsync(order);
        await _notifier.NotifyOrderCreatedAsync(order, request.CustomerEmail);

        _logger.LogInformation("Order {OrderId} created", order.Id);

        return order;
    }
}

// Each concern in its own class
public class OrderValidator : IOrderValidator
{
    public void Validate(OrderRequest request)
    {
        if (string.IsNullOrEmpty(request.CustomerEmail))
            throw new ValidationException("Email required");
    }
}

public class OrderRepository : IOrderRepository
{
    private readonly DbContext _context;

    public async Task AddAsync(Order order)
    {
        _context.Orders.Add(order);
        await _context.SaveChangesAsync();
    }
}

public class EmailOrderNotifier : IOrderNotifier
{
    private readonly IEmailService _emailService;

    public async Task NotifyOrderCreatedAsync(Order order, string email)
    {
        await _emailService.SendAsync(email, "Order Confirmed", $"Order {order.Id} confirmed!");
    }
}
```

### SRP Test: Ask These Questions
1. Can I describe what the class does without using "and"?
2. Would different stakeholders want changes to this class?
3. Does the class have more than 200-300 lines?

---

## O - Open/Closed Principle (OCP)

> Software entities should be open for extension but closed for modification.

### Violation Example
```csharp
// BAD: Must modify class to add new discount types
public class DiscountCalculator
{
    public decimal Calculate(Order order, string discountType)
    {
        switch (discountType)
        {
            case "percentage":
                return order.Total * 0.1m;
            case "fixed":
                return 10m;
            case "loyalty":
                return order.Total * 0.15m;
            // Every new discount requires modifying this class
            default:
                return 0m;
        }
    }
}
```

### Correct Implementation
```csharp
// GOOD: Extensible without modification
public interface IDiscountStrategy
{
    decimal Calculate(Order order);
}

public class PercentageDiscount : IDiscountStrategy
{
    private readonly decimal _percentage;

    public PercentageDiscount(decimal percentage) => _percentage = percentage;

    public decimal Calculate(Order order) => order.Total * _percentage;
}

public class FixedDiscount : IDiscountStrategy
{
    private readonly decimal _amount;

    public FixedDiscount(decimal amount) => _amount = amount;

    public decimal Calculate(Order order) => Math.Min(_amount, order.Total);
}

public class LoyaltyDiscount : IDiscountStrategy
{
    private readonly ILoyaltyService _loyaltyService;

    public LoyaltyDiscount(ILoyaltyService loyaltyService) => _loyaltyService = loyaltyService;

    public decimal Calculate(Order order)
    {
        var tier = _loyaltyService.GetCustomerTier(order.CustomerId);
        return tier switch
        {
            LoyaltyTier.Gold => order.Total * 0.15m,
            LoyaltyTier.Silver => order.Total * 0.10m,
            _ => 0m
        };
    }
}

// New discounts added without touching existing code
public class BulkDiscount : IDiscountStrategy
{
    public decimal Calculate(Order order)
    {
        if (order.Items.Count >= 10)
            return order.Total * 0.20m;
        return 0m;
    }
}

// Calculator is closed for modification
public class DiscountCalculator
{
    public decimal Calculate(Order order, IDiscountStrategy strategy)
    {
        return strategy.Calculate(order);
    }
}
```

### OCP Patterns
- Strategy Pattern (as shown above)
- Template Method Pattern
- Decorator Pattern
- Plugin Architecture

---

## L - Liskov Substitution Principle (LSP)

> Objects of a superclass should be replaceable with objects of its subclasses without breaking the application.

### Violation Example
```csharp
// BAD: Square violates Rectangle's contract
public class Rectangle
{
    public virtual int Width { get; set; }
    public virtual int Height { get; set; }

    public int CalculateArea() => Width * Height;
}

public class Square : Rectangle
{
    public override int Width
    {
        get => base.Width;
        set
        {
            base.Width = value;
            base.Height = value; // Unexpected side effect!
        }
    }

    public override int Height
    {
        get => base.Height;
        set
        {
            base.Height = value;
            base.Width = value; // Unexpected side effect!
        }
    }
}

// This test fails for Square!
[Fact]
public void Rectangle_SetDimensions_CalculatesCorrectArea()
{
    Rectangle rect = new Square(); // Substitution
    rect.Width = 5;
    rect.Height = 4;
    Assert.Equal(20, rect.CalculateArea()); // Fails! Returns 16
}
```

### Correct Implementation
```csharp
// GOOD: Separate abstractions
public interface IShape
{
    int CalculateArea();
}

public class Rectangle : IShape
{
    public int Width { get; }
    public int Height { get; }

    public Rectangle(int width, int height)
    {
        Width = width;
        Height = height;
    }

    public int CalculateArea() => Width * Height;
}

public class Square : IShape
{
    public int Side { get; }

    public Square(int side) => Side = side;

    public int CalculateArea() => Side * Side;
}

// Both work correctly with the abstraction
public class AreaCalculator
{
    public int TotalArea(IEnumerable<IShape> shapes)
    {
        return shapes.Sum(s => s.CalculateArea());
    }
}
```

### LSP Rules
1. Preconditions cannot be strengthened in subtype
2. Postconditions cannot be weakened in subtype
3. Invariants must be preserved in subtype
4. History constraint (no unexpected state changes)

### Common LSP Violations
```csharp
// BAD: Throwing NotSupportedException
public class ReadOnlyCollection<T> : ICollection<T>
{
    public void Add(T item) => throw new NotSupportedException();
}

// BAD: Ignoring base class behavior
public class CachedRepository : Repository
{
    public override void Save(Entity entity)
    {
        // Doesn't call base.Save() - breaks persistence!
        _cache.Add(entity);
    }
}
```

---

## I - Interface Segregation Principle (ISP)

> Clients should not be forced to depend on interfaces they do not use.

### Violation Example
```csharp
// BAD: Fat interface
public interface IWorker
{
    void Work();
    void Eat();
    void Sleep();
    void AttendMeeting();
    void WriteCode();
    void ManageTeam();
}

// Robot can't eat or sleep!
public class Robot : IWorker
{
    public void Work() { /* OK */ }
    public void Eat() => throw new NotSupportedException();
    public void Sleep() => throw new NotSupportedException();
    public void AttendMeeting() => throw new NotSupportedException();
    public void WriteCode() { /* OK */ }
    public void ManageTeam() => throw new NotSupportedException();
}
```

### Correct Implementation
```csharp
// GOOD: Segregated interfaces
public interface IWorkable
{
    void Work();
}

public interface IFeedable
{
    void Eat();
}

public interface ISleepable
{
    void Sleep();
}

public interface IMeetingAttendee
{
    void AttendMeeting();
}

public interface IDeveloper : IWorkable
{
    void WriteCode();
}

public interface IManager : IWorkable, IMeetingAttendee
{
    void ManageTeam();
}

// Clean implementations
public class HumanDeveloper : IDeveloper, IFeedable, ISleepable
{
    public void Work() { }
    public void WriteCode() { }
    public void Eat() { }
    public void Sleep() { }
}

public class Robot : IDeveloper
{
    public void Work() { }
    public void WriteCode() { }
    // No forced empty implementations!
}
```

### Repository ISP Example
```csharp
// BAD: Monolithic repository
public interface IRepository<T>
{
    T GetById(int id);
    IEnumerable<T> GetAll();
    void Add(T entity);
    void Update(T entity);
    void Delete(T entity);
    IEnumerable<T> Find(Expression<Func<T, bool>> predicate);
    void BulkInsert(IEnumerable<T> entities);
    void ExecuteRawSql(string sql);
}

// GOOD: Segregated repositories
public interface IReadRepository<T>
{
    T? GetById(int id);
    IEnumerable<T> GetAll();
}

public interface IWriteRepository<T>
{
    void Add(T entity);
    void Update(T entity);
    void Delete(T entity);
}

public interface IQueryRepository<T>
{
    IEnumerable<T> Find(Expression<Func<T, bool>> predicate);
}

// Compose as needed
public interface IOrderRepository : IReadRepository<Order>, IWriteRepository<Order> { }

public interface IReportRepository : IReadRepository<Report>, IQueryRepository<Report> { }
```

---

## D - Dependency Inversion Principle (DIP)

> High-level modules should not depend on low-level modules. Both should depend on abstractions.

### Violation Example
```csharp
// BAD: High-level depends on low-level
public class OrderService
{
    private readonly SqlOrderRepository _repository; // Concrete!
    private readonly SmtpEmailSender _emailSender;   // Concrete!

    public OrderService()
    {
        _repository = new SqlOrderRepository("connection-string");
        _emailSender = new SmtpEmailSender("smtp.server.com");
    }

    public void CreateOrder(Order order)
    {
        _repository.Save(order);
        _emailSender.Send(order.CustomerEmail, "Order Created");
    }
}
```

### Correct Implementation
```csharp
// GOOD: Depend on abstractions
public interface IOrderRepository
{
    Task SaveAsync(Order order);
    Task<Order?> GetByIdAsync(Guid id);
}

public interface INotificationService
{
    Task SendAsync(string recipient, string subject, string message);
}

public class OrderService
{
    private readonly IOrderRepository _repository;
    private readonly INotificationService _notificationService;

    // Dependencies injected via constructor
    public OrderService(
        IOrderRepository repository,
        INotificationService notificationService)
    {
        _repository = repository;
        _notificationService = notificationService;
    }

    public async Task CreateOrderAsync(Order order)
    {
        await _repository.SaveAsync(order);
        await _notificationService.SendAsync(
            order.CustomerEmail,
            "Order Created",
            $"Your order {order.Id} has been created.");
    }
}

// Low-level modules implement abstractions
public class SqlOrderRepository : IOrderRepository
{
    private readonly DbContext _context;

    public SqlOrderRepository(DbContext context) => _context = context;

    public async Task SaveAsync(Order order)
    {
        _context.Orders.Add(order);
        await _context.SaveChangesAsync();
    }

    public async Task<Order?> GetByIdAsync(Guid id)
    {
        return await _context.Orders.FindAsync(id);
    }
}

public class EmailNotificationService : INotificationService
{
    private readonly IEmailClient _emailClient;

    public EmailNotificationService(IEmailClient emailClient) => _emailClient = emailClient;

    public async Task SendAsync(string recipient, string subject, string message)
    {
        await _emailClient.SendEmailAsync(recipient, subject, message);
    }
}

// Registration in DI container
services.AddScoped<IOrderRepository, SqlOrderRepository>();
services.AddScoped<INotificationService, EmailNotificationService>();
services.AddScoped<OrderService>();
```

### DIP Benefits
1. **Testability**: Mock dependencies easily
2. **Flexibility**: Swap implementations without changing consumers
3. **Maintainability**: Changes isolated to implementations
4. **Parallel development**: Teams work on interfaces

---

## Quick Reference

| Principle | Violation Sign | Fix |
|-----------|----------------|-----|
| SRP | Class has multiple reasons to change | Extract classes by responsibility |
| OCP | Adding features requires modifying existing code | Use abstractions and composition |
| LSP | Subclass can't substitute base class | Fix inheritance or use composition |
| ISP | Implementations throw NotSupported | Split large interfaces |
| DIP | High-level creates low-level instances | Inject dependencies via interfaces |

See [examples.md](examples.md) for more comprehensive examples.
