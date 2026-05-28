---
name: Testing with JUnit & Mockito
description: JUnit 5, Mockito, Spring test slices, integration testing, and test organization.
metadata:
  labels: [java, testing, junit, mockito]
  triggers:
    files: ['**/*Test.java', '**/*IT.java', '**/*Tests.java']
    keywords: [JUnit, Jupiter, Mockito, '@Test', '@ExtendWith', '@MockBean', '@SpringBootTest', '@DataJpaTest', '@WebMvcTest']
---

# Testing Standards

## JUnit 5 Basics

```java
class UserServiceTest {

    @Test
    @DisplayName("should create user with valid data")
    void shouldCreateUser() {
        // Given
        var request = new CreateUserRequest("John", "john@example.com");

        // When
        var user = userService.create(request);

        // Then
        assertThat(user.getName()).isEqualTo("John");
        assertThat(user.getEmail()).isEqualTo("john@example.com");
    }

    @ParameterizedTest
    @ValueSource(strings = {"", " ", "invalid"})
    void shouldRejectInvalidEmail(String email) {
        var request = new CreateUserRequest("John", email);

        assertThatThrownBy(() -> userService.create(request))
            .isInstanceOf(ValidationException.class);
    }

    @BeforeEach
    void setUp() {
        // Setup before each test
    }

    @AfterEach
    void tearDown() {
        // Cleanup after each test
    }
}
```

## Mockito

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    OrderRepository orderRepository;

    @Mock
    InventoryService inventoryService;

    @InjectMocks
    OrderService orderService;

    @Test
    void shouldCreateOrder() {
        // Given
        var request = new CreateOrderRequest("product-1", 2);
        when(inventoryService.checkStock("product-1")).thenReturn(true);
        when(orderRepository.save(any())).thenAnswer(inv -> inv.getArgument(0));

        // When
        var order = orderService.create(request);

        // Then
        assertThat(order).isNotNull();
        verify(inventoryService).checkStock("product-1");
        verify(orderRepository).save(any(Order.class));
    }
}
```

## Spring Test Slices

```java
// Full context
@SpringBootTest
class ApplicationTests {}

// Web layer only
@WebMvcTest(UserController.class)
class UserControllerTest {
    @Autowired MockMvc mockMvc;
    @MockBean UserService userService;

    @Test
    void shouldReturnUser() throws Exception {
        when(userService.findById(1L)).thenReturn(Optional.of(new User(1L, "John")));

        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("John"));
    }
}

// JPA layer only
@DataJpaTest
class UserRepositoryTest {
    @Autowired UserRepository repository;
    @Autowired TestEntityManager entityManager;

    @Test
    void shouldFindByEmail() {
        entityManager.persist(new User("john@example.com"));
        var user = repository.findByEmail("john@example.com");
        assertThat(user).isPresent();
    }
}
```

## Best Practices

1. **Given-When-Then** structure for readability
2. **One assertion concept per test**
3. **Use test slices** to minimize context
4. **AssertJ** for fluent assertions
5. **Parameterized tests** for multiple inputs

## References

- [Test Slices](references/test-slices.md) - Available slices, customization
- [Mockito Patterns](references/mockito-patterns.md) - Stubbing, verification, argument captors
