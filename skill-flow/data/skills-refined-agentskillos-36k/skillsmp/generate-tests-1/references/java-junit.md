# JUnit (Java)

Use for Java projects; prefer JUnit. Load when targeting Java tests.

- Prefer Javadoc for helper methods/classes in tests; on JDK 23+ you may use markdown style (`///`) doc comments. Use `@DisplayName` for test readability.
- Use `assertAll` for grouped assertions.
- For Reactor projects, prefer `reactor-test` with `StepVerifier` for reactive flows.

```java
import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** In-memory user repository tests. */
class UserServiceTest {

    /** Returns user when id exists. */
    @Test
    @DisplayName("returns user when id exists")
    void getUserReturnsUserWhenIdExists() {
        var svc = new UserService(new InMemoryUserRepo());

        var user = svc.getUser("123");

        assertAll(
            () -> assertEquals("123", user.id()),
            () -> assertEquals("Alice", user.name())
        );
    }

    /** Throws NotFoundException for missing user. */
    @Test
    @DisplayName("throws NotFoundException for missing user")
    void getUserThrowsWhenMissing() {
        var svc = new UserService(new InMemoryUserRepo());

        assertThrows(NotFoundException.class, () -> svc.getUser("missing"));
    }
}
```

### Reactor example (reactor-test)
```java
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import reactor.core.publisher.Flux;
import reactor.test.StepVerifier;

/** Reactor tests with StepVerifier. */
class ReactorTest {
    /** Emits two values and completes. */
    @Test
    @DisplayName("emits two values and completes")
    void fluxEmitsValues() {
        var flux = Flux.just("a", "b");

        StepVerifier.create(flux)
            .expectNext("a", "b")
            .verifyComplete();
    }
}
```
