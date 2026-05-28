# Java Implementation Guidelines

Use when implementing Java code in this project. Java 17+, Gradle Kotlin DSL, Checkstyle `google_checks.xml`.

## Null Check Convention

Use `Objects.isNull/Objects.nonNull` instead of `== null` / `!= null`.

- Avoid:
    ```java
    if (value == null) { ... }
    ```
- Preferred:
    ```java
    if (Objects.isNull(value)) { ... }
    ```

## Comments

- Only Javadoc; no inline/block comments. Public API must have Javadoc.
    ```java
    /**
     * Describe what the API does.
     */
    public void doWork() { ... }
    ```

## Whitespace

Avoid extra blank lines; keep formatting consistent.

## JUnit 5 Assertions

Use `org.junit.jupiter.api.Assertions`; avoid `assertThat`.

- Avoid:
    ```java
    assertThat(actual).isEqualTo(expected);
    ```
- Preferred:
    ```java
    assertEquals(expected, actual);
    ```

## assertAll

- Group related assertions with `assertAll`.
    ```java
    assertAll(
        () -> assertEquals(expected1, actual1),
        () -> assertEquals(expected2, actual2)
    );
    ```

## Comparison Ordering

Put constants/smaller values on the left; prefer `<` / `<=` (reorder instead of using `>` / `>=`).

- Avoid:
    ```java
    if (a > 1) { ... }
    if (d >= c) { ... }
    ```
- Preferred:
    ```java
    if (1 < a) { ... }
    if (0 < d && d <= c) { ... }
    if (b <= c && 0 < d) { ... }
    ```

## this Reference

Use `this.` only to resolve shadowing.

- Shadowed parameter (use `this.`):
    ```java
    public void setName(String name) {
        this.name = name;
    }
    ```
- Not shadowed (no `this.`):
    ```java
    public void setDescription(String value) {
        description = value;
    }
    ```

## Lambda Conciseness

- Single-expression lambdas omit braces/return.
    ```java
    list.stream().map(String::toUpperCase);
    ```

## Records

- Use `record` for immutable carriers; if not, note the reason in Javadoc.
    ```java
    public record User(String id, String name) {
    }
    ```

Record components are exposed via public accessors (e.g., `user.id()`).

## FQN Avoidance

- Avoid fully-qualified names; prefer imports/static imports. Use FQN only to resolve collisions.
    ```java
    import com.example.ClientFactory;
    
    ClientFactory factory = ClientFactory.defaultFactory();
    ```

## Braced Conditionals

- Always use braces on `if/else`, `for`, `while`, `do-while` even for single statements.
    ```java
    if (Objects.nonNull(value)) {
        doSomething();
    }
    ```

## Packages

Keep packages consistent with project namespace.
