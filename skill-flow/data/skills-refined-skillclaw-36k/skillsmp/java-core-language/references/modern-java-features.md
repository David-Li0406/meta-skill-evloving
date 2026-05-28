# Modern Java Features

## Records (Java 16+)

```java
// Basic record
public record Point(int x, int y) {}

// Record with validation
public record Email(String value) {
    public Email {
        if (!value.matches("^[\\w.-]+@[\\w.-]+\\.[a-z]{2,}$")) {
            throw new IllegalArgumentException("Invalid email: " + value);
        }
    }
}

// Record with additional methods
public record Range(int start, int end) {
    public Range {
        if (start > end) throw new IllegalArgumentException("start > end");
    }

    public int length() {
        return end - start;
    }

    public boolean contains(int value) {
        return value >= start && value <= end;
    }
}

// Record implementing interface
public record ImmutableUser(String id, String name) implements Identifiable {
    @Override
    public String getId() {
        return id;
    }
}
```

## Sealed Classes (Java 17+)

```java
// Sealed interface with permits
public sealed interface Result<T> permits Success, Failure {
    T getOrThrow();
}

public record Success<T>(T value) implements Result<T> {
    @Override
    public T getOrThrow() {
        return value;
    }
}

public record Failure<T>(Exception error) implements Result<T> {
    @Override
    public T getOrThrow() {
        throw new RuntimeException(error);
    }
}

// Usage with pattern matching
public <T> void handle(Result<T> result) {
    switch (result) {
        case Success<T>(var value) -> process(value);
        case Failure<T>(var error) -> logError(error);
    }
}
```

## Pattern Matching

```java
// Pattern matching for instanceof (Java 16+)
public String format(Object obj) {
    if (obj instanceof String s) {
        return "String: " + s;
    } else if (obj instanceof Integer i) {
        return "Integer: " + i;
    } else if (obj instanceof List<?> list && !list.isEmpty()) {
        return "Non-empty list of size: " + list.size();
    }
    return "Unknown: " + obj;
}

// Pattern matching for switch (Java 21+)
public double area(Shape shape) {
    return switch (shape) {
        case Circle(var r) -> Math.PI * r * r;
        case Rectangle(var w, var h) -> w * h;
        case Triangle(var b, var h) -> 0.5 * b * h;
        case null -> 0.0;
    };
}

// Guarded patterns
public String classify(Integer i) {
    return switch (i) {
        case Integer n when n < 0 -> "negative";
        case Integer n when n == 0 -> "zero";
        case Integer n when n > 0 && n < 10 -> "small positive";
        case Integer n -> "large positive";
    };
}
```

## Text Blocks (Java 15+)

```java
// Multi-line strings
String json = """
    {
        "name": "%s",
        "email": "%s",
        "roles": ["user", "admin"]
    }
    """.formatted(name, email);

// SQL queries
String query = """
    SELECT u.id, u.name, u.email
    FROM users u
    JOIN roles r ON u.role_id = r.id
    WHERE r.name = :roleName
    ORDER BY u.created_at DESC
    """;

// HTML templates
String html = """
    <html>
        <body>
            <h1>Welcome, %s</h1>
        </body>
    </html>
    """.formatted(username);
```

## Virtual Threads (Java 21+)

```java
// Create virtual thread
Thread.startVirtualThread(() -> {
    doBlockingOperation();
});

// Executor with virtual threads
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    List<Future<String>> futures = urls.stream()
        .map(url -> executor.submit(() -> fetchUrl(url)))
        .toList();

    for (Future<String> future : futures) {
        System.out.println(future.get());
    }
}

// Structured concurrency (preview)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<User> user = scope.fork(() -> fetchUser(userId));
    Subtask<List<Order>> orders = scope.fork(() -> fetchOrders(userId));

    scope.join().throwIfFailed();

    return new UserWithOrders(user.get(), orders.get());
}
```
