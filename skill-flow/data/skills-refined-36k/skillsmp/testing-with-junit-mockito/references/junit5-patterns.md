# JUnit 5 Testing Patterns

## Basic Test Structure

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class UserServiceTest {

    private UserService userService;

    @BeforeEach
    void setUp() {
        userService = new UserService();
    }

    @Test
    @DisplayName("Should find user by ID")
    void shouldFindUserById() {
        User user = userService.findById(1L);
        
        assertNotNull(user);
        assertEquals("John", user.getName());
    }

    @Test
    void shouldThrowWhenUserNotFound() {
        assertThrows(UserNotFoundException.class, () -> {
            userService.findById(999L);
        });
    }

    @AfterEach
    void tearDown() {
        // cleanup
    }
}
```

## Parameterized Tests

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;

class ValidationTest {

    @ParameterizedTest
    @ValueSource(strings = {"a@b.com", "test@example.org"})
    void shouldAcceptValidEmails(String email) {
        assertTrue(EmailValidator.isValid(email));
    }

    @ParameterizedTest
    @NullAndEmptySource
    @ValueSource(strings = {"invalid", "@no-local.com"})
    void shouldRejectInvalidEmails(String email) {
        assertFalse(EmailValidator.isValid(email));
    }

    @ParameterizedTest
    @CsvSource({
        "1, 1, 2",
        "2, 3, 5",
        "10, 20, 30"
    })
    void shouldAddNumbers(int a, int b, int expected) {
        assertEquals(expected, Calculator.add(a, b));
    }

    @ParameterizedTest
    @MethodSource("userProvider")
    void shouldValidateUser(User user, boolean expected) {
        assertEquals(expected, UserValidator.isValid(user));
    }

    static Stream<Arguments> userProvider() {
        return Stream.of(
            Arguments.of(new User("John", 25), true),
            Arguments.of(new User("", 25), false),
            Arguments.of(new User("John", -1), false)
        );
    }
}
```

## Nested Tests

```java
@DisplayName("OrderService")
class OrderServiceTest {

    @Nested
    @DisplayName("when creating order")
    class WhenCreatingOrder {

        @Test
        void shouldCreateWithValidItems() { }

        @Test
        void shouldRejectEmptyCart() { }
    }

    @Nested
    @DisplayName("when canceling order")
    class WhenCancelingOrder {

        @Test
        void shouldCancelPendingOrder() { }

        @Test
        void shouldNotCancelShippedOrder() { }
    }
}
```

## Assertions

```java
// Multiple assertions
assertAll("user",
    () -> assertEquals("John", user.getName()),
    () -> assertEquals(25, user.getAge()),
    () -> assertTrue(user.isActive())
);

// Timeout
assertTimeout(Duration.ofSeconds(2), () -> {
    longRunningOperation();
});

// Exception details
var exception = assertThrows(ValidationException.class, () -> {
    service.validate(invalidData);
});
assertEquals("Invalid input", exception.getMessage());
```

## Test Lifecycle

```java
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class ExpensiveResourceTest {

    private Database db;

    @BeforeAll
    void initDatabase() {
        db = new Database();
        db.connect();
    }

    @AfterAll
    void closeDatabase() {
        db.disconnect();
    }
}
```
