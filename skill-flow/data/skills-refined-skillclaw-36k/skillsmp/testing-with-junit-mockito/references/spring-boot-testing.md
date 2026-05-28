# Spring Boot Testing

## Slice Tests

```java
// Web layer only
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private UserService userService;

    @Test
    void shouldGetUser() throws Exception {
        when(userService.findById(1L)).thenReturn(new User(1L, "John"));

        mockMvc.perform(get("/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("John"));
    }

    @Test
    void shouldCreateUser() throws Exception {
        mockMvc.perform(post("/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                    {"name": "John", "email": "john@example.com"}
                    """))
            .andExpect(status().isCreated());
    }
}

// JPA layer only
@DataJpaTest
class UserRepositoryTest {

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private UserRepository userRepository;

    @Test
    void shouldFindByEmail() {
        entityManager.persist(new User("John", "john@example.com"));
        
        Optional<User> found = userRepository.findByEmail("john@example.com");
        
        assertThat(found).isPresent();
        assertThat(found.get().getName()).isEqualTo("John");
    }
}
```

## Integration Tests

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class OrderIntegrationTest {

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    void shouldCreateAndRetrieveOrder() {
        // Create
        OrderRequest request = new OrderRequest(List.of(item1, item2));
        ResponseEntity<Order> createResponse = restTemplate
            .postForEntity("/orders", request, Order.class);
        
        assertThat(createResponse.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        Long orderId = createResponse.getBody().getId();

        // Retrieve
        ResponseEntity<Order> getResponse = restTemplate
            .getForEntity("/orders/" + orderId, Order.class);
        
        assertThat(getResponse.getBody().getItems()).hasSize(2);
    }
}
```

## Testcontainers

```java
@SpringBootTest
@Testcontainers
class PostgresIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
        .withDatabaseName("testdb")
        .withUsername("test")
        .withPassword("test");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    private UserRepository userRepository;

    @Test
    void shouldPersistUser() {
        User saved = userRepository.save(new User("John", "john@example.com"));
        
        assertThat(saved.getId()).isNotNull();
        assertThat(userRepository.findById(saved.getId())).isPresent();
    }
}
```

## Test Configuration

```java
@TestConfiguration
class TestConfig {

    @Bean
    @Primary
    public EmailService mockEmailService() {
        return mock(EmailService.class);
    }
}

@SpringBootTest
@Import(TestConfig.class)
class ServiceTest {
    // Uses mock EmailService
}
```

## Test Properties

```properties
# src/test/resources/application-test.properties
spring.datasource.url=jdbc:h2:mem:testdb
spring.jpa.hibernate.ddl-auto=create-drop
spring.jpa.show-sql=true
```

```java
@SpringBootTest
@ActiveProfiles("test")
class TestWithProfile { }
```
