# Kotlin Test

Use for Kotlin projects; prefer `kotlin("test")` or Kotest. Load when targeting Kotlin tests.

- Prefer KDoc for helpers; use concise doc comments for shared utilities.
- Group assertions with Kotest (`assertSoftly`/`shouldBe`/matchers).
- For mocking, prefer MockK over Mockito in Kotlin.
- For Reactor/Project Reactor in Kotlin, use `reactor-test` with `StepVerifier`.

### Kotest example
```kotlin
import io.kotest.assertions.assertSoftly
import io.kotest.matchers.shouldBe
import io.kotest.assertions.throwables.shouldThrow
import io.kotest.core.spec.style.StringSpec
import io.mockk.every
import io.mockk.mockk

/**
 * UserService tests using Kotest + MockK.
 */
class UserServiceTest : StringSpec({
    "returns user when id exists" {
        val repo = mockk<UserRepo> {
            every { get("123") } returns User("123", "Alice")
        }
        val svc = UserService(repo)

        val user = svc.getUser("123")

        assertSoftly {
            user.id shouldBe "123"
            user.name shouldBe "Alice"
        }
    }

    "throws when missing" {
        val repo = mockk<UserRepo> {
            every { get("missing") } throws NotFoundException("missing")
        }
        val svc = UserService(repo)

        shouldThrow<NotFoundException> { svc.getUser("missing") }
    }
})
```

### Reactor example with StepVerifier
```kotlin
import org.junit.jupiter.api.DisplayName
import org.junit.jupiter.api.Test
import reactor.core.publisher.Flux
import reactor.test.StepVerifier

/** Reactor tests with StepVerifier. */

class ReactorKotlinTest {
    @Test
    @DisplayName("emits two values and completes")
    fun fluxEmitsValues() {
        val flux = Flux.just("a", "b")

        StepVerifier.create(flux)
            .expectNext("a", "b")
            .verifyComplete()
    }
}
```
