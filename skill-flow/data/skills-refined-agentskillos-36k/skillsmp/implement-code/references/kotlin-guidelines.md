# Kotlin Implementation Guidelines

Use when implementing Kotlin code in this project.

## Packages/Build

- Packages: follow project namespace conventions; keep public API consistent.
- Build: Gradle Kotlin DSL.

## Comments

- KDoc only; avoid inline/block comments for behavior. Public API should have KDoc.
    ```kotlin
    /** Formats a user name into display form. */
    fun formatName(user: User): String = "${'$'}{user.first} ${'$'}{user.last}"
    ```

## Null Checks

- Prefer `===` / `!==` and idiomatic Kotlin null-handling (e.g., `?.`, `?:`, `requireNotNull`).
    ```kotlin
    val name: String? = user.name
    requireNotNull(name) { "name required" }
    ```

## Whitespace

- Avoid extra blank lines; keep formatting consistent.

## Tests

- Prefer Kotest or `kotlin("test")`; group assertions with Kotest `assertSoftly`; avoid `assertThat`.
    ```kotlin
    assertSoftly {
        actual.id shouldBe expectedId
        actual.name shouldBe expectedName
    }
    ```

## Comparisons

- Constant/smaller value on the left; prefer `<` / `<=` and reorder operands instead of using `>` / `>=`.
    ```kotlin
    if (1 < a && a <= b) {
        handle(a)
    }
    ```

## Imports / FQN

- Avoid fully-qualified names—use imports/static imports; FQN only to resolve collisions.
    ```kotlin
    import com.example.ClientFactory
    val factory = ClientFactory.defaultFactory()
    ```

## Control Flow

- `if/else`, `for`, `while`, `do-while`: always use braces, even for single statements.
    ```kotlin
    if (user !== null) {
        process(user)
    }
    ```

## Data Classes

- Use `data class` for immutable carriers; if not, document the reason in KDoc.
    ```kotlin
    data class User(val id: String, val name: String)
    ```
