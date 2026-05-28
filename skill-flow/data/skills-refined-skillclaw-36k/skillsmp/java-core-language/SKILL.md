---
name: Java Core Language
description: Java language fundamentals, JVM basics, modern features, and idiomatic patterns.
metadata:
  labels: [java, core, language]
  triggers:
    files: ['**/*.java', 'pom.xml', 'build.gradle', 'build.gradle.kts']
    keywords: [class, interface, record, enum, package, import, extends, implements, throws, sealed, permits]
---

# Java Core Language Standards

## Modern Java Features (17+)

```java
// Records - immutable data carriers
public record User(String id, String name, String email) {
    // Compact constructor for validation
    public User {
        Objects.requireNonNull(id);
        Objects.requireNonNull(name);
    }
}

// Sealed classes - restricted inheritance
public sealed interface Shape permits Circle, Rectangle, Triangle {}
public record Circle(double radius) implements Shape {}
public record Rectangle(double width, double height) implements Shape {}
public final class Triangle implements Shape { /* ... */ }

// Pattern matching for switch (21+)
String describe(Shape shape) {
    return switch (shape) {
        case Circle(var r) -> "Circle with radius " + r;
        case Rectangle(var w, var h) -> "Rectangle " + w + "x" + h;
        case Triangle t -> "Triangle";
    };
}

// Pattern matching for instanceof
if (obj instanceof String s && !s.isBlank()) {
    return s.toUpperCase();
}
```

## Exception Handling

```java
// Custom exception hierarchy
public class DomainException extends RuntimeException {
    private final ErrorCode code;

    public DomainException(ErrorCode code, String message) {
        super(message);
        this.code = code;
    }

    public DomainException(ErrorCode code, String message, Throwable cause) {
        super(message, cause);
        this.code = code;
    }
}

// Try-with-resources
try (var reader = new BufferedReader(new FileReader(path));
     var writer = new BufferedWriter(new FileWriter(output))) {
    reader.lines().map(String::toUpperCase).forEach(writer::write);
} catch (IOException e) {
    throw new DomainException(ErrorCode.IO_ERROR, "File processing failed", e);
}
```

## Generics

```java
// Bounded type parameters
public <T extends Comparable<T>> T max(T a, T b) {
    return a.compareTo(b) > 0 ? a : b;
}

// Wildcards
void processItems(List<? extends Number> items) { /* read-only */ }
void addItems(List<? super Integer> items) { /* write-only */ }

// Generic method with multiple bounds
public <T extends Serializable & Comparable<T>> void process(T item) {}
```

## Null Safety

```java
// Use Optional for return types
public Optional<User> findById(String id) {
    return Optional.ofNullable(repository.get(id));
}

// Never use Optional as parameter or field
// Use @Nullable annotation for nullable parameters
public void process(@Nullable String input) {
    if (input == null) return;
    // ...
}

// Objects utility methods
Objects.requireNonNull(param, "param must not be null");
Objects.requireNonNullElse(value, defaultValue);
```

## Best Practices

1. **Prefer records** for data transfer objects and value objects
2. **Use sealed classes** when you have a fixed set of subtypes
3. **Pattern matching** over instanceof chains and visitor pattern
4. **Immutability by default** - use final fields, unmodifiable collections
5. **Fail fast** - validate at boundaries, throw early
6. **Meaningful exceptions** - include context, use exception chaining

## References

- [Modern Java Features](references/modern-java-features.md) - Records, Sealed Classes, Pattern Matching
- [JVM Memory Model](references/jvm-memory-model.md) - Memory, GC, Performance
