# Java Clean Code Rules

## Naming Conventions

### Variables and Methods
- Use camelCase: `getUserName`, `totalPrice`
- Boolean variables: prefix with `is`, `has`, `should`: `isActive`, `hasPermission`
- Constants: UPPER_SNAKE_CASE: `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`
- Private fields: use camelCase with optional underscore suffix: `userName` or `userName_`

### Classes and Interfaces
- Use PascalCase: `UserAccount`, `OrderProcessor`
- Interfaces: descriptive names without 'I' prefix (prefer `Comparable` over `IComparable`)

### Packages
- Use lowercase: `com.example.service`, `com.example.util`

### Common Anti-patterns
- Avoid: `data`, `info`, `obj`, `val`, `temp`, `result` without context
- Avoid: single letters except `i`, `j`, `k` for loops
- Avoid: Hungarian notation (`strName`, `intCount`)
- Avoid: interface prefix 'I' (`IUserService` -> use `UserService`)

### Good Examples
```java
// Bad
Date d = new Date();
User u = getU();
boolean flag = true;

// Good
Date createdAt = new Date();
User currentUser = getCurrentUser();
boolean isAuthenticated = true;
```

## Method Length

**Target: Maximum 25 lines** (excluding blank lines and closing braces)

Java methods exceeding 25 lines often indicate:
- Multiple responsibilities (violates Single Responsibility Principle)
- Complex nested logic
- Need for private helper methods

### Refactoring Example
```java
// Bad: Too long, does too much
public Order processOrder(Order order) {
    // Validation
    if (order.getItems() == null || order.getItems().isEmpty()) {
        throw new IllegalArgumentException("Empty order");
    }

    // Calculate total
    BigDecimal total = BigDecimal.ZERO;
    for (OrderItem item : order.getItems()) {
        BigDecimal itemTotal = item.getPrice()
            .multiply(BigDecimal.valueOf(item.getQuantity()));
        total = total.add(itemTotal);
    }

    // Apply discount
    if (order.getCoupon() != null) {
        BigDecimal discount = getDiscount(order.getCoupon());
        total = total.subtract(total.multiply(discount));
    }

    // Add shipping
    BigDecimal shipping = calculateShipping(order.getAddress());
    total = total.add(shipping);

    // Save order
    order.setTotal(total);
    order.setStatus(OrderStatus.PENDING);
    Order savedOrder = orderRepository.save(order);

    // Send confirmation
    emailService.send(
        order.getEmail(),
        "Order confirmed",
        emailTemplateService.generateOrderConfirmation(savedOrder)
    );

    return savedOrder;
}

// Good: Split into focused methods
public Order processOrder(Order order) {
    validateOrder(order);
    BigDecimal total = calculateOrderTotal(order);
    Order savedOrder = saveOrder(order, total);
    sendOrderConfirmation(savedOrder);
    return savedOrder;
}

private void validateOrder(Order order) {
    if (order.getItems() == null || order.getItems().isEmpty()) {
        throw new IllegalArgumentException("Empty order");
    }
}

private BigDecimal calculateOrderTotal(Order order) {
    BigDecimal subtotal = calculateSubtotal(order.getItems());
    BigDecimal discount = applyDiscount(subtotal, order.getCoupon());
    BigDecimal shipping = calculateShipping(order.getAddress());
    return subtotal.subtract(discount).add(shipping);
}
```

## Comment Guidelines

### Redundant Comments (Remove)
```java
// Set the name - REDUNDANT
user.setName("John");

// Loop through items - REDUNDANT
for (Item item : items) {
    // ...
}

// Increment counter - REDUNDANT
counter++;

// Return the result - REDUNDANT
return result;

// Constructor - REDUNDANT
public User(String name) {
    this.name = name;
}
```

### Valuable Comments (Keep)
```java
// HACK: API returns null instead of empty list for new users
List<Order> orders = response.getData() != null
    ? response.getData()
    : Collections.emptyList();

// Using HashSet for O(1) lookup performance
Set<Long> uniqueIds = new HashSet<>(ids);

// FIXME: This breaks with different timezones, should use ZonedDateTime
Date deadline = new Date(2024, 1, 1);

// Regex matches email format per RFC 5322 simplified
Pattern emailPattern = Pattern.compile(
    "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
);

// Synchronized to prevent race condition in concurrent access
synchronized (lock) {
    cache.put(key, value);
}
```

## Javadoc vs Comments

Use Javadoc for:
- Public classes and interfaces
- Public and protected methods
- Public fields (when necessary)

```java
/**
 * Calculate total price with optional discount.
 *
 * @param items list of items to calculate total for
 * @param discount discount percentage (0.0 to 1.0)
 * @return total price after discount
 * @throws IllegalArgumentException if discount is negative or > 1.0
 */
public BigDecimal calculateTotal(List<OrderItem> items, BigDecimal discount) {
    validateDiscount(discount);
    BigDecimal subtotal = calculateSubtotal(items);
    return subtotal.multiply(BigDecimal.ONE.subtract(discount));
}
```

Use comments (not Javadoc) for:
- Private method implementation notes
- Complex algorithm explanations
- TODOs and FIXMEs
- Temporary workarounds

## Builder Pattern Over Long Constructors

```java
// Bad: Too many parameters, unclear what each means
User user = new User(
    "John",
    "john@example.com",
    true,
    false,
    null,
    "premium",
    new Date()
);

// Good: Builder pattern for clarity
User user = User.builder()
    .name("John")
    .email("john@example.com")
    .active(true)
    .verified(false)
    .role("premium")
    .createdAt(new Date())
    .build();
```

## Optional Over Null

Prefer `Optional<T>` for return values that might be absent:

```java
// Less clear
public User findUserById(Long id) {
    // Returns null if not found
    return userRepository.findById(id);
}

// More clear
public Optional<User> findUserById(Long id) {
    return userRepository.findById(id);
}
```

## Stream API

Use streams for collection processing, but keep them readable:

```java
// Good: Simple and readable
List<User> activeUsers = users.stream()
    .filter(User::isActive)
    .collect(Collectors.toList());

// Bad: Too complex, hard to read
Map<String, List<BigDecimal>> result = orders.stream()
    .filter(o -> o.getStatus() == OrderStatus.COMPLETED)
    .filter(o -> o.getCreatedAt().isAfter(cutoffDate))
    .collect(Collectors.groupingBy(
        Order::getUserId,
        Collectors.mapping(
            Order::getTotal,
            Collectors.toList()
        )
    ));

// Good: Break down complex streams
List<Order> completedOrders = orders.stream()
    .filter(o -> o.getStatus() == OrderStatus.COMPLETED)
    .filter(o -> o.getCreatedAt().isAfter(cutoffDate))
    .collect(Collectors.toList());

Map<String, List<BigDecimal>> orderTotalsByUser = completedOrders.stream()
    .collect(Collectors.groupingBy(
        Order::getUserId,
        Collectors.mapping(Order::getTotal, Collectors.toList())
    ));
```
