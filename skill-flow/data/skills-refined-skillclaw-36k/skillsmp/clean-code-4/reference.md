# Clean Code Reference

## Naming Conventions

### Classes and Methods
```csharp
// BAD
public class Mgr { }
public void DoIt() { }
public int Calc(int x) { }

// GOOD
public class OrderManager { }
public void ProcessPayment() { }
public int CalculateTotalDiscount(int orderId) { }
```

### Boolean Names
```csharp
// BAD
bool flag;
bool open;
bool status;

// GOOD
bool isActive;
bool hasPermission;
bool canExecute;
bool shouldRetry;
```

### Collections
```csharp
// BAD
List<User> list;
Dictionary<int, Order> dict;

// GOOD
List<User> activeUsers;
Dictionary<int, Order> ordersByCustomerId;
```

### Avoid Mental Mapping
```csharp
// BAD
for (int i = 0; i < users.Length; i++)
    for (int j = 0; j < users[i].Orders.Length; j++)
        Process(users[i].Orders[j]);

// GOOD
foreach (var user in users)
    foreach (var order in user.Orders)
        Process(order);
```

## Function Design

### Single Level of Abstraction
```csharp
// BAD: Mixed abstraction levels
public void ProcessOrder(Order order)
{
    // High level
    ValidateOrder(order);

    // Low level - detail leak
    using var conn = new SqlConnection(_connectionString);
    conn.Open();
    var cmd = new SqlCommand("INSERT INTO Orders...", conn);
    cmd.ExecuteNonQuery();

    // High level again
    SendConfirmationEmail(order);
}

// GOOD: Consistent abstraction
public async Task ProcessOrderAsync(Order order)
{
    await ValidateOrderAsync(order);
    await SaveOrderAsync(order);
    await NotifyCustomerAsync(order);
}
```

### Prefer Exceptions Over Error Codes
```csharp
// BAD
public int CreateUser(User user)
{
    if (user == null) return -1;
    if (string.IsNullOrEmpty(user.Email)) return -2;
    if (UserExists(user.Email)) return -3;
    // ...
    return 0; // Success
}

// GOOD
public void CreateUser(User user)
{
    ArgumentNullException.ThrowIfNull(user);

    if (string.IsNullOrEmpty(user.Email))
        throw new ValidationException("Email is required");

    if (UserExists(user.Email))
        throw new DuplicateUserException(user.Email);

    // ...
}
```

### Guard Clauses
```csharp
// BAD: Deep nesting
public decimal CalculateDiscount(Order order)
{
    if (order != null)
    {
        if (order.Customer != null)
        {
            if (order.Customer.IsPremium)
            {
                if (order.Total > 100)
                {
                    return order.Total * 0.2m;
                }
            }
        }
    }
    return 0;
}

// GOOD: Guard clauses
public decimal CalculateDiscount(Order order)
{
    if (order?.Customer is not { IsPremium: true })
        return 0;

    if (order.Total <= 100)
        return 0;

    return order.Total * 0.2m;
}
```

## Error Handling

### Specific Exceptions
```csharp
// BAD
catch (Exception ex)
{
    Log(ex);
    throw;
}

// GOOD
catch (SqlException ex) when (ex.Number == 2627)
{
    throw new DuplicateEntityException("Entity already exists", ex);
}
catch (SqlException ex) when (ex.Number == 547)
{
    throw new ForeignKeyViolationException("Related entity not found", ex);
}
catch (SqlException ex)
{
    _logger.LogError(ex, "Database error occurred");
    throw new DataAccessException("Database operation failed", ex);
}
```

### Don't Return Null for Collections
```csharp
// BAD
public List<Order>? GetOrdersByCustomer(int customerId)
{
    var orders = _repository.Find(customerId);
    return orders.Any() ? orders : null;
}

// GOOD
public IReadOnlyList<Order> GetOrdersByCustomer(int customerId)
{
    return _repository.Find(customerId);  // Returns empty list if none
}
```

### Result Pattern for Expected Failures
```csharp
// For operations that can fail in expected ways
public record Result<T>
{
    public bool IsSuccess { get; init; }
    public T? Value { get; init; }
    public string? Error { get; init; }

    public static Result<T> Success(T value) =>
        new() { IsSuccess = true, Value = value };

    public static Result<T> Failure(string error) =>
        new() { IsSuccess = false, Error = error };
}

public Result<User> AuthenticateUser(string email, string password)
{
    var user = _userRepository.GetByEmail(email);
    if (user == null)
        return Result<User>.Failure("Invalid credentials");

    if (!VerifyPassword(password, user.PasswordHash))
        return Result<User>.Failure("Invalid credentials");

    return Result<User>.Success(user);
}
```

## Immutability

### Prefer Immutable Objects
```csharp
// BAD: Mutable
public class OrderItem
{
    public int ProductId { get; set; }
    public int Quantity { get; set; }
    public decimal Price { get; set; }
}

// GOOD: Immutable
public record OrderItem(int ProductId, int Quantity, decimal Price)
{
    public decimal Total => Quantity * Price;

    public OrderItem WithQuantity(int newQuantity) =>
        this with { Quantity = newQuantity };
}
```

### Collection Encapsulation
```csharp
// BAD: Exposing mutable collection
public class Order
{
    public List<OrderItem> Items { get; set; } = new();
}

// External code can do:
order.Items.Clear();
order.Items = null;

// GOOD: Encapsulated collection
public class Order
{
    private readonly List<OrderItem> _items = new();

    public IReadOnlyList<OrderItem> Items => _items.AsReadOnly();

    public void AddItem(OrderItem item)
    {
        ArgumentNullException.ThrowIfNull(item);
        _items.Add(item);
    }

    public void RemoveItem(int productId)
    {
        _items.RemoveAll(i => i.ProductId == productId);
    }
}
```

## Dependency Injection Patterns

### Constructor Injection (Preferred)
```csharp
public class OrderService
{
    private readonly IOrderRepository _repository;
    private readonly ILogger<OrderService> _logger;

    public OrderService(IOrderRepository repository, ILogger<OrderService> logger)
    {
        _repository = repository ?? throw new ArgumentNullException(nameof(repository));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
    }
}
```

### Avoid Service Locator
```csharp
// BAD: Service locator anti-pattern
public class OrderService
{
    public void Process()
    {
        var repo = ServiceLocator.Get<IOrderRepository>();
        var logger = ServiceLocator.Get<ILogger>();
    }
}

// GOOD: Explicit dependencies
public class OrderService
{
    private readonly IOrderRepository _repository;

    public OrderService(IOrderRepository repository)
    {
        _repository = repository;
    }
}
```

## Async/Await Best Practices

### ConfigureAwait
```csharp
// Library code - use ConfigureAwait(false)
public async Task<Order> GetOrderAsync(int id)
{
    var data = await _httpClient.GetAsync($"/orders/{id}").ConfigureAwait(false);
    return await data.Content.ReadFromJsonAsync<Order>().ConfigureAwait(false);
}

// Application code - ConfigureAwait not needed (context flows automatically)
public async Task<IActionResult> GetOrder(int id)
{
    var order = await _orderService.GetOrderAsync(id);
    return Ok(order);
}
```

### Avoid Async Void
```csharp
// BAD: Exceptions are lost
public async void SendNotification()
{
    await _emailService.SendAsync(...);
}

// GOOD: Return Task
public async Task SendNotificationAsync()
{
    await _emailService.SendAsync(...);
}

// Exception: Event handlers can use async void
private async void OnButtonClick(object sender, EventArgs e)
{
    try
    {
        await ProcessAsync();
    }
    catch (Exception ex)
    {
        HandleError(ex);
    }
}
```

### Don't Block on Async
```csharp
// BAD: Deadlock risk
public void Process()
{
    var result = GetDataAsync().Result;  // Blocks!
    var result2 = GetDataAsync().GetAwaiter().GetResult();  // Also blocks!
}

// GOOD: Async all the way
public async Task ProcessAsync()
{
    var result = await GetDataAsync();
}
```

## Code Organization

### Vertical Ordering
```csharp
public class OrderService
{
    // 1. Fields
    private readonly IOrderRepository _repository;
    private readonly ILogger _logger;

    // 2. Constructor
    public OrderService(IOrderRepository repository, ILogger logger)
    {
        _repository = repository;
        _logger = logger;
    }

    // 3. Public methods (high-level first)
    public async Task<Order> CreateOrderAsync(CreateOrderRequest request)
    {
        ValidateRequest(request);
        var order = BuildOrder(request);
        await SaveOrderAsync(order);
        return order;
    }

    // 4. Private methods (called in order they're used)
    private void ValidateRequest(CreateOrderRequest request) { }

    private Order BuildOrder(CreateOrderRequest request) { }

    private async Task SaveOrderAsync(Order order) { }
}
```

### Newspaper Metaphor
- Headline (class name)
- Synopsis (public interface)
- Details (private implementation)
- Supporting details (utility methods)
