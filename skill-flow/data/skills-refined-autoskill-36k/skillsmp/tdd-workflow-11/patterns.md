# Advanced TDD Patterns

## Builder Pattern for Test Data

```csharp
public class OrderBuilder
{
    private Guid _id = Guid.NewGuid();
    private List<OrderItem> _items = new();
    private OrderStatus _status = OrderStatus.Pending;
    private decimal _discount = 0;

    public OrderBuilder WithId(Guid id)
    {
        _id = id;
        return this;
    }

    public OrderBuilder WithItem(string product, int quantity, decimal price)
    {
        _items.Add(new OrderItem(product, quantity, price));
        return this;
    }

    public OrderBuilder WithStatus(OrderStatus status)
    {
        _status = status;
        return this;
    }

    public OrderBuilder WithDiscount(decimal discount)
    {
        _discount = discount;
        return this;
    }

    public Order Build()
    {
        return new Order(_id, _items, _status, _discount);
    }

    // Factory methods for common scenarios
    public static OrderBuilder ValidOrder() => new OrderBuilder()
        .WithItem("Product A", 2, 10.00m)
        .WithItem("Product B", 1, 25.00m);

    public static OrderBuilder EmptyOrder() => new OrderBuilder();

    public static OrderBuilder CompletedOrder() => ValidOrder()
        .WithStatus(OrderStatus.Completed);
}

// Usage in tests
[Fact]
public void CalculateTotal_WithMultipleItems_ReturnsSumOfItems()
{
    var order = OrderBuilder.ValidOrder()
        .WithItem("Extra", 1, 5.00m)
        .Build();

    var total = order.CalculateTotal();

    Assert.Equal(50.00m, total);
}
```

## Object Mother Pattern

```csharp
public static class TestUsers
{
    public static User AdminUser() => new User
    {
        Id = Guid.Parse("11111111-1111-1111-1111-111111111111"),
        Email = "admin@test.com",
        Role = UserRole.Admin
    };

    public static User RegularUser() => new User
    {
        Id = Guid.Parse("22222222-2222-2222-2222-222222222222"),
        Email = "user@test.com",
        Role = UserRole.Regular
    };

    public static User GuestUser() => new User
    {
        Id = Guid.NewGuid(),
        Email = "guest@test.com",
        Role = UserRole.Guest
    };
}

// Usage
[Fact]
public void DeleteUser_AsAdmin_Succeeds()
{
    var admin = TestUsers.AdminUser();
    var target = TestUsers.RegularUser();

    var result = _sut.DeleteUser(admin, target.Id);

    Assert.True(result.IsSuccess);
}
```

## Parameterized Tests

```csharp
public class DiscountCalculatorTests
{
    [Theory]
    [InlineData(100, 10, 90)]   // 10% off $100 = $90
    [InlineData(200, 15, 170)]  // 15% off $200 = $170
    [InlineData(50, 0, 50)]     // 0% off $50 = $50
    public void ApplyDiscount_WithVariousInputs_ReturnsCorrectTotal(
        decimal subtotal, decimal discountPercent, decimal expected)
    {
        var result = DiscountCalculator.Apply(subtotal, discountPercent);
        Assert.Equal(expected, result);
    }

    [Theory]
    [MemberData(nameof(DiscountScenarios))]
    public void ApplyDiscount_WithComplexScenarios_ReturnsCorrectTotal(
        DiscountTestCase testCase)
    {
        var result = DiscountCalculator.Apply(testCase.Subtotal, testCase.Discount);
        Assert.Equal(testCase.Expected, result);
    }

    public static IEnumerable<object[]> DiscountScenarios()
    {
        yield return new object[] { new DiscountTestCase(100, 10, 90, "Standard discount") };
        yield return new object[] { new DiscountTestCase(0, 50, 0, "Zero subtotal") };
        yield return new object[] { new DiscountTestCase(100, 100, 0, "Full discount") };
    }
}

public record DiscountTestCase(decimal Subtotal, decimal Discount, decimal Expected, string Description);
```

## Fixture Pattern (Shared Context)

```csharp
public class DatabaseFixture : IDisposable
{
    public DbContext Context { get; }

    public DatabaseFixture()
    {
        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseInMemoryDatabase(Guid.NewGuid().ToString())
            .Options;
        Context = new AppDbContext(options);
        SeedTestData();
    }

    private void SeedTestData()
    {
        Context.Users.Add(TestUsers.AdminUser());
        Context.Users.Add(TestUsers.RegularUser());
        Context.SaveChanges();
    }

    public void Dispose()
    {
        Context.Dispose();
    }
}

[CollectionDefinition("Database")]
public class DatabaseCollection : ICollectionFixture<DatabaseFixture> { }

[Collection("Database")]
public class UserRepositoryTests
{
    private readonly DatabaseFixture _fixture;

    public UserRepositoryTests(DatabaseFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public void GetById_WhenUserExists_ReturnsUser()
    {
        var repo = new UserRepository(_fixture.Context);
        var result = repo.GetById(TestUsers.AdminUser().Id);
        Assert.NotNull(result);
    }
}
```

## Specification Pattern for Complex Assertions

```csharp
public static class OrderAssertions
{
    public static void ShouldBeValid(this Order order)
    {
        Assert.NotEqual(Guid.Empty, order.Id);
        Assert.NotEmpty(order.Items);
        Assert.True(order.Total > 0);
    }

    public static void ShouldHaveStatus(this Order order, OrderStatus expected)
    {
        Assert.Equal(expected, order.Status);
    }

    public static void ShouldContainItem(this Order order, string productName)
    {
        Assert.Contains(order.Items, i => i.ProductName == productName);
    }
}

// Usage
[Fact]
public void CreateOrder_WithValidItems_CreatesValidOrder()
{
    var order = _sut.CreateOrder(items);

    order.ShouldBeValid();
    order.ShouldHaveStatus(OrderStatus.Pending);
    order.ShouldContainItem("Product A");
}
```

## Fake Repository Pattern

```csharp
public class InMemoryOrderRepository : IOrderRepository
{
    private readonly Dictionary<Guid, Order> _orders = new();

    public Task<Order?> GetByIdAsync(Guid id)
    {
        _orders.TryGetValue(id, out var order);
        return Task.FromResult(order);
    }

    public Task<IReadOnlyList<Order>> GetAllAsync()
    {
        return Task.FromResult<IReadOnlyList<Order>>(_orders.Values.ToList());
    }

    public Task AddAsync(Order order)
    {
        _orders[order.Id] = order;
        return Task.CompletedTask;
    }

    public Task UpdateAsync(Order order)
    {
        _orders[order.Id] = order;
        return Task.CompletedTask;
    }

    public Task DeleteAsync(Guid id)
    {
        _orders.Remove(id);
        return Task.CompletedTask;
    }

    // Test helpers
    public void Clear() => _orders.Clear();
    public int Count => _orders.Count;
    public bool Contains(Guid id) => _orders.ContainsKey(id);
}
```

## Auto-Mocking Container

```csharp
public class AutoMocker<T> where T : class
{
    private readonly Dictionary<Type, object> _mocks = new();

    public Mock<TDependency> GetMock<TDependency>() where TDependency : class
    {
        var type = typeof(TDependency);
        if (!_mocks.ContainsKey(type))
        {
            _mocks[type] = new Mock<TDependency>();
        }
        return (Mock<TDependency>)_mocks[type];
    }

    public T CreateInstance()
    {
        var constructor = typeof(T).GetConstructors()
            .OrderByDescending(c => c.GetParameters().Length)
            .First();

        var parameters = constructor.GetParameters()
            .Select(p => GetOrCreateMock(p.ParameterType))
            .ToArray();

        return (T)constructor.Invoke(parameters);
    }

    private object GetOrCreateMock(Type type)
    {
        if (!_mocks.ContainsKey(type))
        {
            var mockType = typeof(Mock<>).MakeGenericType(type);
            var mock = Activator.CreateInstance(mockType);
            _mocks[type] = mock!;
        }
        return ((dynamic)_mocks[type]).Object;
    }
}

// Usage
public class OrderServiceTests
{
    private readonly AutoMocker<OrderService> _mocker = new();
    private readonly OrderService _sut;

    public OrderServiceTests()
    {
        _sut = _mocker.CreateInstance();
    }

    [Fact]
    public void CreateOrder_CallsRepository()
    {
        var order = OrderBuilder.ValidOrder().Build();

        _sut.CreateOrder(order);

        _mocker.GetMock<IOrderRepository>()
            .Verify(r => r.AddAsync(order), Times.Once);
    }
}
```

## Testing Async Code

```csharp
[Fact]
public async Task GetOrderAsync_WhenExists_ReturnsOrder()
{
    // Arrange
    var orderId = Guid.NewGuid();
    var expectedOrder = OrderBuilder.ValidOrder().WithId(orderId).Build();
    _mockRepository
        .Setup(r => r.GetByIdAsync(orderId))
        .ReturnsAsync(expectedOrder);

    // Act
    var result = await _sut.GetOrderAsync(orderId);

    // Assert
    Assert.Equal(expectedOrder, result);
}

[Fact]
public async Task ProcessOrderAsync_WhenFails_ThrowsException()
{
    _mockProcessor
        .Setup(p => p.ProcessAsync(It.IsAny<Order>()))
        .ThrowsAsync(new ProcessingException("Failed"));

    await Assert.ThrowsAsync<ProcessingException>(
        () => _sut.ProcessOrderAsync(new Order()));
}
```

## Testing Events and Callbacks

```csharp
[Fact]
public void ProcessOrder_RaisesOrderProcessedEvent()
{
    // Arrange
    var eventRaised = false;
    Order? raisedOrder = null;

    _sut.OrderProcessed += (sender, args) =>
    {
        eventRaised = true;
        raisedOrder = args.Order;
    };

    var order = OrderBuilder.ValidOrder().Build();

    // Act
    _sut.Process(order);

    // Assert
    Assert.True(eventRaised);
    Assert.Equal(order, raisedOrder);
}

[Fact]
public void ExecuteWithCallback_InvokesCallback()
{
    // Arrange
    var callbackInvoked = false;
    var callback = new Action<Result>(r => callbackInvoked = true);

    // Act
    _sut.ExecuteWithCallback(callback);

    // Assert
    Assert.True(callbackInvoked);
}
```

## Testing Time-Dependent Code

```csharp
public interface IDateTimeProvider
{
    DateTime Now { get; }
    DateTime UtcNow { get; }
}

public class SystemDateTimeProvider : IDateTimeProvider
{
    public DateTime Now => DateTime.Now;
    public DateTime UtcNow => DateTime.UtcNow;
}

public class TestDateTimeProvider : IDateTimeProvider
{
    public DateTime Now { get; set; } = new DateTime(2024, 1, 15, 10, 0, 0);
    public DateTime UtcNow { get; set; } = new DateTime(2024, 1, 15, 10, 0, 0, DateTimeKind.Utc);

    public void Advance(TimeSpan duration)
    {
        Now = Now.Add(duration);
        UtcNow = UtcNow.Add(duration);
    }
}

// Usage
[Fact]
public void CreateOrder_SetsCreatedDateToNow()
{
    var dateProvider = new TestDateTimeProvider();
    var sut = new OrderService(dateProvider);

    var order = sut.CreateOrder();

    Assert.Equal(dateProvider.Now, order.CreatedAt);
}

[Fact]
public void IsExpired_AfterExpiration_ReturnsTrue()
{
    var dateProvider = new TestDateTimeProvider();
    var order = new Order { ExpiresAt = dateProvider.Now.AddHours(1) };

    dateProvider.Advance(TimeSpan.FromHours(2));

    Assert.True(order.IsExpired(dateProvider));
}
```
