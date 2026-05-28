# Java Unit Testing Patterns

## JUnit 5 Patterns

### Test Class Structure

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;
    
    @Mock
    private PaymentGateway paymentGateway;
    
    @InjectMocks
    private OrderService orderService;
    
    @BeforeEach
    void setUp() {
        // Common setup if needed beyond @InjectMocks
    }
    
    @Nested
    @DisplayName("createOrder")
    class CreateOrder {
        
        @Test
        @DisplayName("creates order with valid input")
        void withValidInput_createsOrder() {
            // Arrange
            OrderRequest request = new OrderRequest("item-1", 2);
            when(orderRepository.save(any())).thenReturn(new Order("order-123"));
            
            // Act
            Order result = orderService.createOrder(request);
            
            // Assert
            assertThat(result.getId()).isEqualTo("order-123");
            verify(orderRepository).save(argThat(order -> 
                order.getItemId().equals("item-1") && order.getQuantity() == 2
            ));
        }
        
        @Test
        @DisplayName("throws exception for negative quantity")
        void withNegativeQuantity_throwsException() {
            OrderRequest request = new OrderRequest("item-1", -1);
            
            assertThatThrownBy(() -> orderService.createOrder(request))
                .isInstanceOf(IllegalArgumentException.class)
                .hasMessageContaining("quantity must be positive");
        }
    }
}
```

### Naming Conventions

```
methodName_stateUnderTest_expectedBehavior
```

Examples:
- `createOrder_withValidInput_savesToRepository`
- `calculateTotal_withEmptyCart_returnsZero`
- `authenticate_withExpiredToken_throwsAuthException`

### Parameterized Tests

```java
@ParameterizedTest
@CsvSource({
    "0, 0",
    "1, 1",
    "5, 120",
    "10, 3628800"
})
void factorial_withValidInput_returnsCorrectResult(int input, long expected) {
    assertThat(calculator.factorial(input)).isEqualTo(expected);
}

@ParameterizedTest
@MethodSource("invalidInputProvider")
void process_withInvalidInput_throwsException(String input, Class<? extends Exception> expectedException) {
    assertThatThrownBy(() -> processor.process(input))
        .isInstanceOf(expectedException);
}

static Stream<Arguments> invalidInputProvider() {
    return Stream.of(
        Arguments.of(null, NullPointerException.class),
        Arguments.of("", IllegalArgumentException.class),
        Arguments.of("invalid", ParseException.class)
    );
}
```

## Mockito Patterns

### Stubbing

```java
// Simple return
when(repository.findById(1L)).thenReturn(Optional.of(entity));

// Return different values on consecutive calls
when(service.generate()).thenReturn("first", "second", "third");

// Return based on argument
when(repository.findByName(anyString()))
    .thenAnswer(invocation -> {
        String name = invocation.getArgument(0);
        return Optional.of(new Entity(name));
    });

// Throw exception
when(client.connect()).thenThrow(new IOException("Connection refused"));

// Void method exception
doThrow(new RuntimeException()).when(service).cleanup();
```

### Verification

```java
// Verify called once
verify(repository).save(any(Entity.class));

// Verify call count
verify(service, times(3)).retry();
verify(service, never()).fallback();
verify(service, atLeast(1)).process(any());

// Verify argument
verify(notifier).send(argThat(message -> 
    message.getRecipient().equals("user@example.com") &&
    message.getSubject().contains("Order")
));

// Verify order
InOrder inOrder = inOrder(validator, repository, notifier);
inOrder.verify(validator).validate(any());
inOrder.verify(repository).save(any());
inOrder.verify(notifier).send(any());

// Verify no more interactions
verifyNoMoreInteractions(repository);
```

### Argument Captors

```java
@Captor
ArgumentCaptor<Order> orderCaptor;

@Test
void createOrder_capturesCorrectEntity() {
    orderService.createOrder(request);
    
    verify(repository).save(orderCaptor.capture());
    Order captured = orderCaptor.getValue();
    
    assertThat(captured.getStatus()).isEqualTo(OrderStatus.PENDING);
    assertThat(captured.getCreatedAt()).isNotNull();
}
```

## AssertJ Patterns

```java
// Collections
assertThat(list)
    .hasSize(3)
    .contains("a", "b")
    .doesNotContain("x")
    .containsExactlyInAnyOrder("a", "b", "c");

// Objects
assertThat(user)
    .hasFieldOrPropertyWithValue("name", "John")
    .extracting(User::getEmail, User::isActive)
    .containsExactly("john@example.com", true);

// Exceptions
assertThatThrownBy(() -> service.process(null))
    .isInstanceOf(NullPointerException.class)
    .hasMessageContaining("must not be null");

assertThatCode(() -> service.process(validInput))
    .doesNotThrowAnyException();

// Soft assertions (collect all failures)
SoftAssertions.assertSoftly(softly -> {
    softly.assertThat(result.getName()).isEqualTo("expected");
    softly.assertThat(result.getValue()).isGreaterThan(0);
    softly.assertThat(result.isValid()).isTrue();
});
```

## Micronaut Testing

### @MicronautTest Integration

```java
@MicronautTest
class UserControllerTest {

    @Inject
    @Client("/")
    HttpClient client;
    
    @Inject
    UserRepository userRepository;
    
    @MockBean(EmailService.class)
    EmailService emailService() {
        return mock(EmailService.class);
    }
    
    @Test
    void createUser_returnsCreatedStatus() {
        HttpRequest<UserDto> request = HttpRequest.POST("/users", 
            new UserDto("test@example.com"));
        
        HttpResponse<UserDto> response = client.toBlocking()
            .exchange(request, UserDto.class);
        
        assertThat(response.status()).isEqualTo(HttpStatus.CREATED);
    }
}
```

### Constructor Injection Testing

```java
// Production code - use constructor injection
@Singleton
public class OrderService {
    private final OrderRepository repository;
    private final PaymentGateway gateway;
    
    public OrderService(OrderRepository repository, PaymentGateway gateway) {
        this.repository = repository;
        this.gateway = gateway;
    }
}

// Test - easy to mock
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    @Mock OrderRepository repository;
    @Mock PaymentGateway gateway;
    @InjectMocks OrderService service;
}
```

## Test Data Builders

```java
public class OrderBuilder {
    private String id = "order-" + UUID.randomUUID();
    private String customerId = "customer-1";
    private List<OrderItem> items = new ArrayList<>();
    private OrderStatus status = OrderStatus.PENDING;
    
    public static OrderBuilder anOrder() {
        return new OrderBuilder();
    }
    
    public OrderBuilder withId(String id) {
        this.id = id;
        return this;
    }
    
    public OrderBuilder withStatus(OrderStatus status) {
        this.status = status;
        return this;
    }
    
    public OrderBuilder withItem(String productId, int quantity) {
        items.add(new OrderItem(productId, quantity));
        return this;
    }
    
    public Order build() {
        return new Order(id, customerId, items, status);
    }
}

// Usage in tests
Order order = anOrder()
    .withStatus(OrderStatus.SHIPPED)
    .withItem("product-1", 2)
    .build();
```

## Async Testing

```java
@Test
void asyncOperation_completesWithinTimeout() {
    CompletableFuture<Result> future = service.processAsync(input);
    
    await().atMost(5, SECONDS).until(future::isDone);
    
    assertThat(future.get()).satisfies(result -> {
        assertThat(result.isSuccess()).isTrue();
    });
}

@Test
void reactiveStream_emitsExpectedValues() {
    StepVerifier.create(service.getItems())
        .expectNext("item1")
        .expectNext("item2")
        .expectComplete()
        .verify(Duration.ofSeconds(5));
}
```
