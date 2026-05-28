# SOLID Principles - Comprehensive Examples

## Real-World Refactoring: E-Commerce Order System

### Before: SOLID Violations
```csharp
// This class violates ALL SOLID principles
public class OrderProcessor
{
    private readonly string _connectionString;
    private readonly string _smtpServer;

    public OrderProcessor()
    {
        _connectionString = ConfigurationManager.ConnectionStrings["DB"].ConnectionString;
        _smtpServer = ConfigurationManager.AppSettings["SmtpServer"];
    }

    public string ProcessOrder(
        int customerId,
        List<(int productId, int quantity)> items,
        string paymentType)
    {
        // Validation (SRP violation - validation logic)
        if (items == null || items.Count == 0)
            return "Error: No items";

        using var connection = new SqlConnection(_connectionString);
        connection.Open();

        // Get customer (DIP violation - direct SQL dependency)
        var customer = connection.QuerySingle<Customer>(
            "SELECT * FROM Customers WHERE Id = @Id", new { Id = customerId });

        if (customer == null)
            return "Error: Customer not found";

        // Calculate totals (SRP violation - business logic)
        decimal total = 0;
        foreach (var (productId, quantity) in items)
        {
            var product = connection.QuerySingle<Product>(
                "SELECT * FROM Products WHERE Id = @Id", new { Id = productId });
            total += product.Price * quantity;
        }

        // Apply discount (OCP violation - hardcoded discount types)
        decimal discount = 0;
        if (customer.Type == "Gold")
            discount = total * 0.15m;
        else if (customer.Type == "Silver")
            discount = total * 0.10m;
        else if (customer.Type == "Bronze")
            discount = total * 0.05m;
        // Adding new customer types requires modifying this method

        // Process payment (OCP violation - hardcoded payment types)
        bool paymentSuccess;
        if (paymentType == "CreditCard")
        {
            paymentSuccess = ProcessCreditCard(total - discount);
        }
        else if (paymentType == "PayPal")
        {
            paymentSuccess = ProcessPayPal(total - discount);
        }
        else
        {
            return "Error: Unknown payment type";
        }

        if (!paymentSuccess)
            return "Error: Payment failed";

        // Save order (SRP violation - persistence logic)
        var orderId = Guid.NewGuid().ToString();
        connection.Execute(
            "INSERT INTO Orders (Id, CustomerId, Total) VALUES (@Id, @CustomerId, @Total)",
            new { Id = orderId, CustomerId = customerId, Total = total - discount });

        // Send email (SRP violation - notification logic)
        using var smtp = new SmtpClient(_smtpServer);
        smtp.Send("orders@store.com", customer.Email, "Order Confirmed", $"Order {orderId}");

        // Log (SRP violation - logging logic)
        File.AppendAllText("orders.log", $"{DateTime.Now}: Order {orderId} processed\n");

        return orderId;
    }

    private bool ProcessCreditCard(decimal amount) { /* ... */ return true; }
    private bool ProcessPayPal(decimal amount) { /* ... */ return true; }
}
```

### After: SOLID-Compliant Design

```csharp
// === ABSTRACTIONS (DIP) ===

public interface IOrderRepository
{
    Task<Order> CreateAsync(Order order);
}

public interface ICustomerRepository
{
    Task<Customer?> GetByIdAsync(int id);
}

public interface IProductRepository
{
    Task<Product?> GetByIdAsync(int id);
}

public interface IDiscountStrategy
{
    decimal Calculate(Customer customer, decimal orderTotal);
}

public interface IPaymentProcessor
{
    string PaymentType { get; }
    Task<PaymentResult> ProcessAsync(decimal amount);
}

public interface INotificationService
{
    Task NotifyOrderCreatedAsync(Order order, Customer customer);
}

// === VALUE OBJECTS ===

public record OrderItem(int ProductId, string ProductName, int Quantity, decimal UnitPrice)
{
    public decimal Total => Quantity * UnitPrice;
}

public record PaymentResult(bool Success, string? TransactionId, string? ErrorMessage);

// === ENTITIES ===

public class Order
{
    public Guid Id { get; private set; }
    public int CustomerId { get; private set; }
    public IReadOnlyList<OrderItem> Items => _items.AsReadOnly();
    public decimal Subtotal => _items.Sum(i => i.Total);
    public decimal Discount { get; private set; }
    public decimal Total => Subtotal - Discount;
    public OrderStatus Status { get; private set; }

    private readonly List<OrderItem> _items = new();

    private Order() { } // For EF

    public static Order Create(int customerId) => new()
    {
        Id = Guid.NewGuid(),
        CustomerId = customerId,
        Status = OrderStatus.Pending
    };

    public void AddItem(Product product, int quantity)
    {
        _items.Add(new OrderItem(product.Id, product.Name, quantity, product.Price));
    }

    public void ApplyDiscount(decimal discount)
    {
        Discount = Math.Min(discount, Subtotal);
    }

    public void MarkAsPaid(string transactionId)
    {
        Status = OrderStatus.Paid;
    }
}

// === DISCOUNT STRATEGIES (OCP) ===

public class CustomerTierDiscountStrategy : IDiscountStrategy
{
    public decimal Calculate(Customer customer, decimal orderTotal)
    {
        return customer.Tier switch
        {
            CustomerTier.Gold => orderTotal * 0.15m,
            CustomerTier.Silver => orderTotal * 0.10m,
            CustomerTier.Bronze => orderTotal * 0.05m,
            _ => 0m
        };
    }
}

public class FirstOrderDiscountStrategy : IDiscountStrategy
{
    public decimal Calculate(Customer customer, decimal orderTotal)
    {
        return customer.OrderCount == 0 ? orderTotal * 0.20m : 0m;
    }
}

public class CompositeDiscountStrategy : IDiscountStrategy
{
    private readonly IEnumerable<IDiscountStrategy> _strategies;
    private readonly DiscountCombination _combination;

    public CompositeDiscountStrategy(
        IEnumerable<IDiscountStrategy> strategies,
        DiscountCombination combination = DiscountCombination.Max)
    {
        _strategies = strategies;
        _combination = combination;
    }

    public decimal Calculate(Customer customer, decimal orderTotal)
    {
        var discounts = _strategies.Select(s => s.Calculate(customer, orderTotal));
        return _combination switch
        {
            DiscountCombination.Max => discounts.Max(),
            DiscountCombination.Sum => discounts.Sum(),
            _ => discounts.Max()
        };
    }
}

// === PAYMENT PROCESSORS (OCP) ===

public class CreditCardPaymentProcessor : IPaymentProcessor
{
    private readonly ICreditCardGateway _gateway;

    public string PaymentType => "CreditCard";

    public CreditCardPaymentProcessor(ICreditCardGateway gateway) => _gateway = gateway;

    public async Task<PaymentResult> ProcessAsync(decimal amount)
    {
        var result = await _gateway.ChargeAsync(amount);
        return new PaymentResult(result.Success, result.TransactionId, result.Error);
    }
}

public class PayPalPaymentProcessor : IPaymentProcessor
{
    private readonly IPayPalClient _client;

    public string PaymentType => "PayPal";

    public PayPalPaymentProcessor(IPayPalClient client) => _client = client;

    public async Task<PaymentResult> ProcessAsync(decimal amount)
    {
        var result = await _client.CreatePaymentAsync(amount);
        return new PaymentResult(result.Approved, result.PaymentId, result.Message);
    }
}

// Adding new payment types is easy!
public class CryptoPaymentProcessor : IPaymentProcessor
{
    public string PaymentType => "Crypto";
    public async Task<PaymentResult> ProcessAsync(decimal amount) { /* ... */ }
}

// === PAYMENT PROCESSOR FACTORY ===

public interface IPaymentProcessorFactory
{
    IPaymentProcessor Create(string paymentType);
}

public class PaymentProcessorFactory : IPaymentProcessorFactory
{
    private readonly IEnumerable<IPaymentProcessor> _processors;

    public PaymentProcessorFactory(IEnumerable<IPaymentProcessor> processors)
    {
        _processors = processors;
    }

    public IPaymentProcessor Create(string paymentType)
    {
        var processor = _processors.FirstOrDefault(p => p.PaymentType == paymentType);
        if (processor == null)
            throw new NotSupportedException($"Payment type '{paymentType}' is not supported.");
        return processor;
    }
}

// === VALIDATORS (SRP) ===

public interface IOrderValidator
{
    Task<ValidationResult> ValidateAsync(CreateOrderRequest request);
}

public class OrderValidator : IOrderValidator
{
    private readonly ICustomerRepository _customerRepository;
    private readonly IProductRepository _productRepository;

    public OrderValidator(
        ICustomerRepository customerRepository,
        IProductRepository productRepository)
    {
        _customerRepository = customerRepository;
        _productRepository = productRepository;
    }

    public async Task<ValidationResult> ValidateAsync(CreateOrderRequest request)
    {
        var errors = new List<string>();

        if (request.Items == null || request.Items.Count == 0)
            errors.Add("Order must contain at least one item.");

        var customer = await _customerRepository.GetByIdAsync(request.CustomerId);
        if (customer == null)
            errors.Add($"Customer {request.CustomerId} not found.");

        foreach (var item in request.Items ?? Enumerable.Empty<OrderItemRequest>())
        {
            var product = await _productRepository.GetByIdAsync(item.ProductId);
            if (product == null)
                errors.Add($"Product {item.ProductId} not found.");
        }

        return new ValidationResult(errors.Count == 0, errors);
    }
}

// === ORDER SERVICE (SRP - Orchestration Only) ===

public class OrderService
{
    private readonly IOrderValidator _validator;
    private readonly ICustomerRepository _customerRepository;
    private readonly IProductRepository _productRepository;
    private readonly IOrderRepository _orderRepository;
    private readonly IDiscountStrategy _discountStrategy;
    private readonly IPaymentProcessorFactory _paymentFactory;
    private readonly INotificationService _notificationService;
    private readonly ILogger<OrderService> _logger;

    public OrderService(
        IOrderValidator validator,
        ICustomerRepository customerRepository,
        IProductRepository productRepository,
        IOrderRepository orderRepository,
        IDiscountStrategy discountStrategy,
        IPaymentProcessorFactory paymentFactory,
        INotificationService notificationService,
        ILogger<OrderService> logger)
    {
        _validator = validator;
        _customerRepository = customerRepository;
        _productRepository = productRepository;
        _orderRepository = orderRepository;
        _discountStrategy = discountStrategy;
        _paymentFactory = paymentFactory;
        _notificationService = notificationService;
        _logger = logger;
    }

    public async Task<Result<Order>> CreateOrderAsync(CreateOrderRequest request)
    {
        // Validate
        var validation = await _validator.ValidateAsync(request);
        if (!validation.IsValid)
            return Result<Order>.Failure(validation.Errors);

        // Get customer
        var customer = await _customerRepository.GetByIdAsync(request.CustomerId);

        // Build order
        var order = Order.Create(request.CustomerId);
        foreach (var item in request.Items)
        {
            var product = await _productRepository.GetByIdAsync(item.ProductId);
            order.AddItem(product!, item.Quantity);
        }

        // Apply discount
        var discount = _discountStrategy.Calculate(customer!, order.Subtotal);
        order.ApplyDiscount(discount);

        // Process payment
        var paymentProcessor = _paymentFactory.Create(request.PaymentType);
        var paymentResult = await paymentProcessor.ProcessAsync(order.Total);

        if (!paymentResult.Success)
            return Result<Order>.Failure($"Payment failed: {paymentResult.ErrorMessage}");

        order.MarkAsPaid(paymentResult.TransactionId!);

        // Persist
        await _orderRepository.CreateAsync(order);

        // Notify
        await _notificationService.NotifyOrderCreatedAsync(order, customer!);

        _logger.LogInformation("Order {OrderId} created for customer {CustomerId}", order.Id, customer!.Id);

        return Result<Order>.Success(order);
    }
}

// === DI REGISTRATION ===

public static class ServiceCollectionExtensions
{
    public static IServiceCollection AddOrderServices(this IServiceCollection services)
    {
        // Repositories
        services.AddScoped<ICustomerRepository, SqlCustomerRepository>();
        services.AddScoped<IProductRepository, SqlProductRepository>();
        services.AddScoped<IOrderRepository, SqlOrderRepository>();

        // Validators
        services.AddScoped<IOrderValidator, OrderValidator>();

        // Discount strategies
        services.AddScoped<IDiscountStrategy>(sp =>
            new CompositeDiscountStrategy(new IDiscountStrategy[]
            {
                new CustomerTierDiscountStrategy(),
                new FirstOrderDiscountStrategy()
            }));

        // Payment processors
        services.AddScoped<IPaymentProcessor, CreditCardPaymentProcessor>();
        services.AddScoped<IPaymentProcessor, PayPalPaymentProcessor>();
        services.AddScoped<IPaymentProcessorFactory, PaymentProcessorFactory>();

        // Notifications
        services.AddScoped<INotificationService, EmailNotificationService>();

        // Main service
        services.AddScoped<OrderService>();

        return services;
    }
}
```

## Testing the SOLID Design

```csharp
public class OrderServiceTests
{
    private readonly Mock<IOrderValidator> _mockValidator;
    private readonly Mock<ICustomerRepository> _mockCustomerRepo;
    private readonly Mock<IProductRepository> _mockProductRepo;
    private readonly Mock<IOrderRepository> _mockOrderRepo;
    private readonly Mock<IDiscountStrategy> _mockDiscount;
    private readonly Mock<IPaymentProcessorFactory> _mockPaymentFactory;
    private readonly Mock<INotificationService> _mockNotifier;
    private readonly OrderService _sut;

    public OrderServiceTests()
    {
        _mockValidator = new Mock<IOrderValidator>();
        _mockCustomerRepo = new Mock<ICustomerRepository>();
        _mockProductRepo = new Mock<IProductRepository>();
        _mockOrderRepo = new Mock<IOrderRepository>();
        _mockDiscount = new Mock<IDiscountStrategy>();
        _mockPaymentFactory = new Mock<IPaymentProcessorFactory>();
        _mockNotifier = new Mock<INotificationService>();

        _sut = new OrderService(
            _mockValidator.Object,
            _mockCustomerRepo.Object,
            _mockProductRepo.Object,
            _mockOrderRepo.Object,
            _mockDiscount.Object,
            _mockPaymentFactory.Object,
            _mockNotifier.Object,
            Mock.Of<ILogger<OrderService>>());
    }

    [Fact]
    public async Task CreateOrder_WithValidRequest_ReturnsSuccessfulOrder()
    {
        // Arrange
        var request = CreateValidRequest();
        SetupValidScenario();

        // Act
        var result = await _sut.CreateOrderAsync(request);

        // Assert
        Assert.True(result.IsSuccess);
        Assert.NotNull(result.Value);
    }

    [Fact]
    public async Task CreateOrder_WithInvalidRequest_ReturnsFailure()
    {
        // Arrange
        var request = CreateValidRequest();
        _mockValidator
            .Setup(v => v.ValidateAsync(request))
            .ReturnsAsync(ValidationResult.Failure("Invalid"));

        // Act
        var result = await _sut.CreateOrderAsync(request);

        // Assert
        Assert.False(result.IsSuccess);
    }

    [Fact]
    public async Task CreateOrder_WhenPaymentFails_ReturnsFailure()
    {
        // Arrange
        var request = CreateValidRequest();
        SetupValidScenario();
        SetupPaymentFailure();

        // Act
        var result = await _sut.CreateOrderAsync(request);

        // Assert
        Assert.False(result.IsSuccess);
        Assert.Contains("Payment failed", result.Error);
    }

    private void SetupValidScenario()
    {
        _mockValidator
            .Setup(v => v.ValidateAsync(It.IsAny<CreateOrderRequest>()))
            .ReturnsAsync(ValidationResult.Success);

        _mockCustomerRepo
            .Setup(r => r.GetByIdAsync(It.IsAny<int>()))
            .ReturnsAsync(new Customer { Id = 1, Email = "test@test.com" });

        _mockProductRepo
            .Setup(r => r.GetByIdAsync(It.IsAny<int>()))
            .ReturnsAsync(new Product { Id = 1, Name = "Test", Price = 10.00m });

        var mockProcessor = new Mock<IPaymentProcessor>();
        mockProcessor
            .Setup(p => p.ProcessAsync(It.IsAny<decimal>()))
            .ReturnsAsync(new PaymentResult(true, "txn123", null));

        _mockPaymentFactory
            .Setup(f => f.Create(It.IsAny<string>()))
            .Returns(mockProcessor.Object);
    }

    private void SetupPaymentFailure()
    {
        var mockProcessor = new Mock<IPaymentProcessor>();
        mockProcessor
            .Setup(p => p.ProcessAsync(It.IsAny<decimal>()))
            .ReturnsAsync(new PaymentResult(false, null, "Insufficient funds"));

        _mockPaymentFactory
            .Setup(f => f.Create(It.IsAny<string>()))
            .Returns(mockProcessor.Object);
    }

    private CreateOrderRequest CreateValidRequest() => new()
    {
        CustomerId = 1,
        Items = new[] { new OrderItemRequest { ProductId = 1, Quantity = 2 } },
        PaymentType = "CreditCard"
    };
}
```
