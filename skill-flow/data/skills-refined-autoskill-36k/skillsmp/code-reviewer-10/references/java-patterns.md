# Java/Spring Boot Review Patterns

## Critical Anti-Patterns

### 1. Exception Handling

```java
// ❌ BAD: Swallowing exceptions
try {
    processOrder(order);
} catch (Exception e) {
    log.error("Error processing order", e);
    // continues execution with invalid state
}

// ✅ GOOD: Specific handling with proper propagation
try {
    processOrder(order);
} catch (PaymentFailedException e) {
    throw new OrderProcessingException("Payment failed for order " + order.getId(), e);
} catch (InventoryException e) {
    return OrderResult.outOfStock(order.getItems());
}
```

### 2. Null Safety

```java
// ❌ BAD: Implicit null checks
public String getUserName(Long userId) {
    User user = userRepo.findById(userId);
    return user.getName(); // NPE if not found
}

// ✅ GOOD: Optional with explicit handling
public Optional<String> getUserName(Long userId) {
    return userRepo.findById(userId)
        .map(User::getName);
}

// ✅ GOOD: Fail fast when null is unexpected
public void processUser(User user) {
    Objects.requireNonNull(user, "user must not be null");
    // ...
}
```

### 3. Dependency Injection

```java
// ❌ BAD: Field injection
@Service
public class OrderService {
    @Autowired
    private UserRepository userRepo;
    @Autowired
    private PaymentService paymentService;
}

// ✅ GOOD: Constructor injection
@Service
@RequiredArgsConstructor
public class OrderService {
    private final UserRepository userRepo;
    private final PaymentService paymentService;
}
```

### 4. Transaction Boundaries

```java
// ❌ BAD: Transaction too broad
@Transactional
public void processOrderWithNotification(Order order) {
    orderRepo.save(order);
    emailService.sendConfirmation(order); // HTTP call in transaction!
}

// ✅ GOOD: Transaction only for DB operations
public void processOrderWithNotification(Order order) {
    Order saved = saveOrder(order); // @Transactional
    emailService.sendConfirmation(saved); // outside transaction
}

@Transactional
protected Order saveOrder(Order order) {
    return orderRepo.save(order);
}
```

### 5. N+1 Query Prevention

```java
// ❌ BAD: N+1 queries
public List<OrderDto> getAllOrders() {
    return orderRepo.findAll().stream()
        .map(order -> new OrderDto(
            order.getId(),
            order.getItems() // triggers lazy load per order
        ))
        .toList();
}

// ✅ GOOD: Fetch join
@Query("SELECT o FROM Order o JOIN FETCH o.items")
List<Order> findAllWithItems();

// ✅ GOOD: EntityGraph
@EntityGraph(attributePaths = {"items", "customer"})
List<Order> findAll();
```

### 6. Business Logic in Controllers

```java
// ❌ BAD: Controller doing too much
@PostMapping("/orders")
public ResponseEntity<OrderDto> createOrder(@RequestBody CreateOrderRequest req) {
    if (req.getItems().isEmpty()) {
        throw new BadRequestException("Items required");
    }
    BigDecimal total = req.getItems().stream()
        .map(i -> i.getPrice().multiply(BigDecimal.valueOf(i.getQuantity())))
        .reduce(BigDecimal.ZERO, BigDecimal::add);
    if (total.compareTo(MAX_ORDER) > 0) {
        throw new BadRequestException("Order exceeds limit");
    }
    // ... 50 more lines
}

// ✅ GOOD: Controller delegates to service
@PostMapping("/orders")
public ResponseEntity<OrderDto> createOrder(
    @Valid @RequestBody CreateOrderRequest req
) {
    Order order = orderService.create(req);
    return ResponseEntity.created(uri(order.getId()))
        .body(orderMapper.toDto(order));
}
```

### 7. Immutability

```java
// ❌ BAD: Mutable collections in responses
public List<User> getActiveUsers() {
    return activeUsers; // external code can modify internal state
}

// ✅ GOOD: Defensive copies or immutable
public List<User> getActiveUsers() {
    return List.copyOf(activeUsers);
}

// ✅ GOOD: Records for DTOs (Java 16+)
public record OrderDto(
    Long id,
    List<ItemDto> items,
    BigDecimal total
) {
    public OrderDto {
        items = List.copyOf(items); // immutable
    }
}
```

---

## Security Patterns

### Input Validation

```java
// ❌ BAD: Trust user input
@PostMapping("/search")
public List<User> search(@RequestParam String query) {
    return jdbcTemplate.query(
        "SELECT * FROM users WHERE name LIKE '%" + query + "%'",
        userMapper
    );
}

// ✅ GOOD: Parameterized queries
@PostMapping("/search")
public List<User> search(@RequestParam @Size(max = 100) String query) {
    return userRepo.findByNameContaining(query);
}
```

### Logging Sensitive Data

```java
// ❌ BAD: Logging sensitive data
log.debug("Processing payment for card: {}", cardNumber);
log.info("User login attempt with password: {}", password);

// ✅ GOOD: Mask or exclude
log.debug("Processing payment for card ending: {}", maskCard(cardNumber));
log.info("User login attempt for: {}", username);
```

### Authorization

```java
// ❌ BAD: No authorization check
@GetMapping("/admin/users")
public List<User> getAllUsers() {
    return userService.findAll();
}

// ✅ GOOD: Declarative authorization
@PreAuthorize("hasRole('ADMIN')")
@GetMapping("/admin/users")
public List<User> getAllUsers() {
    return userService.findAll();
}

// ✅ GOOD: ABAC policy
@AbacPolicy(resource = "users", action = "list")
@GetMapping("/admin/users")
public List<User> getAllUsers() {
    return userService.findAll();
}
```

---

## Performance Patterns

### Pagination

```java
// ❌ BAD: Loading all data
public List<Order> getAllOrders() {
    return orderRepo.findAll(); // could be millions
}

// ✅ GOOD: Paginated
public Page<Order> getOrders(Pageable pageable) {
    return orderRepo.findAll(pageable);
}
```

### Caching

```java
// ✅ GOOD: Cache immutable or rarely-changing data
@Cacheable("countries")
public List<Country> getAllCountries() {
    return countryRepo.findAll();
}

// ✅ GOOD: Cache with TTL
@Cacheable(value = "userPreferences", key = "#userId")
public UserPreferences getPreferences(Long userId) {
    return preferenceRepo.findByUserId(userId);
}
```

---

## Testing Patterns

### Testable Design

```java
// ❌ BAD: Hard to test (hidden dependency)
public class PriceCalculator {
    public BigDecimal calculate(Order order) {
        LocalDate today = LocalDate.now(); // hidden dep
        if (isHoliday(today)) {
            return order.getTotal().multiply(HOLIDAY_DISCOUNT);
        }
        return order.getTotal();
    }
}

// ✅ GOOD: Dependency passed in
public class PriceCalculator {
    private final Clock clock;

    public PriceCalculator(Clock clock) {
        this.clock = clock;
    }

    public BigDecimal calculate(Order order) {
        LocalDate today = LocalDate.now(clock);
        // ...
    }
}

// Test
var fixedClock = Clock.fixed(HOLIDAY_DATE, ZoneId.UTC);
var calc = new PriceCalculator(fixedClock);
assertThat(calc.calculate(order)).isEqualTo(expectedHolidayPrice);
```

### Pure Functions

```java
// ✅ GOOD: Extract pure functions for easy testing
public class OrderValidator {
    // Pure function - no dependencies, no side effects
    public ValidationResult validate(Order order, Set<String> validSkus) {
        var errors = new ArrayList<String>();

        if (order.getItems().isEmpty()) {
            errors.add("Order must have at least one item");
        }

        order.getItems().stream()
            .filter(i -> !validSkus.contains(i.getSku()))
            .forEach(i -> errors.add("Invalid SKU: " + i.getSku()));

        return errors.isEmpty()
            ? ValidationResult.valid()
            : ValidationResult.invalid(errors);
    }
}

// Test - no mocks needed
@Test
void shouldRejectEmptyOrder() {
    var result = validator.validate(emptyOrder, validSkus);
    assertThat(result.isValid()).isFalse();
    assertThat(result.getErrors()).contains("Order must have at least one item");
}
```
